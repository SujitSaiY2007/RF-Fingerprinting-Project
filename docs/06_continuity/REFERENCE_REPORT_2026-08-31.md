# Complete Project Reference Report — 31 August 2026

This Markdown copy is the repository companion to the complete professional reference report prepared on 31 August 2026. It preserves the current Track-A Version-B state, experimental boundaries, novelty status, demonstration history and Track-B roadmap in a GitHub-readable form.

## Canonical interpretation

The project is treated as **one complete project executed through constrained tracks**, not as two unrelated projects:

`Complete Project -> Track A under constraints -> Track-A Version B final demonstrator baseline -> Track B broader validation -> desired end product`

Track A was intentionally the faster controlled/reproducible implementation and ideation path. Track B is the future strengthening/validation path and is not completed.

## Current Track-A position

Track A progressed through:

`SMoRFFI -> D2 representation -> Version-A RF control -> B0-B2 model screening -> Version-B protected adaptive profiles -> D8 -> D9 -> D10 -> professional web demonstrator`

Version A is the frozen recognition control. Version B retains the RF recognition backbone and adds security-oriented separation between recognition and authorization to modify persistent RF identity/profile state.

## Frozen evidence

| Measure | Version A | Version B | Interpretation |
|---|---:|---:|---|
| Closed-set RF accuracy | 87.3899% | 87.3899% | Same recognition backbone; no model-accuracy gain claimed |
| Known acceptance | 94.90% | 94.90% | Recognition/open-set control unchanged |
| Unknown rejection | 29.49% | 29.49% | Open-set control unchanged in this setting |
| Profile test accuracy after adaptation | 28.6629% | 37.9704% | +9.3075 pp in tested adaptation scenario |
| Replay acceptance | 100% | 1% | Strong improvement in tested controlled replay scenario |
| Replay hold | 0% | 99% | Strong improvement in tested controlled replay scenario |
| Gain-drift acceptance | 100% | 94.6809% | Some handling, but not perfect |
| Mean profile displacement | 0.995174 | 0.969641 | Smaller mean movement under Version B |
| Target-like unknown contamination | 100% | 100% | Principal unresolved security limitation |

These values are frozen Track-A evidence. They are not projections or universal performance claims.

## Evidence-level discipline

Use four distinct levels:

1. **Implemented** — the mechanism exists in the project.
2. **Tested** — it was exercised under a defined test protocol.
3. **Demonstrated** — the result was observed in the defined Track-A setting.
4. **Scientifically Validated** — broader evidence supports the claim against the required validation conditions.

Track A provides substantial implemented/tested/demonstrated evidence. It does not by itself establish universal scientific validation.

## D8 / D9 / D10

- **D8:** demonstrates chronological profile evolution and protected update authorization in the tested setting.
- **D9:** demonstrates controlled security/poisoning evaluation, with particularly strong replay protection but unresolved target-like unknown contamination.
- **D10:** demonstrates the integrated lifecycle from observation through recognition, open-set decision, update authorization, persistent profile handling, security response and audit/final decision.

These are engineering/research demonstrations under the stated Track-A conditions. They do not prove complete real-world robustness.

## Target-like unknown result

The 100% target-like unknown contamination result must remain visible. It means the tested target-like unknown observations were accepted/allowed through the relevant contamination pathway for both versions. Therefore Version B cannot be described as solving target-like poisoning/profile contamination generally.

This negative result is not a documentation defect; it is a research limitation and an important input to Track B.

## Novelty status

The broad hypothesis that adaptive RF fingerprinting/profile updating itself is novel was narrowed after prior-art review because adaptive/online RF fingerprinting and profile updating already exist.

The remaining candidate research hypothesis is narrower:

> Security-oriented separation of operational identity recognition from authorization to modify persistent RF identity/profile state, especially under target-like unknown contamination/poisoning while still permitting legitimate adaptation.

Current status: **implemented and tested research hypothesis; not formally proven novelty**.

The project must not claim generic adaptive RF updating, generic update gating, or reliable-sample admission as standalone novelty. Stronger novelty requires targeted systematic prior-art validation and stronger experimental evidence.

## Track-A ceiling

Track A was never intended to establish universal RF generalization. Its constraints create a deliberate ceiling. Track A should not be used to claim arbitrary cross-frequency generalization, arbitrary cross-dataset generalization, complete real-world RF validation, or universal Version-B superiority.

## Track-B direction

Track B should build on the Track-A Version-B baseline rather than restart the project. The research program should progressively add:

- broader qualified real RF datasets;
- cross-dataset validation;
- temporal/session/environmental variation;
- receiver/acquisition variation;
- potentially cross-frequency evaluation;
- broader device populations;
- more realistic adversarial and target-like contamination;
- stronger mechanisms specifically addressing the Track-A target-like unknown failure;
- systematic ablations and statistical analysis;
- stronger targeted novelty/prior-art validation.

Track B is future work until these studies are actually executed and evidenced.

## Demonstrator position

The final web demonstrator is a presentation/interaction layer over the current Track-A evidence. It may expose recognition, device profiles, open-set security, security/attack scenarios, audit trail and evaluation/research information. It must clearly label controlled/derived scenarios and must not invent measurements or hide limitations.

## Reference report companion

The editable DOCX and fixed-layout PDF were generated on 31 August 2026 as the full solo reference report. This Markdown copy is the repository-readable companion for continuity and future chats.

## Preservation

No historical evidence, experiment, dataset decision, prior-art record, PR or commit is superseded by this reference report unless explicitly stated. Historical documents remain part of the audit trail.
