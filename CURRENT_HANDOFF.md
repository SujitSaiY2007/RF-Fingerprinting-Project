# CURRENT HANDOFF — 2026-08-21

## Project
**Physics-Based RF Fingerprinting with Continuous Device Learning**

## Canonical repository
`SujitSaiY2007/RF-Fingerprinting-Project`

## Authoritative project state
- Phase: **Phase 1 — Preparation**.
- Current workstream/gate: **D1 — Raw RF Data / Ingestion**.
- Dataset Search & Validation / Qualification is complete as the development-substrate selection gate.
- D1–D10 are **not scientifically completed**.
- Team size: 4.
- All four members remain on the same overall workstream; no permanent technical division exists.

## Repository state — verified
The earlier `main`/`develop` history anomaly has been resolved without intentional history loss.

- Pre-reconciliation `main`: `7770fcb517c5df986b1f5ad4d3e0a07a4995298c`.
- Pre-reconciliation `develop`: `9634ff446958d9f2af0d41e40625a5b5d5b46702`.
- Lossless reconciliation commit: `fa88775ac569358cfe93b2f2a12b6d3b70300dd0`.
- That reconciliation commit has both pre-reconciliation tips as parents.
- Explicit archive branches preserve both old tips:
  - `archive/pre-reconciliation-main-2026-08-21`
  - `archive/pre-reconciliation-develop-2026-08-21`
- `main` and `develop` were re-compared after reconciliation and reported **identical: 0 ahead / 0 behind**.
- The continuity-file updates after reconciliation were intentionally applied to the common branch state.
- No force-reset or history deletion was used.

## Branch workflow from this point
Use:

`task/research branch → Pull Request → develop → review/integration → Pull Request → main`

Do not recreate independent `main`/`develop` histories. Branches represent collaboration/isolation, not permanent technical ownership.

## Qualified dataset portfolio
### KEEP — primary
1. **WiSig** — scale, receiver variation, multi-day/channel robustness.
2. **Oregon State WiFi RFFP** — temporal/domain variation and repeated-device observations.
3. **Oregon State LoRa RFFP** — same-model/environment/location/distance/receiver variation.
4. **SMoRFFI** — large-scale same-model discrimination.

### SECONDARY — supporting
5. **ORACLE** — controlled transmitter-hardware/distance benchmark.
6. **Bluetooth smartphone RF database** — optional cross-technology benchmark.

Do not resume an open-ended dataset search unless D1–D10 experimentation exposes a specific data, metadata, reproducibility, access/licensing or coverage gap.

## D1 objective
Build a reproducible, provenance-aware, integrity-checked raw-RF ingestion foundation, initially using:

1. **WiSig**
2. **Oregon State WiFi RFFP**

D1 must establish:
- authoritative dataset/version identity and provenance;
- acquisition/download instructions;
- package/file manifests and checksums where feasible;
- correct raw-I/Q representation, file format, dtype, shape and channel interpretation;
- a common metadata schema while preserving source-specific metadata;
- device/session/day/receiver/environment/location identifiers needed for later leakage-safe experiments;
- loadability and integrity tests;
- explicit handling of missing/ambiguous metadata;
- reproducible local data-root configuration;
- separation of raw data, normalized metadata, derived data and experiment outputs.

## D1 scientific boundary
Do **not** treat successful file loading as scientific validation. D1 is complete only after its defined experiment, evidence, evaluation protocol and acceptance criteria are satisfied.

Do not prematurely build the classifier, embedding model, continual-learning system or poisoning defense during the initial D1 foundation work.

## Important downstream constraints already established
- Avoid random sample splits when session/burst leakage is possible.
- Prefer session/day/device/receiver holdouts appropriate to the claim.
- D6 requires explicit unseen-identity construction.
- D8 requires a chronological profile-update protocol with frozen evaluation, profile acceptance and rollback protection.
- D9 uses legitimate RF data plus controlled/synthetic poisoning and must be labelled accordingly.
- D10 is integrated end-to-end validation.
- Hardware transfer remains later.

## Immediate next actions
1. Read the current repository state before substantive work.
2. Define the D1 ingestion specification and acceptance checklist.
3. Verify the authoritative WiSig and Oregon State WiFi download/package structure and metadata directly from their original sources.
4. Create source-aware dataset manifests and checksum/provenance records without committing large raw archives.
5. Implement the minimal reproducible ingestion layer and tests.
6. Test raw representation and metadata normalization.
7. Record D1 evidence, limitations, unresolved questions and acceptance results in GitHub.

## Critical research discipline
Distinguish source-derived facts, project decisions, experimental results, inference, hypothesis and speculation. Do not infer undocumented metadata. Do not alter research claims to fit dataset convenience. Do not declare any D-stage complete merely because code or documentation exists.

## Required first response in the next ChatGPT session
Before substantive work, provide a concise **CONTINUITY CHECK** containing:
1. Current phase.
2. Current workstream/gate.
3. Four-member team state.
4. Last completed repository milestone.
5. Important established decisions.
6. Open research questions.
7. Current blockers.
8. Exact next step.
9. Any contradiction, stale assumption, missing evidence or repository inconsistency detected.

Then execute D1 from the recovered repository state without restarting the project.
