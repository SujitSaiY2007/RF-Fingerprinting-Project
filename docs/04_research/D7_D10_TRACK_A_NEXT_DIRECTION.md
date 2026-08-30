# D7–D10 Track-A Direction and Continuation Specification

**Date:** 2026-08-30  
**Track:** A — accelerated implementation / demonstration  
**Purpose:** canonical continuation document for the remaining Track-A lifecycle.

## 1. Canonical position

D1–D2 are not to be redone. The D2 learning gate is passed. The frozen D2 Track-A representation is:

`serialized preamble -> complex[288] -> float32[2,288] I/Q`

The deterministic engineering split is SHA-256 over `(device_id, source_row_index)` with 70/15/15 train/validation/test. This is not a temporal/session split because SMoRFFI does not expose trustworthy temporal/session metadata.

Track A uses SMoRFFI as the current executable substrate. Track B exists for broader scientific validation and must not be conflated with Track A demonstration.

## 2. Completed evidence that must remain frozen

### D4 learned representation
A minimal CNN learned embedding was implemented and tested using the frozen 2x288 input. The reproducible 33-device Track-A snapshot is devices 1–33, 33,000 observations, with 23,030/4,974/4,996 train/validation/test observations. The frozen D4 classifier result is **35.81% test accuracy**. The historical exploratory ~91.1% result is not reproduced and remains historical because the exact prior 10,186-row selection and historical model/configuration are unavailable.

### D5 learned-embedding identity
- D4 classifier: 35.81% accuracy, 31.58% macro-F1, 35.80% balanced accuracy.
- nearest centroid: 36.21%, 33.23%, 36.30%.
- 1-NN: **63.77%**, **63.63%**, **63.80%**.

### D5 classical RF baseline
The current repository D3 extractor contains **16** deterministic RF evidence features. Fixed Random Forest configuration: 100 trees, `random_state=20260830`, `max_features=sqrt`, no tuning. Frozen-test result:

- **87.39% accuracy**
- **87.32% macro-F1**
- **87.41% balanced accuracy**

This is strong closed-set Track-A performance and close to, but does not reproduce, the historical ~91.1% result. The historical ~60-feature list, exact 10,186-row selection and historical RF configuration remain unrecovered. Do not invent them.

### D6 learned-embedding open set
Known devices 1–33; unknown devices 34–123. Frozen D4 centroid-distance rejection threshold is the 95th percentile of known validation distances: `T=21.2566452`.

- Known test acceptance: **95.42%**
- Unknown test rejection: **10.99%** on 13,329 observations from 90 unknown devices.

This is a negative/limiting baseline for open-set separation.

### D6 Random Forest open set
Frozen D5 RF maximum-class-probability score. Threshold chosen only from known validation: `T=0.30` at the 5th percentile.

- Known test acceptance: **94.90%**
- Unknown test rejection: **29.49%**

This is better than the learned-embedding centroid gate but remains weak. It must not be tuned on unknown test data.

### D7 Track-A synthetic robustness stress
Because SMoRFFI does not expose trustworthy temporal/session/receiver/environment boundaries, the first D7 experiment uses controlled perturbations of the frozen known-device test observations.

Gain stress:
- baseline: 87.39%
- -6 dB: 38.07%
- -3 dB: 27.30%
- +3 dB: 20.06%
- +6 dB: 15.93%

AWGN stress:
- 20 dB: 82.29%
- 10 dB: 53.34%
- 5 dB: 20.44%
- 0 dB: 6.73%

Interpretation: the current RF-feature baseline is highly acquisition-sensitive. These are controlled engineering stress results, **not** evidence of real temporal, receiver or environment shift.

## 3. Revised dataset strategy for Track A

A new acquisition requirement must be justified by a specific experimental gap. Do not download large archives merely because they are available.

Track A is allowed to proceed using:

1. **Actual SMoRFFI data** for D1–D6 and the core D8–D10 software path.
2. **Controlled synthetic/constructed datasets** for mechanisms that require sequential shifts, contamination or attacks that public datasets do not directly contain.
3. **Published-paper evidence** to define realistic experimental factors and benchmark assumptions.

Constructed experiments must always be labelled as controlled/synthetic/derived. They must never be presented as measurements from the original published dataset.

External datasets are Track-B validation resources when real metadata is needed.

## 4. External dataset priority — no mandatory mass download

The project portfolio remains:
- WiSig — receiver/day variation and scale.
- Oregon State WiFi RFFP — temporal/environment variation.
- Oregon State LoRa RFFP — same-model deployment variation.
- SMoRFFI — same-model discrimination and D3–D6 development.
- ORACLE — controlled benchmark.
- optional WIDEFT / CNRS-Thales / INRIA resources when a concrete gap justifies them.

For immediate Track-A completion, **no additional large public dataset is mandatory**. A compact external dataset can be added only when a Track-B claim requires independent real-world evidence.

## 5. D7 — exact remaining work

### D7 objective
Determine whether the strong D5 RF closed-set result is stable under distribution changes, and distinguish likely transmitter-related evidence from acquisition-dependent evidence.

### D7-A already completed
Controlled gain and AWGN stress on the frozen SMoRFFI test set. Preserve all results and do not retune the RF model against these tests.

### D7-B — paper-grounded constructed shift suite
Construct a small reproducible benchmark with condition axes motivated by published RF fingerprinting experiments:
- day/age index
- receiver index
- amplitude/gain
- additive noise/interference
- channel distortion
- optional timing/CFO perturbation only where implementation is physically and mathematically defined

The constructed benchmark must vary one factor at a time and then selected combinations. Every scenario needs a machine-readable seed, parameter range and transformation formula.

Run the **frozen D5 RF baseline** and **frozen D4 embedding baseline**. Report baseline score, shifted score, absolute degradation and relative degradation. Do not optimize either model against the shifted test set.

### D7-C — real external evidence, optional Track B
If a compact public dataset can be accessed without the 512 MB upload constraint, use it only to answer a concrete real-world axis such as cross-day or cross-receiver generalization. The first candidates are SmartHomePrivacy RadioFingerprinting for cross-day behavior and compact WiSig/ManySig for receiver/day behavior. Results must be reported under Track B.

## 6. D8 — profile evolution

### Question
Can a device profile adapt to legitimate changes without allowing every recognized observation to rewrite persistent identity state?

### Required implementation
Create a profile manager that stores, at minimum:
- device identity
- representative feature/embedding statistics
- accepted observation count
- last accepted observation index
- profile version
- running dispersion/consistency statistics
- audit record of accepted/rejected/quarantined updates

### Three-way decision
`OBSERVATION -> RECOGNITION -> UPDATE AUTHORIZATION`

Authorization outcomes:
- **ACCEPT / UPDATE** — sufficiently confident and consistent.
- **HOLD / QUARANTINE** — identity may be known but evidence is insufficient or conflicting.
- **REJECT** — unknown or strongly anomalous.

### Sequential protocol
Construct chronological streams from the available real SMoRFFI observations and controlled shifts:
- initial enrollment segment
- legitimate same-device later segment
- controlled shifted-but-legitimate segment
- unknown-device segment

The evaluation set must be frozen before profile updates. No future evaluation observations may be incorporated into the profile before they are evaluated.

### Baseline ladder
At minimum compare:
1. no update / frozen profile
2. always-update after recognition
3. confidence-only admission
4. proposed multi-evidence authorization policy

The exact proposed policy is not fixed in advance. It must be selected by comparison and ablation, not by assuming the novelty hypothesis is true.

## 7. D9 — poisoning / security experiment

### Question
Can controlled malicious or inconsistent observations corrupt profile evolution, and can the authorization layer prevent or limit that corruption?

### Threat construction
Use legitimate SMoRFFI observations as the base and inject clearly labelled controlled/synthetic attack observations. Examples:
- label contamination
- unknown-device contamination into a known profile
- gradual feature/embedding drift
- replay/repetition of suspicious observations

### Required comparison
At minimum:
- always-update baseline
- confidence-only admission baseline
- proposed multi-evidence authorization

### Metrics
- attack acceptance rate
- profile displacement/drift
- legitimate-sample acceptance after attack
- identity accuracy after attack
- unknown acceptance/false acceptance
- recovery/rollback success
- amount of legitimate adaptation preserved

D9 must preserve the frozen evaluation partition and must clearly separate attack-generation data from evaluation data.

## 8. D10 — end-to-end integration

The Track-A demonstrator should execute one coherent lifecycle:

`SMoRFFI/raw observation -> D2 representation -> D3 RF evidence + D4 embedding -> D5 identity -> D6 unknown decision -> D8 profile lookup -> update authorization -> D9 attack/defense path -> audit/final decision`

A successful D10 demonstration must show at least:
- known legitimate observation identified and accepted;
- unknown observation rejected or quarantined;
- legitimate profile evolution accepted when evidence remains consistent;
- suspicious/poisoned observation blocked or quarantined;
- persistent profile remains auditable;
- frozen evaluation is protected from profile updates.

D10 is not merely “all files run”. It must demonstrate the integrated lifecycle.

## 9. Scientific status rules

Every result must carry one of these levels:

1. **Implemented** — code/artifact exists.
2. **Tested** — engineering checks pass.
3. **Demonstrated** — real or explicitly controlled data run completed.
4. **Scientifically Validated** — stage-specific evidence supports the claim.

The current D4–D7 Track-A results are **Demonstrated**, not Scientifically Validated.

## 10. Non-negotiable provenance/leakage rules

- Never use MAC/device identifiers as model features.
- Never infer temporal/session/receiver/environment metadata that the source does not expose.
- Never fit test-set statistics or thresholds.
- Never update persistent profiles with frozen test observations before evaluation.
- Never call controlled synthetic data a real-world measurement.
- Never silently delete, simplify or overwrite prior project evidence.
- Never reconstruct the historical ~91.1% result by inventing the missing ~60-feature list or 10,186-row selection.
- Preserve the historical value as historical/exploratory until exact provenance is recovered.
- Keep Track A and Track B claims visibly separate.

## 11. Relevance of the paper-grounded approach

Published datasets and papers can be used to define realistic shift factors and motivate benchmark ranges, but their reported numbers remain **external literature evidence**, not our measurements. A paper-grounded constructed dataset is a reproducible engineering benchmark, not a substitute for scientific validation on the source dataset.

This distinction allows Track A to complete the software lifecycle without forcing multi-gigabyte downloads while keeping Track B available for later independent validation.

## 12. Exact next-chat sequence

**Start from this document and `PROJECT_STATE.md` / `CURRENT_HANDOFF.md`. Do not restart D1/D2.**

### Action 1 — finalize repository state
Verify D4–D7 artifacts, tests, configs, manifests and metrics. Confirm main/develop content equivalence after the synchronization in this milestone.

### Action 2 — D7 constructed shift suite
Implement/complete the paper-grounded controlled shift benchmark. Produce configuration + seed + transformation manifest + metrics + interpretation. Keep D5 RF and D4 embedding baselines frozen.

### Action 3 — D8 profile manager
Implement chronological profile evolution on SMoRFFI/derived streams with the four baseline policies. Freeze evaluation data before update streams begin.

### Action 4 — D9 security experiment
Inject controlled/synthetic poisoning into the D8 update stream. Compare always-update, confidence-only and multi-evidence authorization. Measure both security damage and legitimate adaptation preservation.

### Action 5 — D10 integrated demonstrator
Wire D2→D3→D4/D5→D6→D8→D9 into one auditable end-to-end run and produce a compact scenario report.

### Action 6 — Track-B gap audit
After D10, list the claims still unsupported without real external condition metadata. Only then decide whether SmartHomePrivacy, ManySig, Oregon State, WiSig, ORACLE or another qualified dataset is worth acquiring.

## 13. Branch discipline

Develop significant work on `develop`. When a milestone is explicitly agreed, synchronize `main` and `develop` by content without loss of historical information. Never force-push protected `main` and never recreate independent histories.

## 14. Canonical interpretation of the RF hypothesis

The current evidence supports retaining Random Forest as a strong **closed-set engineering baseline**, not as proof of transmitter-intrinsic robustness. The large drop under gain/noise stress means acquisition dependence must be treated as a first-class issue in D7/D8.

The candidate research contribution remains provisional:

> A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile poisoning while preserving legitimate adaptation.

D8/D9 are the decisive support/falsification stages for that hypothesis.
