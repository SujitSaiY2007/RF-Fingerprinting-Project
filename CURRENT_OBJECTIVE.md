# CURRENT OBJECTIVE

## Current gate
**D1 — Raw RF Data / Ingestion**

The Dataset Search & Validation / Qualification workstream is complete as a development-substrate selection gate. It is not scientific validation.

## Immediate objective
Establish a reproducible, provenance-aware, integrity-checked ingestion layer for the selected RF datasets, beginning with WiSig and Oregon State WiFi RFFP.

## D1 must establish
- Dataset/version identity and source provenance.
- Acquisition instructions without committing raw RF archives.
- File/package manifests and checksums where feasible.
- Raw sample representation and dtype/shape interpretation.
- Metadata extraction into a common internal schema.
- Device/session/day/receiver/environment identifiers needed for later leakage-safe experiments.
- Basic integrity and loadability tests.
- Explicit handling of missing metadata.
- Reproducible local data-root configuration.

## Scientific discipline
Do not treat successful file loading as D1 scientific validation. D1 is complete only when its defined ingestion experiment, evidence, evaluation protocol and acceptance criteria are satisfied.

## Initial datasets
1. WiSig — primary scale/receiver/day substrate.
2. Oregon State WiFi RFFP — primary temporal/domain substrate.

Oregon State LoRa and SMoRFFI remain reserved for complementary downstream validation responsibilities.

## Continuity
Any material D1 decision, dataset limitation, protocol or acceptance result must be recorded in GitHub. Raw large datasets must remain outside Git.
