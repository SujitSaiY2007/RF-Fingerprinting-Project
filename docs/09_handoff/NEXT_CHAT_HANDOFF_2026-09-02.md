# NEXT CHAT HANDOFF — 02 September 2026

## Purpose

This is the continuation point after the 02 September 2026 ManySig acquisition/inspection and Antigravity IDE setup work. The next chat must continue from the accepted repository state without restarting completed Track-A work or treating ManySig inspection as scientific validation.

## Current project position

The project remains one complete project executed through constrained tracks:

`Complete Project -> Track A under constraints -> Track-A Version-B final demonstrator baseline -> Track B broader validation -> desired end product`

Track A remains the frozen demonstrator baseline. Track B is the broader validation/strengthening direction.

## What happened in this chat

### 1. Antigravity IDE adopted as the local execution environment

The user is using **Antigravity IDE** (not a generic Antigravity service) to assist with local dataset inspection and later Python extraction/processing.

The repository is opened in Antigravity as the working project. The user configured GitHub access using a GitHub Personal Access Token for repository operations. **The token value must never be stored in GitHub, project files, prompts, logs or documentation.**

The preferred security posture is least-privilege, one-time approval for sensitive/expensive commands where practical. Repeated read-only inspection prompts may be approved when the exact command is understood, but unrestricted blanket execution permission should not be assumed.

### 2. ManySig was acquired locally

A large WiSig ManySig archive is now present locally. The raw dataset is kept outside the Git repository.

Observed copies/locations:

- `C:\Users\sujit\Downloads\ManySig.pkl.zip`
- `C:\Users\sujit\OneDrive\Documents\RF-Fingerprinting-Project-Integration\RF-Fingerprinting-Data\ManySig.pkl.zip`
- an empty `C:\Users\sujit\Downloads\ManySig.pkl` directory was observed as an extraction artifact;
- a multi-volume ManySig 7z archive also exists under `C:\Users\sujit\OneDrive\Documents\RF-Datasets\WiSig\`.

Do not delete or overwrite copies without an explicit preservation/checksum decision.

### 3. ManySig non-destructive inspection completed

The archive was inspected without full extraction or modification. The verified schema is recorded in:

`docs/06_continuity/MANYSIG_INSPECTION_2026-09-02.md`

Key verified facts:

- ZIP archive compressed size: `1,454,577,503` bytes (~1.355 GB)
- contained `ManySig.pkl`: `2,359,341,461` bytes (~2.197 GB)
- Pickle Protocol 3
- top-level dictionary keys: `tx_list`, `rx_list`, `capture_date_list`, `equalized_list`, `max_sig`, `data`
- 6 transmitters
- 12 USRP receivers
- 4 capture dates in March 2021
- 2 equalization states
- 576 leaf arrays
- each leaf array: `(1000, 256, 2)` `float64`
- total: 576,000 signal bursts
- each burst: 256 I/Q sample pairs

The report distinguishes verified facts from dataset-context inferences.

### 4. What has NOT yet happened

Do not claim that:

- the final ManySig extractor exists;
- the entire ManySig dataset has been processed;
- the proposed <=25–30 MB streaming-memory claim is proven;
- ManySig has produced model results;
- ManySig has validated D7/D8/D9;
- Track B has been scientifically validated;
- the novelty hypothesis has been proven.

The streaming/chunked ingestion mechanism still needs a small controlled proof-of-concept before final extractor implementation.

## Relationship to existing Track-A state

Do not replace the Track-A SMoRFFI baseline with ManySig merely because ManySig is now available.

Track A remains the accepted SMoRFFI-based demonstrator baseline and its frozen evidence remains unchanged. ManySig is now an acquired, inspected dataset that can support the next broader validation/reproduction/cross-condition work under Track B.

This is consistent with the existing two-track strategy and the prior decision that ManySig is preserved separately rather than silently becoming the Track-A baseline.

## Immediate next research/engineering boundary

The next ManySig task is:

1. verify the actual incremental access/memory behaviour;
2. define the exact experimental purpose for ManySig;
3. design the minimum extraction required for that experiment;
4. preserve raw data unchanged;
5. implement extraction only after the above are accepted;
6. keep extracted/derived data reproducible and provenance-linked.

Do not jump directly to full feature extraction without first resolving the streaming proof-of-concept and experimental split design.

## Deferred Antigravity prompt

When the user is ready to continue inside Antigravity, the following prompt should be used:

> Before implementing the ManySig feature extractor, verify the claimed streaming/chunked ingestion mechanism experimentally.
>
> Do not modify the original `ManySig.pkl.zip`. Do not create a full extracted copy of the dataset.
>
> Determine whether the proposed approach can actually access the 576 leaf NumPy arrays incrementally from the compressed pickle while keeping memory bounded.
>
> Perform a small controlled proof-of-concept using only a few leaf arrays and report:
>
> 1. The exact Python mechanism being used to access a leaf array.
> 2. Whether standard `pickle.load()` / `pickle.Unpickler` is being used, or whether a custom pickle-stream parser is required.
> 3. Peak RAM usage during the test.
> 4. Whether the complete 2.2 GB pickle is ever materialized in memory.
> 5. Whether the ZIP archive must first be fully extracted or can remain compressed.
> 6. Whether one `(1000, 256, 2)` leaf array can be processed and discarded before accessing the next leaf.
> 7. Whether the proposed approach is reliable enough to use for the complete 576,000-burst extraction.
>
> Do not implement the final extractor yet. Do not extract the complete dataset.
>
> Clearly distinguish experimentally verified results from assumptions.

## Recommended next-chat opening prompt for ChatGPT

Use this as the first message in the next ChatGPT project chat:

> Continue the RF Fingerprinting Project from the GitHub repository's canonical state as of 02 September 2026. Do not restart completed Track-A work or alter frozen evidence.
>
> First read and reconcile:
> 1. `PROJECT_STATE.md`
> 2. `CURRENT_OBJECTIVE.md`
> 3. `docs/09_handoff/NEXT_CHAT_HANDOFF_2026-09-02.md`
> 4. `docs/06_continuity/REFERENCE_REPORT_2026-08-31.md`
> 5. `docs/06_continuity/DECISIONS.md`
> 6. `docs/06_continuity/SESSION_LOG.md`
> 7. `docs/06_continuity/MANYSIG_INSPECTION_2026-09-02.md`
>
> The current immediate direction is Track-B ManySig preparation using Antigravity IDE. ManySig has been acquired and non-destructively inspected. Its verified structure is 6 TX × 12 RX × 4 dates × 2 equalization states, with 1,000 bursts per leaf and each burst shaped `(256, 2)` float64 I/Q. The raw archive must remain outside Git.
>
> Before implementing the final extractor, verify the proposed streaming/chunked ingestion mechanism with a small controlled memory test. Do not treat the previous Antigravity inspection claim of <=25–30 MB peak RAM as proven until experimentally demonstrated.
>
> Preserve the existing Track-A SMoRFFI baseline, all historical decisions, evidence and documents. Clearly separate verified facts, inferences, engineering decisions and scientific results. No deletion, force-push, destructive rewrite or silent change of frozen evidence.

## Continuity rules

- GitHub remains the project source of truth.
- Preserve historical documents and experiment artifacts.
- Do not store raw ManySig or GitHub PATs in the repository.
- Do not claim ManySig scientific results until experiments are actually run.
- Keep controlled/derived observations explicitly labelled.
- Use Implemented / Tested / Demonstrated / Scientifically Validated accurately.
- If evidence is insufficient, state: **Not demonstrated by the current evidence.**
- At a substantial accepted milestone, synchronize `main` and `develop` to the same canonical state without destructive history changes.
