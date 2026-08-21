# WiSig — Dataset Qualification

## Decision
**KEEP — primary dataset**

## Responsibility
D4–D7, D5/D6 scalability, D10 supporting dataset; D1/D2 ingestion substrate.

## Evidence summary
Official UCLA/WiSig documentation reports 10 million packets, 174 WiFi transmitters, 41 USRP receivers and four captures spanning about one month, with raw and processed/compact subsets. The dataset provides substantial receiver/day variation and is therefore the primary scale and acquisition-robustness substrate.

## Strengths
- Genuine RF capture / raw-IQ availability.
- Large transmitter population.
- Multi-receiver and multi-day observations.
- Suitable for identity-level holdouts and session-aware evaluation.

## Limitations
- Not a purpose-built same-model benchmark.
- Large raw archive is operationally expensive.
- Open-set and continual-learning protocols must be constructed by the project.

## Scientific boundary
KEEP does not constitute validation of D1–D10.
