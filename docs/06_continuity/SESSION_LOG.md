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
Use an accessible real-data substrate, beginning with WiSig ManySig already acquired by the user, to build the minimum defensible D1–D10 vertical implementation. Oregon State WiFi remains the first intended second implementation dataset but its download time must not block the vertical path.

### Track B — Research Validation / Strengthening
Add larger subsets, additional days/devices and qualified datasets only when a concrete experimental, metadata, access/licensing, integrity or reproducibility requirement justifies them. Use these data for stronger validation, ablations, statistical analysis and support/falsification of the research claim.

### Preservation
This decision changes execution order/dependency only. It does not remove the qualified dataset portfolio, prior-art findings, D1–D10 definitions, leakage controls, poisoning controls, novelty caveats, branch workflow, knowledge base or scientific completion standard.

### Dataset reuse
The project aims to acquire necessary development datasets once, preserve raw copies unchanged and reuse them through D1–D10. Further downloads require a documented need.

### Completion distinction
The project must distinguish implemented, tested, demonstrated on real data and scientifically validated. Track A accelerates the first three; Track B supplies additional evidence where scientific validation requires it.

Detailed policy:
`docs/08_execution/TWO_TRACK_EXECUTION_STRATEGY.md`
