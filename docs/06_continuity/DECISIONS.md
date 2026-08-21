# Project Decisions

## DEC-001 — Software-first development

Use existing/public datasets as the primary development and validation substrate. Hardware capture is a later transfer/validation stage.

## DEC-002 — Dataset portfolio

Do not require one dataset to satisfy every project stage. Each selected dataset must have a defined experimental responsibility.

## DEC-003 — Dataset qualification before implementation dependency

A dataset is not accepted merely because it is labelled as RF fingerprinting data. It must be assessed against the requirement and quality criteria.

## DEC-004 — Independent evaluation

Where metadata permits, avoid random sample splits that allow samples from the same session/burst to appear in both training and test data. Prefer session/day/device/receiver holdouts appropriate to the claim.

## DEC-005 — Poisoning evaluation

Use legitimate real RF data plus controlled/synthetic poisoning for the update-security experiment, explicitly labelling the attack evaluation as controlled/synthetic.

## DEC-006 — GitHub as project source of truth

The repository stores project knowledge, decisions, implementation, experiments, results, provenance and continuity. ChatGPT sessions should update the repository state rather than maintaining critical knowledge only in chat history.

## DEC-007 — Current team collaboration model

The project has four team members and no permanent division into technical ownership areas. All four are currently working on Dataset Search & Validation independently; overlap is intentional.

## DEC-008 — Preliminary multi-dataset portfolio

The first evidence-backed qualification pass indicates that a multi-dataset portfolio is necessary. Preliminary KEEP candidates are WiSig, Oregon State WiFi RFFP, Oregon State LoRa RFFP and SMoRFFI. ORACLE and the Bluetooth smartphone database are retained as SECONDARY candidates. These decisions are preliminary and do not constitute final portfolio lock.

## DEC-009 — Same-model coverage is a distinct requirement

Large heterogeneous datasets such as WiSig should not be assumed to prove subtle same-model fingerprinting. A dedicated same-model dataset such as SMoRFFI and/or the Oregon State same-model LoRa dataset is required for that responsibility.

## DEC-010 — No automatic D7/D8 inference from dataset size

Multi-device data does not automatically establish domain-shift or continual-learning suitability. D7 requires verified acquisition/environment/session variation; D8 additionally requires defensible temporal/sequential semantics. These must be directly verified from metadata before qualification.

## DEC-011 — Repository branch-state discrepancy

The current `main` and `develop` refs are diverged. GitHub reports `develop` seven commits ahead and seven commits behind `main`. This conflicts with the intended clean integration relationship and must be reconciled as repository maintenance before relying on `develop` as a clean baseline.
