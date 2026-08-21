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
A prior structural anomaly existed because `main` and `develop` had independent histories. PR #2 has now been integrated into `develop`. PR #4 is the current reconciliation mechanism, using a branch based on `main` so protected history is not force-rewritten.

### Temporary branch-protection exception — 2026-08-21
The team requested **Option B**: temporarily relax the `main` branch protection requirement for an approving review so the repository owner can merge PR #4 personally, with the intention of restoring the protection rule afterward.

This was attempted through the available GitHub integration. The integration does not expose branch-protection/rules administration, so the protection requirement could not be changed programmatically. An attempted auto-merge path also failed because GitHub auto-merge is disabled for this repository. **No branch-protection rule was changed.** PR #4 therefore remains blocked pending either a manual rule change by a repository administrator or an approval from another authorized reviewer.

This is an operational repository constraint, not a scientific/project-state decision. Once the reconciliation is complete, restore/enforce the intended protection rule and record the final rule state here.

## Next action
Complete the main/develop reconciliation through PR review/merge, verify the branches are structurally aligned, then begin D1.
