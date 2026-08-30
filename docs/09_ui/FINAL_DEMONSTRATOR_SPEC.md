# Final Version-B Demonstrator

## Purpose
Present the frozen research evidence as an interactive, honest V-A vs V-B demonstrator. The site is presentation-only: it does not silently recompute or alter the frozen experiment results.

## Views
1. Overview — primary result and architecture story.
2. V-A vs V-B — complete frozen comparison table.
3. D8 Adaptation — profile evolution and update authorization.
4. D9 Security — replay, gain-drift and the retained target-like contamination limitation.
5. D10 Lifecycle — recognition → evaluation → authorization → evolution → audit.
6. Methodology — real-source vs derived-controlled provenance and limitations.

## Frozen numbers
- RF closed-set accuracy: 87.3899% (V-A and V-B; same M0 recognizer).
- Known acceptance: 94.90% (both).
- Unknown rejection: 29.49% (both).
- Profile test accuracy: 28.6629% frozen vs 37.9704% multi-evidence.
- Replay acceptance: 100% always-update vs 1% V-B.
- Replay hold: 0% vs 99% V-B.
- Gain-drift acceptance: 100% vs 94.6809%.
- Mean profile displacement: 0.995174 vs 0.969641.
- Target-like unknown contamination: 100% vs 100% — unresolved.

## Presentation rules
- Never label derived scenarios as real measurements.
- Never hide the unresolved target-like contamination case.
- Never imply a V-B RF-model accuracy improvement.
- Every future research-number change requires a new dated experiment artifact.

## Deployment
`ui/` is a static site suitable for GitHub Pages. `.github/workflows/deploy-version-b-ui.yml` deploys it from `main`.
