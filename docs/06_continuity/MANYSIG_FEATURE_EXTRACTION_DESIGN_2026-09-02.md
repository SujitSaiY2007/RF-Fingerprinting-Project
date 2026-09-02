# ManySig Feature-Extraction Architecture & Runner Design

**Date:** 2026-09-02  
**Branch:** `task/manysig-feature-extraction-runner-2026-09-02`  
**Status:** **ENGINEERING DESIGN & SMALL VALIDATION IMPLEMENTED; Track-B Scientific Validation NOT Performed**

---

## 1. Executive Summary

This continuity document establishes the formal architecture and validated implementation design for the Track-B **ManySig Streaming Feature-Extraction Runner**. 

The runner connects the demonstrated memory-bounded ManySig streaming ingestion primitive ([`src/manysig_streamer.py`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/src/manysig_streamer.py)) to the frozen 16-feature physical RF evidence contract established in Track-A ([`src/smorffi_d3.py`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/src/smorffi_d3.py)).

A small validation slice was extracted from real Leaf 0 ($Tx=\text{"14-10"}, Rx=\text{"1-1"}, Date=\text{"2021\_03\_01"}, Eq=\text{raw}$), verifying that the vectorized batch extractor matches both the scalar Track-A reference formulas and the actual `src/smorffi_d3.py::extract_rf_features` function down to machine precision ($\max |\Delta| = 4.34 \times 10^{-17}$), with output written to a partitioned Apache Parquet structure accompanied by a streaming-calculated cryptographic manifest.

---

## 2. Pipeline Conceptual Architecture

```text
ManySig.pkl.zip (1.45 GB)
    │
    ▼
Streaming Unpickler (src.manysig_streamer)
    │ (Sequential stream, one (1000, 256, 2) leaf at a time)
    ▼
Vectorized 16-Feature Extractor (src.manysig_features)
    │ (SIMD complex FFT, phase steps, power, statistical moments across 1,000 bursts)
    ▼
Typed Arrow Table Builder (23 Columns: 7 Coordinate/Provenance + 16 Features)
    │ (Zero-copy memory encapsulation)
    ▼
Incremental Parquet Writer (src.manysig_feature_extractor)
    │ (Partitioned by rx_id=<rx>/is_equalized=<0|1>/data.parquet, Snappy-compressed)
    ▼
Streaming Cryptographic Manifest & Checksum Registry (manifest.json)
    │
    ▼
Track-B Research Substrate (Cross-Receiver, Time Drift, Equalization Holdouts)
```

---

## 3. Preservation of Track-A Feature Contract

Track-A defines 16 physical RF evidence features in [`src/smorffi_d3.py`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/src/smorffi_d3.py). The mathematical meaning, names, and formulas are preserved **identically** in [`src/manysig_features.py`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/src/manysig_features.py):

| # | Feature Name | Mathematical Definition | Physical Interpretation | Computable from ManySig? |
| :-: | :--- | :--- | :--- | :-: |
| 1 | `i_mean` | $\mathbb{E}[I]$ | In-phase DC offset / bias | **YES** |
| 2 | `i_std` | $\sigma(I)$ | In-phase energy spread | **YES** |
| 3 | `q_mean` | $\mathbb{E}[Q]$ | Quadrature DC offset / bias | **YES** |
| 4 | `q_std` | $\sigma(Q)$ | Quadrature energy spread | **YES** |
| 5 | `amplitude_mean` | $\mathbb{E}[\sqrt{I^2 + Q^2}]$ | Mean envelope magnitude | **YES** |
| 6 | `amplitude_std` | $\sigma(\sqrt{I^2 + Q^2})$ | Envelope variance | **YES** |
| 7 | `rms_amplitude` | $\sqrt{\mathbb{E}[I^2 + Q^2]}$ | Root-mean-square amplitude | **YES** |
| 8 | `crest_factor` | $\frac{\max(\sqrt{I^2 + Q^2})}{\text{RMS} + \epsilon}$ | Peak-to-average power ratio indicator | **YES** |
| 9 | `mean_power` | $\mathbb{E}[I^2 + Q^2]$ | Baseband instantaneous power | **YES** |
| 10 | `iq_variance_ratio_db` | $10 \log_{10} \frac{\text{Var}(I) + \epsilon}{\text{Var}(Q) + \epsilon}$ | I/Q gain imbalance | **YES** |
| 11 | `iq_correlation` | $\frac{\text{Cov}(I, Q)}{\sigma_I \sigma_Q}$ | I/Q quadrature phase skew | **YES** |
| 12 | `mean_phase_step_rad` | $\mathbb{E}[\angle(x[n] \cdot x^*[n-1])]$ | Mean sample-to-sample phase trajectory | **YES** |
| 13 | `std_phase_step_rad` | $\sigma(\angle(x[n] \cdot x^*[n-1]))$ | Phase step jitter / phase noise | **YES** |
| 14 | `spectral_centroid_hz` | $\sum f_k \cdot \text{PSD}_{\text{norm}}[k]$ | Center frequency of baseband energy | **YES** |
| 15 | `spectral_spread_hz` | $\sqrt{\sum (f_k - f_c)^2 \cdot \text{PSD}_{\text{norm}}[k]}$ | Spectral bandwidth / power dispersion | **YES** |
| 16 | `spectral_entropy_bits`| $-\sum \text{PSD}_{\text{norm}}[k] \log_2(\text{PSD}_{\text{norm}}[k] + \epsilon)$ | Spectral flatness / carrier disorder | **YES** |

### Direct Numerical Verification Against `src/smorffi_d3.py`

To establish direct numerical equivalence beyond feature names, a controlled test was executed on identical 288-sample complex input evaluated simultaneously across `src.smorffi_d3.extract_rf_features` and the ManySig implementations:

| Feature Name | Track-A `smorffi_d3` Value | ManySig Scalar Value | ManySig Batch Value | Max Absolute Difference |
| :--- | :---: | :---: | :---: | :---: |
| `amplitude_mean` | $+6.1590247862 \times 10^{-2}$ | $+6.1590247862 \times 10^{-2}$ | $+6.1590247862 \times 10^{-2}$ | $0.00 \times 10^0$ |
| `amplitude_std` | $+3.1394698317 \times 10^{-2}$ | $+3.1394698317 \times 10^{-2}$ | $+3.1394698317 \times 10^{-2}$ | $0.00 \times 10^0$ |
| `crest_factor` | $+2.7899744693 \times 10^{0}$ | $+2.7899744693 \times 10^{0}$ | $+2.7899744693 \times 10^{0}$ | $0.00 \times 10^0$ |
| `i_mean` | $-5.5476917971 \times 10^{-4}$ | $-5.5476917971 \times 10^{-4}$ | $-5.5476917971 \times 10^{-4}$ | $0.00 \times 10^0$ |
| `i_std` | $+4.9756837935 \times 10^{-2}$ | $+4.9756837935 \times 10^{-2}$ | $+4.9756837935 \times 10^{-2}$ | $0.00 \times 10^0$ |
| `iq_correlation` | $-6.3360084162 \times 10^{-2}$ | $-6.3360084162 \times 10^{-2}$ | $-6.3360084162 \times 10^{-2}$ | $\mathbf{4.16 \times 10^{-17}}$ |
| `iq_variance_ratio_db` | $+3.1712754464 \times 10^{-1}$ | $+3.1712754464 \times 10^{-1}$ | $+3.1712754464 \times 10^{-1}$ | $0.00 \times 10^0$ |
| `mean_phase_step_rad` | $-1.3771665767 \times 10^{-1}$ | $-1.3771665767 \times 10^{-1}$ | $-1.3771665767 \times 10^{-1}$ | $0.00 \times 10^0$ |
| `mean_power` | $+4.7789857141 \times 10^{-3}$ | $+4.7789857141 \times 10^{-3}$ | $+4.7789857141 \times 10^{-3}$ | $0.00 \times 10^0$ |
| `q_mean` | $-1.2374998673 \times 10^{-3}$ | $-1.2374998673 \times 10^{-3}$ | $-1.2374998673 \times 10^{-3}$ | $0.00 \times 10^0$ |
| `q_std` | $+4.7972946731 \times 10^{-2}$ | $+4.7972946731 \times 10^{-2}$ | $+4.7972946731 \times 10^{-2}$ | $0.00 \times 10^0$ |
| `rms_amplitude` | $+6.9130208405 \times 10^{-2}$ | $+6.9130208405 \times 10^{-2}$ | $+6.9130208405 \times 10^{-2}$ | $0.00 \times 10^0$ |
| `spectral_centroid_hz` | $-2.3492599895 \times 10^{5}$ | $-2.3492599895 \times 10^{5}$ | $-2.3492599895 \times 10^{5}$ | $0.00 \times 10^0$ |
| `spectral_entropy_bits` | $+7.5928516433 \times 10^{0}$ | $+7.5928516433 \times 10^{0}$ | $+7.5928516433 \times 10^{0}$ | $0.00 \times 10^0$ |
| `spectral_spread_hz` | $+5.7605956102 \times 10^{6}$ | $+5.7605956102 \times 10^{6}$ | $+5.7605956102 \times 10^{6}$ | $0.00 \times 10^0$ |
| `std_phase_step_rad` | $+1.8522981472 \times 10^{0}$ | $+1.8522981472 \times 10^{0}$ | $+1.8522981472 \times 10^{0}$ | $0.00 \times 10^0$ |

**Conclusion:** All 16 features match the authoritative Track-A implementation to within standard floating-point machine precision ($\le 4.16 \times 10^{-17}$).

---

## 4. Feature Extraction Unit: Per-Burst

- **Decision:** The feature extraction unit is the **individual signal burst** (`shape = (256, 2)`).
- **Scientific Rationale:**
  - In WiSig ManySig, each leaf array of shape `(1000, 256, 2)` represents 1,000 distinct packet transmissions under a single experimental condition $(Tx, Rx, Date, Equalization)$.
  - In physical device authentication, each received burst represents an independent verification event.
  - Aggregating 1,000 bursts into a single leaf mean would destroy $99.9\%$ of the dataset observations and prevent evaluating burst-to-burst repeatability, classifier confidence distributions, or open-set contamination.
- **Output Scale:** Each leaf produces $1,000$ feature records. Full ManySig extraction will produce exactly **$576,000\text{ feature records}$**.

---

## 5. Output Schema & Partitioning Strategy

### Apache Arrow Schema (23 Columns)

```text
Column Name              Arrow Type    Nullability   Description
---------------------------------------------------------------------------------------------
leaf_index               int16         NON-NULL      Flat leaf index (0..575)
burst_index              int16         NON-NULL      Burst index within leaf (0..999)
tx_id                    string        NON-NULL      Transmitter MAC/ID (e.g. "14-10")
rx_id                    string        NON-NULL      Receiver node ID (e.g. "1-1")
capture_date             string        NON-NULL      Capture date string ("2021_03_01")
is_equalized             bool          NON-NULL      False = raw (0), True = equalized (1)
sample_count             int16         NON-NULL      Fixed sample count per burst (256)
i_mean                   float64       NON-NULL      In-phase mean DC offset
i_std                    float64       NON-NULL      In-phase standard deviation
q_mean                   float64       NON-NULL      Quadrature mean DC offset
q_std                    float64       NON-NULL      Quadrature standard deviation
amplitude_mean           float64       NON-NULL      Envelope magnitude mean
amplitude_std            float64       NON-NULL      Envelope magnitude standard deviation
rms_amplitude            float64       NON-NULL      RMS amplitude
crest_factor             float64       NON-NULL      Peak-to-RMS crest factor
mean_power               float64       NON-NULL      Mean baseband signal power
iq_variance_ratio_db     float64       NON-NULL      I/Q variance imbalance (dB)
iq_correlation           float64       NON-NULL      I/Q cross-correlation
mean_phase_step_rad      float64       NON-NULL      Mean sample-to-sample phase step (rad)
std_phase_step_rad       float64       NON-NULL      Standard deviation of phase step (rad)
spectral_centroid_hz     float64       NON-NULL      PSD spectral centroid (Hz)
spectral_spread_hz       float64       NON-NULL      PSD spectral spread / bandwidth (Hz)
spectral_entropy_bits    float64       NON-NULL      PSD spectral entropy (bits)
```

### Partitioning & Storage Layout
- Format: **Apache Parquet (Snappy compressed)**.
- Partition Strategy: Implemented in [`src/manysig_feature_extractor.py`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/src/manysig_feature_extractor.py) using partitioned directory layout:
  `rx_id=<rx_id>/is_equalized=<0|1>/data.parquet`
- Memory Boundedness: Parquet writers stream per partition chunk so that neither raw I/Q bursts nor the full feature table are accumulated in Python RAM.
- Output Footprint:
  - 1,000 rows $\times 23$ columns: $\approx 158\text{ KB}$ per leaf.
  - Complete 576,000-row dataset: estimated $\approx \mathbf{18\text{--}24\text{ MB}}$ total on disk.

---

## 6. Manifest & Streaming Checksum Design

Every extraction run produces an immutable JSON manifest:
1. `source_archive`: Source archive filename (`ManySig.pkl.zip`).
2. `sample_rate_hz`: Scaling sample rate used ($20,000,000.0\text{ Hz}$).
3. `sample_rate_status`: Explicitly flagged as `"REQUIRES VALIDATION (Engineering default)"`.
4. `features`: Ordered list of 16 feature names.
5. `partitions`: Dictionary mapping partition keys to row counts, byte sizes, and **streaming 64 KB chunk-computed SHA-256 digests** (preventing memory exhaustion during checksumming).

---

## 7. Small Validation Slice Results (Leaf 0)

A controlled validation run was executed against real Leaf 0 using [`scripts/validate_manysig_features.py`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/scripts/validate_manysig_features.py):

- **Target Leaf:** Leaf 0 ($Tx=\text{"14-10"}, Rx=\text{"1-1"}, Date=\text{"2021\_03\_01"}, Eq=\text{raw}$)
- **Validated Bursts:** First 20 bursts compared between scalar reference and vectorized batch extractor.
- **Maximum Absolute Discrepancy:** **$4.34 \times 10^{-17}$** (within standard floating point machine epsilon).
- **Validation Parquet Written:** [`experiments/track_b/validation_leaf_0_features.parquet`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/experiments/track_b/validation_leaf_0_features.parquet) ($157,999\text{ bytes}$, 1,000 rows $\times$ 23 columns).
- **Parquet SHA-256 (Streaming Hash):** `97a3b1d258f09cd04d8f2ad1626516cedd7a4019d602a6f6faacbd7a1caefd92`
- **Manifest Written:** [`experiments/track_b/validation_leaf_0_features.manifest.json`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/experiments/track_b/validation_leaf_0_features.manifest.json)
- **Table Read-Back Check:** Successfully read back 1,000 rows $\times$ 23 columns with exact value preservation.

---

## 8. Evidentiary Categorization

### VERIFIED FACTS
1. All 16 Track-A RF evidence feature formulas match `src/smorffi_d3.py::extract_rf_features` to within $\le 4.16 \times 10^{-17}$.
2. Vectorized SIMD batch computation produces results identical to the scalar reference implementation to within $4.34 \times 10^{-17}$ on real Leaf 0 Wi-Fi bursts.
3. Leaf 0 features serialize to Parquet with a size of $157,999\text{ bytes}$ for 1,000 rows.
4. Arrow table read-back preserves all 23 columns and 1,000 rows losslessly.
5. Checksum hashing operates in streaming chunks without loading complete Parquet files into RAM.

### ENGINEERING DECISIONS
1. Set the fundamental observation unit to **1 burst** (yielding 1,000 rows per leaf and 576,000 rows total).
2. Store extracted features in columnar **Apache Parquet with Snappy compression**.
3. Implement partitioned layout (`rx_id=<rx>/is_equalized=<0|1>/data.parquet`) for sub-5ms slice loading during cross-receiver holdout experiments.
4. Require cryptographic SHA-256 manifest generation for every output partition.
5. Implement vectorized batch extraction ([`src/manysig_features.py`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/src/manysig_features.py)) to minimize processing latency.

### REQUIRES VALIDATION (Engineering Assumptions)
1. **Sample Rate Default ($20\text{ MHz}$):** `sample_rate_hz = 20_000_000.0` is an **engineering default** inherited from Track-A. It is **NOT** explicitly recorded in `ManySig.pkl` metadata (which stores only `tx_list`, `rx_list`, `capture_date_list`, `equalized_list`, `max_sig`, `data`). The code permits explicit injection of `sample_rate_hz` to support alternative capture rates (e.g. $25\text{ MS/s}$) once verified from external WiSig documentation.

### SCIENTIFIC QUESTIONS (For Later Track-B Experiments)
1. How do the 16 physical features shift when transmitter signals are observed across different receiver nodes (Rx 1..12)?
2. How does channel equalization (`equalized=1` vs `equalized=0`) alter carrier phase jitter and spectral centroid spread?
3. Can the 16 physical RF features support closed-set identification across the 6 transmitters when evaluated under cross-day holdouts?

### NOT YET DEMONSTRATED
- Full 576-leaf production extraction has **NOT** been performed.
- Machine learning models (Random Forest, CNNs, metric learners) have **NOT** been trained on ManySig features.
- Cross-receiver validation has **NOT** been evaluated.

> **Explicit Boundary:** ManySig feature extraction infrastructure is designed and validated on a small slice; Track-B scientific validation has not yet been performed.
