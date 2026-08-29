# PROJECT STATE

**Last updated:** 2026-08-29

## Authoritative status
- Repository: `SujitSaiY2007/RF-Fingerprinting-Project`
- Stable branch: `main`
- Integration branch: `develop`
- Phase: **Phase 1 — Preparation / accelerated implementation**
- Current engineering gate: **D2 — Minimal deterministic synchronization / preprocessing**
- Current substage: **D2.1 — Sample representation — COMPLETE**
- D1: **COMPLETE at source/schema/ingestion-foundation level**
- D1–D10 scientific validation: **not yet complete**
- Researcher learning state: **Learning Phase — D2 learning gate OPEN**
- Current learning target: **Layers 1–2**, beginning with Complex Numbers → I/Q Representation. The researcher is completing this learning gate before substantive D2.2 work.
- Authoritative learning map: `docs/04_research/LEARNING_GATES.md` (7 explicitly defined learning layers).
- Current handoff: `docs/04_research/HANDOFF_NEXT_CHAT.md`
- Team size: 4
- All four members remain on the same overall workstream.

## Learning workflow — ACTIVE
Technical learning is a first-class, stage-gated project track. Each D-stage has two parallel dimensions: engineering completion and researcher learning completion.

A stage may be engineered while its learning gate is open, but the stage must not be represented as fully knowledge-complete until its required learning gate is passed.

Learning completion is based on understanding and application, not hours watched or course completion. The researcher must be able to explain the concept, interpret a small technical example, connect it to the project stage, and identify a major failure mode.

The authoritative 7-layer map and complete topic lists are maintained in `docs/04_research/LEARNING_GATES.md`.

### Stage-to-learning gate
- D1 → Layer 1 foundations + dataset/data provenance.
- D2 → Layers 1–2; complex numbers, I/Q, sampling, discrete signals, Fourier/FFT, statistics/normalization, leakage and deterministic preprocessing.
- D3 → Layers 1–3; add RF/wireless fundamentals, modulation, noise/SNR and RF impairments.
- D4 → Layers 1–4; add ML, neural networks, CNNs, embeddings and PyTorch.
- D5 → Layers 1–5; add evaluation, experimental design, baselines and reproducibility.
- D6 → Layers 1–6; add open-set recognition, rejection and unknown-device reasoning.
- D7 → Layers 1–6 with temporal/domain/receiver/environment shift understanding.
- D8 → Layers 1–7 with continual learning, profile evolution and update authorization.
- D9 → Layers 1–7 with threat models, poisoning and profile-corruption evaluation.
- D10 → All layers relevant to the implemented system with end-to-end technical/methodological understanding.

### Current researcher learning phase
The immediate D2 learning sprint is:
1. Complex numbers and complex arithmetic.
2. Magnitude, phase and conjugates.
3. I/Q representation and complex baseband.
4. Sampling and sampling rate.
5. Discrete signals.
6. Fourier/DFT/FFT concepts.
7. Basic statistics and normalization.
8. Data leakage and deterministic preprocessing.

The researcher intends to complete this gate before proceeding further into substantive D2.2 execution. Learning checks should be project-linked and should not be replaced by passive course completion.

## Dataset qualification milestone
The dataset-search/qualification gate is complete for development-substrate selection.

### KEEP — primary
- WiSig — scale, receiver variation, multi-day robustness.
- Oregon State WiFi RFFP — temporal/domain variation.
- Oregon State LoRa RFFP — same-model/environment/location/distance/receiver variation.
- SMoRFFI — large-scale same-model discrimination.

### SECONDARY
- ORACLE — controlled hardware/distance benchmark.
- Bluetooth smartphone RF database — optional cross-technology benchmark.

This does not constitute scientific validation of D1–D10.

## Accelerated execution decision
The project is fast-tracked toward a demonstrable D1–D10 software pipeline.

> **Build the smallest defensible end-to-end system first, then strengthen individual stages.**

### Two-track execution model — ACTIVE
**Track A — Fast Implementation / Demonstration**
- Build the minimum defensible D1–D10 vertical path quickly.
- Current Track A substrate: SMoRFFI.
- Keep Oregon State WiFi RFFP as a later intended second implementation dataset when acquisition is practical.
- Produce a real-data end-to-end demonstration before waiting for every large archive.

**Track B — Research Validation / Strengthening**
- Add larger subsets, additional days/devices and other qualified datasets only when required.
- Strengthen cross-condition/cross-dataset validation, ablations, statistical analysis and failure analysis.
- Use Track B to support or falsify research claims rather than manufacture positive evidence.

This changes execution priority/dependency structure; it does not lower scientific completion standards or delete prior decisions.

## Dataset acquisition policy
Acquire necessary development datasets once, preserve raw copies unchanged and reuse them. Additional acquisition is permitted only for a concrete experimental, metadata, access/licensing, integrity or reproducibility requirement. No open-ended dataset hunt. Large raw RF datasets remain outside Git.

## Completion-level discipline
Distinguish:
1. **Implemented** — code/artifact exists.
2. **Tested** — engineering tests or reproducible checks pass.
3. **Demonstrated** — integrated path operates on real data.
4. **Scientifically validated** — stage-specific acceptance evidence supports the claim.

Track A accelerates implementation/testing/demonstration. Track B supplies additional evidence where scientific validation requires it. D-stage completion still requires evidence and acceptance criteria.

## Novelty research status — 2026-08-29
A broad literature audit and targeted forensic audit were completed for RF/RFFI systems involving profile/model updating, sample admission, continual learning and RF security.

Weak standalone novelty claims rejected include RF fingerprinting, learned RF embeddings, physics-informed representation, open-set RF fingerprint recognition, prototype/embedding unknown-device decisions, continual RF learning, temporal/domain/test-time adaptation, adaptive profile updating, generic adversarial/backdoor robustness, historical profiling by itself, and reliability/sample selection in the broad sense.

Important prior-art findings include Nagravision WO2023046581A1 combining RF/IQ authentication, anomaly detection, persistent device models and updating; Liu et al. (2024) combining temporal adaptation, continual learning and selective admission of reliable new signals; other RF/PHY online adaptation work; and RF backdoor research establishing security sensitivity.

Canonical comparison: `docs/04_research/targeted_prior_art_matrix.md`.

## Revised primary novelty hypothesis
> **A security-oriented continual RF profile-evolution mechanism that treats device recognition and permission to modify persistent identity state as separate decisions, and evaluates that separation against controlled profile-poisoning while preserving legitimate adaptation.**

Core distinction:
`Identification correctness != authorization to update the persistent profile`

Novelty remains **PROVISIONAL — NOT FINALIZED**. The strongest remaining uncertainty is whether security-specific separation provides measurable value beyond a well-designed reliability/admission baseline.

## D1–D10 fast-track relationship
- D1: reproducible raw-data foundation — **COMPLETE for Track-A SMoRFFI source/schema/ingestion foundation**.
- D2: minimal deterministic synchronization/preprocessing.
  - **D2.1: sample representation — COMPLETE.**
  - D2.2: actual package/schema inspection and signal-field confirmation.
  - D2.3: deterministic preprocessing transformation definition.
  - D2.4: leakage-safe split strategy.
  - D2.5+: implementation, tests, evidence and acceptance.
- D3: interpretable RF evidence.
- D4: simple learned representation/embedding.
- D5: closed-set identity baseline.
- D6: explicit unseen-device/open-set baseline.
- D7: temporal/receiver/environment/domain-shift evidence.
- D8: chronological profile evolution and update-policy comparison.
- D9: controlled/synthetic poisoning and profile-corruption evaluation.
- D10: integrated end-to-end demonstration.

D8/D9 are primary experimental stages for proving/falsifying the candidate contribution, but require validated upstream artifacts.

## D1 completion milestone — 2026-08-29
SMoRFFI D1 is complete at the **source/schema/ingestion-foundation** level.

Artifacts:
- `src/smorffi_d1.py`
- `tests/test_smorffi_d1.py`
- `datasets/SMORFFI_D1_EVIDENCE.md`
- `datasets/dataset_registry.csv`

Published source evidence establishes 123 CSV files per release, 1,000 records per device, MAC/device identifiers, raw preamble data and RF-feature variants. Published acquisition: one USRP B210, 123 same-model M5Stack Core2 devices, 20 MS/s, IEEE 802.11g, Channel 6, 20 MHz bandwidth, fixed 25 cm separation, controlled indoor single-day collection.

The implementation does not infer chronology, session, receiver, environment or multi-day metadata that the source does not provide. Large RF archives remain outside Git.

**Integrity boundary:** a byte-level checksum of the full downloaded Kaggle archive has not been independently reproduced in this environment. Therefore D1 completion must not be represented as proof of local archive acquisition.

## D2.1 completion milestone — 2026-08-29
`docs/04_research/D2_1_SAMPLE_REPRESENTATION.md` defines the sample contract:
- one source CSV row is one atomic source observation / candidate sample;
- signal-derived information is the model-input boundary;
- device identity/source identifiers are labels/provenance, not predictive inputs;
- source file, row index, device ID/MAC and original source row are retained for provenance;
- unavailable metadata is not inferred;
- exact numeric signal shape, parser, scaling, windowing/padding and normalization are deferred to D2.2/D2.3 until actual package inspection;
- no device identity shortcut may enter the baseline model input;
- later transformations remain traceable to the source observation.

D2.1 does not claim optimal preprocessing, model performance or scientific validation.

## Current next action
1. **Researcher completes and passes the D2 Learning Gate (Layers 1–2).**
2. Use the next-chat handoff in `docs/04_research/HANDOFF_NEXT_CHAT.md` to resume from this exact state.
3. After the learning check, begin D2.2 by inspecting the actual SMoRFFI package/schema available for execution.
4. Confirm exact signal fields, parsing representation and numeric sample shape from observed data rather than assumptions.
5. Define deterministic preprocessing and leakage-safe splitting after schema confirmation.
6. Preserve raw/source rows and provenance; derived artifacts remain reproducible from D1 inputs.
7. Keep D7/D8 claims blocked until a dataset with required temporal/receiver/environment metadata is selected.
8. Maintain Track-A/Track-B separation and branch synchronization rules.

## Continuity rule
When a significant progress milestone is completed and agreed at the end of a chat, synchronize the canonical project state so `main` and `develop` contain the same agreed project state. Work-in-progress task branches/open PRs may remain ahead during implementation but must not silently alter `main`.

All prior dataset qualifications, novelty findings, D1–D10 definitions, leakage controls, poisoning controls, branch rules and scientific completion standards remain unchanged unless explicitly superseded by a recorded decision.
