# NEXT CHAT HANDOFF — 2026-09-02

## Purpose
This handoff closes the current Antigravity/ChatGPT working session and defines the exact starting point for the next session. The next session must continue from this state rather than repeating completed Track-A work, ManySig inspection, streaming POC, or full feature extraction.

## Canonical repository state at handoff
- Repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Working branch for the completed ManySig engineering phase: `task/manysig-feature-extraction-runner-2026-09-02`
- ManySig extraction/provenance checkpoint: commit `0bee709552e440b620205ed4cd412a6625449f44`
- State/objective handoff updates follow that checkpoint on the same task branch.
- Current working direction: **Track-B B1 — ManySig Scientific Validation / Dataset Quality Analysis**
- Do not merge this task branch into `develop`/`main` as part of B1. Promotion is a separate milestone decision.

## What is already complete — DO NOT REPEAT

### Track A — frozen baseline
Track-A Version-B is complete to its intended demonstration ceiling. The following are frozen and must not be silently changed, deleted or recomputed as a replacement baseline:
- D2 input contract: `serialized preamble -> complex[288] -> float32[2,288] I/Q`
- 16 deterministic RF evidence features
- Version-A fixed Random Forest control
- B0-B2 model-selection screening and negative result for learned replacements
- D8 profile evolution
- D9 security/poisoning evaluation
- D10 integrated lifecycle
- final web demonstrator
- all historical evidence, limitations and novelty decisions

Principal unresolved Track-A security limitation: **target-like unknown contamination remained 100% accepted in the tested scenario**. Do not hide, relabel or imply that Track B has already solved this problem.

### ManySig acquisition and inspection
ManySig was acquired as `ManySig.pkl.zip` and preserved as the original raw archive outside Git.

Verified archive structure:
- 6 TX
- 12 RX
- 4 dates
- 2 equalization states
- 576 leaves total
- 1,000 bursts per leaf
- 576,000 bursts total
- each burst `(256, 2)` float64 I/Q

The raw archive must remain outside Git and must not be modified, renamed, moved, extracted into the repository, or committed.

### Real-archive streaming POC
Completed and documented in:
`docs/06_continuity/MANYSIG_REAL_STREAMING_POC_2026-09-02.md`

Core implementation:
`src/manysig_streamer.py`

The POC demonstrated real-archive opcode-level streaming with bounded process memory. Selective/full-stream tests reached approximately 45–53 MiB peak RSS and approximately 14–17 MiB incremental RSS overhead. The informal earlier `<=25–30 MB total RSS` target is not claimed as an absolute process-RSS achievement; runtime/interpreter baseline makes that target unsuitable.

The POC is an **engineering result**, not Track-B scientific validation.

### ManySig full feature extraction
Completed and committed in:
`0bee709552e440b620205ed4cd412a6625449f44`

Tracked artifacts include:
- `src/manysig_feature_extractor.py`
- `scripts/run_manysig_feature_extraction.py`
- `docs/06_continuity/MANYSIG_FULL_EXTRACTION_2026-09-02.md`
- `datasets/features/manysig/manifest.json`
- `datasets/features/manysig/extraction_summary.json`
- updated `docs/06_continuity/SESSION_LOG.md`

The extraction produced:
- 576,000 per-burst feature records
- 16 Track-A RF evidence features reused without changing their definitions
- 24 receiver/equalization Parquet partitions
- cryptographic SHA-256 manifest
- machine-readable extraction summary

The Parquet files are intentionally ignored by Git. The raw ManySig archive is not tracked. Provenance metadata and continuity documentation are tracked.

The extraction is an **engineering input artifact**, not a scientific result.

## Important scientific qualification
The ManySig source inspection did not verify a sample-rate field. A nominal **20 MHz** sample rate exists only as an engineering default and is explicitly **REQUIRES VALIDATION**. Do not convert it into a verified dataset fact.

## Dataset acquisition status
Only ManySig has been acquired so far. The remaining qualified datasets have not yet been downloaded. This does **not** block B1. Do not delay B1 solely to acquire the remaining datasets. Their later role is cross-dataset validation.

## Exact next phase — B1
### Phase name
**Track-B B1 — ManySig Scientific Validation / Dataset Quality Analysis**

### Objective
Determine whether the completed ManySig feature dataset is scientifically usable and characterize its structure, coverage, variation and risks before any Track-B model training or hypothesis testing.

### B1 tasks
1. Read this handoff first and treat it as the starting checkpoint.
2. Verify the current Git branch/commit and working-tree status without rewriting history.
3. Inspect only the targeted files needed to execute B1; do not restart the full historical repository audit unless a specific inconsistency is found.
4. Verify the tracked ManySig manifest and extraction summary against the existing extraction report.
5. Verify schema, row counts, coordinate coverage and partition completeness.
6. Characterize coverage across TX, RX, date and equalization dimensions.
7. Perform feature-level sanity checks and descriptive statistical/distribution analysis.
8. Look for obvious duplication, leakage, partition contamination and split-design risks.
9. Examine receiver/date/equalization variation that will matter for future train/test or cross-condition validation.
10. Check whether the 16-feature definitions remain exactly aligned with the frozen Track-A definitions. This is a methodological consistency check, not a modification of Track A.
11. Explicitly document the sample-rate metadata gap and any other provenance limitations.
12. Separate every output into **Verified Fact / Engineering Observation / Inference / Scientific Result** as appropriate.
13. Produce a dated B1 report in `docs/06_continuity/` and update continuity/handoff state as necessary.

### B1 is NOT allowed to do
- Do not redo ManySig archive inspection unless required to resolve a concrete inconsistency.
- Do not rerun the real-archive streaming POC merely to reproduce an already verified result.
- Do not re-extract all 576 leaves unless a specific reproducibility defect is discovered.
- Do not alter the frozen Track-A feature definitions.
- Do not alter the frozen Track-A metrics or evidence.
- Do not start unrestricted ML training.
- Do not perform classifier benchmarking as a Track-B scientific result.
- Do not perform adversarial/poisoning experiments.
- Do not perform cross-dataset validation yet.
- Do not claim cross-frequency/generalization evidence.
- Do not claim scientific validation merely because descriptive analysis succeeds.
- Do not invent or silently assume sample-rate metadata.
- Do not commit raw data or ignored Parquet binaries.
- Do not delete historical files.
- Do not force-push, reset, rebase destructively, or rewrite history.

## B1 deliverables
At the end of B1, the repository should contain, as appropriate:
- a dated ManySig B1 scientific validation/quality report;
- any small, reproducible analysis/validation scripts needed for the report;
- machine-readable summary artifacts only where they materially improve reproducibility;
- updated session/decision/current-objective documentation if the evidence changes the project state;
- a new next-chat handoff defining the next bounded phase.

Do not create unnecessary duplicate documents or duplicate analysis scripts.

## B1 stop condition
**Stop the chat after B1 is complete.** Completion means:
- provenance/schema integrity is assessed;
- coverage across TX/RX/date/equalization is documented;
- feature sanity/distributions are documented;
- leakage/duplication/split risks are documented;
- the sample-rate limitation is explicitly preserved;
- the scientific usability and limitations of ManySig features are stated;
- all claims are evidence-labelled;
- the B1 report and continuity state are committed/pushed;
- the next-chat handoff is written.

At that point, do not continue into ML, adversarial experiments or cross-dataset validation in the same chat. Stop and hand off.

## Evidence vocabulary
Use only the project vocabulary:
- **Implemented** — code exists.
- **Tested** — a defined test was executed.
- **Demonstrated** — the behaviour was empirically shown in the stated setting.
- **Scientifically Validated** — only when the appropriate scientific experiment/design supports that level.

Never upgrade an engineering demonstration into scientific validation.

## Preservation rules
The project is intentionally cumulative. Preserve all historical evidence and decisions. Prefer additive updates over replacement. Do not remove files because a new phase supersedes them. The Track-A baseline remains the control/reference against which later Track-B work may be interpreted.

## Starting instruction for the next Antigravity chat
Begin with the following principle:

> **Continue from this handoff. Do not restart completed work. First verify the current Git state, then execute only Track-B B1 ManySig Scientific Validation / Dataset Quality Analysis. Stop at the B1 stop condition and create the next handoff.**
