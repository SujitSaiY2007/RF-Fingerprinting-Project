# D4 — Learned Representation Baseline

**Date:** 2026-08-30
**Status:** **IMPLEMENTED / TESTED (unit-level); reproducibility closure BLOCKED by missing exact dataset snapshot.**

## Objective
Move from deterministic interpretable D3 RF-evidence features to a compact learned representation derived directly from the canonical Track-A I/Q input.

## Frozen input contract
The D4 input remains the D2 Track-A baseline:

`serialized preamble -> complex[288] -> real[2,288] (I,Q)`

MAC address and device number are labels/provenance only and are not model inputs. No normalization is introduced.

## Fixed minimal model
The committed Track-A baseline is a lightweight 1-D CNN:

`Conv1d(2,16,k=7) -> ReLU -> MaxPool(2) -> Conv1d(16,32,k=5) -> ReLU -> AdaptiveAvgPool(1) -> Linear(32,32) embedding -> Linear(32,C) classifier`

Configuration is frozen in `configs/track_a_d4_baseline.json`:
- seed: `20260830`;
- embedding dimension: `32`;
- epochs: `12`;
- batch size: `128`;
- learning rate: `1e-3`;
- weight decay: `1e-4`;
- split: existing D2 SHA-256 `(device_id, source_row_index)` 70/15/15 policy;
- accuracy tuning: explicitly disabled.

Implementation: `src/smorffi_d4.py` and `scripts/run_smorffi_d4.py`.

## Reproducibility tooling
`scripts/make_smorffi_manifest.py` generates a machine-readable manifest containing file names, byte sizes, SHA-256 hashes, row counts and device counts for an exact local CSV snapshot.

`experiments/track_a/d4_manifest.json` records the current canonical-state limitation: the exact raw CSV snapshot used for the exploratory run is not present in the repository and is not available through the current connected file state. The prior handoff reports **10,186 usable observations across 33 devices**, but that number alone is insufficient to reproduce a run.

## Exploratory result reconciliation
The previously reported **~91.1%** closed-set test accuracy remains an **exploratory historical result**. It cannot be reproduced or independently verified from the current canonical repository state because the exact input snapshot, per-file hashes and prior model artifact are absent.

Therefore the project **does not promote 91.1% to a formal D4 benchmark and does not invent a replacement score**. This is an explicit reproducibility correction, not a failed attempt hidden behind tuning.

## Current acceptance assessment
| Requirement | Status |
|---|---|
| Minimal learned embedding implementation | **PASS — Implemented** |
| Fixed input shape/model/configuration | **PASS — Implemented** |
| Unit tests for input/model contract | **PASS — Implemented** |
| Deterministic seed/training controls | **PASS — Implemented** |
| Identity/MAC leakage exclusion | **PASS — by design** |
| Exact dataset manifest for exploratory run | **BLOCKED — source snapshot unavailable** |
| Reproduction of ~91.1% | **NOT REPRODUCIBLE from canonical state** |
| Formal D4 numerical acceptance | **NOT YET ACCEPTED** |

## Boundary
D4 must not be marked fully engineering-accepted until the exact SMoRFFI snapshot is supplied and the fixed runner produces a recorded result. Once that happens, D5 can use the **frozen embedding** without changing the D4 architecture.

Do **not** hyperparameter-tune merely to increase closed-set accuracy. Stronger models or ablations remain Track B unless a documented Track-A failure requires one.

## Scientific guardrails
- This is not open-set recognition.
- It does not establish temporal, receiver, channel or environment robustness.
- It does not establish transmitter-intrinsic causation for the learned representation.
- Exploratory runtime numbers must not be quoted as validated results without reproducible code/configuration/manifest evidence.
