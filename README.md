# Physics-Based RF Fingerprinting with Continuous Device Learning

## Project Overview

This repository is the persistent source of truth for the project's research direction, system design, datasets, implementation, experiments, validation and continuity between work sessions.

The project studies how wireless transmitters can be identified from characteristics present in their received RF signals, while also investigating how a continuously learning system can adapt its device profiles without blindly trusting every new observation.

## Core Research Question

A conventional continual RF fingerprinting system may follow:

`RF Observation → Identify Device → Update Device Profile`

Our project investigates a stricter separation:

`RF Observation → Identify Device → Check Whether the Observation Is Safe to Learn From → Update / Reject / Quarantine`

The central research hypothesis is:

> **Correctly recognizing a device does not automatically mean that the observation should be authorized to modify the persistent device profile.**

The candidate security mechanism may use several kinds of evidence, such as identity confidence, learned-representation consistency, RF characteristics, temporal behaviour, historical profile consistency and anomaly evidence.

This is a **provisional research hypothesis**, not a finalized claim of novelty.

## What We Are Not Claiming as Novel

The project deliberately does not treat these as standalone novelty claims because they are established research areas:

- RF fingerprinting
- learned RF embeddings
- physical-information-aware RF representation
- open-set recognition
- incremental/continual RF learning
- temporal/domain/test-time adaptation
- adaptive RF model/profile updating
- generic adversarial or backdoor robustness
- historical device profiling by itself
- reliability/sample selection before learning in the broad sense

## Current Novelty Direction

The targeted prior-art investigation identified important close and adjacent systems, including RF authentication with adaptive model updating and continual SEI systems that admit reliable observations before updating.

The remaining candidate contribution is narrower:

> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile poisoning while preserving legitimate adaptation.**

The decisive comparison will be against both ordinary updating and reliability/confidence-based admission methods.

## Validation Framework

| Stage | Focus |
|---|---|
| D1 | Raw RF Data / Ingestion |
| D2 | Synchronization & DSP |
| D3 | Physics-Based RF Features |
| D4 | Device Representation / Embedding |
| D5 | Closed-Set Identification |
| D6 | Open-Set Recognition |
| D7 | Robustness / Domain Shift |
| D8 | Continual Learning / Profile Evolution |
| D9 | Poisoning / Adversarial Protection |
| D10 | End-to-End Validation |

D-stage completion requires implementation, testing and scientific evidence. Code existence alone does not constitute validation.

## Dataset Strategy

### Primary development/validation datasets
- **WiSig** — scale, receiver variation and multi-day robustness.
- **Oregon State WiFi RFFP** — temporal/domain variation and repeated-device observations.
- **Oregon State LoRa RFFP** — same-model/environment/location/distance/receiver variation.
- **SMoRFFI** — large-scale same-model discrimination.

### Secondary datasets
- **ORACLE** — controlled transmitter-hardware/distance benchmark.
- **Bluetooth smartphone RF database** — optional cross-technology benchmark.

The first implementation pair is **WiSig + Oregon State WiFi RFFP**. Large raw datasets remain outside Git.

## Current Execution Strategy

The project is being fast-tracked toward a demonstrable end-to-end software pipeline.

The rule is:

> **Build the smallest defensible end-to-end system first, then strengthen individual stages.**

The intended path is:

`Raw RF → Preprocessing → RF Evidence → Embedding → Device Identification → Open-Set Decision → Domain/Temporal Evaluation → Profile Evolution → Poisoning Test → Update Authorization → End-to-End Demonstration`

## Research and Engineering Discipline

For every meaningful claim or component:

`Requirement → Design → Implementation → Test → Experiment → Result → Interpretation → Decision`

Important safeguards:

- Avoid random splits when session/burst leakage is possible.
- Keep evaluation data isolated from profile updates.
- Clearly label controlled/synthetic poisoning experiments.
- Do not infer metadata that the source does not provide.
- Distinguish implemented, tested and scientifically validated.
- Do not claim novelty, superiority, publication-worthiness or patentability without evidence.

## Repository Navigation

- `PROJECT_STATE.md` — current authoritative state and next action.
- `PROJECT_MASTER_PLAN.md` — complete lifecycle and validation framework.
- `CURRENT_OBJECTIVE.md` — current execution objective.
- `CURRENT_HANDOFF.md` — current human-readable handoff.
- `docs/04_research/` — literature and prior-art records.
- `docs/06_continuity/` — decisions and session history.
- `docs/07_knowledge_base/` — theory and practical learning guide.
- `docs/08_execution/` — fast-track execution and next-chat instructions.
- `datasets/` — dataset registry, qualification records, metadata and manifests; not raw archives.
- `experiments/` — reproducible experiment definitions and records.
- `src/` — implementation.
- `tests/` — validation and regression tests.

## Continuity

At the end of every substantial project session, update the relevant project state, decisions, unresolved questions, session log and next-chat handoff. GitHub remains the canonical project source of truth.

## Branch Workflow

- `main` — stable reviewed state.
- `develop` — integration/development state.
- `task/*` or `research/*` — isolated implementation/research work.
- Use Pull Requests for integration.
- Keep `main` and `develop` identical when no integration work is pending.

## Research Status

The current repository records a **provisional** novelty direction. The strongest uncertainty is whether the proposed security-specific separation provides measurable benefit beyond a well-designed reliability/admission baseline.

The project should change or abandon the novelty claim if the evidence does not support it.
