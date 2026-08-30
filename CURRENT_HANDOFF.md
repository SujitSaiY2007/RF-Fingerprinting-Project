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

## D4–D7 evidence that is frozen
### D4 learned embedding
Minimal CNN on frozen 2x288 I/Q, 32-D embedding. Test accuracy **35.8086%**. Historical ~91.12% remains **unreconstructed**, because the exact historical 10,186-row selection and historical configuration are not recoverable.

### D5 closed-set identity
Learned embedding:
- classifier 35.81% accuracy, 31.58% macro-F1, 35.80% balanced accuracy;
- nearest centroid 36.21%, 33.23%, 36.30%;
- 1-NN **63.77%**, **63.63%**, **63.80%**.

Classical D3 RF features + fixed Random Forest:
- 16 deterministic features;
- 100 trees, `random_state=20260830`, `max_features=sqrt`, no tuning;
- **87.39% accuracy**, **87.32% macro-F1**, **87.41% balanced accuracy**.

This RF result is the primary Track-A closed-set baseline. It is close to, but does not reproduce, the historical ~91.1% result.

### D6 open-set
Known = devices 1–33; unknown = devices 34–123.

Learned-embedding centroid gate: threshold `21.2566452`, known acceptance **95.42%**, unknown rejection **10.99%**.

RF confidence gate: threshold `0.30`, known acceptance **94.90%**, unknown rejection **29.49%**.

Conclusion: closed-set RF strength does not imply strong unknown-device rejection.

### D7 Track-A synthetic robustness
Frozen D5 RF was tested without retraining/test tuning.

Gain stress: baseline 87.39%; -6 dB 38.07%; -3 dB 27.30%; +3 dB 20.06%; +6 dB 15.93%.

AWGN: 20 dB 82.29%; 10 dB 53.34%; 5 dB 20.44%; 0 dB 6.73%.

Conclusion: the current RF feature baseline is highly acquisition-sensitive. These are controlled engineering stresses, **not** real temporal/receiver/environment claims.

## D7 -> D8 decision
The D7 result establishes the exact motivation for D8:

> Strong closed-set discrimination is not sufficient if the system cannot distinguish transmitter-specific evidence from acquisition-dependent variation.

Therefore D8 must not simply “keep retraining.” It must implement **profile evolution with an explicit authorization decision** and preserve a frozen evaluation partition. This follows the project’s research question:

`RF observation -> identify device -> decide whether observation is safe to learn from -> update / hold / reject`

The candidate novelty remains provisional and must be supported/falsified through comparison with strong baselines.

## D8 — exact work to perform next
1. Implement a persistent device profile manager.
2. Profile state must include at least: device identity, representative embedding/RF-feature statistics, dispersion/consistency statistics, observation count, profile version, and update audit history.
3. Separate recognition from update authorization.
4. Implement three outcomes: **ACCEPT/UPDATE**, **HOLD/QUARANTINE**, **REJECT**.
5. Create chronological update streams from SMoRFFI observations plus explicitly labelled controlled shifts.
6. Freeze evaluation data before any update stream is processed.
7. Compare this baseline ladder:
   - frozen/no-update;
   - always-update after recognition;
   - confidence-only admission;
   - multi-evidence authorization.
8. Measure both adaptation benefit and profile damage.

Minimum D8 metrics:
- identity accuracy before/after evolution;
- profile displacement/drift;
- legitimate new-observation acceptance;
- rejection/hold rate;
- performance under controlled shifts;
- rollback success where enabled.

## D9 — exact work to perform after D8
Use legitimate SMoRFFI observations plus controlled/synthetic attack construction. Do not search for a special poisoning dataset.

Attack families:
- label contamination;
- unknown-device contamination into a known profile;
- gradual embedding/feature drift;
- suspicious replay/repetition.

Use the same D8 baseline ladder. Measure:
- attack acceptance;
- profile drift/displacement;
- post-attack identity accuracy;
- false acceptance of unknowns;
- legitimate-observation acceptance after attack;
- rollback/recovery;
- legitimate adaptation preserved.

The experiment must be capable of falsifying the novelty hypothesis. Do not tune attack parameters to guarantee a positive result.

## D10 — exact integration target
Build one auditable Track-A lifecycle:

`SMoRFFI observation -> D2 -> D3 RF evidence + D4 embedding -> D5 identity -> D6 known/unknown -> D8 profile lookup -> update authorization -> D9 poisoning defense -> audit/final decision`

The demonstrator must show at minimum:
- known legitimate sample identified and accepted;
- unknown sample rejected or quarantined;
- legitimate later observations can evolve a profile;
- suspicious/poisoned observations are blocked or quarantined;
- profile versions and decisions are auditable;
- frozen evaluation data are never consumed by the updater before evaluation.

D10 is a systems demonstration, not automatic scientific validation.

## Track A / Track B boundary
### Track A
Goal: complete a small, defensible, reproducible D1–D10 software lifecycle using SMoRFFI plus controlled/derived scenarios and paper-grounded experimental design.

### Track B
Goal: test whether the Track-A claims survive independently collected real-world variation. Use qualified datasets only when a concrete gap requires them.

Current real-world gaps:
- actual day/session boundaries;
- actual receiver variation;
- actual environment variation;
- cross-dataset transfer.

Do not label synthetic transformations as these real-world conditions.

## Scientific status discipline
Use exactly four maturity labels:
1. **Implemented**
2. **Tested**
3. **Demonstrated**
4. **Scientifically Validated**

Current D4–D7 Track-A artifacts are at **Demonstrated**, not Scientifically Validated. D8–D10 will start as Implemented and advance only when evidence justifies it.

## Historical-result discipline
The historical values remain preserved, not deleted:
- approximately 91.12% D4 exploratory result;
- approximately 90.9% earlier RF exploratory result;
- approximately 60 historical features.

The exact historical dataset selection/configuration is not recoverable. Do not fabricate or silently infer missing details. The current reproducible RF baseline is 87.39% on the frozen 33-device protocol.

## Repository records to use first
For the next chat read:
- `PROJECT_STATE.md`
- `CURRENT_HANDOFF.md`
- `docs/04_research/D7_D10_TRACK_A_NEXT_DIRECTION.md`
- `docs/04_research/D4_LEARNED_REPRESENTATION_BASELINE.md`
- `docs/04_research/D5_CLOSED_SET_IDENTITY.md`
- `docs/04_research/D5_RANDOM_FOREST_CLASSICAL_BASELINE.md`
- `docs/04_research/D6_OPEN_SET_UNKNOWN_REJECTION.md`
- `docs/04_research/D6_RF_OPEN_SET_BASELINE.md`
- `docs/04_research/D7_RF_DISTRIBUTION_SHIFT.md`
- relevant configs/metrics under `configs/` and `experiments/track_a/`

## Exact next-chat continuation prompt

> Continue the RF Fingerprinting Project from the canonical GitHub state of `SujitSaiY2007/RF-Fingerprinting-Project`. First read `PROJECT_STATE.md`, `CURRENT_HANDOFF.md`, and `docs/04_research/D7_D10_TRACK_A_NEXT_DIRECTION.md`, then read the existing D4–D7 evidence documents/configs/metrics before modifying anything. D2 learning gate is PASSED and the frozen D2 contract is `serialized preamble -> complex[288] -> float32[2,288] I/Q`; do not redo D1/D2 or assume a new schema. The historical ~91.1% result remains historical/unreconstructed; the current frozen Track-A RF baseline is 87.39% closed-set on devices 1–33, with D6 RF unknown rejection 29.49% at ~94.90% known acceptance and D7 synthetic gain/AWGN stress showing strong degradation. Track A is now explicitly allowed to complete D8–D10 using real SMoRFFI data, controlled/derived synthetic scenarios, and published-paper evidence; additional multi-gigabyte datasets are not required to unblock Track-A. A constructed dataset must be labelled synthetic/derived and never represented as a measurement from the cited paper/dataset. Track B remains for real temporal/environment/receiver/cross-dataset validation using qualified datasets only when a concrete gap requires them. Proceed directly with D8 profile evolution: implement persistent profiles, recognition vs update authorization separation, ACCEPT/HOLD/REJECT decisions, chronological update streams, frozen evaluation, and the required baseline ladder of frozen/no-update, always-update, confidence-only admission, and multi-evidence authorization. Then run D9 controlled/synthetic poisoning against that ladder and D10 the integrated auditable lifecycle. Preserve provenance, leakage controls, frozen evaluation, novelty boundaries, and the Implemented/Tested/Demonstrated/Scientifically Validated discipline. Do not silently delete or overwrite prior information. Develop on `develop`; synchronize `main` only after an explicitly agreed milestone.`

## Branch rule
Significant work lands on `develop` first. When a milestone is explicitly agreed, synchronize `main` and `develop` to the same **content state** without deleting or silently reverting earlier information. Never force-push protected `main`.
