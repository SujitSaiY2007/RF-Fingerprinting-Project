# D4 — Learned Representation Baseline

**Date:** 2026-08-30  
**Track:** A — accelerated implementation  
**Status:** **IMPLEMENTED / TESTED / DEMONSTRATED; historical ~91.1% result NOT REPRODUCIBLE; new frozen baseline recorded.**

## Objective
Move from D3 interpretable RF-evidence features to a compact learned representation derived directly from the frozen D2 I/Q input.

## Frozen D2 input
`serialized preamble -> complex[288] -> float32[2,288] (I,Q)`

No per-observation normalization, clipping, resampling or filtering is applied. Device number and MAC address are labels/provenance only and never model inputs.

## Minimal Track-A model
`Conv1d(2,16,k=7) -> ReLU -> MaxPool(2) -> Conv1d(16,32,k=5) -> ReLU -> AdaptiveAvgPool(1) -> Linear(32,32) embedding -> Linear(32,C) classifier`

Frozen configuration:
- seed: `20260830`
- embedding dimension: `32`
- epochs: `12`
- batch size: `128`
- learning rate: `1e-3`
- weight decay: `1e-4`
- split: D2 SHA-256 `(device_id, source_row_index)` 70/15/15
- accuracy tuning: disabled

## Dataset provenance closure
The complete user-supplied archive was inspected on 2026-08-30:
- 123 CSV files
- 122,511 rows
- 123 devices
- archive SHA-256: `1d9ebcf2539e5fb7fb1dc678dba3fd2a50cada2befb86f5d84faff2b4f541037`

The Track-A D4 reproducible snapshot is devices **1–33**:
- 33 files
- 33,000 observations
- deterministic split: 23,030 train / 4,974 validation / 4,996 test

The complete archive contains known row-count anomalies at devices 67 (999), 87 (999), and 109 (513). They are retained as source data and are not silently corrected.

## Historical ~91.1% reconciliation
The prior exploratory D4 result was approximately **91.12% test accuracy**, with the prior runtime recorded as **10,186 usable observations across 33 devices**. Earlier project state did not contain the exact 10,186-row selection, per-file hashes, trained model, or complete historical run configuration.

The newly supplied archive establishes the complete available source corpus, but it does **not** reveal which 10,186 observations were used in that historical experiment. Consequently:

> **The ~91.1% result is not retrospectively reproducible/certifiable.**

This is a provenance correction, not an accuracy-tuning exercise. The old number must remain labelled historical/exploratory and must not be quoted as the D4 benchmark.

## Frozen reproducible result
Running the repository's fixed minimal model on the explicit 33-device snapshot produced:

- test accuracy: **35.8086%**
- macro-F1: **31.5819%** for the classifier output
- balanced accuracy: **35.7971%**

The result is materially below the historical 91.1%. That difference is not interpreted as evidence that the historical result was false: the historical data selection/model configuration are not recoverable from the evidence currently available. It establishes that the current minimal baseline does not reproduce 91.1%.

## Reproducibility implementation
- `src/smorffi_d4.py` — fixed encoder and deterministic controls.
- `scripts/run_smorffi_d4.py` — BOM-safe loader, explicit device selection, D2 split reuse, frozen training configuration.
- `scripts/make_smorffi_manifest.py` — file hashes, sizes, row/device counts; handles the BOM present in the supplied CSV headers.
- `experiments/track_a/d4_manifest.json` — source archive and exact Track-A snapshot provenance.

## D4 acceptance assessment
| Requirement | Status |
|---|---|
| Frozen D2 input | **PASS** |
| Minimal learned embedding | **PASS** |
| Deterministic training/split | **PASS** |
| Identity/MAC leakage exclusion | **PASS** |
| Exact supplied snapshot documented | **PASS** |
| Historical 10,186-row run reproduced | **NO — historical selection/configuration unavailable** |
| ~91.1% certified as D4 benchmark | **NO** |
| New reproducible Track-A baseline | **PASS — 35.81% test accuracy** |

## Boundary and scientific status
This closes **engineering reproducibility for the current frozen Track-A baseline**, but does not scientifically validate transmitter-intrinsic fingerprinting. The D2 split is deterministic rather than temporal/session-held-out. Cross-condition, receiver, environment and cross-dataset claims remain Track B.

D5 may now use the frozen embedding without changing the D4 model/configuration. D6 must evaluate unknown devices without fitting on unknown-device data.

No hyperparameter tuning was performed to improve the reported score.
