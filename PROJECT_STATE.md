# PROJECT STATE

**Last updated:** 2026-09-02

## Authoritative status
- Repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Stable branch: `main`
- Integration branch: `develop`
- Current phase: **Track-A Version-B baseline frozen; Track-B ManySig ingestion and full feature-extraction infrastructure demonstrated; next direction Track-B scientific validation**
- D2 learning gate: **PASSED**
- D7 Track A: **COMPLETE / DEMONSTRATED**
- B0-B2: **COMPLETE AS MODEL-SELECTION SCREENING / DEMONSTRATED — no learned candidate justified replacing the RF control**
- D8: **DEMONSTRATED**
- D9: **DEMONSTRATED — replay protection strong; target-like unknown contamination unresolved**
- D10: **DEMONSTRATED — integrated lifecycle**
- Final web demonstrator: **DEPLOYED via GitHub Pages**
- Track-B ManySig streaming ingestion POC: **COMPLETED / VERIFIED**
- Track-B ManySig full 576-leaf feature extraction: **COMPLETED / VERIFIED as engineering execution and provenance**
- Current activity: **Track-B ManySig scientific validation/quality analysis; no Track-B ML/scientific validation result yet**

## Project strategy: Track A -> Track B
The project is treated as one complete project executed through constrained tracks:

`Complete Project -> Track A under constraints -> Track-A Version-B final demonstrator baseline -> Track B broader validation -> desired end product`

Track A was deliberately established as a quicker, controlled, reproducible implementation and ideation track for the final product demonstrator. Its purpose was to establish the RF pipeline, create Version A, improve it into Version B, generate evidence, identify architectural limits, and produce a working demonstrator without waiting for the broader validation burden of Track B.

Track A is not an inferior or disposable track. It is a constrained evidence-producing foundation. Its agreed constraints impose a ceiling on generalization claims.

The intended future direction is **Track B after Track-A Version-B**. Track B is responsible for broader validation beyond Track-A constraints, including real temporal/session/environment/receiver conditions, cross-dataset validation, potentially cross-frequency validation, and more realistic adversarial evaluation. Track B must not be presented as already completed.

## What Track A has achieved
The Track-A progression is:

`SMoRFFI -> D2 representation -> Version-A RF baseline -> B0-B2 model screening -> Version-B protected adaptive profiles -> D8 -> D9 -> D10 -> web demonstrator`

Version A established the recognition control. Version B retained the RF recognition backbone and improved the security/governance surrounding persistent profile updates. The project therefore demonstrates a complete Track-A concept-to-demonstrator flow.

## Frozen D2 contract
`serialized preamble -> complex[288] -> float32[2,288] I/Q`

Do not restart D1/D2 or silently change the input schema. Baseline preprocessing remains without per-observation normalization, clipping, filtering, resampling or arbitrary interpolation. Device number/MAC is label/provenance only.

## Version-A frozen reference
SMoRFFI known devices 1–33; deterministic 70/15/15 engineering split; 16 deterministic RF evidence features; fixed Random Forest: 100 trees, `random_state=20260830`, `max_features=sqrt`, no tuning.

- Accuracy: **87.3899%**
- Macro-F1: **87.3226%**
- Balanced accuracy: **87.4117%**
- D6 RF confidence threshold: **0.30**
- Known acceptance: **94.90%**
- Unknown rejection: **29.49%**

Historical ~91.1% remains historical/unreconstructed and is not a certified result.

## Version-B model-selection boundary
The frozen B0-B2 benchmark retains M0 RF as the Track-A recognition backbone. M1 compact I/Q CNN and M2 I/Q metric/prototype head were weaker. M3 supervised-contrastive prototype screening was promising relative to M1/M2 but incomplete and materially below the RF control. No learned candidate is certified as a replacement.

This is a legitimate negative model-selection result and must remain in the audit trail. It does not prove RF is globally optimal.

## Version-B architecture
Working Track-A architecture:

`SMoRFFI observation -> D2 -> RF evidence / RF recognition -> open-set novelty decision -> D8 update authorization -> persistent profile -> D9 poisoning defense -> audit/final decision`

The core security design separates:
`OBSERVATION -> RECOGNITION -> UPDATE AUTHORIZATION -> PROFILE UPDATE`

Required update outcomes are:
- ACCEPT / UPDATE
- HOLD / QUARANTINE
- REJECT

## Frozen V-A vs V-B evidence
- Closed-set RF accuracy: **87.3899% vs 87.3899%** — same recognizer; no unsupported model gain claimed.
- Known acceptance: **94.90% vs 94.90%**.
- Unknown rejection: **29.49% vs 29.49%**.
- Profile test accuracy after adaptation: **28.6629% vs 37.9704% (+9.3075 pp)**.
- Replay acceptance: **100% vs 1% (-99 pp)**.
- Replay hold: **0% vs 99% (+99 pp)**.
- Gain-drift acceptance: **100% vs 94.6809% (-5.3191 pp)**.
- Mean profile displacement: **0.995174 vs 0.969641**.
- Target-like unknown contamination: **100% vs 100% — unresolved**.

These values are frozen Track-A evidence, not projections. Controlled/derived attack scenarios are explicitly labelled as such.

## Outcome status
### Demonstrated / working
- Reproducible Track-A RF pipeline on SMoRFFI.
- Version-A RF control.
- Open-set evaluation in the defined setting.
- Legitimate adaptive profile evolution in the tested scenario.
- Protected update authorization and quarantine behaviour.
- Strong replay improvement in the tested controlled scenario.
- D8 profile evolution.
- D9 controlled poisoning/security evaluation.
- D10 integrated lifecycle.
- Final web demonstrator and GitHub Pages deployment.
- ManySig archive schema inspection.
- ManySig bounded-memory streaming ingestion POC.
- ManySig full 576-leaf / 576,000-burst feature extraction and partitioned feature-data provenance.

### Partially achieved / limited
- General poisoning resistance: only selected tested attack classes improved.
- Gain-drift handling: improved control but not perfect acceptance.
- Profile evolution: demonstrated in the tested Track-A setting, not general real-world validation.
- ManySig sample-rate metadata: **20 MHz is an engineering default and requires validation; it is not a verified source-dataset fact.**

### Not achieved / not demonstrated
- Prevention of target-like unknown contamination: **100% remains accepted in the tested scenario**.
- Universal Version-B superiority over Version A.
- Generalization across arbitrary real RF frequencies/datasets/acquisition conditions.
- Formal proof that the narrowed novelty hypothesis is new relative to all prior art.
- Track-B scientific/ML validation.
- Cross-dataset validation using the remaining datasets.

## Novelty hypothesis status
The original broad hypothesis — that adaptive RF fingerprinting/profile updating itself is novel — was narrowed after prior-art review because adaptive/online RF fingerprinting and profile updating already exist.

The remaining research hypothesis concerns a security-oriented separation between RF recognition and authorization to modify a persistent RF identity/profile, particularly under target-like unknown contamination/poisoning conditions.

Current status: **implemented and tested research hypothesis; not formally proven novelty**. The 100% target-like unknown contamination result is a central limitation and prevents a claim that Version B has solved target-like profile poisoning. A stronger novelty claim requires targeted systematic prior-art validation and stronger evidence.

## Evidence language
Use exactly: **Implemented / Tested / Demonstrated / Scientifically Validated**. Do not upgrade evidence level silently.

Track A may use real SMoRFFI, controlled/derived synthetic scenarios and published-paper evidence. Synthetic/derived observations must never be represented as source-dataset measurements.

## Track-B current checkpoint — ManySig
ManySig has been acquired as `ManySig.pkl.zip` outside the Git repository and preserved as the original raw archive. Verified structure:

`6 TX × 12 RX × 4 dates × 2 equalization states = 576 leaves`

Each leaf contains 1,000 bursts, each burst shaped `(256, 2)` with `float64` I/Q, for **576,000 bursts total**.

The raw archive must remain outside Git. Derived Parquet feature partitions are also intentionally ignored by Git; reproducibility is represented through tracked manifests, summaries and dated continuity documentation.

The real-archive streaming POC demonstrated bounded process memory with approximately **45–53 MiB peak RSS** and approximately **14–17 MiB incremental RSS overhead** across selective and full-stream tests. The earlier informal `<=25–30 MB total RSS` target is not a valid absolute-process target and is not claimed as achieved.

The full feature extraction generated **576,000 per-burst records** using the 16 Track-A RF evidence feature definitions and 24 receiver/equalization partitions. The extraction and cryptographic provenance were completed and committed on branch `task/manysig-feature-extraction-runner-2026-09-02` at commit `0bee709552e440b620205ed4cd412a6625449f44`.

The extracted feature dataset is an **engineering input artifact, not yet a scientific result**. The next bounded phase is ManySig scientific validation/quality analysis.

## Track-B future direction
Track B should build on the Track-A demonstrator rather than restart it. Candidate future work includes:
- cross-dataset real RF validation;
- temporal/session/environment/receiver variation;
- potentially cross-frequency evaluation;
- broader device populations and acquisition conditions;
- more realistic adversarial/target-like contamination scenarios;
- improved mechanisms specifically addressing the Track-A target-like unknown failure;
- stronger novelty/prior-art validation.

## Next bounded phase
The next chat/session is limited to **Track-B Phase B1: ManySig Scientific Validation / Dataset Quality Analysis**.

B1 should establish whether the extracted ManySig feature table is scientifically usable and what structure/variation it contains, without yet claiming classifier performance or Track-B hypothesis validation. It should include provenance/schema integrity checks, per-receiver/date/equalization coverage checks, feature distributions and sanity checks, identification of leakage risks, and a controlled comparison of ManySig feature behaviour with the frozen Track-A feature definitions where scientifically appropriate.

**B1 stop condition:** once the ManySig feature dataset has a documented quality/provenance assessment, coverage summary, feature sanity report, and clearly stated limitations/next experimental questions, stop and produce a handoff. Do not begin unrestricted ML training, adversarial experiments, cross-dataset experiments, or broad model selection in B1 unless a later dated phase explicitly authorizes them.

## Final demonstrator
The web application is separated from the RF engine. Current/planned UI surfaces include Dashboard, Identification, Device Profiles, Open-Set Security, Security/Attack Lab, Audit Trail and Evaluation/Research. The UI must present frozen results, methodology, provenance and limitations without inventing measurements.

## Current checkpoint artifacts
- Complete project reference: `docs/06_continuity/REFERENCE_REPORT_2026-08-31.md`
- Next-chat handoff: `docs/09_handoff/NEXT_CHAT_HANDOFF_2026-08-31.md`
- Historical Q/A continuation note: `docs/09_handoff/NEXT_CHAT_QA_NOTE.md`
- D8/D10 milestone addendum: `docs/06_continuity/D8_D10_TRACK_A_MILESTONE_ADDENDUM_2026-08-30.md`
- ManySig streaming POC report: `docs/06_continuity/MANYSIG_REAL_STREAMING_POC_2026-09-02.md`
- ManySig full extraction report: `docs/06_continuity/MANYSIG_FULL_EXTRACTION_2026-09-02.md`
- ManySig extraction manifest: `datasets/features/manysig/manifest.json`
- ManySig extraction summary: `datasets/features/manysig/extraction_summary.json`

## Repository discipline
- Preserve all historical documents, experiment artifacts, decisions, PRs and commits.
- No unnecessary deletion.
- No force-push or destructive history rewrite.
- `develop` is the active implementation branch.
- `main` is synchronized with `develop` at agreed significant milestones.
- Before new Track-B implementation, preserve the accepted Track-A baseline and explicitly define the new dated research boundary.
