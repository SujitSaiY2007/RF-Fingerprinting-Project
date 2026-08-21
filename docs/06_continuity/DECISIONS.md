# Project Decisions

## DEC-001 — Software-first development
Use existing/public datasets as the primary development and validation substrate. Hardware capture is a later transfer/validation stage.

## DEC-002 — Dataset portfolio
Do not require one dataset to satisfy every project stage. Each selected dataset must have a defined experimental responsibility.

## DEC-003 — Dataset qualification before implementation dependency
A dataset is not accepted merely because it is labelled as RF fingerprinting data. It must be assessed against requirement and quality criteria.

## DEC-004 — Independent evaluation
Where metadata permits, avoid random sample splits that allow samples from the same session/burst to appear in both training and test data. Prefer session/day/device/receiver holdouts appropriate to the claim.

## DEC-005 — Poisoning evaluation
Use legitimate real RF data plus controlled/synthetic poisoning for the update-security experiment, explicitly labelling the attack evaluation as controlled/synthetic.

## DEC-006 — GitHub as project source of truth
The repository stores project knowledge, decisions, implementation, experiments, results, provenance and continuity.

## DEC-007 — Four-member collaboration model
All four members currently work on the same overall workstream. No permanent technical ownership division exists.

## DEC-008 — Branch model
`main` is stable; `develop` is integration; task/research branches provide isolation. Branch structure is not technical ownership. Scientific validation is independent of merge status.

## DEC-009 — Dataset portfolio qualification gate
WiSig, Oregon State WiFi RFFP, Oregon State LoRa RFFP and SMoRFFI are KEEP primary datasets. ORACLE and the Bluetooth smartphone database are SECONDARY. This is a development-substrate decision, not D1–D10 validation.

## DEC-010 — No open-ended dataset hunt before D1
Further dataset search should be triggered only by a specific experimental, reproducibility, access/licensing or metadata gap.

## DEC-011 — Continual-learning caveat
No public dataset automatically proves D8. The project must construct a chronological update protocol with frozen evaluation, profile acceptance and rollback protection.

## DEC-012 — Repository reconciliation
The earlier `main`/`develop` divergence is a repository-history anomaly, not a scientific issue. Because `main` is protected and direct force movement is prohibited, reconciliation must proceed through a normal PR from a branch based on `main`, synchronizing the required stable project content rather than rewriting protected history.

## DEC-013 — D1 transition
After dataset qualification, the next project gate is D1 Raw RF Data / Ingestion, beginning with WiSig and Oregon State WiFi.
