# D8 — Persistent Profile Evolution, Update Authorization & Frozen Evaluation

**Status:** Version-B implementation specification — D8 is one complete stage; do not split into D8.x milestones.
**Branch:** `develop`
**Date:** 2026-08-30

## Objective

D8 converts the frozen Version-A recognizer into a persistent, auditable adaptive identity system while keeping recognition and permission to change identity state as separate decisions.

D8 must answer one question:

> Can legitimate RF observations improve a persistent device profile without allowing uncertain observations to silently rewrite identity state?

D8 is a complete controlled experiment. D9 will attack the resulting update boundary with poisoning.

## Frozen inputs and controls

- D2 input remains `serialized preamble -> complex[288] -> float32[2,288] I/Q`.
- Track-A real substrate remains SMoRFFI.
- Version-A RF recognizer remains the immutable control: 16 deterministic RF features + Random Forest, 100 trees, seed `20260830`, `sqrt`, no tuning.
- Version-A closed-set reference: 87.39% accuracy, 87.32% macro-F1, 87.41% balanced accuracy.
- Version-A open-set reference: 94.90% known acceptance and 29.49% unknown rejection at validation-selected RF confidence threshold 0.30.
- Evaluation data are frozen before chronological profile updates.
- A sample cannot update a profile before that same sample is evaluated.
- Source observations, derived/controlled observations and literature-inspired scenarios remain separately labelled.

## Persistent profile

Each enrolled device profile must contain at minimum:

- `device_id`
- `profile_version`
- `observation_count`
- robust identity representation/statistics
- RF-feature profile statistics
- central tendency and dispersion/consistency statistics
- last accepted update timestamp/index
- update policy identifier
- parent profile/checkpoint identifier
- audit references

The profile is versioned. Updates create a new profile version rather than mutating history invisibly.

## Recognition versus update authorization

D8 explicitly separates:

`OBSERVATION -> RECOGNITION -> NOVELTY/CONSISTENCY EVIDENCE -> UPDATE AUTHORIZATION -> PROFILE UPDATE`

Recognition answers **which enrolled device is the best explanation?**

Update authorization answers **is this observation sufficiently trustworthy to modify that device's persistent identity state?**

A high classifier confidence is evidence, not authorization by itself.

## Decision states

Every observation receives exactly one primary lifecycle decision:

- **ACCEPT / UPDATE** — recognized and authorized for profile evolution.
- **HOLD / QUARANTINE** — recognition may be plausible but evidence is insufficient or conflicting; do not modify the persistent profile.
- **REJECT** — novelty/security evidence indicates that the observation should not be accepted as the enrolled identity.

The audit record must store the evidence and policy that produced the decision.

## Chronological evaluation protocol

Construct one or more deterministic chronological streams from the real SMoRFFI observations and explicitly labelled controlled/derived shifts.

For each stream:

1. establish an initial enrollment profile using only the designated enrollment subset;
2. freeze the evaluation partition;
3. process observations in chronological/index order;
4. evaluate the observation using the profile state available immediately before it;
5. record recognition and security evidence;
6. apply the selected update policy;
7. if authorized, create the next immutable profile version;
8. continue until the stream ends;
9. evaluate the frozen partition against the resulting profile only after the stream, without allowing evaluation observations to update it.

No random reshuffling is permitted inside the chronological stream.

## Required baseline ladder

D8 must evaluate the same chronological stream under four policies:

### Policy A — Frozen / No Update
Profile never changes after enrollment.

### Policy B — Always Update
Every recognized observation updates the profile. This intentionally unsafe baseline establishes the cost of unrestricted adaptation.

### Policy C — Confidence Only
Update when recognition confidence exceeds a validation-selected threshold.

### Policy D — Multi-Evidence Authorization
Update only when multiple independent evidence conditions agree. The initial implementation should combine:

- recognition confidence;
- distance/similarity to the enrolled profile;
- profile consistency/dispersion;
- sequential/repeated observation consistency;
- novelty/open-set evidence.

The exact thresholds are selected from validation data only and frozen before final evaluation.

## Update mechanics

Updates must be bounded and reversible.

Required safeguards:

- bounded update contribution per observation;
- minimum evidence count where applicable;
- robust/trimmed aggregation rather than unrestricted replacement;
- profile versioning;
- checkpoint before update;
- rollback capability;
- audit record for every accepted, held and rejected observation;
- no direct access by the UI to mutate profile state.

D8 should measure both adaptation utility and profile movement.

## Metrics

For each policy report:

### Recognition
- accuracy
- macro-F1
- balanced accuracy
- per-device performance

### Adaptation
- performance before evolution
- performance after evolution
- profile displacement/drift
- profile dispersion change
- legitimate observation acceptance
- HOLD rate
- REJECT rate
- update count
- number of profile versions

### Robustness
- performance under gain/AWGN controlled shifts
- performance by stream position
- degradation/recovery curves

### Security readiness
- unauthorized update rate
- updates caused by unknown/suspicious observations
- rollback success
- frozen-evaluation integrity

## Required D8 conclusion

D8 must not claim that multi-evidence authorization is secure until the policies have been compared. The result may falsify the hypothesis.

The strongest acceptable D8 conclusion is comparative:

> Under the frozen chronological protocol, the proposed update policy either improves legitimate adaptation while reducing unsafe profile modification relative to the baseline ladder, or the evidence shows that it does not.

D9 then tests the boundary adversarially with controlled poisoning.

## UI integration requirements

D8 is developed in parallel with the application layer.

The UI must consume read-only API representations of:

- current profile;
- profile version history;
- recognition evidence;
- novelty/consistency evidence;
- ACCEPT/HOLD/REJECT decision;
- update authorization;
- audit events;
- frozen experiment results.

The UI must never directly implement the D8 decision algorithm.

Required D8 UI surfaces:

1. **Profiles** — enrolled devices and version history.
2. **Identification** — observation result and decision evidence.
3. **Profile Evolution** — chronological profile changes.
4. **Security** — update authorization and suspicious events.
5. **Evaluation** — policy comparison.
6. **Audit** — immutable event history.

## Evidence discipline

- Implemented: profile manager, policy interfaces, versioning and audit structures exist.
- Tested: deterministic unit/integration tests pass.
- Demonstrated: complete chronological streams execute on real/controlled Track-A data.
- Scientifically Validated: requires evidence appropriate to the claim and remains a later standard.

D8 Track-A completion requires the complete lifecycle and all four policy baselines to execute with frozen evaluation. It is not complete merely because the profile class exists.
