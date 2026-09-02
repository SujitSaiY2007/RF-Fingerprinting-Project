# Project Decisions

## DEC-001 — Software-first development
Use existing/public datasets as the primary development and validation substrate. Hardware capture is a later transfer/validation stage.

## DEC-002 — Dataset portfolio
Do not require one dataset to satisfy every project stage. Each selected dataset must have a defined experimental responsibility.

## DEC-003 — Dataset qualification before implementation dependency
A dataset is not accepted merely because it is labelled as RF fingerprinting data. It must be assessed against requirement and quality criteria.

## DEC-004 — Independent evaluation
Where metadata permits, avoid random sample splits that allow samples from the same session/burst to appear in both training and test data. Prefer session/day/device/receiver holdouts appropriate to the claim.

## DEC-005 — Poisoning evaluation
Use legitimate real RF data plus controlled/synthetic poisoning for the update-security experiment, explicitly labelling the attack evaluation as controlled/synthetic.

## DEC-006 — GitHub as project source of truth
The repository stores project knowledge, decisions, implementation, experiments, results, provenance and continuity.

## DEC-007 — Four-member collaboration model
All four members currently work on the same overall workstream. No permanent technical ownership division exists.

## DEC-008 — Branch model
`main` is stable; `develop` is integration; task/research branches provide isolation. Branch structure is not technical ownership. Scientific validation is independent of merge status.

## DEC-009 — Dataset portfolio qualification gate
WiSig, Oregon State WiFi RFFP, Oregon State LoRa RFFP and SMoRFFI are KEEP primary datasets. ORACLE and the Bluetooth smartphone database are SECONDARY. This is a development-substrate decision, not D1–D10 validation.

## DEC-010 — No open-ended dataset hunt before D1
Further dataset search should be triggered only by a specific experimental, reproducibility, access/licensing or metadata gap.

## DEC-011 — Continual-learning caveat
No public dataset automatically proves D8. The project must construct a chronological update protocol with frozen evaluation, profile acceptance and rollback protection.

## DEC-012 — Repository reconciliation without history loss
The earlier `main`/`develop` divergence was a repository-history anomaly, not a scientific issue. The histories were reconciled using a merge commit with both pre-reconciliation branch tips as parents. Explicit archive branches were also created. No force-reset or history deletion was used.

## DEC-013 — Canonical branch alignment
After reconciliation, `main` and `develop` must remain structurally aligned at the same canonical state when no integration work is pending. Future work must use task/research branches and the documented PR workflow rather than creating independent branch histories.

## DEC-014 — D1 transition
After dataset qualification and repository reconciliation, the next project gate is D1 Raw RF Data / Ingestion, beginning with WiSig and Oregon State WiFi.

## DEC-015 — D1 ingestion boundary
D1 initially establishes reproducible provenance, manifests/checksums, raw-I/Q interpretation, metadata normalization, integrity/loadability tests and leakage-safe data foundations. It does not prematurely implement downstream ML, continual learning or poisoning defenses.

## DEC-016 — Literature audit invalidates weak standalone novelty claims
The 2026-08-25 Q2/Q4 literature audit established that physics-informed RF representation, open-set RF fingerprint recognition, incremental/continual RF fingerprint learning, physics-aware temporal adaptation, and generic adversarial robustness are already active research areas. These are therefore treated as enabling components/baselines rather than standalone project novelty.

The detailed evidence and representative sources are recorded in `docs/04_research/novelty_literature_gap_audit.md`.

## DEC-017 — Secure continual profile evolution is the primary novelty hypothesis
The project will investigate, but not yet claim as proven novelty, a security-aware continual RF device-profile evolution mechanism in which identity recognition is explicitly separated from authorization to modify the persistent device profile.

The core research distinction is:

`Identification correctness != authorization to update the persistent profile`

A newly observed sample may therefore be accepted for identity/authentication while being rejected for profile update when its physical, embedding-space, temporal, historical-profile or anomaly evidence is inconsistent.

## DEC-018 — Multi-evidence update authorization as a candidate mechanism
The candidate update gate may combine identity confidence, embedding consistency, RF-physical consistency, temporal consistency, historical-profile consistency and anomaly/deviation evidence. The scoring function and thresholds are not frozen and must be established through design, ablation and experiment rather than assumed.

## DEC-019 — D8/D9 research coupling
D8 Continual Learning / Profile Evolution and D9 Poisoning / Adversarial Protection should be experimentally connected through the secure profile-update pathway. D8 establishes chronological profile evolution; D9 evaluates whether anomalous or controlled/synthetic poisoned observations can corrupt that pathway and whether the candidate update gate prevents or limits corruption.

## DEC-020 — Novelty remains provisional until targeted audit
The secure profile-update pathway is currently a candidate research gap, not a finalized novelty claim. Before promotion to a formal contribution, the team must perform a targeted audit of RF/RFFI continual learning, profile-based RF authentication, poisoning/adversarial RF work and closely related continual-learning security literature, explicitly checking whether prior systems separate identity recognition from permission to modify a persistent device profile.

## DEC-021 — Targeted audit narrows the novelty claim
The 2026-08-29 targeted audit established two critical boundaries:

1. Nagravision WO2023046581A1 already combines RF/IQ authentication, anomaly detection, persistent device models and adaptive model updating.
2. Liu et al. (2024) already uses reliability-based admission of new signals before continual SEI database/model updating.

Therefore the project must not claim generic update gating, reliable-sample admission, or adaptive RF model updating as novelty.

The remaining candidate is narrower: **security-oriented separation of operational identity recognition from permission to modify persistent identity state, evaluated against controlled profile poisoning and legitimate adaptation.**

The canonical matrix is `docs/04_research/targeted_prior_art_matrix.md`.

## DEC-022 — Fast-track D1–D10 execution
The project will use an evidence-first vertical implementation strategy: build the smallest defensible version of D1–D10, test it, document it, then strengthen individual components. This accelerates demonstration without changing the scientific completion standard.

D8/D9 must compare:

A. naive update;
B. confidence-only update;
C. reliability/consistency admission;
D. security/update-safety authorization.

The decisive research comparison is C versus D.

## DEC-023 — Knowledge base and next-chat continuity
The project maintains a dedicated theory/practical knowledge base at `docs/07_knowledge_base/RF_FINGERPRINTING_KNOWLEDGE_BASE.md` and a detailed next-chat execution prompt at `docs/08_execution/NEXT_CHAT_FAST_TRACK_PROGRESS_PROMPT.md`. These are project-control artifacts, not evidence of D1–D10 completion.

## DEC-024 — End-of-chat canonical branch synchronization
When a substantial project change is completed and agreed upon by the end of a project chat, `develop` and `main` must be brought to **exactly the same canonical commit/state** before the chat is considered complete, unless an explicitly documented review/integration task is intentionally left pending.

New work during a chat may be isolated on a task/research branch or on `develop` through the normal PR workflow. Once the change is agreed as the accepted project state, it must be promoted so that:

`main == develop`

This rule is for repository consistency and does not mean that scientific claims or D-stage validation are complete merely because the branches are synchronized.

## DEC-025 — Two-track accelerated execution
Because large RF dataset acquisition can become a material time bottleneck, the project adopts a two-track execution model without lowering its scientific standards.

### Track A — Fast Implementation / Demonstration
Build the smallest defensible real-data D1–D10 vertical path as the immediate critical path. WiSig ManySig is the immediate accessible development substrate. Oregon State WiFi remains the first intended second implementation dataset when acquisition is practical, but its download time must not block the vertical implementation.

### Track B — Research Validation / Strengthening
In parallel or after Track A, add larger subsets, additional days/devices and qualified datasets only when a concrete experimental, metadata, access/licensing, integrity or reproducibility requirement justifies them. Use these data for stronger cross-condition/cross-dataset validation, ablations, statistical analysis and falsification/support of the research claim.

### Preservation rule
This decision changes **execution order and dependency structure only**. It does not replace or weaken the existing dataset qualification gate, primary/secondary dataset portfolio, D1–D10 definitions, leakage controls, poisoning controls, novelty caveats, branch workflow, knowledge base or scientific completion standard.

### Dataset reuse rule
The project aims to acquire necessary development datasets once, preserve raw copies unchanged and reuse them throughout D1–D10. Repeated downloads of the same dataset are not expected. Additional acquisition requires a documented need.

### Completion-level rule
Always distinguish:
1. implemented;
2. tested;
3. demonstrated on real data;
4. scientifically validated.

Track A accelerates the first three levels; Track B supplies additional evidence where level four requires it.

The strategy is documented in `docs/08_execution/TWO_TRACK_EXECUTION_STRATEGY.md`.

## DEC-026 — ManySig separated from the rapid internet-data implementation track
The user-provided WiSig ManySig archive is preserved as a **separate acquired dataset** and is not the default Track A working substrate. It will be retained for later controlled validation, reproduction and/or cross-checking.

Track A will instead prioritize **internet-accessible real RF/IQ datasets that the execution environment can fetch or inspect directly**, avoiding user-side large-file transfer wherever practical. Candidate datasets must still pass the existing qualification gate before being used for scientific claims.

This is an execution optimization only. It does not downgrade ManySig, change its qualified status, delete it from the project portfolio, or alter the D1–D10 scientific acceptance criteria.

## DEC-027 — ORACLE selected as the Track A working dataset
Following the explicit decision to separate ManySig from the rapid implementation path, **ORACLE is selected as the first Track A working dataset**, subject to final D1 accessibility, integrity, metadata/provenance and project-qualification checks before scientific claims are made from it.

The reason for selection is execution suitability: ORACLE provides real RF/IQ recordings, device identity labels, accompanying metadata and experimental variation that can support a compact D1–D10 demonstration without requiring the user to first transfer the large ManySig archive or wait for the slow Oregon State download.

This does **not** promote ORACLE into the primary qualified dataset portfolio, remove it from its existing secondary classification, or supersede WiSig/Oregon State as the project's broader validation datasets. It is a Track A execution decision only.

ManySig remains preserved separately for Track B validation/reproduction/cross-checking, and Oregon State acquisition remains independent of the Track A critical path.

## DEC-028 — SMoRFFI selected as the Track A working dataset; ORACLE retained separately
Following evaluation of the Track A objective against the practical access constraint, the project **supersedes DEC-027** and selects **SMoRFFI as the Track A working dataset**.

Rationale:
- SMoRFFI is explicitly a real RF fingerprinting dataset rather than a general RF/protocol-classification dataset.
- Its qualified record reports 123 same-model commercial IEEE 802.11g devices, raw I/Q data and RF features, making it directly relevant to device-level fingerprinting and the D3–D6/D10 objectives.
- It is a better fit for the rapid implementation objective than ORACLE's current official distribution, which requires a large archive download.
- SMoRFFI is already present in the project's **KEEP — primary same-model dataset** qualification portfolio; no new dataset-qualification milestone is created by this decision.

### Scope and scientific boundary
SMoRFFI becomes the **Track A implementation substrate**, subject to actual package accessibility, metadata inspection and D1 loadability/integrity checks before scientific claims are made from it.

The existing SMoRFFI qualification states that its strongest defined responsibility is **D3–D6 and D10**, while D7/D8 require package-level metadata verification. Therefore Track A must not assume that SMoRFFI alone can scientifically support every D7/D8 claim. If a concrete D7/D8 requirement is not covered, a qualified Track B dataset may be used for that stage without delaying the minimum vertical implementation.

### Preservation and non-regression
- **WiSig ManySig remains preserved separately as Track B** validation/reproduction/cross-checking data.
- **ORACLE remains qualified and secondary**, and may be used later as a controlled benchmark when justified; its prior Track A implementation work is not deleted.
- Oregon State WiFi/LoRa and the remaining qualified portfolio are unchanged.
- No prior dataset qualification, novelty finding, D1–D10 definition, leakage control, poisoning control, branch rule or scientific completion standard is removed or weakened.
- This decision changes the **Track A execution substrate only** and does not constitute D1–D10 scientific validation.

## DEC-029 — Track A access criterion
For the fast-track path, a dataset must satisfy both **scientific task fit** and **practical access suitability**. A scientifically strong dataset is not sufficient if its official acquisition method makes it a critical-path bottleneck under the project's time constraint. Conversely, download convenience alone is never sufficient for selection.

## DEC-030 — ManySig acquisition and non-destructive schema inspection
On 02 September 2026, the user acquired the WiSig ManySig archive locally and performed a non-destructive schema inspection using Antigravity IDE. This creates a new **Track-B data-preparation checkpoint**, not a replacement of the Track-A SMoRFFI baseline.

Verified inspection facts include:
- `ManySig.pkl.zip` compressed size `1,454,577,503` bytes (~1.355 GB);
- contained `ManySig.pkl` size `2,359,341,461` bytes (~2.197 GB);
- Python Pickle Protocol 3;
- top-level keys `tx_list`, `rx_list`, `capture_date_list`, `equalized_list`, `max_sig`, `data`;
- 6 transmitters, 12 receivers, 4 capture dates, 2 equalization states;
- `data[tx][rx][date][eq]` leaf arrays;
- 576 leaf arrays, each `(1000, 256, 2)` `float64`;
- 576,000 total signal bursts.

The raw ManySig archive remains outside Git and must not be committed. The project records its schema/provenance in `docs/06_continuity/MANYSIG_INSPECTION_2026-09-02.md`.

### Scientific and engineering boundary
The inspection does **not** establish D1/D7/D8/D9 completion, model results, temporal adaptation results, poisoning results or novelty. The reported possibility of <=25–30 MB peak-RAM incremental processing remains unproven until a controlled memory test demonstrates it.

Before implementing the final extractor, the next task is a small proof-of-concept that verifies whether the compressed pickle can be accessed incrementally, what mechanism is required, and what the actual peak memory usage is. Only after that should the minimum extraction schema and experiment-specific feature set be frozen.

### Security/provenance rule
GitHub Personal Access Token credentials used for repository access must never be stored in the repository, dataset folder, prompts, logs or project documentation. Local IDE credentials/settings are operational configuration, not project evidence.

## DEC-031 — Standard pickle loading is not a bounded-memory ManySig ingestion mechanism
A controlled synthetic Protocol-3 POC on 02 September 2026 used 24 NumPy leaves with the verified ManySig leaf shape `(1000, 256, 2)` and `float64` dtype. The measured peak RSS was approximately 184.88 MiB for plain `pickle.load()` and 189.19 MiB when the pickle was read from a compressed ZIP member before `pickle.load()`.

This establishes an engineering boundary for the proposed implementation: ordinary `pickle.load()` / normal `Unpickler` object reconstruction must not be treated as leaf-wise streaming access to the verified single top-level ManySig object.

This decision is based on a controlled synthetic analogue, not the real ManySig archive. It therefore does **not** establish the real archive's peak memory or prove that a custom parser can achieve <=25–30 MB.

Until a real-archive proof-of-concept demonstrates correctness and measured memory behaviour, the final ManySig extractor must not assume a bounded-memory streaming mechanism.
