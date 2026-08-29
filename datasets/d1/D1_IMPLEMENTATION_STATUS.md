# D1 Implementation Status — 2026-08-29

## Current status
**D1 foundation extended for ORACLE; real binary loadability remains pending execution against the actual archive.**

## Implemented
- Common normalized RF metadata record.
- Manifest-driven CSV ingestion.
- Existing WiSig metadata loader.
- Existing Oregon State WiFi RFFP metadata loader.
- ORACLE SigMF-compatible metadata discovery and normalization.
- ORACLE paired `.sigmf-meta` / `.sigmf-data` validation.
- ORACLE device/receiver/environment/distance provenance extraction.
- Explicit ORACLE `complex128` interpretation based on the publisher's dataset note.
- Deterministic manifest checksum helper.
- Normalized JSONL writer.
- Common and ORACLE-specific record validation.
- Unit tests covering ORACLE metadata normalization, discovery/validation and missing paired data rejection.

## Source verification completed
The official GENESYS ORACLE documentation confirms Dataset #1 is raw OTA IQ from 16 X310 transmitters, recorded with a fixed B210 receiver at 5 MS/s and 2.45 GHz, with distance variation from 2 ft to 62 ft. It documents paired SigMF-compatible metadata/data files and explicitly states that the released binary samples are stored as 64-bit floating point and should be parsed as `complex128`.

## Explicit limitation
The actual ORACLE binary archive has not yet been executed through the loader in this environment. Therefore this milestone is **not D1 completion** and does not claim real-archive loadability or scientific validation.

## Next D1 action
1. Make a small ORACLE raw recording plus its `.sigmf-meta` available to the execution environment, or otherwise obtain a directly readable archive subset.
2. Run the loader against the real files.
3. Verify byte size / complex128 interpretation and metadata-to-sample consistency.
4. Generate a real normalized manifest and provenance report.
5. Establish leakage-safe device/run/distance partition identifiers.
6. Freeze the D1 Track-A data contract.

After that, move immediately into D2 while retaining the D1 evidence artifact.

## SUPERSEDING TRACK-A UPDATE — 2026-08-29
DEC-028 supersedes the ORACLE Track A selection. **SMoRFFI is now the Track A working dataset.** The ORACLE-specific D1 implementation above is retained as reusable secondary work and is not deleted, but it is no longer the immediate Track A dependency.

The next D1 action is therefore to inspect the actual SMoRFFI package/access path, verify metadata and loadability/integrity, and establish the Track-A manifest/data contract from real files. Do not claim D1 completion until those checks are performed.

SMoRFFI's existing qualification defines D3–D6 and D10 as its strongest responsibilities and makes D7/D8 contingent on package-level metadata verification. Do not infer unsupported temporal/receiver/environment variation; use a qualified Track B dataset for a specific missing D7/D8 requirement if necessary.
