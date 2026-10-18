# Master Execution Plan: Phases 3, 4, and 5
## Community Aware Secure Continual RF Fingerprinting for IoT Device Authentication

**Branch:** `main` (Sole canonical working branch)  
**Initial HEAD SHA:** `5f202f19fd226e69ae5e7ecbd79e29dfe86892f8`  
**Execution Environment:** Python 3.12.4, scikit-learn 1.9.1, pyarrow 22.0.0, pandas 2.3.3, numpy 2.2.6, psutil 7.2.2  

---

## 1. Stage A: Repository & Experiment-Contract Audit

### 1.1 Repository State & Integrity Verification
- **Git Branch:** `main` (clean of tracked modifications, ahead of `origin/main` by 9 commits).
- **Working Tree:** Exactly 22 untracked Phase 2 files verified present and intact (5 configs, 5 results, 5 runners, 2 source modules, 5 unit tests).
- **Baseline Test Suite:** All 19 Phase 2 unit tests passing in 0.114s.
- **Dataset Verification:** `datasets/features/manysig/` contains all 12 receivers (`rx_id=1-1` through `rx_id=8-8`), each with `is_equalized=0` and `is_equalized=1` (576,000 total rows across 24 Parquet partitions).
- **Raw Data Safety:** `RF-Fingerprinting-Data/ManySig.pkl.zip` is preserved unextracted and unmodified.

### 1.2 Observation-Matching Contract for EXP-B3-01
- **Inspection Finding:** The ManySig Parquet partitions contain metadata fields: `['leaf_index', 'burst_index', 'tx_id', 'rx_id', 'capture_date', 'is_equalized', 'sample_count']` followed by 16 physical RF features.
- **Scientific Limitation Disclosed:** ManySig bursts lack microsecond RF hardware timestamps and 802.11 MAC sequence numbers. While rows across receivers share `(tx_id, capture_date, burst_index)` tuples (24,000 matching rows per receiver pair), absolute physical packet simultaneity cannot be independently verified from the serialized slices.
- **Defensible Multi-Receiver Protocol:**
  1. **Single-Receiver Baselines:** Individual performance of each receiver node ($N=12$).
  2. **Index-Paired Fusion (Upper Bound / Co-Session Proxy):** Concatenated feature-level fusion and soft-voting decision fusion across receiver sets observing index-matched bursts within the same capture session.
  3. **Decision-Level Multi-View Consensus (Robust Community Baseline):** Soft-voting (averaging predicted class probability distributions) and hard majority voting across participating receivers.
  4. **Degraded & Missing Observation Stress Tests:** Evaluation under missing receiver channels (1 to 5 failing receivers) and receiver disagreement conditions.
  5. **Equalization Comparison:** Evaluation under raw ($is\_equalized=0$) vs. equalized ($is\_equalized=1$) features.

### 1.3 Open-Set Partitioning Contract for EXP-B3-02
- **Transmitter Identities ($N=6$):** `['14-10', '14-7', '20-15', '20-19', '6-15', '8-20']`
- **Known Transmitters ($K=4$):** `['14-10', '14-7', '20-15', '20-19']` (lexicographically ordered known gallery).
- **Held-Out Unknown Transmitters ($U=2$):** `['6-15', '8-20']` (strictly excluded from all training, model fitting, and validation).
- **Threshold Calibration Protocol:**
  - Classifier trained on Days 1-3 of known transmitters.
  - Threshold $T$ calibrated **strictly on known validation partition** (e.g., 5th percentile of maximum predicted class probability $P_{max}$ on Day 3 known validation set, targeting ~95% known acceptance).
  - Test evaluation on unseen Day 4 (`2021_03_23`): evaluates known test samples against unknown test samples without test-label leakage.
  - Metrics reported: Known Identification Accuracy, Known False Rejection Rate (K-FRR), Unknown False Acceptance Rate (U-FAR), Open-Set Macro F1, and Decision Uncertainty.

---

## 2. Planned Implementation Architecture & File Inventory

### Phase 3 Deliverables
1. `configs/exp_b3_01_fusion.json` & `scripts/run_manysig_exp_b3_01_fusion.py`
   - Evaluates single-receiver vs. feature-level fusion vs. decision-level soft/hard voting across receivers.
   - Saves: `experiments/track_b/exp_b3_01_fusion_results.json`
2. `configs/exp_b3_02_open_set.json` & `scripts/run_manysig_exp_b3_02_open_set.py`
   - Evaluates closed-set vs. open-set rejection across known (4) and unknown (2) transmitters.
   - Saves: `experiments/track_b/exp_b3_02_open_set_results.json`
3. Unit test suites: `tests/test_exp_b3_01.py` and `tests/test_exp_b3_02.py`

### Phase 4 Deliverables
1. `src/integrated_auth_engine.py`
   - Decoupled 8-stage pipeline:
     1. Feature ingestion
     2. Identity prediction
     3. Open-set known/unknown gating
     4. Multi-receiver evidence fusion
     5. Community witness consensus
     6. Adaptation authorization
     7. Profile update / quarantine / rejection
     8. Cryptographic hash-chained event audit log
2. `configs/exp_b4_01_integrated_defense.json` & `scripts/run_exp_b4_01_integrated_defense.py`
   - Simulates 1,000 adaptation rounds across legitimate drift, stealthy poisoning, unknown spoofing, and replay attacks under matched denominators.
   - Saves: `experiments/track_b/exp_b4_01_integrated_defense_results.json`
3. Unit test suite: `tests/test_exp_b4_01.py`

### Phase 5 Deliverables
1. `scripts/run_phase5_comprehensive_evaluation.py`
   - Master reproduction runner executing full ablation matrix, runtime/memory benchmarking, and cross-phase metric collation.
   - Saves: `experiments/track_b/phase5_comprehensive_evaluation_results.json`
2. Unit test suite: `tests/test_phase5_evaluation.py`
3. Final consolidated evidence report and claim-to-evidence matrix.
