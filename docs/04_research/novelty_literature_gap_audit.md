# Novelty & Literature Gap Audit — Q2/Q4

**Status:** Preliminary research record; novelty is NOT yet finalized.

**Date:** 2026-08-25

**Purpose:** Record the literature-driven refinement of the project's proposed novelty before downstream representation/continual-learning implementation. This document is the canonical research record for the current novelty hypothesis.

## 1. Research question from the progress meeting

The professor's Question 2 is treated as a novelty-design question connected to Question 4:

> What is genuinely different about this project, where will that difference be implemented, and how can the claim be defended against existing solutions?

The initial decomposition is:

1. Representation
2. Decision making
3. Security

The project must not call a component novel merely because it is included in the pipeline.

## 2. Literature review conclusion so far

The first broad literature audit shows that several originally suspected novelty claims are already established research areas. Therefore they are treated as **enabling components**, not standalone novelty claims.

| Candidate idea | Current assessment | Project treatment |
|---|---|---|
| RF fingerprinting + deep learning | Established | Baseline/component |
| Learned RF device embeddings | Established | D4 component |
| Physics-informed RF representation | Existing research direction | D3/D4 component; not standalone novelty |
| Open-set RF fingerprint recognition | Established and active | D6 component |
| Prototype/embedding-based unknown-device decision | Established | D4/D6 component |
| Incremental/continual RF fingerprint learning | Existing research direction | D8 component |
| Physics-aware temporal/test-time adaptation | Existing recent work | D7/D8 component; not standalone novelty |
| Open-set + incremental RF learning | Existing recent work | Baseline to compare against |
| Generic adversarial robustness of RF fingerprinting | Existing research direction | D9 baseline/security context |
| Historical device profiling | Existing concept | D8 component |
| **Separate authorization of profile updates from identity recognition** | **Potential research gap; requires targeted audit** | **Primary novelty candidate** |
| **Multi-evidence secure update gate for continual RF profile evolution** | **Potential research gap; requires targeted audit and experiments** | **Primary/secondary novelty candidate** |
| Integrated physics + representation + open-set + continual evolution + update security | Potential system-level contribution, but only if differentiated experimentally | Candidate integrated contribution |

## 3. Evidence that invalidates weaker novelty claims

### 3.1 Physics-informed representation is not sufficient novelty

Recent work already investigates physical-information-aware RF fingerprint representations and temporal adaptation. In particular, RFF-TTA (AAAI 2026) explicitly uses physical impairment information, including CFO-related information, to construct physically informed prototypes for temporally varying RF fingerprinting and performs online test-time adaptation.

Source:
- AAAI 2026, *RFF-TTA: Physical Information-Aware Prototype for Temporally Varying RF Fingerprinting Online Test-Time-Adaptation*:
  https://ojs.aaai.org/index.php/AAAI/article/view/37034/40996

**Decision:** Do not claim "physics-aware representation" alone as the project's novelty.

### 3.2 Open-set RF fingerprinting is established

Existing work includes improved prototype learning for open-set RF fingerprint identification, HiNoVa for open-set RF device detection, Siamese/comparison approaches, and newer prototype/reconstruction/open-set methods.

Representative sources:
- *Open-Set RF Fingerprinting via Improved Prototype Learning* (2023):
  https://arxiv.org/abs/2306.13895
- HiNoVa (2023):
  https://arxiv.org/abs/2305.09594
- Recent multi-task prototype/open-set RFFI work:
  https://www.mdpi.com/1424-8220/25/17/5415

**Decision:** Do not claim unknown-device recognition or prototype-based open-set decision as standalone novelty.

### 3.3 Incremental/continual RF fingerprint learning is established

RF fingerprint identification has prior incremental-learning research. More recent work such as Meta-RFF combines few-shot, open-set and incremental/continual RF fingerprint recognition.

Representative sources:
- *Incremental Learning for Radio Frequency Fingerprint Identification* (2021):
  https://www.semanticscholar.org/paper/4c916c37e68d9accd5ade6c24431129f2970554c
- Meta-RFF:
  https://www.zhenyu.info/papers/Meta-RFFJ.pdf

**Decision:** Do not claim continuous/incremental RF device learning alone as novelty.

### 3.4 Generic adversarial robustness is established

RF fingerprinting systems have been studied under adversarial manipulation, and recent work includes backdoor attacks against RF fingerprinting models.

Representative sources:
- RF fingerprinting challenges/opportunities review:
  https://pure.tue.nl/ws/portalfiles/portal/343587032/Radio_Frequency_Fingerprinting_via_Deep_Learning_Challenges_and_Opportunities.pdf
- Recent RF fingerprinting backdoor work:
  https://livrepository.liverpool.ac.uk/3195117/

**Decision:** Do not claim "security against adversarial attacks" generically as novelty.

## 4. Potential research gap

The stronger candidate is not merely recognizing a device, adapting a model, or resisting an inference-time attack. The candidate gap is the **security of the continual profile-update pathway itself**.

### Existing conceptual flow

`Observation -> Identity decision -> Profile update`

The concern is that a sample can be classified as a known device while still being unsafe to incorporate into that device's persistent profile.

### Proposed research flow

`Observation -> Identity decision -> Independent update-safety assessment -> Update authorization -> Profile evolution`

The key conceptual separation is:

> **Identification correctness is not equivalent to authorization to modify the persistent device profile.**

An observation could therefore be:

- accepted for identity/authentication;
- rejected for profile update;
- flagged for security analysis;

without treating those outcomes as contradictory.

## 5. Candidate secure update gate

The project will investigate whether profile-update authorization can use multiple independent evidence sources:

- identity confidence;
- embedding-space consistency;
- physics-feature consistency;
- temporal consistency;
- historical profile consistency;
- anomaly/deviation evidence.

A conceptual update score is:

`T_update = f(identity confidence, physics consistency, embedding consistency, temporal consistency, profile consistency, anomaly evidence)`

and a conceptual policy is:

`Update profile iff T_update >= tau_update`

This formula is a **research hypothesis**, not a frozen implementation specification.

## 6. Why this is potentially stronger

The proposed mechanism addresses a lifecycle-level question:

> Can a continuously learning RF fingerprinting system evolve device profiles without allowing anomalous or adversarial observations to silently corrupt those profiles?

This connects D8 and D9 rather than treating continual learning and poisoning protection as completely independent capabilities.

## 7. What is NOT being claimed

At this stage the project does **not** claim that:

- no prior paper has used a trust/update gate;
- the proposed update gate is patentable;
- the proposed mechanism is publication-novel;
- the proposed scoring function is new;
- physics-informed embeddings are new;
- open-set RF fingerprinting is new;
- continual RF fingerprint learning is new.

A targeted literature audit is still required before converting the candidate gap into a formal novelty claim.

## 8. Required targeted Q4 audit

The next literature review must focus specifically on whether prior RF/RFFI systems explicitly separate:

1. identity recognition;
2. confidence/consistency assessment;
3. authorization to modify a persistent device profile;
4. protection of that update path against poisoning or anomalous observations.

The review should compare at least:

- RF fingerprinting papers;
- continual/incremental RF learning papers;
- RF adversarial/poisoning papers;
- profile-based RF authentication systems;
- closely related continual-learning security literature where RF-specific evidence is absent.

For each paper, record:

- representation method;
- decision method;
- open-set handling;
- adaptation/profile mechanism;
- update acceptance mechanism;
- poisoning/adversarial model;
- whether recognition and learning authorization are explicitly separated;
- exact difference from this project.

## 9. Experimental implication

If the targeted audit supports the gap, the project should eventually construct controlled experiments comparing at least:

### Baseline A — automatic update
`Identify -> Update`

### Baseline B — existing confidence-based update
`Identify -> confidence threshold -> Update`

### Candidate system — secure update gate
`Identify -> multi-evidence consistency -> update authorization -> Update/Reject`

The poisoning experiment should use legitimate RF data plus controlled/synthetic poisoning, consistent with DEC-005. Results must measure both normal adaptation and profile-corruption resistance.

## 10. Relationship to D1-D10

- D3: establish the physical RF evidence used by the later update gate.
- D4: establish the device representation/embedding and its geometry.
- D5: establish known-device identification baseline.
- D6: establish unknown-device/open-set baseline.
- D7: measure behaviour under temporal/receiver/environment/domain shifts.
- D8: implement and evaluate chronological profile evolution.
- D9: evaluate controlled/synthetic poisoning and the update-security mechanism.
- D10: evaluate the integrated lifecycle.

D1 remains the current engineering gate and must not be declared complete from this research record.

## 11. Current novelty position

**Primary candidate:**

> **Secure continual RF device-profile evolution through explicit separation of identity recognition from authorization to modify the persistent device profile.**

**Supporting candidate:**

> **A multi-evidence update authorization mechanism combining representation, RF-physical, temporal and historical-profile consistency before allowing continual profile modification.**

**System-level candidate:**

> **An experimentally validated RF fingerprinting lifecycle that integrates physics-based evidence, learned representations, open-set recognition, continual profile evolution and security-gated updates, with the novelty claim centered on the secure update pathway rather than any individual component.**

These are **working hypotheses**, not final novelty claims.

## 12. Finalization criterion

The novelty claim may be promoted from "candidate" to "project contribution" only after:

1. targeted literature audit is completed;
2. nearest prior systems are explicitly mapped;
3. a measurable difference is identified;
4. an experiment is defined that can falsify the claimed advantage;
5. the selected datasets can support that experiment;
6. D8/D9 evidence demonstrates the proposed behaviour.

Until then, the repository should describe the secure update pathway as a **research hypothesis / candidate contribution**.
