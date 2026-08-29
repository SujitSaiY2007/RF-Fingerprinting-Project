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

`Internet-accessible rapid-prototyping data -> minimum D1 -> D2 -> ... -> D10 demonstrable path -> broader validation with preserved qualified datasets`

## 2. Two independent but connected tracks

### Track A — Fast Implementation / Demonstration Track

**Purpose:** Obtain a small, reproducible, real-data, end-to-end implementation as quickly as possible without requiring the user to download large archives or upload them to ChatGPT.

**Dataset policy:** Track A uses **internet-accessible RF datasets that can be fetched/inspected directly by the execution environment or through stable public endpoints**, prioritizing:
- real RF/IQ data;
- clear device/identity labels;
- usable metadata/provenance;
- manageable size or downloadable subsets;
- formats that can be parsed programmatically;
- enough variation for the minimum D1–D10 path.

**Current Track A decision:** Use **ORACLE** as the first Track A candidate/working substrate, subject to final D1 accessibility, integrity, metadata and project-qualification checks before any scientific claim is made from it. This is an execution decision, not a claim that ORACLE has superseded the qualified primary dataset portfolio.

**Track A exclusions:** The user's uploaded **WiSig ManySig archive is deliberately kept separate from Track A**. It is preserved for Track B validation/reproduction/cross-checking and is not a dependency of the fast implementation path. Oregon State WiFi acquisition is likewise not permitted to block Track A.

Track A executes the minimum vertical path:

`D1 ingestion -> D2 DSP -> D3 RF evidence -> D4 embedding -> D5 identity -> D6 open-set -> D7 shift -> D8 profile evolution -> D9 poisoning -> D10 integration`

The target is a **working demonstration**, not a claim that every scientific acceptance criterion has already been satisfied.

### Track B — Research Validation / Strengthening Track

**Purpose:** Strengthen claims after or alongside the complete implementation path using the qualified/preserved datasets and broader experiments.

Activities include:
- WiSig ManySig validation using the already acquired user copy;
- Oregon State WiFi validation when acquisition is practical;
- larger subsets and additional days/devices where required;
- Oregon State LoRa and SMoRFFI where their defined experimental responsibilities are needed;
- ORACLE or Bluetooth as secondary benchmarks when justified beyond its Track A use;
- stronger cross-condition/cross-dataset validation;
- statistical analysis, ablation and failure analysis;
- experiments required to support or falsify the novelty hypothesis.

Track B must never be used to manufacture evidence after the fact. It strengthens or falsifies the claims produced by Track A.

## 3. Dataset acquisition policy

The project aims to avoid making the user repeatedly download or upload large datasets. Track A should prefer public data that the execution environment can access directly. User-side acquisition is only required when direct programmatic access is unavailable, licensing/terms require it, or the dataset is specifically needed for Track B validation.

Once a dataset is accepted for a track, preserve its raw copy unchanged where practical and reuse it throughout the relevant D1–D10 work.

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

It changes only the **execution priority and dependency structure**. The explicit separation of Track A from the already acquired ManySig copy is an execution decision: ManySig remains preserved and qualified for Track B rather than serving as the Track A dependency.
