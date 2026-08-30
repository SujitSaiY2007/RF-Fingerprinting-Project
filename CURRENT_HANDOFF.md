# CURRENT HANDOFF — 2026-08-30

## Project
**Physics-Based RF Fingerprinting with Continuous Device Learning**

## Canonical repository
`SujitSaiY2007/RF-Fingerprinting-Project`

## Current position
- Phase: **Phase 1 — Accelerated implementation / demonstrator construction**.
- Stable branch: `main`.
- Integration branch: `develop`.
- Current engineering gate: **D4 — learned representation; reproducibility closure before D5**.
- D1: **COMPLETE at source/schema/ingestion-foundation level**.
- D2.1: **COMPLETE**.
- D2.2: **OBSERVED / IMPLEMENTED / TESTED on a 20-file SMoRFFI subset**.
- D2.3: **DEFINED / IMPLEMENTED / TESTED**.
- D2.4: **DEFINED / IMPLEMENTED / TESTED as an engineering split**.
- D2.5: **ENGINEERING ACCEPTED**.
- D3: **IMPLEMENTED / exploratory demonstrated; scientific validation not complete**.
- D4: **EXPLORATORY RESULT RECORDED; reproducibility closure still required**.
- D5+: **NOT STARTED**.
- D2 learning gate: **PASSED**.
- D3/D4 learning gates: **OPEN**.
- D1–D10 scientific validation: **not yet complete**.

## Fast-track objective
Move rapidly from the validated minimum data representation to a demonstrable D1–D10 software lifecycle while keeping the distinction between implementation, testing, demonstration and scientific validation.

Execution principle:
`Build minimum viable evidence path -> test -> document -> strengthen`

Fast-track does not permit inventing schema, hiding anomalies, claiming robustness without evidence, or converting exploratory results into validated findings.

## Active two-track execution model
### Track A — Fast Implementation / Demonstration
Current substrate: **SMoRFFI**.
Immediate path:
`D4 reproducibility closure -> D5 closed-set identity -> D6 open-set -> D7 shift -> D8 profile evolution -> D9 poisoning -> D10 integration`

### Track B — Research Validation / Strengthening
Use qualified datasets such as WiSig and Oregon State WiFi RFFP when claims require temporal, receiver, environment or broader robustness evidence. Track B supports or falsifies claims rather than manufacturing positive evidence.

## D2 learning gate result
The researcher passed the D2 learning gate through concept checks covering complex arithmetic, I/Q representation, magnitude/phase, sampling, Nyquist/aliasing and project-linked dataset/schema reasoning. The researcher demonstrated why sample count alone is insufficient and why the actual SMoRFFI representation must be inspected before preprocessing.

## SMoRFFI D2.2 observed schema
Twenty uploaded IQ-only CSVs were inspected directly, totaling **19,513 rows**.

Observed schema:
- `Device Number`
- `MAC_address`
- `preamble`

Observed signal representation:
- `preamble` is a serialized whitespace-separated complex-valued sequence;
- all inspected rows parse successfully;
- stored sequence length is **288–579 complex samples**;
- 5,783 rows are exactly 288 samples;
- 13,730 rows contain additional samples;
- device 109 has 513 rows and stored lengths 448–579; this anomaly is retained rather than silently repaired.

The published SMoRFFI definition describes the canonical preamble as **288 complex samples** and reports a 20 MS/s acquisition. Track-A therefore selects the first 288 parsed samples and records original length plus discarded-tail count as provenance.

## D2.3 preprocessing contract
`serialized preamble -> complex[288] -> real[2,288] (I,Q)`.

No per-observation normalization, clipping, filtering, resampling or arbitrary interpolation is applied. Amplitude normalization remains a future ablation.

Implementation: `src/smorffi_d2.py`
Tests: `tests/test_smorffi_d2.py`
Specifications: `docs/04_research/D2_2_SMORFFI_SCHEMA_EVIDENCE.md`, `D2_3_PREPROCESSING_CONTRACT.md`.

## D2.4/D2.5
Track-A engineering split is 70/15/15 using deterministic SHA-256 assignment from `(device_id, source_row_index)`. It is not claimed to be a temporal/session holdout. Integrated D2 checks are accepted on the 20-file subset.

## D3 state
`src/smorffi_d3.py` extracts deterministic, label-free evidence including I/Q moments, amplitude/power statistics, I/Q correlation/variance ratio, local phase-step statistics, FFT spectral centroid/spread and spectral entropy. Phase slope is deliberately not called calibrated CFO.

An earlier fast-track runtime experiment reported approximately **90.9% Random Forest closed-set accuracy**. This remains exploratory until the exact dataset manifest/configuration are re-established.

## D4 state
A fast-track neural experiment using the canonical `2 x 288` I/Q input and compact learned representation reported approximately **91.1% closed-set test accuracy** on the available runtime subset.

This is **exploratory only**. The exact dataset manifest, model implementation/configuration and reproducible run artifact are not yet committed/tested. Formal D4 acceptance requires a reproducible implementation, tests, configuration, dataset manifest, deterministic controls and embedding-level evaluation.

Reference: `docs/04_research/D4_LEARNED_REPRESENTATION_BASELINE.md`.

## Dataset-count correction
A prior conversational update stated **32,513 observations** after additional uploads. That number is not authoritative. The reproducible runtime snapshot available for the D4 exploratory run contained **10,186 usable observations across 33 devices**. Until a complete manifest is regenerated, use only explicitly verified counts in formal results. The 19,513-row D2.2 inspection remains valid for its stated subset.

## Next-chat execution plan
### First — close D4 reproducibility
1. Inspect the current repository and preserve all existing information.
2. Implement the smallest reproducible learned encoder using the frozen `2 x 288` I/Q input.
3. Add tests, fixed configuration and a dataset manifest/snapshot record.
4. Reproduce or explicitly correct the exploratory ~91.1% result; never force agreement.
5. Freeze one baseline. Do not hyperparameter-tune merely to increase accuracy.

### Then — D5 closed-set identity
Use the frozen embedding and evaluate nearest-centroid/nearest-neighbour and a simple classifier where useful. Report confusion matrix, per-device precision/recall/F1, macro-F1 and balanced accuracy, with reproducibility controls.

### Then — D6 open-set recognition
Reserve unseen device classes and evaluate unknown rejection. Select thresholds without using the frozen test set. Report known-device performance, unknown rejection, false acceptance and false rejection.

### Later — D7–D10
- D7: controlled distribution shift using only variation actually exposed by the data; stronger temporal/receiver/environment claims belong to Track B.
- D8: persistent device profiles/prototypes; separate recognition from authorization to modify a profile.
- D9: controlled/synthetic poisoning of profile updates; compare admission policies and legitimate adaptation.
- D10: integrate the complete lifecycle into one demonstrable path.

## Professor-demonstration priority
Target coherent path:
`SMoRFFI CSV -> D2 parse/IQ -> D3 RF evidence -> D4 embedding -> D5 identity -> D6 unknown rejection -> D8 update decision -> D9 poisoning defense -> final decision`

Every result must be labelled **Implemented / Tested / Demonstrated / Scientifically Validated**.

## Scientific guardrails
- Never use MAC/device identifiers as model inputs.
- Keep source rows and derived representations traceable.
- Never fit preprocessing statistics on validation/test data.
- Do not claim temporal/session/receiver/environment robustness from SMoRFFI alone.
- Keep Track A and Track B evidence separate.
- D9 poisoning data must be controlled/synthetic or explicitly labelled.
- D8/D9 novelty comparisons must include the baseline ladder.
- D10 must demonstrate the lifecycle.
- Never silently delete, overwrite or simplify earlier project decisions/documents.
- Exploratory runtime numbers are not formal benchmarks without reproducible code/configuration/manifest evidence.

## Novelty boundary
Current candidate contribution remains provisional:
> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile-poisoning while preserving legitimate adaptation.**

Do not present this as proven novelty until D8/D9 evidence supports or falsifies it.

## Branch synchronization rule
At the end of a significant agreed milestone, synchronize `main` and `develop` to the same **content state** without deleting or silently reverting prior information. Merge commits may make histories differ even when file contents are identical; content equivalence is the operative synchronization requirement.

The D2–D4 milestone has now been synchronized to both branches. Future significant milestones should land on `develop` first and then be synchronized to `main` after agreement.

## Exact prompt for the next chat
> Continue the RF Fingerprinting Project from the canonical GitHub state. First read `PROJECT_STATE.md`, `CURRENT_HANDOFF.md`, `docs/04_research/LEARNING_GATES.md`, `docs/04_research/D2_2_SMORFFI_SCHEMA_EVIDENCE.md`, `docs/04_research/D2_3_PREPROCESSING_CONTRACT.md`, `docs/04_research/D2_4_LEAKAGE_SAFE_SPLIT.md`, `docs/04_research/D2_5_INTEGRATED_ACCEPTANCE.md`, and `docs/04_research/D4_LEARNED_REPRESENTATION_BASELINE.md`. The D2 learning gate is passed. Do not redo D1/D2 or assume the SMoRFFI schema. We are in accelerated Track-A implementation mode. First close D4 reproducibility honestly: implement the smallest reproducible learned embedding using the frozen `2 x 288` I/Q D2 input, add tests/configuration/manifest, and reproduce or explicitly correct the exploratory ~91.1% result. Do not tune merely for accuracy. Then freeze D4 and proceed directly to D5 closed-set identity using the learned embedding, with confusion matrix, per-device metrics, macro-F1/balanced accuracy and nearest-centroid/nearest-neighbour baseline where useful. After D5, move to D6 open-set unknown-device rejection. Maintain Track A/Track B separation, provenance, leakage controls, frozen test evaluation, novelty boundaries, and the Implemented/Tested/Demonstrated/Scientifically Validated status discipline. Do not silently delete or overwrite existing project information. At the end of the chat, update the handoff and synchronize main/develop after the milestone is explicitly agreed.
