# D5 — Random Forest Classical RF-Feature Baseline

**Date:** 2026-08-30  
**Track:** A  
**Status:** **IMPLEMENTED / TESTED / DEMONSTRATED; not scientifically validated.**

## Why this experiment was added
The project history records an exploratory closed-set result of approximately **91.1%** on the same general SMoRFFI development data, associated with a Random Forest and an approximately 60-feature engineered RF feature list. The exact historical feature list, exact 10,186-row selection and historical configuration are not recoverable.

A clean classical baseline was therefore run rather than assuming the historical result was reproducible.

## Current repository feature set
The current D3 implementation exposes **16 deterministic, label-free features** from the frozen D2 `2 x 288` I/Q input. This is **not** claimed to be the historical ~60-feature list.

Features:
`i_mean, i_std, q_mean, q_std, amplitude_mean, amplitude_std, rms_amplitude, crest_factor, mean_power, iq_variance_ratio_db, iq_correlation, mean_phase_step_rad, std_phase_step_rad, spectral_centroid_hz, spectral_spread_hz, spectral_entropy_bits`.

## Protocol
- Track-A dataset: SMoRFFI.
- Known devices: 1–33.
- Total observations: 33,000.
- Split: existing deterministic SHA-256 `(device_id|source_row_index)` 70/15/15 contract.
- Train: 23,030.
- Validation: 4,974.
- Frozen test: 4,996.
- Input source: canonical D2 `2 x 288` I/Q.
- Model: `RandomForestClassifier`.
- Trees: 100.
- `random_state = 20260830`.
- `max_features = sqrt`.
- No hyperparameter search or test-set tuning.

## Result
| Metric | Random Forest |
|---|---:|
| Accuracy | **87.39%** |
| Macro-F1 | **87.32%** |
| Balanced accuracy | **87.41%** |

This materially outperforms the frozen D4 classifier (35.81%), D4 nearest-centroid (36.21%), and D4 1-NN (63.77%) under the same known-device test protocol.

## Relation to historical ~91.1%
The current result is **close to, but does not reproduce,** the historical ~91.1% result. The numerical gap is about **3.72 percentage points**, but this is not a controlled performance comparison because the historical feature list, exact 10,186-row selection and historical RF configuration are unavailable.

The strongest supported conclusion is:

> A fixed Random Forest over the current repository's 16 engineered RF features is a strong closed-set Track-A baseline and substantially outperforms the minimal frozen learned embedding readouts. The historical ~91.1% result remains unreconstructed.

## Feature importance
Largest impurity-based importances in this run:

| Feature | Importance |
|---|---:|
| spectral_centroid_hz | 0.1570 |
| std_phase_step_rad | 0.1104 |
| spectral_spread_hz | 0.1063 |
| mean_phase_step_rad | 0.0730 |
| rms_amplitude | 0.0668 |
| mean_power | 0.0661 |
| amplitude_std | 0.0585 |
| i_std | 0.0563 |
| q_std | 0.0532 |
| crest_factor | 0.0514 |

These importance values are model-dependent and are not causal evidence that the features are transmitter-intrinsic. Spectral/phase descriptors can contain acquisition and channel effects.

## Scientific boundary
This does not establish robust transmitter identification across time, receivers, environments or datasets. The D2 split is retained and is not a temporal/session holdout.

Status:
- Implemented: **PASS**
- Tested: **PASS**
- Demonstrated: **PASS**
- Scientifically Validated: **NO**

## Decision
Retain this Random Forest as a **parallel D5 classical baseline**. Do not overwrite D4 or replace the learned embedding. D7 should use these fixed baselines and test an explicitly observable distribution shift rather than tuning against the existing test set.
