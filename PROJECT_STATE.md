# PROJECT STATE

**Last updated:** 2026-08-30

## Authoritative status
- Repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Stable branch: `main`
- Integration branch: `develop`
- Phase: **Phase 1 — Accelerated implementation / demonstrator construction**
- Current engineering gate: **D4 — learned representation; reproducibility closure before D5**
- D1: **COMPLETE at source/schema/ingestion-foundation level**
- D2.1: **COMPLETE — sample representation contract**
- D2.2: **OBSERVED / IMPLEMENTED / TESTED on a 20-file SMoRFFI inspection subset**
- D2.3: **DEFINED / IMPLEMENTED / TESTED on the same subset**
- D2.4: **DEFINED / IMPLEMENTED / TESTED as a Track-A engineering split**
- D2.5: **ENGINEERING ACCEPTED on the 20-file subset**
- D3: **IMPLEMENTED / exploratory demonstrated on real SMoRFFI data; scientific validation not complete**
- D4: **EXPLORATORY LEARNED-REPRESENTATION RESULT RECORDED; reproducible repository implementation/acceptance still required**
- D5+: **NOT STARTED**
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
The project is being fast-tracked toward a demonstrable D1–D10 software pipeline.

Execution principle:

> **Build the smallest defensible end-to-end system first, then strengthen individual stages.**

Fast-tracking means reducing waiting and unnecessary ceremony; it does **not** permit inventing schema, claiming robustness, hiding anomalies, or promoting exploratory results to validated findings.

### Two-track execution model — ACTIVE
**Track A — Fast Implementation / Demonstration**
- Build the minimum defensible D1–D10 vertical path quickly.
- Current Track A substrate: SMoRFFI.
- Keep Oregon State WiFi RFFP as a later intended second implementation dataset when acquisition is practical.
- Produce a real-data end-to-end demonstration before waiting for every large archive.

**Track B — Research Validation / Strengthening**
- Add larger subsets, additional days/devices and other qualified datasets only when required.
- Strengthen cross-condition/cross-dataset validation, ablations, statistical analysis and failure analysis.
- Use Track B to support or falsify research claims rather than manufacture positive evidence.

This changes execution priority and dependency structure; it does not lower the scientific completion standard.

## Completion-level discipline
Distinguish:
1. **Implemented** — code/artifact exists.
2. **Tested** — engineering tests or reproducible checks pass.
3. **Demonstrated** — integrated path operates on real data.
4. **Scientifically validated** — stage-specific acceptance evidence supports the claim.

Track A accelerates implementation/testing/demonstration. Track B supplies evidence where scientific validation requires broader data.

## Novelty status
The candidate contribution remains provisional:

> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile-poisoning while preserving legitimate adaptation.**

The project must still compare this against strong reliability/admission baselines before claiming novelty.

## D1–D10 fast-track relationship
`D1 ingestion -> D2 DSP -> D3 RF evidence -> D4 embedding -> D5 identity -> D6 open-set -> D7 shift -> D8 profile evolution -> D9 poisoning -> D10 integration`

D8/D9 remain the primary experimental stages for supporting/falsifying the novelty hypothesis and must use validated upstream artifacts.

## D2 current state
### D2.1 — COMPLETE
One source CSV row is one atomic source observation. Signal-derived information is the model-input boundary; identity and source identifiers remain labels/provenance. Exact parser/shape/scaling/windowing were deferred until package inspection.

### D2.2 — OBSERVED / IMPLEMENTED / TESTED
A 20-file local subset of the IQ-only SMoRFFI release was inspected: **19,513 rows** total.

Observed:
- columns: `Device Number`, `MAC_address`, `preamble`;
- `preamble` is a serialized complex-sample sequence;
- all inspected rows parse successfully;
- stored sequence length is **288–579** complex samples;
- 5,783 rows are exactly 288 and 13,730 are longer;
- one uploaded device-109 file contains 513 rows rather than the published 1,000 and is retained as an explicit anomaly.

The published SMoRFFI paper defines the canonical preamble as **288 complex samples** and reports 20 MS/s acquisition. Therefore the Track-A baseline selects the first 288 parsed complex samples while retaining original length and excluded-tail count as provenance. This is documented in `docs/04_research/D2_2_SMORFFI_SCHEMA_EVIDENCE.md`.

### D2.3 — DEFINED / IMPLEMENTED / TESTED
Baseline transformation:
`serialized preamble -> complex[288] -> real[2,288] (I,Q)`.

No per-observation normalization, clipping, resampling or filtering is applied in the baseline. Normalization remains an explicit future ablation because amplitude may carry RF-discriminative information. See `docs/04_research/D2_3_PREPROCESSING_CONTRACT.md` and `src/smorffi_d2.py`.

### D2.4 — DEFINED / IMPLEMENTED / TESTED
A deterministic 70/15/15 engineering split is assigned from `(device_id, source_row_index)` using SHA-256. This is **not** claimed to be a temporal/session holdout because the inspected SMoRFFI files do not expose those boundaries. See `docs/04_research/D2_4_LEAKAGE_SAFE_SPLIT.md`.

### D2.5 — ENGINEERING ACCEPTED
Integrated D2 checks pass on the 20-file local subset. See `docs/04_research/D2_5_INTEGRATED_ACCEPTANCE.md`.

## D3 current state
### D3 — IMPLEMENTED / EXPLORATORY DEMONSTRATED
`src/smorffi_d3.py` defines deterministic, label-free interpretable RF evidence features from the canonical 288-sample complex preamble:
- I/Q moments and variance ratio;
- amplitude mean/std, RMS and crest factor;
- mean power;
- I/Q correlation;
- local phase-step statistics;
- FFT spectral centroid and spectral spread;
- spectral entropy.

An exploratory closed-set baseline on the available runtime data produced approximately **90.9% Random Forest test accuracy** in the earlier fast-track run. This is recorded as an engineering/demo result, not a validated transmitter-intrinsic fingerprinting claim. The exact runtime dataset must be re-established before this number is used as a formal benchmark.

The implementation deliberately does **not** call phase slope a calibrated CFO estimate. RF/channel/receiver effects can contribute to these descriptors, so D3 treats them as evidence features rather than unique transmitter fingerprints.

## D4 current state
### D4 — EXPLORATORY RESULT; REPRODUCIBILITY CLOSURE REQUIRED
A fast-track neural experiment was reported using the canonical `2 x 288` I/Q input and a compact learned representation, with an exploratory closed-set result of approximately **91.1% test accuracy**. Because the experiment artifact/model code and exact runtime dataset snapshot are not yet committed and reproducibly tested in the repository, this result is **not** promoted to a formal D4 acceptance metric.

The next D4 action is to commit a minimal reproducible learned-embedding implementation, tests, configuration and result record, then freeze the D4 baseline before starting D5. Do not tune for a higher accuracy merely to improve the number.

## Experimental dataset-count correction
A prior conversational update stated **32,513 observations** after additional uploads. The repository must not treat that number as authoritative because the current reproducible runtime snapshot available for the D4 exploratory run contained **10,186 usable observations across 33 devices**. Until a complete manifest is regenerated from all uploaded files, use only explicitly verified counts in formal results. The earlier 19,513-row 20-file D2.2 inspection remains valid for its stated subset.

## Important experimental constraints
- Avoid identity leakage: MAC/device identifiers are never model features.
- Do not fit preprocessing statistics on validation/test data.
- Preserve frozen evaluation data during profile-update experiments.
- D9 uses legitimate RF data plus controlled/synthetic poisoning and labels the threat source explicitly.
- D10 must demonstrate the lifecycle rather than isolated blocks.
- Never convert an exploratory runtime result into a formal benchmark without a reproducible dataset manifest, code/configuration and test evidence.

## Continuity / branch rule
When a significant milestone is agreed at the end of a chat, synchronize `main` and `develop` to the same **content state** without deleting or silently reverting prior information. Merge commits may make branch histories differ even when their file contents are identical; content equivalence is the operative synchronization requirement.

All prior dataset qualifications, novelty findings, D1–D10 definitions, leakage controls, poisoning controls and scientific completion standards remain unchanged unless explicitly superseded by a recorded decision.
