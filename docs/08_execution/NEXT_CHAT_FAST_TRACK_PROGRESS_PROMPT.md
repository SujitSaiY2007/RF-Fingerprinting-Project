# Next-Chat Fast-Track Continuation Prompt

Copy this entire document into the next ChatGPT session.

## CONTINUATION INSTRUCTION

Continue the RF Fingerprinting Project from:

`SujitSaiY2007/RF-Fingerprinting-Project`

Treat GitHub as the **single canonical source of truth**. Before implementation inspect:

- `PROJECT_STATE.md`
- `CURRENT_OBJECTIVE.md`
- `CURRENT_HANDOFF.md`
- `PROJECT_MASTER_PLAN.md`
- `docs/04_research/novelty_literature_gap_audit.md`
- `docs/04_research/targeted_prior_art_matrix.md`
- `docs/06_continuity/DECISIONS.md`
- `docs/06_continuity/SESSION_LOG.md`
- `docs/07_knowledge_base/RF_FINGERPRINTING_KNOWLEDGE_BASE.md`
- `docs/08_execution/TWO_TRACK_EXECUTION_STRATEGY.md`
- this file

Preserve all prior decisions, evidence, limitations and history.

# 1. Active two-track fast-track position

The immediate objective is to obtain a **small but complete demonstrable implementation covering D1–D10**, without falsely claiming scientific completion.

The active execution model is:

### Track A — Fast Implementation / Demonstration
Build the minimum defensible real-data D1–D10 vertical path as the immediate critical path using **SMoRFFI as the selected working dataset**, subject first to actual package accessibility, metadata and D1 loadability/integrity checks.

SMoRFFI is selected because it is already a qualified real RF fingerprinting dataset with a large same-model device population and is better aligned with the rapid implementation objective than the official ORACLE distribution's large archive download requirement.

The user's uploaded **WiSig ManySig archive is explicitly kept separate from Track A**. Do not make Track A dependent on extracting, re-uploading or processing the ManySig archive unless a later decision deliberately promotes it into the working substrate.

ORACLE is **not** the current Track A dataset. It remains a qualified secondary benchmark and prior ORACLE implementation work is preserved.

Track A must not assume that SMoRFFI alone supports every D7/D8 requirement. Its existing qualification assigns its strongest defined responsibility to D3–D6 and D10, with D7/D8 contingent on package-level metadata verification. If a specific D7/D8 experiment requires variation not present in verified SMoRFFI data, use a qualified Track B dataset for that requirement without allowing it to block the minimum vertical path.

### Track B — Research Validation / Strengthening
Use the preserved ManySig dataset plus Oregon State WiFi, Oregon State LoRa, ORACLE, SMoRFFI broader subsets and other qualified datasets when a concrete experimental, metadata, access/licensing, integrity or reproducibility requirement justifies them. Use Track B for stronger cross-condition/cross-dataset validation, ablations, statistical analysis, failure analysis and support/falsification of the novelty hypothesis.

Detailed policy:
`docs/08_execution/TWO_TRACK_EXECUTION_STRATEGY.md`

This changes execution order and dependency structure only. It does **not** lower the scientific completion standard or remove previous decisions.

## 2. Dataset acquisition and reuse rule

The qualified portfolio remains:

### Primary
1. WiSig
2. Oregon State WiFi RFFP
3. Oregon State LoRa RFFP
4. SMoRFFI

### Secondary
5. ORACLE
6. Bluetooth smartphone RF database

The user's ManySig copy is preserved as a separate acquired dataset for Track B validation/reproduction/cross-checking.

Large raw datasets stay outside Git.

Track A should prefer public datasets that the execution environment can access directly. User-side acquisition is only required when direct programmatic access is unavailable, licensing/terms require it, or the dataset is specifically needed for Track B validation.

Once accepted for a track, preserve raw data unchanged where practical and reuse it through the relevant D1–D10 work. Further acquisition requires a documented need. No open-ended dataset hunt.

## 3. Novelty status — revised after targeted audit

Do **not** claim that an “update gate” is automatically novel.

The targeted audit found:

### Nagravision WO2023046581A1
Already combines RF/IQ authentication, anomaly detection, persistent device models and model updating using new RF observations.

Therefore:

> **RF authentication + adaptive model updating is not our novelty.**

### Liu et al., 2024 — temporal SEI + continual learning
This work processes new observations over time, compares them with preserved feature distributions, identifies **reliable** new signals, adds them to the database and updates the model.

Therefore:

> **Reliable-sample admission before continual updating is also not sufficient novelty by itself.**

### Revised candidate

> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile-poisoning while preserving legitimate adaptation.**

Supporting mechanism:

> **A multi-evidence update-authorization policy using identity confidence together with representation, RF-physical, temporal, historical-profile and anomaly evidence, with the exact policy selected through experimental comparison and ablation.**

This remains a **candidate contribution**, not a proven novelty claim.

## 4. Required novelty proof

Compare at least four policies:

### A — Naive
`Identify -> Update`

### B — Confidence-only
`Identify -> Confidence threshold -> Update`

### C — Reliability/admission baseline
`Identify -> Consistency/reliability check -> Update`

### D — Proposed security-gated policy
`Identify -> Independent security/update-safety evaluation -> Authorization -> Update / Reject / Quarantine`

The decisive comparison is **C versus D**.

Question:

> Does the security-oriented separation protect the persistent profile against controlled poisoning better than ordinary confidence/reliability admission, while preserving legitimate adaptation?

If not, revise or abandon the claim.

## 5. D1–D10 aggressive execution

## D1 — Raw RF Data / Ingestion
Build:
- authoritative source/version references;
- local data-root configuration;
- manifests/checksums;
- metadata schema;
- loader for **SMoRFFI Track A**;
- existing WiSig/Oregon loaders retained for Track B;
- integrity/loadability tests;
- dataset inspection report;
- leakage-safe identifiers.

Minimum normalized record, where available:
- signal reference;
- device ID;
- session ID;
- day/date;
- receiver;
- environment/location;
- channel/frequency;
- source dataset;
- raw shape/dtype;
- preprocessing status.

Acceptance: another team member can reproduce the ingestion after setting one local data-root configuration.

Track A establishes minimum D1 evidence first on SMoRFFI. Track B broadens D1 evidence with ManySig and other datasets when justified.

## D2 — Synchronization & DSP
Build a deterministic minimum chain:

`raw I/Q -> validity -> burst/sample selection -> synchronization/alignment -> normalization -> model-ready tensor`

Keep raw data untouched.

Evidence:
- before/after plots;
- output-shape checks;
- preprocessing configuration;
- reproducibility test.

## D3 — Physics-Based RF Evidence
Start with a small interpretable feature set, depending on dataset support:
- CFO-related feature;
- amplitude statistics;
- phase/frequency statistics;
- spectral characteristics;
- I/Q imbalance-related measurements;
- transient characteristics.

Do not claim these as novel.

Measure device discrimination and sensitivity to time/receiver/environment.

## D4 — Device Representation / Embedding
Use a simple baseline such as a lightweight 1D CNN.

Output:
1. classifier prediction;
2. embedding vector.

Check:
- training/validation curves;
- embedding shape;
- within-device vs between-device distances;
- simple visualization if useful.

Avoid complex architectures unless a documented failure justifies them.

## D5 — Closed-Set Identification
Train known-device baseline.

Evaluate:
- accuracy;
- precision/recall/F1;
- confusion matrix;
- confidence distribution.

Use leakage-safe splits.

This becomes the identity model used downstream.

## D6 — Open-Set Recognition
Hold out some devices completely from training.

Start with:
- confidence threshold;
- embedding/prototype distance;
- or both.

Evaluate known acceptance, unknown rejection and threshold sensitivity.

Do not claim open-set recognition as novelty.

## D7 — Robustness / Domain Shift
Create a shift matrix using at least one available change:
- day/session;
- receiver;
- environment/location;
- SNR/channel condition.

For SMoRFFI, **verify package-level metadata first**. Do not fabricate a D7 shift from information the dataset does not actually provide. If SMoRFFI lacks a suitable shift dimension, use a qualified Track B dataset for D7.

Measure performance degradation.

Use this to demonstrate why adaptation is needed.

Do not prematurely build sophisticated test-time adaptation.

## D8 — Continual Learning / Profile Evolution
Create a simple chronological profile per device containing, at minimum:
- embedding prototype/statistics;
- accepted observation count;
- temporal summary;
- optional RF-feature statistics;
- update history.

Implement:

A. `Identify -> Update`

B. `Identify -> Confidence -> Update`

C. `Identify -> Reliability/Consistency -> Update`

D. candidate security-gated update.

Maintain a **frozen evaluation set** that is never used for profile updates.

If SMoRFFI package metadata cannot support a defensible chronological D8 protocol, use a qualified Track B dataset for that experiment rather than inferring chronology.

Measure:
- adaptation speed;
- profile drift;
- embedding stability;
- forgetting;
- legitimate adaptation;
- update acceptance/rejection.

## D9 — Poisoning / Adversarial Protection
Threat model:

`malicious/abnormal observation -> accepted as Device A -> incorporated into A profile -> future decisions change`

Use legitimate RF data plus clearly labelled controlled/synthetic poisoning.

Start with a reproducible simple attack such as controlled perturbation, interpolation or feature-space displacement. Do not optimize for attack sophistication first.

Compare A/B/C/D.

Measure:
- profile corruption;
- attack success;
- malicious observations required;
- recognition degradation;
- recovery;
- legitimate false rejection.

## D10 — End-to-End Validation
Integrate:

`RF -> DSP -> RF evidence -> embedding -> identity -> open-set -> shift assessment -> update-safety -> authorization -> update/reject/quarantine -> monitoring`

Demonstrate:

1. normal Device A recognition + legitimate profile update;
2. unknown-device rejection;
3. legitimate temporal change + adaptation;
4. suspicious Device A observation recognized operationally but rejected for profile update;
5. controlled poisoning attempt + policy comparison;
6. recovery after rejection/quarantine.

The central demonstration should be:

> **“The system recognizes the device, but does not automatically trust the observation as learning material.”**

## 6. Aggressive implementation rules

1. Simple baselines before SOTA.
2. Every stage produces an artifact or measurable result.
3. Never call a placeholder “complete.”
4. Label controlled/synthetic attacks clearly.
5. Never commit large raw datasets.
6. Avoid hard-coded machine paths.
7. Record seeds/configuration.
8. Avoid random splits when session/burst leakage is possible.
9. Keep frozen evaluation isolated from profile updates.
10. Preserve meaningful results in GitHub.
11. Record failures instead of silently replacing methods.
12. Use the knowledge base as the learning checklist.
13. Do not let large dataset acquisition block the minimum vertical implementation.
14. Add further data only when a concrete validation requirement is documented.
15. Preserve the distinction between implementation/demo evidence and scientific validation.
16. Keep ManySig separate from Track A unless a later explicit decision promotes it.
17. Do not treat dataset download convenience alone as sufficient scientific justification for Track A selection.

## 7. Repository outputs expected

Maintain as the project grows:

- D1 manifests/ingestion/tests;
- D2 preprocessing/tests;
- D3 RF-feature extraction;
- D4 baseline model/embedding;
- D5 closed-set evaluation;
- D6 open-set evaluation;
- D7 shift evaluation;
- D8 profile store/update logic;
- D9 controlled poisoning/evaluation;
- D10 integrated pipeline;
- experiment configs/results;
- decision records;
- novelty evidence;
- limitations/failure records.

## 8. Research-control updates

When evidence changes the scientific position, update:

- `PROJECT_STATE.md`
- `CURRENT_OBJECTIVE.md`
- `CURRENT_HANDOFF.md`
- `PROJECT_MASTER_PLAN.md`
- `docs/04_research/novelty_literature_gap_audit.md`
- `docs/04_research/targeted_prior_art_matrix.md`
- `docs/06_continuity/DECISIONS.md`
- `docs/06_continuity/SESSION_LOG.md`

Use the documented task/research branch -> PR -> develop -> review -> PR -> main workflow. Do not force-reset history.

## 9. First actions in the next chat

1. Inspect the canonical repository state.
2. Confirm current branch comparison.
3. Read the targeted prior-art matrix.
4. Read the knowledge base.
5. Read `docs/08_execution/TWO_TRACK_EXECUTION_STRATEGY.md`.
6. Inspect which D1–D10 code/evidence already exists.
7. Do not restart dataset qualification.
8. Verify **SMoRFFI Track A** package accessibility, actual data files and metadata using the existing qualification gate.
9. Begin/continue the Track A D1 implementation immediately using SMoRFFI.
10. Keep ManySig and Track B acquisition/validation separate so they do not block Track A.
11. After each meaningful stage, update evidence and continuity records.

## 10. Fast-track success condition

The fast-track is successful when the repository contains a reproducible demonstration of:

`RF observation -> device recognition -> independent learning-safety decision -> authorized update or rejection`

and the result is compared against automatic and confidence/reliability-based updating.

The conclusion may support, weaken, equalize, or falsify the novelty hypothesis. Follow the evidence.

## SUPERSEDING DATASET DECISION — 2026-08-29
**DEC-028 supersedes the earlier ORACLE Track A selection. SMoRFFI is the current Track A working dataset.**

Do not select ORACLE again unless a new explicit project decision changes Track A. Do not treat this selection as D1–D10 scientific validation. Verify SMoRFFI access, package structure, metadata and loadability first. Preserve all prior decisions and the qualified portfolio.
