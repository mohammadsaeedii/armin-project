# Phase 2 — bounded development implementation

Authorized by the researcher's request to start coding on 18 October 2026. This authorization follows the initial Phase 1 hold. It does not establish novelty or authorize a manuscript claim. See the [final evidence update](final_evidence_check.md).

## Scope implemented

The default command builds 200 training, 40 validation and 40 development-evaluation base signals, trains one source-noise CNN for up to five epochs, selects classical settings, evaluates independent development corruptions, and records CPU microbenchmarks. The default wall-time ceiling is five minutes for the run, checked between processing units. Interrupting an individual numerical call is not guaranteed. There is no final-test namespace or main-experiment command.

Signal families are balanced by index: sinusoidal mixtures, linear chirps, three positive Gaussian pulses, and piecewise-constant steps. Features and SHA-256 digests are saved with split IDs. Seeds isolate base signals and corruptions across partitions. Noise is regenerated deterministically; no large dataset download is needed.

Three additive noises are implemented: white Gaussian; AR(1) Gaussian with rho=0.8 and burn-in; Bernoulli–Gaussian impulses with p=0.01 and Gaussian background SD=0.05. Each finite realization is scaled to the requested power SNR, including signal DC. Exact normalization constrains the finite-sequence distribution and is declared in the output. There is no post-corruption clipping or target-derived inference normalization.

Methods: identity, soft universal wavelet shrinkage, local adaptive Wiener, Savitzky–Golay, median, and a fully convolutional residual CNN. Both classical settings and CNN checkpoints use mean per-example validation RMSE in original signal units. The CNN uses training-fitted scalar RMS normalization and MSE training. Initialization starts at the identity map. No per-family inference labels, true test SNR or clean test statistics are supplied to methods.

## Explicit changes from the provisional Phase 1 plan

| Item | Development implementation / reason |
|---|---|
| Main experiment | Deferred; only an independently named development evaluation is available |
| Wavelet SURE | Deferred; universal soft thresholds first, with 12 wavelet/level configurations |
| CNN | Fixed default: 5 convolution layers, 24 hidden channels, kernel 7; exact count recorded by each run |
| Checkpoint selection | Mean per-example validation RMSE, shared with classical tuning; MSE remains the training objective. This avoids differing aggregation criteria for selection |
| Training regimes/seeds | Default is source-only, one seed. Mixed training can be configured explicitly; no six-run sweep is launched |
| Evaluation repetitions | One realization per condition for the short pilot; no claim of sufficient uncertainty coverage |
| Spectral metric | Whole one-sided spectrum relative power error, rather than application-specific signal-band/ridge metrics |
| Pulse recovery | Positive peak within fixed target ROI; missing if below 25% of target peak. This is a provisional diagnostic, not a validated event detector |
| Steps | Jump error from fixed adjacent plateaus and overshoot outside the true local level interval |
| Statistical inference | Per-example paired IDs and descriptive summaries only; cluster bootstrap, seed uncertainty and power analysis deferred |
| Runtime | Same-process CPU microbenchmark with batch 1/32, warmup/repeats; conversion/scaling included and I/O excluded. A repeated white-noise input does not estimate all-condition latency |
| Memory | Entire-process peak RSS only. No unsupported per-method memory comparisons |

Different border rules are recorded in source: symmetric wavelet extension, reflected local/median/CNN padding, mirrored SG. Full-length and fixed boundary/interior errors are reported. A shared 32-sample boundary diagnostic is not proof that every method's entire boundary influence is excluded.

The code is independently implemented from the documented proposal. PTSS1D and other authors' code are not copied or executed. A repository's CPU option is not used as evidence for this project's runtime.

## Reproduce locally

From the project root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m denoising validate-config --config configs/pilot.json
.venv/bin/python -m denoising pilot --config configs/pilot.json --output outputs/pilot-new
```

The lock file records the dependencies used for the verified local run; wheel availability can differ across Python versions/platforms. The CLI sets CPU thread limits before importing numerical libraries and uses CPU tensors only. Existing output directories are refused; choose a new path for each run. A failed/timed-out run has `status: incomplete` and must not be treated as a completed result.

To apply a saved CNN to an existing numeric `.npy` array of shape `[1024]` or `[N, 1024]` (use the checkpoint's length):

```sh
.venv/bin/python -m denoising infer --checkpoint outputs/pilot-new/best.pt --input noisy.npy --output denoised.npy
```

Inference adds no synthetic noise, does not retrain, rejects nonfinite/mismatched arrays, and refuses to overwrite outputs. A checkpoint from a development pilot is not a validated application model.

Outputs include configuration, source hashes, software/platform information, split/feature manifest, noise specifications, classical tuning audit, fitted parameters, training history, best checkpoint, per-example metrics, stratified summaries, clean-input distortion, latency and status. Nonfinite metrics are retained in CSV with valid/nonfinite counts in summaries; they are not silently converted to zero.

## Remaining review decisions

Before a main experiment: approve the narrowed replication/extension framing; finalize generators and feature thresholds; decide whether to add SURE and a diversity-trained control; freeze tuning and selection rules; approve three seeds/repetitions and the total CPU budget; review pilot limitations and seal new final-test data. Real-data validation and manuscript preparation remain separate decisions.

## Verification record

The initial implementation passed 16 invariant tests and completed the default five-epoch CPU pilot. See [measured verification record](phase2_verification.md), including artifact checks, timings and limits. No performance claim is extrapolated from this development run.
