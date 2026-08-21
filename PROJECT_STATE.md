# PROJECT STATE

**Last updated:** 2026-08-21

## Authoritative status
- Repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Stable branch: `main`
- Integration branch: `develop`
- Phase: **Phase 1 — Preparation**
- Current gate: **D1 — Raw RF Data / Ingestion**
- Implementation status: D1 not yet implemented
- Team size: 4

## Team model
All four members currently work on the same overall project workstream. No permanent technical division exists.

## Dataset qualification milestone
The dataset-search/qualification gate is complete for development-substrate selection.

### KEEP
- WiSig — scale, receiver variation, multi-day robustness.
- Oregon State WiFi RFFP — temporal/domain variation.
- Oregon State LoRa RFFP — same-model/environment/location/distance/receiver variation.
- SMoRFFI — large-scale same-model discrimination.

### SECONDARY
- ORACLE — controlled hardware/distance benchmark.
- Bluetooth smartphone RF database — optional cross-technology benchmark.

This does not constitute scientific validation of D1–D10.

## D1 entry conditions
- Portfolio selected.
- Large raw datasets remain outside Git.
- D1 must establish common ingestion, provenance, metadata, integrity/checksum and leakage-safe partition foundations.
- Initial implementation pair: WiSig + Oregon State WiFi.

## Remaining scientific gates
D6 requires explicit unseen-identity holdouts; D8 requires a chronological profile-update protocol with frozen evaluation and rollback; D9 requires controlled/synthetic poisoning; D10 requires integrated end-to-end validation; hardware transfer remains later.

## Repository consistency
A prior structural anomaly existed because `main` and `develop` had independent histories. PR #2 has now been integrated into `develop`. A reconciliation branch based on `main` is being prepared to synchronize the stable tree without force-moving protected `main`. The branches should only be considered fully reconciled after the reconciliation PR is merged and the refs are re-compared.

## Next action
Complete the main/develop reconciliation through PR review/merge, verify the branches are structurally aligned, then begin D1.
