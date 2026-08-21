# ChatGPT Continuation Prompt

Use this prompt when opening a new ChatGPT session for the project.

---

You are continuing an ongoing research/engineering project maintained in the GitHub repository `SujitSaiY2007/RF-Fingerprinting-Project`.

Treat GitHub as the project's persistent source of truth. Before proposing work, inspect and understand the current repository state, especially:

1. `README.md`
2. `PROJECT_STATE.md`
3. `PROJECT_MASTER_PLAN.md`
4. `CURRENT_OBJECTIVE.md`
5. `docs/01_project_definition/`
6. `docs/03_dataset_strategy/`
7. `docs/06_continuity/SESSION_LOG.md`
8. `docs/06_continuity/DECISIONS.md`
9. the latest relevant Issues, branches, commits and Pull Requests

Do not restart the project from the beginning and do not assume that previous claims are correct merely because they are documented. Distinguish established facts, project decisions, experimental evidence, inference and open hypotheses.

The project concerns physics-based RF fingerprinting with continuous device learning. The current direction combines RF signal processing, RF physics features, learned device representations, known/unknown device recognition, continual profile evolution, poisoning/update protection, end-to-end software validation, and eventual hardware transfer/edge deployment.

The current development philosophy is software-first: existing/public datasets are the primary development and validation substrate, while hardware capture is introduced later for transfer validation.

The dataset framework consists of D1-D10:
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

The project's methodology is:

Project Claim -> What Must Be Proven -> Experiment -> Required Data -> Dataset Search -> Dataset Qualification -> Validation

Do not select datasets first and retrofit claims around them.

When solving the current task:

- Continue from the exact repository state.
- Check existing work before duplicating it.
- Use evidence and reproducible reasoning.
- Identify uncertainty and missing information explicitly.
- Do not silently change project scope.
- Do not mark an experiment complete without evidence.
- Keep research documentation synchronized with implementation.
- For code changes, use the team's branch/PR workflow.
- For significant decisions, update `docs/06_continuity/DECISIONS.md`.
- At the end of substantial work, update `PROJECT_STATE.md`, `CURRENT_OBJECTIVE.md`, and `SESSION_LOG.md` so the next ChatGPT session can continue without reconstructing context from chat history.

First determine:

1. What has actually been completed?
2. What is currently in progress?
3. What is blocked?
4. What is the single most important next action?
5. What evidence is required to declare that action complete?

Then execute the current objective rather than inventing a new project direction.
