# D2.5 — Integrated D2 Acceptance

**Status:** ENGINEERING ACCEPTED / TRACK-A DEMONSTRATION PATH
**Date:** 2026-08-30

## Scope
D2.5 integrates the observed SMoRFFI schema, deterministic canonical representation, and leakage-aware engineering split on the 20-file local inspection subset.

## Acceptance checks

| Check | Result |
|---|---|
| CSV files inspected | 20 |
| Source rows inspected | 19,513 |
| Required columns present | PASS |
| `preamble` complex parsing | 19,513 / 19,513 PASS |
| Minimum stored length >= 288 | PASS |
| Canonical extraction produces 288 complex samples | PASS |
| I/Q conversion produces two real channels | PASS |
| No baseline normalization/clipping/resampling/filtering | PASS by contract |
| Split assignment deterministic | PASS |
| Device/MAC used only as label/provenance | PASS |
| Device-109 513-row anomaly preserved | PASS |

## D2 baseline contract

`serialized preamble -> complex samples -> first 288 source-defined canonical samples -> (I,Q) channels`

The original stored sequence length and discarded-tail count remain provenance fields. No claim is made that the trailing samples are meaningless.

## Limitations

- This acceptance is for the 20-file local Track-A inspection subset, not the complete 123-file release.
- The 70/15/15 hash split is an engineering split, not a temporal/session holdout.
- The published 20 MS/s sampling rate is source-reported; package-level metadata does not appear as a per-row field in the inspected CSVs.
- Scientific validity of downstream RF evidence and classifiers is not established by D2 acceptance.

## Next

Proceed immediately to D3 interpretable RF evidence, then D4 learned representation, D5 closed-set identity, and D6 unseen-device/open-set demonstration. Track-B validation remains separate.
