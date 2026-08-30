# D8–D10 Track-A Milestone Addendum — 2026-08-30

This file is an additive continuation of `PROJECT_STATE.md`, `CURRENT_HANDOFF.md`, and `docs/04_research/D7_D10_TRACK_A_NEXT_DIRECTION.md`. It does not delete or reinterpret earlier evidence.

## Completed in this milestone

### D8 — profile evolution
- Persistent profile manager implemented in `src/profile_evolution.py`.
- Recognition and update authorization are separate calls.
- Decisions: `ACCEPT_UPDATE`, `HOLD_QUARANTINE`, `REJECT`.
- Baseline ladder implemented: frozen/no-update, always-update, confidence-only, multi-evidence.
- Enrollment/update stream protocol: 50/150 source-row-indexed training observations per known device.
- Validation-only consistency threshold: 95th percentile = **1.357946538332526** in the recorded run.
- Frozen test partition is never used for profile updates.
- Core D8 run uses real SMoRFFI only; no synthetic attack observations are mixed into D8 evidence.
- D8 profile-only centroid accuracy rises from 28.66% to 38.17% under always/confidence-only updates and to 37.97% under multi-evidence. These are profile-readout engineering metrics, not replacements for D5 RF recognition.
- Local fixed-RF execution used to supply recognition evidence produced 85.67% test accuracy. The canonical D5 recorded 87.39% remains frozen and unchanged; no D5 retuning was performed.

### D9 — poisoning
- Controlled/derived attack suite implemented.
- Attack families: unknown-device contamination, replay/repetition, gradual 0–3 dB derived gain drift, and label contamination.
- Unknown attack source: devices 34–40; candidate observations selected by the frozen recognizer as target identity 1 with D6 confidence >= 0.30.
- Multi-evidence + replay guard reduced exact replay acceptance to 1% with 99% held, but **unknown target-like contamination remained at 100% acceptance** in this constructed scenario.
- Target profile displacement versus the clean reference was approximately **0.633 standardized-feature units**.
- This is an explicit negative/falsifying boundary condition. The novelty hypothesis is not assumed true.

### D10 — auditable lifecycle
- Integrated demonstrator implemented.
- Demonstrated: known legitimate acceptance; legitimate profile evolution; unknown rejection by frozen D6 confidence; suspicious replay handling; persistent audit and profile versioning.
- The first target-like suspicious observation can still pass; its exact replay is quarantined by the replay guard.
- D10 therefore demonstrates the lifecycle and exposes a security limitation; it is not a security guarantee.

## Files added
- `src/profile_evolution.py`
- `scripts/run_smorffi_d8.py`
- `scripts/run_smorffi_d9.py`
- `scripts/run_smorffi_d10.py`
- `tests/test_profile_evolution.py`
- `configs/track_a_d8_profile_evolution.json`
- `configs/track_a_d9_poisoning.json`
- `configs/track_a_d10_lifecycle.json`
- `experiments/track_a/d8_profile_metrics.json`
- `experiments/track_a/d9_poisoning_metrics.json`
- `experiments/track_a/d10_lifecycle_metrics.json`
- `docs/04_research/D8_PROFILE_EVOLUTION.md`
- `docs/04_research/D9_PROFILE_POISONING.md`
- `docs/04_research/D10_AUDITABLE_LIFECYCLE.md`

## Verification
- New profile-manager unit tests: **5 passed**.
- D8, D9 and D10 scripts were executed against the supplied SMoRFFI archive (same recorded SHA-256 as the canonical archive).
- All constructed attack scenarios are explicitly labelled synthetic/derived.

## Status discipline
D8–D10 are now **Implemented / Tested / Demonstrated** for Track A. They are **not Scientifically Validated**. Track-B real temporal/session/environment/receiver/cross-dataset validation remains separate.

## Open engineering/security limitation
The next meaningful improvement is **not** to overwrite the current multi-evidence policy. Instead, add new ablations for delayed/batched promotion, multi-observation diversity, stronger cross-evidence agreement, and rollback/recovery. Each must be compared against the frozen D8 ladder and must preserve the negative D9 result.

## Branch rule
This milestone is committed to `develop` only. `main` remains untouched until an explicit milestone-synchronization decision is made.
