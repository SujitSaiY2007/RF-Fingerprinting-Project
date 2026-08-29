# PROJECT STATE

**Last updated:** 2026-08-29

## Authoritative status
- Repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Stable branch: `main`
- Integration branch: `develop`
- Phase: **Phase 1 — Preparation / accelerated implementation**
- Current engineering gate: **D2 — Minimal deterministic synchronization / preprocessing**
- Current substage: **D2.1 — Sample representation — COMPLETE**
- D1: **COMPLETE at source/schema/ingestion-foundation level**
- D1–D10 scientific validation: **not yet complete**
- Team size: 4
- All four members remain on the same overall workstream.

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
The project is now being fast-tracked toward a demonstrable D1–D10 software pipeline.

The execution principle is:

> **Build the smallest defensible end-to-end system first, then strengthen individual stages.**

### Two-track execution model — ACTIVE
The project now separates execution into two connected tracks:

**Track A — Fast Implementation / Demonstration**
- Build the minimum defensible D1–D10 vertical path quickly.
- Current Track A substrate: SMoRFFI.
- Keep Oregon State WiFi RFFP as a later intended second implementation dataset when acquisition is practical.
- Produce a real-data end-to-end demonstration before waiting for every large archive.

**Track B — Research Validation / Strengthening**
- Add larger subsets, additional days/devices and other qualified datasets only when required.
- Strengthen cross-condition/cross-dataset validation, ablations, statistical analysis and failure analysis.
- Use Track B to support or falsify research claims rather than to manufacture positive evidence.

This changes execution priority and dependency structure; it does **not** lower the scientific completion standard or delete prior decisions.

## Dataset acquisition policy under the two-track model
The project aims to acquire necessary development datasets once, preserve raw copies unchanged and reuse them throughout D1–D10. Repeated downloads of the same dataset are not expected.

Additional acquisition is permitted only for a concrete experimental, metadata, access/licensing, integrity or reproducibility requirement. No open-ended dataset hunt is allowed.

Large raw RF datasets remain outside Git.

## Completion-level discipline
Distinguish:
1. **Implemented** — code/artifact exists.
2. **Tested** — engineering tests or reproducible checks pass.
3. **Demonstrated** — integrated path operates on real data.
4. **Scientifically validated** — stage-specific acceptance evidence supports the claim.

Track A accelerates implementation/testing/demonstration. Track B supplies additional evidence where scientific validation requires it.

D-stage completion still requires evidence and acceptance criteria. Code existence alone is not completion.

The first implementation pair remains **SMoRFFI + Oregon State WiFi RFFP** for the accelerated path, with WiSig ManySig preserved as Track B.

## Novelty research status — 2026-08-29
A broad literature audit was followed by a targeted forensic audit of RF/RFFI systems involving profile/model updating, sample admission, continual learning and RF security.

### Weak standalone novelty claims rejected
The following are established or active research areas and are not treated as standalone project novelty:
- RF fingerprinting;
- learned RF embeddings;
- physics-informed RF representation;
- open-set RF fingerprint recognition;
- prototype/embedding-based unknown-device decision;
- incremental/continual RF fingerprint learning;
- temporal/domain/test-time adaptation;
- adaptive RF model/profile updating;
- generic adversarial/backdoor robustness;
- historical device profiling by itself;
- reliability/sample selection before learning, in the broad sense.

### Important prior-art findings
1. **Nagravision WO2023046581A1** already combines RF/IQ authentication, anomaly detection, persistent device models and model updating with new RF observations for environmental adaptation.
2. **Liu et al. (2024)** combines temporal adaptation, continual learning and selective admission of “reliable” new signals before database/model update.
3. Other RF/PHY authentication work uses online adaptation and multiple physical attributes.
4. RF backdoor research establishes that learned RF identity models are security-sensitive.

The canonical comparison is:
`docs/04_research/targeted_prior_art_matrix.md`

## Revised primary novelty hypothesis
The project will investigate:

> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile-poisoning while preserving legitimate adaptation.**

Core distinction:
`Identification correctness != authorization to update the persistent profile`

A candidate system may therefore accept an observation for operational identity while rejecting/quarantining it for persistent profile modification.

### Supporting candidate mechanism
A multi-evidence update-authorization policy may use:
- identity confidence;
- embedding consistency;
- RF-physical consistency;
- temporal consistency;
- historical-profile consistency;
- anomaly/deviation evidence.

The exact policy and thresholds are not frozen.

### Novelty status
**PROVISIONAL — NOT FINALIZED.**

The targeted audit substantially narrowed the gap but does not prove that no prior system has the same architecture. The strongest remaining uncertainty is whether a security-specific separation provides measurable value beyond a well-designed reliability/admission baseline.

## D1–D10 fast-track relationship
- D1: reproducible raw-data foundation. **COMPLETE for Track-A SMoRFFI source/schema/ingestion foundation.**
- D2: minimal deterministic synchronization/preprocessing.
  - **D2.1: sample representation — COMPLETE.**
  - D2.2: actual package/schema inspection and signal-field confirmation.
  - D2.3: deterministic preprocessing transformation definition.
  - D2.4: leakage-safe split strategy.
  - D2.5+: implementation, tests, evidence and acceptance.
- D3: interpretable RF evidence.
- D4: simple learned representation/embedding.
- D5: closed-set identity baseline.
- D6: explicit unseen-device/open-set baseline.
- D7: temporal/receiver/environment/domain-shift evidence.
- D8: chronological profile evolution and update-policy comparison.
- D9: controlled/synthetic poisoning and profile-corruption evaluation.
- D10: integrated end-to-end demonstration.

D8 and D9 are the primary experimental stages for proving/falsifying the candidate contribution, but they must use validated upstream artifacts.

## D1 completion milestone — 2026-08-29
SMoRFFI D1 is now recorded as complete at the **source/schema/ingestion-foundation** level.

Completed artifacts:
- `src/smorffi_d1.py` — metadata-first SMoRFFI CSV ingestion.
- `tests/test_smorffi_d1.py` — deterministic IQ/feature/invalid-identity tests.
- `datasets/SMORFFI_D1_EVIDENCE.md` — source structure, acquisition evidence, schema decisions, integrity boundary and scientific limits.
- `datasets/dataset_registry.csv` — SMoRFFI D1 status and published acquisition metadata.

Published source evidence establishes 123 CSV files per release, 1,000 records per device, MAC/device identifiers, raw preamble data and RF-feature variants. The published acquisition is one USRP B210, 123 same-model M5Stack Core2 devices, 20 MS/s, IEEE 802.11g, Channel 6, 20 MHz bandwidth, fixed 25 cm separation, controlled indoor single-day collection.

The implementation deliberately does not infer chronology, session, receiver, environment or multi-day metadata that the source does not provide. Large RF archives remain outside Git.

**Integrity boundary:** a byte-level checksum of the full downloaded Kaggle archive has not been independently reproduced in this environment. The repository records the deterministic SHA-256 helper and the exact evidence required for a future local acquisition record. Therefore this D1 completion must not be represented as proof of local archive acquisition.

## D2.1 completion milestone — 2026-08-29
The D2.1 sample representation contract is recorded in `docs/04_research/D2_1_SAMPLE_REPRESENTATION.md`.

Established:
- one source CSV row is one atomic source observation / candidate sample;
- signal-derived information is the model-input boundary;
- device identity and source identifiers are labels/provenance, not predictive inputs;
- source file, row index, device ID/MAC and original source row are retained for provenance;
- unavailable metadata is not inferred;
- exact numeric signal shape, parser, scaling, windowing/padding and normalization are deliberately deferred to D2.2/D2.3 until the actual package schema is inspected;
- no device identity shortcut may enter the baseline model input;
- later transformations must remain traceable to their source observation.

This substage does not claim optimal preprocessing, model performance or scientific validation.

## Current next action
1. Begin D2.2 by inspecting the actual SMoRFFI package/schema available for execution.
2. Confirm the exact signal field(s), parsing representation and numeric sample shape from observed data rather than assumption.
3. Define deterministic preprocessing and leakage-safe splitting after schema confirmation.
4. Preserve raw/source rows and provenance; derived artifacts remain reproducible from D1 inputs.
5. Keep D7/D8 claims blocked until a dataset with the required temporal/receiver/environment metadata is selected.
6. Maintain the Track-A/Track-B separation and branch synchronization rules.

## Continuity rule
When a significant progress milestone is completed and agreed at the end of a chat, the canonical project state must be synchronized so that `main` and `develop` contain the same agreed project state. Work-in-progress task branches and open PRs may remain ahead during implementation, but they must not silently alter `main`.

All prior dataset qualifications, novelty findings, D1–D10 definitions, leakage controls, poisoning controls, branch rules and scientific completion standards remain unchanged unless explicitly superseded by a recorded decision.
