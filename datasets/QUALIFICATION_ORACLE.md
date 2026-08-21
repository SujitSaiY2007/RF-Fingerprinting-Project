# ORACLE — Preliminary Qualification

## Identity

- Dataset: ORACLE RF Fingerprinting Dataset
- Source: GENESYS Lab / Northeastern University
- Intended D-stages: D2/D3/D5; secondary controlled benchmark
- Decision: **SECONDARY**

## Evidence

The official dataset page describes Dataset 1 as raw over-the-air IQ from 16 USRP X310 transmitter radios with the same USRP B210 as receiver. The radios transmit IEEE 802.11a frames at 2.45 GHz; receiver sampling is 5 MS/s. Recordings are organized by transmitter-receiver separation from 2 ft to 62 ft in 6-ft increments, and each radio has over 20 million samples. The recordings include SigMF-compatible metadata.

A second ORACLE dataset contains demodulated IQ symbols from 16 intentionally configured IQ-imbalance conditions, providing a controlled hardware-impairment study.

## Qualification

- D1: Strong.
- D2: Strong.
- D3: Excellent for controlled impairment studies.
- D4/D5: Useful but limited to 16 transmitters.
- D6: Weak as a primary open-set source.
- D7: Useful for distance variation, but not a receiver/domain-shift benchmark.
- D8: Weak; no strong evidence of multi-day sequential evolution in the retrieved documentation.
- D9: Suitable as legitimate base data, but not itself an attack dataset.
- D10: Useful controlled benchmark, not sufficient as the portfolio's sole end-to-end dataset.

## Decision rationale

SECONDARY because its controlled, bit-similar X310 setup is scientifically valuable for testing whether proposed RF-physics features remain device-informative under controlled distance and hardware-impairment conditions. Its small transmitter count and fixed receiver make it unsuitable as the main portfolio dataset.
