# HANDOFF — NEXT CHAT

**Date:** 2026-08-29  
**Repository:** `SujitSaiY2007/RF-Fingerprinting-Project`  
**Current engineering state:** D2.1 complete; D2.2 next  
**Current researcher state:** Learning Phase — D2 Learning Gate OPEN

## 1. Authoritative project state

Read `PROJECT_STATE.md` first. It is the continuity source of truth.

The project is in **Phase 1 — Preparation / accelerated implementation**.

- D1 is complete at the SMoRFFI source/schema/ingestion-foundation level.
- D2.1 sample representation is complete.
- D2.2 has **not** been completed.
- The researcher is currently completing the prerequisite **D2 learning gate** before substantive D2.2 execution.
- The authoritative learning map is `docs/04_research/LEARNING_GATES.md`.
- The learning map contains **7 explicitly defined layers**, with the complete topic list for every layer.

## 2. Current learning gate

The immediate requirement is **Layers 1–2**.

The researcher is starting with:
1. Complex numbers and complex arithmetic.
2. Magnitude, phase and conjugates.
3. I/Q representation and complex baseband.
4. Sampling and sampling rate.
5. Discrete signals.
6. Fourier/DFT/FFT concepts.
7. Basic statistics and normalization.
8. Data leakage and deterministic preprocessing.

Do not treat video/course completion as proof of learning. Use short concept checks and project-linked exercises. A learning gate is passed only when the researcher can explain concepts, interpret a small technical example, connect them to the project, and identify major failure modes.

## 3. D2.1 decision already made

Read `docs/04_research/D2_1_SAMPLE_REPRESENTATION.md`.

The current contract is:
- one source CSV row = one atomic source observation / candidate sample;
- signal-derived information is the model-input boundary;
- device identity/MAC is the label, not a predictive feature;
- source file, row index and device identity remain provenance/label information;
- unavailable metadata is never invented;
- exact numerical signal shape, parser, scaling, windowing/padding and normalization are deliberately deferred until actual package inspection.

## 4. D2.2 required work after learning gate

Do **not** assume the SMoRFFI signal schema from the paper or from generic RF knowledge.

D2.2 must inspect the actual package/schema available for execution and establish, from observed data:
- exact signal field(s);
- encoding/parsing representation;
- data types;
- sample dimensions/shape;
- missing/invalid value behaviour;
- relationship between row, device identity and signal;
- any source metadata actually present;
- provenance needed for later reproducibility.

Only after this inspection should D2.3 define deterministic preprocessing.

## 5. Scientific guardrails

- Never feed device identity or an identity-derived filename/row shortcut into the baseline model input.
- Never invent session/day/receiver/environment metadata.
- Never normalize using statistics computed from the full dataset before partitioning.
- Preserve raw/source observations and provenance.
- Keep Track A (SMoRFFI) separate from Track B (ManySig/WiSig-related validation work).
- Do not claim D7/D8 temporal/receiver/environment evidence from SMoRFFI alone; its published acquisition is controlled and single-day/single-receiver.
- Distinguish implemented, tested, demonstrated and scientifically validated.
- Novelty remains provisional; do not present the revised profile-update authorization hypothesis as proven novelty.

## 6. Repository workflow

The project uses:

`task branch → PR → develop → agreed milestone → main`

When a significant milestone is completed and agreed at the end of a chat, synchronize `main` and `develop` to the same agreed project state. Do not silently modify the canonical branches from work-in-progress.

## 7. What the next chat should do

First acknowledge and verify:
- current project state;
- current learning state;
- that D2.1 is complete;
- that the researcher is in the D2 Layers 1–2 learning phase;
- that D2.2 is blocked pending the learning check if the researcher has not yet passed it.

Then continue the learning process. Do not restart D1 or D2.1.

When the researcher says the learning gate is complete, administer a concise D2 knowledge check before proceeding to actual D2.2 inspection.

After the gate is passed, inspect the actual SMoRFFI package/schema and continue D2.2 from evidence, not assumption.

## 8. Suggested opening prompt for the next chat

Use the following prompt exactly or with minor personal wording changes:

> Continue the RF Fingerprinting Project from the canonical GitHub state. First read `PROJECT_STATE.md`, `docs/04_research/LEARNING_GATES.md`, `docs/04_research/D2_1_SAMPLE_REPRESENTATION.md`, and this handoff file. The project is at **D2.1 COMPLETE → D2.2 NEXT**. I am currently in the **D2 Learning Phase**, and I am completing the **Layers 1–2 learning gate** before proceeding with substantive D2.2 work. Do not redo D1 or D2.1, do not assume the SMoRFFI signal schema, and do not advance D2.2 until you have checked whether I have passed the D2 learning gate. Continue teaching/testing me through the required concepts, starting from **Complex Numbers → I/Q Representation**, and connect every concept to the RF fingerprinting project. Once I pass the gate, proceed to D2.2 by inspecting the actual SMoRFFI package/schema and establishing the exact observed signal representation before defining preprocessing.
