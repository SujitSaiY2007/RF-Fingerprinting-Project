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

### Two-track execution model — ACTIVE
The project now separates execution into two connected tracks:

**Track A — Fast Implementation / Demonstration**
- Build the minimum defensible D1–D10 vertical path quickly.
- Use an accessible real-data development substrate, beginning with WiSig ManySig already acquired by the user.
- Keep Oregon State WiFi RFFP as the first intended second implementation dataset when acquisition is practical.
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

**Boundary:** the large real RF archives are not stored in Git. Real-archive inspection, manifest generation, loadability testing and leakage-safe partition construction remain the D1 acceptance work.

## Next action
1. Use the accessible WiSig ManySig data as the immediate Track A substrate and complete the minimum D1 evidence needed for implementation.
2. Continue Oregon State WiFi acquisition in parallel only as practical; do not let its download speed block Track A.
3. Build the minimum vertical D2–D10 path aggressively.
4. Add Track B datasets/conditions when a specific validation requirement justifies them.
5. Maintain A/B/C/D update-policy baselines for the later security experiment.
6. Record every material implementation result, failure and decision in GitHub.

## SUPERSEDING STATE UPDATE — 2026-08-29
The above historical state is superseded for the **current Track A execution substrate** by DEC-028 and DEC-029 in `docs/06_continuity/DECISIONS.md`.

### Current Track A
**SMoRFFI** is now the selected Track A working dataset. It is already a qualified **KEEP — primary same-model dataset** and is selected because it better satisfies the project's combined scientific-fit and rapid-access objective than the ORACLE distribution.

### Current Track B
- **WiSig ManySig:** preserved separately for validation/reproduction/cross-checking.
- **ORACLE:** retained as a qualified secondary controlled benchmark; prior ORACLE ingestion work is preserved and may be reused later.
- **Oregon State WiFi/LoRa:** unchanged; acquisition remains independent of Track A.

### D1 boundary after the switch
The Track A D1 work must now verify the actual SMoRFFI package, metadata, access path and loadability before scientific claims. The existing ORACLE-specific implementation is **not deleted**; it is no longer the Track A dependency.

### SMoRFFI stage responsibility caveat
The existing qualification record assigns SMoRFFI primarily to **D3–D6 and D10** and leaves D7/D8 contingent on package-level metadata verification. Therefore Track A must not assume SMoRFFI alone supplies all evidence needed for D7/D8. If a concrete D7/D8 requirement is not covered, a qualified Track B dataset may be used for that stage.

All prior dataset qualifications, novelty findings, D1–D10 definitions, leakage controls, poisoning controls, branch rules and scientific completion standards remain unchanged.
