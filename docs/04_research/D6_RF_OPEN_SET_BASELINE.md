# D6 — Random Forest Open-Set Baseline

**Date:** 2026-08-30  
**Track:** A  
**Status:** **IMPLEMENTED / TESTED / DEMONSTRATED; not scientifically validated.**

## Objective
Test whether the strong D5 Random Forest closed-set baseline also provides useful rejection of previously unseen device identities.

## Protocol
- Known devices: 1–33.
- Unknown devices: 34–123.
- Known training/validation/test split remains the frozen D2 SHA-256 70/15/15 split.
- Unknown evaluation uses the deterministic test partition only: 13,329 observations from 90 devices.
- D5 Random Forest remains frozen: 100 trees, `random_state=20260830`, `max_features=sqrt`.

## Rejection rule
Use the Random Forest's maximum predicted class probability as the confidence score.

Threshold is selected from known-device validation observations only:

`T = 5th percentile(max class probability)`

Recorded `T = 0.30`.

A sample is accepted as one of the 33 known identities when max probability >= 0.30; otherwise it is rejected as UNKNOWN.

No unknown test observation is used for threshold selection.

## Results
| Metric | Result |
|---|---:|
| Known-test acceptance | **94.90%** |
| Unknown-test rejection | **29.49%** |
| Unknown test observations | 13,329 |
| Unknown devices | 90 |
| Known-test RF accuracy | **87.39%** |
| Known-test RF macro-F1 | **87.32%** |
| Known-test RF balanced accuracy | **87.41%** |

## Interpretation
The RF confidence gate is substantially better at rejecting unseen devices than the frozen D4 embedding centroid gate (10.99%), but it still accepts about 70.5% of unknown observations at the selected ~95%-known-acceptance operating point.

Therefore the D5 closed-set result does **not** automatically imply strong open-set recognition. The RF model is strong for the current closed-set protocol but has limited novelty rejection under this simple confidence rule.

## Scientific boundary
Known/unknown identity separation is based on device numbers within one SMoRFFI corpus. This does not establish robustness to new environments, receivers, sessions or datasets. Track-B validation remains necessary.

## Status discipline
- Implemented: **PASS**
- Tested: **PASS**
- Demonstrated: **PASS**
- Scientifically Validated: **NO**
