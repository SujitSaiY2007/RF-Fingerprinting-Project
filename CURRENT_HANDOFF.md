# CURRENT HANDOFF — 2026-08-21

## Project
Physics-Based RF Fingerprinting with Continuous Device Learning.

## Current state
- Phase 1 — Preparation.
- Dataset Search & Validation / Qualification completed as the development-substrate selection gate.
- Next gate: **D1 — Raw RF Data / Ingestion**.
- Four members remain on the same overall workstream; no permanent technical division exists.

## Qualified development portfolio
### KEEP
- WiSig — scale, receiver variation, multi-day robustness.
- Oregon State WiFi RFFP — temporal/domain variation.
- Oregon State LoRa RFFP — same-model/environment/location/distance/receiver variation.
- SMoRFFI — large-scale same-model discrimination.

### SECONDARY
- ORACLE — controlled hardware/distance benchmark.
- Bluetooth smartphone RF database — optional cross-technology benchmark.

## Scientific status
D1–D10 remain scientifically incomplete. Dataset qualification is not validation.

## Repository reconciliation status
PR #2 has been merged into `develop`. The earlier attempt to directly promote `develop` to `main` exposed merge conflicts because the branches have independent histories. `main` is protected against force-push. A reconciliation branch based on `main` is now synchronizing the required stable-tree content through a normal PR.

## Exact next actions
1. Complete and merge the main/develop reconciliation PR.
2. Re-compare `main` and `develop` and verify the structural anomaly is cleared or explicitly characterized.
3. Begin D1 using WiSig + Oregon State WiFi.
4. Record package metadata, provenance, checksums/manifests and ingestion acceptance evidence in GitHub.

## D1 boundary
Successful loading is not scientific validation. D1 requires defined experiments, evidence and acceptance criteria.
