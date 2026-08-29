# D1 Implementation Status — 2026-08-29

## Current status
**D1 foundation implemented; D1 scientific/operational acceptance pending real local archives.**

## Implemented in this task branch
- Common normalized RF metadata record.
- Manifest-driven CSV ingestion.
- WiSig metadata loader.
- Oregon State WiFi RFFP metadata loader.
- Deterministic manifest checksum helper.
- Normalized JSONL writer.
- Duplicate/malformed-record validation.
- Unit tests for the above contract.
- D1 provenance and acceptance specification.

## Explicit limitation
The repository does not contain the large RF archives, and the current environment has not provided local copies of those archives. Therefore the loaders have not yet been exercised against real WiSig/Oregon State files in this task.

This is an implementation milestone, **not D1 completion**.

## Next D1 action
When the local data root is available:

1. inspect the actual WiSig compact/raw subset selected for the experiment;
2. inspect the Oregon State WiFi release structure and metadata files;
3. generate real manifests;
4. checksum manifests/source artifacts where feasible;
5. run the loaders against real files;
6. produce a dataset inspection report;
7. establish leakage-safe identifiers and partition metadata;
8. record any source-specific parsing failures instead of silently normalizing them away.
