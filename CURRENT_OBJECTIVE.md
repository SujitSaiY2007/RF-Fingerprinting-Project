# CURRENT OBJECTIVE

## Current checkpoint — Track-A Version-B baseline established; Track-B ManySig preparation started
Track-A Version-B security core is demonstrated and the professional web demonstrator is deployed. The Q/A truth-audit has been completed, the current evidence/limitations have been consolidated, and the complete solo project reference/handoff artifacts have been prepared.

The project is now treated as one complete project executed through constrained tracks:

`Complete Project -> Track A under constraints -> Track-A Version-B final demonstrator baseline -> Track B broader validation -> desired end product`

Track A is complete to its intended demonstration ceiling. Track B is the planned future research/validation direction and is not a completed result.

## Agreed project direction — Track A -> Track B
Track A was deliberately created as a quicker, controlled, reproducible implementation and ideation track for the final product demonstrator. It established Version A, improved it into Version B, generated evidence, exposed limitations and produced the working demonstrator.

Track A has a defined ceiling because of its agreed constraints. It should not be presented as universal RF generalization or as complete real-world validation.

Track B is the planned future direction after Track-A Version-B. It should address broader validation outside Track-A constraints, including real temporal/session/environment/receiver conditions, cross-dataset validation, potentially cross-frequency evaluation, broader acquisition conditions and more realistic adversarial evaluation. Track B is future work, not a completed result.

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
Demonstrated: reproducible Track-A pipeline, Version-A baseline, open-set evaluation in the defined setting, legitimate profile evolution in the tested scenario, protected update authorization, strong replay improvement in the tested controlled scenario, D8/D9/D10 demonstrations, and final web demonstrator deployment.

Not demonstrated: universal Version-B superiority, prevention of target-like unknown contamination, arbitrary cross-frequency/cross-dataset generalization, complete real-world validation, or formal proof of novelty against all prior art.

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

## Current Track-B ManySig preparation checkpoint — 02 September 2026
ManySig has now been acquired locally and non-destructively inspected with Antigravity IDE. It is retained outside Git as raw data and remains a Track-B validation/reproduction/cross-condition resource; it does not replace the frozen Track-A SMoRFFI baseline.

Verified ManySig structure:
- Python Pickle Protocol 3;
- top-level keys: `tx_list`, `rx_list`, `capture_date_list`, `equalized_list`, `max_sig`, `data`;
- 6 transmitters;
- 12 receivers;
- 4 March 2021 capture dates;
- 2 equalization states;
- `data[tx][rx][date][eq]` hierarchy;
- 576 leaf arrays;
- each leaf `(1000, 256, 2)` `float64`;
- 576,000 signal bursts;
- compressed archive ~1.355 GB and contained pickle ~2.197 GB.

Detailed evidence record:
`docs/06_continuity/MANYSIG_INSPECTION_2026-09-02.md`

### Immediate next boundary
Before final feature extraction, verify the proposed incremental/chunked ingestion mechanism with a small controlled memory test. The previously reported <=25–30 MB peak-RAM figure is not yet scientifically/experimentally verified.

Only after ingestion behaviour is demonstrated should the project define the exact ManySig experiment, extraction schema and feature set. Do not load/extract the full dataset merely for inspection.

## Reference and handoff artifacts
- Complete project reference: `docs/06_continuity/REFERENCE_REPORT_2026-08-31.md`
- ManySig inspection: `docs/06_continuity/MANYSIG_INSPECTION_2026-09-02.md`
- Current next-chat handoff: `docs/09_handoff/NEXT_CHAT_HANDOFF_2026-09-02.md`
- Previous handoff: `docs/09_handoff/NEXT_CHAT_HANDOFF_2026-08-31.md`
- Historical Q/A continuation note: `docs/09_handoff/NEXT_CHAT_QA_NOTE.md`
- D8/D10 milestone addendum: `docs/06_continuity/D8_D10_TRACK_A_MILESTONE_ADDENDUM_2026-08-30.md`

## Repository discipline
- Preserve all historical documents, experiment artifacts, decisions, PRs and commits.
- No unnecessary deletion.
- No force-push or destructive history rewrite.
- `develop` is the active implementation branch.
- Synchronize `main` and `develop` at agreed significant milestones.
- The current accepted Track-A state must be preserved before Track-B work begins.
- Raw datasets and secrets such as GitHub Personal Access Tokens must never be committed to the repository.
