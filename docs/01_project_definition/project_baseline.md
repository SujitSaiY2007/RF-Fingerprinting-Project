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
- Target local/edge operation.

## Important Scope Boundary

The project is being developed software-first using existing/public datasets wherever possible. Hardware capture is a later transfer/validation stage, not a prerequisite for every software experiment.

## Contribution Discipline

The project does not claim to invent RF fingerprinting. The proposed contribution is the integrated framework and its experimentally validated combination of physics-based features, representation learning, open-set recognition, controlled continuous profile evolution, and update protection.
