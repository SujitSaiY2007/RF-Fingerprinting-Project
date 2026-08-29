# CURRENT OBJECTIVE

## Immediate project objective
**Fast-track the project toward a small, reproducible, demonstrable D1–D10 software pipeline while preserving scientific validity.**

The project is not allowed to call a stage complete merely because code exists. Each stage needs an artifact, test/experiment and acceptance evidence appropriate to its claim.

## Active execution model — two tracks

The project now uses two connected tracks so large dataset acquisition does not become the critical path.

### Track A — Fast Implementation / Demonstration
Build the minimum defensible D1–D10 vertical path using an accessible real-data development substrate. **WiSig ManySig** is the immediate substrate already acquired by the user. Oregon State WiFi remains the first intended second implementation dataset when acquisition is practical, but its download speed must not block Track A.

### Track B — Research Validation / Strengthening
Add larger subsets, additional days/devices and qualified datasets when a concrete experimental, metadata, access/licensing, integrity or reproducibility requirement justifies them. Use Track B for stronger cross-condition/cross-dataset validation, statistical analysis, ablations, failure analysis and support/falsification of the research claim.

Detailed policy:
`docs/08_execution/TWO_TRACK_EXECUTION_STRATEGY.md`

## Dataset acquisition policy
Acquire necessary development datasets once where practical, preserve raw copies unchanged and reuse them throughout D1–D10. Repeated downloads are not expected. Additional acquisition requires a documented need. Large raw datasets remain outside Git.

## Current engineering gate
**D1 — Raw RF Data / Ingestion**

The dataset-search/qualification workstream is complete as a development-substrate selection gate. It is not scientific validation.

First implementation pair:
1. **WiSig**
2. **Oregon State WiFi RFFP**

## Current research-control position
The broad literature audit rejected weak standalone novelty claims including:
- RF fingerprinting itself;
- learned RF embeddings;
- physics-informed RF representation;
- open-set RF fingerprint recognition;
- incremental/continual RF learning;
- temporal/domain/test-time adaptation;
- adaptive RF model/profile updating;
- generic adversarial/backdoor robustness;
- historical profiling by itself;
- reliability/sample selection before learning in the broad sense.

A targeted audit then examined the narrow profile-update question.

### Critical prior-art findings
**Nagravision WO2023046581A1** already describes RF/IQ authentication, anomaly detection, stored per-device models and updating a stored model using new RF observations for environmental adaptation.

**Liu et al. (2024)** describes temporal SEI continual learning in which new observations are compared with preserved feature distributions, “reliable” signals are selected, added to the database and used for model updating.

Therefore the project must not claim either:

`RF authentication + adaptive model update`

or

`reliable sample admission + continual update`

as standalone novelty.

## Revised provisional novelty hypothesis
> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile-poisoning while preserving legitimate adaptation.**

Core distinction:

`Identification correctness != authorization to update the persistent profile`

Supporting candidate mechanism:

`identity confidence + embedding consistency + RF-physical consistency + temporal consistency + historical-profile consistency + anomaly evidence -> update authorization`

The exact scoring/fusion method and thresholds are not fixed.

## Novelty proof requirement
Compare at least:

A. `Identify -> Update`

B. `Identify -> Confidence threshold -> Update`

C. `Identify -> Reliability/consistency -> Update`

D. `Identify -> Independent security/update-safety evaluation -> Authorization -> Update / Reject / Quarantine`

The decisive comparison is **C versus D**.

Research question:

> Does the security-oriented separation reduce profile corruption under controlled poisoning while preserving legitimate adaptation better than ordinary confidence/reliability admission?

If not, revise or abandon the candidate novelty.

## D1 immediate objective
Establish:
- authoritative source/version provenance;
- reproducible local data roots;
- manifests/checksums where feasible;
- raw I/Q interpretation;
- common metadata schema;
- device/session/day/receiver/environment identifiers;
- integrity/loadability tests;
- leakage-safe partition foundations;
- raw/normalized/derived/experiment separation.

## Fast-track D1–D10 execution
After D1 is minimally accepted, implement a vertical path through:

- **D2:** minimal deterministic synchronization/preprocessing;
- **D3:** small interpretable RF-feature set;
- **D4:** lightweight learned representation/embedding;
- **D5:** closed-set identity baseline;
- **D6:** unseen-device/open-set baseline;
- **D7:** temporal/receiver/environment/domain-shift test;
- **D8:** chronological profile evolution with A/B/C/D update policies;
- **D9:** controlled/synthetic poisoning and profile-corruption evaluation;
- **D10:** integrated end-to-end demonstration.

Do not over-engineer individual stages before the vertical path works.

## Required project evidence
Every stage must leave enough evidence to answer:
- What was implemented?
- What data were used?
- What split/protocol was used?
- What was measured?
- What failed?
- What was learned?
- What decision follows?

## Completion-level distinction
Preserve four levels:
1. **Implemented** — code/artifact exists.
2. **Tested** — engineering tests/reproducible checks pass.
3. **Demonstrated** — integrated path operates on real data.
4. **Scientifically validated** — stage-specific acceptance evidence supports the claim.

Track A primarily accelerates levels 1–3. Track B supplies additional evidence where level 4 requires it.

## Repository discipline
- Large raw datasets remain outside Git.
- Material decisions/results/limitations belong in GitHub.
- Use task/research branch -> PR -> develop -> review -> PR -> main.
- Do not force-reset or recreate independent branch histories.
- When a substantial project change is agreed at the end of a chat, synchronize `main == develop` unless an explicitly documented review/integration task remains pending.

## Knowledge base
Use:
`docs/07_knowledge_base/RF_FINGERPRINTING_KNOWLEDGE_BASE.md`

It defines the theory and practical skills to learn alongside implementation.

## Next concrete task
1. Start/continue D1 implementation using the accessible WiSig ManySig substrate.
2. Do not restart dataset qualification.
3. Continue Oregon State WiFi acquisition only as practical and do not let it block Track A.
4. Build the minimum vertical D1–D10 path aggressively.
5. Record implementation/evaluation evidence continuously.
6. Add Track B data only when a concrete validation requirement is documented.
