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
