# NEXT CHAT HANDOFF — VERSION B / D8

Date: 2026-08-30
Repository: `SujitSaiY2007/RF-Fingerprinting-Project`
Canonical development branch: `develop`
Canonical stable branch: `main`

## START HERE

Read these files before doing any work:
1. `PROJECT_STATE.md`
2. `CURRENT_HANDOFF.md`
3. `CURRENT_OBJECTIVE.md`
4. `docs/04_research/D7_D10_TRACK_A_NEXT_DIRECTION.md`
5. `docs/04_research/VERSION_B_RESEARCH_SPECIFICATION.md`
6. `configs/version_b_b0_b2_benchmark.json`
7. `configs/d8_profile_policies.json`
8. `src/d8_profile_manager.py`
9. `scripts/run_d8_evaluation.py`
10. `ui/README_VERSION_B.md`

## DO NOT REPEAT

- Do not redo D1 or D2.
- Do not change the frozen D2 representation: `serialized preamble -> complex[288] -> float32[2,288] I/Q`.
- Do not replace the Version-A RF control before evidence justifies it.
- Do not treat historical ~91.1% as reconstructed evidence.
- Do not redo B0.
- Do not rerun or reinterpret the rejected/compute-limited M1/M2/M3 screening as if it were a valid model-selection result.
- Do not claim D8 is demonstrated yet.
- Do not represent synthetic/derived data as source-dataset measurements.
- Do not use the evaluation set to train, tune thresholds, update profiles, or select the method.

## CURRENT PROJECT POSITION

Version A is the frozen control:
- closed-set RF accuracy: 87.39%
- macro-F1: 87.32%
- balanced accuracy: 87.41%
- D6 RF known acceptance: ~94.90%
- D6 RF unknown rejection: 29.49%
- D7 gain/AWGN experiments demonstrate strong acquisition sensitivity.

Version B preserves RF recognition as the control backbone and focuses on open-set security, fingerprint-purity/acquisition dependence, protected profile adaptation, poisoning resistance and auditable application integration.

## D8 STATUS

D8 is one complete stage. Do not subdivide it into D8.x stages.

Implemented:
- persistent profiles
- profile versions
- running mean/variance state
- chronological leakage guard
- ACCEPT_UPDATE / HOLD / REJECT
- four policy ladder
- bounded update step
- audit history/export

Not yet demonstrated:
- real chronological SMoRFFI evaluation of all four policies
- before/after recognition metrics
- profile displacement results
- legitimate adaptation retention
- unknown false-acceptance behavior under profile evolution
- rollback/recovery evidence

The current runner accepts a precomputed chronological evidence stream. It intentionally does not invent recognition metrics. A proper D8 evaluation harness must construct evidence from the frozen RF pipeline and real SMoRFFI observations, then freeze evaluation before update processing.

## REQUIRED D8 EVALUATION

Use one chronological stream. Establish initial profiles from an explicitly defined enrollment segment. Freeze evaluation observations before update-stream processing.

Compare:
1. frozen/no-update
2. always-update
3. confidence-only
4. multi-evidence

Report:
- recognition accuracy before/after
- known acceptance
- unknown rejection / false acceptance
- update / hold / reject rates
- profile displacement
- profile version evolution
- legitimate adaptation retained
- audit completeness
- rollback/recovery where implemented

The current thresholds in `configs/d8_profile_policies.json` are engineering defaults, not scientifically validated values. They must be calibrated/justified without leaking evaluation data.

## NEXT TECHNICAL PRIORITY

Build the missing D8 evaluation harness around the existing RF feature/recognition pipeline. Do not invent a new input schema. Then execute the complete chronological comparison and record results under `experiments/track_a/`.

After D8 is actually Tested and Demonstrated, proceed to D9 poisoning. D9 must attack the persistent profile lifecycle, not merely the static classifier.

## UI PARALLEL WORKSTREAM

Continue the UI shell in parallel using `ui/README_VERSION_B.md`. The frontend must not implement security decisions. Mock data must be visibly marked MOCK; real SMoRFFI and derived/controlled scenarios must remain distinguishable.

## BRANCH RULE

Work on `develop`. After an explicitly agreed significant milestone, synchronize `main`. The 2026-08-30 synchronization was performed as a two-parent merge commit so prior main history remains reachable; a pre-sync archive branch also exists:
`archive/main-before-version-b-sync-2026-08-30`.

## SCIENTIFIC STATUS VOCABULARY

Implemented = code exists.
Tested = tests pass.
Demonstrated = integrated experiment is executed and recorded.
Scientifically Validated = claim survives appropriate independent/held-out evidence.

Do not promote one status to another without evidence.
