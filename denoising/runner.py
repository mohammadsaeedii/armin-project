"""Bounded, auditable CPU development runs; no final-test experiment command."""
import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import resource
import sys
import time
from collections import defaultdict

import numpy as np
import torch

from .classical import candidates, denoise
from .data import make_partition
from .metrics import evaluate
from .model import ResidualCNN, predict
from .noise import NOISE_SPEC, corrupt


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False)+"\n")


def write_csv(path, rows):
    if not rows:
        raise ValueError("Cannot write an empty result table.")
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with Path(path).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def check_deadline(deadline):
    if time.perf_counter() > deadline:
        raise TimeoutError("Pilot time limit reached; this run is incomplete, not a result.")


def validation_pairs(signals, cfg):
    pairs = []
    for index, signal in enumerate(signals):
        for noise in cfg.training_noise:
            for level_index, level in enumerate(cfg.training_snrs):
                noisy = corrupt(signal.clean, noise, level, [cfg.dataset_seed, 202, index, level_index])
                pairs.append((noisy, signal.clean))
    return pairs


def tune_classical(pairs, deadline):
    selected, audit = {}, []
    for method, grid in candidates().items():
        best = float("inf")
        for params in grid:
            check_deadline(deadline)
            start = time.perf_counter()
            score = float(np.mean([np.sqrt(np.mean((denoise(y, method, params)-x)**2)) for y, x in pairs]))
            audit.append({"method": method, "parameters": json.dumps(params, sort_keys=True), "validation_rmse": score, "seconds": time.perf_counter()-start})
            if score < best:
                best, selected[method] = score, params
    return selected, audit


def train_model(signals, pairs, cfg, output, deadline):
    torch.manual_seed(cfg.model_seed)
    torch.use_deterministic_algorithms(True)
    model = ResidualCNN(cfg.channels, cfg.layers, cfg.kernel_size).cpu()
    parameter_count = sum(p.numel() for p in model.parameters())
    if parameter_count >= 50000:
        raise ValueError("Architecture exceeds the pilot's 50,000 parameter cap.")
    # One scalar fitted only to training targets. No per-test clean statistics.
    scale = float(np.sqrt(np.mean([np.mean(s.clean**2) for s in signals])))
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.learning_rate)
    x_val = torch.tensor(np.stack([x for _, x in pairs])/scale, dtype=torch.float32).unsqueeze(1)
    y_val = torch.tensor(np.stack([y for y, _ in pairs])/scale, dtype=torch.float32).unsqueeze(1)
    history, best, bad_epochs = [], float("inf"), 0
    started = time.perf_counter()
    for epoch in range(cfg.epochs):
        check_deadline(deadline)
        rng = np.random.default_rng([cfg.dataset_seed, 101, epoch])
        conditions = [(noise, snr) for noise in cfg.training_noise for snr in cfg.training_snrs]
        labels = np.arange(len(signals)) % len(conditions)
        rng.shuffle(labels)
        ys = []
        for i, signal in enumerate(signals):
            noise, snr = conditions[labels[i]]
            ys.append(corrupt(signal.clean, noise, snr, [cfg.dataset_seed, 101, epoch, i]))
        x = torch.tensor(np.stack([s.clean for s in signals])/scale, dtype=torch.float32).unsqueeze(1)
        y = torch.tensor(np.stack(ys)/scale, dtype=torch.float32).unsqueeze(1)
        model.train()
        total = 0.0
        order = rng.permutation(len(signals))
        for offset in range(0, len(order), cfg.batch_size):
            check_deadline(deadline)
            ids = order[offset:offset+cfg.batch_size]
            optimizer.zero_grad(set_to_none=True)
            loss = torch.mean((model(y[ids])-x[ids])**2)
            if not torch.isfinite(loss):
                raise RuntimeError("Nonfinite training loss.")
            loss.backward()
            optimizer.step()
            total += float(loss.detach())*len(ids)
        model.eval()
        squared_error, rmse_sum = 0.0, 0.0
        with torch.inference_mode():
            for offset in range(0, len(pairs), cfg.batch_size):
                check_deadline(deadline)
                sl = slice(offset, offset+cfg.batch_size)
                error_squared = (model(y_val[sl])-x_val[sl])**2
                squared_error += float(torch.sum(error_squared))
                rmse_sum += float(torch.sqrt(error_squared.mean(dim=(1, 2))).sum())*scale
        val_loss = squared_error/x_val.numel()
        val_rmse = rmse_sum/len(pairs)
        history.append({"epoch": epoch+1, "train_normalized_mse": total/len(signals), "validation_normalized_mse": val_loss, "validation_rmse": val_rmse})
        write_csv(output/"training_history.csv", history)
        if val_rmse < best:
            best, bad_epochs = val_rmse, 0
            torch.save({"state_dict": model.state_dict(), "scale": scale, "config": cfg.to_dict(), "best_epoch": epoch+1, "parameter_count": parameter_count}, output/"best.pt")
        else:
            bad_epochs += 1
        print(f"epoch {epoch+1}/{cfg.epochs}: validation RMSE={val_rmse:.6g}", flush=True)
        if bad_epochs >= cfg.patience:
            break
    checkpoint = torch.load(output/"best.pt", map_location="cpu", weights_only=True)
    model.load_state_dict(checkpoint["state_dict"])
    return model, scale, {"seconds": time.perf_counter()-started, "epochs_completed": len(history), "best_epoch": checkpoint["best_epoch"], "parameters": parameter_count, "training_scale": scale}


def evaluate_development(signals, cfg, settings, model, scale, deadline):
    rows, clean_rows = [], []
    for index, signal in enumerate(signals):
        check_deadline(deadline)
        for noise in cfg.evaluation_noise:
            for level_index, level in enumerate(cfg.evaluation_snrs):
                for repetition in range(cfg.noise_repetitions):
                    y = corrupt(signal.clean, noise, level, [cfg.dataset_seed, 303, index, level_index, repetition])
                    outputs = {name: denoise(y, name, params) for name, params in settings.items()}
                    outputs["cnn"] = predict(model, y, scale)
                    for method, z in outputs.items():
                        row = {"signal_id": signal.identity, "family": signal.family, "noise": noise, "nominal_snr_db": level, "repetition": repetition, "method": method, "model_seed": cfg.model_seed}
                        row.update(evaluate(signal.clean, y, z, signal.features, cfg.boundary_width))
                        rows.append(row)
        for method in [*settings, "cnn"]:
            z = predict(model, signal.clean, scale) if method == "cnn" else denoise(signal.clean, method, settings[method])
            clean_rows.append({"signal_id": signal.identity, "family": signal.family, "method": method, "clean_input_rmse": float(np.sqrt(np.mean((z-signal.clean)**2)))})
    return rows, clean_rows


def summarize(rows):
    groups = defaultdict(list)
    keys = ("method", "family", "noise", "nominal_snr_db")
    metric_names = [k for k in rows[0] if k not in (*keys, "signal_id", "repetition", "model_seed")]
    metric_names += ["pulse_amplitude_mae", "pulse_timing_mae_samples", "pulse_miss_rate", "step_jump_mae", "step_overshoot"]
    identity = {(r["signal_id"], r["noise"], r["nominal_snr_db"], r["repetition"]): r["rmse"] for r in rows if r["method"] == "identity"}
    for row in rows:
        groups[tuple(row[k] for k in keys)].append(row)
    result = []
    for key, members in groups.items():
        row = dict(zip(keys, key))
        row["n"] = len(members)
        for metric in dict.fromkeys(metric_names):
            values = np.array([m[metric] for m in members if metric in m], dtype=float)
            finite = values[np.isfinite(values)]
            row[metric+"_applicable_n"] = len(values)
            row[metric+"_mean"] = float(np.mean(finite)) if len(finite) else float("nan")
            row[metric+"_finite_n"] = len(finite)
            row[metric+"_nonfinite_n"] = int(np.sum(~np.isfinite(values)))
        row["paired_rmse_minus_identity"] = float(np.mean([m["rmse"]-identity[(m["signal_id"], m["noise"], m["nominal_snr_db"], m["repetition"])] for m in members]))
        result.append(row)
    return result


def time_methods(cfg, settings, model, scale, signal, deadline):
    y = corrupt(signal.clean, "white", 5, [cfg.dataset_seed, 404])
    rows = []
    for batch_size in (1, 32):
        batch = np.repeat(y[None, :], batch_size, axis=0)
        for method in [*settings, "cnn"]:
            def call():
                if method == "cnn":
                    return predict(model, batch, scale)
                return np.stack([denoise(item, method, settings[method]) for item in batch])
            for _ in range(cfg.timing_warmup):
                check_deadline(deadline)
                call()
            durations = []
            for _ in range(cfg.timing_repeats):
                check_deadline(deadline)
                start = time.perf_counter_ns()
                call()
                durations.append((time.perf_counter_ns()-start)/1e6)
            p25, median, p75, p95 = np.percentile(durations, [25, 50, 75, 95])
            rows.append({"method": method, "batch_size": batch_size, "length": cfg.length, "median_ms": median, "iqr_ms": p75-p25, "p95_ms": p95, "signals_per_second": batch_size*1000/median, "repeats": cfg.timing_repeats})
    return rows


def run_pilot(cfg, output):
    cfg.validate()
    output = Path(output)
    # Refuse even empty existing directories, avoiding accidental reuse of an old run.
    output.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    deadline = start + cfg.runtime_limit_seconds
    write_json(output/"config.json", cfg.to_dict())
    write_json(output/"status.json", {"status": "running", "stage": cfg.stage})
    try:
        torch.set_num_threads(cfg.threads)
        torch.set_num_interop_threads(1)
        versions = {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "PyWavelets", "torch")}
        code_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob("*.py")}
        write_json(output/"environment.json", {"python": sys.version, "platform": platform.platform(), "machine": platform.machine(), "processor": platform.processor(), "logical_cpu_count": os.cpu_count(), "device": "cpu", "torch_threads": torch.get_num_threads(), "packages": versions, "code_sha256": code_hashes, "thread_env": {name: os.environ.get(name) for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")}})
        write_json(output/"noise_spec.json", NOISE_SPEC)
        partitions = {name: make_partition(cfg.dataset_seed, name, count, cfg.length) for name, count in (("train", cfg.train_count), ("validation", cfg.validation_count), ("development_evaluation", cfg.evaluation_count))}
        write_json(output/"split_manifest.json", {name: [{"id": s.identity, "family": s.family, "clean_sha256": hashlib.sha256(s.clean.tobytes()).hexdigest(), "features": s.features} for s in signals] for name, signals in partitions.items()})
        pairs = validation_pairs(partitions["validation"], cfg)
        print("Selecting classical settings using source validation only...", flush=True)
        settings, audit = tune_classical(pairs, deadline)
        write_json(output/"classical_settings.json", settings)
        write_csv(output/"classical_tuning.csv", audit)
        print("Training compact CNN on CPU...", flush=True)
        model, scale, training = train_model(partitions["train"], pairs, cfg, output, deadline)
        write_json(output/"training_summary.json", training)
        print("Evaluating development signals only...", flush=True)
        rows, clean_rows = evaluate_development(partitions["development_evaluation"], cfg, settings, model, scale, deadline)
        write_csv(output/"per_example.csv", rows)
        write_csv(output/"summary.csv", summarize(rows))
        write_csv(output/"clean_input.csv", clean_rows)
        print("Measuring CPU latency and throughput...", flush=True)
        write_csv(output/"timing.csv", time_methods(cfg, settings, model, scale, partitions["development_evaluation"][0], deadline))
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        peak_bytes = int(rss if sys.platform == "darwin" else rss*1024)
        summary = {"status": "completed", "stage": cfg.stage, "elapsed_seconds": time.perf_counter()-start, "per_example_rows": len(rows), "peak_process_rss_bytes": peak_bytes, "memory_scope": "entire process high-water mark; not per-method memory", "conclusion": "Development feasibility only; no final-test or novelty claim."}
        write_json(output/"status.json", summary)
        (output/"README.md").write_text("# Development pilot only\n\nThis run is not a final experiment. See config.json and status.json.\n\nClassical settings and CNN checkpoints both use mean per-example source-validation RMSE. CNN training uses MSE.\nTiming includes array conversion, training-fitted scaling and output restoration, excludes disk I/O, and uses one repeated white-noise input. It is a local microbenchmark, not a noise-dependent latency claim.\n\nPer-example metrics retain paired signal IDs. Summary averages exclude nonfinite values and report their counts; no confidence intervals or significance claims are produced by this pilot. Clean-input error is reported separately. Peak RSS is process-wide, not a method comparison.\n")
        print(json.dumps(summary, indent=2), flush=True)
        return summary
    except Exception as exc:
        write_json(output/"status.json", {"status": "incomplete", "stage": cfg.stage, "error": str(exc), "elapsed_seconds": time.perf_counter()-start})
        raise
