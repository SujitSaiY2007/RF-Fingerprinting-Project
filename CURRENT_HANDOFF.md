# CURRENT HANDOFF — 2026-08-30

## Project
**Physics-Based RF Fingerprinting with Continuous Device Learning**

## Canonical repository state
- Repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Stable branch: `main`
- Integration branch: `develop`
- Phase: **Phase 1 — Accelerated implementation / demonstrator construction**
- D2 learning gate: **PASSED**
- Current execution point: **D7 complete at Track-A synthetic-stress scope; remaining Track-A critical path is D8 -> D9 -> D10**

## Do not restart
Do **not** redo D1/D2, re-derive the SMoRFFI schema, or replace the D2 contract. The frozen Track-A representation is:
`serialized preamble -> complex[288] -> float32[2,288] I/Q`

Baseline preprocessing: no per-observation normalization, clipping, filtering, resampling or arbitrary interpolation. Device number and MAC remain labels/provenance only. Track-A engineering split: deterministic SHA-256 over `(device_id, source_row_index)` with 70/15/15; explicitly **not** a temporal/session split.

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

D4–D7 Track-A results are **Demonstrated**, not Scientifically Validated. D8–D10 start at Implemented and advance only when evidence supports the higher status.

## Historical-result discipline
Preserve, but do not certify, the historical values: approximately 91.12% D4, approximately 90.9% earlier RF result, approximately 60 historical RF features. Never invent the missing 10,186-row selection, feature list or configuration.

## Canonical detailed direction
`docs/04_research/D7_D10_TRACK_A_NEXT_DIRECTION.md` is the authoritative D7–D10 work breakdown and must be read before starting new work.

## Required next-chat reading
- `PROJECT_STATE.md`
- `CURRENT_HANDOFF.md`
- `docs/04_research/D7_D10_TRACK_A_NEXT_DIRECTION.md`
- `docs/04_research/D4_LEARNED_REPRESENTATION_BASELINE.md`
- `docs/04_research/D5_CLOSED_SET_IDENTITY.md`
- `docs/04_research/D5_RANDOM_FOREST_CLASSICAL_BASELINE.md`
- `docs/04_research/D6_OPEN_SET_UNKNOWN_REJECTION.md`
- `docs/04_research/D6_RF_OPEN_SET_BASELINE.md`
- `docs/04_research/D7_RF_DISTRIBUTION_SHIFT.md`
- related configs and metrics under `configs/` and `experiments/track_a/`

## Exact next-chat continuation prompt

> Continue the RF Fingerprinting Project from the canonical GitHub state of `SujitSaiY2007/RF-Fingerprinting-Project`. Read `PROJECT_STATE.md`, `CURRENT_HANDOFF.md`, and `docs/04_research/D7_D10_TRACK_A_NEXT_DIRECTION.md` first, then inspect the existing D4–D7 evidence/configuration before modifying anything. D2 learning gate is PASSED; the frozen D2 input is `serialized preamble -> complex[288] -> float32[2,288] I/Q`; do not redo D1/D2 or assume a new schema. Historical ~91.1% remains historical/unreconstructed. Current frozen Track-A RF baseline is 87.39% closed-set on devices 1–33; D6 RF unknown rejection is 29.49% at ~94.90% known acceptance; D7 synthetic gain/AWGN tests show strong acquisition sensitivity. Track A is explicitly allowed to complete D8–D10 using real SMoRFFI, controlled/derived synthetic scenarios, and published-paper evidence. Additional multi-gigabyte datasets are not required to unblock Track-A. Synthetic/derived datasets must be explicitly labelled and never represented as source-dataset measurements. Track B remains for real temporal/session/environment/receiver/cross-dataset validation. Proceed directly with D8 profile evolution: persistent profiles, recognition vs update authorization, ACCEPT/HOLD/REJECT, chronological update streams, frozen evaluation, and the baseline ladder frozen/no-update, always-update, confidence-only, multi-evidence. Then perform D9 controlled/synthetic poisoning and D10 the complete auditable lifecycle. Preserve provenance, leakage controls, frozen evaluation, novelty boundaries and Implemented/Tested/Demonstrated/Scientifically Validated discipline. Do not silently delete or overwrite existing project information. Develop on `develop`; synchronize `main` after an explicitly agreed milestone.`

## Branch state
`main` and `develop` are intended to remain content-equivalent at agreed milestones. For this milestone the content has been synchronized using a two-parent merge so both histories are preserved. Develop remains the working branch for the next milestone.
