> **Current status — 18 October 2026:** Phase 2 development coding is authorized. See [implementation and commands](research/phase2_implementation.md) and [final evidence update](research/final_evidence_check.md). The original Phase 1 status below is retained as historical context; main experiments remain pending review.

**Pilot verified:** 16 tests passed; the five-epoch CPU run completed in 42.17 seconds. See [verification and output links](research/phase2_verification.md). These are development checks, not main-experiment findings.

# 1D signal denoising — Phase 1

Status: literature review completed for researcher review; **Phase 2 is not authorized**.

Review date: **17 October 2026**, Asia/Tehran. This is a focused, evidence-led scoping review, not an exhaustive systematic review or a claim of established novelty.

The project investigates whether a reproducible, CPU-oriented comparison of classical denoisers and a small 1D CNN can usefully characterize degradation under training–test noise mismatch. The intended contribution is an evaluation protocol and empirical evidence, subject to further validation, rather than a presumed new denoising algorithm.

The directory was inspected before changes and was empty, including no Git repository, datasets, code, or existing research records. No denoisers, training code, environments, model weights, or experimental results have been created. Public bibliographic metadata was retrieved; those retrievals are not experiments.

## Reading order and records

1. [Phase 1 report](research/phase1_report.md): conclusion, provisional experimental scope, and decisions requiring approval.
2. [Literature matrix](research/literature_matrix.md): 18 selected references, their verified metadata, experimental evidence, and limitations.
3. [Research gaps](research/research_gap.md): evidence, counter-evidence, confidence, and further searches.
4. [Search strategy](research/search_strategy.md): executed queries, source coverage, failed accesses, and screening decisions.
5. [BibTeX](references.bib): verified reference identities only; a preprint is explicitly marked as such.
6. [Metadata directory](research/metadata/): 15 saved public Crossref JSON responses with retrieval dates and source URLs. These verify identity and publication details, not the validity of a paper's experiments.

## Evidence conventions

- **Verified** means supported by an identified publisher record, original paper, official proceedings, author manuscript, or reliable bibliographic record. It does not mean independently reproduced.
- **Interpretation / proposal** denotes our reasoning or a possible protocol, not an author-reported finding.
- **Unresolved / NV** means not verified in the accessible material. It must never be silently converted to “not studied” or “not reported.”
- **N/A** means a field is inapplicable, for example a CNN training split in a classical theoretical paper.
- Full-text, abstract-only, indexed-excerpt, and preprint evidence are distinguished in the matrix. Bibliographic verification and methodological verification are separate.

Use the stable IDs F1–F6, C1–C10, A1, and P1 when discussing the review. Their BibTeX keys are recorded in the matrix. Cite a source beside each factual claim. Preserve reported noise conventions; do not compare raw SNR/RMSE values across incompatible datasets or definitions.

For updates, append the search date, exact query, source/access outcome, and inclusion decision to `search_strategy.md`; revise the matrix and gap confidence together; then update the report and bibliography. Retain raw metadata snapshots and note corrections or conflicting publication dates. Before submission, refresh the search and check publisher corrections/retractions for every central source. No scheduled monitoring has been configured.

Do not add `src/`, training notebooks, generated data, or results until the researcher approves the decisions in the report. Phase 1 ends with a reviewable proposal, not a finalized experiment.

## Update — 18 October 2026

The researcher has authorized coding a bounded Phase 2 development pilot. The initial Phase 1 text above is preserved as the earlier decision record; its no-code status describes that earlier phase. Main experiments and publication claims remain unapproved.

- [Final evidence check](research/final_evidence_check.md): stable C9/C10 crosswalk, updated access, PTSS1D and additional close precedent C11.
- [Implementation and run instructions](research/phase2_implementation.md): CPU pilot, safeguards and explicit deviations.
- Run: `.venv/bin/python -m denoising pilot --config configs/pilot.json --output outputs/pilot-new`
- Tests: `.venv/bin/python -m unittest discover -s tests -v`

The initial six records are preserved in [history](research/history/phase1_before_final_evidence_check/manifest.json). Current bibliography contains 19 verified identities; PTSS1D remains a repository lead rather than an invented paper citation.
