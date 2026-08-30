# D6 — Open-Set Unknown-Device Rejection

**Date:** 2026-08-30  
**Track:** A  
**Status:** **IMPLEMENTED / TESTED / DEMONSTRATED; not scientifically validated.**

## Objective
Extend the frozen D5 identity pipeline so that a sample can be rejected when it is sufficiently far from the known-device embedding gallery.

## Known/unknown boundary
- Known devices: **1–33**.
- Unknown devices: **34–123** from the supplied archive.
- Unknown devices are never used to train the D4 encoder or construct known-device centroids.
- The D6 threshold is selected using **known-device validation embeddings only**.
- The final unknown evaluation uses the deterministic test partition of devices 34–123.

The supplied archive contains 90 unknown devices and 13,329 unknown-device test observations.

## Rejection rule
For each known device, compute its centroid from D4 training embeddings. For an evaluation embedding, use the squared Euclidean distance to the nearest known centroid.

Threshold:

`T = 95th percentile of known-device validation nearest-centroid distance`

Recorded threshold: **21.2566452**.

Accept as a known device when distance <= T; otherwise reject as **UNKNOWN**.

The threshold is fixed before unknown-device test evaluation. No unknown test sample is used to choose T.

## Results
- Known-device frozen test acceptance: **95.42%** (4,767 / 4,996).
- Unknown-device test rejection: **10.99%** (approximately 1,465 / 13,329).
- Unknown devices evaluated: **90**.

Per-device unknown rejection rates are stored in `experiments/track_a/d6_metrics.json`.

## Interpretation
The result shows that the present minimal embedding plus a simple centroid-distance gate has **weak open-set separation** on this Track-A snapshot. Most unknown devices fall inside the known-device embedding region under this threshold.

This is an important negative/limiting result, not a reason to tune the threshold against the unknown test set. A stronger open-set method may be investigated later, but doing so to improve this number would be a new experiment and should remain explicitly documented.

The 95% validation acceptance target is a threshold-selection convention, not a claim of scientific optimality.

## Status discipline
- Implemented: **PASS**
- Tested: **PASS**
- Demonstrated on real known/unknown data: **PASS**
- Scientifically validated: **NO**

## Scientific boundary
The known/unknown distinction is device-number based within one SMoRFFI corpus. It is therefore not equivalent to deployment-grade novelty detection across receivers, environments, collection sessions or datasets. Track-B work is required before making such claims.
