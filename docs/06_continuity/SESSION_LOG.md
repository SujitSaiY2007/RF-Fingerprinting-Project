# Session Log

## 2026-08-21 — Repository Initialization
The project repository was established as the persistent source of truth. Project-control files, Dataset Requirement Matrix, registry and qualification template were established.

## 2026-08-21 — Dataset Search & Qualification
Recovered the repository state, performed evidence-backed candidate research, qualified a complementary portfolio and recorded D1–D10 coverage/gaps. KEEP: WiSig, Oregon State WiFi RFFP, Oregon State LoRa RFFP, SMoRFFI. SECONDARY: ORACLE, Bluetooth smartphone RF database. No D1–D10 scientific validation was claimed.

## 2026-08-21 — Branch anomaly investigation and repair
### Finding
`main` and `develop` initially had independent/divergent histories. `main` was protected, so direct force movement was not used. PR #2 was merged into `develop`, integrating the dataset qualification work. A direct `develop` → `main` promotion exposed conflicts because of the independent histories.

### Lossless reconciliation
Before changing branch topology, explicit archive branches were created from the pre-reconciliation tips:
- `archive/pre-reconciliation-main-2026-08-21` → pre-reconciliation `main` `7770fcb517c5df986b1f5ad4d3e0a07a4995298c`.
- `archive/pre-reconciliation-develop-2026-08-21` → pre-reconciliation `develop` `9634ff446958d9f2af0d41e40625a5b5d5b46702`.

A reconciliation merge commit `fa88775ac569358cfe93b2f2a12b6d3b70300dd0` was then created with both pre-reconciliation tips as parents. The stable `main` tree was retained as the canonical working tree. No history was deleted or force-reset.

Both `main` and `develop` were moved to the reconciliation state and subsequently updated with the same continuity-file changes. A final GitHub comparison reported `main` and `develop` as **identical: 0 ahead / 0 behind**.

### Repository conclusion
The branch-history anomaly is resolved. The old histories remain reachable through the merge commit and explicit archive branches. Future development must not recreate independent `main`/`develop` histories.

## 2026-08-21 — D1 transition
Dataset qualification is complete as a development-substrate gate and the repository topology is clean. The next project gate is D1 Raw RF Data / Ingestion, beginning with WiSig and Oregon State WiFi.

D1 must first establish authoritative source/version provenance, acquisition instructions, manifests/checksums, raw-I/Q representation, metadata normalization, integrity/loadability tests, reproducible local data roots and leakage-safe partition foundations. Large raw datasets remain outside Git.

Successful loading is not D1 scientific validation. D1 is complete only when its defined experiment, evidence, evaluation protocol and acceptance criteria are satisfied.

## 2026-08-25 — Q2/Q4 novelty literature audit
A broad literature audit was performed in response to the professor's progress-meeting Question 2 (representation, decision making, security novelty) and Question 4 (review of existing solutions/articles).

### Findings
The audit rejected the following as standalone novelty claims because they are already established/active areas:
- physics-informed RF representation;
- learned RF embeddings;
- open-set RF fingerprint recognition;
- incremental/continual RF fingerprint learning;
- physics-aware temporal/test-time adaptation;
- generic adversarial robustness;
- historical device profiling by itself.

Representative evidence and source links are preserved in `docs/04_research/novelty_literature_gap_audit.md`.

### Refined research direction
The stronger candidate research gap is **secure continual RF device-profile evolution**, specifically separating:

`identity recognition`

from

`authorization to modify the persistent device profile`.

The central hypothesis is:

`Identification correctness != authorization to update the persistent profile`

A candidate update gate may combine identity confidence, embedding consistency, RF-physical consistency, temporal consistency, historical-profile consistency and anomaly/deviation evidence.

### D8/D9 coupling
This creates a direct research connection between D8 Continual Learning / Profile Evolution and D9 Poisoning / Adversarial Protection. D8 should eventually evaluate chronological profile evolution; D9 should test controlled/synthetic poisoning and whether the update-security mechanism limits profile corruption.

### Status
This is **provisional**. The literature audit must continue with a targeted forensic search for RF/RFFI systems that explicitly separate identity recognition from authorization to modify a persistent profile. No novelty, patentability or superiority claim is finalized yet.

The current objective remains D1; novelty work is a research-control activity and does not authorize premature D4/D8/D9 implementation.

## 2026-08-25 — Updated handoff
The canonical project-control files were updated with the Q2/Q4 findings. The next session must recover the updated repository state, complete the targeted novelty audit, and then continue D1 without restarting dataset qualification or project architecture.
