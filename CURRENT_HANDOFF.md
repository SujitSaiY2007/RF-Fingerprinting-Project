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

Baseline preprocessing remains: no per-observation normalization, clipping, filtering, resampling or arbitrary interpolation. Device number and MAC remain labels/provenance only. The Track-A engineering split is deterministic SHA-256 over `(device_id, source_row_index)` with 70/15/15 and is explicitly **not** a temporal/session split.

## Dataset situation and policy
The complete user-supplied SMoRFFI archive is the executable Track-A source: 123 CSV files, 122,511 rows, 123 devices, archive SHA-256 `1d9ebcf2539e5fb7fb1dc678dba3fd2a50cada2befb86f5d84faff2b4f541037`. Track-A known devices are 1–33: 33 files, 33,000 rows; split 23,030/4,974/4,996.

The project will **not** block Track-A on multi-gigabyte external datasets. Published papers may be used to justify shift/attack mechanisms and to construct controlled derived datasets, provided those datasets are explicitly labelled synthetic/derived. Published empirical results remain external evidence and are never presented as our own measurements.

Track B remains responsible for real temporal/environment/receiver/cross-dataset validation. First candidates remain Oregon State WiFi RFFP and WiSig/ManySig; SmartHomePrivacy is an optional smaller cross-day source. No unrestricted dataset hunt is permitted.

## Frozen evidence through D7
### D4 learned embedding
Minimal CNN on frozen 2x288 I/Q, 32-D embedding. Test accuracy **35.8086%**. Historical ~91.12% remains **unreconstructed**, because the exact historical 10,186-row selection and historical configuration are not recoverable.

### D5 closed-set identity
Learned embedding: classifier 35.81% accuracy, 31.58% macro-F1, 35.80% balanced accuracy; nearest centroid 36.21%, 33.23%, 36.30%; 1-NN **63.77%**, **63.63%**, **63.80%**.

Classical D3 RF features + fixed Random Forest: 16 deterministic features; 100 trees, `random_state=20260830`, `max_features=sqrt`, no tuning; **87.39% accuracy**, **87.32% macro-F1**, **87.41% balanced accuracy**. This is the primary Track-A closed-set baseline. Historical ~91.1% remains unreconstructed.

### D6 open-set
Known = devices 1–33; unknown = devices 34–123.

Learned-embedding centroid gate: threshold `21.2566452`, known acceptance **95.42%**, unknown rejection **10.99%**.

RF confidence gate: threshold `0.30`, known acceptance **94.90%**, unknown rejection **29.49%**.

Conclusion: closed-set RF strength does not imply strong unknown-device rejection.

### D7 Track-A synthetic robustness
Frozen D5 RF was tested without retraining/test tuning.

Gain stress: baseline 87.39%; -6 dB 38.07%; -3 dB 27.30%; +3 dB 20.06%; +6 dB 15.93%.

AWGN: 20 dB 82.29%; 10 dB 53.34%; 5 dB 20.44%; 0 dB 6.73%.

Conclusion: the RF feature baseline is strongly acquisition-sensitive. These are controlled engineering stress results, not real temporal/receiver/environment measurements.

## D7 -> D8 decision
D7 establishes the motivating engineering problem:

> Strong closed-set discrimination is not sufficient if the system cannot distinguish transmitter-specific evidence from acquisition-dependent variation.

Therefore D8 must implement **profile evolution with an explicit update-authorization decision**, not simply continuous retraining. The project question remains:

`RF observation -> identify device -> decide whether observation is safe to learn from -> update / hold / reject`

The novelty claim remains provisional and must be compared against strong admission/update baselines.

## D8 exact next work
Implement a persistent profile manager with at least identity, representation/RF-feature statistics, dispersion/consistency, observation count, version and audit history. Separate recognition from update authorization. Support **ACCEPT/UPDATE**, **HOLD/QUARANTINE**, and **REJECT**.

Create chronological update streams from SMoRFFI observations plus explicitly labelled controlled shifts. Freeze evaluation before update streams. Compare: (1) frozen/no-update, (2) always-update after recognition, (3) confidence-only admission, (4) proposed multi-evidence authorization.

Measure identity performance before/after evolution, profile drift/displacement, legitimate-observation acceptance, hold/reject rate, shift performance and rollback where enabled.

## D9 exact next work after D8
Use legitimate RF observations plus controlled/synthetic poisoning; no special poisoning dataset is required. Attack families: label contamination, unknown-device contamination into a known profile, gradual representation/feature drift, and suspicious replay/repetition.

Use the same D8 baseline ladder. Measure attack acceptance, profile drift, post-attack accuracy, unknown false acceptance, legitimate acceptance after attack, rollback/recovery and preserved legitimate adaptation.

The experiment must be able to falsify the novelty hypothesis. Do not tune attacks to guarantee a positive outcome.

## D10 exact integration target
Build one auditable lifecycle:

`SMoRFFI observation -> D2 -> D3 RF evidence + D4 embedding -> D5 identity -> D6 known/unknown -> D8 profile lookup -> update authorization -> D9 poisoning defense -> audit/final decision`

The demonstrator must show known legitimate acceptance, unknown rejection/quarantine, legitimate profile evolution, suspicious-update blocking/quarantine, auditable profile versions/decisions, and protection of frozen evaluation data.

D10 is an integrated Track-A demonstration, not automatic scientific validation.

## Track A / Track B boundary
Track A completes the smallest reproducible D1–D10 software lifecycle using SMoRFFI, controlled/derived scenarios and paper-grounded experimental design. Track B tests whether claims survive independently collected real-world variation.

Current Track-B gaps: actual day/session boundaries, actual receiver variation, actual environment variation and cross-dataset transfer.

Do not label synthetic transformations as those real-world conditions.

## Scientific status discipline
Use exactly four maturity labels:
1. **Implemented**
2. **Tested**
3. **Demonstrated**
4. **Scientifically Validated**

D4–D7 Track-A results are **Demonstrated**, not Scientifically Validated. D8–D10 must advance only when evidence justifies it.

## Historical-result discipline
Preserve historical values but do not certify them: approximately 91.12% D4, approximately 90.9% earlier RF result, approximately 60 historical RF features. Missing historical row selection/configuration must not be invented.

## Canonical next-direction document
The detailed, non-overlapping continuation plan is:
`docs/04_research/D7_D10_TRACK_A_NEXT_DIRECTION.md`

Read it together with `PROJECT_STATE.md` before starting the next chat. It is the authoritative work breakdown for D7→D10 and the dataset/acquisition policy.

## Exact next-chat continuation prompt

> Continue the RF Fingerprinting Project from the canonical GitHub state of `SujitSaiY2007/RF-Fingerprinting-Project`. First read `PROJECT_STATE.md`, `CURRENT_HANDOFF.md`, and `docs/04_research/D7_D10_TRACK_A_NEXT_DIRECTION.md`, then read the existing D4–D7 evidence documents/configs/metrics before modifying anything. D2 learning gate is PASSED and the frozen D2 contract is `serialized preamble -> complex[288] -> float32[2,288] I/Q`; do not redo D1/D2 or assume a new schema. The historical ~91.1% result remains historical/unreconstructed; the current frozen Track-A RF baseline is 87.39% closed-set on devices 1–33, with D6 RF unknown rejection 29.49% at ~94.90% known acceptance and D7 synthetic gain/AWGN stress showing strong degradation. Track A is explicitly allowed to complete D8–D10 using real SMoRFFI data, controlled/derived synthetic scenarios, and published-paper evidence; additional multi-gigabyte datasets are not required to unblock Track-A. A constructed dataset must be labelled synthetic/derived and never represented as a measurement from the cited paper/dataset. Track B remains for real temporal/environment/receiver/cross-dataset validation using qualified datasets only when a concrete gap requires them. Proceed directly with D8 profile evolution: implement persistent profiles, recognition vs update-authorization separation, ACCEPT/HOLD/REJECT decisions, chronological update streams, frozen evaluation, and the baseline ladder of frozen/no-update, always-update, confidence-only admission, and multi-evidence authorization. Then run D9 controlled/synthetic poisoning against that ladder and D10 the integrated auditable lifecycle. Preserve provenance, leakage controls, frozen evaluation, novelty boundaries, and the Implemented/Tested/Demonstrated/Scientifically Validated discipline. Do not silently delete or overwrite prior information. Develop on `develop`; synchronize `main` only after an explicitly agreed milestone.`

## Branch state
`main` and `develop` are synchronized to the same **content state** for the D4–D7 consolidation. Their histories remain non-linear because synchronization used a two-parent merge commit; both histories are preserved. Develop remains the working branch for future milestones.
