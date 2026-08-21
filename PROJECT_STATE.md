# PROJECT STATE

**Last updated:** 2026-08-21

## Authoritative status

- Project repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Stable branch: `main`
- Integration branch: `develop`
- Development status: **Phase 1 — Preparation**
- Current workstream: **Dataset Search & Validation / Qualification**
- Implementation status: **Not started / intentionally gated**
- Team size: **4 members**

## Current team model

All four team members are currently working on the same overall workstream at individual levels: Dataset Search & Validation / Qualification. There is no permanent technical division or fixed member-to-module ownership. Independent overlap is expected and should be consolidated through GitHub evidence.

## Completed in this workstream

- Recovered the repository continuity layer and verified the Dataset Requirement Matrix.
- Confirmed that the dataset registry was previously only a header/template and contained no qualified candidates.
- Performed a first external evidence-backed candidate search.
- Added a preliminary portfolio and qualification records for WiSig, Oregon State WiFi RFFP, Oregon State LoRa RFFP, SMoRFFI, ORACLE and a Bluetooth smartphone database.
- Populated `datasets/dataset_registry.csv` with preliminary decisions and known limitations.
- Established that a multi-dataset portfolio is necessary at the current evidence level.

## Current preliminary portfolio

**KEEP:** WiSig; Oregon State WiFi RFFP; Oregon State LoRa RFFP; SMoRFFI.

**SECONDARY:** ORACLE; Bluetooth smartphone database.

These are preliminary qualification decisions, not final portfolio lock decisions.

## Important evidence-based interpretation

- WiSig is strongest for scale, receiver variation and multi-day robustness.
- Oregon State WiFi is strong for temporal/domain variation with repeated Pycom devices.
- Oregon State LoRa is strong for same-model and environmental robustness outside WiFi.
- SMoRFFI is especially important for large-scale same-model discrimination.
- ORACLE is valuable as a controlled hardware-impairment/distance benchmark but is too limited to be the primary portfolio.
- D8 remains incompletely qualified because a defensible continual-learning protocol requires verified sequential/session semantics.
- D9 should continue to use legitimate RF data plus controlled/synthetic poisoning under DEC-005.

## Current blockers / open questions

1. Direct inspection of each candidate's actual metadata/download package is still required before final lock.
2. Dataset-specific license/redistribution/use terms must be confirmed from the actual dataset source, not inferred from the paper license alone.
3. SMoRFFI receiver/session/day/environment coverage is not yet sufficiently established for D7/D8.
4. Oregon State scenario-level metadata and exact sequential semantics require direct inspection.
5. A final split protocol for D6 unknown-device evaluation must be defined before claiming open-set support.
6. Portfolio lock criteria and final dataset-to-D-stage responsibility matrix still need to be finalized.

## Repository consistency issue discovered

`main` and `develop` are currently **diverged** rather than being in the clean relationship described by the collaboration model. GitHub reports `develop` ahead by 7 commits and behind `main` by 7 commits. The latest closed PR #1 established the initial infrastructure, but later continuity commits exist on the branches without a subsequent reconciliation. This is a repository-state issue, not a scientific issue, and must be resolved before relying on `develop` as a clean integration base.

## Next exact action

Perform direct dataset-package/metadata/access verification for the four KEEP candidates, beginning with WiSig and Oregon State RFFP, then SMoRFFI and ORACLE as required. Convert every major claim from "reported by source" to "verified for project use" or explicitly leave it unresolved. Then produce the final coverage/gap matrix and only after that decide whether the portfolio can be locked.

## Validation status

D1–D10 remain scientifically incomplete. No dataset qualification is itself evidence that any D-stage has been validated.
