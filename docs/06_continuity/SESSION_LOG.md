# Session Log

## 2026-08-21 — Repository Initialization

The project repository was initialized as the persistent source of truth. Project-control files, Dataset Requirement Matrix, registry and qualification template were established. No scientific validation was claimed.

## 2026-08-21 — Dataset Search & Qualification

### Continuity recovery

Recovered the repository control layer, project baseline, architecture index, Dataset Requirement Matrix, decision log, session log, dataset registry and qualification template. Confirmed the Phase 1 dataset-search state and verified that no qualified dataset had previously been recorded.

### Repository verification

- `main` is the stable branch and `develop` exists as the integration branch.
- No project Issues were found.
- PR #1 is merged and infrastructure-only.
- `main` and `develop` remain diverged by 7 commits in each direction; this is a repository integration issue requiring deliberate reconciliation.

### External research completed

Evidence was gathered from authoritative/primary or strong research sources for WiSig, Oregon State WiFi/LoRa RFFP, SMoRFFI, ORACLE and a Bluetooth smartphone RF database.

### Dataset qualification completed

The first serious candidate portfolio is now selected for development use:

**KEEP / PRIMARY**
- WiSig — scale, receiver variation, multi-day robustness.
- Oregon State WiFi RFFP — temporal/domain variation and repeated Pycom devices.
- Oregon State LoRa RFFP — same-model plus environment/location/distance/receiver variation.
- SMoRFFI — large-scale same-model discrimination.

**SECONDARY**
- ORACLE — controlled hardware-impairment/distance benchmark.
- Bluetooth smartphone RF database — optional cross-technology benchmark.

Added `datasets/PORTFOLIO_LOCK_AND_GAP_ANALYSIS_2026-08-21.md` with the D1–D10 coverage matrix and residual gaps.

### Decision

Dataset Search & Qualification is complete **as a development-substrate selection gate**. This is not scientific validation. Further dataset search should only be triggered by a concrete experimental, access/licensing, metadata or reproducibility failure.

### Remaining scientific/engineering gaps

1. D1 package-level ingestion/provenance/checksum verification.
2. Leakage-safe session/day/device split implementation.
3. Explicit D6 unknown-identity holdout protocol and metrics.
4. Explicit D8 chronological update stream, frozen evaluation population, acceptance and rollback rules.
5. Controlled/synthetic D9 poisoning experiment.
6. Cross-dataset normalization/common RF representation.
7. Later hardware-transfer validation.

### Exact next step

Review and merge the dataset qualification PR into `develop`, deliberately reconcile `main`/`develop`, then begin D1 implementation using WiSig and Oregon State WiFi as the initial pair. Preserve Oregon LoRa and SMoRFFI for their complementary validation responsibilities.

### Validation boundary

D1–D10 remain scientifically incomplete. The dataset portfolio is a readiness decision, not validation evidence.
