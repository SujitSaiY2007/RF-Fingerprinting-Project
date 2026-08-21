# PROJECT MASTER PLAN

## 1. Project Definition

Establish the problem, objectives, intended contribution, assumptions, limitations, and success criteria from the initial IDP.

## 2. Architecture Definition

Maintain the complete software pipeline:

RF signal/dataset -> data ingestion -> signal preprocessing -> RF physics features -> device representation -> device identification -> continual learning -> security/poisoning protection -> edge/real-time system.

The physical ESP32/SDR chain is a later hardware-transfer validation domain.

## 3. Dataset Strategy

Use a dataset portfolio rather than forcing one dataset to support every claim.

D1 Raw RF Data / Ingestion
D2 Synchronization & DSP
D3 Physics-Based RF Features
D4 Device Representation / Embedding
D5 Closed-Set Identification
D6 Open-Set Recognition
D7 Robustness / Domain Shift
D8 Continual Learning / Profile Evolution
D9 Poisoning / Adversarial Protection
D10 End-to-End Validation

## 4. Dataset Search & Qualification

For each candidate:

Project claim -> required evidence -> experiment -> required data -> candidate dataset -> qualification -> decision.

Apply the Dataset Qualification protocol and record provenance, license, reproducibility, metadata completeness, rawness, labels, diversity, independence, compatibility, and research value.

## 5. Data Foundation

After qualification, acquire approved datasets externally, create manifests and metadata records, and implement loaders that convert heterogeneous sources into a common internal RF representation.

D1 validation must establish that the selected data can reproduce the planned processing pipeline.

## 6. DSP / Signal Processing

Implement and validate burst extraction, timing alignment, CFO estimation/correction, filtering, normalization, and signal-quality checks.

Do not proceed to ML merely because a loader works; DSP validation must pass its defined experiments.

## 7. RF Physics Features

Investigate measurable transmitter-related features such as CFO, IQ imbalance, EVM, spectral characteristics, and other justified features. Evaluate intra-device stability versus inter-device separation before relying on them in ML.

## 8. Representation Learning

Develop a device representation/embedding model. Prefer independent session/day evaluation rather than random sample splitting where metadata permits.

Candidate metric-learning approaches include triplet loss and supervised contrastive learning, subject to experimental evidence.

## 9. Closed-Set Identification

Establish a baseline known-device identification problem with defensible train/validation/test separation and appropriate metrics.

## 10. Open-Set Recognition

Introduce a known-vs-unknown decision mechanism, threshold selection using validation data, and open-set metrics including FAR, FRR, unknown detection rate, AUROC, AUPR, F1, and threshold sensitivity.

## 11. Robustness / Domain Shift

Evaluate temporal, receiver, distance, environment, SNR, and channel variation only when supported by dataset metadata. Use explicit train/test variation matrices.

## 12. Continual Learning

Compare static and continual models under sequential observations. Measure identity performance over time, profile drift, adaptation speed, false acceptance/rejection, and forgetting.

## 13. Poisoning Protection

Use legitimate sequential RF data plus controlled/synthetic poisoning. Compare an unprotected continual learner against the protected update mechanism. Report poisoning acceptance, profile displacement, identity degradation, legitimate update acceptance, recovery time, and attack effort.

## 14. End-to-End Validation

Integrate the validated components and evaluate on held-out configurations/datasets not used to tune every individual component.

## 15. Hardware Transfer

Only after software/data validation is mature, introduce the intended ESP32/SDR capture chain and evaluate transfer to the physical target environment.

## 16. Edge Deployment

Measure latency, resource use, and operational constraints on the intended edge platform after the algorithmic pipeline has been validated.

## 17. Final Research Package

Maintain reproducible code, dataset provenance, experiment records, metrics, figures, tables, limitations, claims supported by evidence, and final technical documentation.
