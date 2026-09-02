# Session Log

## 2026-08-21 — Repository Initialization
The project repository was established as the persistent source of truth. Project-control files, Dataset Requirement Matrix, registry and qualification template were established.

## 2026-08-21 — Dataset Search & Qualification
Recovered the repository state, performed evidence-backed candidate research, qualified a complementary portfolio and recorded D1–D10 coverage/gaps. KEEP: WiSig, Oregon State WiFi RFFP, Oregon State LoRa RFFP, SMoRFFI. SECONDARY: ORACLE, Bluetooth smartphone RF database. No D1–D10 scientific validation was claimed.

## 2026-08-21 — Branch anomaly investigation and repair
### Finding
`main` and `develop` initially had independent/divergent histories. `main` was protected, so direct force movement was not used. PR #2 was merged into `develop`, integrating the dataset qualification work. A direct `develop` → `main` promotion exposed conflicts because of the independent histories.

### Lossless reconciliation
Before changing branch topology, explicit archive branches were created from the pre-reconciliation tips. A reconciliation merge commit preserved both histories. No history was deleted or force-reset.

## 2026-08-21 — D1 transition
Dataset qualification is complete as a development-substrate gate. The next engineering gate is D1 Raw RF Data / Ingestion, beginning with WiSig and Oregon State WiFi.

## 2026-08-25 — Q2/Q4 novelty literature audit
A broad literature audit rejected standalone novelty claims around physics-informed representation, embeddings, open-set recognition, continual learning, temporal/test-time adaptation and generic adversarial robustness.

The research direction was narrowed to secure continual RF profile evolution and the distinction:

`identity recognition != authorization to modify persistent profile`

The status remained provisional.

## 2026-08-29 — Targeted forensic prior-art audit
A narrower search was performed specifically for:
- RF authentication with online model/profile updating;
- continual RF/SEI learning;
- reliable/sample admission before updating;
- RF poisoning/backdoor security;
- online/adaptive physical-layer authentication;
- patents involving adaptive RF profiles.

### Critical findings
**Nagravision WO2023046581A1** already combines RF/IQ authentication, anomaly detection, persistent device models and adaptive model updating using new RF observations.

**Liu et al. (2024)** combines temporal/domain adaptation with continual SEI learning and selectively admits “reliable” new signals before database/model updating.

These findings invalidate broad claims such as:
- RF authentication + adaptive update;
- generic update gating;
- reliable-sample admission before continual learning.

The remaining candidate is narrower: security-oriented separation of operational identity recognition from permission to modify persistent identity state, evaluated against controlled profile poisoning and legitimate adaptation.

The proof matrix is recorded in:
`docs/04_research/targeted_prior_art_matrix.md`

### Experimental consequence
The decisive experiment must compare:

A. naive update;
B. confidence-only update;
C. reliability/consistency admission;
D. security/update-safety authorization.

The key comparison is C versus D.

## 2026-08-29 — Fast-track implementation strategy
The project is being accelerated toward a demonstrable D1–D10 software pipeline.

The strategy is:

`Build minimum -> test -> evidence -> strengthen`

The scientific completion standard is unchanged. A stage is not complete merely because code exists.

The first implementation pair remains WiSig + Oregon State WiFi RFFP.

A theory/practical knowledge base was added at:
`docs/07_knowledge_base/RF_FINGERPRINTING_KNOWLEDGE_BASE.md`

A detailed continuation prompt was added at:
`docs/08_execution/NEXT_CHAT_FAST_TRACK_PROGRESS_PROMPT.md`

The next session should inspect the repository, avoid restarting completed dataset qualification, begin D1 immediately and build the minimum vertical path through D10.

## 2026-08-29 — Repository cleanup and synchronization policy
The two superseded continuity/research documents were archived for traceability:
- `docs/05_archive/research/novelty_proof_matrix_2026-08-26.md`
- `docs/05_archive/continuity/CHATGPT_CONTINUATION_PROMPT.md`

Their active replacements remain:
- `docs/04_research/targeted_prior_art_matrix.md`
- `docs/08_execution/NEXT_CHAT_FAST_TRACK_PROGRESS_PROMPT.md`

A permanent repository rule was added: when a substantial project change is completed and agreed upon by the end of a project chat, `main` and `develop` must be synchronized to exactly the same canonical commit/state unless an explicitly documented review/integration task remains pending. Branch synchronization does not imply scientific validation or stage completion.

## 2026-08-29 — D1 ingestion foundation
A task branch `task/d1-ingestion-foundation-2026-08-29` was created from the canonical `main` state after confirming `main` and `develop` were identical.

Implemented:
- manifest-driven common RF metadata ingestion;
- WiSig metadata loader;
- Oregon State WiFi RFFP metadata loader;
- manifest checksum helper;
- normalized JSONL metadata output;
- deterministic validation tests;
- D1 provenance/acceptance specification.

### Boundary
The repository intentionally does not contain the large raw RF archives, and the current execution environment did not provide local copies. Therefore the real-archive loadability and metadata inspection tests remain pending. This milestone is **implementation foundation only**, not D1 completion.

The next action is to exercise the loaders against real local WiSig/Oregon State WiFi archives, generate real manifests and establish leakage-safe identifiers before accepting D1.

## 2026-08-29 — Two-track execution decision
Because large raw RF dataset acquisition became a practical time bottleneck, the project adopted a two-track execution model.

### Track A — Fast Implementation / Demonstration
Use an accessible real-data substrate to build the minimum defensible D1–D10 vertical implementation. The user's acquired WiSig ManySig copy is explicitly preserved separately; Track A prioritizes internet-accessible real RF/IQ datasets that the execution environment can fetch or inspect directly, avoiding user-side large-file transfer wherever practical.

### Track B — Research Validation / Strengthening
Retain ManySig for later controlled validation/reproduction/cross-checking, and add larger subsets, additional days/devices and other qualified datasets only when a concrete experimental, metadata, access/licensing, integrity or reproducibility requirement justifies them. Use these data for stronger validation, ablations, statistical analysis and support/falsification of the research claim.

### Preservation
This decision changes execution order/dependency only. It does not remove the qualified dataset portfolio, prior-art findings, D1–D10 definitions, leakage controls, poisoning controls, novelty caveats, branch workflow, knowledge base or scientific completion standard.

### Dataset access principle
Track A should minimize user-side downloads and uploads. Candidate internet datasets must still pass the existing qualification gate before being used for scientific claims. No open-ended dataset hunt is permitted.

### Completion distinction
The project must distinguish implemented, tested, demonstrated on real data and scientifically validated. Track A accelerates the first three; Track B supplies additional evidence where scientific validation requires it.

Detailed policy:
`docs/08_execution/TWO_TRACK_EXECUTION_STRATEGY.md`

## 2026-08-29 — ORACLE selected for Track A
The user explicitly approved **ORACLE as the first Track A working dataset** after evaluating the need for a directly accessible real RF/IQ substrate that does not require a large user-side download/upload.

ORACLE is used as the Track A implementation substrate subject to final D1 checks for accessibility, integrity, metadata/provenance and project qualification before scientific claims are made from it.

ManySig remains deliberately separate as a preserved Track B dataset. Oregon State WiFi remains independent of the Track A critical path. The existing qualified dataset portfolio and all prior scientific controls remain unchanged.

## 2026-08-29 — SMoRFFI selected for Track A; ORACLE selection superseded
After evaluating ORACLE's actual official distribution against the project's fast-track access objective, the user explicitly selected **SMoRFFI** as the new Track A working dataset.

The reason is not download convenience alone: SMoRFFI is already a qualified real RF fingerprinting dataset with 123 same-model commercial IEEE 802.11g devices, raw I/Q data and RF features, directly matching the core device-level fingerprinting objective. The official ORACLE distribution instead requires a large archive download, which conflicts with the time-constrained rapid-access requirement.

DEC-028 therefore supersedes DEC-027. **SMoRFFI is Track A; ORACLE remains qualified secondary; ManySig remains separate Track B.**

### Scientific boundary
SMoRFFI's existing qualification assigns its strongest defined responsibility to D3–D6 and D10 and leaves D7/D8 contingent on package-level metadata verification. The project will therefore inspect the actual SMoRFFI package before claiming D7/D8 coverage and will use a qualified Track B dataset for any specific D7/D8 requirement that SMoRFFI cannot defensibly support.

No prior dataset qualification, novelty finding, D1–D10 definition, leakage control, poisoning control, branch rule or scientific completion standard is removed or weakened. No raw dataset is added to Git.

## 2026-09-02 — ManySig acquired and inspected with Antigravity IDE
The user acquired the WiSig ManySig archive locally and began using Antigravity IDE as the local agent-assisted execution environment for dataset inspection and later extraction work.

The user also configured GitHub Personal Access Token access for repository operations. The token itself is a secret and is not stored in the repository or project documentation.

### Non-destructive ManySig inspection
Antigravity inspected the compressed archive and the initial pickle stream without modifying, renaming, moving or permanently extracting the raw dataset.

Verified structure:
- ZIP archive compressed size: `1,454,577,503` bytes (~1.355 GB);
- contained `ManySig.pkl` size: `2,359,341,461` bytes (~2.197 GB);
- Pickle Protocol 3;
- top-level keys: `tx_list`, `rx_list`, `capture_date_list`, `equalized_list`, `max_sig`, `data`;
- 6 transmitter IDs;
- 12 receiver IDs;
- 4 weekly March 2021 capture dates;
- 2 equalization states `[0, 1]`;
- `data[tx][rx][date][eq]` hierarchy;
- 576 leaf arrays;
- each leaf array `(1000, 256, 2)` with `float64` values;
- 576,000 total bursts.

The detailed inspection record is:
`docs/06_continuity/MANYSIG_INSPECTION_2026-09-02.md`

### Boundary and next action
This is **dataset preparation/understanding progress**, not D1/D7/D8/D9 scientific validation. The proposed low-memory streaming/chunked processing approach has not yet been independently demonstrated. The next engineering task is a small controlled proof-of-concept measuring the actual incremental access mechanism and peak memory before implementing the final extractor.

ManySig remains a Track-B dataset and does not replace the frozen Track-A SMoRFFI baseline.

## 2026-09-02 — Controlled ManySig-style streaming memory POC
A controlled synthetic Protocol-3 pickle POC was executed before final extractor implementation. It used 24 NumPy leaves with the inspected ManySig leaf shape `(1000, 256, 2)` and `float64` dtype, approximately 3.90625 MiB per leaf.

Observed peak process RSS:
- plain pickle + `pickle.load()`: ~184.88 MiB;
- ZIP member + `zipfile.ZipFile.open()` + `pickle.load()`: ~189.19 MiB.

The POC demonstrates an engineering limitation: standard `pickle.load()` materializes the single top-level object rather than exposing it as a leaf-wise streaming reader. Streaming the compressed ZIP member into `pickle.load()` does not remove that materialization behaviour.

This is controlled engineering evidence from a synthetic analogue, not a real-ManySig memory measurement. The prior <=25–30 MB claim remains unverified for the real archive.

The detailed POC record and reproduction script are:
- `docs/06_continuity/MANYSIG_STREAMING_POC_2026-09-02.md`
- `tools/manysig_streaming_poc.py`

### Next boundary
Antigravity must now test the actual ManySig stream with a narrowly scoped read-only proof-of-concept to determine whether a custom opcode-aware/incremental mechanism can recover selected leaves without materializing the complete top-level object. Actual peak RSS and recovery correctness must be measured before any final extractor is implemented.
