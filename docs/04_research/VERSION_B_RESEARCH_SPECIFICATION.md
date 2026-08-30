# Version B Research Specification — Robust Open-Set RF Fingerprinting

**Status:** Research specification / decision framework — UI architecture added; B0–B2 next execution gates
**Branch:** `develop`
**Date:** 2026-08-30
**Relationship to Version A:** Version A remains frozen as the reference baseline. Version B must preserve the same high-level lifecycle while replacing or strengthening individual mechanisms only when evidence justifies the change.

---

## 1. Purpose

Version B addresses the three principal weaknesses identified by Track-A Version A: weak open-set/unknown-device rejection; unverified separation of transmitter fingerprint information from acquisition/channel/receiver effects; and vulnerability of adaptive profile evolution to profile poisoning.

The project is **not** restarting D1/D2. The frozen D2 input contract remains:

`serialized preamble -> complex[288] -> float32[2,288] I/Q`

The Version-B lifecycle remains:

`RF observation -> representation -> recognition -> novelty/security decision -> update authorization -> persistent profile -> audit`

---

## 2. Version A reference — never overwrite

- SMoRFFI real substrate; known devices 1–33.
- Frozen classical RF baseline: 16 deterministic RF evidence features + fixed Random Forest.
- Closed-set test accuracy: **87.39%**; macro-F1 **87.32%**; balanced accuracy **87.41%**.
- RF confidence gate: **94.90% known acceptance**, **29.49% unknown rejection**.
- D7 gain/AWGN stress: strong acquisition sensitivity.
- D8 profile evolution: implemented/tested/demonstrated.
- D9 replay resistance: demonstrated in the controlled scenario.
- D9 poisoning resistance: not established; target-like contamination remained a vulnerability.
- Fingerprint purity: not scientifically established.
- Temporal/session/environment/receiver generalization: Track-B evidence, not Track-A evidence.
- Historical ~91.1% remains historical/unreconstructed.

Version B must always report deltas against this frozen reference.

---

## 3. Research principles

### 3.1 Evidence hierarchy

Claims are tagged **Implemented**, **Tested**, **Demonstrated**, or **Scientifically Validated**. A higher label cannot be inferred from a lower one.

### 3.2 No model-chasing

Model selection follows the evaluation problem. A model is not selected because it gives the largest closed-set accuracy on one split.

### 3.3 No dataset laundering

1. **REAL_SOURCE_DATA** — directly measured/source observations.
2. **DERIVED_CONTROLLED_DATA** — transformations applied to source observations, explicitly synthetic/derived.
3. **PAPER_REPRODUCTION_SCENARIO** — controlled experiments inspired by published methodology/parameter ranges; not exact reproduction unless original dataset, preprocessing, split and configuration are available.

Synthetic data cannot be presented as source-dataset measurements.

### 3.4 Frozen evaluation and leakage control

For each experiment the final evaluation set is frozen before model/threshold selection, profile updates, or attack generation that could influence it. No future evaluation observation may update a profile before evaluation.

### 3.5 Security-first interpretation

Higher closed-set accuracy does not automatically constitute improvement if unknown rejection, robustness, or poisoning resistance becomes worse.

---

# 4. Literature-derived mechanism matrix

## 4.1 Baseline / dataset lesson

### SMoRFFI
The 2026 SMoRFFI paper describes 123 same-model IEEE 802.11g devices and a large raw I/Q corpus. Its same-model design is relevant to difficult device discrimination. The repository's **87.39%** result remains its own frozen configuration and must not be conflated with the paper's reported result.

### Dataset-versus-model lesson
Recent RFFI literature warns against assuming that larger models automatically solve dataset and evaluation limitations. Version B therefore benchmarks compact and learned candidates rather than model-chasing.

## 4.2 Open-set recognition

Relevant literature motivates:
- prototype representation and distance-to-prototype rejection;
- consistency regularization and label smoothing;
- supervised contrastive learning with explicit open-set classifiers;
- multi-task classification/prototype/reconstruction objectives;
- calibrated/support-aware prototype scoring;
- incremental open-set recognition with explicit new/unknown handling.

These mechanisms are candidates for controlled reproduction/testing, not guaranteed improvements.

## 4.3 Representation learning / fingerprint purity

Contrastive learning is a candidate mechanism for compact same-device/separated different-device embeddings. Cross-receiver RFFI literature identifies receiver/domain shift as a major concern and motivates domain-adversarial learning, receiver/domain auxiliary heads, contrastive invariance, feature disentanglement and calibration.

Track A can stress controlled nuisance transformations but cannot scientifically prove receiver invariance without trustworthy receiver metadata. Track B remains necessary for real receiver/environment validation.

## 4.4 Profile evolution and poisoning

Adaptive templates can be manipulated by carefully constructed observations. Version B therefore treats update authorization as a security boundary and investigates confidence, distance, consistency, temporal evidence, replay detection, update budgets, quarantine, evidence accumulation, robust/trimmed updates, bounded profile movement, rollback/checkpointing and post-update validation.

The system must attack these mechanisms rather than assume they work.

---

# 5. Version B candidate model families

- **M0 — Version-A RF baseline:** immutable control.
- **M1 — Compact learned I/Q classifier:** small 1-D CNN/temporal encoder under the frozen 2×288 I/Q contract.
- **M2 — I/Q encoder + metric/prototype head:** recognition using embedding geometry rather than only softmax.
- **M3 — I/Q encoder + supervised contrastive objective + prototype/open-set head:** primary hypothesis unless experiments disprove it.
- **M4 — M3 + reconstruction/consistency auxiliary objective:** controlled extension if justified.
- **M5 — M3/M4 + domain-invariance mechanism:** later robustness/Track-B-oriented extension when metadata support it.

No final Version-B backbone is frozen before B0–B2 evidence.

---

# 6. Version B evaluation ladder

## B0 — Reproducibility

Freeze dataset manifest, D2 input, deterministic configuration, source/derived provenance and leakage controls; reproduce Version-A controls.

## B1 — Closed-set

For M0–M3 under identical splits/configuration report accuracy, macro-F1, balanced accuracy, per-device metrics, confusion matrix and repeated-seed variance.

## B2 — Open-set

Known devices remain 1–33; unknown devices are held out from training/enrollment. Report known acceptance, unknown rejection, unknown false acceptance, AUROC, AUPR where meaningful, FPR at matched operating points, OSCR or equivalent, and open-set macro-F1. Thresholds are validation-only.

## B3 — Controlled acquisition stress

Evaluate gain, AWGN/SNR and physically justified phase/frequency/channel-like perturbations using explicit derived-data provenance. Report degradation curves.

## B4 — Fingerprint-purity diagnostics

Measure same-device embedding stability under nuisance variation, different-device separation, class compactness/separation, identity performance across perturbations, and optional nuisance/domain predictability.

## B5 — Profile evolution

Compare frozen/no-update, always-update, confidence-only, multi-evidence and the Version-B protected policy using the same chronological stream and frozen evaluation.

## B6 — Poisoning

Attack wrong-label contamination, unknown contamination, gradual target-like drift, replay/repetition, mixed streams and feasible adaptive attacks. Measure attack acceptance, profile displacement, identity degradation, legitimate acceptance, rollback and recovery.

## B7 — Integrated lifecycle

Demonstrate `observation -> representation -> recognition -> novelty -> authorization -> profile -> audit` for known, unknown, legitimate-update and poisoning cases.

---

# 7. Dataset and scenario plan

Track A uses the supplied SMoRFFI archive plus explicitly derived controlled scenarios. Every derived record records source file/row, transformation, parameters, seed, physical interpretation, scenario ID and synthetic/derived flag.

Literature-inspired scenarios cover SNR/noise, gain/acquisition scaling, condition drift, channel-like distortion, unknown/open-set exposure and gradual poisoning. These are not represented as source measurements.

Track B later uses independently collected datasets with trustworthy metadata for real day/environment/receiver/channel evidence. Track-B evidence remains separate.

---

# 8. Version B success criteria

Version B requires a defensible Pareto improvement over Version A: reproducibility preserved; materially better unknown rejection at comparable known acceptance; improved controlled-shift robustness; useful legitimate adaptation; materially stronger poisoning resistance; no leakage; auditable architecture; and evidence-level discipline.

Higher closed-set accuracy alone is insufficient.

---

# 9. Recommended Version B architecture

```text
Frozen D2 I/Q
    |
    v
Compact learned encoder
    |
    +-------------------------------+
    |                               |
    v                               v
Device embedding              optional nuisance/domain
    |                           representation
    v
Prototype / metric evidence
    |
    +-------------------------------+
    |               |               |
    v               v               v
identity score  novelty score  consistency evidence
    |               |               |
    +---------------+---------------+
                    v
          ACCEPT / HOLD / REJECT
                    |
             update authorization
                    |
             persistent profile
                    |
                 audit log
```

This is an architecture hypothesis, not a final implementation commitment.

---

# 10. Research questions

**RQ1:** Can compact learned representation plus calibrated prototype/metric evidence materially improve unknown rejection over 29.49% without unacceptable known-acceptance loss?

**RQ2:** Does supervised contrastive/metric learning produce a more compact/discriminative device embedding than the current learned and classical baselines?

**RQ3:** Can controlled nuisance augmentation/consistency reduce acquisition/channel-like degradation?

**RQ4:** Can protected update authorization preserve legitimate adaptation while making poisoning materially harder than always-update/confidence-only policies?

**RQ5:** Can the improved mechanisms remain auditable and implementable as one demonstrable application without coupling UI behaviour to unvalidated scientific assumptions?

---

# 11. UI / Application Architecture — ADDED DECISION

The final Track-A/Version-B deliverable will be a **research demonstrator web application** around the RF engine. The UI is a presentation/control layer and must not contain or redefine scientific decision logic.

## 11.1 Separation of concerns

```text
Web UI
  |
  | API
  v
Backend application layer
  |
  v
RF fingerprint engine
  |
  +--> representation
  +--> recognition
  +--> novelty/open-set decision
  +--> update authorization
  +--> persistent profiles
  +--> audit/provenance
```

The RF engine remains independently executable for experiments and tests.

## 11.2 Planned UI surfaces

### A. Dashboard
System state, enrolled/known-device count, recent decisions, security events and Version-A versus Version-B headline metrics. Version-A values are immutable.

### B. Identification
Select/upload an RF observation or controlled experiment sample. Show input validation, predicted identity, recognition evidence, novelty evidence, profile consistency, ACCEPT/HOLD/REJECT and an evidence summary. Never treat classifier confidence as proof of authenticity.

### C. Device Profiles
Show enrolled profiles, profile version, observation count, representation/RF statistics, dispersion/consistency and profile evolution history.

### D. Open-Set Security
Show known acceptance, unknown rejection, false acceptance and operating curves for frozen experiments, with Version-A/B comparison at identical operating conditions.

### E. Security / Attack Lab
Controlled demonstration of replay, unknown contamination, label contamination and gradual/target-like poisoning. Show attack acceptance, profile displacement, quarantined observations, rollback/recovery and final decision. Generated attacks must be visibly labelled synthetic/derived/controlled.

### F. Audit Trail
Chronological observation/decision/update events with observation ID, source/provenance, model version, profile version, recognition evidence, novelty evidence, authorization, decision and reason.

### G. Evaluation / Research
Frozen experiment results, Version-A/B comparisons, stress curves, confusion matrices and provenance/configuration information.

## 11.3 UI implementation milestones

**UI-A — Skeleton:** after B0/B1/B2 API/data contracts are stable; navigation, dashboard shell and API interfaces may initially use mock data.

**UI-B — Connected demonstrator:** connect real identification, open-set decisions, profiles and audit records after Version-B core implementation.

**UI-C — Final research demonstrator:** add Version-A/B comparison, attack lab, profile-evolution visualisation, evaluation views and provenance/reproducibility displays.

## 11.4 UI truthfulness rules

The UI must distinguish recognition from authentication/authorization; expose ACCEPT/HOLD/REJECT; label real versus derived versus paper-reproduction data; show model/profile versions; expose audit evidence; and never imply scientific validation where only engineering demonstration exists.

## 11.5 Technology decision

No frontend/backend framework is frozen yet. Technology selection follows stable API/data contracts and implementation constraints. Experiments must remain independently runnable.

---

# 12. Immediate execution plan — B0 → B2

The next implementation sequence is fixed:

### B0
Reproduce Version-A controls exactly and freeze the Version-B benchmark manifest/configuration.

### B1
Run M0–M3 closed-set comparison under identical data/split/seed controls.

### B2
Run the same candidates under a validation-calibrated open-set protocol and compare unknown rejection at matched known-acceptance operating points.

**No final Version-B backbone is declared before B0–B2 evidence is reviewed.**

After B2, the best-supported candidate becomes the Version-B backbone and the project proceeds into robustness, fingerprint-purity diagnostics and protected profile evolution/poisoning.

---

# 13. Change-control rule

Version A remains frozen. No historical metric, configuration or evidence may be silently replaced.

All Version-B additions are additive and provenance-preserving. Conflicts with canonical prior results are recorded and investigated rather than resolved by overwriting prior evidence.

`develop` is the active implementation branch. `main` is synchronized only after an explicitly agreed milestone.
