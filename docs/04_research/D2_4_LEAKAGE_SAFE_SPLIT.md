# D2.4 — Leakage-Safe Split Policy for Track-A SMoRFFI

**Status:** IMPLEMENTED / TESTED as an engineering split
**Date:** 2026-08-30

## Dataset limitation

The inspected SMoRFFI CSVs expose device identity and source-row order but do not provide explicit session, burst-group, capture-time, receiver-instance, or day identifiers. The published collection is a controlled single-environment/single-day acquisition.

Therefore a true session/time holdout cannot be claimed from these files alone.

## Track-A engineering split

Each source observation is assigned deterministically from `(device_id, source_row_index)` using SHA-256. The first 64 bits are mapped to a uniform value `u`:

- `u < 0.70` -> train
- `0.70 <= u < 0.85` -> validation
- `u >= 0.85` -> test

Because the hash input contains the device identifier, each device contributes observations to all three partitions while no source row can appear in more than one partition.

## Leakage controls

- MAC address is never used as a model feature.
- Device ID is used only for labels, grouping and split assignment.
- The original source row index is provenance, not a model feature.
- No test observation is used to fit preprocessing statistics.
- If future normalization is introduced, its parameters must be fitted on training data only and frozen for validation/test.
- Profile updates in later D8/D9 experiments must never modify the frozen test set.

## Scientific limitation

This is a deterministic **engineering split for the current Track-A demonstration**, not evidence of temporal generalization or session independence. The absence of session/chronology metadata is itself recorded as a dataset limitation.

For stronger scientific validation, Track B must use a dataset that exposes the required temporal/session/receiver/environment structure when the claim under test requires it.

## Next stage

Proceed to the D2 implementation/acceptance checks, then build the minimum D3 RF-evidence path without claiming that SMoRFFI alone can validate temporal or receiver-shift robustness.
