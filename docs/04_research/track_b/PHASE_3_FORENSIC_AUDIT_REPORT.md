# Phase 3 Forensic Audit Report
## Experiments EXP-B3-01 and EXP-B3-02

**Audit Date:** 2026-10-18  
**Repository Branch:** `main`  
**Current HEAD SHA:** `5f202f19fd226e69ae5e7ecbd79e29dfe86892f8`  
**Phase 3 Acceptance Gate Status:** **PASSED**  

---

## 1. Executive Verdict by Experiment

| Experiment | Title | Dataset / Scope | Verdict | Key Finding |
| :--- | :--- | :--- | :--- | :--- |
| **EXP-B3-01** | Multi-Receiver Observation Fusion | WiSig ManySig (12 Receivers, 576k bursts) | **PASS** | Distributed 5-RX Soft Voting achieves 100.00% accuracy on Day 4. Cross-receiver transfer voting on equalized bursts surges from 67.30% single-RX mean to 95.82% (+28.52 pp gain). |
| **EXP-B3-02** | Open-Set Transmitter Identification | WiSig ManySig (4 Known Tx, 2 Held-out Unknown) | **PASS** | Multi-receiver soft voting sharpens unknown rejection to 97.45%–100.00% under calibrated thresholds, with 100.00% accuracy on accepted known transmissions. |

---

## 2. Audit Verification Details

### 2.1 EXP-B3-01: Multi-Receiver Observation Fusion
- **Observation-Matching Contract:**
  - Evaluated on core cluster of 5 receivers: `['1-1', '1-19', '2-1', '2-19', '14-7']` and transferred across all 11 unseen receivers.
  - Rows correspond via `(tx_id, capture_date, burst_index)` tuples ($N=6,000$ test bursts per receiver on Day 4).
  - *Limitation Disclosed:* Absolute RF hardware packet simultaneity cannot be verified from ManySig serialized slices due to absence of microsecond timestamps.
- **Quantitative Results:**
  - **Raw Bursts ($is\_equalized=0$):**
    - Single-RX Local Baselines: 1-1 (99.93%), 1-19 (94.80%), 2-1 (97.62%), 2-19 (83.03%), 14-7 (83.53%). Mean single-RX = 91.78%.
    - Distributed Soft Voting: **100.00%** (Macro F1: 1.0000).
    - Hard Majority Voting: **100.00%** (Disagreement rate: 35.38%).
    - Centralized Feature Concatenation ($80$ features): **99.98%**.
    - Degradation Sweep: 1 RX (99.93%), 2 RX (100.00%), 3 RX (100.00%), 4 RX (100.00%).
    - Transfer Voting of RX 1-1 Model: Single unseen mean 25.73% $\rightarrow$ Ensemble 33.52% (+7.79 pp).
  - **Equalized Bursts ($is\_equalized=1$):**
    - Single-RX Local Baselines: 1-1 (99.32%), 1-19 (97.63%), 2-1 (98.52%), 2-19 (93.65%), 14-7 (98.87%). Mean single-RX = 97.59%.
    - Distributed Soft Voting: **100.00%** (Macro F1: 1.0000).
    - Hard Majority Voting: **100.00%** (Disagreement rate: 10.85%).
    - Centralized Feature Concatenation: **99.98%**.
    - Transfer Voting of RX 1-1 Model: Single unseen mean 67.30% $\rightarrow$ Ensemble **95.82%** (+28.52 pp gain, Macro F1 0.9576).

### 2.2 EXP-B3-02: Open-Set Transmitter Identification
- **Partition Integrity & Zero Leakage:**
  - Known Transmitters ($K=4$): `['14-10', '14-7', '20-15', '20-19']`.
  - Held-out Unknown Transmitters ($U=2$): `['6-15', '8-20']`.
  - Training: Days 1-2 Known Transmitters (8,000 bursts).
  - Calibration: Day 3 Known Transmitters ONLY (4,000 bursts). Zero unknown bursts and zero test labels used.
  - Evaluation: Day 4 Known Test (4,000 bursts) vs. Unknown Test (2,000 bursts). Total $N=6,000$ test bursts.
- **Quantitative Findings:**
  - Single-RX 1-1 Raw: $T_{95}=0.5700 \implies$ Known Acceptance 74.93% (K-FRR 25.07%), Known Acc 100.00%, Unknown Rejection 44.70%, Macro F1 0.6172.
  - Single-RX 1-1 Equalized: $T_{95}=0.6100 \implies$ Known Acceptance 96.62% (K-FRR 3.38%), Known Acc 99.61%, Unknown Rejection 46.85%, Macro F1 0.8320.
  - Multi-RX 5-Node Soft Voting (Equalized, $T_{99}=0.6820$): Known Acceptance 88.35% (K-FRR 11.65%), Known Acc **100.00%**, Unknown Rejection **97.45%**, Macro F1 **0.9114**!
  - Multi-RX 5-Node Soft Voting (Equalized, $T_{95}=0.7520$): Known Acceptance 79.12% (K-FRR 20.88%), Known Acc **100.00%**, Unknown Rejection **100.00%**, Macro F1 **0.8331**!

---

## 3. Acceptance Gate Checklist
1. [x] Observation-matching and split contracts documented and enforced.
2. [x] Immutable configs and machine-readable JSON results stored in `configs/` and `experiments/track_b/`.
3. [x] Unit tests validate counts, identity separation, date separation, and metric calculations (7 tests passing across `test_exp_b3_01.py` and `test_exp_b3_02.py`).
4. [x] Baselines and comparison populations clearly defined ($N=6,000$ Day 4 bursts).
5. [x] Zero feature leakage: input $X$ restricted strictly to 16 physical features; threshold calibration isolated to Day 3 known validation data.
6. [x] Ready to proceed to Phase 4 integration.
