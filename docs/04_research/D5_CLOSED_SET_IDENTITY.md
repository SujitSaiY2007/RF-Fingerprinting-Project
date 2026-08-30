# D5 — Closed-Set Device Identity Using Frozen D4 Embedding

**Date:** 2026-08-30  
**Track:** A  
**Status:** **IMPLEMENTED / TESTED / DEMONSTRATED; not scientifically validated.**

## Objective
Evaluate closed-set device identity using the **frozen D4 learned embedding**. D5 does not retrain or tune the D4 encoder. Device identities 1–33 are the known closed-set classes.

## Evaluation boundary
- Dataset: user-supplied SMoRFFI archive.
- Known Track-A snapshot: devices 1–33, 33,000 observations.
- D2 split: deterministic SHA-256 `(device_id, source_row_index)` 70/15/15.
- Test set: 4,996 observations, frozen before metric calculation.
- Input: `2 x 288` I/Q.
- Embedding: frozen 32-dimensional D4 output.

## Methods
Three identity readouts were evaluated without changing D4:
1. **D4 classifier head** — reference closed-set classifier.
2. **Nearest centroid** — one centroid per device computed from training embeddings only.
3. **1-nearest neighbour** — nearest training embedding; training labels are used only as identity labels.

No test data are used to construct centroids or neighbours.

## Results
| Method | Accuracy | Macro-F1 | Balanced accuracy |
|---|---:|---:|---:|
| D4 classifier | 35.81% | 31.58% | 35.80% |
| Nearest centroid | 36.21% | 33.23% | 36.30% |
| **1-nearest neighbour** | **63.77%** | **63.63%** | **63.80%** |

The nearest-neighbour result is materially stronger than the classifier/centroid readouts. This is useful evidence that the learned embedding contains local identity structure even though the compact classifier head itself generalizes poorly on this deterministic split.

## Per-device metrics and confusion matrix
The complete per-device precision/recall/F1/support values and 33x33 confusion matrices are stored in `experiments/track_a/d5_metrics.json`.

## Interpretation
D5 demonstrates a closed-set identity pipeline on real SMoRFFI data. It does **not** demonstrate robust transmitter-intrinsic identification because the split does not expose temporal/session boundaries and the data are from a single source/collection context.

The 63.77% nearest-neighbour score must not be compared directly with the historical ~91.1% D4 number as if they were the same experiment. The historical D4 dataset selection/configuration is not recoverable. D5 uses the newly frozen reproducible 33-device Track-A snapshot.

## Status discipline
- Implemented: **PASS**
- Tested: **PASS**
- Demonstrated on real data: **PASS**
- Scientifically validated: **NO**

## Next stage
D6 uses the same frozen embedding and known-device training profiles to reject devices not present in the closed-set identity gallery. Unknown-device data must not be used to fit the rejection threshold.
