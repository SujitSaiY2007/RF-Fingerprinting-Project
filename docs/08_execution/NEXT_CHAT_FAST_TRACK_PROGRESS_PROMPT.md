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
- this file

Preserve all prior decisions, evidence, limitations and history.

# 1. Fast-track project position

The immediate objective is to obtain a **small but complete demonstrable implementation covering D1–D10**, without falsely claiming scientific completion.

The principle is:

> **Build the smallest defensible end-to-end system first, then strengthen it.**

Do not over-engineer a stage before the complete path exists.

The qualified datasets remain:

### Primary
1. WiSig
2. Oregon State WiFi RFFP
3. Oregon State LoRa RFFP
4. SMoRFFI

### Secondary
5. ORACLE
6. Bluetooth smartphone RF database

First development pair:

**WiSig + Oregon State WiFi RFFP.**

Large raw datasets stay outside Git.

# 2. Novelty status — revised after targeted audit

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

# 3. Required novelty proof

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

# 4. D1–D10 aggressive execution

## D1 — Raw RF Data / Ingestion
Build:
- authoritative source/version references;
- local data-root configuration;
- manifests/checksums;
- metadata schema;
- WiSig loader;
- Oregon State WiFi loader;
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

# 5. Aggressive implementation rules

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

# 6. Repository outputs expected

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

# 7. Research-control updates

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

# 8. First actions in the next chat

1. Inspect the canonical repository state.
2. Confirm current branch comparison.
3. Read the targeted prior-art matrix.
4. Read the knowledge base.
5. Inspect which D1–D10 code/evidence already exists.
6. Do not restart dataset qualification.
7. Begin D1 implementation immediately.
8. After each meaningful stage, update evidence and continuity records.

# 9. Fast-track success condition

The fast-track is successful when the repository contains a reproducible demonstration of:

`RF observation -> device recognition -> independent learning-safety decision -> authorized update or rejection`

and the result is compared against automatic and confidence/reliability-based updating.

The conclusion may support, weaken, equalize, or falsify the novelty hypothesis. Follow the evidence.
