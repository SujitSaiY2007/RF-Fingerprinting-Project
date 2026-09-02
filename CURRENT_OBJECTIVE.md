# CURRENT OBJECTIVE

## Current checkpoint — Track-A Version-B baseline frozen; Track-B ManySig engineering pipeline demonstrated
Track-A Version-B security core is demonstrated and the professional web demonstrator is deployed. The Q/A truth-audit and reference consolidation are complete. Track-B has now begun with a real ManySig ingestion and feature-extraction engineering path, while scientific/ML validation remains pending.

The project is treated as one complete project executed through constrained tracks:

`Complete Project -> Track A under constraints -> Track-A Version-B final demonstrator baseline -> Track B broader validation -> desired end product`

Track A is complete to its intended demonstration ceiling. Track B is the planned broader research/validation direction and must be completed through separately dated, evidence-bounded phases.

## Agreed project direction — Track A -> Track B
Track A was deliberately created as a quicker, controlled, reproducible implementation and ideation track for the final product demonstrator. It established Version A, improved it into Version B, generated evidence, exposed limitations and produced the working demonstrator.

Track A has a defined ceiling because of its agreed constraints. It should not be presented as universal RF generalization or as complete real-world validation.

Track B is the direction after Track-A Version-B. It should address broader validation outside Track-A constraints, including real temporal/session/environment/receiver conditions, cross-dataset validation, potentially cross-frequency evaluation, broader acquisition conditions and more realistic adversarial evaluation. Track B is not scientifically validated merely because its ingestion/extraction infrastructure exists.

## Frozen V-A vs V-B evidence
- Closed-set RF accuracy: 87.3899% vs 87.3899%.
- Known acceptance: 94.90% vs 94.90%.
- Unknown rejection: 29.49% vs 29.49%.
- Profile test accuracy after adaptation: 28.6629% vs 37.9704% (+9.3075 pp).
- Replay acceptance: 100% vs 1% (-99 pp).
- Replay hold: 0% vs 99% (+99 pp).
- Gain-drift acceptance: 100% vs 94.6809% (-5.3191 pp).
- Mean profile displacement: 0.995174 vs 0.969641.
- Target-like unknown contamination: 100% vs 100% — unresolved.

These are frozen Track-A evidence, not projections. Controlled/derived attack scenarios are explicitly labelled as such.

## Outcome interpretation
Demonstrated: reproducible Track-A pipeline, Version-A baseline, open-set evaluation in the defined setting, legitimate profile evolution in the tested scenario, protected update authorization, strong replay improvement in the tested controlled scenario, D8/D9/D10 demonstrations, final web demonstrator deployment, ManySig streaming ingestion, and ManySig full feature extraction/provenance.

Not demonstrated: universal Version-B superiority, prevention of target-like unknown contamination, arbitrary cross-frequency/cross-dataset generalization, complete real-world validation, Track-B scientific/ML validation, or formal proof of novelty against all prior art.

The 100% target-like unknown contamination result is the principal unresolved security limitation. It must remain visible in documentation/UI and must not be hidden or relabelled.

## Novelty hypothesis status
The original broad novelty idea (adaptive RF fingerprinting/profile updating itself) was narrowed after prior-art review because adaptive/online RF fingerprinting and profile updating already exist.

The remaining hypothesis concerns a security-oriented separation between RF recognition and authorization to modify a persistent RF identity/profile, especially under target-like unknown contamination/poisoning conditions.

Current status: implemented and tested research hypothesis, not formally proven novelty. Stronger novelty claims require targeted systematic prior-art validation and stronger evidence.

## B0-B2 boundary
M0 RF remains the Track-A recognition backbone. M1/M2 were weaker; M3 screening was promising relative to them but incomplete and below the RF control. No learned candidate is certified as a replacement. Do not fabricate learned-model results.

## Evidence language
Use exactly: Implemented / Tested / Demonstrated / Scientifically Validated. Do not silently upgrade evidence level.

Track A may use real SMoRFFI, controlled/derived synthetic scenarios and published-paper evidence. Controlled/derived observations must never be represented as source-dataset measurements.

## ManySig Track-B engineering checkpoint — 2026-09-02
ManySig has been acquired as `ManySig.pkl.zip` and preserved outside the Git repository. Its verified structure is:

`6 TX × 12 RX × 4 dates × 2 equalization states = 576 leaves`

Each leaf contains 1,000 bursts of shape `(256, 2)` float64 I/Q, giving **576,000 bursts total**.

A real-archive opcode-level streaming ingestion POC was completed. Selective and full-stream tests demonstrated bounded process memory at approximately **45–53 MiB peak RSS**, with approximately **14–17 MiB incremental RSS overhead**. The earlier informal `<=25–30 MB total RSS` target is not claimed; interpreter/runtime baseline makes it unsuitable as an absolute process-RSS target.

The full ManySig archive was streamed once to produce **576,000 per-burst feature records** using the 16 Track-A RF evidence feature definitions, written as 24 receiver/equalization Parquet partitions. Cryptographic manifest and extraction summary were generated. The derived Parquet files remain ignored by Git; provenance metadata and continuity documentation are tracked.

The engineering checkpoint is committed on branch `task/manysig-feature-extraction-runner-2026-09-02` at commit `0bee709552e440b620205ed4cd412a6625449f44` before this state-file update.

**Important:** ManySig feature extraction is an engineering input/provenance result. It is **not** Track-B scientific validation, classifier evaluation, adversarial validation, or evidence that the Track-A security hypothesis generalizes.

The ManySig source metadata does not verify a sample-rate field. A nominal **20 MHz** value is currently recorded only as an engineering default and **REQUIRES VALIDATION**.

## Current bounded phase — Track-B B1
The next implementation/research phase is **B1: ManySig Scientific Validation / Dataset Quality Analysis**.

B1 must build on the completed extraction and must not repeat the streaming POC or re-extract the 576 leaves unless a reproducibility check is specifically required. The purpose is to establish whether the extracted ManySig feature data are scientifically usable and to characterize their structure and limitations before model training or hypothesis testing.

B1 scope:
1. Verify manifest/schema/row-count/provenance integrity against the completed extraction artifacts.
2. Summarize coverage across TX, RX, date and equalization dimensions.
3. Perform feature-level sanity checks and descriptive distributions.
4. Identify obvious leakage, duplication, partitioning and split-design risks.
5. Examine receiver/date/equalization variation relevant to future validation design.
6. Compare feature definitions/behaviour with the frozen Track-A definitions where this is a methodological consistency check, without altering the Track-A baseline.
7. Record what ManySig can and cannot support scientifically, including the unresolved sample-rate metadata issue.
8. Produce a dated B1 validation report and explicit next-phase questions.

### B1 stop condition
Stop after the ManySig quality/provenance assessment, coverage analysis, feature sanity report, leakage/split-risk assessment and clearly stated scientific limitations/future questions are documented and verified.

Do **not** start unrestricted ML training, classifier benchmarking, broad model selection, adversarial/poisoning experiments, cross-dataset validation, or claims of scientific generalization in B1. Those require a new dated phase and explicit scope.

## Dataset acquisition status
Only ManySig has currently been acquired for Track-B work. The remaining qualified datasets are not required to complete B1 and should not block the ManySig quality-validation phase. Their acquisition remains future work for later cross-dataset validation.

## Reference and handoff artifacts
- Complete project reference: `docs/06_continuity/REFERENCE_REPORT_2026-08-31.md`
- Historical next-chat handoff: `docs/09_handoff/NEXT_CHAT_HANDOFF_2026-08-31.md`
- Historical Q/A continuation note: `docs/09_handoff/NEXT_CHAT_QA_NOTE.md`
- D8/D10 milestone addendum: `docs/06_continuity/D8_D10_TRACK_A_MILESTONE_ADDENDUM_2026-08-30.md`
- ManySig streaming POC: `docs/06_continuity/MANYSIG_REAL_STREAMING_POC_2026-09-02.md`
- ManySig full extraction report: `docs/06_continuity/MANYSIG_FULL_EXTRACTION_2026-09-02.md`
- ManySig manifest: `datasets/features/manysig/manifest.json`
- ManySig extraction summary: `datasets/features/manysig/extraction_summary.json`
- **Current handoff:** `docs/09_handoff/NEXT_CHAT_HANDOFF_2026-09-02.md`

## Repository discipline
- Preserve all historical documents, experiment artifacts, decisions, PRs and commits.
- No unnecessary deletion.
- No force-push or destructive history rewrite.
- `develop` is the active implementation branch.
- Synchronize `main` and `develop` only at agreed significant milestones.
- Preserve the accepted Track-A baseline before and throughout Track-B work.
- Use dated phase boundaries and stop conditions so each Antigravity chat can be closed cleanly with a handoff rather than accumulating unbounded context.
