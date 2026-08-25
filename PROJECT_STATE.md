# PROJECT STATE

**Last updated:** 2026-08-25

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

## Novelty research status — 2026-08-25
A broad Q2/Q4 literature audit was performed before freezing the project's novelty direction.

### Weak standalone novelty claims rejected
The following are established or active research areas and are therefore **not** treated as standalone project novelty:
- physics-informed RF representation;
- learned RF device embeddings;
- open-set RF fingerprint recognition;
- prototype/embedding-based unknown-device decision;
- incremental/continual RF fingerprint learning;
- physics-aware temporal/test-time adaptation;
- generic adversarial robustness of RF fingerprinting;
- historical device profiling by itself.

Detailed evidence and representative literature are recorded in:
`docs/04_research/novelty_literature_gap_audit.md`

### Current primary novelty hypothesis
The project will investigate:

> **Secure continual RF device-profile evolution through explicit separation of identity recognition from authorization to modify the persistent device profile.**

Core distinction:

`Identification correctness != authorization to update the persistent profile`

The candidate system may accept an observation for identity/authentication while rejecting it for profile update when physical, embedding-space, temporal, historical-profile or anomaly evidence is inconsistent.

### Supporting candidate mechanism
A **multi-evidence update authorization gate** may combine:
- identity confidence;
- embedding consistency;
- RF-physical consistency;
- temporal consistency;
- historical-profile consistency;
- anomaly/deviation evidence.

This mechanism is a research hypothesis, not a frozen algorithm or novelty claim.

### D8/D9 connection
The novelty investigation connects:
- **D8 — Continual Learning / Profile Evolution**: chronological profile evolution with frozen evaluation and update acceptance;
- **D9 — Poisoning / Adversarial Protection**: controlled/synthetic poisoning and evaluation of profile-corruption resistance.

The central security question is whether a continuously learning RF fingerprinting system can evolve legitimate device profiles without allowing anomalous or adversarial observations to silently corrupt them.

### Novelty claim status
**PROVISIONAL — NOT FINALIZED.**

The team must perform a targeted forensic literature audit before promoting the candidate gap to a formal contribution. The audit must explicitly search whether existing RF/RFFI systems separate identity recognition from authorization to modify a persistent device profile.

## Remaining scientific gates
D6 requires explicit unseen-identity holdouts; D8 requires a chronological profile-update protocol with frozen evaluation, profile acceptance and rollback; D9 requires controlled/synthetic poisoning; D10 requires integrated end-to-end validation; hardware transfer remains later.

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

## Next action
Do **not** abandon the D1 gate. The novelty research has been recorded as a project-control update, not as permission to prematurely implement D4/D8/D9.

Immediate sequence:
1. Complete the targeted Q4 novelty audit around secure profile-update authorization.
2. Preserve the resulting evidence and nearest-prior comparison in GitHub.
3. Then continue the D1 Raw RF Data / Ingestion work using WiSig + Oregon State WiFi.
4. Do not implement the final novelty mechanism until the targeted audit and experiment design establish the exact differentiator.
