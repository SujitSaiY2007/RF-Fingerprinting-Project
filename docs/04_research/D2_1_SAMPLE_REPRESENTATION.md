# D2.1 — SMoRFFI Sample Representation Specification

## Status
**D2.1 COMPLETE — sample identity, model-input boundary, and provenance boundary defined**

## Objective
Define exactly what constitutes one experimental sample before implementing D2 preprocessing.

## 1. Unit of observation
For Track-A SMoRFFI, the atomic source observation is **one row of one published SMoRFFI CSV file**. The D1 ingestion layer assigns a deterministic `row_index` within the source file and retains the complete original row in `source_row`.

`one CSV row -> one source observation -> one candidate experimental sample`

A later D2 transformation may convert the signal field into a numeric tensor/window representation, but it must retain a traceable relationship to this source observation.

## 2. Model-input boundary
The baseline model input must contain **signal information only**, after deterministic transformations explicitly defined by D2.

The following are labels/provenance and must not be supplied as predictive input:
- device number / device identifier
- MAC address
- source filename
- source row index
- any identifier derived from the above

The model must learn transmitter identity from the signal representation rather than being given an identity shortcut.

## 3. Signal representation boundary
D1 establishes raw preamble samples in the IQ-only release and RF-feature fields in the feature release. D1 does **not** establish a single numeric tensor shape for the raw preamble field.

D2.1 therefore does not invent a tensor shape, sample length, parser, scaling rule, or windowing rule. Those are D2.2/D2.3 decisions and must be derived from the observed package schema.

D2 must explicitly record: source signal field(s), parsing representation, numeric shape, truncation/windowing/padding rule, normalization rule, and deterministic malformed-record handling.

## 4. Metadata/provenance boundary
Metadata remains attached to the sample for auditing and leakage-safe experimental control, but is not part of the baseline predictive feature vector.

Required provenance carried forward from D1:
- `source_file`
- `row_index`
- `device_id` when present
- `mac_address` when present
- complete `source_row`

Unavailable metadata remains unavailable. D2 must not infer session, chronology, receiver variation, environment variation, distance variation, or multi-day structure not explicitly exposed by the source.

## 5. Label definition
For closed-set device-identification experiments, the prediction target is the **device identity** represented by the source device identifier/MAC mapping established during ingestion.

The label is used only as the supervised target. It is not included in the model input.

Any transformation of identifiers into internal integer class indices must be deterministic and documented, and the mapping must be reproducible without becoming a model feature.

## 6. Leakage controls established by D2.1
D2 preprocessing must not:
- normalize using statistics computed from the full dataset before splitting;
- encode device identity into filenames, paths, array positions, or feature columns reaching the model;
- create synthetic session/receiver/environment metadata and treat it as experimental fact;
- allow the same source observation to appear in multiple evaluation partitions.

The exact train/validation/test grouping rule is a D2.4 decision.

## 7. Representation contract
The D2 pipeline must produce a conceptual record:

```text
Sample
├── model_input
│   └── deterministic numeric signal representation
├── label
│   └── device identity (training/evaluation target only)
└── provenance
    ├── source_file
    ├── row_index
    ├── device_id / MAC when available
    └── original source_row
```

Key invariants:

`model_input != device identity`

and

`model_input remains traceable to exactly one source observation unless a later, explicitly documented aggregation/windowing operation states otherwise.`

## 8. D2.1 acceptance criteria
- source observation unit is unambiguous;
- model inputs are separated from labels and provenance;
- no device identity shortcut is permitted in baseline input;
- exact numeric signal shape is explicitly deferred until actual schema inspection;
- provenance requirements are fixed;
- unavailable metadata is not inferred;
- downstream D2 stages have explicit responsibilities for signal parsing, preprocessing and splitting.

## Scientific boundary
This specification does not claim that a particular preprocessing method is optimal, nor does it establish model performance or scientific validity. It establishes the experimental contract that later D2 implementation must satisfy.

## Source basis
Grounded in the completed SMoRFFI D1 evidence record and ingestion implementation: `datasets/SMORFFI_D1_EVIDENCE.md` and `src/smorffi_d1.py`.
