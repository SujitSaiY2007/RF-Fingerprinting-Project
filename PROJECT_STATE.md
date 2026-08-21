# PROJECT STATE

**Last updated:** 2026-08-21

## Authoritative status

- Project repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Stable branch: `main`
- Integration branch: `develop`
- Development status: **Phase 1 — Preparation**
- Current workstream: **Dataset Search & Validation / Qualification**
- Implementation status: **Not started / intentionally gated**
- Team size: **4 members**

## Current team model

All four team members are currently working on the **same overall workstream** at individual levels: Dataset Search & Validation. There is currently **no permanent technical division or fixed member-to-module ownership**. Independent overlap is expected and should be consolidated through GitHub.

## Established project baseline

1. Initial project concept and IDP.
2. Software-first strategy using existing/public datasets as the primary development and validation substrate.
3. Complete conceptual architecture.
4. Dataset Requirement Matrix.
5. Ten dataset/validation stages D1–D10.
6. Dataset quality/provenance requirements.
7. Dataset acceptance/qualification methodology.
8. Separation of software/data validation from later hardware-transfer validation.
9. GitHub repository as persistent project source of truth and ChatGPT continuity mechanism.
10. Four-member collaboration model with branch/PR-based integration.

## Current objective

Identify, compare and qualify candidate datasets against the established D1–D10 requirements and build a defensible dataset portfolio. Do not begin substantial model implementation merely because a dataset is available.

## Immediate next actions

1. Populate/extend the candidate dataset registry.
2. Search candidates against D1–D10 requirements.
3. Record evidence, missing requirements, licensing/provenance and reproducibility information.
4. Allow each of the four members to record independent investigations without assuming permanent technical ownership.
5. Compare overlapping findings and consolidate them into canonical qualification records.
6. Assign KEEP / SECONDARY / REJECT decisions with explicit reasons.
7. Identify coverage gaps and whether a secondary dataset or later controlled capture is required.
8. Lock the initial dataset portfolio.
9. Begin D1 implementation/validation only after the portfolio is sufficiently qualified.

## Integration model

`Individual research/task branch -> Pull Request -> develop -> review/integration -> Pull Request -> main`

The branch model is for safe collaboration, traceability and integration; it is **not** a statement that the four members own separate technical modules. During the current dataset workstream, multiple members may work on the same dataset/topic.

A merge into `main` means the repository change is integrated into the stable project state. It does **not** by itself mean that a scientific claim, dataset qualification, or D-stage has been validated.

## Important constraints

- Do not silently change the research question or scope.
- Do not claim a dataset supports a validation stage without evidence.
- Do not treat D1–D10 as completed merely because requirements or code exist.
- Do not invent permanent team-member responsibilities.
- Do not discard overlapping team findings merely because another member submitted first.
- Keep raw large datasets outside Git where appropriate; store metadata, manifests, checksums, acquisition instructions and qualification records in Git.
- Preserve historical decisions rather than overwriting them.
- Distinguish source-derived facts, experiment results, inference and speculation.

## Continuity rule

Any substantial ChatGPT session must end by updating the relevant project-state and continuity files. A future session must read this file and the latest continuity records before taking substantive action.
