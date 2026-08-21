# CURRENT OBJECTIVE

## Objective

Perform Dataset Search & Qualification for the RF Fingerprinting project.

## Current team mode

All four team members are currently working on this same objective independently. There is **no fixed technical division of the project among the four members at this stage**. Independent work may overlap intentionally and should be consolidated through GitHub rather than treated as competing implementations.

## Required Output

Create a defensible dataset portfolio in which every selected dataset has an explicit experimental responsibility.

For every candidate dataset record:

- Dataset name and source
- Intended D-stage(s)
- Raw IQ availability
- Device/transmitter labels
- Number and type of physical transmitters
- Same-model availability
- Session/day structure
- Receiver information
- Distance/environment information
- Sampling rate and center frequency
- Waveform/protocol information
- Sequential/temporal structure
- Known/unknown-device suitability
- Documentation and provenance
- License and intended-use compatibility
- Reproducibility/accessibility
- Data integrity
- Missing information
- Validation experiments possible
- Qualification decision: KEEP / SECONDARY / REJECT
- Reason for decision

## GitHub integration

Individual members should preserve meaningful independent work in their own task/research branches where isolation is useful. Use Pull Requests to integrate contributions into `develop`; after review and appropriate validation, promote the integrated stable state to `main` through a Pull Request. The branch structure is about safe integration, **not about permanent division of technical ownership**.

When multiple members investigate the same dataset, keep the work attributable and mergeable. Consolidation should compare evidence and conclusions rather than silently overwriting one member's findings.

## Research Discipline

Do not modify project claims to fit available datasets. If a dataset cannot support a desired claim, record that limitation explicitly.

Do not download or commit large raw datasets into Git. Store metadata, manifests, qualification records, scripts, and reproducibility information instead.

## Completion Condition

This objective is complete only when the candidate dataset portfolio is sufficiently qualified to support the next implementation/validation step without relying on undocumented assumptions.
