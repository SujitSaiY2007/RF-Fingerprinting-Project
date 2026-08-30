# D8 — Persistent Profile Evolution

**Date:** 2026-08-30  
**Track:** A  
**Status:** **IMPLEMENTED / TESTED / DEMONSTRATED; not scientifically validated.**

## Purpose
D8 separates four operations that must not be collapsed:

`OBSERVATION -> IDENTITY RECOGNITION -> UPDATE AUTHORIZATION -> PROFILE UPDATE`

Recognition evidence is supplied by the existing classifier path. The profile manager never retrains the classifier and never uses MAC/device identifiers as features.

## Frozen data contract
- Dataset: real user-supplied SMoRFFI archive.
- Archive SHA-256: `1d9ebcf2539e5fb7fb1dc678dba3fd2a50cada2befb86f5d84faff2b4f541037`.
- Known devices: 1–33.
- D2 input remains `serialized preamble -> complex[288] -> float32[2,288] I/Q`.
- Existing deterministic SHA-256 `(device_id|source_row_index)` 70/15/15 split is retained.
- Source-row ordering is used only to create a reproducible chronological **engineering stream**; it is **not** claimed to be temporal/session ordering.

## Profile state
Each persistent profile stores:
- device identity;
- running mean/centroid of standardized RF evidence;
- running dispersion (`m2` / variance);
- accepted observation count;
- profile version;
- last accepted source-row index;
- immutable-in-place audit history.

The update uses an online mean/M2 recurrence, so the profile can evolve without retaining all accepted observations.

## Authorization outcomes
- **ACCEPT_UPDATE** — recognition and admission policy permit persistent mutation.
- **HOLD_QUARANTINE** — identity may be plausible, but evidence is insufficient/conflicting or updates are disabled.
- **REJECT** — identity is outside the persistent profile store.

## Baseline ladder
Exactly four policies were implemented:
1. frozen/no-update;
2. always-update after recognition;
3. confidence-only admission using the frozen D6 threshold `0.30`;
4. multi-evidence: confidence `>=0.30` plus profile consistency distance below a threshold selected from known validation only.

The multi-evidence threshold is the 95th percentile of initial-profile distances on the known validation partition. It is **not** fit to the frozen test partition.

## Chronological protocol
For each known device:
- 50 earliest source-row-indexed training observations form enrollment;
- the next 150 source-row-indexed training observations form the update stream;
- validation remains available only for policy threshold selection;
- the frozen test partition is evaluated only after all updates and is never admitted before evaluation.

Feature standardization is fit on enrollment observations only.

## Observed Track-A result
The profile-only nearest-centroid readout is intentionally treated as a separate engineering readout, not as a replacement for D5 RF recognition. In this run:

| Policy | Frozen-test profile accuracy before stream | After stream | Updates | Holds |
|---|---:|---:|---:|---:|
| frozen/no-update | 28.66% | 28.66% | 0 | 4,950 |
| always-update | 28.66% | 38.17% | 4,950 | 0 |
| confidence-only | 28.66% | 38.17% | 4,950 | 0 |
| multi-evidence | 28.66% | 37.97% | 4,799 | 151 |

These values demonstrate that profile evolution changes persistent state and that the authorization layer can withhold updates. They do **not** establish that the profile mechanism is a better identity recognizer than the frozen D5 RF baseline.

### Recognition reproducibility caveat
The D8 engineering run refits the fixed D5 RF configuration locally only to provide recognition evidence to the profile manager. That local execution produced **85.67%** frozen-test RF accuracy, whereas the repository's frozen D5 recorded result is **87.39%**. This discrepancy is preserved as a reproducibility/environment issue and **does not modify or overwrite the canonical D5 metric**. No D5 retuning was performed.

## Scientific interpretation
D8 supports the architectural proposition that recognition and permission to modify persistent identity state can be separated. It does **not** yet establish robust continual RF learning or security superiority. D9 is specifically required to test whether the admission layer actually limits poisoning.

## Provenance / leakage controls
- No frozen test observation is used for profile updates.
- No test statistic is used for threshold selection.
- No MAC/device identifier is a feature.
- No temporal claim is made from SMoRFFI row order.
- All profile decisions retain source identifiers, policy, confidence, consistency distance, version transition and synthetic flag.
