# Search strategy and audit record

Search date and cutoff: **17 October 2026 (Asia/Tehran)**. Priority window: 2020–2026, with foundational and directly relevant earlier work. Searches were in English. Search-result crawl timestamps were not treated as publication dates.

## Scope and process

Question: how does training–test noise mismatch affect reconstruction, signal detail, and computational cost for classical methods versus a small CNN on controlled 1D signals?

The search proceeded from broad discovery to exact-title verification, original-source inspection, backward references, and targeted counter-evidence searches. It covered ECG, EEG, motion signals, ultrasonic echoes, motor acoustics, and random telegraph signals. One image-denoising paper is retained solely as methodological precedent for unseen noise levels. Speech/image results were not treated as direct evidence for generic 1D performance.

This is a focused scoping review. There was no exhaustive export, deduplicated database corpus, formal double screening, or PRISMA count. No numerical count of all screened hits is claimed. **18 references were selected**: 15 research papers, one correction, one foundational book, and one clearly marked preprint. Selection favors relevance and evidence quality, not citation volume.

## Sources actually used

| Source | Actual use | Limitation |
|---|---|---|
| Web search tool | General discovery, exact titles, domain-restricted searches, publisher-indexed passages | Rankings and snippets are incomplete and change; this is not equivalent to searching each database's native interface |
| Crossref REST API | Direct DOI lookups; 15 successful records saved in `metadata/` | Lookup verifies metadata, not full methods; not a broad Crossref subject search |
| Springer Nature Link | Wang C5 chapter metadata, abstract and references | Subscription preview; full methods inaccessible |
| Nature / Scientific Reports | Bai C9 full article, methods and performance sections | Readable despite cookie redirect; data available on request in article |
| PubMed | Qiu C4, Zhang C3, Qian C8, Yang C10 records/abstracts; some via indexed search | No native database-wide PubMed search/export; some direct opens returned almost empty pages |
| PMC | Indexed original-paper sections for Shaheen C7, Yang C10 and Schmid F5 | Several direct opens returned a browser-check page; indexed text is labeled as excerpts, not unrestricted full-text access |
| IEEE Xplore | Chiang C1 indexed publisher PDF and record; DOI metadata checked separately | Direct PDF returned HTTP 418; no native Xplore search or subscription access |
| ScienceDirect / Elsevier | Hu C6 and Qian C8 indexed publisher abstracts/sections | Direct opens returned HTTP 403; full baseline lists/SNR grids not assumed |
| IOPscience | Indexed Zhang C3 publisher content; Qiu C4 via PubMed and Crossref | Direct article access blocked by robots.txt or cache miss |
| Oxford Academic | Foundational Donoho–Johnstone F3 abstract record | Direct canonical URL failed on publisher redirect; metadata verified with Crossref |
| ACS Publications | F2 record, F5 indexed article and F6 correction text | Some content obtained through indexed publisher pages/PMC |
| MIT Press | Wiener F1 bibliographic record and edition information | Linked open-access DOI returned 403; book not read in full |
| EURASIP proceedings | Casas C2 complete five-page paper | Conference label and actual publication year differ; documented below |
| OpenReview | Mohan A1 published ICLR PDF | Forum-page access failed; official PDF succeeded |
| arXiv | Zhang C3 author manuscript v4; Nejad P1 preprint PDF | A manuscript is not automatically the journal version; P1 peer review not established |
| Institutional records, DBLP, OpenAlex | Discovery and metadata cross-checks | Used to locate primary sources, not to substantiate experimental results when originals were available |
| Author repositories | EEGdenoiseNet and FGDAE availability; PTSS1D lead | Repositories were not executed, reproduced, or comprehensively audited |
| Google Scholar, Scopus, Web of Science | **Not searched directly** | No claim of database coverage; native searches/citation chasing remain future work |

No login, purchase, author contact, email, or account modification was performed.

## Executed discovery queries and outcomes

The following records preserve exact substantive queries. Exact-title verification searches for every retained modern paper followed discovery; the titles are listed verbatim in the matrix. Some calls batched independent queries, so no per-query hit counts can be reliably assigned.

| Group | Exact queries executed | Outcome / disposition |
|---|---|---|
| Broad 1D | `"1D signal denoising" "noise" "generalization"`; `"signal denoising" "CNN" "unseen" noise synthetic`; `"one-dimensional" "denoising" "noise distributions"`; `"signal denoising" "generalization" "synthetic" CNN benchmark` | Domain studies dominated; no exact generic benchmark was verified from these queries |
| Lightweight | `"ECG denoising" "lightweight" "noise" CNN`; `"ECG denoising" "generalization" "noise types" 2024 2025` | Qiu, Hu, Shaheen, Nejad leads; classification-only studies excluded |
| Synthetic classics | `"Denoising" "synthetic signals" "convolutional" wavelet comparison`; `"signal denoising" "Blocks" "Bumps" "neural"`; `"denoising" "Doppler" "CNN" "Blocks"` | No verified exact match for the canonical-signal/CNN mismatch study; this is not evidence of absence |
| Distribution shift | `"1D" "denoising" "noise mismatch"`; `"signal denoising" "noise mismatch" convolutional`; `"signal denoising" "unseen noise"`; `"denoising" "unseen noise types" ECG` | Wang C5 is direct counter-evidence to novelty of unseen-noise evaluation |
| Generic comparators | `"one-dimensional signal denoising" convolutional synthetic`; `"signal denoising" "Savitzky" "CNN" synthetic` | Casas C2 and PTSS1D lead; no verified four-method generic factorial comparison |
| Foundations | `Donoho Johnstone ideal spatial adaptation wavelet shrinkage 1994 DOI Savitzky Golay 1964`; `Savitzky Golay 1964 "10.1021"`; `"De-noising by soft-thresholding" 1995 DOI`; `"Wiener" "Extrapolation, Interpolation" mitpress 1949` | F1–F4 verified |
| SG limitations | `"Why and How Savitzky–Golay Filters Should Be Replaced"`; `"Why and How Savitzky" Schmid Rath Diebold 2022`; `"Correction to" "Why and How Savitzky"` | F5 and its code correction F6 retained |
| Unseen levels | `denoising NeLU unseen noise levels 2024 signal processing`; `"Robust and Interpretable Blind Image Denoising" 2020` | A1 retained as adjacent-domain evidence; NeLU image paper not needed in core matrix |
| Unsuccessful terminology | `"Why and When Can Deep" denoising generalize noise 2020`; `"Why and When Can Deep" denoising` | Returned unrelated approximation-theory work; excluded |
| EEG benchmark | `"EEGdenoiseNet" benchmark 2021`; `"EEGdenoiseNet" 2021 journal neural engineering`; `EEGdenoiseNet benchmark dataset Zhang Zhao 2021`; `"EEGdenoiseNet" "−7" "2"` | C3 verified; primary author manuscript inspected; source SNR convention flagged |
| Metadata follow-up | `"A lightweight U-Net model for denoising and noise localization" authors`; `"Adversarial Signal Denoising" "10.23919"`; `"Fully-Gated Denoising Auto-Encoder" "Shaheen"` | Author lists and dates resolved against original records/Crossref |
| Protocol follow-up | `"Application-specific guided-wave" "SNR" "training"`; `"Fully-Gated Denoising Auto-Encoder" "SNR" "0.2"`; `"Fully-Gated Denoising Auto-Encoder" "noise" "0.5"` | C7 peak-amplitude scaling and C8 training information retrieved; not all details available |
| Failed precision searches | `site.pmc.ncbi.nlm.nih.gov/articles/PMC11821071 "3.3" "3.4" "noise"`; `site.pmc.ncbi.nlm.nih.gov/articles/PMC11821071 "SNR" "−" "Table 16"`; `site.pmc.ncbi.nlm.nih.gov/articles/PMC11821071 "Table 17" "CPU"` | Irrelevant hits; no methodological inference made from failure |
| Publication status | `"Lightweight Deep Autoencoder for ECG Denoising with Morphology Preservation" journal 2026` | No verified journal version found; retain P1 as preprint only |
| 2025–2026 update | `"signal denoising" "train" "colored noise" "impulsive" CNN 2025 2026`; `"synthetic signal denoising" "benchmark" "2026"`; `"signal denoising" "noise mismatch" "2025"`; `"signal denoising" "unseen" "Wiener"` | C9 and C10 found, substantially strengthening counter-evidence |
| Additional lead | `"Structure–Capacity Matching" "Prediction Target Selection"` | PTSS1D repository found; peer-reviewed publication not verified |
| Latest primary checks | `"Noise-Adversarial Denoising of Motor Acoustic Signals Across Noise Domains"`; `"A high-performance training-free pipeline for robust random telegraph signal characterization"` | C9/C10 publisher/PubMed and Crossref records verified |
| Domain-restricted | `"A lightweight U-net for ECG denoising using knowledge distillation"` restricted to PubMed/IOP; `"Noise-Adversarial Denoising of Motor Acoustic Signals Across Noise Domains" "SNR"` restricted to MDPI/PMC | C4 abstract and C10 leave-one-noise-domain-out protocol obtained |

## Inclusion and exclusion

Include primary 1D denoising studies that inform at least one key design axis: noise mismatch, controlled corruption, classical/CNN comparisons, waveform-detail evaluation, efficiency, or reproducibility. Retain theoretical foundations needed to define baselines. Include high-overlap preprints to avoid false novelty, but label their status. Include one targeted image-domain precedent, without extrapolating its results to 1D signals.

Exclude classification-only work, image/seismic-image studies without a necessary methodological connection, blogs, patents, unverified repository claims, and papers whose only overlap is the word “denoising.” Reviews supplied discovery leads but do not substitute for original studies in the selected matrix. Numerical performance values were not pooled across papers.

## Access failures, recovery, and version issues

- Crossref: initial sandbox request failed DNS; Python HTTPS outside the sandbox failed certificate validation. System `curl` with normal certificate verification succeeded. Four initial API requests returned 429; sequential retries recovered all four. All 15 selected article/chapter DOI responses are saved. HTTPS verification was not disabled.
- Springer C5: only subscription preview available. Noise-transfer evaluation is verified from the abstract, but SNR grids, full baseline roster and timing protocol remain NV.
- IEEE C1 PDF: HTTP 418. IOP C3: robots exclusion; C4: cache miss/robots exclusion. ScienceDirect C6/C8: HTTP 403. Original indexed excerpts and/or PubMed were used, with explicit evidence labels.
- PMC F5/C7 direct pages: browser-check response. MDPI C7/C10 direct pages: 429/inaccessible; indexed original-paper sections remained available. Oulu C7 PDF open failed; indexed passages were visible.
- arXiv P1 HTML URL returned 404; the PDF succeeded. OpenReview forum attempts failed, including an initial unusable candidate URL; the official published PDF was successfully located and used.
- OUP F3 canonical page failed on redirect. Crossref and the publisher abstract available through the index corroborated identity. MIT Press's linked digital-book DOI returned 403; the verified 1949 print edition is cited.
- C5: first online 27 November 2023; Springer recommended citation and Crossref print year are 2024. Use `wang2024` with an online-date note.
- C2: proceedings named **EUSIPCO 2020**, Crossref publication date in January **2021**. Use `casas2021`; do not infer the year from the DOI suffix.
- F2: original print year 1964; Crossref's 2002 online date is digitization, not the original study year. C6: 2024 issue despite 2023 in DOI. C3: 2020/2021 arXiv versions are distinct from the 2021 journal citation.
- F6 corrects a bandwidth function in the supporting Java code for weighted Savitzky–Golay smoothing. Consult corrected code if that method is later selected. [ACS correction](https://doi.org/10.1021/acsmeasuresciau.3c00017)

## Leads not promoted to verified evidence

| Lead | Why kept / why not selected |
|---|---|
| [PTSS1D author repository](https://github.com/fzg1023/PTSS1D) | Directly relevant 1D architectures and white/pink noise; no verified paper identity or peer-review status. Must investigate before a novelty claim. |
| [2026 EFIB-Net publisher page](https://www.mdpi.com/2076-3417/16/13/6401) | Cross-database ECG, downstream metrics and efficiency; publication/protocol not fully extracted in this review. Cross-database shift is not automatically noise-type holdout. |
| [2026 SWIFT-Mamba publisher page](https://www.mdpi.com/1424-8220/26/16/5048) | Synthetic wavefront signals and broad SNR testing; state-space architecture, not a simple CNN. Needs further protocol screening. |
| [2026 partial-discharge comparison](https://www.sciencedirect.com/science/article/abs/pii/S026322412602227X) | Very recent indexed lead; exact date, authors, DOI and overlap not verified. Excluded from BibTeX. |
| [2025 ECG comparison preprint](https://assets-eu.researchsquare.com/files/rs-7563670/v1_covered_209fd3b6-54ac-4fac-a860-dd4bdcdfe40e.pdf) | Classical/deep/embedded overlap; publication status and methods not verified. Do not confuse with P1. |

## Further searches before a novelty claim

Run native Scholar/Xplore/Scopus or Web of Science searches when available for `(one-dimensional OR 1D OR time-series) AND denois* AND (mismatch OR out-of-distribution OR cross-noise OR unseen)`, and `(wavelet OR Wiener OR Savitzky-Golay) AND (CNN OR convolutional) AND (runtime OR CPU OR benchmark)`. Search exact synthetic families, impulsive/burst noise, and noise-spectrum shifts. Forward/backward chase C5, C9 and C10, and obtain C4–C6 full methods. Verify the PTSS1D paper and C9's pretrained DAEUBL source/training distribution. These are proposed searches, not searches already completed.
