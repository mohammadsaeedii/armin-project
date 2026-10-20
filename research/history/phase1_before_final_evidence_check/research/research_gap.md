# Candidate research gaps and counter-evidence

Assessment date: 17 October 2026. **No novelty claim is validated.** Confidence below means confidence that a defensible, incompletely covered research opportunity remains, not confidence in an expected numerical result. Full bibliographic details and evidence depth are in [the matrix](literature_matrix.md).

## Verdict on the original direction

The proposed question is scientifically meaningful, but most of its ingredients already have clear precedents. Noise-type transfer exists in ECG and motor acoustics; unseen-level testing exists in neural denoising; synthetic noise, detail metrics and runtime/memory comparisons already coexist in random-telegraph analysis. [C5](https://doi.org/10.1007/978-981-99-8388-9_40), [C10](https://doi.org/10.3390/s26144489), [A1](https://openreview.net/pdf/ae5ecd6a31912546f2851cd3d1034a3537b633b8.pdf), [C9](https://doi.org/10.1038/s41598-026-36656-2)

**Interpretation:** pursue a transparent benchmark/replication contribution only if it produces useful, reproducible evidence about method selection. A different signal generator, one fewer layer, or a new combination of familiar metrics is not by itself a strong publication contribution.

## Candidate-by-candidate evaluation

| Candidate gap | Supporting evidence and closest studies | Counter-evidence / already addressed | Further work needed | Preliminary confidence |
|---|---|---|---|---|
| **G1. Isolate noise-process shift from SNR shift in a classical-versus-small-CNN comparison** | C5/C10 establish relevance of noise transfer. Accessible descriptions do not establish our exact factorial experiment with frozen tuning, fixed clean-family distribution and power-matched synthetic noise. | C5 explicitly examines unseen noise; C10 uses leave-one-noise-domain-out; A1 includes distribution transfer. Thus “first unseen-noise denoising study” is untenable. | Full C5/C10 protocols; native database and citation searches for generic 1D cross-noise benchmarks; PTSS1D paper verification. | **Medium** for useful controlled evaluation; **low** for novelty. |
| **G2. Test genuinely unseen noise levels** | A1 and P1 motivate distinguishing extrapolation from interpolation. Our protocol could separate these from type shift. | A1 already tests outside training levels; P1 trains at −5 dB and tests at 0/+5 dB. Merely adding test SNRs is established practice. | Check C4–C6 train/test grids; distinguish continuous training-range sampling from held-out support. | **Low** as a standalone gap. |
| **G3. Quantify detail loss specifically under mismatch** | Aggregate errors may not answer whether small events survive. A useful synthetic protocol could score known pulse amplitudes/timing and step overshoot. F5 motivates boundary analysis. | C9 already evaluates switching structure; C7 addresses morphology; C8 has detection/ROI measures; C5 includes downstream outcomes. “Beyond RMSE” is already addressed. | Search exact feature-error metrics in pulse/ultrasonic/RTS studies and full mismatch protocols; identify which feature errors add information beyond existing measures. | **Medium** for a narrowly specified mismatch interaction; **low** for detail preservation generally. |
| **G4. Fair CPU cost–quality comparison with source-only tuning** | C7's reported GPU/CPU division limits interpretation as all-CPU latency. C4 reports size/FLOPs; actual CPU costs require measurement. | C9 includes runtime and peak memory under fixed hardware; P1 includes Raspberry Pi deployment. “First efficient comparison” is not supported. | Audit hardware, thread counts, batch sizes, preprocessing and tuning access in closest papers; search CPU/edge benchmark studies. | **Medium** for the exact protocol; **low** for efficiency evaluation generally. |
| **G5. Public, reproducible synthetic benchmark** | Publishing generators, partitions, tuning spaces and per-example results could make comparisons auditable; some essential methods remain inaccessible. | C3 already releases a benchmark and code; C7 has an author repository; synthetic comparisons are common. C9 gives a detailed protocol even though its data are on request. | Audit licensing and executability of existing resources; compare protocol coverage, not just repository presence. | **Low** as standalone novelty; useful enabling contribution. |
| **G6. A new lightweight denoising CNN** | C4 supports feasibility of small networks. | C4, C6, C7 and P1 already study compact architectures. No specific new mechanism has been identified here. | Only revisit if a literature-supported mechanism and a controlled ablation are justified after baseline experiments. | **Low**; **do not pursue as the Phase 2 claim**. |

Source links for the evidence table: [F5](https://doi.org/10.1021/acsmeasuresciau.1c00054), [C3](https://doi.org/10.1088/1741-2552/ac2bf8), [C4](https://doi.org/10.1088/1361-6579/ac96cd), [C5](https://doi.org/10.1007/978-981-99-8388-9_40), [C6](https://doi.org/10.1016/j.bspc.2023.105504), [C7](https://doi.org/10.3390/s25030801), [C8](https://doi.org/10.1016/j.ultras.2026.108054), [C9](https://doi.org/10.1038/s41598-026-36656-2), [C10](https://doi.org/10.3390/s26144489), [A1](https://openreview.net/pdf/ae5ecd6a31912546f2851cd3d1034a3537b633b8.pdf), [P1](https://arxiv.org/abs/2511.12478).

## Strongest candidate, provisionally

**Proposed question:** For a fixed population of analytic 1D signals, when do the rankings of validation-tuned classical filters and a fixed compact CNN change as noise moves from white Gaussian to temporally correlated Gaussian or impulsive contamination, at matched input power-SNR? How do those changes depend on local signal structure, and what are the measured training, tuning and inference costs on one CPU?

This combines G1, G3 and G4. **Confidence in scientific usefulness: medium. Confidence in distinct publishable novelty: low.** This distinction should remain in any project brief. No “first,” “novel framework,” or “unexplored problem” wording is justified.

The contrast with C9 must be explicit: separate denoising from downstream digitization, and control how the neural model was trained relative to each noise condition. The contrast with C5/C10 must be explicit: isolate changes in a specified stochastic noise process at equal power while holding signal population fixed. Neither difference establishes priority without additional searches. [C9](https://doi.org/10.1038/s41598-026-36656-2), [C5](https://doi.org/10.1007/978-981-99-8388-9_40), [C10](https://doi.org/10.3390/s26144489)

## Definitions that prevent false gap claims

- **Matched distribution:** new independent realizations from the same signal and noise generators. Test examples are still held out.
- **Unseen noise type/process:** the test process is absent from both training and model-selection data. Different NSTDB segments alone do not satisfy this.
- **Unseen level:** an exact test value absent from training. If it lies inside the training range, call it interpolation; outside the support, call it extrapolation.
- **Joint shift:** type and level both change. Report separately so one cannot explain away the other.
- **Clean-signal shift:** new morphology/frequency family. Exclude from the primary experiment; add only as a separate extension.
- **Colored Gaussian versus white Gaussian:** their marginal distributions can both be Gaussian; the changed temporal covariance is itself a distribution shift. Do not describe the colored case simply as “non-Gaussian.”
- **Mixed-noise training:** if a component is in training, testing on it is not evidence of unseen-component generalization. A diversity-trained control answers a different question.
- **Classical mismatch:** a classical filter has assumptions, tuning data and estimators rather than neural training. Freeze its tuning on the same source validation conditions, while allowing declared adaptation using the observed noisy input.

These are operational definitions proposed for this project. They are not claims that previous authors used the same definitions.

## What would make the result worth reporting?

**Interpretation / decision criteria, not predicted findings:** useful evidence could include stable crossover regions, loss of small events despite similar RMSE, or a clear quality–cost tradeoff that survives paired uncertainty analysis and reasonable classical tuning. A negative result is valid: a small CNN might offer no benefit under shift, or mixed-noise training might remove the effect. Failure to reproduce an apparent advantage after controlling leakage or information access would also be informative if documented carefully.

Avoid claiming that a difference between Gaussian-trained and mixed-trained models identifies a causal “mismatch penalty” by itself: training diversity changes too. A clean adaptation estimate would require equal-budget, target-distribution training/validation arms with test data still held out. That extension is outside the initial minimal proposal.

For fixed-shape feed-forward CNNs, changing noise usually does not change the operation count. Therefore, expect runtime to be primarily a property of method, length, batch, implementation and hardware. Study quality under shift and quality–cost tradeoffs; do not presume noise shift causes a substantial latency change. Adaptive algorithms may behave differently, which should be measured rather than assumed.

## Open questions and stop conditions

1. Does a prior generic 1D study already implement the exact factorial, source-tuned, detail-sensitive CPU protocol? **Unresolved.** Verify C5 full text and PTSS1D first.
2. Are the proposed features meaningful beyond the chosen synthetic generators? **Unresolved.** Synthetic-only conclusions must remain conditional; a later small real-data validation may be needed for the target venue.
3. Is one architecture enough? Enough for a scoped comparison of named methods, not for a conclusion about all deep learning. Architecture choice should be fixed before observing test performance.
4. Can CPU training fit the available time? **Unmeasured.** Only an approved Phase 2 pilot can answer this.
5. If close prior art covers the exact protocol, reframe as replication/extension or pivot to a specific application. Do not manufacture novelty by changing window length or adding another aggregate metric.

The recommendation is a **conditional go for a modest benchmark pilot after approval**, and a **no-go for asserting novelty or starting the full paper now**.
