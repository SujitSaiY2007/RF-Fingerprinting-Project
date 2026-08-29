# RF Fingerprinting Project — Theory & Practical Knowledge Base

**Purpose:** Fast-track learning companion for the team. This is not a textbook. It lists what a team member should understand, implement, explain, and troubleshoot while progressing through the project.

**Rule:** You do not need expert-level knowledge of every topic before implementation. Learn each topic to the level required by the current stage, then deepen it when an experiment exposes a need.

# 1. Project in one picture

`RF transmission -> received I/Q -> preprocessing/DSP -> RF evidence -> learned representation -> device identity -> known/unknown decision -> update-safety evaluation -> update authorization -> profile update / reject / quarantine -> monitoring`

Two different questions:

1. **Who does this signal appear to come from?**
2. **Should this observation be allowed to change what the system learns about that device?**

The second question is the candidate research contribution. It is not assumed to be novel until experiments and prior-art evidence support it.

# 2. Minimum foundations

## RF basics
Know:
- frequency, wavelength, bandwidth;
- carrier frequency and baseband;
- amplitude and phase;
- modulation at a basic level;
- SNR;
- channel effects and multipath;
- transmitter versus receiver effects.

Be able to explain why two nominally identical transmitters can leave slightly different hardware-related patterns in their received signals.

## Complex/IQ signals
Know:
- I = in-phase component;
- Q = quadrature component;
- complex sample = `I + jQ`;
- magnitude = `sqrt(I^2 + Q^2)`;
- phase = `atan2(Q, I)`;
- why RF datasets often store I/Q.

Practical ability:
- load I/Q;
- inspect shape/dtype;
- plot I/Q;
- plot magnitude/phase;
- detect malformed samples.

## Sampling
Know sample rate, Nyquist idea, samples per burst, represented time duration, and why resampling can change model inputs.

## Signal processing
Know at a basic level:
- normalization;
- filtering;
- FFT/spectrum;
- spectrogram;
- burst detection;
- synchronization;
- CFO;
- timing offset;
- phase/frequency correction.

Do not memorize formulas without understanding the problem each operation solves.

# 3. Machine-learning foundations

Know:
- train/validation/test split;
- classification;
- features and labels;
- neural-network basics;
- loss and optimizer;
- overfitting;
- regularization;
- batch/epoch;
- inference versus training;
- checkpointing;
- reproducibility.

Metrics:
- accuracy;
- precision;
- recall;
- F1;
- confusion matrix;
- ROC-AUC where appropriate;
- false acceptance;
- false rejection.

Do not report only accuracy.

# 4. Data leakage — mandatory

Random sample splitting can be misleading when nearby samples come from the same burst/session/recording.

Prefer splits based on the claim:
- device holdout;
- session holdout;
- day holdout;
- receiver holdout;
- environment/location holdout;
- chronological holdout.

Always ask:

> What information from the test period could accidentally be present in training?

# 5. D1 — Raw RF Data / Ingestion

**Goal:** reliable, reproducible foundation.

Know:
- raw versus derived data;
- provenance;
- metadata;
- checksums;
- file formats;
- dtype/shape/channel interpretation;
- device/session/day/receiver/environment identifiers;
- reproducible data roots;
- manifests.

Practical work for WiSig + Oregon State WiFi:
1. identify authoritative source/version;
2. document acquisition/reference;
3. keep raw archives outside Git;
4. create manifests/checksums where feasible;
5. inspect file structure;
6. write loaders;
7. normalize metadata;
8. preserve source-specific fields;
9. record missing/ambiguous metadata;
10. write loadability/integrity tests;
11. create leakage-safe partition metadata.

**Exit evidence:** manifest + loader + metadata schema + tests + provenance + reproducible local data root.

# 6. D2 — Synchronization & DSP

**Goal:** consistently aligned model-ready observations without destroying device-specific information.

Know burst/packet boundaries, synchronization, CFO, filtering, normalization, resampling, SNR and preprocessing consistency.

Build:

`raw I/Q -> validity check -> burst selection -> synchronization -> optional filtering/normalization -> model-ready signal`

Keep raw data untouched.

**Critical risk:** over-processing can remove fingerprint information.

# 7. D3 — Physics-Based RF Evidence

**Goal:** extract interpretable transmitter-related RF characteristics.

Know examples such as:
- CFO;
- phase/frequency behaviour;
- I/Q imbalance;
- amplitude statistics;
- transient behaviour;
- spectral characteristics;
- other hardware-induced imperfections.

**Important:** carrier frequency itself is not the fingerprint.

Start with a small defensible feature set. Ask whether each feature is reproducible, device-discriminative and robust to receiver/environment/time changes.

# 8. D4 — Device Representation / Embedding

**Goal:** learn a compact representation where same-device observations are related and different devices are separated.

Know:
- embedding/vector;
- feature space;
- cosine/Euclidean distance;
- metric learning at a basic level;
- prototype/centroid;
- classification versus representation learning.

Start with a lightweight 1D CNN or comparable sequence model. Extract an embedding before the classifier. Compare within-device versus between-device distances.

**Decision:** embeddings are an enabling component, not the novelty claim.

# 9. D5 — Closed-Set Identification

**Goal:** among known devices, identify the likely device.

Know closed-set classification, confidence, confusion matrix, class imbalance and basic calibration.

Evaluate:
- accuracy;
- per-device precision/recall/F1;
- confusion matrix;
- confidence distribution.

This becomes the reference identity model.

# 10. D6 — Open-Set Recognition

**Goal:** recognize known devices while rejecting devices never seen during training.

Know:
- known versus unknown;
- rejection threshold;
- prototype distance;
- confidence versus uncertainty;
- false acceptance of unknown devices.

Hold out some devices completely from training. Test known acceptance, unknown rejection and threshold sensitivity.

**Decision:** open-set recognition is established, not standalone novelty.

# 11. D7 — Robustness / Domain Shift

**Goal:** understand whether a device still looks like itself when conditions change.

Possible shifts:
- day/time;
- receiver;
- environment/location;
- channel;
- SNR;
- temperature/load when metadata exists.

Know domain shift, temporal drift, distribution shift, domain adaptation and test-time adaptation conceptually.

Train on one condition and test on another. Measure degradation rather than hiding it through random mixing.

# 12. D8 — Continual Learning / Profile Evolution

**Goal:** let legitimate observations change a device profile over time.

Know:
- continual/incremental learning;
- catastrophic forgetting;
- replay/basic memory;
- chronological evaluation;
- profile drift;
- rollback;
- frozen evaluation sets.

Maintain frozen evaluation data while a separate chronological stream updates the profile.

Minimum baselines:

A. `Identify -> Update`

B. `Identify -> Confidence threshold -> Update`

C. `Identify -> Reliability/consistency -> Update`

D. candidate security-gated update.

Measure adaptation speed, profile drift, embedding stability, forgetting, legitimate adaptation and update acceptance.

# 13. D9 — Poisoning / Adversarial Protection

**Goal:** determine whether bad observations can silently corrupt a persistent device profile.

Know the difference between:
- inference-time adversarial attack;
- poisoning/training-data attack;
- backdoor attack;
- model corruption;
- profile corruption.

Threat example:

`malicious observation -> accepted as Device A -> incorporated into A profile -> future decisions change`

Use legitimate RF data plus clearly labelled controlled/synthetic poisoning.

Compare A/B/C/D.

Measure:
- attack success;
- profile drift/corruption;
- recognition degradation;
- malicious observations required;
- recovery;
- legitimate false rejection.

# 14. D10 — End-to-End Validation

Connect:

`RF -> preprocessing -> RF evidence -> representation -> identity/open-set -> update-safety -> authorization -> profile evolution -> monitoring`

Demonstrate:
1. normal known-device recognition;
2. unknown-device rejection;
3. legitimate temporal adaptation;
4. profile stability;
5. controlled poisoning;
6. update rejection/quarantine where appropriate;
7. recovery and continued adaptation.

The final question is whether the candidate mechanism improves the security–adaptation trade-off.

# 15. Novelty knowledge

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
> **Treat permission to modify persistent RF identity state as a separate security decision from recognizing the device, and test whether this protects continual profile evolution against poisoning without blocking legitimate adaptation.**

## Important challenge
Prior work already performs related reliability/sample-admission and adaptive-update operations. The project must therefore prove that the **security-oriented separation and explicit update outcome** add value beyond ordinary confidence/reliability filtering.

# 16. Practical Python knowledge

Minimum skills:
- NumPy arrays and complex numbers;
- slicing/reshaping;
- pandas metadata tables;
- pathlib/file handling;
- JSON/YAML configuration;
- matplotlib;
- scikit-learn metrics/baselines;
- PyTorch basics if used;
- random seeds;
- checkpoints;
- experiment logging.

Always verify tensor shape rather than copying assumptions.

# 17. Experiment discipline

Record for every experiment:
- dataset/version;
- exact split;
- preprocessing configuration;
- model configuration;
- random seed;
- training configuration;
- metrics;
- checkpoint;
- result file;
- interpretation;
- decision.

Lifecycle:

`Requirement -> Design -> Implementation -> Test -> Experiment -> Result -> Interpretation -> Decision`

# 18. Learn first when time is limited

### Tier 1 — immediate
1. I/Q data.
2. RF fingerprint concept.
3. dataset metadata/leakage.
4. train/test evaluation.
5. CNN/embedding basics.
6. closed-set vs open-set.
7. temporal/domain shift.
8. continual learning.
9. profile updates.
10. poisoning versus inference-time attack.

### Tier 2 — while implementing
1. synchronization;
2. CFO/RF impairments;
3. metric learning;
4. calibration/uncertainty;
5. replay/forgetting;
6. anomaly detection;
7. attack generation;
8. ablation studies.

### Tier 3 — only if needed
1. advanced domain adaptation;
2. advanced self-supervised learning;
3. sophisticated continual-learning algorithms;
4. advanced adversarial training;
5. hardware/SDR implementation.

# 19. Professor-meeting questions

Be able to answer:
1. What is an RF fingerprint?
2. Where does the fingerprint information come from?
3. Why is carrier frequency alone not the fingerprint?
4. What is I/Q data?
5. How do we know which device produced a training sample?
6. How do we prevent leakage?
7. What is open-set recognition?
8. What changes over time?
9. Why do we need continual learning?
10. What is dangerous about automatic profile updating?
11. Why can correct recognition still be unsafe for learning?
12. What evidence can make an observation suspicious?
13. What existing work is closest?
14. What exactly is different?
15. How will we prove the difference?
16. What result would falsify the novelty claim?

# 20. Learning rule

Do not study the entire field before coding.

`Build -> encounter concept -> learn concept -> implement -> measure -> explain -> document`

The goal is working scientific understanding, not memorization.
