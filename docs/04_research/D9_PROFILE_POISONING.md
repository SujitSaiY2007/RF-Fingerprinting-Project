# D9 — Controlled / Synthetic Profile-Poisoning Evaluation

**Date:** 2026-08-30  
**Track:** A  
**Status:** **IMPLEMENTED / TESTED / DEMONSTRATED; not scientifically validated.**

## Question
Can controlled malicious or inconsistent observations corrupt persistent profile evolution, and does the authorization layer prevent or limit that corruption?

## Data boundary
The attack streams are **controlled/derived synthetic scenarios**, constructed from real SMoRFFI observations. They are not measurements of attacks in the SMoRFFI source dataset and are not attributed to the source paper/dataset.

Known-device frozen test data remain untouched. Attack generation uses training/unknown observations outside the frozen known test partition.

## Attack families
1. **Unknown-device contamination:** device 34–40 observations selected only when the frozen recognition model maps them to known identity 1 at D6 confidence `>=0.30`.
2. **Replay/repetition:** one suspicious unknown observation is repeated 100 times.
3. **Gradual derived gain drift:** legitimate device-1 observations are transformed with a deterministic 0–3 dB gain ramp before feature extraction.
4. **Label contamination:** a false claimed identity is attached conceptually, but the profile manager receives only recognition output; claimed labels are not an update input.

## Baselines
- always-update;
- confidence-only (`>=0.30`);
- multi-evidence (`>=0.30` confidence + validation-derived profile consistency), with an explicit replay guard.

## Results
| Policy | Unknown contamination acceptance | Replay acceptance | Replay hold | Gain-drift acceptance |
|---|---:|---:|---:|---:|
| always-update | 100.0% | 100.0% | 0.0% | 100.0% |
| confidence-only | 100.0% | 100.0% | 0.0% | 94.68% |
| multi-evidence | 100.0% | **1.0%** | **99.0%** | 94.68% |

Unknown-contamination acceptance caused a target-profile displacement of approximately **0.633 standardized-feature units** versus the clean reference for all three policies in this constructed scenario.

Label contamination did not control the update identity: the false claimed label was not consumed by the profile manager. Recognized identity was the only identity passed to authorization.

## Interpretation
This is an intentionally non-guaranteeing result.

- The replay guard is effective against repeated exact observations after the first occurrence.
- The consistency gate rejects some gain-drift observations but does not eliminate gradual drift admission.
- Most importantly, an unknown observation that is already sufficiently similar to a known profile and receives adequate classifier confidence can pass multi-evidence authorization. **The proposed mechanism therefore does not yet establish strong poisoning resistance.**

This is a meaningful boundary condition for the novelty hypothesis rather than evidence manufactured to guarantee success.

## Required next strengthening
The next security iteration should test stronger multi-observation admission rules, cross-evidence diversity, delayed/batched promotion and recovery/rollback. Any such change must be treated as a new policy and compared against the frozen four-policy ladder rather than silently replacing it.

## Scientific boundary
These are Track-A controlled/derived security experiments. They demonstrate the software mechanism and expose failure modes, but they do not constitute scientific validation against real attacker traffic or real temporal/receiver/environment conditions.
