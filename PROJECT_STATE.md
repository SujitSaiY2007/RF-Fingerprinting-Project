# PROJECT STATE

**Last updated:** 2026-08-30

## Authoritative status
- Repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Stable branch: `main`
- Integration branch: `develop`
- Phase: **Phase 1 — Accelerated implementation / demonstrator construction**
- Current engineering gate: **D7 — Track-A synthetic stress complete; real-shift evidence is Track-B and not required to block Track-A D8–D10 implementation**
- D1: **COMPLETE at source/schema/ingestion-foundation level**
- D2.1: **COMPLETE — sample representation contract**
- D2.2: **OBSERVED / IMPLEMENTED / TESTED on a 20-file SMoRFFI inspection subset**
- D2.3: **DEFINED / IMPLEMENTED / TESTED on the same subset**
- D2.4: **DEFINED / IMPLEMENTED / TESTED as a Track-A engineering split**
- D2.5: **ENGINEERING ACCEPTED on the 20-file subset**
- D3: **IMPLEMENTED / exploratory demonstrated on real SMoRFFI data; scientific validation not complete**
- D4: **IMPLEMENTED / TESTED / DEMONSTRATED with reproducible 33-device Track-A baseline; historical ~91.1% result remains unreproducible**
- D5: **IMPLEMENTED / TESTED / DEMONSTRATED — learned-embedding and classical RF-feature closed-set baselines complete**
- D6: **IMPLEMENTED / TESTED / DEMONSTRATED — learned-embedding and RF open-set baselines complete**
- D7 Track A: **IMPLEMENTED / TESTED / DEMONSTRATED — controlled gain and AWGN stress**
- D7 Track B: **PLANNED / optional — real temporal/domain/receiver shift requires an external dataset with verified condition metadata**
- D8–D10 Track A implementation: **NEXT**
- D3–D10 scientific validation: **not yet complete**
- Team size: 4

## Dataset qualification milestone
The dataset-search/qualification gate is complete. The project uses a portfolio rather than forcing one dataset to answer every research question.

### Primary
- WiSig — scale, receiver variation, multi-day robustness.
- Oregon State WiFi RFFP — temporal/domain variation.
- Oregon State LoRa RFFP — same-model/environment/location/distance/receiver variation.
- SMoRFFI — large-scale same-model discrimination.

### Secondary
- ORACLE — controlled hardware/distance benchmark.
- Bluetooth smartphone RF database — optional cross-technology benchmark.

The portfolio is qualified but dataset acquisition is now demand-driven. No unrestricted dataset hunt is permitted.

## Accelerated execution decision — final form
The project is fast-tracked toward a demonstrable D1–D10 software pipeline.

Execution principle:
> **Build the smallest defensible end-to-end system first, then strengthen individual stages.**

Track A may use three data/evidence sources:
1. real SMoRFFI observations already supplied;
2. controlled/derived synthetic datasets constructed from those observations;
3. published-paper evidence used to justify the choice of shift mechanisms, parameter ranges and attack scenarios.

A constructed dataset is **not** a substitute for a real-world measurement and must never be reported as if it came from the cited paper/dataset.

Track B uses independently collected external datasets when a scientific claim requires metadata or condition boundaries unavailable in Track A.

## Two-track execution model — ACTIVE
### Track A — Fast Implementation / Demonstration
- Current real substrate: SMoRFFI.
- Complete the remaining D7–D10 software path without waiting for multi-gigabyte external datasets.
- Use controlled/derived scenarios where the mechanism itself is the object of the experiment.
- Keep all constructed scenarios explicitly labelled and reproducible.

### Track B — Research Validation / Strengthening
- Use Oregon State WiFi RFFP for real day/environment variation.
- Use WiSig / ManySig for real receiver/day/channel variation.
- Add another qualified dataset only when a concrete metadata, reproducibility or scientific-validity gap is demonstrated.
- Track-B results must never be silently merged into Track-A evidence.

## Completion-level discipline
1. **Implemented** — code/artifact exists.
2. **Tested** — engineering tests or reproducible checks pass.
3. **Demonstrated** — integrated path operates on real or explicitly controlled data.
4. **Scientifically validated** — stage-specific external/independent evidence supports the claim.

Track A accelerates implementation/testing/demonstration. Track B supplies evidence where scientific validation requires broader or independently collected data.

## Novelty status
The candidate contribution remains provisional:
> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile-poisoning while preserving legitimate adaptation.**

D8/D9 remain the primary stages for supporting/falsifying this hypothesis and must use a baseline ladder rather than assuming the proposed policy is superior.

## D1–D10 relationship
`D1 ingestion -> D2 DSP -> D3 RF evidence -> D4 embedding -> D5 identity -> D6 open-set -> D7 shift -> D8 profile evolution -> D9 poisoning -> D10 integration`

## D4 reproducibility closure
The complete user-supplied archive was inspected:
- 123 CSV files
- 122,511 observations
- 123 devices
- archive SHA-256: `1d9ebcf2539e5fb7fb1dc678dba3fd2a50cada2befb86f5d84faff2b4f541037`

Track-A D4 known snapshot: devices **1–33**, 33 files, 33,000 observations, with 23,030/4,974/4,996 train/validation/test under the existing D2 deterministic split.

Source anomalies retained: device 67 has 999 rows; device 87 has 999; device 109 has 513. No anomaly was silently corrected.

Historical D4: approximately **10,186 usable observations across 33 devices**, approximately **91.12% test accuracy**. Exact historical row selection and configuration are unrecoverable. Therefore 91.12% remains historical/exploratory and is not certified.

Frozen minimal D4 baseline: **35.8086% test accuracy**, embedding dimension 32, input 2x288 I/Q, no accuracy tuning.

## D5 current state
### Learned embedding
- D4 classifier: 35.81% accuracy, 31.58% macro-F1, 35.80% balanced accuracy.
- nearest centroid: 36.21%, 33.23%, 36.30%.
- 1-NN: **63.77%**, **63.63%**, **63.80%**.

### Classical RF feature baseline
The current repository D3 implementation contains **16** deterministic RF evidence features. Fixed RF: 100 trees, `random_state=20260830`, `max_features=sqrt`, no tuning.

- **87.39% accuracy**
- **87.32% macro-F1**
- **87.41% balanced accuracy**

This is substantially stronger than the learned-embedding readouts and is retained as the primary Track-A classical identity baseline.

The historical ~91.1% result used an approximately 60-feature list, but the exact list, exact 10,186-row selection and historical configuration remain unavailable. Do not invent or silently reconstruct them.

## D6 current state
Known devices: **1–33**. Unknown devices: **34–123**.

### Learned embedding centroid gate
- threshold: `21.2566452`, selected only from known validation distances at the 95th percentile.
- known-test acceptance: **95.42%**.
- unknown-test rejection: **10.99%** over 13,329 observations from 90 unknown devices.

### RF confidence gate
- frozen D5 RF maximum-class-probability threshold: `0.30`, selected only from known validation at the 5th percentile.
- known-test acceptance: **94.90%**.
- unknown-test rejection: **29.49%**.

Conclusion: the RF closed-set classifier is strong, but open-set rejection remains weak. Closed-set recognition and novelty rejection must remain separate decisions.

## D7 current state
### Track-A synthetic stress — COMPLETE
The frozen D5 RF classifier was evaluated without retraining/test tuning under deterministic synthetic perturbations.

Gain:
- baseline 87.39%
- -6 dB 38.07%
- -3 dB 27.30%
- +3 dB 20.06%
- +6 dB 15.93%

AWGN:
- 20 dB 82.29%
- 10 dB 53.34%
- 5 dB 20.44%
- 0 dB 6.73%

Interpretation: the current RF-feature baseline is highly acquisition-sensitive. These are controlled engineering stress results, not real temporal/receiver/environment measurements.

### Track-B real-shift requirement — OPTIONAL FOR TRACK-A, REQUIRED FOR REAL-WORLD CLAIMS
SMoRFFI metadata does not expose trustworthy temporal/session/receiver/environment boundaries. Therefore those claims require external data.

First priority: **Oregon State WiFi RFFP** for real day/environment variation.  
Second priority: **WiSig / ManySig** for real receiver/day/channel variation.  
SmartHomePrivacy is a useful smaller cross-day option if acquisition is practical.

No additional large download is required merely to continue Track A.

## D7–D10 paper-grounded constructed-data policy
Published papers may be used to establish that particular shift mechanisms, open-set conditions and attack scenarios are realistic research questions and to motivate controlled parameter ranges. Their empirical numbers remain external literature evidence.

Track-A constructed datasets shall record:
- source observation IDs
- transformation family
- parameters/ranges
- random seed
- intended physical interpretation
- whether the transformation is a stress test or a mechanism simulation
- explicit statement that it is synthetic/derived.

This is the selected practical solution to the 512 MB upload constraint. It does not lower the scientific-validation standard.

## D8 exact direction
Build a chronological profile manager using SMoRFFI real observations plus explicitly constructed condition/shift streams.

The minimum state per profile is:
- device identity
- representation centroid/statistics
- RF-feature profile statistics
- observation count
- profile version
- dispersion/consistency statistics
- update audit history

Separate:
`OBSERVATION -> IDENTITY RECOGNITION -> UPDATE AUTHORIZATION -> PROFILE UPDATE`

Required decisions:
- ACCEPT / UPDATE
- HOLD / QUARANTINE
- REJECT

Baseline ladder:
1. frozen/no-update;
2. always-update after recognition;
3. confidence-only admission;
4. proposed multi-evidence authorization.

The evaluation partition is frozen before the chronological update stream begins. Future evaluation observations cannot be used to update the profile before they are evaluated.

## D9 exact direction
Use legitimate RF observations plus controlled/synthetic poisoning. Attack classes:
- label contamination;
- unknown-device contamination into a known profile;
- gradual representation drift;
- replay/repetition of suspicious observations.

Compare the same admission-policy ladder used in D8.

Measure:
- attack acceptance rate;
- profile displacement/drift;
- legitimate-sample acceptance after attack;
- post-attack identity accuracy;
- unknown false acceptance;
- rollback/recovery success;
- legitimate adaptation preserved.

The experiment must support or falsify the novelty hypothesis; it must not be designed to guarantee a positive result.

## D10 exact direction
Build one auditable Track-A lifecycle:

`SMoRFFI observation -> D2 -> D3 RF evidence + D4 embedding -> D5 identity -> D6 known/unknown -> D8 profile lookup -> update authorization -> D9 poisoning defense -> audit/final decision`

Demonstrate at minimum:
- known legitimate sample identified and accepted;
- unknown sample rejected/quarantined;
- legitimate new observations can evolve a profile;
- suspicious/poisoned observations are blocked/quarantined;
- profile history is auditable;
- frozen evaluation remains untouched by updates.

D10 is an integrated demonstrator, not a claim of scientific validation.

## Files for current milestone
- D4: `docs/04_research/D4_LEARNED_REPRESENTATION_BASELINE.md`, `configs/track_a_d4_baseline.json`, `experiments/track_a/d4_manifest.json`
- D5: `docs/04_research/D5_CLOSED_SET_IDENTITY.md`, `docs/04_research/D5_RANDOM_FOREST_CLASSICAL_BASELINE.md`, RF config/metrics and per-device/confusion artifacts
- D6: `docs/04_research/D6_OPEN_SET_UNKNOWN_REJECTION.md`, `docs/04_research/D6_RF_OPEN_SET_BASELINE.md`, RF/embedding metrics/config artifacts
- D7: `docs/04_research/D7_RF_DISTRIBUTION_SHIFT.md`, `experiments/track_a/d7_rf_shift_metrics.json`
- Next-direction master: `docs/04_research/D7_D10_TRACK_A_NEXT_DIRECTION.md`

## Branch / synchronization rule
Significant implementation happens on `develop` first. At the end of a milestone, `main` and `develop` must be synchronized to the same **content state** without deletion or silent rollback. Merge histories may differ; content equivalence is what matters. Never force-push protected `main`.

## Current milestone
The D4–D7 Track-A milestone is **consolidated and explicitly requested for synchronization**. `develop` contains the canonical state and the new D7–D10 direction document. `main` still contains the older D4-only state and must be reconciled losslessly.

All earlier project decisions, dataset qualifications, novelty boundaries, leakage controls, learning gates, D1–D2 evidence and historical records remain valid unless explicitly superseded above.
