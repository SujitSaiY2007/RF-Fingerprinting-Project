# Novelty Proof Matrix — Targeted Forensic Audit

**Date:** 2026-08-26  
**Status:** Research-control evidence; not a legal patentability opinion.  
**Scope:** RF/RFFI online adaptation, profile/update admission, poisoning/backdoor impact on future state, closely related trust-aware learning, and relevant patent literature.

## 1. Audit conclusion

The targeted search found an important prior-art complication that materially strengthens the falsification test: **WO2023046581A1 / EP4152223B1 (Nagravision)** explicitly combines RF-device anomaly detection, operational authentication, and post-enrollment model updating. It therefore prevents the project from claiming simply that "RF authentication has never separated security from learning" or that "RF models were not previously updated after authentication."

However, the searched material did **not** reveal an RF/RFFI system whose central mechanism is an independently defined, persistent-profile **update authorization decision** that is distinct from the operational identity/authentication decision and is specifically evaluated as a defense against poisoning of continual profile evolution.

This remains a **potential gap**, not proof of universal novelty.

## 2. Proof matrix

| # | Prior system / work | Representation | Identity / open-set decision | Continual / profile mechanism | Update acceptance / admission | Security / poisoning model | Classification | Exact difference from project |
|---|---|---|---|---|---|---|---|---|
| 1 | **Nagravision, WO2023046581A1 / EP4152223B1, Method and system for authentication of RF device** | I/Q feature data; per-device ML/anomaly model | Model outputs known/unknown; known device may be granted access | Stored per-device model can be updated with new RF data to adapt to environmental conditions | Filtering can remove abnormal short signals; operational model update is described after recognized genuine-device data. No separately specified persistent-profile security authorization gate | Clone/anomaly detection; secure initial enrollment | **Closest prior system** | It already has RF anomaly detection + authentication + online model updating. The project must therefore add a *distinct update-safety decision* whose purpose is to decide whether an observation may alter persistent identity state, with evidence independent of the identity result and tested against profile poisoning. |
| 2 | **Jing et al., 2022, Threshold-free multi-attributes physical layer authentication** | RSSI, CIR, CFO | Binary legal/illegal authentication | Current authentication attributes are recorded as training data for the next authentication | No independent admission gate; the paper assumes previous authentication labels are correct and records attributes regardless of source legitimacy | Spoofing resistance through multiple physical attributes | **Closest academic adjacent prior art** | Strong evidence that authentication and future learning can be coupled. Project differs by explicitly questioning that coupling and adding an independent learning-authorization decision. |
| 3 | **Li et al., 2025, Meta-RFF: Few-Shot Open-Set Incremental Learning for RF Fingerprint Recognition** | Learned RF representation / prototypes | Few-shot open-set recognition | Continual/class-incremental model and prototype evolution | New classes/samples are incorporated by the incremental learning procedure; no security authorization layer | Focus is incremental recognition and forgetting, not poisoning of persistent profiles | **Adjacent prior art** | Shows that open-set + continual RF evolution is established. It does not target malicious observations corrupting a persistent identity profile or separate recognition from learning authorization. |
| 4 | **Li et al., 2025, Open-Set RF Fingerprint Recognition via Fine-Tuning-Based Incremental Learning** | CNN features + classifier/prototypes | Open-set recognition | Incremental fine-tuning for new device classes | Incremental samples/classes are admitted through the learning procedure; no independent security gate | Primarily efficiency/accuracy and forgetting trade-off | **Adjacent prior art** | Same continual/open-set direction, but no independent update-safety authorization or poisoning-focused profile-integrity objective. |
| 5 | **Zhang et al., 2025/2026, Open-Set Few-Shot Class Incremental Learning for SEI** | Learned features + prototype classifier | Prototype-distance open-set recognition | Sustainably evolving prototype classifier with calibration | Unknown signals may be clustered/learned into new categories; admission is part of recognition/learning | Catastrophic forgetting / overfitting, not profile poisoning | **Adjacent prior art** | Prototype evolution is known; the proposed contribution is not prototype evolution itself but a separate security decision controlling whether an observation is allowed to modify persistent state. |
| 6 | **Zhang et al., 2026, Semi-Supervised Cross-Domain Incremental Learning for SEI** | Learned RF features with domain adaptation | Incremental SEI recognition | Semi-supervised cross-domain incremental updates on WiSig; addresses time-varying channels and forgetting | Target-domain samples are used for incremental learning under the proposed method; no separate learning authorization | Domain shift / catastrophic forgetting | **Adjacent prior art** | Demonstrates that real-world RF continual adaptation is active and practical. It does not address malicious profile-state corruption or independent update authorization. |
| 7 | **Xie et al., 2026, Class-incremental open-set RF fingerprints identification based on prototypes extraction and self-attention transformation** | Learned features + prototypes | Open-set + class-incremental identification | Class-incremental RF fingerprint learning | Prototype/class expansion is integrated into the learning method | Recognition under open-set/class-incremental conditions | **Adjacent prior art** | Reinforces that open-set incremental RF recognition is established; no security-gated profile update path was identified. |
| 8 | **Zhao et al., 2025 / IEEE TMC 2026, Data-Free Backdoor Attacks on Pre-Trained Models for RF Fingerprinting** | RF I/Q-derived pretrained representations | Downstream RF fingerprint tasks | Not a continual profile-update system; attacks pretrained model representations | No update-admission mechanism; attack targets model behavior through backdoor implantation | Data-free/protocol-agnostic backdoor attack | **Adjacent security prior art** | Establishes that RF fingerprint model state can be security-sensitive and attackable, but does not solve secure online profile evolution. |
| 9 | **Ma et al., 2025/2026, Adversarial Attacks Against Deep Learning-Based RFFI** | Deep RF fingerprint models | Device identification/authentication | Static model evaluation rather than secure continual profile evolution | No update authorization mechanism | FGSM, PGD, UAP and practical attacks | **Adjacent security prior art** | Supports the threat model but not the proposed update-control mechanism. |
| 10 | **Cao et al., 2025, Adversarial-Driven Experimental Study on Deep Learning for RF Fingerprinting** | Raw received RF signals / DL | RFFI classification | Static/adaptive robustness analysis | Confidence thresholds are discussed as insufficient against some attack behavior | Adversarial/backdoor-like exploitation under domain shift | **Adjacent security prior art** | Particularly relevant because it shows confidence thresholds alone may be insufficient. Project must test this directly rather than assume multi-evidence gating is superior. |
| 11 | **Jing et al., 2022 / CN114727286A, threshold-free multi-attribute PLA patent family** | RSSI/CIR/CFO physical-layer attributes | ML classification authentication | Authentication history is used in subsequent learning | No explicit independent update authorization; authentication result feeds subsequent training data | Spoofing / transmitter imitation | **Patent adjacent prior art** | Shows multi-attribute physical evidence and adaptive authentication are already patented. The project must avoid claiming multi-attribute authentication itself as novel. |
| 12 | **Electronic spectrum-management / device-sensing patent family, e.g. US20240214968A1 and US20240267770A1** | Signal characteristics, profiles, historical/reference data | Device/signal identification with confidence/rating | Stores profile comparisons and updates information/historical data for improved matching | Profile/history updating is described, but no RF fingerprint continual-learning security gate equivalent to the project was identified in the searched material | Spectrum sensing, identification, historical comparison | **Patent adjacent prior art** | Demonstrates that profile-based RF/device identification and historical updating are known. The proposed distinction must remain specifically about security authorization of persistent identity-state learning. |

## 3. Closest-prior forensic finding

### Nagravision patent family is the most important challenge

The 2023 PCT publication **WO2023046581A1**, with priority date 2021-09-21, describes an RF-device authentication method using I/Q-derived fingerprint data and an anomaly-detection model. It explicitly states that the stored model may be updated with newly received RF feature data so that it can adapt to environmental conditions. Its operational flow also filters abnormal feature data, performs the anomaly/known-device decision, grants access to a known device, and then describes further training of the corresponding stored model. Claims include both anomaly-detection model operation and updating the stored model from new RF data.

This prior art therefore covers much of the following chain:

`RF signal -> fingerprint -> anomaly/identity decision -> access decision -> model update`

The searched disclosure does **not** explicitly establish the project's proposed second security decision:

`identity result -> independent update-safety evaluation -> authorization to modify persistent profile`

Nor does it present controlled poisoning of the continual update path as the central security objective.

**Research implication:** the novelty claim must be narrowed from "authentication followed by secure updating" to **independent authorization of persistent identity-state modification, evaluated against adversarial profile corruption while preserving legitimate adaptation**.

## 4. Important academic counterexample

Jing et al. (2022) is particularly useful for the project because it shows the opposite design choice. The authentication receiver records the physical-layer attributes of the current message with its authentication tag as training data for the next authentication, under an assumption that previous labels are correct.

This is close to the problematic pattern:

`authenticate -> trust result -> use result for future learning`

It supports the project's motivation, but it does not prove the proposed solution is novel.

## 5. What is actually differentiated after this audit?

The strongest defensible candidate is now:

> **A continual RF fingerprinting mechanism in which the operational identity decision and the authorization to modify persistent device identity state are explicitly separate decisions, with the latter evaluated from independent consistency evidence and tested as a control against profile poisoning.**

The phrase **"independent consistency evidence"** is important. Simply adding a confidence threshold is not enough, because confidence is still part of the identity decision and can fail in the same conditions as the classifier.

## 6. Falsification requirements

The claim must be rejected or narrowed if any of the following occur:

1. A prior RF system is found that explicitly implements independent update authorization for persistent RF identity profiles.
2. A confidence-only gate matches the proposed gate on security/adaptation metrics.
3. The additional evidence sources are redundant and add no measurable protection.
4. Legitimate adaptation is rejected so frequently that the security gate is operationally unusable.
5. The proposed "persistent profile" is merely a classifier/prototype update with no independently measurable profile-integrity property.

## 7. Legal / patent boundary

This audit is a research prior-art screen, **not** a patentability, freedom-to-operate, infringement, or legal novelty opinion. Patent families, claim scope, prosecution history, jurisdictional status, unpublished applications and non-indexed material require specialist patent searching and legal review before any patent-related claim is made.
