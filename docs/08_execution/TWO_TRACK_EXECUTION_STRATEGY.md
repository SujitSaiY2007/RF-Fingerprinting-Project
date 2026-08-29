# Two-Track Accelerated Execution Strategy

**Decision date:** 2026-08-29  
**Status:** Active execution policy  
**Purpose:** Separate fast end-to-end implementation from research-strength validation so dataset acquisition does not become the critical path under the project time constraint.

## 1. Why the execution model changed

The project has already completed dataset qualification and has a defensible primary dataset portfolio. However, large raw RF archives can take substantial time to acquire and inspect. Waiting for every large dataset before implementing D1–D10 would make data logistics the critical path and delay demonstration of the complete project idea.

The project therefore changes **execution order**, not the scientific standard.

Previous implicit sequence:

`Acquire large datasets -> inspect all data -> D1 -> D2 -> ... -> D10`

New sequence:

`Accessible real development substrate -> minimum D1 -> D2 -> ... -> D10 demonstrable path -> strengthen/validate with additional qualified datasets`

## 2. Two independent but connected tracks

### Track A — Fast Implementation / Demonstration Track

**Purpose:** Obtain a small, reproducible, real-data, end-to-end implementation as quickly as possible.

Primary working substrate:
- WiSig ManySig, already acquired by the user;
- Oregon State WiFi RFFP remains the first intended second implementation dataset when acquisition is practical;
- another already-qualified dataset may be substituted or added only when a documented access/metadata/experimental reason justifies it.

Track A executes the minimum vertical path:

`D1 ingestion -> D2 DSP -> D3 RF evidence -> D4 embedding -> D5 identity -> D6 open-set -> D7 shift -> D8 profile evolution -> D9 poisoning -> D10 integration`

The target is a **working demonstration**, not a claim that every scientific acceptance criterion has already been satisfied.

### Track B — Research Validation / Strengthening Track

**Purpose:** Strengthen claims after the complete implementation path exists.

Activities include:
- larger subsets and additional days/devices where required;
- Oregon State WiFi validation;
- Oregon State LoRa and SMoRFFI where their defined experimental responsibilities are needed;
- ORACLE or Bluetooth as secondary benchmarks when justified;
- stronger cross-condition/cross-dataset validation;
- statistical analysis, ablation and failure analysis;
- experiments required to support or falsify the novelty hypothesis.

Track B must never be used to manufacture evidence after the fact. It strengthens or falsifies the claims produced by Track A.

## 3. Dataset acquisition policy

The project aims to acquire the necessary development datasets once, preserve the raw copies unchanged, and reuse them throughout D1–D10.

Repeated downloads of the same dataset are not expected.

Additional acquisition is allowed only when a concrete need appears, such as:
- an experimental requirement not covered by the current subset;
- a missing day/device/receiver/environment needed for a claim;
- an access, integrity or reproducibility problem;
- a licensing/provenance issue;
- a benchmark requirement that materially strengthens validation.

No open-ended dataset hunt is permitted.

Large raw datasets remain outside Git.

## 4. Scientific completion remains unchanged

A stage is not scientifically complete merely because its code exists or because a demonstration runs.

Maintain the distinction:

1. **Implemented** — code/artifact exists.
2. **Tested** — implementation passes defined tests or produces reproducible engineering results.
3. **Demonstrated** — the integrated path operates on real data.
4. **Scientifically validated** — the stage's acceptance criteria and evidence support the stated claim.

Track A primarily accelerates levels 1–3. Track B is used wherever level 4 requires additional data or stronger experiments.

## 5. Novelty discipline under the two-track model

The project must not treat implementation alone as proof of novelty.

The current provisional contribution remains:

> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile-poisoning while preserving legitimate adaptation.**

The decisive experiment remains the comparison of:

- A: naive update;
- B: confidence-only update;
- C: reliability/consistency admission;
- D: security/update-safety authorization.

The key comparison is **C versus D**.

If D does not provide a measurable advantage over C while preserving legitimate adaptation, the novelty claim must be revised or abandoned.

## 6. Fast-track implementation rule

Do not over-engineer individual stages before the complete path exists.

For each stage:

`Minimum defensible implementation -> test -> record evidence -> move forward -> strengthen after vertical path`

Failures and limitations must be recorded rather than hidden.

## 7. Relationship to the original plan

This strategy does **not** delete or replace the qualified dataset portfolio, prior-art findings, D1–D10 definitions, branch rules, leakage controls, poisoning controls, knowledge base, or scientific completion criteria.

It changes only the **execution priority and dependency structure** so that real-data acquisition is no longer an unnecessary blocker to building the complete software lifecycle.
