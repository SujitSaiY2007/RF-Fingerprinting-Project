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

Do not claim scientific completion from code existence or from a single closed-set accuracy number.

## Active two-track execution model

### Track A — Fast Implementation / Demonstration
Current substrate: **SMoRFFI**.

Immediate path:
`D4 reproducibility closure -> D5 closed-set identity -> D6 open-set -> D7 shift -> D8 profile evolution -> D9 poisoning -> D10 integration`

The objective is to get a real-data end-to-end demonstration quickly.

### Track B — Research Validation / Strengthening
Use qualified datasets such as WiSig and Oregon State WiFi RFFP when a claim requires temporal, receiver, environment or broader robustness evidence. Track B must support or falsify claims rather than manufacture positive evidence.

## D2 learning gate result
The researcher passed the D2 learning gate through concept checks covering complex arithmetic, I/Q representation, magnitude/phase, sampling, Nyquist/aliasing and project-linked dataset/schema reasoning. The researcher demonstrated understanding of why sample count alone is insufficient and why the actual SMoRFFI representation must be inspected before preprocessing.

## SMoRFFI D2.2 observed schema
Twenty uploaded IQ-only CSVs were inspected directly, totaling **19,513 rows**.

Observed file schema:
- `Device Number`
- `MAC_address`
- `preamble`

Observed signal representation:
- `preamble` is a serialized whitespace-separated complex-valued sequence;
- all inspected rows parse successfully;
- stored sequence length is **288–579 complex samples**;
- 5,783 rows are exactly 288 samples;
- 13,730 rows contain additional samples;
- the device-109 file contains 513 rows and stored lengths 448–579, so this anomaly is retained rather than silently repaired.

The published SMoRFFI definition describes the canonical preamble as **288 complex samples** and reports a 20 MS/s acquisition. The Track-A baseline therefore selects the first 288 parsed samples and records original length plus discarded-tail count as provenance. Full rationale: `docs/04_research/D2_2_SMORFFI_SCHEMA_EVIDENCE.md`.

## D2.3 preprocessing contract
Baseline:
`serialized preamble -> complex[288] -> real[2,288] (I,Q)`.

No per-observation normalization, clipping, filtering, resampling or arbitrary interpolation is applied. Amplitude normalization remains a future ablation because it may remove RF-discriminative information.

Implementation: `src/smorffi_d2.py`
Tests: `tests/test_smorffi_d2.py`
Specification: `docs/04_research/D2_3_PREPROCESSING_CONTRACT.md`

## D2.4 split policy
Track-A engineering split:
- 70% train;
- 15% validation;
- 15% test;
- deterministic SHA-256 assignment from `(device_id, source_row_index)`.

This is **not** claimed to be a temporal/session holdout because SMoRFFI does not expose those boundaries. Device identity and MAC remain labels/provenance only.

Specification: `docs/04_research/D2_4_LEAKAGE_SAFE_SPLIT.md`

## D2.5 acceptance
Integrated D2 checks pass on the 20-file local subset. Specification: `docs/04_research/D2_5_INTEGRATED_ACCEPTANCE.md`.

## D3 state and result
`src/smorffi_d3.py` defines deterministic, label-free interpretable RF evidence features from the canonical 288-sample complex preamble:
- I/Q moments and variance ratio;
- amplitude mean/std, RMS and crest factor;
- mean power;
- I/Q correlation;
- local phase-step statistics;
- FFT spectral centroid and spectral spread;
- spectral entropy.

An earlier fast-track runtime experiment reported approximately **90.9% Random Forest closed-set test accuracy**. This remains an exploratory engineering/demo result until the exact dataset manifest and run configuration are re-established. It is not a validated transmitter-intrinsic fingerprinting claim.

## D4 state and result
A fast-track neural experiment was reported using the canonical `2 x 288` I/Q input and a compact learned representation, with approximately **91.1% closed-set test accuracy** on the runtime subset available for that experiment.

This result is intentionally classified as **exploratory** because the exact dataset manifest, model implementation/configuration and reproducible run artifact are not yet committed and tested in the repository. Do not quote 91.1% as a formal benchmark yet.

D4 reproducibility closure requirements:
1. commit a minimal learned-embedding implementation;
2. commit tests and configuration;
3. record the exact dataset manifest/snapshot;
4. verify deterministic splitting and training controls;
5. record embedding dimension and model definition;
6. evaluate the embedding independently of classifier accuracy;
7. freeze the baseline before moving to D5.

Do not hyperparameter-tune merely to increase the headline accuracy.

## Dataset-count correction
A prior conversational update stated **32,513 observations** after additional uploads. That count is not authoritative. The current reproducible runtime snapshot available for the D4 exploratory run contained **10,186 usable observations across 33 devices**. Until a complete manifest is regenerated from all uploaded files, use only explicitly verified counts in formal results. The original 19,513-row 20-file D2.2 inspection remains valid for its stated subset.

## Next-chat execution plan

### First: close D4 reproducibility
- Inspect the current repository tree and preserve all existing documents.
- Implement the smallest reproducible learned encoder/baseline compatible with the D2 input contract.
- Keep the model simple and fixed; no accuracy-chasing.
- Run engineering tests.
- Generate a machine-readable result/configuration record and dataset manifest for the available data snapshot.
- Reproduce or explicitly supersede the exploratory ~91.1% result. If it cannot be reproduced, record the discrepancy rather than forcing agreement.

### Then: D5 closed-set identity
Use the frozen D4 embedding and evaluate:
- nearest-centroid and/or nearest-neighbour identity;
- a simple classifier baseline;
- confusion matrix;
- per-device precision/recall/F1;
- balanced accuracy and macro-F1;
- reproducibility controls.

The purpose is to establish whether the learned representation is useful as an identity representation, not merely as a classifier input.

### Then: D6 open-set recognition
Reserve device classes not used for training and evaluate unknown-device rejection. Report threshold selection procedure, known-device performance, unknown rejection, false acceptance and false rejection. Do not choose a threshold using the frozen test set.

### Later D7–D10
- **D7:** controlled distribution-shift experiments using only variation the available data actually exposes; Track B datasets supply stronger temporal/receiver/environment evidence.
- **D8:** persistent device profiles/prototypes; separate recognition from authorization to modify a profile.
- **D9:** controlled/synthetic poisoning of the profile-update path; compare admission policies and legitimate adaptation.
- **D10:** integrate the complete lifecycle into a demonstrable pipeline.

## Professor-demonstration priority
The fast-track demonstrator should eventually show one coherent path:

`SMoRFFI CSV -> D2 parse/IQ -> D3 RF evidence -> D4 embedding -> D5 identity -> D6 unknown rejection -> D8 update decision -> D9 poisoning defense -> final decision`

Use a clear status label for every result: **Implemented / Tested / Demonstrated / Scientifically Validated**.

## Scientific guardrails retained
- Do not use MAC/device identifiers as model inputs.
- Keep raw/source rows and derived representations traceable.
- Do not fit preprocessing statistics on validation/test data.
- Do not claim temporal/session/receiver/environment robustness from SMoRFFI alone.
- Keep Track A and Track B evidence separate.
- D9 poisoning data must be controlled/synthetic or otherwise explicitly labelled.
- D8/D9 novelty comparisons must include the required baseline ladder.
- D10 must demonstrate the complete lifecycle.
- Never convert an exploratory runtime result into a formal benchmark without a reproducible dataset manifest, code/configuration and test evidence.
- Never silently delete, overwrite or simplify earlier project decisions/documents.

## Novelty boundary
The current candidate contribution remains provisional:

> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile-poisoning while preserving legitimate adaptation.**

Do not present this as proven novelty until D8/D9 evidence supports or falsifies it.

## Branch synchronization rule
At the end of a significant agreed milestone, synchronize `main` and `develop` to the same **content state** without deleting or silently reverting prior information. Merge commits may make branch histories differ even when their file contents are identical; content equivalence is the operative synchronization requirement.

The D2–D4 milestone has now been synchronized to both branches. Future significant milestones should again land on `develop` first and then be synchronized to `main` after agreement.

## Exact prompt for the next chat

> Continue the RF Fingerprinting Project from the canonical GitHub state. First read `PROJECT_STATE.md`, `CURRENT_HANDOFF.md`, `docs/04_research/LEARNING_GATES.md`, `docs/04_research/D2_2_SMORFFI_SCHEMA_EVIDENCE.md`, `docs/04_research/D2_3_PREPROCESSING_CONTRACT.md`, `docs/04_research/D2_4_LEAKAGE_SAFE_SPLIT.md`, `docs/04_research/D2_5_INTEGRATED_ACCEPTANCE.md`, and `docs/04_research/D4_LEARNED_REPRESENTATION_BASELINE.md`. The D2 learning gate is passed. Do not redo D1/D2 or assume the SMoRFFI schema. We are in accelerated Track-A implementation mode. First close D4 reproducibility honestly: inspect the current repository, implement the smallest reproducible learned embedding using the frozen `2 x 288` I/Q D2 input, add tests/configuration/manifest, and reproduce or explicitly correct the exploratory ~91.1% result. Do not tune merely for accuracy. Then freeze D4 and proceed directly to D5 closed-set identity using the learned embedding, with confusion matrix, per-device metrics, macro-F1/balanced accuracy and nearest-centroid/nearest-neighbour baseline where useful. After D5, move to D6 open-set unknown-device rejection. Maintain Track A/Track B separation, provenance, leakage controls, frozen test evaluation, novelty boundaries, and the Implemented/Tested/Demonstrated/Scientifically Validated status discipline. Do not silently delete or overwrite any existing project information. At the end of the chat, prepare the updated handoff and synchronize main/develop only after the milestone is explicitly agreed.`
