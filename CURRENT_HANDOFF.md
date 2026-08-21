# CURRENT HANDOFF — 2026-08-21

## Project

Physics-Based RF Fingerprinting with Continuous Device Learning.

## Phase / workstream

- Phase 1 — Preparation
- Dataset Search & Validation / Qualification

## Team state

Four members are working on the same dataset-search/qualification workstream. No permanent technical division exists.

## What this session completed

- Recovered and checked the project control layer and Dataset Requirement Matrix.
- Confirmed the registry was initially empty apart from its header.
- Performed external evidence-backed candidate research.
- Added preliminary qualification records for WiSig, Oregon State WiFi RFFP, Oregon State LoRa RFFP, SMoRFFI, ORACLE and a Bluetooth smartphone RF database.
- Populated the dataset registry.
- Established a preliminary multi-dataset portfolio: WiSig, Oregon WiFi, Oregon LoRa and SMoRFFI as KEEP; ORACLE and Bluetooth as SECONDARY.
- Identified that no single dataset currently provides sufficient evidence for all D1–D10 responsibilities.

## What remains incomplete

- The portfolio is **not locked**.
- Direct download-package and metadata verification remains outstanding.
- Dataset-specific license/access terms require confirmation.
- SMoRFFI D7/D8 suitability is unresolved.
- Oregon scenario-level sequential semantics require verification.
- D6 open-set protocols still need explicit identity-level split design.
- D8 continual-learning data protocol is not yet fully qualified.
- D9 remains a controlled/synthetic poisoning experiment over legitimate RF data.
- D1 implementation remains intentionally gated.

## Important repository issue

`main` and `develop` are currently diverged: GitHub reports each branch as 7 commits ahead of the other. The project documentation describes a clean main -> develop -> main integration flow, but the current refs do not satisfy that state. This must be reconciled before using `develop` as a clean integration baseline.

## Exact next action

Directly inspect and verify the actual packages/metadata for WiSig and Oregon State RFFP first. Record each major requirement as VERIFIED, REPORTED, UNKNOWN or NOT SUPPORTED. Then perform the same verification for SMoRFFI and ORACLE, produce the final D1–D10 coverage/gap matrix, and decide whether the portfolio can be locked.
