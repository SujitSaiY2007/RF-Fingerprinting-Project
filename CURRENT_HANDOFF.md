# CURRENT HANDOFF — 2026-08-30

## Project
**Physics-Based RF Fingerprinting with Continuous Device Learning**

## Canonical repository
`SujitSaiY2007/RF-Fingerprinting-Project`

## Current position
- Phase: **Phase 1 — Preparation / accelerated implementation**.
- Stable branch: `main`.
- Integration branch: `develop`.
- Current engineering gate: **D2 — Minimal deterministic synchronization / preprocessing**.
- D1: **COMPLETE at source/schema/ingestion-foundation level**.
- D2.1: **COMPLETE**.
- D2.2: **OBSERVED / IMPLEMENTED / TESTED on a 20-file SMoRFFI subset**.
- D2.3: **DEFINED / IMPLEMENTED / TESTED**.
- D2.4: **DEFINED / IMPLEMENTED / TESTED as an engineering split**.
- D2.5+: **NEXT — integrated acceptance and minimum D3–D6 vertical demonstration path**.
- D1–D10 scientific validation: **not yet complete**.

## Fast-track objective
Move rapidly from the validated minimum data representation to a demonstrable D1–D10 software lifecycle while keeping the distinction between implementation, testing, demonstration and scientific validation.

Execution principle:

`Build minimum viable evidence path -> test -> document -> strengthen`

Do not claim scientific completion from code existence.

## Active two-track execution model

### Track A — Fast Implementation / Demonstration
Current substrate: **SMoRFFI**.

Immediate path:
`D2 acceptance -> D3 RF evidence -> D4 embedding -> D5 closed-set identity -> D6 open-set -> D7 shift -> D8 profile evolution -> D9 poisoning -> D10 integration`

The objective is to get a real-data end-to-end demonstration quickly.

### Track B — Research Validation / Strengthening
Use qualified datasets such as WiSig and Oregon State WiFi RFFP when a claim requires temporal, receiver, environment or broader robustness evidence. Track B must support or falsify claims rather than manufacture positive evidence.

## SMoRFFI D2.2 observed schema
Twenty uploaded IQ-only CSVs were inspected directly, totaling **19,513 rows**.

Observed file schema:
- `Device Number`
- `MAC_address`
- `preamble`

Observed signal representation:
- `preamble` is a serialized whitespace-separated complex-valued sequence;
- all inspected rows parse successfully;
- stored sequence length is **288–579 complex samples**;
- 5,783 rows are exactly 288 samples;
- 13,730 rows contain additional samples;
- the device-109 file contains 513 rows and stored lengths 448–579, so this anomaly is retained rather than silently repaired.

The published SMoRFFI definition describes the canonical preamble as **288 complex samples** and reports a 20 MS/s acquisition. The Track-A baseline therefore selects the first 288 parsed samples and records original length plus discarded-tail count as provenance. The full rationale is in:
`docs/04_research/D2_2_SMORFFI_SCHEMA_EVIDENCE.md`

## D2.3 preprocessing contract
Baseline:
`serialized preamble -> complex[288] -> real[2,288] (I,Q)`.

No per-observation normalization, clipping, filtering, resampling or arbitrary interpolation is applied. Amplitude normalization remains a future ablation because it may remove RF-discriminative information.

Implementation:
`src/smorffi_d2.py`

Tests:
`tests/test_smorffi_d2.py`

Specification:
`docs/04_research/D2_3_PREPROCESSING_CONTRACT.md`

## D2.4 split policy
Track-A engineering split:
- 70% train;
- 15% validation;
- 15% test;
- deterministic SHA-256 assignment from `(device_id, source_row_index)`.

This is **not** claimed to be a temporal/session holdout because SMoRFFI does not expose those boundaries. Device identity and MAC remain labels/provenance only.

Specification:
`docs/04_research/D2_4_LEAKAGE_SAFE_SPLIT.md`

## Next execution sequence
1. Run integrated D2 acceptance checks on the local SMoRFFI subset.
2. Build D3 RF-physical evidence features/visualization from the canonical I/Q signal.
3. Build D4 compact learned embedding baseline.
4. Build D5 closed-set identity classifier.
5. Build D6 unseen-device/open-set baseline.
6. Use these validated upstream blocks to construct D7–D10 progressively.

Do not block Track A on acquisition of additional large datasets.

## Scientific guardrails retained
- Do not use MAC/device identifiers as model inputs.
- Keep raw/source rows and derived representations traceable.
- Do not fit preprocessing statistics on validation/test data.
- Do not claim temporal/session/receiver/environment robustness from SMoRFFI alone.
- Keep Track A and Track B evidence separate.
- D9 poisoning data must be controlled/synthetic or otherwise explicitly labelled.
- D8/D9 novelty comparisons must include the required baseline ladder.
- D10 must demonstrate the complete lifecycle.

## Novelty boundary
The current candidate contribution remains provisional:

> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile-poisoning while preserving legitimate adaptation.**

Do not present this as proven novelty until D8/D9 evidence supports or falsifies it.

## Branch synchronization rule
The D2.2–D2.4 milestone has been committed to **`develop` only** during this chat. `main` has not been changed. At the end of a significant agreed milestone, synchronize `main` and `develop` to the same agreed project state; do not silently delete or revert prior documents.
