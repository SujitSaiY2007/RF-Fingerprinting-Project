# Session Log

## 2026-08-21 — Repository Initialization

The project repository was initialized as the persistent source of truth. Project-control files, Dataset Requirement Matrix, registry and qualification template were established. No scientific validation was claimed.

## 2026-08-21 — Dataset Search & Preliminary Qualification Pass

### Continuity recovery

Recovered and inspected the repository control layer, project baseline, system-architecture index, Dataset Requirement Matrix, decision log, session log, dataset registry and qualification template. Confirmed the repository's stated Phase 1 / Dataset Search & Qualification state.

### Repository verification

- `main` is the stable branch and `develop` exists as the integration branch.
- The dataset registry was previously empty apart from its header.
- No project Issues were found.
- PR #1 is merged and established infrastructure only.
- `main` and `develop` are currently diverged; GitHub reports 7 commits ahead and 7 commits behind. This is a repository consistency issue that requires later reconciliation.

### External research completed

Evidence was gathered from authoritative/primary or strong research sources for:

- WiSig: UCLA CORES dataset page and WiSig dataset repositories/publication.
- Oregon State WiFi and LoRa RFFP: NetSTAR dataset page, release note and public dataset index; supporting survey evidence for LoRa.
- ORACLE: GENESYS Lab official dataset page.
- SMoRFFI: 2026 Computer Networks data article and associated research-lab/public records.
- Bluetooth smartphone database: published dataset description and Zenodo DOI reference.

### Work completed

- Added `datasets/QUALIFICATION_2026-08-21_PORTFOLIO.md`.
- Added preliminary qualification records for WiSig, Oregon State RFFP, SMoRFFI, ORACLE and Bluetooth smartphone data.
- Populated `datasets/dataset_registry.csv`.
- Preliminary decisions: KEEP = WiSig, Oregon WiFi, Oregon LoRa, SMoRFFI; SECONDARY = ORACLE, Bluetooth smartphone database.

### Scientific interpretation

The evidence supports a multi-dataset strategy. WiSig is strongest for receiver/day scale; Oregon datasets provide temporal/environmental and same-model complements; SMoRFFI addresses same-model scale. No dataset currently proves all D1–D10 responsibilities. D8 remains incompletely qualified until sequential/temporal semantics are verified.

### Unresolved questions

1. Verify actual data-package metadata and sample representation for all primary candidates.
2. Confirm dataset-specific licensing/access terms.
3. Verify SMoRFFI session/day/receiver/environment metadata.
4. Verify Oregon scenario-level temporal/sequential semantics.
5. Define D6 identity-level open-set splits.
6. Define D8 sequential profile-update protocol and required data fields.
7. Produce final D1–D10 coverage/gap matrix.
8. Reconcile `main` and `develop` before using `develop` as a clean integration baseline.

### Exact next step

Directly inspect the actual downloadable packages and metadata for WiSig and Oregon State RFFP first, then SMoRFFI and ORACLE. Upgrade claims from source-reported to project-verified where evidence permits; otherwise record UNKNOWN/NOT SUPPORTED. Only then decide whether the dataset portfolio can be locked.

### Validation boundary

D1–D10 remain scientifically incomplete. Dataset qualification is preparatory evidence, not experimental validation.
