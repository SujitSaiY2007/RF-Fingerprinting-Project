# PROJECT MASTER PLAN

## 1. Project foundation

- Preserve the initial IDP as the origin of the project.
- Maintain the research question, objectives, scope and contribution as controlled project records.
- Maintain a decision log so later changes are traceable.
- Treat novelty as an evidence-backed research claim, not an assumption made from the architecture.

## 2. Preparation and fast-track strategy

The project is now executed with an **evidence-first two-track vertical strategy**:

`Accessible real development substrate -> minimum implementation -> test -> evidence -> complete D1–D10 vertical path -> strengthen with additional validation`

The goal is to obtain a complete demonstrable software lifecycle quickly without falsely claiming that unvalidated stages are complete.

### Track A — Fast Implementation / Demonstration

Track A is the immediate critical path. It uses an accessible real-data substrate, beginning with WiSig ManySig already acquired by the user, to build the minimum defensible D1–D10 pipeline quickly.

Oregon State WiFi remains the first intended second implementation dataset when acquisition is practical, but its download time must not block Track A.

### Track B — Research Validation / Strengthening

Track B runs in parallel where practical or after Track A and adds larger subsets, additional days/devices, qualified datasets, cross-condition/cross-dataset validation, statistical analysis, ablation and failure analysis when a concrete requirement justifies them.

This changes execution order and dependency structure only. It does not lower the scientific completion standard.

The first development pair remains WiSig + Oregon State WiFi RFFP.

## 3. Dataset strategy

- Search/qualification is complete for the current development portfolio.
- KEEP: WiSig, Oregon State WiFi RFFP, Oregon State LoRa RFFP, SMoRFFI.
- SECONDARY: ORACLE, Bluetooth smartphone RF database.
- Large raw archives remain outside Git.
- Acquire necessary development datasets once where practical, preserve raw copies unchanged and reuse them through D1–D10.
- Further acquisition is triggered only by a specific experimental, access/licensing, metadata, integrity or reproducibility gap.
- No open-ended dataset hunt is permitted.

## 4. Novelty strategy — revised 2026-08-29

The following are not standalone novelty claims:
- RF fingerprinting;
- learned RF embeddings;
- physics-informed RF representation;
- open-set RF recognition;
- incremental/continual RF learning;
- temporal/domain/test-time adaptation;
- adaptive RF model/profile updating;
- generic adversarial/backdoor robustness;
- historical device profiling;
- reliability/sample selection before learning in the broad sense.

### Critical prior-art boundaries

**Nagravision WO2023046581A1** already combines RF/IQ authentication, anomaly detection, persistent device models and adaptive model updating.

**Liu et al. (2024)** combines temporal/domain adaptation, continual SEI learning, reliable-signal admission and database/model updating.

Therefore the project cannot claim a generic update gate or reliable-sample admission as its novelty.

### Current provisional candidate
> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile-poisoning while preserving legitimate adaptation.**

Supporting candidate:

> **A multi-evidence update-authorization policy using identity confidence together with representation, RF-physical, temporal, historical-profile and anomaly evidence, with the exact policy selected through experimental comparison and ablation.**

The targeted evidence is recorded in:
`docs/04_research/targeted_prior_art_matrix.md`

The claim remains provisional.

## 5. D1–D10 validation framework

### D1 — Raw RF Data / Ingestion
Establish reproducible provenance, manifests/checksums, raw I/Q interpretation, normalized metadata, integrity/loadability tests, reproducible data roots and leakage-safe identifiers.

### D2 — Synchronization & DSP
Implement the minimum deterministic preprocessing required by the selected datasets: validity checks, burst/sample selection, synchronization/alignment, normalization and model-ready formatting.

### D3 — Physics-Based RF Features
Extract a small defensible set of transmitter-related RF features and measure their device-discriminative value and sensitivity to time/receiver/environment changes.

### D4 — Device Representation / Embedding
Build a lightweight learned representation and expose an embedding for distance/prototype analysis. Treat embedding design as an enabling component, not standalone novelty.

### D5 — Closed-Set Identification
Establish the known-device baseline with leakage-safe evaluation, accuracy and per-device metrics.

### D6 — Open-Set Recognition
Hold out unseen devices and evaluate known acceptance and unknown rejection. Open-set recognition is an established baseline capability.

### D7 — Robustness / Domain Shift
Measure degradation under at least one meaningful temporal, receiver, environment, location, channel or SNR shift. Use the result to motivate adaptation.

### D8 — Continual Learning / Profile Evolution
Implement chronological profile evolution with a frozen evaluation set and explicit update-policy comparison:

A. `Identify -> Update`

B. `Identify -> Confidence -> Update`

C. `Identify -> Reliability/Consistency -> Update`

D. `Identify -> Security/Update-Safety -> Authorization -> Update/Reject/Quarantine`

Measure adaptation, profile drift, embedding stability, forgetting and legitimate adaptation.

### D9 — Poisoning / Adversarial Protection
Use legitimate RF data plus controlled/synthetic poisoning. Measure profile corruption, attack success, malicious observations required, recognition degradation, recovery and legitimate false rejection.

### D10 — End-to-End Validation
Integrate the complete lifecycle and test normal operation, unknown devices, legitimate temporal change, suspicious observations and controlled poisoning.

## 6. Hardware transfer

Hardware remains a later validation domain. Software/data evidence should not be blocked by requiring an SDR/ESP32 capture chain for every stage.

## 7. Engineering lifecycle

For every component:

`Requirement -> Design -> Implementation -> Unit Test -> Experiment -> Result -> Interpretation -> Decision`

## 8. Research lifecycle

For every research claim:

`Claim -> Literature audit -> What must be proven -> Experiment -> Required data -> Dataset qualification -> Validation -> Conclusion`

## 9. Fast-track execution rules

1. Simple baselines before SOTA.
2. Build a vertical D1–D10 path before polishing individual blocks.
3. Every stage must produce an artifact or measurable result.
4. Code existence is not scientific completion.
5. Preserve frozen evaluation data.
6. Avoid random splits when session/burst leakage is possible.
7. Clearly label controlled/synthetic attacks.
8. Never commit large raw datasets.
9. Record seeds/configuration/results.
10. Preserve failed experiments and limitations.
11. Do not let large dataset acquisition block the minimum vertical implementation.
12. Add further data only when a concrete validation need is documented.

## 10. Team workflow

- `main`: stable project state.
- `develop`: integration.
- task/research branches: isolated work.
- Pull requests are the normal integration mechanism.
- Significant research decisions go in `docs/06_continuity/DECISIONS.md`.

## 11. Completion standard

A phase is complete only when its acceptance criteria and evidence exist.

A novelty claim is complete only when:
1. nearest prior work is mapped;
2. the claimed difference is explicit;
3. an experiment can falsify the claim;
4. suitable data support the experiment;
5. experimental evidence demonstrates the claimed contribution.

The decisive novelty comparison is **reliability/admission baseline versus security-oriented update authorization**.

## 12. Two-track operating rule

Track A may establish an implementation/demo using a smaller accessible real-data subset before every qualified dataset is available.

Track B is responsible for strengthening claims that require broader data diversity or stronger experimental support.

The distinction between **implemented**, **tested**, **demonstrated** and **scientifically validated** must be preserved in all project records and professor-facing material.

The detailed operating policy is:
`docs/08_execution/TWO_TRACK_EXECUTION_STRATEGY.md`
