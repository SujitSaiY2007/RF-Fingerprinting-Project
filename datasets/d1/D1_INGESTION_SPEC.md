# D1 — Raw RF Data / Ingestion Specification

**Status:** Implemented foundation; dataset-specific ingestion remains pending local-data validation.

## Scope

D1 establishes a reproducible metadata and provenance layer for the first development pair:

1. WiSig
2. Oregon State WiFi RFFP

Large raw RF archives are intentionally kept outside Git.

## Authoritative external sources

### WiSig
- Official dataset page: https://cores.ee.ucla.edu/downloads/datasets/wisig/
- Dataset paper: Hanna, Karunaratne & Cabric, IEEE Access 2022, DOI 10.1109/ACCESS.2022.3154790.
- The official page describes raw, processed and compact subsets and recommends compact subsets when they satisfy the experimental requirement.

### Oregon State WiFi RFFP
- Official release note: https://research.engr.oregonstate.edu/hamdaoui/sites/research.engr.oregonstate.edu.hamdaoui/files/release_note_datasets_wifi_oct2023_v2_0.pdf
- Associated paper: Elmaghbub, Hamdaoui & Wong, ADL-ID, arXiv:2301.12360.
- The release describes raw time-domain I/Q captures from 50 Pycom devices using an Ettus B210 at 2.412 GHz and 25 MS/s, with day/environment metadata.

## Local data-root contract

The implementation must never hard-code a machine-specific path. A local setup should expose one data root, for example:

```text
RF_DATA_ROOT=/path/to/local/rf-data
```

Expected local layout is intentionally not prescribed until the downloaded archives are inspected. The generated manifest records the exact local signal reference used by each experiment.

## Normalized metadata contract

Each manifest row should provide, where the source supports it:

- `signal_reference`
- `device_id`
- `session_id`
- `day`
- `date`
- `receiver`
- `environment`
- `location`
- `channel`
- `frequency_hz`
- `source_dataset`
- `raw_shape`
- `raw_dtype`
- `preprocessing_status`

Missing metadata is represented as missing, not inferred.

## Leakage-safe identifiers

The manifest must preserve identifiers needed to construct non-random partitions. At minimum, use device plus the strongest available recording/session/day identifier. Do not derive a session identifier merely from row order.

## Integrity

For every locally generated manifest:

- record manifest checksum;
- record source/version reference;
- record generation date;
- keep raw files unchanged;
- keep normalized metadata separate from raw data;
- validate duplicate signal references and malformed numeric fields.

## D1 acceptance evidence

D1 can be considered minimally accepted only after local archives are actually available and the team has produced:

- source/version provenance;
- real manifest(s);
- checksum record;
- successful loader run against the real archives;
- metadata inspection report;
- integrity/loadability test output;
- leakage-safe partition identifiers.

The current code establishes the reusable ingestion contract and tests, but **does not by itself prove full D1 acceptance**.
