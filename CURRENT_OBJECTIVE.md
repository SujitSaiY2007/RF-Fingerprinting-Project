# CURRENT OBJECTIVE

## Current milestone — Version-B security core complete
Version-B security-core is now frozen for presentation/UI work. The proven Version-A Random Forest (M0) remains the immutable recognition backbone. Version-B adds the security-oriented separation between recognition and authorization to modify persistent RF profiles, with demonstrated adaptive profile evolution, replay quarantine, controlled gain-drift handling and full lifecycle/audit behaviour.

The final frozen comparison is recorded in:
- `experiments/track_a/version_b_final_results.json`
- `docs/08_execution/VERSION_B_COMPLETION.md`

## Frozen V-A vs V-B evidence
- Closed-set RF accuracy: 87.3899% vs 87.3899% (same recognizer; no unsupported model gain claimed).
- Known acceptance: 94.90% vs 94.90%.
- Unknown rejection: 29.49% vs 29.49%.
- Profile test accuracy after adaptation: 28.6629% frozen vs 37.9704% multi-evidence (+9.3075 pp).
- Replay acceptance: 100% always-update vs 1% multi-evidence (-99 pp).
- Replay hold: 0% vs 99% (+99 pp).
- Gain-drift acceptance: 100% vs 94.6809% (-5.3191 pp).
- Target-like unknown contamination: 100% vs 100% — unresolved falsifying boundary condition.

These values are frozen evidence, not projections. Controlled/derived attack scenarios are explicitly labelled as such.

## B1/B2 model-selection boundary
The repository's original B0-B2 benchmark contract defines M0–M3 candidate models. B0 is numerically reproduced. Candidate-model B1/B2 training/evaluation is not certified in the current repository. No CNN/metric-learning/contrastive result is fabricated. For the completed Version-B security-core milestone, M0 is intentionally retained as the recognition backbone so the research conclusion rests on measured D8-D10 security behaviour rather than an unverified model substitution. A future B1/B2 model-selection study is a separate experiment and must not rewrite these frozen numbers.

## D8-D10 status
- D8: Demonstrated — chronological engineering stream, frozen test protection, four update policies, profile evolution evidence.
- D9: Demonstrated — controlled/derived poisoning evaluation; replay protection strong, target-like unknown contamination remains unresolved.
- D10: Demonstrated — integrated lifecycle, unknown rejection, profile evolution, replay quarantine and audit events.

## Version-B UI / website is now the only active development direction
From this milestone onward, research numbers and security logic are frozen unless a new dated experiment is intentionally opened. Work should focus on:
1. authoritative backend/API integration;
2. UI/UX refinement;
3. V-A vs V-B comparison dashboards;
4. D8/D9/D10 visualizations;
5. provenance and REAL_SOURCE_DATA vs DERIVED_CONTROLLED_DATA presentation;
6. methodology/limitations pages;
7. attack-lab demonstrations;
8. responsive design and accessibility;
9. GitHub Pages/deployment verification;
10. final project presentation and documentation.

## Scientific guardrail
Do not claim that Version B is universally superior. The defensible conclusion is narrower: Version B materially improves measured adaptive-security behaviour over an always-update profile manager, especially replay handling and profile evolution, while retaining the Version-A recognizer; target-like unknown contamination remains a known weakness. Any stronger conclusion requires a new experiment.

## Repository discipline
Large raw datasets remain outside Git. Material decisions/results/limitations belong in GitHub. `main` and `develop` should be synchronized at the end of an agreed significant milestone; future UI work should proceed through the established development/PR discipline.
