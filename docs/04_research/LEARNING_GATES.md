# Project Learning Gates

## Purpose
The project now treats technical understanding as a parallel gate to engineering completion. The repository records what the researcher should understand before each D-stage is considered knowledge-complete.

## Operating rule
Each stage has two linked tracks:
1. Engineering: implementation, testing, demonstration and scientific evidence as applicable.
2. Learning: required technical concepts and demonstrated understanding.

A stage may be implemented while its learning gate is still open. It must not be represented as fully knowledge-complete until the corresponding learning gate is passed.

Learning is assessed by understanding and application, not by hours watched or course completion. The researcher should be able to explain the concept, interpret it in project data, explain why it matters, and identify important failure modes.

## Learning layers

### Layer 1 — Mathematical and data foundations
- Complex numbers and complex arithmetic
- Magnitude, phase and conjugates
- Vectors and basic matrix concepts
- Probability and random variables
- Mean, variance, standard deviation and distributions
- Basic statistical reasoning
- Dataset/sample/label/feature concepts

### Layer 2 — Signals, I/Q and preprocessing
- Continuous vs discrete signals
- Sampling and sampling rate
- Nyquist limit and aliasing
- Time-domain representation
- Frequency-domain representation
- Fourier transform, DFT and FFT concepts
- Basic filtering and convolution intuition
- I/Q representation and complex baseband
- Signal magnitude and phase
- Normalization/scaling
- Data leakage and deterministic preprocessing

### Layer 3 — Wireless/RF fundamentals
- RF/baseband/passband concepts
- Transmitter, receiver, channel and ADC/DAC roles
- Modulation fundamentals
- OFDM at conceptual level
- Noise and SNR
- Bandwidth and carrier frequency
- Common RF impairments: CFO, phase noise, IQ imbalance, nonlinearities and transient effects
- RF feature extraction intuition

### Layer 4 — Machine learning and learned representations
- Supervised classification
- Features, labels and model inputs
- Train/validation/test methodology
- Overfitting, underfitting and generalization
- Loss functions and optimization
- Logistic regression, k-NN, tree/ensemble and SVM intuition
- Neural networks and backpropagation
- CNN/1-D CNN concepts
- Embeddings and representation learning
- Tensor/Dataset/DataLoader/model/training concepts in PyTorch

### Layer 5 — Evaluation and experimental methodology
- Accuracy, precision, recall, F1 and confusion matrices
- Per-class performance
- Reproducibility and random seeds
- Leakage-safe partitioning
- Distribution shift and confounding
- Baselines, ablations and controlled comparisons
- Statistical uncertainty and confidence intervals at an appropriate level

### Layer 6 — Open-set and adaptation concepts
- Closed-set vs open-set recognition
- Unknown-device rejection
- Decision thresholds and confidence
- Domain shift
- Temporal variation
- Receiver/environment variation
- Incremental and continual learning
- Online learning and test-time adaptation

### Layer 7 — Persistent profiles and security
- Device embeddings/prototypes
- Persistent identity profiles
- Profile evolution
- Recognition vs authorization-to-update separation
- Update admission policies
- Threat models
- Poisoning and profile corruption
- Adversarial manipulation and backdoor intuition
- Security-oriented evaluation

## Stage-to-learning-gate map

| Stage | Required learning gate before stage is knowledge-complete |
|---|---|
| D1 | Layer 1 foundations + dataset/data provenance concepts |
| D2 | Layers 1–2; emphasis on complex signals, I/Q, sampling, FFT, normalization and leakage |
| D3 | Layers 1–3; add RF/wireless fundamentals, modulation, noise/SNR and RF impairments |
| D4 | Layers 1–4; add ML, neural networks, CNNs, embeddings and PyTorch concepts |
| D5 | Layers 1–5; add evaluation, experimental design, baselines and reproducibility |
| D6 | Layers 1–6; add open-set recognition, rejection and unknown-device reasoning |
| D7 | Layers 1–6; specifically demonstrate understanding of temporal/domain/receiver/environment shift |
| D8 | Layers 1–7; specifically demonstrate continual learning, profile evolution and update authorization |
| D9 | Layers 1–7; specifically demonstrate threat models, poisoning and profile-corruption evaluation |
| D10 | All layers relevant to the implemented system; demonstrate end-to-end technical and methodological understanding |

## Current learning state — 2026-08-29
- Project engineering state: **D2.1 complete; D2.2 next**.
- Researcher learning state: **Learning Phase — D2 gate open**.
- Current target: **Layer 1 → Layer 2**, beginning with complex numbers and I/Q representation, followed by sampling, discrete signals, Fourier/FFT, statistics/normalization and leakage.
- The D2 engineering workflow may continue while this learning gate is open, but D2 knowledge completion requires the corresponding concepts to be understood and checked.

## Learning-check protocol
For each gate, the project workflow should use short concept checks and project-linked exercises rather than passive course completion. A gate is considered understood when the researcher can:
1. explain the concept in their own words;
2. solve or interpret a small technical example;
3. connect it to the current project stage; and
4. identify at least the major methodological mistake or failure mode associated with it.

## Relationship to external learning resources
External courses, lectures and documentation are learning resources, not project authority. The repository records the concepts and the project's application of them; external material supplies the underlying theory.

## Important boundary
The learning gate is not a substitute for engineering or scientific acceptance. Passing a learning gate does not imply that an experimental result is valid; conversely, an implemented stage does not imply that the researcher has mastered its technical basis.
