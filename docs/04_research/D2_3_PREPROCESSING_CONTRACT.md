# D2.3 — Deterministic Preprocessing Contract

**Status:** IMPLEMENTED / TESTED on the 20-file SMoRFFI inspection subset
**Date:** 2026-08-30

## Objective

Define the smallest deterministic preprocessing transformation justified by the observed SMoRFFI schema while preserving RF-relevant information and provenance.

## Baseline transformation

For each source row:

1. Parse the serialized `preamble` string into complex samples.
2. Require at least 288 complex samples.
3. Select the first 288 samples as the source-defined canonical preamble.
4. Split each complex sample into two real channels:
   - channel 0 = I = real part;
   - channel 1 = Q = imaginary part.
5. Cast downstream numeric arrays to a stable floating-point representation such as float32.
6. Do **not** apply per-observation magnitude normalization, phase normalization, global standardization, clipping, filtering, resampling, or arbitrary interpolation in the baseline.
7. Preserve source file, source row index, device ID, MAC, original stored length, canonical length, and discarded-tail count as provenance metadata.

## Why no normalization in the first baseline?

Amplitude may contain transmitter/receiver-dependent information relevant to RF fingerprinting. A normalization operation can remove or alter that information. Therefore normalization is not silently included in the first baseline. It should be evaluated later as an explicit ablation, with any statistics fitted on training data only.

## Shape contract

`complex[288] -> real[2,288]`

Equivalent tensor convention for PyTorch:

`[channels=2, samples=288]`

The project must document the convention consistently; no flattening into identity/metadata fields is allowed.

## Determinism

The same source row must always produce the same canonical I/Q array. No random operation occurs in D2.3.

## Reversibility / provenance

The original serialized preamble is retained outside the derived tensor. The transformation records the original sequence length and the number of excluded trailing samples. Derived data can therefore be traced back to the exact source observation.

## Important limitation

The source paper describes the canonical preamble as 288 samples, while the inspected stored field is variable-length. The baseline therefore uses the first 288 source-defined samples rather than treating the observed trailing values as another signal segment. This is a documented source-informed decision, not an assertion that all trailing values are scientifically meaningless.

## Future ablations

After a working baseline exists, compare explicitly:

- no normalization;
- training-set-fitted global I/Q standardization;
- magnitude/phase representation;
- optional filtering if justified by a stated signal-processing hypothesis.

These are experimental alternatives, not part of the frozen baseline contract.
