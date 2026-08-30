# Version-B Completion — Security Core

## Decision
Version-B security-core is frozen for UI/deployment work. It retains the proven Version-A Random Forest as the recognition backbone and adds the adaptive authorization/profile-security layer demonstrated through D8–D10. This is a deliberate scope decision: no unverified B1/B2 candidate-model number is presented as a result.

## Version-A vs Version-B evidence

| Metric | Version A control | Version B security core | Change |
|---|---:|---:|---:|
| Closed-set RF accuracy | 87.3899% | 87.3899% | 0 pp |
| Known acceptance | 94.90% | 94.90% | 0 pp |
| Unknown rejection | 29.49% | 29.49% | 0 pp |
| Profile test accuracy after update | 28.6629% frozen | 37.9704% multi-evidence | +9.3075 pp |
| Accepted profile updates | 0 | 4,799 / 4,950 | adaptive |
| Held updates | 0 | 151 / 4,950 | +151 |
| Mean profile displacement L2 | 0.995174 always-update | 0.969641 multi-evidence | -2.56% |
| Replay acceptance | 100% always-update | 1% multi-evidence | -99% |
| Replay hold | 0% | 99% | +99 pp |
| Gain-drift acceptance | 100% always-update | 94.6809% | -5.3191 pp |
| Target-like unknown contamination | 100% | 100% | unresolved |

## Interpretation
Version-B provides a materially stronger adaptive-security result than an always-update profile manager: exact replay is almost completely quarantined, profile evolution remains possible, and profile displacement is modestly reduced. The result is not a universal improvement in every metric. Target-like unknown contamination remains a falsifying boundary condition and must be shown prominently in the UI rather than hidden.

## D8
D8 is demonstrated using the frozen 1–33 known-device protocol, 50-observation enrollment, 150-observation update stream and a frozen 4,996-observation known test set protected from updates. The source-row ordering used for the stream is engineering chronology only; SMoRFFI does not supply trustworthy temporal/session metadata.

## D9
D9 controlled/derived attacks demonstrate strong replay protection under multi-evidence, but not resistance to target-like unknown contamination. Attack data are derived from real observations and are explicitly labelled as controlled scenarios.

## D10
D10 demonstrates an end-to-end lifecycle: legitimate recognition and update, legitimate profile evolution, unknown rejection, first suspicious target-like event acceptance, repeated-event replay quarantine, profile version progression and audit events.

## B1/B2 boundary
The repository's B0–B2 benchmark contract defines M0–M3 candidates, but B1/B2 candidate-model training/evaluation is not certified in the current repository. Therefore no CNN/metric-learning/contrastive accuracy is invented. The UI-freeze Version-B is defined as the security-core extension over M0. A future model-selection study can be added as a separate experiment without rewriting these frozen results.

## UI freeze rule
From this milestone forward, presentation work may improve layout, charts, wording, navigation and deployment. Frozen experiment numbers, provenance labels and limitations must not be changed except by adding a new dated experiment artifact.
