# CURRENT HANDOFF — 2026-08-30

## Project
**Physics-Based RF Fingerprinting with Continuous Device Learning**

## Canonical repository state
- Repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Stable branch: `main`
- Integration branch: `develop`
- Phase: **Phase 1 — Accelerated implementation / demonstrator construction**
- D2 learning gate: **PASSED**
- Current execution point: **Version-B benchmark B0 complete; B1–B2 candidate evaluation remains the active execution gate before backbone selection**

## Do not restart
Do **not** redo D1/D2, re-derive the SMoRFFI schema, or replace the D2 contract. The frozen Track-A representation is:
`serialized preamble -> complex[288] -> float32[2,288] I/Q`

Baseline preprocessing: no per-observation normalization, clipping, filtering, resampling or arbitrary interpolation. Device number and MAC remain labels/provenance only. Track-A engineering split: deterministic SHA-256 over `(device_id, source_row_index)` with 70/15/15; explicitly **not** a temporal/session split.

## Version-B benchmark status
### B0 — REPRODUCIBILITY CONTROL: COMPLETE / DEMONSTRATED
The supplied SMoRFFI archive was used as the real source substrate. The frozen Version-A RF control was reproduced exactly under the repository configuration:

- known devices: 1–33
- rows: 33,000
- train/validation/test: 23,030 / 4,974 / 4,996
- 16 deterministic RF evidence features
- Random Forest: 100 trees, `random_state=20260830`, `max_features=sqrt`, no tuning
- test accuracy: **87.3899%**
- macro-F1: **87.3226%**
- balanced accuracy: **87.4117%**

Frozen D6 open-set reference remains:
- threshold `0.30`
- known acceptance approximately **94.90%**
- unknown rejection **29.49%**

The complete B0 record is `experiments/track_a/version_b_b0_results.json`; the frozen benchmark contract is `configs/version_b_b0_b2_benchmark.json`.

### B1 — CLOSED-SET CANDIDATE BENCHMARK: NEXT
Candidates remain:
1. M0 Version-A RF control;
2. M1 compact 1-D CNN on frozen I/Q;
3. M2 I/Q encoder + metric/prototype head;
4. M3 I/Q encoder + supervised contrastive objective + prototype/open-set head.

Required metrics: accuracy, macro-F1, balanced accuracy, per-device metrics, confusion matrix and seed variance.

### B2 — OPEN-SET CANDIDATE BENCHMARK: NEXT
The same candidates must be evaluated under one frozen open-set protocol. Thresholds are selected from known validation only. Unknown test observations are never used for model or threshold selection.

Required metrics: known acceptance, unknown rejection, false acceptance, AUROC, AUPR and OSCR/equivalent open-set curve where applicable.

**No Version-B backbone is selected before B1/B2 candidate evidence is available.**

## Dataset and evidence policy
Complete supplied SMoRFFI archive: 123 CSV files, 122,511 rows, 123 devices; archive SHA-256 `1d9ebcf2539e5fb7fb1dc678dba3fd2a50cada2befb86f5d84faff2b4f541037`. Track-A known snapshot: devices 1–33, 33 files, 33,000 rows; 23,030/4,974/4,996 split.

Track A does not block on multi-gigabyte external datasets. It may use real SMoRFFI, controlled/derived synthetic scenarios, and published-paper evidence for experimental design. A constructed dataset must be labelled synthetic/derived and never represented as a measurement from the cited paper/dataset.

Track B is reserved for real temporal/session/environment/receiver/cross-dataset validation. First candidates remain Oregon State WiFi RFFP and WiSig/ManySig; SmartHomePrivacy is optional. No unrestricted dataset hunt.

## Frozen D4–D7 evidence
### D4
Minimal frozen 32-D CNN embedding from 2x288 I/Q. Reproducible test accuracy **35.8086%**. Historical ~91.12% remains historical/unreconstructed because the exact prior 10,186-row selection and configuration are unavailable.

### D5
Learned embedding: classifier 35.81%, centroid 36.21%, 1-NN **63.77%** accuracy.

Classical D3 features + fixed RF (16 features; 100 trees; `random_state=20260830`; `max_features=sqrt`; no tuning): **87.39% accuracy**, **87.32% macro-F1**, **87.41% balanced accuracy**. This is the primary Track-A closed-set baseline.

### D6
D4 centroid gate: known acceptance **95.42%**, unknown rejection **10.99%**, threshold `21.2566452` from known validation only.

RF confidence gate: known acceptance **94.90%**, unknown rejection **29.49%**, threshold `0.30` from known validation only.

Conclusion: strong closed-set RF performance does not imply strong open-set rejection.

### D7
Frozen D5 RF under controlled gain stress: 87.39% baseline; -6 dB 38.07%; -3 dB 27.30%; +3 dB 20.06%; +6 dB 15.93%.

Frozen D5 RF under AWGN: 20 dB 82.29%; 10 dB 53.34%; 5 dB 20.44%; 0 dB 6.73%.

Conclusion: the current RF feature baseline is strongly acquisition-sensitive. These are controlled engineering stresses, not real temporal/receiver/environment evidence.

## D7 -> D8 decision
The D7 result establishes the key motivation: strong closed-set discrimination is insufficient if the system cannot distinguish transmitter-specific evidence from acquisition-dependent variation.

D8 therefore must implement **profile evolution plus explicit authorization to modify persistent identity state**, rather than unconditional continual retraining.

## D8 exact work
Implement persistent device profiles containing identity, representation/RF-feature statistics, dispersion/consistency, observation count, profile version and audit history.

Separate:
`OBSERVATION -> IDENTITY RECOGNITION -> UPDATE AUTHORIZATION -> PROFILE UPDATE`

Decision outcomes: **ACCEPT/UPDATE**, **HOLD/QUARANTINE**, **REJECT**.

Create chronological streams from real SMoRFFI observations plus explicitly labelled controlled shifts. Freeze evaluation before update streams are processed.

Compare exactly this baseline ladder:
1. frozen/no-update;
2. always-update after recognition;
3. confidence-only admission;
4. proposed multi-evidence authorization.

Measure identity performance before/after evolution, profile drift/displacement, legitimate-observation acceptance, hold/reject rate, shift performance and rollback/recovery where implemented.

## D9 exact work
Use legitimate RF observations plus controlled/synthetic poisoning; no special poisoning dataset is required.

Attack families: label contamination, unknown-device contamination, gradual representation/feature drift, suspicious replay/repetition.

Compare the same D8 baseline ladder. Measure attack acceptance, profile drift, post-attack identity accuracy, unknown false acceptance, legitimate acceptance after attack, rollback/recovery and legitimate adaptation preserved.

The experiment must be capable of falsifying the novelty hypothesis.

## D10 exact integration target
`SMoRFFI observation -> D2 -> D3 RF evidence + D4 embedding -> D5 identity -> D6 known/unknown -> D8 profile lookup -> update authorization -> D9 poisoning defense -> audit/final decision`

Demonstrate known legitimate acceptance, unknown rejection/quarantine, legitimate profile evolution, suspicious-update blocking/quarantine, auditable profile versions/decisions and protection of frozen evaluation data.

D10 is an integrated Track-A demonstration, not automatic scientific validation.

## Scientific status discipline
Use exactly: **Implemented / Tested / Demonstrated / Scientifically Validated**.

D4–D7 Track-A results are **Demonstrated**, not Scientifically Validated. B0 is now **Demonstrated**. B1/B2 remain incomplete until candidate runs finish under the frozen protocol.

## Historical-result discipline
Preserve, but do not certify, the historical values: approximately 91.12% D4, approximately 90.9% earlier RF result, approximately 60 historical RF features. Never invent or modify the missing 10,186-row selection, feature list or configuration.

## Canonical detailed direction
`docs/04_research/D7_D10_TRACK_A_NEXT_DIRECTION.md` remains the authoritative D7–D10 work breakdown. `docs/04_research/VERSION_B_RESEARCH_SPECIFICATION.md` is the authoritative Version-B research/evaluation specification, including the added UI/application architecture.

## Branch state
Develop is the active working branch. The current Version-B benchmark additions are on `develop`. `main` is not synchronized for this milestone because the agreed rule is to synchronize only after an explicitly agreed milestone.
