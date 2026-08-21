# PROJECT STATE

**Last updated:** 2026-08-21

## Authoritative status

- Project repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Stable branch: `main`
- Integration branch: `develop`
- Development status: **Phase 1 — Preparation**
- Current workstream: **Dataset Search & Validation / Qualification**
- Implementation status: **D1 ready to begin after PR/repository reconciliation**
- Team size: **4 members**

## Current team model

All four team members remain on the same overall dataset-search/qualification workstream. No permanent technical division exists.

## Dataset qualification milestone

The initial portfolio has now been qualified sufficiently to select development substrates for D1–D10. This is a **portfolio readiness decision**, not scientific validation of D1–D10.

### Primary KEEP datasets

- WiSig — scale, receiver variation, multi-day robustness.
- Oregon State WiFi RFFP — temporal/domain variation with repeated Pycom devices.
- Oregon State LoRa RFFP — same-model, environmental/location/distance/receiver variation.
- SMoRFFI — large-scale same-model discrimination.

### SECONDARY datasets

- ORACLE — controlled hardware-impairment/distance benchmark.
- Bluetooth smartphone RF database — optional cross-technology benchmark; non-blocking.

## D1–D10 coverage decision

The portfolio provides a defensible data substrate for all ten stages. D6 is supported by constructible identity-level holdouts; D8 has adequate repeated temporal observations but still requires a formally specified continual-learning protocol; D9 uses legitimate RF data plus controlled/synthetic poisoning under DEC-005.

The portfolio does not itself prove any stage. Scientific completion remains experiment-dependent.

## Remaining non-dataset gaps

1. Leakage-safe session/day/device split implementation.
2. Explicit D6 unknown-identity holdout protocol and metrics.
3. Explicit chronological D8 profile-update stream, frozen evaluation population, acceptance and rollback rules.
4. Controlled/synthetic D9 poisoning generation and evaluation.
5. Cross-dataset normalization and common RF representation.
6. Later hardware-transfer validation.

These are experimental/design gates, not blockers to beginning D1.

## Repository consistency issue

`main` and `develop` remain diverged by 7 commits in each direction. This is a repository integration issue and should be reconciled before using `develop` as the long-term integration baseline.

## Phase transition decision

**Dataset Search & Qualification is complete for the purpose of selecting D1 development substrates, subject to scientific re-evaluation if implementation reveals a material contradiction.** Further dataset searching should be triggered only by a specific evidence gap, access/licensing failure, or reproducibility failure.

## Exact next action

1. Review/merge the dataset qualification PR into `develop` after team review.
2. Deliberately reconcile `develop` and `main`.
3. Begin D1: raw RF ingestion/provenance validation on WiSig + Oregon State WiFi as the initial implementation pair.
4. Preserve SMoRFFI and Oregon LoRa as parallel validation substrates for later D3–D7 work.

## Validation status

D1–D10 remain scientifically incomplete. Dataset qualification is a readiness gate, not validation evidence.
