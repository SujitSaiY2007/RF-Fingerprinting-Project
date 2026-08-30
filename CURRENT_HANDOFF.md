# CURRENT HANDOFF — 2026-08-30

## Project
**Physics-Based RF Fingerprinting with Continuous Device Learning**

## Canonical repository
`SujitSaiY2007/RF-Fingerprinting-Project`

## Current position
- Phase: **Phase 1 — Accelerated implementation / demonstrator construction**
- Stable branch: `main`
- Integration branch: `develop`
- D2 learning gate: **PASSED**
- D1: **COMPLETE at established scope**
- D2.1–D2.5: **COMPLETE / engineering accepted at established Track-A scope**
- D3: **IMPLEMENTED / TESTED / EXPLORATORY DEMONSTRATED; scientific validation incomplete**
- D4: **IMPLEMENTED / TESTED / DEMONSTRATED; reproducible 33-device baseline frozen; historical ~91.1% not reproducible**
- D5: **IMPLEMENTED / TESTED / DEMONSTRATED; closed-set identity baseline complete**
- D6: **IMPLEMENTED / TESTED / DEMONSTRATED; open-set rejection baseline complete**
- Next stage: **D7 controlled distribution-shift experiments**
- D3–D10 scientific validation: **not complete**

## Active execution model
### Track A — Fast implementation/demonstration
Current substrate: **SMoRFFI**. Build the minimum defensible D1–D10 vertical path quickly.

### Track B — Research validation/strengthening
Use WiSig and Oregon State datasets when temporal, receiver, environment, cross-condition or broader robustness claims require evidence. Do not mix Track-B evidence into Track-A claims.

## D2 contract retained
The D2 baseline is frozen and must not be redefined in later chats:
`serialized preamble -> complex[288] -> float32[2,288] I/Q`.
No baseline normalization, clipping, filtering or resampling. Device/MAC identifiers are labels/provenance only. Split is deterministic SHA-256 `(device_id, source_row_index)` 70/15/15 and is explicitly **not** a temporal/session holdout.

## Supplied dataset provenance
The complete user-supplied archive was inspected:
- 123 CSV files
- 122,511 observations
- 123 devices
- archive SHA-256: `1d9ebcf2539e5fb7fb1dc678dba3fd2a50cada2befb86f5d84faff2b4f541037`

Track-A D4/D5 known snapshot:
- devices 1–33
- 33 files
- 33,000 observations
- 23,030 train / 4,974 validation / 4,996 test under the frozen D2 split

Source anomalies retained without silent repair:
- device 67: 999 rows
- device 87: 999 rows
- device 109: 513 rows

The historical D4 runtime was recorded as **10,186 usable observations across 33 devices**. The exact historical selection is not recoverable from the supplied corpus/repository evidence.

## D4 closure decision
The frozen minimal Track-A learned encoder is:
`Conv1d(2,16,k7) -> ReLU -> MaxPool(2) -> Conv1d(16,32,k5) -> ReLU -> AdaptiveAvgPool(1) -> Linear(32,32) embedding -> Linear(32,C)`.

Configuration:
- seed `20260830`
- embedding dimension `32`
- 12 epochs
- batch size `128`
- learning rate `1e-3`
- weight decay `1e-4`
- no accuracy tuning

Reproducible run on devices 1–33:
- test accuracy: **35.8086%**

Historical exploratory result:
- approximately **91.12% test accuracy**
- remains **historical/exploratory and not reproducible/certified** because the exact 10,186-row selection and prior model/configuration are unavailable.

Do not reinterpret the 35.81% result as proof that 91.12% was false. The scientifically correct conclusion is that the historical run cannot be reconstructed from currently recoverable evidence, while the current frozen baseline is reproducible.

## D5 closure
D5 uses the frozen D4 embedding and frozen test set. No D4 retraining or test-set fitting occurs.

| Method | Accuracy | Macro-F1 | Balanced accuracy |
|---|---:|---:|---:|
| D4 classifier | 35.81% | 31.58% | 35.80% |
| Nearest centroid | 36.21% | 33.23% | 36.30% |
| **1-nearest neighbour** | **63.77%** | **63.63%** | **63.80%** |

The 1-NN result is the strongest Track-A readout and indicates local identity structure in the embedding. It is not evidence of temporal/receiver/environment robustness. Per-device metrics and the 33x33 confusion matrix are retained in `experiments/track_a/d5_nn_per_device.md` and `experiments/track_a/d5_nn_confusion_matrix.csv`.

## D6 closure
Known devices: 1–33. Unknown devices: 34–123.

D6 score: nearest known-device centroid squared Euclidean distance in the frozen embedding.

Threshold:
- selected only from known-device validation data
- 95th percentile
- `T = 21.2566452`

Results:
- known frozen-test acceptance: **95.42%** (4,996 known test observations)
- unknown test rejection: **10.99%** (13,329 observations from 90 unknown devices)

Interpretation: the minimal embedding has **weak open-set separation**. This is a valid negative/limiting result. Do not tune the threshold against unknown test data.

## Files added/updated in this milestone
- `src/smorffi_d4.py`
- `scripts/run_smorffi_d4.py`
- `scripts/make_smorffi_manifest.py`
- `tests/test_d4_contracts.py`
- `configs/track_a_d4_baseline.json`
- `experiments/track_a/d4_manifest.json`
- `experiments/track_a/d5_metrics.json`
- `experiments/track_a/d5_full_metrics.json`
- `experiments/track_a/d5_nn_per_device.md`
- `experiments/track_a/d5_nn_confusion_matrix.csv`
- `experiments/track_a/d6_metrics.json`
- `docs/04_research/D4_LEARNED_REPRESENTATION_BASELINE.md`
- `docs/04_research/D5_CLOSED_SET_IDENTITY.md`
- `docs/04_research/D6_OPEN_SET_UNKNOWN_REJECTION.md`
- `PROJECT_STATE.md`

No raw 356 MB archive is committed to the repository. The archive hash and exact 33-device snapshot definition are recorded for provenance.

## Next stage — D7
D7 should begin from the **frozen D4 embedding and D5/D6 baselines**. Do not alter D4 to improve D5/D6.

First determine which distribution-shift axes are actually observable in the supplied SMoRFFI data. Do not call device-number holdout a temporal/session/receiver shift unless the source exposes that boundary. Use Track B datasets for stronger shift claims.

D7 should measure degradation from the D5 closed-set baseline under an explicitly defined, reproducible shift and preserve a frozen evaluation partition.

## Scientific status discipline
Every stage must be labelled:
1. Implemented
2. Tested
3. Demonstrated
4. Scientifically Validated

Current D4–D6 stages are at **Demonstrated**, not Scientifically Validated.

## Novelty boundary
Candidate contribution remains provisional:
> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile-poisoning while preserving legitimate adaptation.**

D8/D9 remain the primary stages for supporting or falsifying this hypothesis.

## Branch rule
Significant milestones are developed on `develop` first. **Do not synchronize `main` until the milestone is explicitly agreed.** Synchronization means content equivalence without deletion or silent rollback of earlier information.

**Current state:** D4–D6 milestone is committed on `develop`; `main` has intentionally not been synchronized yet.

## Next-chat continuation prompt

> Continue the RF Fingerprinting Project from the canonical GitHub state. First read `PROJECT_STATE.md`, `CURRENT_HANDOFF.md`, `docs/04_research/LEARNING_GATES.md`, `docs/04_research/D2_2_SMORFFI_SCHEMA_EVIDENCE.md`, `docs/04_research/D2_3_PREPROCESSING_CONTRACT.md`, `docs/04_research/D2_4_LEAKAGE_SAFE_SPLIT.md`, `docs/04_research/D2_5_INTEGRATED_ACCEPTANCE.md`, `docs/04_research/D4_LEARNED_REPRESENTATION_BASELINE.md`, `docs/04_research/D5_CLOSED_SET_IDENTITY.md`, and `docs/04_research/D6_OPEN_SET_UNKNOWN_REJECTION.md`. D2 is passed and D4–D6 Track-A baselines are frozen. Do not redo D1/D2 or assume the SMoRFFI schema. Continue directly with D7 controlled distribution-shift experiments using the frozen D4 embedding, D5 identity baselines and D6 rejection baseline. First inspect what shift axes are actually exposed by the available data; do not label device-number differences as temporal/session/receiver shifts without source evidence. Maintain Track A/Track B separation, provenance, leakage controls, frozen test evaluation, novelty boundaries, and Implemented/Tested/Demonstrated/Scientifically Validated discipline. Do not silently delete or overwrite existing information. Develop on `develop` and synchronize `main` only after the milestone is explicitly agreed.`
