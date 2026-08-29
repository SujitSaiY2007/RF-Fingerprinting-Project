# SMoRFFI — D1 Ingestion Evidence

## Status
**D1 COMPLETE — source/schema qualification and ingestion foundation**

This status means the SMoRFFI source, published data structure, supported fields,
scientific scope, and deterministic ingestion/validation code have been recorded.
It does **not** mean that a local copy of the full Kaggle archive has been committed
or that every byte-level checksum has been independently reproduced in this
repository.

## Source evidence

The 2026 Computer Networks data article identifies two public SMoRFFI releases:

1. `RFFI-IQ_only-wifi-802.11g-2.4G-123-m5stack`
2. `RFFI-kf_feature-IQ-wifi-802.11g-2.4G-123-m5stack`

The article states that each release contains **123 CSV files**, one per device,
with **1,000 records per file**. The IQ-only release contains MAC address and raw
preamble samples. The feature release additionally contains RF-feature fields.

The published acquisition configuration is one USRP B210 receiver, 123 M5Stack
Core2 transmitters, IEEE 802.11g, 20 MHz bandwidth, 20 MS/s sampling, Channel 6,
and a fixed 25 cm transmitter/receiver separation in a controlled indoor setting.
All signals were collected within one day.

## D1 schema decision

The ingestion layer preserves only information explicitly exposed by the source:

- source file / row provenance
- device number / device identifier
- MAC address
- raw preamble when present
- all original CSV columns through `source_row`

Chronology, session identity, receiver variation, environment variation, distance
variation, and multi-day structure are **not inferred**. The published data article
explicitly describes a single controlled environment and one-day acquisition.

## Validation implemented

`src/smorffi_d1.py` provides:

- UTF-8-SIG CSV parsing
- deterministic row numbering
- device identifier normalization
- MAC address normalization
- raw preamble preservation
- recursive CSV discovery
- SHA-256 calculation for locally acquired artifacts
- metadata-only validation

`tests/test_smorffi_d1.py` covers IQ-style records, feature-style records, and
missing identity metadata.

## Integrity boundary

The repository intentionally keeps the large RF dataset outside Git. When the
public archive is locally acquired, `file_sha256()` is the canonical helper for
recording artifact checksums. A future package-acquisition record must include the
actual downloaded artifact path, byte size, SHA-256, acquisition date, and the
observed file count/row counts.

## Scientific boundary

SMoRFFI is qualified for Track-A same-model development. Its 123-device same-model
population is directly relevant to D3–D6 and D10. Its controlled single-day,
single-receiver design does **not** establish D7/D8 robustness. Those claims remain
out of scope until a suitable package-level source or complementary dataset is
verified.

## External source

Guo, Z. et al., *SMoRFFI: A large-scale same-model 2.4 GHz Wi-Fi dataset and
reproducible framework for RF fingerprinting*, Computer Networks 282 (2026),
112309, DOI: 10.1016/j.comnet.2026.112309.
