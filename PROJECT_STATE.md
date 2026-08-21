# PROJECT STATE

**Last initialized:** 2026-08-21

## Authoritative status

- Project repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Default branch: `main`
- Development status: **Preparation Phase**
- Current workstream: **Dataset Search & Qualification**
- Implementation status: **Not started / intentionally gated**

## Established

1. Initial project concept and IDP.
2. Software-first development strategy using existing/public datasets wherever possible.
3. Complete conceptual architecture.
4. Dataset Requirement Matrix.
5. Ten dataset/validation stages D1–D10.
6. Dataset quality/provenance requirements.
7. Dataset acceptance methodology.
8. Separation of software/data validation from later hardware transfer validation.

## Current objective

Build and qualify the dataset portfolio required to support the claims and experiments across D1–D10. Do not begin substantial model implementation merely because a dataset is available; first establish that the dataset satisfies the requirements needed for the intended experiment.

## Immediate next actions

1. Populate the candidate dataset registry.
2. Search candidate datasets against the D1–D10 requirements.
3. Record evidence, missing requirements, licensing/provenance, and reproducibility information.
4. Assign KEEP / REJECT / SECONDARY decisions with reasons.
5. Identify coverage gaps that may require a secondary dataset or later controlled capture.
6. Lock the initial dataset portfolio.
7. Only then begin D1 implementation/validation.

## Important constraints

- Do not silently change the research question or scope.
- Do not claim a dataset supports a validation stage without evidence.
- Do not treat D1–D10 as completed merely because a pipeline component exists.
- Keep raw large datasets outside Git where appropriate; store metadata, manifests, checksums, acquisition instructions and qualification records in Git.
- Preserve historical decisions rather than overwriting them.
- Distinguish source-derived facts, experiment results, inference and speculation.

## Continuity rule

Any substantial ChatGPT session must end by updating the relevant project-state and continuity files. A future session must read this file and the latest continuity records before taking action.
