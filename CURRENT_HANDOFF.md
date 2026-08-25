# CURRENT HANDOFF — 2026-08-25

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
- No force-reset or history deletion was used.

## Branch workflow from this point
Use:

`task/research branch → Pull Request → develop → review/integration → Pull Request → main`

Do not recreate independent `main`/`develop` histories.

## Qualified dataset portfolio
### KEEP — primary
1. **WiSig** — scale, receiver variation, multi-day/channel robustness.
2. **Oregon State WiFi RFFP** — temporal/domain variation and repeated-device observations.
3. **Oregon State LoRa RFFP** — same-model/environment/location/distance/receiver variation.
4. **SMoRFFI** — large-scale same-model discrimination.

### SECONDARY — supporting
5. **ORACLE** — controlled transmitter-hardware/distance benchmark.
6. **Bluetooth smartphone RF database** — optional cross-technology benchmark.

## Q2/Q4 novelty research — 2026-08-25
A broad literature audit was performed before freezing the novelty direction.

### Weak standalone novelty claims rejected
The following are established/active research areas and must not be presented as standalone novelty:
- physics-informed RF representation;
- learned RF device embeddings;
- open-set RF fingerprint recognition;
- incremental/continual RF fingerprint learning;
- physics-aware temporal/test-time adaptation;
- generic adversarial robustness;
- historical device profiling by itself.

Detailed evidence and representative literature are recorded in:
`docs/04_research/novelty_literature_gap_audit.md`

### Current primary novelty hypothesis — provisional
> **Secure continual RF device-profile evolution through explicit separation of identity recognition from authorization to modify the persistent device profile.**

Core distinction:

`Identification correctness != authorization to update the persistent profile`

The candidate architecture may allow an observation to be accepted for identity/authentication while rejecting it for persistent profile update when physical, embedding-space, temporal, historical-profile or anomaly evidence is inconsistent.

### Supporting candidate mechanism
A **multi-evidence update authorization gate** may combine:
- identity confidence;
- embedding consistency;
- RF-physical consistency;
- temporal consistency;
- historical-profile consistency;
- anomaly/deviation evidence.

This is a research hypothesis, not a frozen algorithm.

### D8/D9 connection
The novelty investigation connects D8 Continual Learning / Profile Evolution with D9 Poisoning / Adversarial Protection. D8 establishes chronological profile evolution; D9 evaluates controlled/synthetic poisoning and profile-corruption resistance.

### Novelty status
**PROVISIONAL — NOT FINALIZED.**

A targeted forensic Q4 audit is still required before the candidate gap becomes a formal contribution. It must explicitly test whether prior RF/RFFI systems separate identity recognition from permission to modify a persistent device profile.

## D1 objective
Build a reproducible, provenance-aware, integrity-checked raw-RF ingestion foundation, initially using:

1. **WiSig**
2. **Oregon State WiFi RFFP**

D1 must establish authoritative source/version identity, provenance, acquisition instructions, manifests/checksums, raw-I/Q interpretation, common metadata, leakage-safe identifiers, integrity/loadability tests, missing-metadata handling, reproducible local data roots and separation of raw/normalized/derived/experiment data.

## Important downstream constraints
- Avoid random sample splits when session/burst leakage is possible.
- Prefer session/day/device/receiver holdouts appropriate to the claim.
- D6 requires explicit unseen-identity construction.
- D8 requires a chronological profile-update protocol with frozen evaluation and rollback protection.
- D9 uses legitimate RF data plus controlled/synthetic poisoning and must be labelled accordingly.
- D10 is integrated end-to-end validation.
- Hardware transfer remains later.

## Immediate next actions
1. Complete the targeted Q4 novelty audit and record the nearest-prior comparison.
2. Do not implement the candidate novelty mechanism until the differentiator is supported and an experiment can falsify it.
3. Continue D1: define the ingestion specification and acceptance checklist.
4. Verify authoritative WiSig and Oregon State WiFi packages/metadata.
5. Implement and validate the minimal reproducible ingestion layer.

## Research discipline
Distinguish source-derived facts, repository-derived facts, project decisions, experimental results, inference, hypothesis and speculation. Do not claim novelty, superiority, publication-worthiness or patentability without evidence.
