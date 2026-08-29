# PROJECT STATE

**Last updated:** 2026-08-29

## Authoritative status
- Repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Stable branch: `main`
- Integration branch: `develop`
- Phase: **Phase 1 — Preparation / accelerated implementation**
- Current engineering gate: **D1 — Raw RF Data / Ingestion**
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

D-stage completion still requires evidence and acceptance criteria. Code existence alone is not completion.

The first implementation pair remains **WiSig + Oregon State WiFi RFFP**.

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
- D1: reproducible raw-data foundation.
- D2: minimal deterministic synchronization/preprocessing.
- D3: interpretable RF evidence.
- D4: simple learned representation/embedding.
- D5: closed-set identity baseline.
- D6: explicit unseen-device/open-set baseline.
- D7: temporal/receiver/environment/domain-shift evidence.
- D8: chronological profile evolution and update-policy comparison.
- D9: controlled/synthetic poisoning and profile-corruption evaluation.
- D10: integrated end-to-end demonstration.

D8 and D9 are the primary experimental stages for proving/falsifying the candidate contribution, but they must use validated upstream artifacts.

## D1 implementation milestone — 2026-08-29
A first reusable ingestion foundation now exists on `task/d1-ingestion-foundation-2026-08-29`:
- common RF metadata record;
- manifest-driven CSV ingestion;
- WiSig loader;
- Oregon State WiFi loader;
- deterministic checksum helper;
- normalized JSONL output;
- metadata validation tests;
- D1 provenance/acceptance specification.

**Boundary:** the large real RF archives are not stored in Git and were not available in the execution environment. Therefore this milestone is **implemented foundation only**, not D1 acceptance or scientific validation. Real-archive inspection, manifest generation, loadability testing and leakage-safe partition construction remain next.

## Scientific discipline
- Distinguish implemented, tested and scientifically validated.
- Do not infer metadata that the source does not provide.
- Do not use random splits when session/burst leakage is possible.
- Keep frozen evaluation data isolated from profile updates.
- Clearly label controlled/synthetic poisoning.
- Do not claim publication novelty, patentability or superiority without evidence.

## Next action
1. Inspect real local WiSig and Oregon State WiFi archives when available.
2. Generate and checksum real manifests.
3. Run loadability/integrity tests against real data.
4. Establish leakage-safe identifiers and partition metadata.
5. Once D1 has minimum acceptance evidence, build the minimum vertical D2–D10 path.
6. Maintain A/B/C/D update-policy baselines for the later security experiment.
7. Record every material implementation result, failure and decision in GitHub.
