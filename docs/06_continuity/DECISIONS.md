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

The project has four team members. There is currently no permanent division of the project into four separate technical ownership areas. All four members are presently working on the same project workstream: Dataset Search & Validation, independently at the individual level. Do not invent a fixed member-to-module assignment.

## DEC-008 — Integration into main

A merge into `main` is a repository integration event, not scientific validation. `main` is the stable state; `develop` is the integration branch; task/research branches provide isolation and attribution.

## DEC-009 — Dataset portfolio qualification gate

As of 2026-08-21, the dataset search/qualification workstream has produced a sufficiently complementary development-substrate portfolio to begin D1. Primary KEEP datasets are WiSig, Oregon State WiFi RFFP, Oregon State LoRa RFFP and SMoRFFI. ORACLE and the Bluetooth smartphone database remain SECONDARY. This decision does not certify D1–D10 and may be reopened if package-level ingestion or experimentation exposes a material contradiction.

## DEC-010 — No open-ended dataset hunt before D1

After the initial portfolio qualification, additional dataset search is no longer the default next action. Search should resume only in response to a specific experimental, reproducibility, licensing/access or metadata gap. The next gate is D1 implementation and validation.

## DEC-011 — Continual-learning dataset caveat

No public dataset is currently treated as automatically proving D8. Repeated days/sessions provide candidate observations, but the project must construct and validate a chronological update protocol with a frozen evaluation population, profile acceptance criteria and rollback protection.
