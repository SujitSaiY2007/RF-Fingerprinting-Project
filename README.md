# Physics-Based RF Fingerprinting with Continuous Device Learning

## Project Master Repository

This repository is the persistent source of truth for the project: research direction, architecture, dataset strategy, experiments, software implementation, validation, team workflow, and continuity between ChatGPT sessions.

## Current Project State

**Current phase:** Preparation

**Current workstream:** Dataset Search & Qualification

The project has evolved from the initial IDP into a software-first research and engineering framework. Public/existing RF datasets are intended to support the majority of development and validation before hardware-in-the-loop work.

## Core Idea

The project combines conventional RF signal processing with machine learning to identify known transmitters, detect previously unseen transmitters, remain robust to acquisition/environment changes, and continuously update device profiles while rejecting inconsistent observations.

## Project Validation Framework

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

Hardware transfer is treated as a later validation domain rather than a prerequisite for every software stage.

## Repository Navigation

- `PROJECT_STATE.md` — authoritative current state and next action.
- `PROJECT_MASTER_PLAN.md` — complete lifecycle and phase structure.
- `CURRENT_OBJECTIVE.md` — the exact task currently being executed.
- `docs/` — canonical project documentation and research records.
- `datasets/` — dataset registry, qualification records, metadata and manifests; not raw large datasets.
- `experiments/` — reproducible experiment definitions and records.
- `src/` — implementation.
- `tests/` — validation and regression tests.
- `results/` — generated figures/tables/logs where appropriate.
- `hardware/` — eventual ESP32/SDR and edge validation material.
- `.github/` — team workflow templates and automation.

## Continuity Rule

At the end of every substantial project session, update the project state, current objective, decisions, unresolved questions, and session log. The next ChatGPT session should read those files before proposing new work.

## Research Method

Do not select datasets merely because they are interesting. The project follows:

`Project Claim -> What Must Be Proven -> Experiment -> Required Data -> Dataset Search -> Dataset Qualification -> Validation`

This repository records that chain explicitly.
