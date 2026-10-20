# Development pilot verification — 18 October 2026

Implementation and a short development run were authorized by the researcher's request to start coding. The main scientific experiment has not been run.

## Executed checks

- `python -m unittest discover -s tests -v`: **16 tests passed**. These cover split reproducibility/separation; exact SNR; noise covariance sanity; invalid input rejection; constant preservation and output shape across classical candidates; identity/perfect reconstruction metrics; gain-error visibility; missed pulses; step fidelity; CNN parameter budget/gradients; checkpoint roundtrip; file inference and overwrite protection; validation isolation; nonfinite counts; main-stage rejection.
- `python -m pip check`: no broken requirements.
- Default configuration validation and Python syntax checks passed.
- All six original research documents remain in the history snapshot, with matching SHA-256 hashes. Original contents are still present in current documents, with added updates and a current-status banner. Current local document links resolve.

## Actual development execution

Command from the project root:

```sh
.venv/bin/python -m denoising pilot --config configs/pilot.json --output outputs/pilot-2026-10-18
```

| Item | Observed value |
|---|---|
| Status | Completed |
| Device | CPU; one PyTorch compute thread |
| Base signals | 200 training / 40 validation / 40 development evaluation |
| CNN | 12,529 trainable parameters; five epochs |
| Training routine elapsed time | 12.21 seconds |
| Entire runner elapsed time | 42.17 seconds; dependency installation and initial module import excluded |
| Evaluation rows | 5,040 = 40 signals × 3 noise processes × 7 levels × 6 methods |
| Timing rows | 12 = 6 methods × 2 batch sizes; 100 repeats after 20 warmups |
| Peak process resident memory | Approximately 426.23 MiB; entire process, not a per-method estimate |

The final artifact audit verified unique split IDs and clean-array hashes, all six expected methods, achieved SNR within 1e-10 dB of the requested values, finite RMSE values, zero identity SNR gain within tolerance, use of development IDs only, checkpoint selection by validation RMSE, and matching source hashes. No test-based model selection was performed. The best epoch was 5, at the pilot's epoch limit; convergence has not been established.

Environment/package versions and source hashes are in [environment.json](../outputs/pilot-2026-10-18/environment.json); installation versions are pinned in [requirements.lock.txt](../requirements.lock.txt). Detailed hardware sysctl access was denied by the local sandbox; processor/RAM identification is therefore incomplete and should be completed before a publishable hardware comparison.

## Outputs and limits

- [Run status](../outputs/pilot-2026-10-18/status.json)
- [Training history](../outputs/pilot-2026-10-18/training_history.csv)
- [Per-example development metrics](../outputs/pilot-2026-10-18/per_example.csv)
- [Stratified descriptive summary](../outputs/pilot-2026-10-18/summary.csv)
- [CPU microbenchmarks](../outputs/pilot-2026-10-18/timing.csv)
- [Clean-input distortion](../outputs/pilot-2026-10-18/clean_input.csv)
- [Best checkpoint](../outputs/pilot-2026-10-18/best.pt)

This is one training seed and one noise repetition with a small development set. No clustered confidence intervals, general method-ranking claim or publication result is justified. The timing includes array conversion/scaling and excludes disk I/O; it uses a repeated white-noise input. Main-experiment seeds, uncertainty analysis, source-versus-mixed comparison and final-test data remain deferred. The literature's novelty assessment remains low confidence.
