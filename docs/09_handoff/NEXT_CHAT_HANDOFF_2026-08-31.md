# NEXT CHAT HANDOFF — 31 August 2026

## Purpose

This document is the current continuation point after the project's Q/A truth-audit, professional dashboard refinement, glossary preparation and complete reference-report preparation.

The next chat must use the repository as the source of truth and must not restart completed work or silently change frozen evidence.

## Current project position

Treat the project as **one complete project executed through constrained tracks**:

`Complete Project -> Track A under constraints -> Track-A Version B final demonstrator baseline -> Track B broader validation -> desired end product`

Track A is complete to its intended demonstration ceiling. The current Track-A Version-B system is the new baseline for future research. Track B is the next research direction for broader validation and strengthening; it is not completed.

## Current Track-A baseline

- SMoRFFI is the Track-A real RF working dataset.
- Version A is the frozen RF recognition control.
- Version B retains the RF recognition backbone and adds protected adaptive profile management.
- D8, D9 and D10 are demonstrated in the defined Track-A setting.
- The professional web demonstrator is deployed.
- The complete reference report is recorded at `docs/06_continuity/REFERENCE_REPORT_2026-08-31.md`.

## Frozen V-A vs V-B evidence

- Closed-set RF accuracy: **87.3899% vs 87.3899%**.
- Known acceptance: **94.90% vs 94.90%**.
- Unknown rejection: **29.49% vs 29.49%**.
- Profile test accuracy after adaptation: **28.6629% vs 37.9704% (+9.3075 pp)**.
- Replay acceptance: **100% vs 1% (-99 pp)**.
- Replay hold: **0% vs 99% (+99 pp)**.
- Gain-drift acceptance: **100% vs 94.6809% (-5.3191 pp)**.
- Mean profile displacement: **0.995174 vs 0.969641**.
- Target-like unknown contamination: **100% vs 100% — unresolved**.

Do not hide, soften, relabel or reinterpret the target-like unknown result.

## What the current evidence supports

### Strongly demonstrated in Track A
- reproducible RF fingerprinting pipeline on SMoRFFI;
- Version-A RF recognition control;
- open-set evaluation in the defined setting;
- legitimate adaptive profile evolution in the tested scenario;
- protected update authorization/quarantine behaviour;
- strong replay improvement in the tested controlled scenario;
- D8/D9/D10 integrated demonstrations;
- deployed final demonstrator.

### Limited / partially achieved
- general poisoning resistance;
- gain-drift handling;
- secure adaptive profile evolution beyond the tested Track-A conditions.

### Not demonstrated
- universal Version-B superiority;
- complete target-like poisoning resistance;
- arbitrary cross-dataset generalization;
- arbitrary cross-frequency generalization;
- complete real-world RF validation;
- formal proof of novelty against all prior art;
- Track-B validation.

## Novelty status

The broad adaptive-RF-update novelty idea was rejected as too broad after prior-art review. The current hypothesis is narrower:

`identity recognition != authorization to modify persistent RF identity/profile`

The candidate contribution concerns security-oriented separation of recognition from authorization to modify persistent profile state, especially under target-like unknown contamination while still allowing legitimate adaptation.

Status: **plausible, implemented and tested research hypothesis; not formally proven novelty**.

Do not claim generic adaptive updating, generic update gating, or reliable-sample admission as standalone novelty.

## Track-B mission

Track B should take the current Version-B implementation as the baseline and test the complete architecture under broader conditions:

1. additional qualified real RF datasets;
2. cross-dataset validation;
3. temporal/session variation;
4. environment variation;
5. receiver/acquisition variation;
6. potentially cross-frequency evaluation;
7. broader device populations;
8. more realistic adversarial and target-like contamination;
9. targeted mechanisms to address the Track-A 100% target-like unknown failure;
10. ablations/statistical analysis;
11. systematic prior-art/novelty validation.

Track B must be opened as a dated research phase with explicit datasets, hypotheses, protocols and success/falsification criteria. Do not silently turn the roadmap into completed evidence.

## Required reading at the start of the next chat

1. `PROJECT_STATE.md`
2. `CURRENT_OBJECTIVE.md`
3. `docs/09_handoff/NEXT_CHAT_HANDOFF_2026-08-31.md`
4. `docs/06_continuity/REFERENCE_REPORT_2026-08-31.md`
5. `docs/09_handoff/NEXT_CHAT_QA_NOTE.md` for historical Q/A context
6. `docs/06_continuity/DECISIONS.md`
7. `docs/06_continuity/SESSION_LOG.md`
8. relevant D8/D9/D10 evidence and Version-A/Version-B documentation
9. `docs/04_research/targeted_prior_art_matrix.md`
10. the professor-facing submitted document when preparing presentation material

## Next-chat operating rules

- Start by identifying the user's explicit objective for that chat.
- Do not modify GitHub, code, experiments, datasets, UI or decisions merely because a possible improvement is noticed.
- Preserve all historical documents and evidence.
- No force-push, reset, destructive rewrite or unnecessary deletion.
- Frozen Track-A research numbers remain unchanged unless a new dated experiment is explicitly opened.
- Separate fact, inference, project decision and experimental result.
- Use the evidence levels **Implemented / Tested / Demonstrated / Scientifically Validated** accurately.
- Controlled/derived scenarios must remain explicitly labelled and must not be presented as source-dataset measurements.
- Do not invent literature support or experimental evidence.
- If evidence is insufficient, state: **Not demonstrated by the current evidence.**
- At significant accepted milestones, synchronize `main` and `develop` to the same canonical project state without destructive history changes.

## Presentation/reference priority

The current Track-A Version-B demonstrator is the product baseline for presentation. Presentation material should explain both the successful security improvement and the unresolved target-like unknown limitation. A credible presentation is stronger when it shows the negative result rather than implying complete security.

The next research implementation should not begin until its exact Track-B objective and experiment boundary are explicitly agreed.
