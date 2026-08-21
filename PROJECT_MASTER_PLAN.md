# PROJECT MASTER PLAN

## 1. Project foundation

- Preserve the initial IDP as the origin of the project.
- Maintain the research question, objectives, scope and contribution as controlled project records.
- Maintain a decision log so later changes are traceable.

## 2. Preparation phase

### 2.1 Research and architecture baseline
- Establish the complete software-oriented system architecture.
- Map claims to required evidence and experiments.
- Define interfaces between ingestion, DSP, RF-physics features, representation, identification, open-set recognition, continual learning and poisoning protection.

### 2.2 Dataset strategy
- Maintain the Dataset Requirement Matrix.
- Search existing/public datasets first.
- Qualify datasets against explicit requirements rather than dataset popularity.
- Record dataset quality, provenance, licensing and reproducibility.
- Lock an initial dataset portfolio before substantial model implementation.

## 3. D1–D10 validation framework

### D1 — Raw RF Data / Ingestion
Validate that required raw RF/IQ data can be loaded, interpreted and represented consistently.

### D2 — Synchronization & DSP
Validate required signal-processing operations such as burst extraction, synchronization, filtering and related preprocessing.

### D3 — Physics-Based RF Features
Validate extraction of transmitter/device-relevant RF characteristics and their stability/utility under the defined experimental conditions.

### D4 — Device Representation / Embedding
Develop and evaluate learned representations suitable for device discrimination and later metric/open-set processing.

### D5 — Closed-Set Identification
Establish a baseline for identifying known devices under a defined closed-world protocol.

### D6 — Open-Set Recognition
Evaluate known-vs-unknown device behaviour using a protocol that prevents leakage between known and unknown identities.

### D7 — Robustness / Domain Shift
Evaluate changes caused by acquisition conditions, receiver/domain differences, sessions, environments or other defined shifts.

### D8 — Continual Learning / Profile Evolution
Evaluate controlled profile updates over sequential observations while monitoring stability, forgetting and erroneous updates.

### D9 — Poisoning / Adversarial Protection
Evaluate whether inconsistent or malicious observations can corrupt device profiles and test the defined protection mechanisms.

### D10 — End-to-End Validation
Integrate the validated components and evaluate the complete software pipeline against the project claims.

## 4. Hardware transfer

Hardware is a later validation domain. Software/data validation should not be blocked by requiring an ESP32/SDR capture chain for every stage. Hardware work begins after the relevant software evidence is established.

## 5. Engineering lifecycle

For every component:

`Requirement -> Design -> Implementation -> Unit Test -> Experiment -> Result -> Interpretation -> Decision`

## 6. Research lifecycle

For every research claim:

`Claim -> What must be proven -> Experiment -> Required data -> Dataset search -> Dataset qualification -> Validation -> Conclusion`

## 7. Team workflow

- `main`: stable project state.
- `develop`: integration branch when the team begins multi-branch implementation.
- `feature/*`: member/task branches.
- Pull requests are the normal integration mechanism.
- Issues define work items and preserve accountability.
- Significant research decisions must be recorded in `docs/06_continuity/DECISIONS.md`.

## 8. Completion standard

A phase is complete only when its defined acceptance criteria and evidence exist. Presence of code alone does not constitute validation.
