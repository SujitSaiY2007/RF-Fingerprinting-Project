# CURRENT HANDOFF — 2026-08-29

## Project
**Physics-Based RF Fingerprinting with Continuous Device Learning**

## Canonical repository
`SujitSaiY2007/RF-Fingerprinting-Project`

## Current position
- Phase: **Phase 1 — Preparation / accelerated implementation**.
- Current engineering gate: **D1 — Raw RF Data / Ingestion**.
- Dataset qualification is complete as a development-substrate selection gate.
- D1–D10 are not scientifically completed.
- Team size: 4.

## Fast-track objective
The project must move quickly from planning to a demonstrable software pipeline.

Execution principle:

`Build minimum viable evidence path -> test -> document -> strengthen`

Do not claim scientific completion from code existence.

## Qualified dataset portfolio
### Primary
1. WiSig — scale, receiver variation, multi-day/channel robustness.
2. Oregon State WiFi RFFP — temporal/domain variation.
3. Oregon State LoRa RFFP — same-model/environment/location/distance/receiver variation.
4. SMoRFFI — large-scale same-model discrimination.

### Secondary
5. ORACLE — controlled transmitter-hardware/distance benchmark.
6. Bluetooth smartphone RF database — optional cross-technology benchmark.

First implementation pair: **WiSig + Oregon State WiFi RFFP**.

## Novelty status — revised 2026-08-29
The targeted audit found two especially important boundaries:

### Nagravision WO2023046581A1
Already combines RF/IQ authentication, anomaly detection, persistent device models and adaptive model updating using new RF observations.

### Liu et al. (2024)
Combines temporal/domain adaptation with continual SEI learning and selectively admits “reliable” new signals into the database before model updating.

Therefore neither of the following is sufficient novelty:

- RF authentication + adaptive model update;
- reliability/sample admission + continual RF update.

### Current candidate contribution
> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile-poisoning while preserving legitimate adaptation.**

Candidate supporting mechanism:

> **Multi-evidence update authorization using identity confidence, representation consistency, RF-physical consistency, temporal consistency, historical-profile consistency and anomaly evidence.**

The policy, score and thresholds remain open research variables.

### Current uncertainty
The strongest unresolved question is whether this security-specific separation provides a measurable advantage beyond a strong reliability/admission baseline. If not, the novelty claim must be revised or abandoned.

Canonical evidence:
`docs/04_research/targeted_prior_art_matrix.md`

## D1 objective
Build the reproducible raw-RF foundation for WiSig + Oregon State WiFi:
- provenance/version identity;
- acquisition/reference instructions;
- manifests/checksums where feasible;
- I/Q interpretation;
- normalized metadata;
- missing-metadata handling;
- integrity/loadability tests;
- reproducible data root;
- leakage-safe identifiers;
- raw/normalized/derived/experiment separation.

## D1–D10 accelerated execution
After minimal D1 acceptance, proceed with a vertical implementation path:

`D1 ingestion -> D2 DSP -> D3 RF evidence -> D4 embedding -> D5 identity -> D6 open-set -> D7 shift -> D8 profile evolution -> D9 poisoning -> D10 integration`

D8/D9 must compare:

A. `Identify -> Update`

B. `Identify -> Confidence -> Update`

C. `Identify -> Reliability/Consistency -> Update`

D. `Identify -> Security/Update-Safety -> Authorization -> Update/Reject/Quarantine`

The decisive novelty comparison is C versus D.

## Important experimental constraints
- Avoid random splits where session/burst leakage is possible.
- Prefer session/day/device/receiver holdouts appropriate to the claim.
- Keep frozen evaluation data isolated from profile updates.
- D9 uses legitimate RF data plus controlled/synthetic poisoning and must be labelled accordingly.
- D10 must demonstrate the complete lifecycle, not only isolated blocks.

## Knowledge base
Use:
`docs/07_knowledge_base/RF_FINGERPRINTING_KNOWLEDGE_BASE.md`

It contains the theory and practical minimum knowledge needed while implementing D1–D10.

## Next-chat continuation
Use:
`docs/08_execution/NEXT_CHAT_FAST_TRACK_PROGRESS_PROMPT.md`

The next session should inspect the repository first, determine which stages have real code/evidence, then start D1 immediately without repeating completed dataset qualification or broad literature searching.

## Research discipline
Distinguish:
- source-derived fact;
- repository-derived fact;
- implementation;
- test result;
- experiment result;
- inference;
- hypothesis;
- speculation.

Do not claim novelty, superiority, publication-worthiness or patentability without evidence.
