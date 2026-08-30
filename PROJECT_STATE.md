# PROJECT STATE

**Last updated:** 2026-08-30

## Authoritative status
- Repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Stable branch: `main`
- Integration branch: `develop`
- Phase: **Phase 1 — Accelerated implementation / demonstrator construction**
- Current engineering gate: **D6 — open-set rejection baseline complete; D7 next**
- D1: **COMPLETE at source/schema/ingestion-foundation level**
- D2.1: **COMPLETE — sample representation contract**
- D2.2: **OBSERVED / IMPLEMENTED / TESTED on a 20-file SMoRFFI inspection subset**
- D2.3: **DEFINED / IMPLEMENTED / TESTED on the same subset**
- D2.4: **DEFINED / IMPLEMENTED / TESTED as a Track-A engineering split**
- D2.5: **ENGINEERING ACCEPTED on the 20-file subset**
- D3: **IMPLEMENTED / exploratory demonstrated on real SMoRFFI data; scientific validation not complete**
- D4: **IMPLEMENTED / TESTED / DEMONSTRATED with reproducible 33-device Track-A baseline; historical ~91.1% result remains unreproducible**
- D5: **IMPLEMENTED / TESTED / DEMONSTRATED — closed-set identity using frozen D4 embedding**
- D6: **IMPLEMENTED / TESTED / DEMONSTRATED — unknown-device rejection baseline**
- D7+: **NOT STARTED**
- D3–D10 scientific validation: **not yet complete**
- Team size: 4

## Dataset qualification milestone
The dataset-search/qualification gate is complete for development-substrate selection.

### KEEP — primary
- WiSig — scale, receiver variation, multi-day robustness.
- Oregon State WiFi RFFP — temporal/domain variation.
- Oregon State LoRa RFFP — same-model/environment/location/distance/receiver variation.
- SMoRFFI — large-scale same-model discrimination.

### SECONDARY
- ORACLE — controlled hardware/distance benchmark.
- Bluetooth smartphone RF database — optional cross-technology benchmark.

This does not constitute scientific validation of D1–D10.

## Accelerated execution decision
The project is fast-tracked toward a demonstrable D1–D10 software pipeline.

Execution principle:
> **Build the smallest defensible end-to-end system first, then strengthen individual stages.**

Fast-tracking reduces waiting and unnecessary ceremony; it does **not** permit inventing schema, claiming robustness, hiding anomalies, or promoting exploratory results to validated findings.

### Two-track execution model — ACTIVE
**Track A — Fast Implementation / Demonstration**
- Current Track-A substrate: SMoRFFI.
- Build the minimum defensible D1–D10 vertical path quickly.
- Produce a real-data end-to-end demonstration before waiting for every large archive.

**Track B — Research Validation / Strengthening**
- Add larger subsets, additional days/devices and other qualified datasets only when required.
- Strengthen cross-condition/cross-dataset validation, ablations, statistical analysis and failure analysis.
- Use Track B to support or falsify research claims rather than manufacture positive evidence.

## Completion-level discipline
1. **Implemented** — code/artifact exists.
2. **Tested** — engineering tests or reproducible checks pass.
3. **Demonstrated** — integrated path operates on real data.
4. **Scientifically validated** — stage-specific acceptance evidence supports the claim.

Track A accelerates implementation/testing/demonstration. Track B supplies evidence where scientific validation requires broader data.

## Novelty status
The candidate contribution remains provisional:
> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile-poisoning while preserving legitimate adaptation.**

D8/D9 remain the primary stages for supporting/falsifying this hypothesis and must use validated upstream artifacts.

## D1–D10 fast-track relationship
`D1 ingestion -> D2 DSP -> D3 RF evidence -> D4 embedding -> D5 identity -> D6 open-set -> D7 shift -> D8 profile evolution -> D9 poisoning -> D10 integration`

## D4 reproducibility closure
The complete user-supplied archive was inspected:
- 123 CSV files
- 122,511 observations
- 123 devices
- archive SHA-256: `1d9ebcf2539e5fb7fb1dc678dba3fd2a50cada2befb86f5d84faff2b4f541037`

The Track-A D4 snapshot is devices **1–33**, 33 files and 33,000 observations. D2 deterministic split gives 23,030 train / 4,974 validation / 4,996 test.

The complete archive retains row-count anomalies: device 67 has 999 rows, device 87 has 999, and device 109 has 513. No anomaly was silently corrected.

The historical D4 run recorded approximately **10,186 usable observations across 33 devices** and approximately **91.12% test accuracy**. The exact 10,186-row selection and historical model/configuration were not recoverable from the repository. Therefore **91.12% remains historical/exploratory and is not certified as a reproducible benchmark**.

The frozen minimal repository D4 model was run on the explicit 33-device snapshot without accuracy tuning:
- test accuracy: **35.8086%**
- embedding dimension: **32**
- input: **2 x 288 I/Q**

This is the formal reproducible Track-A baseline for the committed implementation. The lower result does not prove the historical result false; it proves only that the historical result cannot be reproduced from the recoverable evidence and that the current minimal baseline does not match it.

See `docs/04_research/D4_LEARNED_REPRESENTATION_BASELINE.md`, `configs/track_a_d4_baseline.json`, and `experiments/track_a/d4_manifest.json`.

## D5 current state
D5 uses the frozen D4 embedding and frozen test set. Results:

| Method | Accuracy | Macro-F1 | Balanced accuracy |
|---|---:|---:|---:|
| D4 classifier | 35.81% | 31.58% | 35.80% |
| Nearest centroid | 36.21% | 33.23% | 36.30% |
| **1-nearest neighbour** | **63.77%** | **63.63%** | **63.80%** |

The 1-NN result indicates useful local identity structure in the embedding despite weak classifier/centroid generalization. Per-device metrics and the 33x33 1-NN confusion matrix are retained under `experiments/track_a/`.

## D6 current state
Known devices are 1–33; unknown devices are 34–123. Unknown data are not used to fit D4 or known-device centroids.

Rejection score: nearest known-device centroid squared Euclidean distance in frozen D4 embedding.

Threshold is selected only from known-device validation data at the **95th percentile**, yielding `T = 21.2566452`.

On the frozen known test set, acceptance is **95.42%**. On the deterministic test partition of 90 unknown devices (13,329 observations), rejection is only **10.99%**.

This is a deliberately simple open-set baseline and a **negative/limiting result**: the current embedding does not separate most unknown devices from the known gallery. The threshold was not tuned against unknown test data.

See `docs/04_research/D6_OPEN_SET_UNKNOWN_REJECTION.md` and `experiments/track_a/d6_metrics.json`.

## Important experimental constraints
- Avoid identity leakage: MAC/device identifiers are never model features.
- Do not fit preprocessing statistics on validation/test data.
- Preserve frozen evaluation data during profile-update experiments.
- D9 uses legitimate RF data plus controlled/synthetic poisoning and labels the threat source explicitly.
- D10 must demonstrate the lifecycle rather than isolated blocks.
- Never convert an exploratory runtime result into a formal benchmark without a reproducible dataset manifest, code/configuration and test evidence.

## Continuity / branch rule
When a significant milestone is explicitly agreed at the end of a chat, synchronize `main` and `develop` to the same **content state** without deleting or silently reverting prior information. Merge commits may make histories differ even when file contents are identical; content equivalence is the operative synchronization requirement.

**Current branch state:** the D4–D6 milestone is committed on `develop`; `main` has intentionally not been synchronized yet because explicit milestone agreement is still required.

All prior dataset qualifications, novelty findings, D1–D10 definitions, leakage controls, poisoning controls and scientific completion standards remain unchanged unless explicitly superseded by a recorded decision.
