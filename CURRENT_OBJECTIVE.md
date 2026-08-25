# CURRENT OBJECTIVE

## Current gate
**D1 — Raw RF Data / Ingestion**

The Dataset Search & Validation / Qualification workstream is complete as a development-substrate selection gate. It is not scientific validation.

## Parallel research-control objective
A broad Q2/Q4 literature audit has refined the project's novelty direction before downstream ML implementation.

The audit rejected several weak standalone novelty claims because they are already active research areas:
- physics-informed RF representation;
- learned RF embeddings;
- open-set RF fingerprint recognition;
- incremental/continual RF fingerprint learning;
- physics-aware temporal/test-time adaptation;
- generic adversarial robustness.

The current **provisional novelty hypothesis** is:

> **Secure continual RF device-profile evolution through explicit separation of identity recognition from authorization to modify the persistent device profile.**

The central research distinction is:

`Identification correctness != authorization to update the persistent profile`

A candidate multi-evidence update gate may use identity confidence, embedding consistency, RF-physical consistency, temporal consistency, historical-profile consistency and anomaly/deviation evidence before allowing a profile update.

This is a hypothesis, not a finalized novelty claim or frozen implementation.

## Required targeted Q4 audit
Before implementing the proposed novelty mechanism, perform a forensic literature audit of:
- continual/incremental RF fingerprint learning;
- profile-based RF authentication;
- RF adversarial/poisoning work;
- secure continual-learning mechanisms;
- any system that explicitly separates identity recognition from permission to modify a persistent device profile.

For every nearest prior system, record the representation, decision mechanism, profile/update mechanism, security model and exact difference from the project.

The detailed research record is:
`docs/04_research/novelty_literature_gap_audit.md`

## Immediate D1 objective
Establish a reproducible, provenance-aware, integrity-checked ingestion layer for the selected RF datasets, beginning with WiSig and Oregon State WiFi RFFP.

## D1 must establish
- Dataset/version identity and authoritative source provenance.
- Acquisition/download instructions without committing large raw RF archives to Git.
- File/package manifests and cryptographic checksums where feasible.
- Raw sample representation, file format, dtype, shape and channel interpretation.
- Metadata extraction into a common internal schema without destroying source-specific information.
- Device/session/day/receiver/environment/location identifiers needed for later leakage-safe experiments.
- Basic integrity, loadability and metadata-consistency tests.
- Explicit representation of missing, ambiguous or unverifiable metadata.
- Reproducible local data-root configuration so code does not depend on a contributor's machine-specific paths.
- Clear separation between raw/source data, normalized metadata, derived/intermediate data and experiment outputs.
- Initial dataset manifests that permit another team member to reproduce the ingestion setup.

## D1 implementation boundary
D1 is an ingestion/data-foundation stage. Do not prematurely build the ML classifier, embedding model, continual-learning mechanism or poisoning defense.

The first implementation pair is:
1. **WiSig** — primary scale/receiver/day substrate.
2. **Oregon State WiFi RFFP** — primary temporal/domain substrate.

Oregon State LoRa and SMoRFFI remain reserved for complementary downstream validation responsibilities unless D1 evidence exposes a specific need to ingest them earlier.

## D1 scientific acceptance principle
Successful file loading is not D1 scientific validation. D1 is complete only when its defined ingestion experiment, evidence, evaluation protocol and acceptance criteria are satisfied.

At minimum, D1 evidence must establish that:
- the intended source/version can be identified;
- the required data can be acquired or deterministically referenced;
- the package/file integrity can be checked;
- the raw signal representation is correctly interpreted;
- required metadata can be extracted or its absence explicitly recorded;
- the normalized representation is reproducible;
- later experiment partitioning can be performed without undocumented leakage assumptions.

## Research discipline
Do not infer metadata that the source does not provide. Preserve source-specific facts and uncertainty. Do not silently change the dataset qualification decision to accommodate an implementation convenience.

Do not claim D1–D10 completion from code existence. Each stage requires its own experiment, evidence and acceptance criteria.

## Repository discipline
- Large raw RF datasets remain outside Git.
- Git stores acquisition instructions, manifests, checksums, metadata schemas, scripts, tests, qualification records and appropriate derived results.
- Material D1 decisions, novelty decisions, limitations, protocol changes and acceptance evidence must be recorded in GitHub.
- `main` and `develop` are currently structurally aligned. Do not recreate independent histories; use the documented task/research branch → PR → develop → reviewed promotion → main workflow.

## Next concrete task
1. Complete the targeted Q4 novelty audit and record the nearest-prior comparison.
2. Do not implement the proposed novelty mechanism until the differentiator is supported by the audit and an experiment can be defined.
3. Continue D1 by defining the ingestion specification and acceptance checklist.
4. Verify the authoritative download/package structure and metadata for WiSig and Oregon State WiFi.
5. Implement the minimal reproducible ingestion layer and tests.
