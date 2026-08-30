# PROJECT STATE

**Last updated:** 2026-08-30

## Authoritative status
- Repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Stable branch: `main`
- Integration branch: `develop`
- Phase: **Version B — security-first improvement / demonstrator construction**
- D2 learning gate: **PASSED**
- D7 Track A: **COMPLETE / DEMONSTRATED**
- B0: **COMPLETE / DEMONSTRATED — Version-A control reproduced**
- B1-B2: **COMPLETE AS MODEL-SELECTION SCREENING / DEMONSTRATED — no learned candidate justified replacing the RF control**
- Current engineering gate: **D8 profile evolution / protected update authorization**
- D3–D10 scientific validation: **not yet complete**

## Frozen D2 contract
`serialized preamble -> complex[288] -> float32[2,288] I/Q`

Do not restart D1/D2 or silently change the input schema. Baseline preprocessing remains without per-observation normalization, clipping, filtering, resampling or arbitrary interpolation. Device number/MAC is label/provenance only.

## Version-A frozen reference
SMoRFFI known devices 1–33; deterministic 70/15/15 engineering split; 16 deterministic RF evidence features; fixed Random Forest: 100 trees, `random_state=20260830`, `max_features=sqrt`, no tuning.

- Accuracy: **87.3899%**
- Macro-F1: **87.3226%**
- Balanced accuracy: **87.4117%**
- D6 RF confidence threshold: **0.30**
- Known acceptance: **94.90%**
- Unknown rejection: **29.49%**

Historical ~91.1% remains historical/unreconstructed and is not a certified result.

## Version-B B0-B2 result
The frozen benchmark contract is `configs/version_b_b0_b2_benchmark.json`.

B0 reproduced the RF control on 33,000 known-device observations: 23,030 train / 4,974 validation / 4,996 test.

B1-B2 candidate screening used the same real SMoRFFI source substrate and frozen I/Q contract. Full recorded results are in `experiments/track_a/version_b_b1_b2_results.json`.

### M0 — Version-A RF control
Retained as the strongest demonstrated Track-A recognition mechanism: 87.39% closed-set accuracy and 29.49% unknown rejection at the frozen 0.30 confidence threshold.

### M1 — compact I/Q CNN
15 epochs on raw frozen I/Q:
- 7.07% accuracy
- 2.95% macro-F1
- 7.05% balanced accuracy
- open-set AUROC 0.4582
- unknown rejection 2.74% at validation-calibrated confidence threshold

**Decision: rejected as Version-B replacement.**

### M2 — I/Q metric/prototype head
15 epochs:
- 8.83% accuracy
- 2.05% macro-F1
- 8.53% balanced accuracy
- open-set AUROC 0.5718
- unknown rejection 6.27% at validation-calibrated prototype-distance threshold

**Decision: rejected as Version-B replacement.**

### M3 — supervised-contrastive prototype screening
3 completed CPU epochs:
- 57.29% accuracy
- 55.77% macro-F1
- 57.01% balanced accuracy
- open-set AUROC 0.6366
- unknown rejection 9.91% at validation-calibrated prototype-distance threshold

The longer SupCon run could not be completed within the available execution budget. Therefore M3 is **not a certified winner** and must not be represented as fully optimized. It remains a literature-informed future candidate rather than a reason to block Track-A D8-D10.

### B1-B2 selection decision
**Do not replace the RF recognition backbone.** The executed Track-A evidence does not justify a learned I/Q replacement. M1/M2 were decisively weaker; M3 screening was promising relative to M1/M2 but still materially below the RF control and incompletely trained.

This does **not** prove RF is globally optimal. It establishes only that a replacement is not justified by the executed benchmark. Version B therefore concentrates its improvement effort on the identified weaknesses: **open-set security, fingerprint-purity diagnostics, protected adaptive profiles and poisoning resistance**, while retaining the RF mechanism as the recognition control/backbone.

This is a legitimate negative model-selection result and must remain in the audit trail.

## Version-B architecture decision
Working Track-A architecture:

`SMoRFFI observation -> D2 -> D3 RF evidence / RF recognition -> open-set novelty decision -> D8 update authorization -> persistent profile -> D9 poisoning defense -> audit/final decision`

The RF recognition mechanism is retained for Version B. Novelty/security mechanisms are allowed to evolve aggressively.

The final deliverable remains a research-demonstrator web application separated from the RF engine. Planned UI surfaces: Dashboard, Identification, Device Profiles, Open-Set Security, Security/Attack Lab, Audit Trail and Evaluation/Research. UI architecture is documented in `docs/04_research/VERSION_B_RESEARCH_SPECIFICATION.md`.

## Immediate next execution: D8
Build chronological persistent profiles using real SMoRFFI observations plus explicitly labelled controlled/derived scenarios.

Profile state:
- identity
- RF-feature statistics
- representation/statistics where available
- observation count
- dispersion/consistency
- profile version
- update audit history

Separate:
`OBSERVATION -> RECOGNITION -> UPDATE AUTHORIZATION -> PROFILE UPDATE`

Required decisions:
- ACCEPT / UPDATE
- HOLD / QUARANTINE
- REJECT

Required baseline ladder:
1. frozen/no-update;
2. always-update;
3. confidence-only;
4. multi-evidence authorization.

Freeze the evaluation set before chronological update streams. Never let future evaluation observations update a profile before evaluation.

## D9 next
Controlled/synthetic poisoning against the same D8 ladder:
- unknown-device contamination;
- wrong-label contamination;
- gradual target-like drift;
- replay/repetition.

Measure attack acceptance, profile displacement, identity degradation, false acceptance, legitimate acceptance, rollback/recovery and legitimate adaptation retained.

## D10 next
Integrate:
`observation -> D2 -> RF recognition -> open set -> profile -> authorization -> poisoning defense -> audit`

Demonstrate known acceptance, unknown rejection/quarantine, legitimate adaptation, suspicious-update blocking and auditable profile versions/decisions.

D10 remains demonstration, not automatic scientific validation.

## Data/evidence policy
Track A may use real SMoRFFI, controlled/derived synthetic scenarios and published-paper evidence. Synthetic/derived observations must never be represented as source-dataset measurements.

Track B remains responsible for real temporal/session/environment/receiver/cross-dataset validation. No additional multi-gigabyte dataset is required to unblock Track-A D8-D10.

## Completion discipline
Use exactly: **Implemented / Tested / Demonstrated / Scientifically Validated**. Do not upgrade evidence level silently.

## Branch rule
`develop` is the active implementation branch. `main` must only be synchronized after an explicitly agreed milestone. No force-push or destructive history rewrite.
