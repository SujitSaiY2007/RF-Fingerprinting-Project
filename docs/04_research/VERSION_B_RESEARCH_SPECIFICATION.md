# Version B Research Specification — Robust Open-Set RF Fingerprinting

**Status:** Research specification / decision framework — not yet implemented
**Branch:** `develop`
**Date:** 2026-08-30
**Relationship to Version A:** Version A remains frozen as the reference baseline. Version B must preserve the same high-level lifecycle while replacing or strengthening individual mechanisms only when evidence justifies the change.

---

## 1. Purpose

Version B is the next research prototype intended to address the three principal weaknesses identified by Track A Version A:

1. weak open-set/unknown-device rejection;
2. unverified separation of transmitter fingerprint information from acquisition/channel/receiver effects;
3. vulnerability of adaptive profile evolution to profile poisoning.

The project is **not** restarting D1/D2. The frozen D2 input contract remains:

`serialized preamble -> complex[288] -> float32[2,288] I/Q`

The Version B architecture must retain the lifecycle:

`RF observation -> representation -> recognition -> novelty/security decision -> update authorization -> persistent profile -> audit`

The implementation inside those stages may change.

---

## 2. Version A reference — never overwrite

The current Track-A reference is:

- real substrate: SMoRFFI;
- known devices: 1–33;
- frozen classical RF baseline: 16 deterministic RF evidence features + fixed Random Forest;
- closed-set test accuracy: **87.39%**;
- macro-F1: **87.32%**;
- balanced accuracy: **87.41%**;
- RF confidence-gate known acceptance: **94.90%**;
- RF confidence-gate unknown rejection: **29.49%**;
- D7 gain/AWGN stress: strong acquisition sensitivity;
- D8 persistent profile mechanism: implemented/tested/demonstrated;
- D9 replay resistance: demonstrated in the controlled scenario;
- D9 poisoning resistance: not established; target-like contamination remained a vulnerability;
- fingerprint purity: not scientifically established;
- temporal/session/environment/receiver generalization: Track B evidence, not Track-A evidence.

Historical ~91.1% remains historical/unreconstructed and must not be used as Version A's reproduced result.

Version B must always report deltas against this frozen reference.

---

## 3. Research principles

### 3.1 Evidence hierarchy

Each Version B claim must be tagged:

- **Implemented** — code exists.
- **Tested** — engineering/reproducibility tests pass.
- **Demonstrated** — integrated operation is shown on real or explicitly controlled data.
- **Scientifically Validated** — claim survives independent/held-out evidence appropriate to the claim.

A higher label cannot be inferred from a lower one.

### 3.2 No model-chasing

Model selection must follow the evaluation problem. The project will not select a model because it produces the largest closed-set accuracy on one split.

### 3.3 No dataset laundering

Three data classes remain distinct:

1. **REAL_SOURCE_DATA** — directly measured/source observations.
2. **DERIVED_CONTROLLED_DATA** — transformations applied to source observations, explicitly synthetic/derived.
3. **PAPER_REPRODUCTION_SCENARIO** — controlled experiments inspired by published methodology/parameter ranges; not a claim of exact reproduction unless the original dataset, preprocessing, split and configuration are available.

Synthetic data can test mechanisms but cannot be presented as source-dataset measurements.

### 3.4 Frozen evaluation

For every experiment, the final evaluation set is frozen before any model selection, threshold selection, profile update stream or attack generation that could influence it.

### 3.5 Leakage control

No future evaluation observation may update a profile before that observation is evaluated. No test-derived threshold may be reused as a training/admission threshold without explicit separation.

### 3.6 Security-first interpretation

A model with higher closed-set accuracy but worse unknown rejection, condition robustness or poisoning resistance is not automatically an improvement.

---

# 4. Literature-derived mechanism matrix

## 4.1 Baseline / dataset lesson

### SMoRFFI
The 2026 SMoRFFI paper describes 123 same-model IEEE 802.11g devices, 35.42M raw I/Q samples and a reproducible RF-feature pipeline, with a published Random Forest baseline of 88.6%. Its same-model design is highly relevant to this project because same-model discrimination is harder than separating different hardware families.

**Project use:** primary Track-A real substrate and reference for classical RF features. Do not claim that the published 88.6% result is our exact result; our frozen repository result is 87.39% under its own configuration/split.

### “Why RF Fingerprinting Needs Better Data, Not Bigger Models”
This 2025 IEEE Access study compares lightweight fully connected networks with larger architectures and argues that dataset/evaluation design can matter more than model size. It reports competitive performance with much lower computation and comparable resilience to channel/device variability.

**Project use:** strong warning against selecting a large deep model solely for headline accuracy. Version B must benchmark a compact model alongside a CNN/metric-learning candidate.

---

## 4.2 Open-set recognition

### Improved Prototype Learning — Wang, Liao, Gan (2023)
The paper explicitly targets open-set RFFI and uses prototype learning with consistency-based regularization and online label smoothing to make the feature space more suitable for unknown-device rejection.

**Mechanisms to reproduce/test:**
- prototype representation;
- distance-to-class prototype;
- consistency regularization;
- label smoothing;
- validation-derived rejection threshold.

**Reason:** directly aligned with the current 29.49% unknown-rejection weakness.

### FSST + Supervised Contrastive Learning + Open Classifier (2024)
This work explicitly combines a distinctive RF representation with supervised contrastive learning and an open-set classifier. It evaluates noisy and high-openness conditions and reports strong performance improvements under those conditions.

**Mechanisms to reproduce/test:**
- supervised contrastive embedding;
- more concentrated class structure;
- explicit open-set decision layer;
- SNR/openness stress.

**Constraint:** the project must preserve the frozen D2 I/Q contract. FSST/spectrogram representations may be tested as an auxiliary candidate, but cannot silently replace the canonical input.

### Multi-Task Prototype Learning (2025)
This work combines discriminative classification, reconstruction and prototype clustering in a shared encoder/decoder/classifier architecture for open-set RFFI.

**Mechanisms to reproduce/test:**
- classification loss;
- prototype clustering loss;
- reconstruction/consistency auxiliary task;
- prototype-based novelty scoring.

**Reason:** reconstruction may provide an additional signal for rejecting observations that do not resemble enrolled device manifolds.

### Calibrated Open-Set Prototypes (2026)
A recent open-access paper combines calibrated prototype scores with support-aware prototype aggregation and explicitly targets cross-domain open-set emitter recognition and few-shot registration.

**Mechanisms to reproduce/test:**
- calibrated prototype score;
- validation-based rejection threshold;
- support-aware prototype aggregation;
- robust support trimming/centrality weighting;
- explicit novel-device registration state.

**Reason:** particularly relevant to the project’s combination of open-set rejection and later profile evolution.

### Incremental Open-Set Recognition with Contrastive Learning (2024 journal publication)
This work addresses transmitter identification where transmitter categories can change and new categories appear incrementally.

**Mechanisms to study:**
- contrastive embedding for incremental class structure;
- explicit unknown/new-class handling;
- separation of recognition from category expansion.

**Reason:** closely related to the desired lifecycle of persistent RF profiles.

---

## 4.3 Representation learning / fingerprint purity

### Contrastive learning
The open-set literature consistently motivates contrastive learning as a way to compact same-device samples and separate different devices. Version B should therefore test supervised contrastive learning as a candidate representation objective rather than assuming ordinary cross-entropy classification is sufficient.

### Receiver/channel disentanglement
Recent cross-receiver work shows that RFFI can overfit receiver-specific features. Published approaches include contrastive adaptation, adversarial/domain-invariant learning, style/feature disentanglement and receiver calibration.

**Mechanisms to test:**
- domain-adversarial feature learning;
- receiver/domain classification with gradient reversal;
- contrastive invariance across controlled channel/acquisition transformations;
- explicit receiver/domain auxiliary head;
- feature-ablation tests to determine whether device identity survives condition changes.

**Important:** Track A cannot scientifically prove receiver invariance without receiver metadata. Controlled transformations are stress tests, not substitutes for Track-B real receiver evidence.

### Cross-receiver source-free adaptation
Recent work reports contrastive/self-supervised source-free adaptation for receiver changes. This is relevant as a future Track-B mechanism, but it should not be the first Version-B dependency because Track A does not yet possess verified receiver-domain metadata.

---

## 4.4 Profile evolution and poisoning

The project's novelty hypothesis concerns **authorization to update persistent identity state**, not merely classification.

General adaptive-authentication research demonstrates that self-updating templates can be poisoned gradually by carefully crafted samples. This supports treating profile update authorization as a security boundary rather than a convenience feature.

**Mechanisms Version B must investigate:**

- confidence threshold;
- identity/prototype distance;
- profile consistency/dispersion;
- temporal consistency;
- repeated-observation/replay detection;
- update rate/budget limits;
- quarantine before admission;
- evidence accumulation across independent observations;
- robust/trimmed prototype update;
- bounded profile movement;
- rollback/checkpointing;
- post-update validation against a frozen reference set;
- explicit human/admin approval mode as a comparison, if appropriate.

The project must attack these mechanisms rather than assuming they work.

---

# 5. Version B candidate model families

No single model is frozen yet.

## Candidate M0 — Version A RF baseline

16 RF features + fixed Random Forest.

**Purpose:** immutable reference/control.

## Candidate M1 — Compact learned I/Q classifier

Small 1-D CNN or compact temporal encoder using the frozen 2x288 I/Q input.

**Purpose:** determine whether learned representation can outperform the classical feature baseline without excessive model complexity.

## Candidate M2 — I/Q encoder + metric/prototype head

Encoder produces an embedding; identity is determined by prototype/distance evidence rather than only a softmax head.

**Purpose:** direct open-set candidate.

## Candidate M3 — I/Q encoder + supervised contrastive objective + prototype/open-set head

Train embedding for intra-device compactness/inter-device separation, then use calibrated prototype distances for recognition/novelty.

**Purpose:** primary Version-B candidate unless experiments disprove it.

## Candidate M4 — M3 + auxiliary reconstruction/consistency objective

Add reconstruction or consistency task to discourage unstable representations.

**Purpose:** test whether multi-task representation learning improves open-set behaviour and robustness.

## Candidate M5 — M3/M4 + domain-invariance mechanism

Add receiver/channel/domain invariance only when the experimental metadata or controlled scenarios support it.

**Purpose:** fingerprint-purity/robustness research, not an assumed requirement for the first Version-B model.

### Current recommendation

**Do not immediately build M5.** First compare M0–M3 under a frozen open-set protocol. M4 becomes a controlled extension if reconstruction/consistency evidence is useful. M5 belongs to the robustness stage and eventually Track B.

---

# 6. Version B evaluation ladder

Every candidate must pass the same ladder.

## Gate B0 — Reproducibility

- deterministic seed/configuration;
- frozen D2 input;
- exact dataset manifest;
- source/derived provenance;
- no evaluation leakage.

## Gate B1 — Closed-set

Report:
- accuracy;
- macro-F1;
- balanced accuracy;
- per-device precision/recall/F1;
- confusion matrix;
- repeated-seed variance.

Closed-set improvement is necessary but not sufficient.

## Gate B2 — Open-set

Known devices remain 1–33. Unknown devices are held out from training/enrollment.

Report:
- known acceptance rate;
- unknown rejection rate;
- unknown false-acceptance rate;
- AUROC;
- AUPR where meaningful;
- FPR at fixed TPR/known-acceptance operating points;
- OSCR or an equivalent open-set curve;
- macro-F1 for the open-set decision task.

Thresholds must be selected only from the validation partition.

## Gate B3 — Controlled acquisition stress

Use explicitly derived scenarios:
- gain shifts;
- AWGN/SNR sweep;
- controlled phase/frequency perturbations where physically justified;
- combinations of shifts;
- optionally channel-like multipath transformations with clear physical interpretation.

Report degradation curves rather than one cherry-picked point.

## Gate B4 — Fingerprint-purity diagnostics

Test whether embedding identity remains stable under controlled nuisance transformations.

Required analyses:
- same-device embedding distance under nuisance variation;
- different-device embedding distance;
- class compactness/separation;
- identity accuracy across perturbation families;
- optional domain/nuisance probe to determine whether the embedding still encodes the nuisance strongly.

A reduction in nuisance predictability is evidence of improved invariance, not proof of physical transmitter purity.

## Gate B5 — Profile evolution

Compare:
1. frozen/no-update;
2. always-update;
3. confidence-only;
4. multi-evidence;
5. any Version-B protected update policy.

The same chronological stream and frozen evaluation must be used across policies.

## Gate B6 — Poisoning

Attack classes:
- wrong-label contamination;
- unknown-device contamination;
- gradual target-like drift;
- replay/repetition;
- mixed legitimate/attack streams;
- adaptive attack that uses observed accept/reject behaviour, if feasible.

Measure:
- attack acceptance rate;
- profile displacement;
- identity degradation;
- false acceptance after attack;
- legitimate acceptance after attack;
- rollback success;
- number of attack observations required to cause a defined failure;
- recovery time/observations.

## Gate B7 — Integrated lifecycle

Demonstrate:

`observation -> representation -> recognition -> novelty -> authorization -> profile -> audit`

with known, unknown, legitimate-update and poisoning cases.

---

# 7. Dataset and scenario plan

## Track A — immediate

Use the supplied complete SMoRFFI archive and construct controlled/derived scenarios from it.

Required provenance fields for every derived record:

- source file;
- source row/index;
- transformation family;
- parameter value/range;
- random seed;
- physical interpretation;
- scenario ID;
- synthetic/derived flag.

## Literature-inspired scenarios

Use published studies to select realistic stress families and compare mechanisms, but do not claim the derived data are measured observations from those studies.

Priority scenario families:

1. SNR/noise;
2. gain/acquisition scaling;
3. time/condition drift;
4. channel-like distortion;
5. unknown/open-set device exposure;
6. gradual profile poisoning.

## Track B — later scientific validation

Use independently collected datasets with trustworthy metadata:

- Oregon State WiFi RFFP for real day/environment variation;
- WiSig/ManySig for real receiver/day/channel variation;
- ORACLE for controlled hardware/distance comparison.

Track-B evidence must remain separate from Track-A evidence.

---

# 8. What counts as Version B success?

Version B is **not** successful merely because it exceeds 87.39% closed-set accuracy.

A defensible success requires a Pareto improvement over Version A, with at minimum:

1. no regression in reproducibility;
2. materially better unknown rejection at a comparable known-acceptance operating point;
3. improved robustness under the controlled D7 stress families;
4. profile updates remain useful for legitimate adaptation;
5. poisoning requires substantially more attack effort or produces substantially less profile damage;
6. no evaluation leakage;
7. the architecture remains auditable;
8. claims are labelled by evidence level.

A candidate that improves closed-set accuracy but worsens open-set security should be rejected or retained only as an explicit ablation.

---

# 9. Recommended Version B architecture

The current working hypothesis is:

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

This is an **architecture hypothesis**, not a final implementation commitment.

The project will preserve the Version-A lifecycle while improving the internal mechanisms.

---

# 10. Research questions Version B must answer

### RQ1 — Open-set
Can a learned compact representation plus calibrated prototype/metric evidence substantially improve unknown-device rejection over the Version-A 29.49% result without unacceptable loss of known-device acceptance?

### RQ2 — Representation
Does supervised contrastive/metric learning produce a more compact and discriminative device embedding than the current learned classifier and classical RF feature baseline?

### RQ3 — Robustness
Can controlled nuisance augmentation/consistency mechanisms reduce the severe gain/AWGN sensitivity observed in D7?

### RQ4 — Fingerprint purity
Does the improved embedding preserve device identity under controlled nuisance variation while reducing dependence on nuisance factors?

### RQ5 — Adaptive security
Can update authorization permit legitimate profile evolution while resisting gradual, target-like and replay-based contamination?

### RQ6 — Lifecycle
Can all improvements coexist in one auditable pipeline without allowing future evaluation data to influence the decision being evaluated?

---

# 11. Explicit non-goals

Version B will not:

- redo D1/D2;
- silently change the frozen input representation;
- claim the historical ~91.1% result has been reproduced;
- treat synthetic data as real measurements;
- claim receiver/channel invariance from SMoRFFI alone;
- claim poisoning resistance merely because one attack failed;
- optimize thresholds on the final test set;
- replace Version A evidence;
- force Track-B datasets into Track-A results.

---

# 12. Literature shortlist

1. Jagannath et al., *A comprehensive survey on radio frequency (RF) fingerprinting: Traditional approaches, deep learning, and open challenges*, Computer Networks, 2022. DOI: 10.1016/j.comnet.2022.109455.
2. Sankhe et al., *ORACLE: Optimized Radio clAssification through Convolutional neuraL nEtworks*, IEEE INFOCOM, 2019. Dataset and project resources: GENESYS Lab.
3. Guo et al., *SMoRFFI: A large-scale same-model 2.4 GHz Wi-Fi dataset and reproducible framework for RF fingerprinting*, Computer Networks, 2026, 112309. DOI: 10.1016/j.comnet.2026.112309.
4. Wang, Liao & Gan, *Open-Set RF Fingerprinting via Improved Prototype Learning*, 2023, arXiv:2306.13895.
5. Huang et al., *Radio frequency fingerprint extraction and authentication towards open set in noisy channels*, Digital Signal Processing, 2024, 104363.
6. Zhang et al., *Transmitter Identification With Contrastive Learning in Incremental Open-Set Recognition*, IEEE Internet of Things Journal, 2024, 11(3):4693–4711. DOI: 10.1109/JIOT.2023.3300122.
7. Bothereau et al., *Why RF Fingerprinting Needs Better Data, Not Bigger Models*, IEEE Access, 2025, 13:171348–171355. DOI: 10.1109/ACCESS.2025.3614459.
8. Cross-receiver RFFI work using contrastive/subdomain adaptation, IEEE Xplore document 10034841.
9. Cross-receiver RFFI source-free adaptation / CSCNet, 2025, PubMed/PMC record.
10. Pan et al., *Cross-Receiver Generalization for RF Fingerprint Identification via Feature Disentanglement and Adversarial Training*, 2025.
11. He et al., *Deep Learning based Cross-Receiver Radio Frequency Fingerprint Identification Under Varying Channels*, 2026, arXiv:2603.08402.
12. Li et al., *Calibrated Open-Set Prototypes for Cross-Domain Radio-Frequency Emitter Recognition*, Electronics, 2026, 15(14):3077. DOI: 10.3390/electronics15143077.
13. Xue et al., *LOPA: A linear offset based poisoning attack method against adaptive fingerprint authentication system*, Computers & Security, 2020, 99:102046. DOI: 10.1016/j.cose.2020.102046. This is biometric-template literature, not RF-specific; it is used only to motivate and structure the adaptive-profile poisoning threat model.

---

# 13. Decision status

**Approved direction for investigation:**

- Preserve Version A as immutable reference.
- Start Version B with a mechanism/literature study rather than immediate model implementation.
- Benchmark M0–M3 first.
- Treat M3 (learned I/Q embedding + supervised contrastive objective + calibrated prototype/open-set head) as the leading candidate, not a predetermined winner.
- Add M4 only if auxiliary reconstruction/consistency evidence supports it.
- Defer domain/receiver disentanglement to the robustness stage and Track B validation.
- Treat adaptive profile authorization as a separate security layer from recognition.
- Attack every proposed improvement with controlled unknown and poisoning scenarios.

**No Version B model or metric is frozen by this document.** The next implementation milestone is the construction of the reproducible B0/B1/B2 benchmark harness and literature-mechanism reproductions before selecting the final Version-B backbone.
