# ChatGPT Continuation Prompt

Use this prompt when opening a new ChatGPT session for the project.

---

You are continuing the long-running research/engineering project maintained in `SujitSaiY2007/RF-Fingerprinting-Project`.

Treat GitHub as the project's persistent source of truth and continuity layer. Before proposing work, inspect the repository state rather than relying on chat memory.

## Mandatory first inspection

Read:

1. `README.md`
2. `PROJECT_STATE.md`
3. `PROJECT_MASTER_PLAN.md`
4. `CURRENT_OBJECTIVE.md`
5. `docs/01_project_definition/`
6. `docs/02_system_architecture/`
7. `docs/03_dataset_strategy/`
8. `docs/06_continuity/SESSION_LOG.md`
9. `docs/06_continuity/DECISIONS.md`
10. the latest relevant Issues, branches, commits and Pull Requests.

Do not restart the project from the beginning. Do not assume that a documented claim is automatically true. Distinguish source-derived facts, project decisions, experimental evidence, inference, and unresolved hypotheses.

## Project identity

The project is physics-based RF fingerprinting with continuous device learning. The direction combines RF signal processing, RF physics features, learned device representations, known/unknown device recognition, continual profile evolution, poisoning/update protection, end-to-end software validation, and eventual hardware transfer/edge deployment.

The development philosophy is software-first: existing/public datasets are the primary development and validation substrate. Hardware capture is a later transfer-validation domain unless the repository explicitly changes this decision.

## Validation framework

D1 Raw RF Data / Ingestion
D2 Synchronization & DSP
D3 Physics-Based RF Features
D4 Device Representation / Embedding
D5 Closed-Set Identification
D6 Open-Set Recognition
D7 Robustness / Domain Shift
D8 Continual Learning / Profile Evolution
D9 Poisoning / Adversarial Protection
D10 End-to-End Validation

A stage is not complete merely because code exists. Completion requires its defined evidence and acceptance criteria.

## Research methodology

`Project Claim -> What Must Be Proven -> Experiment -> Required Data -> Dataset Search -> Dataset Qualification -> Validation -> Conclusion`

Do not select datasets first and retrofit the project claims around whatever data happens to be available.

## Engineering methodology

`Requirement -> Design -> Implementation -> Test -> Experiment -> Result -> Interpretation -> Decision`

## Operating rules

- Continue from the exact repository state.
- Check existing work before duplicating it.
- Challenge weak assumptions and identify contradictions.
- Never claim evidence that has not been generated.
- Never silently change project scope or research questions.
- Keep research documentation synchronized with implementation.
- Use Issues and Pull Requests for team work.
- Record significant research/design decisions in `DECISIONS.md`.
- Keep large raw datasets outside Git when appropriate; retain manifests, metadata, checksums and qualification records in Git.

## End-of-session protocol

At the end of substantial work:

1. State what was completed.
2. State what remains incomplete.
3. Record important decisions.
4. Record unresolved questions.
5. Update `PROJECT_STATE.md` and `CURRENT_OBJECTIVE.md` when needed.
6. Add a concise entry to `SESSION_LOG.md`.
7. If another ChatGPT session is likely, provide the next-session continuation prompt.

First determine:

1. What has actually been completed?
2. What is currently in progress?
3. What is blocked?
4. What is the single most important next action?
5. What evidence is required to declare that action complete?

Then execute the current objective rather than inventing a new project direction.
