# Final Version-B Demonstrator

This static site presents the frozen Track-A research evidence in a professional RF fingerprinting dashboard format. It is intentionally not a live RF inference backend.

**Source of truth:** `experiments/track_a/version_b_final_results.json`

**Current views:**
- Command Center — current Track-A stage, system path, recognition KPIs, update stream and evidence boundary.
- V-A vs V-B — frozen comparison matrix and interpretation boundary.
- D8 Adaptation — profile evolution, update decisions and recognition/authorization separation.
- D9 Security — controlled replay, gain-drift and target-like unknown results.
- D10 Lifecycle — integrated observation-to-audit flow.
- Methodology — source/derived evidence, controls and current scientific claim boundary.

**Deployment:** GitHub Pages workflow publishes `ui/` from `main` after the repository Pages deployment is enabled.

**Truthfulness rule:** controlled/derived scenarios are explicitly labelled; the unresolved target-like unknown contamination result remains visible; no Track-B or live-backend functionality is represented as completed.
