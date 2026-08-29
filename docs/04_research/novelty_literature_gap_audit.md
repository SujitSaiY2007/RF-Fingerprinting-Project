# Novelty & Literature Gap Audit — Q2/Q4 + Targeted Forensic Update

**Status:** Preliminary-to-targeted research record; novelty is **NOT finalized**.  
**Initial audit:** 2026-08-25  
**Targeted update:** 2026-08-29

## 1. Research question from the progress meeting

> What is genuinely different about this project, where will that difference be implemented, and how can the claim be defended against existing solutions?

The project must not call a component novel merely because it appears in the pipeline.

## 2. Broad audit conclusion

The following are established or active research areas and are treated as enabling components/baselines:

| Candidate idea | Current assessment | Project treatment |
|---|---|---|
| RF fingerprinting + deep learning | Established | Baseline/component |
| Learned RF device embeddings | Established | Representation component |
| Physics-informed RF representation | Existing research direction | RF-evidence/representation component |
| Open-set RF fingerprint recognition | Established and active | Open-set component |
| Prototype/embedding-based unknown-device decision | Established | Open-set baseline |
| Incremental/continual RF fingerprint learning | Established/active | Profile-evolution component |
| Physics-aware temporal/test-time adaptation | Existing recent work | Robustness/adaptation component |
| Adaptive RF model/profile updating | Existing | Baseline capability |
| Generic adversarial/backdoor robustness | Existing research direction | Security baseline/context |
| Historical device profiling | Existing concept | Profile component |
| Reliability/sample selection before learning | Existing in adjacent RF/SEI work | Admission baseline |
| Security-specific separation of recognition from persistent-state update authorization | Potential gap | Primary candidate; requires proof |

## 3. Critical prior-art boundaries discovered in targeted audit

### 3.1 Nagravision — WO2023046581A1

The patent describes RF-device authentication using I/Q-derived RF data, anomaly detection, stored per-device models and updating a stored model with new RF observations to adapt to environmental conditions.

This is a critical boundary because it already covers the broad pattern:

`RF observation -> authentication/anomaly decision -> persistent model -> adaptive update`

**Decision:** Do not claim RF authentication + adaptive model updating as novel.

Source:
https://patents.google.com/patent/WO2023046581A1/en

### 3.2 Liu et al. — Specific emitter identification unaffected by time through adversarial domain adaptation and continual learning (2024)

This work addresses temporal changes in emitter fingerprints using domain adaptation and continual learning. New observations are compared with preserved feature distributions; reliable new signals are identified, labeled, added to the database and used for model updating.

This is the strongest academic challenge to a simple “we check whether an observation is reliable before updating” claim.

**Decision:** Reliability/sample admission before continual RF updating is not sufficient novelty by itself.

Source:
https://doi.org/10.1016/j.engappai.2024.109324

### 3.3 Online/adaptive physical-layer authentication

Prior physical-layer authentication research already uses multiple attributes and online learning/adaptation in dynamic environments.

Representative sources:
- https://doi.org/10.1177/15501329221107822
- https://doi.org/10.1109/TNSE.2020.3013232
- https://www.sciencedirect.com/science/article/pii/S1570870522000634

**Decision:** Multi-evidence authentication and online adaptation are not standalone novelty.

### 3.4 RF backdoor/security literature

RF fingerprinting models have been shown to be vulnerable to backdoor attacks, including model-agnostic and data-free attacks.

Representative sources:
- https://doi.org/10.1109/INFOCOM52122.2024.10621289
- https://doi.org/10.1109/INFOCOM55648.2025.11044704
- https://doi.org/10.1109/TMC.2025.3628527

**Decision:** Generic RF model security is not standalone novelty. It provides the threat/security context for the profile-update experiment.

### 3.5 RFF-TTA and recent RF adaptation

RFF-TTA (AAAI 2026) uses physical impairment information and online test-time adaptation for temporally varying RF fingerprint recognition.

Source:
https://doi.org/10.1609/aaai.v40i1.37034

**Decision:** physical RF evidence + temporal adaptation are enabling components, not standalone novelty.

## 4. Revised candidate research gap

The stronger candidate is not:

- recognizing a device;
- adapting a model;
- selecting reliable samples;
- detecting anomalies;
- resisting a generic inference-time attack.

The candidate gap is the **security of the continual persistent-profile update pathway**.

### Broad existing patterns

`Observation -> Identity decision -> Update`

or, in some prior work:

`Observation -> Reliability/consistency selection -> Update`

### Candidate project pattern

`Observation -> Identity decision -> Independent security/update-safety assessment -> Update authorization -> Update / Reject / Quarantine`

The key distinction is:

> **A correct identity decision does not automatically authorize persistent learning from that observation.**

The intended system may therefore produce:

`Operational identity = Device A`

while simultaneously producing:

`Profile-update authorization = REJECT`

This explicit two-outcome behaviour is the central thing that must be demonstrated and compared against prior admission strategies.

## 5. Candidate multi-evidence mechanism

The project will investigate whether update authorization can use:

- identity confidence;
- embedding-space consistency;
- RF-physical consistency;
- temporal consistency;
- historical-profile consistency;
- anomaly/deviation evidence.

Conceptually:

`UpdateSafety = f(identity, embedding, physical RF, temporal, profile history, anomaly)`

The exact function, weights and thresholds are **not frozen**.

The correct approach is to compare simple policies first and use ablation to determine whether each evidence source adds value.

## 6. Required proof experiment

The minimum comparison is:

### Baseline A — Naive update
`Identify -> Update`

### Baseline B — Confidence-only update
`Identify -> Confidence threshold -> Update`

### Baseline C — Reliability/consistency admission
`Identify -> Consistency/Reliability -> Update`

### Candidate D — Security-gated update
`Identify -> Independent security/update-safety evaluation -> Authorization -> Update / Reject / Quarantine`

The decisive comparison is **C versus D**.

### Normal adaptation metrics
- identification accuracy;
- open-set rejection;
- adaptation speed;
- temporal/domain robustness;
- profile drift;
- embedding stability;
- forgetting;
- legitimate adaptation.

### Security metrics
- poisoning/profile-corruption success;
- malicious observations required;
- attack success;
- recovery after rejection/quarantine;
- recognition degradation;
- false rejection of legitimate observations.

## 7. Falsification rules

The candidate novelty must be modified or abandoned if:

- a close RF-specific prior system is found with the same security-specific separation;
- the reliability/admission baseline performs equally well;
- additional evidence does not materially reduce profile corruption;
- the gate blocks legitimate adaptation excessively;
- the claimed separation cannot be measured independently;
- the result is only a repackaging of an existing trust/admission mechanism.

## 8. What the project is NOT claiming

At this stage the project does not claim:

- no prior paper has used an update/admission gate;
- no RF system has ever separated recognition from learning;
- the candidate is patentable;
- the candidate is definitely publication-novel;
- the candidate scoring function is new;
- physics-informed RF features are new;
- open-set RF recognition is new;
- continual RF learning is new;
- adaptive RF model updating is new.

## 9. Targeted prior-art matrix

The detailed 12-system comparison is maintained separately at:

`docs/04_research/targeted_prior_art_matrix.md`

It records representation, identity decision, open-set handling, adaptation/profile mechanism, update admission, security model, classification and exact difference.

## 10. Relationship to D1–D10

- D1: establish trustworthy RF data foundations.
- D2: establish reproducible preprocessing.
- D3: establish physical RF evidence.
- D4: establish learned representation/embedding.
- D5: establish known-device identity baseline.
- D6: establish unseen-device/open-set baseline.
- D7: establish temporal/receiver/environment shift evidence.
- D8: establish chronological profile evolution and update-policy baselines.
- D9: evaluate controlled/synthetic poisoning of the profile-update pathway.
- D10: evaluate the integrated lifecycle.

D1 remains the first engineering implementation gate, but the project is now using an accelerated vertical implementation strategy after the minimum D1 evidence is established.

## 11. Current novelty position

### Primary candidate
> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile-poisoning while preserving legitimate adaptation.**

### Supporting candidate
> **A multi-evidence update-authorization policy combining identity confidence, representation, RF-physical, temporal, historical-profile and anomaly consistency before allowing persistent profile modification.**

### System-level candidate
> **An experimentally evaluated RF fingerprinting lifecycle that integrates recognition, open-set handling, continual profile evolution and security-gated profile updates, with the contribution centered on the security of the persistent update pathway rather than on any individual RF/ML component.**

These remain working hypotheses.

## 12. Finalization criterion

Promote the candidate from “research hypothesis” to “project contribution” only when:

1. nearest prior systems are mapped;
2. the exact difference is explicit;
3. the difference is not already implemented in a close RF-specific system;
4. a falsifiable experiment exists;
5. suitable datasets support it;
6. D8/D9 evidence shows a measurable security–adaptation advantage.

Until then, describe the contribution as **provisional**.
