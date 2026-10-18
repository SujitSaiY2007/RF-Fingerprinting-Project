# F0 Handoff — Roadmap Created

**From:** F0 (planning)  
**To:** F1 (forensic evidence reconciliation)  
**Repository:** https://github.com/SujitSaiY2007/RF-Fingerprinting-Project  
**Required branch:** `main` only  
**Plan:** `docs/06_continuity/future_execution/README.md`

## What F0 accomplished

- Defined the future execution sequence F1–F9 with bounded scopes, entry conditions, exit criteria, and handoff requirements.
- Established `main` as the only development and reference branch for future work.
- Explicitly rejected new develop/task/research branches, merge-based integration workflows, destructive history changes, and unreviewed changes.
- Ordered evidence reconciliation before code repair or new experiments.
- Separated offline ManySig evidence, synthetic security simulations, unit/integration tests, performance benchmarks, and any future OTA/hardware validation.
- Preserved the existing repository's history and prior artifacts as the source context; this handoff does not assert that the scientific results have been independently validated.

## Starting point known to F0

The previously reported latest commit was `457cc635f9e75c1705492f1fe9f90d68f03ca4f7` (October 18, 2026). F1 must inspect the actual current HEAD and status rather than assuming this SHA is still current.

The current README and project state contain claims that conflict with the earlier audit narrative, including cross-receiver accuracy, fusion/open-set claims, Phase 5 validation, and what is complete versus future work. A prior report also described Phase 5 collation errors. Treat all conflicting metrics as unresolved until traced to actual result JSON, config, runner, and metric calculation.

## F1 entry point

1. Verify repository identity, current branch, HEAD, and `git status --short --branch`.
2. Read this handoff, the full future execution plan, `PROJECT_STATE.md`, README, all Track-B result JSONs, associated configs/runners/tests, and current research reports.
3. Build a claim-to-evidence ledger for B2-01 through B2-05, B3-01, B3-02, B4-01, and Phase 5.
4. Prioritize B2-02, B3-02, B3-01, B2-03, security metrics, and Phase 5 collation.
5. Do not modify experiment code, rerun experiments, or overwrite outputs in F1.

## F1 exit requirements

- Each important reported claim is marked `VERIFIED`, `PARTIALLY VERIFIED`, `UNVERIFIED`, or `CONTRADICTED`.
- Every verdict points to exact repository paths and JSON keys/functions/tests.
- Any unresolved discrepancy remains visible and is not replaced with a convenient number.
- Provide a precise specification for F2's Phase 5 collation repair, if supported by evidence.
- Create `F1_HANDOFF.md` for F2, update the plan's stage status, and commit only reviewed scoped documentation changes to `main` if safe.

## Prohibited assumptions

- Do not trust the README or master report over the underlying implementation automatically.
- Do not equate passing tests with correct scientific conclusions.
- Do not call synthetic security evaluation physical attack validation.
- Do not claim receiver invariance from matched-receiver accuracy.
- Do not create or switch branches.
- Do not start F2 implementation before F1 has established the evidence and precise defect.

**Next chat label: F1. Do not start at F0 or renumber the sequence.**
