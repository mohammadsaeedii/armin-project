"""Scientific invariants and failure behavior, not numerical performance claims."""
import tempfile
import unittest
from pathlib import Path

import numpy as np
import torch

from denoising.classical import candidates, denoise
from denoising.config import Config
from denoising.data import FAMILIES, make_partition, make_signal
from denoising.metrics import evaluate, snr
from denoising.model import ResidualCNN, predict
from denoising.inference import infer_file
from denoising.noise import corrupt
from denoising.runner import run_pilot, summarize, validation_pairs

torch.set_num_threads(1)


class ScientificIntegrityTests(unittest.TestCase):
    def test_independent_and_reproducible_partitions(self):
        a = make_partition(91, "train", 12, 256)
        b = make_partition(91, "validation", 12, 256)
        again = make_partition(91, "train", 12, 256)
        self.assertEqual(set(s.family for s in a), set(FAMILIES))
        self.assertFalse(set(s.identity for s in a) & set(s.identity for s in b))
        self.assertFalse({s.clean.tobytes() for s in a} & {s.clean.tobytes() for s in b})
        for x, y in zip(a, again):
            np.testing.assert_array_equal(x.clean, y.clean)
        with self.assertRaises(KeyError):
            make_signal(1, "final_test", 0, 256)

    def test_exact_snr_all_noise_types_and_levels(self):
        x = make_signal(1, "train", 2, 1024).clean
        for noise in ("white", "colored", "impulsive"):
            for level in (-5, 0, 2.5, 5, 10, 15):
                with self.subTest(noise=noise, level=level):
                    y = corrupt(x, noise, level, [4, 5])
                    self.assertAlmostEqual(snr(x, y-x), level, places=10)
                    np.testing.assert_array_equal(y, corrupt(x, noise, level, [4, 5]))

    def test_noise_realizations_and_covariance(self):
        x = np.ones(8192)
        white = corrupt(x, "white", 5, [123])-x
        colored = corrupt(x, "colored", 5, [123])-x
        self.assertLess(abs(np.corrcoef(white[:-1], white[1:])[0, 1]), 0.08)
        self.assertGreater(np.corrcoef(colored[:-1], colored[1:])[0, 1], 0.70)
        self.assertFalse(np.array_equal(white, corrupt(x, "white", 5, [124])-x))

    def test_invalid_inputs_fail_explicitly(self):
        with self.assertRaises(ValueError):
            corrupt(np.zeros(64), "white", 0, [1])
        with self.assertRaises(ValueError):
            corrupt(np.ones(64), "white", float("nan"), [1])
        with self.assertRaises(ValueError):
            evaluate(np.ones(64), np.ones(64), np.zeros(63), {}, 4)

    def test_all_classical_candidates_preserve_shape_and_constants(self):
        x = np.ones(257)*3.25
        for method, grid in candidates().items():
            for settings in grid:
                z = denoise(x, method, settings)
                self.assertEqual(z.shape, x.shape)
                self.assertTrue(np.isfinite(z).all())
                np.testing.assert_allclose(z, x, atol=1e-9)

    def test_identity_and_perfect_metrics(self):
        signal = make_signal(5, "validation", 0, 256)
        y = corrupt(signal.clean, "white", 5, [45])
        identity = evaluate(signal.clean, y, y, {}, 16)
        self.assertAlmostEqual(identity["snr_improvement_db"], 0, places=12)
        perfect = evaluate(signal.clean, y, signal.clean, {}, 16)
        self.assertEqual(perfect["rmse"], 0)
        self.assertTrue(np.isinf(perfect["output_snr_db"]))
        self.assertAlmostEqual(perfect["correlation"], 1)

    def test_gain_errors_not_hidden_by_correlation(self):
        x = make_signal(5, "validation", 0, 256).clean
        result = evaluate(x, x, 2*x, {}, 16)
        self.assertAlmostEqual(result["correlation"], 1)
        self.assertGreater(result["rmse"], 0)

    def test_pulse_metrics_count_missing_events(self):
        s = make_signal(8, "validation", 2, 1024)
        perfect = evaluate(s.clean, s.clean, s.clean, s.features, 32)
        self.assertEqual(perfect["pulse_timing_mae_samples"], 0)
        self.assertEqual(perfect["pulse_amplitude_mae"], 0)
        missing = evaluate(s.clean, s.clean, np.zeros_like(s.clean), s.features, 32)
        self.assertEqual(missing["pulse_miss_rate"], 1)
        self.assertTrue(np.isnan(missing["correlation"]))
        self.assertGreater(missing["pulse_amplitude_mae"], 0)

    def test_step_features_perfect_and_erased(self):
        s = make_signal(9, "validation", 3, 1024)
        perfect = evaluate(s.clean, s.clean, s.clean, s.features, 32)
        self.assertEqual(perfect["step_jump_mae"], 0)
        self.assertEqual(perfect["step_overshoot"], 0)
        erased = evaluate(s.clean, s.clean, np.zeros_like(s.clean), s.features, 32)
        self.assertGreater(erased["step_jump_mae"], 0)

    def test_cnn_shape_budget_and_training_gradients(self):
        torch.manual_seed(41)
        model = ResidualCNN()
        self.assertLess(sum(p.numel() for p in model.parameters()), 50000)
        y = torch.randn(2, 1, 257)
        np.testing.assert_array_equal(model(y).detach().numpy(), y.numpy())
        torch.mean(model(y)**2).backward()
        self.assertTrue(torch.isfinite(model.network[-1].weight.grad).all())
        self.assertGreater(float(model.network[-1].weight.grad.abs().sum()), 0)

    def test_checkpoint_roundtrip(self):
        model = ResidualCNN(channels=8, layers=3)
        with torch.no_grad():
            model.network[-1].weight.fill_(0.01)
        x = np.random.default_rng(20).normal(size=(2, 256))
        before = predict(model, x, 1.7)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"state.pt"
            torch.save(model.state_dict(), path)
            recovered = ResidualCNN(channels=8, layers=3)
            recovered.load_state_dict(torch.load(path, weights_only=True, map_location="cpu"))
            np.testing.assert_array_equal(before, predict(recovered, x, 1.7))

    def test_validation_uses_only_declared_source_conditions(self):
        cfg = Config(length=256, train_count=4, validation_count=4, evaluation_count=4)
        partition = make_partition(cfg.dataset_seed, "validation", 4, 256)
        pairs = validation_pairs(partition, cfg)
        self.assertEqual(len(pairs), 12)
        for i, (y, x) in enumerate(pairs):
            self.assertAlmostEqual(snr(x, y-x), cfg.training_snrs[i % 3], places=10)
        cfg.evaluation_noise = ["impulsive"]
        cfg.evaluation_snrs = [-5]
        for (a, _), (b, _) in zip(pairs, validation_pairs(partition, cfg)):
            np.testing.assert_array_equal(a, b)

    def test_file_inference_and_output_protection(self):
        cfg = Config(length=256, channels=8, layers=3)
        model = ResidualCNN(8, 3)
        x = np.random.default_rng(8).normal(size=(3, 256))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            torch.save({"config": cfg.to_dict(), "scale": 1.5, "state_dict": model.state_dict()}, root/"model.pt")
            np.save(root/"input.npy", x)
            infer_file(root/"model.pt", root/"input.npy", root/"out.npy", 2)
            np.testing.assert_allclose(np.load(root/"out.npy"), x, atol=2e-7)
            with self.assertRaises(FileExistsError):
                infer_file(root/"model.pt", root/"input.npy", root/"out.npy", 2)

    def test_summary_preserves_nonfinite_counts(self):
        row = {"signal_id": "a", "family": "pulses", "noise": "white", "nominal_snr_db": 0, "repetition": 0, "method": "identity", "model_seed": 1, "rmse": 1.0, "correlation": float("nan")}
        summary = summarize([row])[0]
        self.assertEqual(summary["correlation_finite_n"], 0)
        self.assertEqual(summary["correlation_nonfinite_n"], 1)
        self.assertEqual(summary["paired_rmse_minus_identity"], 0)

    def test_existing_run_directory_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            sentinel = Path(tmp)/"keep.txt"
            sentinel.write_text("original")
            with self.assertRaises(FileExistsError):
                run_pilot(Config(), tmp)
            self.assertEqual(sentinel.read_text(), "original")

    def test_main_stage_and_bad_configs_rejected(self):
        for cfg in (Config(stage="main"), Config(train_count=5), Config(training_noise=[]), Config(training_snrs=[float("nan")]), Config(kernel_size=4), Config(runtime_limit_seconds=0)):
            with self.assertRaises(ValueError):
                cfg.validate()


if __name__ == "__main__":
    unittest.main()
