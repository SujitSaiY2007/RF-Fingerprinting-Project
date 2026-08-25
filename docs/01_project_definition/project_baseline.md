# Project Baseline

## Source Documents

This repository was initialized from three project documents:

1. Initial IDP — the original project concept.
2. Complete Project Architecture — the evolved system decomposition and validation methodology.
3. Dataset Requirement Matrix — the current dataset strategy and D1-D10 requirements.

The original documents should be preserved as historical source artifacts where practical. This Markdown repository is the operational/canonical working representation.

## Core Problem

Wireless identifiers can be spoofed or cloned. RF fingerprinting seeks to identify transmitters through hardware-related imperfections in their emitted RF signals.

## Project Direction

The proposed system combines conventional RF signal processing, measurable RF physics characteristics, learned device representations, open-set recognition, continuous profile updates, and security checks for profile updates.

## Intended Objectives

- Identify known transmitters.
- Detect previously unseen transmitters.
- Evaluate robustness under environmental/acquisition variation.
- Adapt device profiles over time without complete retraining.
- Protect continual profile evolution against erroneous or controlled/synthetic malicious updates.
- Target local/edge operation.

## Novelty Position — 2026-08-25

A broad literature audit established that physics-informed representation, learned RF embeddings, open-set RF fingerprint recognition, incremental/continual RF fingerprint learning, physics-aware temporal/test-time adaptation and generic adversarial robustness are not standalone novelty claims.

The current **provisional research contribution** is therefore centered on secure continual device-profile evolution:

> **Explicitly separate the decision to identify a device from the decision to authorize a new observation to modify that device's persistent RF profile.**

The candidate mechanism is a multi-evidence update authorization gate using, where experimentally justified, identity confidence, embedding consistency, RF-physical consistency, temporal consistency, historical-profile consistency and anomaly/deviation evidence.

This remains a hypothesis until the targeted literature audit and D8/D9 experiments establish a defensible differentiator.

Detailed evidence and the required forensic audit are recorded in `docs/04_research/novelty_literature_gap_audit.md`.

## Important Scope Boundary

The project is being developed software-first using existing/public datasets wherever possible. Hardware capture is a later transfer/validation stage, not a prerequisite for every software experiment.

## Contribution Discipline

The project does not claim to invent RF fingerprinting. The project must not claim novelty for individual established techniques. The contribution claim must be based on an explicitly differentiated system mechanism and experimental evidence. No claim of publication-worthiness or patentability is made without appropriate evidence.
