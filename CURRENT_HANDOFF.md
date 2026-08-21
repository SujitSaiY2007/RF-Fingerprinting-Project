# CURRENT HANDOFF — 2026-08-21

## Project

Physics-Based RF Fingerprinting with Continuous Device Learning.

## Phase / workstream

- Phase 1 — Preparation
- Dataset qualification gate completed
- Next workstream: D1 Raw RF Data / Ingestion

## Team state

Four members continue to work collaboratively on the same overall project. No permanent technical division has been created.

## Dataset milestone completed

The first serious candidate search and qualification pass is complete. The development-substrate portfolio is now:

### KEEP
- WiSig — scale, receiver variation, multi-day robustness.
- Oregon State WiFi RFFP — temporal/domain variation with repeated Pycom devices.
- Oregon State LoRa RFFP — same-model and environmental/location/distance/receiver variation.
- SMoRFFI — large-scale same-model discrimination.

### SECONDARY
- ORACLE — controlled hardware-impairment/distance benchmark.
- Bluetooth smartphone RF database — optional cross-technology benchmark.

The portfolio is locked for development-substrate selection, not protected from later scientific revision.

## Scientific status

D1–D10 remain incomplete. Dataset qualification is not scientific validation.

## Remaining research/engineering gaps

1. D1 ingestion must verify actual package metadata, checksums, framing and provenance.
2. D6 requires explicit identity-level unknown-device holdouts and open-set metrics.
3. D8 requires a chronological profile-update stream, frozen evaluation set, acceptance policy and rollback mechanism.
4. D9 requires controlled/synthetic poisoning over legitimate RF data.
5. Cross-dataset normalization/common RF representation must be defined.
6. Hardware transfer remains a later validation stage.

## Repository issue

`main` and `develop` remain diverged by seven commits in each direction. Reconcile deliberately after PR #2 review; do not silently reset either branch.

## Exact next action

Review PR #2, reconcile the branch topology, then start D1 implementation on WiSig + Oregon State WiFi. During D1 ingestion, convert reported dataset properties into package-level VERIFIED/UNKNOWN records and capture checksums/manifests without committing raw RF archives.
