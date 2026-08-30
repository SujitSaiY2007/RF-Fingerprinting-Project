# D4 — Learned Representation Baseline

**Date:** 2026-08-30
**Status:** Exploratory result recorded; reproducibility closure required before D5 acceptance.

## Objective
Move from deterministic interpretable D3 RF-evidence features to a compact learned representation derived directly from the canonical Track-A I/Q input.

## Input contract
`serialized preamble -> complex[288] -> real[2,288] (I,Q)`.
MAC address and device number are labels/provenance only and are not model inputs.

## Exploratory result
A fast-track neural experiment was reported using the canonical `2 x 288` I/Q representation and a compact learned representation. The reported closed-set test accuracy was approximately **91.1%** on the runtime subset available for that experiment.

This result is **exploratory**, not a formal benchmark. The exact dataset manifest, model implementation, configuration and run artifact are not yet committed and reproducibly tested in the repository.

## Interpretation
The result is close to the earlier D3 Random Forest result (~90.9%), so current evidence does not justify claiming that the learned representation is materially superior. The useful D4 question is whether the embedding supports later identity, open-set and shift experiments better than the handcrafted feature representation.

## Acceptance boundary
D4 becomes engineering-accepted only after:
1. a minimal reproducible learned-embedding implementation is committed;
2. exact input shape and model configuration are recorded;
3. deterministic train/validation/test handling is verified;
4. training does not use identity leakage;
5. the result can be regenerated from a recorded dataset manifest;
6. embedding-level evaluation is separated from classifier accuracy.

## Fast-track decision
Do **not** hyperparameter-tune merely to increase closed-set accuracy. First freeze one reproducible baseline and proceed to D5 identity evaluation. Stronger models and ablations belong in Track B unless required by a Track-A failure.

## Scientific guardrails
- This is a closed-set engineering result, not open-set recognition.
- It does not establish temporal, receiver, channel or environment robustness.
- It does not establish transmitter-intrinsic causation for the learned representation.
- Exploratory runtime numbers must not be quoted as validated results until reproducibility evidence exists.
