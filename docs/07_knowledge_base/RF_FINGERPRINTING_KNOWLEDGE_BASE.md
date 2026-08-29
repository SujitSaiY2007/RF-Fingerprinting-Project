# RF Fingerprinting Project — Theory & Practical Knowledge Base

**Purpose:** Fast-track learning companion for the team. This is not a textbook. It lists what a team member should understand, implement, explain, and troubleshoot while progressing through the project.

**Rule:** You do not need expert-level knowledge of every topic before implementation. Learn each topic to the level required by the current stage, then deepen it when an experiment exposes a need.

---

# 1. The project in one picture

`RF transmission -> received I/Q -> preprocessing/DSP -> RF evidence -> learned representation -> device identity -> known/unknown decision -> update-safety evaluation -> update authorization -> profile update / reject / quarantine -> monitoring`

The project has two different questions:

1. **Who does this signal appear to come from?**
2. **Should this observation be allowed to change what the system learns about that device?**

The second question is the candidate research contribution. It is not assumed to be novel until experiments and prior-art evidence support it.

---

# 2. Minimum foundations to know before coding

## 2.1 RF basics
Know:
- frequency, wavelength, bandwidth;
- carrier frequency and baseband;
- amplitude and phase;
- modulation at a basic level;
- signal-to-noise ratio (SNR);
- channel effects and multipath;
- transmitter versus receiver effects.

You should be able to explain why two nominally identical transmitters can leave slightly different hardware-related patterns in their received signals.

## 2.2 Complex/IQ signals
Know:
- I = in-phase component;
- Q = quadrature component;
- complex sample: `I + jQ`;
- magnitude: `sqrt(I^2 + Q^2)`;
- phase: `atan2(Q, I)`;
- why RF datasets often store I/Q rather than a single real-valued waveform.

Practical ability:
- load I/Q data;
- inspect shape and dtype;
- plot I and Q;
- plot magnitude/phase;
- detect clipping, NaNs, constant signals and malformed samples.

## 2.3 Sampling
Know:
- sample rate;
- Nyquist idea;
- samples per burst/packet;
- time duration represented by a sample sequence;
- why changing sample rate or resampling can change what a model sees.

## 2.4 Basic signal processing
Know at least:
- normalization;
- filtering;
- FFT and spectrum;
- spectrogram/time-frequency representation;
- synchronization;
- burst detection;
- carrier frequency offset (CFO) at a conceptual level;
- timing offset;
- phase/frequency correction.

Do not memorize formulas without understanding what problem each operation solves.

---

# 3. Machine-learning foundations

Know:
- train/validation/test split;
- classification;
- labels;
- features;
- neural network basics;
- loss function;
- optimizer;
- overfitting;
- regularization;
- batch/epoch;
- inference versus training;
- checkpointing and reproducibility.

## Metrics
Know when to use:
- accuracy;
- precision;
- recall;
- F1;
- confusion matrix;
- ROC-AUC where appropriate;
- false acceptance rate;
- false rejection rate.

For this project, do not report only accuracy.

---

# 4. Data leakage — mandatory knowledge

This is one of the most important practical concepts in the project.

A random sample split can be misleading when neighbouring samples come from the same burst, session or recording.

Example:

`same recording session -> many slices -> random train/test split`

can make the model appear extremely accurate because train and test contain nearly identical acquisition conditions.

Prefer splits based on the actual claim:
- device holdout;
- session holdout;
- day holdout;
- receiver holdout;
- environment/location holdout;
- chronological holdout.

Always ask:

> “What information from the test period could accidentally be present in training?”

---

# 5. D1 — Raw RF Data / Ingestion

## Goal
Create a reliable and reproducible foundation for all later experiments.

## Theory to know
- raw versus derived data;
- provenance;
- metadata;
- checksums;
- file formats;
- dtype/shape/channel interpretation;
- device/session/day/receiver/environment identifiers;
- data roots and configuration;
- reproducible manifests.

## Practical work
For WiSig and Oregon State WiFi RFFP:
1. identify authoritative source/version;
2. document acquisition/reference;
3. keep large raw archives outside Git;
4. create manifests/checksums where feasible;
5. inspect file structures;
6. write loaders;
7. normalize metadata into a common schema;
8. preserve source-specific fields;
9. record missing/ambiguous metadata;
10. write loadability/integrity tests;
11. create leakage-safe partition metadata.

## Must be able to answer
- What exactly is one sample?
- What does each dimension mean?
- Is it I/Q, real, complex, or transformed data?
- Which device produced it?
- When and where was it recorded?
- Which receiver was used?
- Can another team member reproduce the same load?

## Exit evidence
A manifest + loader + metadata schema + tests + documented provenance + reproducible local data root.

---

# 6. D2 — Synchronization & DSP

## Goal
Turn raw RF observations into consistently aligned observations without accidentally removing device-specific information.

## Theory to know
- burst/packet boundaries;
- timing synchronization;
- carrier/frequency offset;
- filtering;
- normalization;
- resampling;
- signal quality/SNR;
- preprocessing consistency.

## Practical work
Build a minimal deterministic preprocessing chain:

`raw I/Q -> validity check -> burst selection -> synchronization -> optional filtering/normalization -> model-ready signal`

Keep the raw signal untouched.

## Critical risk
Over-processing can remove the very hardware imperfections that contain the fingerprint.

## Exit evidence
A documented preprocessing function, before/after plots, parameter record, and tests showing consistent output shapes.

---

# 7. D3 — Physics-Based RF Evidence

## Goal
Extract interpretable RF characteristics that may carry transmitter-specific information.

## Theory to know
Examples:
- carrier frequency offset (CFO);
- phase/frequency behaviour;
- I/Q imbalance;
- amplitude-related characteristics;
- transient behaviour;
- spectral characteristics;
- other hardware-induced imperfections.

Important distinction:

**Carrier frequency itself is not the RF fingerprint.** Hardware imperfections around the transmitted signal can create device-specific patterns.

## Practical work
Start small. Extract a few defensible features rather than building a huge feature library.

For each feature ask:
- Is it reproducible?
- Is it device-discriminative?
- Is it strongly affected by receiver/environment?
- Does it remain useful across time?

## Exit evidence
Feature extraction code + feature distributions + basic device-separation analysis + sensitivity analysis.

---

# 8. D4 — Device Representation / Embedding

## Goal
Learn a compact representation in which observations from the same device tend to be related and different devices can be separated.

## Theory to know
- embedding/vector representation;
- feature space;
- distance/similarity;
- cosine similarity;
- Euclidean distance;
- metric learning at a basic level;
- prototype/centroid;
- classification versus representation learning.

## Practical work
Build a simple baseline first:
- CNN or similarly simple sequence model;
- extract embedding before final classifier;
- visualize embeddings with PCA/UMAP if useful;
- calculate within-device versus between-device distances.

## Important project decision
Embeddings are an enabling component, **not the novelty claim**.

## Exit evidence
Reproducible model + embeddings + distance statistics + baseline identification performance.

---

# 9. D5 — Closed-Set Device Identification

## Goal
Answer:

> “Among the devices the system already knows, which device produced this observation?”

## Theory
- closed-set classification;
- decision confidence;
- confusion matrix;
- class imbalance;
- calibration at a basic level.

## Practical work
Train a clean baseline using leakage-safe splits.

Report:
- accuracy;
- per-device precision/recall/F1;
- confusion matrix;
- confidence distribution.

## Exit evidence
A reproducible baseline that becomes the reference point for every later stage.

---

# 10. D6 — Open-Set Recognition

## Goal
Answer both:

> “Which known device is this?”

and

> “Could this actually be a device the system has never seen?”

## Theory
- known versus unknown;
- open-set recognition;
- rejection threshold;
- prototype distance;
- confidence versus uncertainty;
- false acceptance of unknown devices.

## Practical protocol
Hold out some devices completely from training.

Do not leak observations from an unknown device into representation/model fitting.

Test:
- known-device acceptance;
- unknown-device rejection;
- threshold sensitivity.

## Exit evidence
Known/unknown evaluation with an explicit unseen-device protocol.

---

# 11. D7 — Robustness / Domain Shift

## Goal
Understand whether a device still looks like itself when conditions change.

## Possible shifts
- day/time;
- receiver;
- environment;
- location;
- channel;
- SNR;
- temperature/load when metadata exists.

## Theory
- domain shift;
- temporal drift;
- distribution shift;
- domain adaptation;
- test-time adaptation.

## Practical work
Train on one condition and test on another.

Measure degradation rather than hiding it through random mixing.

## Key question
Is a change caused by the device, or by the measurement environment?

## Exit evidence
A shift matrix and baseline robustness results.

---

# 12. D8 — Continual Learning / Profile Evolution

## Goal
Allow a device profile/model to evolve as legitimate observations arrive over time.

## Theory to know
- continual learning;
- incremental learning;
- catastrophic forgetting;
- replay/basic memory;
- chronological evaluation;
- profile drift;
- rollback;
- frozen evaluation set.

## Core project idea
Do **not** let the test set evolve with the model.

Maintain:

`frozen evaluation data`

while the profile is updated using a separate chronological stream.

## Baselines
A. `Identify -> Update`

B. `Identify -> Confidence threshold -> Update`

C. `Identify -> Reliability/consistency -> Update`

D. Candidate secure update authorization.

## Exit evidence
A chronological profile-update experiment with measured adaptation, drift, forgetting and update acceptance.

---

# 13. D9 — Poisoning / Adversarial Protection

## Goal
Test whether bad observations can silently corrupt the persistent device profile.

## Theory
Know the difference between:
- inference-time adversarial attack;
- poisoning/training-data attack;
- backdoor attack;
- model corruption;
- profile corruption.

The project's key threat is:

`malicious/abnormal observation -> accepted as Device A -> incorporated into A's profile -> future decisions change`

## Controlled experiment
Use legitimate RF data and clearly labelled controlled/synthetic poisoning.

Do not claim that synthetic attacks reproduce every real attacker.

## Compare
- naive update;
- confidence-only update;
- reliability/admission update;
- proposed security-gated update.

## Metrics
- attack success;
- profile drift;
- recognition degradation;
- number of malicious observations needed;
- recovery after rejection;
- legitimate false rejection.

## Exit evidence
A reproducible attack-generation protocol + before/after profile measurements + comparison across update policies.

---

# 14. D10 — End-to-End Validation

## Goal
Connect the validated pieces into one coherent software lifecycle.

`RF -> preprocessing -> RF evidence -> representation -> identity/open-set -> update-safety -> authorization -> profile evolution -> monitoring`

## What to demonstrate
1. normal known-device recognition;
2. unknown-device rejection;
3. adaptation to legitimate temporal/domain change;
4. profile stability;
5. controlled poisoning attempt;
6. update rejection/quarantine where appropriate;
7. recovery and continued legitimate adaptation.

## Exit evidence
A complete experiment report showing whether the candidate contribution actually improves the security–adaptation trade-off.

---

# 15. Novelty knowledge — what we must be able to explain

## Not novel individually
- RF fingerprinting;
- RF embeddings;
- open-set recognition;
- continual/incremental learning;
- adaptive RF model updating;
- temporal/domain adaptation;
- physical RF features;
- generic adversarial robustness.

## Current candidate
The candidate is narrower:

> **Treat permission to modify persistent RF identity state as a separate security decision from recognizing the device, and test whether this protects continual profile evolution against poisoning without blocking legitimate adaptation.**

## Important challenge
Prior work already performs related forms of reliable-sample admission and adaptive updating. Therefore the project must prove that the **security-oriented separation and its explicit update outcome** add value beyond ordinary reliability/confidence filtering.

---

# 16. Practical Python knowledge

Minimum skills:
- NumPy arrays;
- complex numbers;
- slicing/reshaping;
- pandas metadata tables;
- pathlib/file handling;
- JSON/YAML configuration;
- matplotlib plots;
- scikit-learn baselines and metrics;
- PyTorch basics if used;
- random seeds;
- saving/loading checkpoints;
- logging experiment parameters/results.

## Must understand
Do not blindly copy tensor shapes. Always write down:

`[samples, channels, time]`

or whatever the actual dataset uses, and verify it.

---

# 17. Experiment discipline

Every experiment should record:

- dataset/version;
- exact split;
- preprocessing configuration;
- model configuration;
- random seed;
- training configuration;
- evaluation metrics;
- checkpoint identifier;
- result file;
- interpretation;
- decision.

Use the lifecycle:

`Requirement -> Design -> Implementation -> Test -> Experiment -> Result -> Interpretation -> Decision`

---

# 18. What to learn first when time is extremely limited

### Tier 1 — must know immediately
1. I/Q data.
2. RF fingerprint concept.
3. dataset metadata and leakage.
4. train/test evaluation.
5. CNN/embedding basics.
6. closed-set vs open-set.
7. temporal/domain shift.
8. continual learning concept.
9. profile update concept.
10. poisoning versus inference-time attack.

### Tier 2 — learn while implementing
1. synchronization details;
2. CFO and RF impairments;
3. metric learning;
4. calibration/uncertainty;
5. replay and forgetting;
6. anomaly detection;
7. attack generation;
8. ablation studies.

### Tier 3 — only if needed
1. advanced domain adaptation;
2. advanced self-supervised learning;
3. sophisticated continual-learning algorithms;
4. advanced adversarial training;
5. hardware/SDR implementation.

---

# 19. Questions you should be able to answer in a professor meeting

1. What is an RF fingerprint?
2. Where does the fingerprint information come from?
3. Why is the carrier frequency alone not the fingerprint?
4. What is I/Q data?
5. How do we know which device produced a training sample?
6. How do we prevent train/test leakage?
7. What is open-set recognition?
8. What changes over time in an RF signal?
9. Why do we need continual learning?
10. What is the danger of automatically updating a device profile?
11. Why is a correct identity decision not necessarily a safe learning decision?
12. What evidence could make an observation suspicious?
13. What existing work already does something similar?
14. What exactly is different in our proposed mechanism?
15. How will we prove that difference experimentally?
16. What result would make us abandon the novelty claim?

If you cannot answer one of these, that topic becomes a targeted learning item before the relevant implementation stage.

---

# 20. Final learning rule

Do not study the entire field before coding.

Use:

`Build -> encounter concept -> learn concept -> implement -> measure -> explain -> document`

The goal is **working scientific understanding**, not memorization.
