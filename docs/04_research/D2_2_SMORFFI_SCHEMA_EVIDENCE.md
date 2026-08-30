# D2.2 — SMoRFFI Actual Schema Evidence

**Status:** OBSERVED / DEVELOP-ONLY MILESTONE
**Inspection date:** 2026-08-30
**Inspected local subset:** 20 IQ-only CSV files supplied from `RFFI-IQ_only-wifi-802.11g-2.4G-123-m5stack`

## Purpose

D2.2 establishes the actual signal representation from the downloaded SMoRFFI files before preprocessing. This document separates direct file observations from source-paper claims and unresolved questions.

## Directly observed in the 20 uploaded CSVs

- Files inspected: **20**
- Total source rows inspected: **19,513**
- All files use three columns:
  - `Device Number`
  - `MAC_address`
  - `preamble`
- `preamble` is a serialized whitespace-separated sequence of complex-valued samples.
- Complex samples are represented in Python-compatible form such as `a+bj`; real-only values also occur and are valid complex values with zero imaginary part.
- Every inspected row parsed successfully.
- Every inspected row contains at least **288 complex samples**.
- Observed stored preamble length: **288–579 complex samples**.
- Exactly **5,783** rows contain 288 samples.
- **13,730** rows contain more than 288 samples.
- Maximum observed stored length: **579** samples.
- Therefore the stored `preamble` field is **variable-length**, despite the published 288-sample preamble definition.

## File-level anomaly observed

Nineteen uploaded files contain 1,000 rows. The file for device 109 (`78_21_84_93_5b_0c_pre.csv`) contains **513 rows** and all of its observed preamble lengths are **448–579** samples. This is retained as an explicit source anomaly. No rows are fabricated, duplicated, padded, or silently discarded.

## Source-paper definition

The SMoRFFI paper defines the canonical raw preamble after dropping the first two 16-sample STS repetitions as a **288-sample complex sequence** consisting conceptually of:

- 128 samples of retained STS;
- 32 samples of GI2;
- 128 samples of LTS.

The paper also reports 20 MS/s sampling and 20 MHz bandwidth for acquisition.

## Representation decision for Track A baseline

Because every inspected stored preamble contains at least 288 samples and the published dataset definition identifies the canonical preamble as 288 samples, the Track-A baseline representation is:

`stored preamble string -> complex samples -> first 288 canonical samples -> two real channels (I,Q)`

The complete parsed source sequence and its original length remain provenance information. Samples beyond 288 are **not treated as meaningless**; they are excluded from the baseline input because the source-defined canonical preamble is 288 samples. This choice is explicitly traceable and must be revisited if full-package inspection or source-code evidence establishes a different semantics for the trailing samples.

## What is NOT claimed

- The observed floating-point range is not treated as proof of a universal ADC scaling convention.
- No per-observation normalization is assumed.
- No chronology, session ID, receiver variation, environment variation, or multi-day metadata is inferred from these CSVs.
- The 20-file inspection does not prove that every file in the 123-file release is identical in structure.
- D2.2 does not establish scientific validity of a classifier.

## Baseline signal object

For each source observation:

`X_raw = complex[original_length]`

`X_canonical = X_raw[:288]`

`X_IQ = [(Re(X_canonical[n]), Im(X_canonical[n])) for n=0..287]`

The model-input candidate is therefore a **2 x 288 real-valued representation** when converted to tensor form, with channel 0 = I and channel 1 = Q.

## Next stage

D2.3 defines deterministic preprocessing on this representation. The baseline deliberately avoids amplitude normalization so that a later ablation can test whether normalization removes useful RF-discriminative information.
