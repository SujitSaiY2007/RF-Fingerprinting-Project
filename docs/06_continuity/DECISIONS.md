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
