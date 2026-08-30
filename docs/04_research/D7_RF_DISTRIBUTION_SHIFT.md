# D7 — RF Closed-Set Robustness / Distribution-Shift Stress Test

**Date:** 2026-08-30  
**Track:** A  
**Status:** **IMPLEMENTED / TESTED / DEMONSTRATED; not scientifically validated.**

## Why D7 was run
D5 established that the current 16-feature D3 representation plus a fixed Random Forest reaches 87.39% closed-set accuracy. D6 showed that simple RF confidence rejection rejects only 29.49% of unseen-device test observations at ~94.90% known acceptance. D7 asks whether the strong closed-set result is stable under controlled distribution shift.

## Data boundary
The inspected SMoRFFI CSV schema exposes only `Device Number`, `MAC_address`, and `preamble`. It does **not** expose trustworthy temporal/session/receiver/environment labels. Therefore D7 does not claim a real temporal, receiver or environmental split.

Instead, Track A uses controlled synthetic stress applied to the already frozen known-device test I/Q. No model retraining or test-set tuning is performed.

## Baseline
Frozen D5 Random Forest:
- 100 trees
- `random_state=20260830`
- `max_features=sqrt`
- 16 deterministic D3 features
- baseline frozen-test accuracy: **87.39%**
- macro-F1: **87.32%**
- balanced accuracy: **87.41%**

## Shift 1 — amplitude/gain perturbation
A multiplicative gain is applied to every complex test sample:

`x_shift = x * 10^(dB/20)`

Results:

| Shift | Accuracy | Macro-F1 | Balanced accuracy |
|---|---:|---:|---:|
| Baseline | 87.39% | 87.32% | 87.41% |
| -6 dB | 38.07% | 39.56% | 38.12% |
| -3 dB | 27.30% | 25.93% | 27.24% |
| +3 dB | 20.06% | 19.28% | 20.31% |
| +6 dB | 15.93% | 14.96% | 16.23% |

The result is a severe limitation: several current RF features encode absolute amplitude information, so the classifier is not gain-invariant.

## Shift 2 — additive white Gaussian noise
Noise is added at fixed per-observation SNR using deterministic seed `20260830`. The model is not retrained.

| SNR | Accuracy | Macro-F1 | Balanced accuracy |
|---|---:|---:|---:|
| 20 dB | 82.29% | 82.07% | 82.21% |
| 10 dB | 53.34% | 52.42% | 53.16% |
| 5 dB | 20.44% | 18.55% | 20.18% |
| 0 dB | 6.73% | 3.76% | 6.64% |

## Interpretation
The answer to the D7 question is **no, the 87.39% closed-set result is not robust to the tested synthetic shifts**. It is strong under the original Track-A protocol but degrades sharply under gain changes and progressively under noise.

This does not mean the RF features are useless. It means the present baseline has substantial sensitivity to acquisition conditions. That is exactly the type of limitation D7 is intended to expose.

## Scientific boundary
These perturbations are controlled engineering stress tests. They are not substitutes for genuine cross-session, cross-receiver or cross-environment validation. Track B must use datasets exposing those axes (for example WiSig or Oregon State RFFP) before claims about real-world domain robustness can be made.

## Status discipline
- Implemented: **PASS**
- Tested: **PASS**
- Demonstrated: **PASS**
- Scientifically Validated: **NO**

## Decision boundary
Do not tune the D5 RF model on these test perturbations. Any gain-invariant feature redesign or augmentation is a new experiment and must preserve the original frozen baseline for comparison.
