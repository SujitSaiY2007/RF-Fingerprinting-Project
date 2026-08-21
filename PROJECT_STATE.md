# PROJECT STATE

**Last initialized:** 2026-08-21

## Current Status

- Project concept defined from the initial IDP.
- Complete software-oriented architecture documented.
- Dataset Requirement Matrix established with D1-D10 stages.
- Dataset acceptance/qualification methodology established.
- Current repository is being initialized as the permanent project source of truth.

## Current Phase

**Phase 1 — Preparation**

## Current Workstream

**Dataset Search & Qualification**

The next substantive project activity is to identify candidate datasets for the defined experimental responsibilities and qualify them against the matrix and dataset-quality protocol.

## Completed Knowledge Baseline

1. Initial problem statement and objectives.
2. Physics-based RF feature concept.
3. Embedding/metric-learning direction.
4. Known/unknown device decision concept.
5. Continuous device profile update concept.
6. Edge deployment direction.
7. Eight-stage system decomposition in the architecture document.
8. Ten-stage dataset/validation framework D1-D10.
9. Dataset quality/provenance criteria.
10. Dataset acceptance protocol.

## Current Non-Goals

- Do not start model training before dataset qualification and D1 validation.
- Do not assume a dataset is suitable because it is labelled RF fingerprinting data.
- Do not treat random sample splits as valid evidence where session/time independence is unavailable.
- Do not introduce hardware as a prerequisite for software-stage validation.

## Immediate Next Action

Build the candidate dataset portfolio and qualification records for D1-D10. Each candidate must have a documented role, requirements coverage, missing information, validation possibility, license status, and decision.

## Blocking Questions

- Which public datasets satisfy the mandatory requirements for each D stage?
- Which dataset combinations provide complementary experimental coverage?
- Which claims can be supported by each dataset, and which cannot?

## Continuity Instruction

A future ChatGPT session must read this file together with `PROJECT_MASTER_PLAN.md`, `CURRENT_OBJECTIVE.md`, `docs/03_dataset_strategy/dataset_requirement_matrix.md`, and the latest session/decision records before continuing work.
