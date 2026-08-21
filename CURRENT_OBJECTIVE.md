# CURRENT OBJECTIVE

## Current gate
**D1 — Raw RF Data / Ingestion**

The Dataset Search & Validation / Qualification workstream is complete as a development-substrate selection gate. It is not scientific validation.

## Immediate objective
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
- Material D1 decisions, limitations, protocol changes and acceptance evidence must be recorded in GitHub.
- `main` and `develop` are currently structurally aligned. Do not recreate independent histories; use the documented task/research branch → PR → develop → reviewed promotion → main workflow.

## Next concrete task
Before substantive ingestion coding, define the D1 ingestion specification and acceptance checklist, then verify the authoritative download/package structure and metadata for WiSig and Oregon State WiFi. After that, implement the minimal reproducible ingestion layer and its tests.
