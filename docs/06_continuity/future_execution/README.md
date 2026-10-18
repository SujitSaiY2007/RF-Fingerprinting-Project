# Future Execution Plan — F0 to F9

**Project:** Community Aware Secure Continual RF Fingerprinting for IoT Device Authentication  
**Canonical repository:** https://github.com/SujitSaiY2007/RF-Fingerprinting-Project  
**Development/reference branch:** `main` only  
**Plan owner:** F0 (planning and handoff)  
**Next execution chat:** F1  
**Status:** Plan established; execution stages not yet completed by this plan.

## 1. Purpose

This plan defines a bounded, multi-chat execution sequence for the remaining research. Each chat has one main objective, explicit entry conditions, bounded scope, expected evidence, exit criteria, and a handoff to the next numbered chat. This is intended to prevent context loss and avoid unplanned expansion.

The current code and results are the starting point, not unquestionable truth. Existing negative findings and artifacts must be preserved. All metrics remain provisional until tied to the exact code, configuration, split, and result artifact that produced them.

## 2. Branch and repository rules

1. Work only on `main`; it is both the development branch and reference branch.
2. Do not create, use, merge, or integrate a `develop`, `task/*`, or `research/*` branch. Historical branches may remain preserved; do not delete them as part of this plan.
3. Each chat begins by inspecting `git status --short --branch`, `git branch --show-current`, `git rev-parse HEAD`, and the latest relevant project handoff.
4. If the working tree has unexpected user changes, stop and report them. Never overwrite or discard them.
5. Make small, scoped changes. Test or validate them where appropriate. Review diffs before committing.
6. Commit directly to `main` only when the change is scoped, reviewed, and locally validated. Do not push unless the active chat's user instructions authorize it; the project owner has previously allowed synchronization of intended project changes, but each chat must still inspect outgoing commits and remote state.
7. Never force-push, rewrite history, use destructive reset/clean operations, or delete historical evidence.
8. Do not install packages or acquire new datasets without explicit authorization. Prefer existing environment and qualified datasets.
9. Never fabricate results. Label simulated results as synthetic and separate implementation tests from scientific validation.
10. Do not claim a stage is complete because files exist or tests pass; satisfy the stage's exit criteria.

## 3. Chat-size and continuity protocol

- One numbered chat owns one stage only. Do not silently absorb the next stage.
- Start each chat by reading this plan, `F0_HANDOFF.md`, `PROJECT_STATE.md`, and the previous chat's handoff.
- Keep a running summary of: goal, decisions, files changed, commands/tests, verified findings, unresolved issues, current HEAD, and next action.
- Stop when the exit criteria are satisfied, when a blocker needs owner input, or when context/workload is becoming large enough to risk continuity. Do not continue just to make the conversation appear complete.
- At exit, create/update the stage handoff file under this folder, update the status table in this plan and relevant project state, review the diff, and commit scoped changes to `main) only if safe.
- The handoff must specify the exact next chat number, entry point, starting commit, completed work, evidence paths, unresolved questions, forbidden assumptions, and first action.
- If a stage cannot be completed, mark it **BLOCKED** or **PARTIAL**, explain why, and hand the unresolved item to the next chat without pretending the exit criteria passed.
- Keep chat labels sequential: F0 is planning; the next chat is F1, then F2, and so on. Do not skip or reuse numbers.

## 4. Current status

| Chat | Stage | Status at plan creation |
|---|---|---|
| F0 | Define roadmap and handoff contract | PLAN CREATED |
| F1 | Forensic evidence reconciliation | NOT STARTED |
| F2 | Repair and verify Phase 5 collation | NOT STARTED |
| F3 | Lock reproducible evaluation contracts and baselines | NOT STARTED |
| F4 | Specify continual adaptation protocol and fair baselines | NOT STARTED |
| F5 | Evaluate secure continual adaptation and poisoning | NOT STARTED |
| F6 | Resolve receiver generalization, fusion, and open-set claims | NOT STARTED |
| F7 | Hardware/OTA validation planning and feasibility | NOT STARTED |
| F8 | End-to-end integration, security, and performance verification | NOT STARTED |
| F9 | Final scientific synthesis and submission package | NOT STARTED |

## 5. Execution stages

### F1 — Forensic evidence reconciliation

**Goal:** Establish a trusted claim-to-evidence ledger before modifying experiments.

**Entry conditions**
- Begin on `main` with a clean or fully understood working tree.
- Read this plan, `F0_HANDOFF.md`, `PROJECT_STATE.md`, README, Track-B JSON outputs, runners, configs, tests, and existing research reports.
- Preserve the previous commit and all historical artifacts.

**Tasks**
1. Inventory the current repository and confirm exact paths.
2. Trace each reported headline metric to its result JSON key, runner, configuration, split, population, denominator, and metric calculation.
3. Specifically reconcile B2-01 protocol differences; B2-02 cross-receiver values; B2-03 temporal values; B3-01 fusion protocols; B3-02 open-set rates and thresholds; B2-04 topology counts; B2-05 versus B4-01 security metrics; and Phase 5 collation errors.
4. Inspect whether tests actually validate the scientific results or only schemas/contracts.
5. Build a claim ledger with statuses `VERIFIED`, `PARTIALLY VERIFIED`, `UNVERIFIED`, or `CONTRADICTED`.
6. Do not change experiment logic or regenerate outputs in this stage.

**Exit criteria**
- Claim ledger cites exact evidence paths and JSON keys/functions/test names.
- Every contradiction is either resolved with evidence or explicitly left unresolved.
- No unsupported metric is promoted to a verified claim.
- Handoff identifies the precise Phase 5 correction needed, if confirmed.

**Out of scope:** Fixing scripts, rerunning experiments, hardware work, rewriting the research narrative.

### F2 — Phase 5 collation repair and regression

**Goal:** Correct the confirmed collation defect without changing the underlying experiment outputs.

**Entry conditions**
- F1 claim ledger is complete.
- The precise schema mismatch and expected correct behavior are evidenced.
- Current `main` is inspected; no unreviewed user changes are overwritten.

**Tasks**
1. Reproduce the failure safely in a temporary output location or using a non-writing test harness.
2. Correct the collation helper to read the actual authoritative result schema.
3. Preserve all original experiment JSON files; write any newly generated master summary to a new versioned file or explicitly approved target only.
4. Add tests that catch missing, mismatched, or misleading collation statuses and test actual key/value mapping rather than merely checking that keys exist.
5. Run the relevant existing test suite without package installation.
6. Compare before/after summaries and explain every changed field.

**Exit criteria**
- All eight experiment records are collated from their actual artifacts or clearly marked unavailable.
- No false `VALIDATED_AND_VERIFIED` status is generated when evidence is missing.
- Original raw results are unchanged.
- Tests and diff are reviewed; stage handoff is updated.

**Stop condition:** If a safe repair requires rerunning an experiment that overwrites original outputs, stop and request a decision.

### F3 — Reproducible evaluation contracts and baselines

**Goal:** Freeze comparable protocols and baseline definitions for future claims.

**Entry conditions**
- F1 ledger exists; F2 is complete or its remaining blocker is explicitly documented.

**Tasks**
1. Define train/validation/test separation, date/receiver/device holdouts, class populations, denominator conventions, random seeds, and threshold calibration policy.
2. Separate model selection and threshold tuning from final test evaluation.
3. Define metric formulas and aggregation: accuracy, macro-F1, balanced accuracy, known acceptance, unknown rejection, attack acceptance, contamination, adaptation utility, and resource metrics.
4. Record the fixed baseline models and controls, including no-update/static profile, naive update, confidence-only admission, and proposed security-gated update where applicable.
5. Make evaluation configs machine-readable and add leakage/split-contract tests.
6. State exactly which dataset supports each experiment and what metadata does not support.

**Exit criteria**
- A reviewable protocol specification and experiment matrix exist.
- Every future comparison has a defined population, split, baseline, metric, and output location.
- No result is called reproducible until a clean run or equivalent evidence demonstrates it.

### F4 — Secure continual-adaptation protocol and implementation design

**Goal:** Define the research mechanism around the central hypothesis: recognizing identity is separate from authorizing a persistent profile update.

**Entry conditions**
- F3's evaluation contract and baselines are accepted.
- No assumption that current community gating already proves continual learning.

**Tasks**
1. Define a chronological stream and a frozen evaluation set that is never used for updates or threshold tuning.
2. Specify legitimate drift scenarios and controlled poisoning/spoofing scenarios with documented assumptions.
3. Define candidate update authorization evidence: identity confidence, RF-feature/profile deviation, temporal consistency, witness agreement, open-set result, and replay freshness as applicable.
4. Define quarantine, rejection, rollback, recovery, and profile-state logging.
5. Specify ablations and fair baselines: frozen profile, naive update, confidence-only update, and proposed gate.
6. Establish success criteria before running the experiment.

**Exit criteria**
- A protocol/design note and configs define all scenarios, baselines, metrics, and safety boundaries.
- The distinction between identification, authentication decision, and permission to learn is explicit.
- Any implementation gap is listed rather than silently assumed complete.

### F5 — Controlled continual adaptation and poisoning evaluation

**Goal:** Measure whether secure update authorization preserves legitimate adaptation while limiting adversarial profile corruption.

**Entry conditions**
- F4 protocol is approved and the evaluation set is frozen.
- Output paths are versioned so existing artifacts cannot be overwritten.
- Data and simulation boundaries are explicit.

**Tasks**
1. Implement only the approved protocol and necessary tests.
2. Evaluate frozen, naive, confidence-only, and proposed gated-update controls on the same streams.
3. Report legitimate acceptance and adaptation utility alongside attack acceptance, contamination, false holds, recovery, and profile distortion.
4. Run ablations to identify which gate components actually contribute.
5. Use multiple seeds/repetitions where appropriate and report variability.
6. Mark synthetic attacks as synthetic; do not infer physical validation.

**Exit criteria**
- Results are generated from the locked protocol and tied to code/configuration/version.
- Security improvements are assessed alongside legitimate adaptation cost.
- Negative or inconclusive results are preserved and interpreted honestly.

### F6 — Receiver generalization, fusion, and open-set reconciliation

**Goal:** Establish defensible claims about receiver portability, multi-receiver fusion, and unknown-device rejection.

**Entry conditions**
- F1 ledger and F3 evaluation contract are available.
- Existing results are preserved as historical records.

**Tasks**
1. Reconcile the exact B2-02, B3-01, and B3-02 protocols and denominators.
2. Check whether observations across receivers are physically simultaneous or only metadata-matched.
3. Compare single-receiver, equalized, and fusion results on a common, leakage-safe evaluation contract.
4. Separate closed-set identification accuracy from unknown-device rejection and accepted-known accuracy.
5. Examine missing receiver behavior and the effect of receiver count.
6. Rerun only where necessary, approved, and safely versioned.

**Exit criteria**
- Comparable result tables clearly identify protocol differences.
- Claims about multi-receiver gains include the matching assumptions and receiver availability conditions.
- Unknown rejection, known acceptance, and conditional accuracy are reported separately.

### F7 — Hardware and over-the-air validation planning

**Goal:** Decide what can realistically be validated on hardware and prepare a safe, costed test plan.

**Entry conditions**
- The software evaluation and limitations are documented.
- Available hardware, budget, lab access, and regulatory constraints are known or explicitly listed as unknown.

**Tasks**
1. Define the minimum viable OTA experiment and which claims it can validate.
2. Identify candidate SDR/radio boards, transmitters, receivers, antennas, cables, synchronization/timestamp needs, and lawful test environment.
3. Distinguish replay/freshness protocol tests from RF waveform replay or RF perturbation experiments.
4. Define capture metadata, calibration, repeatability, and data-provenance requirements.
5. Produce a bill of materials with alternatives and an explicit go/no-go decision based on budget/access.
6. Do not purchase equipment or transmit RF without explicit owner approval and required compliance.

**Exit criteria**
- Hardware test plan, dependencies, risks, and costs are documented.
- Any unavailable synchronization or timestamp capability is called out.
- The project has an explicit decision: proceed with an approved testbed, use an existing lab, or clearly limit claims to offline/synthetic evidence.

### F8 — End-to-end integration, security, and performance verification

**Goal:** Validate the actual pipeline as a system rather than treating isolated module tests as end-to-end evidence.

**Entry conditions**
- The scientific claim ledger is current.
- Relevant components and tests are stable.
- Hardware results are included only if F7 has an approved and completed testbed.

**Tasks**
1. Trace input from RF observation through feature extraction, classifier, open-set gate, receiver/community evidence, freshness check, update authorization, profile state, and audit log.
2. Add or verify integration tests for legitimate, unknown, replay, spoof, poisoning, stale state, missing receivers, malformed input, and recovery paths.
3. Verify audit-chain tamper detection and failure behavior.
4. Measure latency, throughput, memory, and resource usage with a documented environment and repeated runs.
5. Ensure Phase 5 collation consumes current schemas and fails closed on missing evidence.
6. Distinguish unit-test results, simulated scenario results, offline dataset results, and OTA results.

**Exit criteria**
- A traceable end-to-end test report exists.
- Performance numbers include methodology and conditions.
- No test badge or status implies stronger scientific validation than the tests provide.

### F9 — Final scientific synthesis and submission package

**Goal:** Turn verified implementation and evidence into a defensible final research narrative and team handoff.

**Entry conditions**
- F1–F8 are complete or explicitly marked partial/blocked.
- The claim ledger is the source of truth for all numbers and claims.

**Tasks**
1. State the research question, contributions, novelty boundary, and relevant baselines.
2. Present methods, dataset provenance, protocols, results, uncertainty, limitations, and negative findings.
3. Separate real ManySig experiments, synthetic security simulations, software tests, benchmarks, and hardware results.
4. Build all tables/figures directly from authoritative evidence.
5. Reconcile README, `PROJECT_STATE.md`, research reports, and submission text without deleting historical reports.
6. Provide a reproducibility checklist and remaining-work statement.

**Exit criteria**
- Every quantitative claim maps to an authoritative artifact and protocol.
- No unsupported physical/security/generalization claim remains.
- The report's scope matches the actual evidence and the team can reproduce the stated workflow.

## 6. Definition of done for every chat

A stage is done only when:
- Entry conditions were checked.
- Scoped work is complete or clearly marked blocked.
- Evidence and validation commands/results are recorded.
- Relevant files and diffs were reviewed.
- The working tree and branch state are reported.
- A handoff for the next numbered chat is saved.
- The next chat's first action and stop conditions are explicit.
- No branch other than `main` was used.

## 7. Project-wide research guardrails

- Existing Track-A and Track-B artifacts, raw data, negative findings, and history are valuable and must be preserved.
- A synthetic result is never described as an OTA/physical attack result.
- Matched-receiver accuracy is not cross-receiver generalization.
- Metadata-matched receiver observations are not proof of physical simultaneity.
- Replay detection requires freshness state where identical RF features cannot distinguish original and replay.
- A passing test suite verifies only the behaviors those tests actually exercise.
- The research novelty remains a hypothesis until compared fairly against appropriate baselines.
- No result is upgraded to verified solely because a report, README, or test says so.

## 8. Next action

**Start F1 — Forensic evidence reconciliation.** First inspect current `main` and its working tree; then build the claim-to-evidence ledger. Do not implement fixes during F1.
