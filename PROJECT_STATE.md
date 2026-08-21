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

## Repository consistency — RESOLVED
The previous `main`/`develop` history divergence has been reconciled without discarding either history.

- Pre-reconciliation `main`: `7770fcb517c5df986b1f5ad4d3e0a07a4995298c`
- Pre-reconciliation `develop`: `9634ff446958d9f2af0d41e40625a5b5d5b46702`
- Reconciliation merge commit: `fa88775ac569358cfe93b2f2a12b6d3b70300dd0`
- Both `main` and `develop` now point to the subsequent common canonical state after the continuity update.
- The reconciliation commit has both pre-reconciliation tips as parents, preserving both histories in the reachable commit graph.
- Archive branches `archive/pre-reconciliation-main-2026-08-21` and `archive/pre-reconciliation-develop-2026-08-21` preserve the two branch tips independently as explicit recovery references.
- The canonical working tree is the stable `main` tree, with the `develop` history preserved as the second parent.
- GitHub comparison reports `main` and `develop` as **identical**: 0 commits ahead, 0 behind.

No force-reset or history deletion was used.

## Branch protection note
The temporary Option B request was not executable through the available GitHub integration. No branch-protection rule was changed programmatically. PR #4 was merged after the repository owner handled the required approval-rule condition manually. The intended protection rule should be restored/enforced if it was temporarily relaxed during the merge.

## Next action
The repository topology is clean. Begin D1: Raw RF Data / Ingestion using WiSig + Oregon State WiFi, while preserving Oregon State LoRa and SMoRFFI for complementary downstream validation responsibilities.
