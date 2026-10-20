# Phase 1 report — 1D signal denoising

**Date:** 17 October 2026. **Status:** complete for researcher review. No denoising implementation, training, generated datasets or experimental results. Phase 2 requires approval.

## Conclusion and recommendation

The proposed question is relevant, but **this review does not establish a novel research gap**. Unseen-noise evaluation, detail preservation, lightweight models and computational comparisons all have precedents. The strongest remaining candidate is a tightly controlled, openly reproducible comparison that separates noise-process shift from noise-level shift, freezes model selection to declared source conditions, measures feature errors, and runs every method on the same CPU.

**Interpretation:** scientific usefulness is **medium confidence**; distinct publishable novelty is **low confidence**. Approve only a bounded feasibility pilot if this benchmark/replication framing is acceptable. Do not begin a full paper or advertise a novel CNN. Prior art may require a narrower application or a replication contribution.

The directory was inspected before changes and was empty. The six requested documents and 15 public Crossref metadata snapshots form the research record. Nothing pre-existing was overwritten. This is a focused scoping review, not an exhaustive systematic review.

## Verified evidence and closest precedents

“Verified” below means supported by identified primary or bibliographic sources, not independently reproduced. Full metadata and evidence-access levels are in the [literature matrix](literature_matrix.md); gaps and counter-evidence are in the [gap assessment](research_gap.md).

| Verified fact | Implication for our proposal — interpretation |
|---|---|
| Wang et al. explicitly examine ECG denoiser transfer to unseen noise/data. The chapter's citation year is 2024 although it appeared online in November 2023. [C5](https://doi.org/10.1007/978-981-99-8388-9_40) | “First comparison under unseen noise” is not defensible. Full methods remain necessary to compare protocols. |
| Yang et al. use leave-one-noise-domain-out motor-acoustic evaluation with classical and learned comparators. [C10](https://doi.org/10.3390/s26144489) | Noise-domain holdout is already explicit in recent 1D research. Our possible distinction is a controlled stochastic-process/SNR factorial. |
| Bai et al. combine white/pink-noise synthetic RTS experiments, classical/neural processing, structural outcomes, runtime and memory. [C9](https://doi.org/10.1038/s41598-026-36656-2) | The combined benchmark concept already exists. Separate denoising from digitization and declare the neural training distribution. |
| Qiu et al. report a compact ECG U-Net; Shaheen et al. examine reconstruction, morphology and resources. [C4](https://doi.org/10.1088/1361-6579/ac96cd), [C7](https://doi.org/10.3390/s25030801) | A small CNN is a reasonable comparator. Parameter count alone does not establish CPU training feasibility. |
| EEGdenoiseNet provides a controlled semi-synthetic benchmark. Qian et al. use application-specific synthetic ultrasonic noise. [C3](https://doi.org/10.1088/1741-2552/ac2bf8), [C8](https://doi.org/10.1016/j.ultras.2026.108054) | Synthetic evaluation is justified, but a new generator is not itself a research gap. |

Foundational sources establish wavelet shrinkage, Wiener filtering and polynomial smoothing; they do not imply equal suitability for every signal/noise pair. SG has documented stopband and boundary limitations, with a later supporting-code correction. [F1](https://mitpress.mit.edu/9780262730051/extrapolation-interpolation-and-smoothing-of-stationary-time-series/), [F2](https://doi.org/10.1021/ac60214a047), [F3](https://doi.org/10.1093/biomet/81.3.425), [F4](https://doi.org/10.1109/18.382009), [F5](https://doi.org/10.1021/acsmeasuresciau.1c00054), [F6](https://doi.org/10.1021/acsmeasuresciau.3c00017)

Adjacent image research already tests out-of-range noise and architectural effects on robustness. A recent ECG preprint also includes unseen levels and edge deployment; it is not counted as verified peer-reviewed evidence. [A1](https://openreview.net/pdf/ae5ecd6a31912546f2851cd3d1034a3537b633b8.pdf), [P1](https://arxiv.org/abs/2511.12478)

## Proposed research question and evidential limits

**Proposal, not a result:** For independent analytic signals from a fixed family distribution, how do rankings of source-tuned classical denoisers and one compact 1D CNN change under noise-process and noise-level shifts? Are those rankings consistent for aggregate reconstruction, local details and measured CPU cost?

The primary comparison estimates performance under specified shifts. It does not establish that all CNNs behave similarly, prove a causal penalty relative to an optimally adapted target model, or demonstrate clinical/industrial utility. No improvement, ranking reversal or training duration is predicted as a finding.

Useful results could include reproducible crossover conditions, a difference between RMSE and feature fidelity, or a quality–cost tradeoff. Null results are valid. A synthetic-only paper may be less convincing to an application journal; a later real-data extension should be a separate decision.

## Provisional experiment for approval

Every choice below is a **proposed design**, not an implemented or finalized protocol. Numerical budgets are planning limits, not measured feasibility claims. Revisit them after an approved pilot without consulting the final test set.

### Signals and partitions

- Start with length **1,024 samples** and four families: sinusoidal mixtures, chirps, sparse smooth pulses, and piecewise smooth/constant signals with jumps. Specify parameter distributions, minimum feature widths, frequency bounds below Nyquist, amplitude ranges and boundary behavior before generating data.
- Propose **2,000 training, 400 validation and 400 test base signals**, balanced by family. Independently sample parameters within the same family distribution. Hold out entire base-signal identities before generating any noise or augmented copies; all copies of one clean signal remain in its partition.
- Use independent random streams for clean parameters, noise and model initialization. Prevent overlapping segments, duplicated waveforms and shared noise records across partitions. Save seeds and partition manifests.
- Fixed canonical wavelet-test functions may be illustrative diagnostics only. Do not treat repeated noise on one fixed shape as many independent clean test signals.
- Do not combine clean-family shift with the primary noise-shift experiment. A held-out clean family would answer a separate question.

Analytic targets allow exact feature annotation but simplify real acquisition. The families are stress tests, not validated surrogates for ECG, EEG, ultrasound or motor acoustics.

### Noise and SNR conditions

| Factor | Proposed values | Interpretation |
|---|---|---|
| Source noise | Additive white Gaussian | Source-only training and validation |
| Test noise | White Gaussian; stationary AR(1) Gaussian with provisional correlation coefficient 0.8; sparse Bernoulli–Gaussian impulses with provisional occurrence probability 0.01 and a small Gaussian background | The latter two processes are absent from source-only training/selection |
| Training/validation levels | 0, 5, 10 dB | Discrete, balanced source support |
| Matched test levels | 0, 5, 10 dB | Independent signals/noise at seen levels |
| Interpolation levels | 2.5, 7.5 dB | Unseen values inside training range |
| Extrapolation levels | −5, +15 dB | Outside training support, in both directions |
| Test noise repetitions | Three independent realizations per base signal and condition | Repeated measures, not independent clean-signal samples |

Colored and impulsive components are justified as abstract stressors by existing controlled-noise applications, including C8 and C9. The precise AR(1)/impulse parameters are our proposed choices, not values validated by those papers. [C8](https://doi.org/10.1016/j.ultras.2026.108054), [C9](https://doi.org/10.1038/s41598-026-36656-2)

Define input SNR consistently as `10 log10(sum(x²)/sum(n²))`. For a nonzero raw noise draw `n0`, scale it by `||x||₂ / ||n0||₂ × 10^(−SNR/20)`, then set `y = x + n`. Signal energy includes DC unless the generator explicitly defines zero-mean signals. Reject zero-energy cases under a declared rule. This per-realization power normalization slightly constrains the finite-sample noise distribution; apply it consistently and describe it accurately.

For AR(1), use a stationary initialization or declared burn-in. Define impulse/background variance before scaling; keep the same parameters across partitions. No undocumented clipping or filtering after noise scaling. Save achieved SNR checks. A sensitivity sweep over correlation/impulse rate is optional and should not expand the first pilot.

At equal power, colored Gaussian noise changes temporal covariance, while impulses change tail behavior. Do not call every nonwhite process “non-Gaussian.” Record process and level effects separately, including their interaction.

The proposed test set contains **400 × 3 × 7 × 3 = 25,200 noisy sequences**. Stream or batch these; storing float32 clean/noisy pairs without sharing clean arrays is about **206 MB decimal**, a storage calculation only. The final test set stays sealed during implementation and model selection.

### Methods and equal information access

| Method | Proposed specification / reason |
|---|---|
| Identity/no processing | Mandatory reference for both improvement and clean-signal distortion |
| Wavelet thresholding | Decimated DWT with soft thresholding; universal and level-dependent SURE candidates if implemented correctly; declare wavelets, levels, extension mode and noisy-input scale estimator |
| Local adaptive Wiener filter | Window and input-based noise-variance estimation declared; not an oracle spectral Wiener filter supplied with clean power spectra |
| Savitzky–Golay | Validation-selected odd window and polynomial order; explicit boundary handling; consult F5/F6 before relying on supporting code |
| Median filter | Small, inexpensive robust comparator so impulsive tests do not rely only on Gaussian-oriented baselines |
| One compact 1D CNN | Fully convolutional residual denoiser, approximately 4–6 layers and 16–32 channels; provisional target below 50,000 trainable parameters; avoid flattening to a large dense head |

The CNN is an existing model class chosen for manageable capacity, not a proposed novel architecture. Use one fixed architecture and MSE objective initially. Exact kernel sizes, receptive field and parameter count must be checked in the approved implementation. Do not assume the ECG model's reported size or accuracy transfers to our signals. [C1](https://doi.org/10.1109/ACCESS.2019.2912036), [C4](https://doi.org/10.1088/1361-6579/ac96cd)

Select classical settings on the same source validation data available to the CNN, using a declared aggregate reconstruction criterion. Freeze settings before test. Predeclare finite grids, initially capped at roughly 12 configurations per classical method, and report actual tuning cost. Equal validation access is essential; equal candidate counts do not imply equal computational effort.

Allow explicitly declared adaptation from the noisy observation, such as variance estimation. Do not give any method test targets, true test noise, true SNR, clean normalization factors or family labels at inference. Fixed normalization may use training statistics; per-input scaling must depend only on the noisy input and be reversed consistently. Targets are available only for training, validation selection and evaluation.

Use global settings for the main benchmark. Per-family or oracle-parameter results, if later requested, must be clearly separate sensitivity bounds. Handle padding consistently and document unavoidable algorithm differences. Report full-length error and a predetermined interior-versus-boundary breakdown; do not crop away failures selectively.

### Training regimes and manageable budget

The main arm uses only white-Gaussian source training/validation. A recommended **diversity-trained control** uses all three processes at the same three levels with the same number of training pairs/updates, architecture and selection budget. Retune classical methods on the corresponding mixed validation conditions for this control. Colored/impulsive tests are no longer unseen types for the mixed arm.

Propose three initialization seeds per neural regime: six runs total. Initially cap at 30 epochs, early stopping after five non-improving validation epochs, batch size 32, and about 2,000 balanced training pairs per epoch. Fix optimizer and selection rules before the definitive experiment. Save validation-selected checkpoints, training curves and failures. Do not choose the best seed on test data.

Changing training diversity is a controlled intervention but not a complete target-adaptation experiment. Avoid calling the source-versus-mixed difference a pure mismatch penalty. A target-specific training arm would require additional runs and separate approval.

**Proposed pilot:** use a separate development subset of about 200 training/40 validation signals, one seed, five epochs, and development-only noise checks. Measure CPU time/memory and confirm transformations, information access and metrics. Do not inspect the final test set or publish pilot scores as evidence. Suggested feasibility gate: projected training no more than one CPU hour per complete run and six CPU hours across six runs, excluding classical tuning/evaluation. These limits need user approval and are not promises. If exceeded, reduce sample count/channel width once using development evidence and document the revision before locking the protocol.

### Metrics and statistical comparison

| Outcome | Proposed measure and interpretation |
|---|---|
| Primary reconstruction | RMSE per signal and condition; avoid pooling raw amplitudes across families without showing stratified results |
| Familiar signal metric | Output SNR `10 log10(sum(x²)/sum((x−xhat)²))`; improvement = output minus achieved input SNR |
| Shape agreement | Pearson correlation, with undefined constant/zero-variance cases flagged rather than silently assigned zero |
| Pulse fidelity | Peak amplitude error, peak-time error and missed-event rate using fixed clean-target regions and a declared matching/detection rule |
| Step fidelity | Jump-amplitude error and overshoot/undershoot in predetermined neighborhoods around true transitions |
| Oscillatory fidelity | Relative spectral-power error over declared signal bands; optional frequency/ridge error only if reliably defined |
| Boundaries / clean input | Whole-signal versus predefined boundary/interior scores; identity-input distortion on clean held-out signals |
| Cost | CPU training, validation/tuning and inference time; peak resident memory; parameters and serialized model size |

RMSE and output SNR are mathematically linked for fixed signal energy; they are not independent confirmations. Correlation can ignore gain errors. Feature metrics address a different question, but definitions and tolerances must be fixed before test. Use ground-truth feature annotations only in evaluation; apply identical rules to all methods. Missing peaks must count as failures, not be dropped. Report undefined relative errors for near-zero denominators under a predeclared rule.

Compare methods on the **same** clean/noisy test instances. Report per-family, per-process and per-level summaries and paired differences, plus a predeclared overall average with equal condition weighting. Keep interpolation, extrapolation and type shifts identifiable. Bootstrap at the base-signal level so all its noise repetitions remain together; also report variability across training seeds. Three seeds give only a limited estimate of optimization variability, not a guarantee of statistical power.

Prefer effect sizes and interval estimates over a large collection of uncorrected significance tests. Designate RMSE and a small family-specific feature set as primary; label remaining analyses exploratory. A later power/sensitivity calculation can use pilot variability without examining the final test outcomes.

### CPU timing and reproducibility

Disable GPU/MPS for the primary comparison. Record Mac/CPU model, core/thread count, RAM, OS, framework/library versions and numeric precision. Measure all methods on the same machine, with one CPU thread as the primary reproducible setting; optionally add a documented multicore setting separately.

Report batch-one latency and moderate-batch throughput (initially batch 32) for length 1,024. Warm up each implementation, then collect repeated timings, initially at least 100 calls after 20 warmups, increasing work if timer granularity dominates. Report median, spread and p95. Keep machine load and run ordering controlled. Distinguish core inference from end-to-end preprocessing/inverse scaling, and exclude disk I/O from core timing. Report training and hyperparameter-search cost separately; do not hide these inside a single “fast” label.

Operation counts for a fixed feed-forward CNN ordinarily do not vary with input noise. The meaningful efficiency question is quality at a given cost, rather than an assumed latency penalty caused by mismatch. Adaptive algorithms can be checked for data-dependent timing.

After approval, preserve generator specifications, seeds, split IDs, tuning grids, fitted settings, raw per-example metrics, timings, version/environment files and commands. No repository executability or CPU performance has been validated in Phase 1. Licensing and source-code correctness must be checked before reuse.

## Unresolved questions and search limits

1. **Prior-art completeness:** native Google Scholar/Scopus/Web of Science searches and an exhaustive forward/backward citation search were not conducted. Publisher/DOI verification is stronger than claims of exhaustive topic coverage. See the exact [search log](search_strategy.md).
2. **Methods access:** several publisher endpoints returned access errors; some evidence is abstract-only or indexed passages. Obtain full C4–C6 methods and verify C8/C10 noise grids/timing before asserting protocol differences. Check C9's pretrained neural training distribution.
3. **Recent leads:** verify the publication and full methods behind PTSS1D and the additional 2026 leads recorded in the search log. Their omission from the selected bibliography is not evidence of irrelevance. Update the search before any novelty claim.
4. **Metric comparability:** source SNR definitions, amplitude-based noise scales and preprocessing differ. EEGdenoiseNet's inspected manuscript equation requires a final-paper/code check. Do not infer comparative performance from cross-paper numbers.
5. **Evidence status:** P1 is an explicitly labeled preprint. Bibliographic identity does not establish peer review or reproducibility. Check publication updates and corrections before manuscript submission.
6. **Feasibility and application relevance:** CPU training/runtime are unmeasured; exact feature metrics and generator distributions remain provisional. Synthetic conclusions may need a later small real-data validation appropriate to the eventual venue.

## Decisions requiring approval before Phase 2

The recommendation is to approve a **bounded development pilot first**, then review feasibility and freeze the full protocol before the main experiment. None of the following is authorized by this report alone.

1. **Contribution:** accept a controlled benchmark/replication direction with low novelty confidence, rather than a new-CNN claim; prioritize full-text/citation checks of the closest studies before manuscript positioning.
2. **Data and shifts:** approve the four synthetic families, length 1,024, three proposed noise processes and seven test SNRs; keep real-data validation and clean-family shift outside the initial scope.
3. **Methods and controls:** approve identity plus wavelet, local Wiener, SG and median baselines; one compact CNN architecture; source-only and diversity-trained regimes with three seeds each for the later main experiment.
4. **Evaluation and budget:** approve paired reconstruction/feature metrics, frozen validation tuning, same-CPU measurements, and the proposed one-hour-per-run/six-hour-training ceiling. Confirm or replace that ceiling before running the pilot.
5. **Authorization boundary:** explicitly authorize Phase 2 pilot implementation only after reviewing these deliverables. The full experiment and full paper remain subsequent review decisions.

## Deliverables and audit trail

- [README](../README.md): scope, initial environment and record-maintenance conventions.
- [Search strategy](search_strategy.md): executed queries, sources, inclusion/exclusion, failures and pending leads.
- [Literature matrix](literature_matrix.md): 18 selected references with bibliographic and methodological evidence.
- [Research gap](research_gap.md): six candidate gaps, counter-evidence and confidence.
- This report: conclusion, provisional protocol and approval decisions.
- [BibTeX](../references.bib): the same 18 verified identities, including an explicitly marked preprint and correction.
- [Crossref snapshots](metadata/): 15 public metadata records; these are evidence records, not experimental data.

Reference count comprises 15 research papers, one correction, one foundational book and one preprint. The adjacent image paper is identified as such. Local document links, selected citation keys and metadata consistency were checked; algorithms and models were not implemented or tested.
