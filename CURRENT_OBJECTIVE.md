# CURRENT OBJECTIVE

## Current checkpoint — Track-B B1 ManySig Scientific Validation COMPLETE; Consolidated on main; Next direction Phase B2 Split Design & Community-Aware Modeling
Track-A Version-B baseline remains frozen and demonstrator deployed. The ManySig streaming feature extraction and Track-B B1 Scientific Validation have been fully executed, verified, and documented. The repository has been consolidated onto main as the sole active working branch.

The project is executed through two disciplined tracks:

Complete Project -> Track A under constraints (FROZEN BASELINE) -> Track-B ManySig Streaming Ingestion (COMPLETE) -> Track-B Feature Extraction (COMPLETE) -> Track-B B1 Scientific Validation (COMPLETE) -> Track-B B2 Split Design & Community-Aware Engine -> desired end product

Track-A remains complete to its defined ceiling. Track-B B1 has established the empirical data quality, 16-feature distributions, and environmental confounding bounds of ManySig ( = 576,000$ bursts) before machine learning.

### Track-B Completed Milestones
1. **ManySig Streaming Ingestion POC:** Demonstrated bounded-memory opcode streaming unpickler (src/manysig_streamer.py, .84\text{ MiB}$ peak RSS), superseding the synthetic unpickling limitation documented in 	ools/manysig_streaming_poc.py and docs/06_continuity/MANYSIG_STREAMING_POC_2026-09-02.md.
2. **ManySig Feature Extraction:** Extracted all 576 leaves (,000\text{ bursts}$) into 24 Parquet partitions (.4\text{ MB}$, datasets/features/manysig/) matching the frozen 16-feature contract.
3. **Track-B B1 Scientific Validation:** Completed empirical data-quality audit, 16-feature sanity analysis, ANOVA variance decomposition, coordinate duplication checks, leakage hazard evaluation, and sample-rate sensitivity audit (docs/06_continuity/MANYSIG_B1_VALIDATION_2026-09-06.md, experiments/track_b/manysig_b1_validation_results.json).

### Track-B Next Objectives (Phase B2 & Community Integration)
1. **Formalize Leak-Free Split Protocol:** Implement split-generation routines adhering to DEC-035 (Receiver Holdout, Date Holdout, Transmitter Open-Set Holdout, Equalization Holdout).
2. **Establish Track-B Recognition Baselines:** Benchmark baseline classifiers under leak-free split protocols.
3. **Quantify Receiver Penalty Hypothesis:** Test whether moving from matched-receiver evaluation to unseen cross-receiver evaluation induces an estimated 30-percentage-point performance drop (to be empirically tested, not assumed).
4. **Community-Aware Subsystem Design:** Implement synthetic IoT topology generator (=50$ nodes) to provide graph-level co-occurrence and routing evidence for device authentication.

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
Demonstrated: reproducible Track-A pipeline, Version-A baseline, open-set evaluation in the defined setting, legitimate profile evolution in the tested scenario, protected update authorization, strong replay improvement in the tested controlled scenario, D8/D9/D10 demonstrations, final web demonstrator deployment, ManySig streaming ingestion, ManySig full feature extraction/provenance, and ManySig B1 dataset-quality validation.

Not demonstrated: universal Version-B superiority, prevention of target-like unknown contamination, arbitrary cross-frequency/cross-dataset generalization, complete real-world validation, Track-B ML benchmarks/classification models, or formal proof of novelty against all prior art.

The 100% target-like unknown contamination result is the principal unresolved security limitation. It must remain visible in documentation/UI and must not be hidden or relabelled. Proposed community-aware gating targets reducing contamination to <10% while preserving >=90% legitimate adaptation as an engineering acceptance criterion, not an already demonstrated result.

## Novelty hypothesis status
The original broad novelty idea (adaptive RF fingerprinting/profile updating itself) was narrowed after prior-art review because adaptive/online RF fingerprinting and profile updating already exist.

The remaining hypothesis concerns a security-oriented separation between RF recognition and authorization to modify a persistent RF identity/profile, especially under target-like unknown contamination/poisoning conditions.

Current status: implemented and tested research hypothesis, not formally proven novelty. Stronger novelty claims require targeted systematic prior-art validation and stronger evidence.

## B0-B2 boundary
M0 RF remains the Track-A recognition backbone. M1/M2 were weaker; M3 screening was promising relative to them but incomplete and below the RF control. No learned candidate is certified as a replacement. Do not fabricate learned-model results.

## Evidence language
Use exactly: Implemented / Tested / Demonstrated / Scientifically Validated. Do not silently upgrade evidence level.

Track A may use real SMoRFFI, controlled/derived synthetic scenarios and published-paper evidence. Controlled/derived observations must never be represented as source-dataset measurements.

## ManySig Track-B engineering & B1 validation summary
ManySig has been acquired as ManySig.pkl.zip and preserved outside the Git repository. Its verified structure is:

6 TX × 12 RX × 4 dates × 2 equalization states = 576 leaves

Each leaf contains 1,000 bursts of shape (256, 2) float64 I/Q, giving **576,000 bursts total**.

A real-archive opcode-level streaming ingestion POC was completed with approximately **45–53 MiB peak RSS**, with approximately **14–17 MiB incremental RSS overhead**.

The full ManySig archive was streamed to produce **576,000 per-burst feature records** using the 16 Track-A RF evidence feature definitions, written as 24 receiver/equalization Parquet partitions (.4\text{ MB}$, datasets/features/manysig/).

The Track-B B1 Scientific Validation established data integrity (\%$ finite, non-null, 0 duplicate feature vectors), perfect factorial balance (,000\text{ bursts/cell}$), strong receiver confounding (intra-TX cross-receiver distance equals inter-TX distance at .00\times$), equalization manifold shift (.41\times$), and sample-rate sensitivity ( = 20.0\text{ MHz}$ is REQUIRES VALIDATION (Engineering default)).

## Reference and handoff artifacts
- Complete project reference: docs/06_continuity/REFERENCE_REPORT_2026-08-31.md
- ManySig inspection: docs/06_continuity/MANYSIG_INSPECTION_2026-09-02.md
- ManySig synthetic streaming POC: docs/06_continuity/MANYSIG_STREAMING_POC_2026-09-02.md
- ManySig real streaming POC: docs/06_continuity/MANYSIG_REAL_STREAMING_POC_2026-09-02.md
- ManySig full extraction report: docs/06_continuity/MANYSIG_FULL_EXTRACTION_2026-09-02.md
- ManySig manifest: datasets/features/manysig/manifest.json
- ManySig extraction summary: datasets/features/manysig/extraction_summary.json
- ManySig Track-B B1 validation report: docs/06_continuity/MANYSIG_B1_VALIDATION_2026-09-06.md
- ManySig B1 validation artifact: experiments/track_b/manysig_b1_validation_results.json
- Historical next-chat handoff: docs/09_handoff/NEXT_CHAT_HANDOFF_2026-08-31.md
- Historical Q/A continuation note: docs/09_handoff/NEXT_CHAT_QA_NOTE.md
- D8/D10 milestone addendum: docs/06_continuity/D8_D10_TRACK_A_MILESTONE_ADDENDUM_2026-08-30.md

## Repository discipline
- Preserve all historical documents, experiment artifacts, decisions, PRs and commits.
- No unnecessary deletion.
- No force-push or destructive history rewrite.
- main is the sole active working branch for all future implementation, documentation, and handoffs.
- Preserve the accepted Track-A baseline before and throughout Track-B work.
- Raw datasets and secrets such as GitHub Personal Access Tokens must never be committed to the repository.
