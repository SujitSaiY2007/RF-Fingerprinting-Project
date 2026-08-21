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

The project has four team members. **There is currently no permanent division of the project into four separate technical ownership areas.** All four members are presently working on the **same project workstream: Dataset Search & Validation**, independently at the individual level. Their work may overlap by design because the team is currently exploring and qualifying the dataset space rather than implementing separate modules.

Do not invent or document a fixed member-to-module assignment unless the team explicitly decides to create one later.

## DEC-008 — Integration into `main`

The GitHub integration model is independent of technical ownership. A team member may work on dataset research/qualification, documentation, code, experiments, or another task as the project evolves. Changes should be made through the agreed branch/PR workflow and integrated after review/validation.

`main` represents the stable project state. `develop` is the integration branch. Task/feature branches are used when work needs isolation. During the current dataset-search workstream, separate branches may represent individual dataset investigations even though all four members are working on the same overall topic.

A Pull Request into `develop` should describe the dataset(s), evidence, qualification findings, decision, or other contribution. After integration and appropriate validation, `develop` can be promoted into `main` through a Pull Request. A merge into `main` does **not** mean that a scientific claim is validated; scientific completion still requires the project's experiment/acceptance criteria.
