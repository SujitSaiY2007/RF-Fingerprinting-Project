# ManySig Real-Archive Streaming Ingestion POC — 2026-09-02

**Date:** 2026-09-02  
**Branch:** `task/manysig-real-streaming-poc-2026-09-02`  
**Status:** **ENGINEERING POC DEMONSTRATED; NOT Track-B Scientific Validation**

---

## 1. Executive Summary

This continuity record documents the empirical evaluation of the custom memory-bounded streaming unpickler against the actual 2.2 GB `ManySig.pkl` archive located at `C:\Users\sujit\Downloads\ManySig.pkl.zip` ($1,454,577,503\text{ bytes}$).

The proof-of-concept verified that:
1. Individual leaf arrays of shape `(1000, 256, 2)` can be extracted selectively from the serialized archive without loading the full 2.2 GB object into RAM.
2. The memory consumption is bounded: process working set remained between **30.42 MiB baseline and 45.24–49.82 MiB peak RSS** (Delta $\approx$ **14.82 MiB** for single leaf extraction, and **16.90 MiB** for full 576-leaf sequential streaming).
3. The historical informal target of $\le 25\text{--}30\text{ MB}$ total process RSS is clarified: the Python interpreter + Windows CRT baseline alone consumes $\approx 28\text{--}30\text{ MiB}$, while the unpickler's incremental memory delta is only **14.82 MiB**, yielding an effective process peak RSS of **$\approx 45\text{--}52\text{ MiB}$**.
4. The full stream throughput is **$27,497\text{ bursts/second}$**, processing all 576,000 observations across all 576 leaves in **20.95 seconds**.

---

## 2. Technical Mechanism

### Root Cause of Standard `pickle.load()` Memory Blowup
Standard `pickle.load()` deserialization fails to maintain bounded memory because:
- In Protocol 3, each array buffer ($4,096,000\text{ bytes}$) is preceded by `BINBYTES (0x42)` and followed by `BINPUT (0x71)`.
- The unpickler's internal `memo` dictionary stores a reference to every single `bytes` object pushed by `BINPUT`.
- Retaining all 576 byte buffers forces the process RSS to exceed $\mathbf{2.288\text{ GiB}}$.

### Custom Opcode Dispatch Solution
The module [`src/manysig_streamer.py`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/src/manysig_streamer.py) implements a specialized `pickle._Unpickler` subclass with custom opcode handlers:
- **`custom_load_reduce` (Opcode 0x52):** For non-target leaves, pushes a lightweight `_DummyArray` placeholder with `__slots__ = ()`, bypassing full NumPy ndarray object allocation.
- **`custom_load_binbytes` (Opcode 0x42):** For non-target leaves, reads the $4,096,000\text{ byte}$ buffer in 64 KB discarded chunks and pushes `b""` (0 bytes) to the stack/memo. For target leaves (or during callback streaming), the buffer is materialized as a NumPy `ndarray` view of shape `(1000, 256, 2)` and dtype `float64`.

---

## 3. Empirical Measurements

Measurements were recorded using Windows `GetProcessMemoryInfo` (working set size) on the actual ManySig zip archive without disk decompression.

### Single-Leaf Selective Recovery Tests

| Leaf Index | Coordinates $(Tx, Rx, Date, Eq)$ | Recovered Shape & Dtype | Array Size | SHA-256 Checksum | Baseline RSS | Peak RSS | Memory Delta | Elapsed Time |
| :--- | :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **Leaf 0 (Early)** | $Tx=\text{14-10}, Rx=\text{1-1}, Date=\text{2021\_03\_01}, Eq=\text{raw}$ | $(1000, 256, 2)$, `float64` | 4,096,000 B | `27798a5668c6b2b2...` | 30.42 MiB | **45.24 MiB** | **14.82 MiB** | 9.01 s |
| **Leaf 288 (Middle)** | $Tx=\text{20-19}, Rx=\text{1-1}, Date=\text{2021\_03\_01}, Eq=\text{raw}$ | $(1000, 256, 2)$, `float64` | 4,096,000 B | `b8c0bbaf1f056c90...` | 35.55 MiB | **49.82 MiB** | **14.27 MiB** | 8.96 s |
| **Leaf 575 (Final)** | $Tx=\text{8-20}, Rx=\text{8-8}, Date=\text{2021\_03\_23}, Eq=\text{equalized}$ | $(1000, 256, 2)$, `float64` | 4,096,000 B | `1e9ae4513278d9ca...` | 35.92 MiB | **49.82 MiB** | **13.90 MiB** | 9.35 s |

### Full Sequential Stream Test (All 576 Leaves / 576,000 Bursts)

- **Total Observations Processed:** 576,000 bursts
- **Baseline RSS:** 35.94 MiB
- **Peak RSS:** **52.84 MiB**
- **Memory Delta:** **16.90 MiB**
- **Elapsed Time:** **20.95 seconds**
- **Effective Scan Rate:** **$27,497.1\text{ bursts/second}$**
- **Recorded JSON Artifact:** [`experiments/track_b/poc_manysig_streaming_results.json`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/experiments/track_b/poc_manysig_streaming_results.json)

---

## 4. Evidentiary Categorization

* **VERIFIED FACT:**
  - `ManySig.pkl` contains 576 leaf arrays of shape `(1000, 256, 2)` and dtype `float64`, totaling 576,000 observations.
  - Standard `pickle.load()` on the archive consumes $\ge 2.288\text{ GiB}$ peak RSS.
  - The custom streaming unpickler recovers leaf 0 with exact SHA-256 `27798a5668c6b2b2946b9db556bfcb4eafacbbe60aacf11a98472c3ca3d94281` while limiting peak RSS to $45.24\text{ MiB}$ (delta: $14.82\text{ MiB}$).
  - All 576 leaves stream sequentially in $20.95\text{ s}$ with peak RSS of $52.84\text{ MiB}$.

* **ENGINEERING OBSERVATION:**
  - The old informal $\le 25\text{--}30\text{ MB}$ total process working set claim was overly optimistic for total Python process memory (which idles at $\approx 28\text{--}30\text{ MiB}$ on 64-bit Windows), but the **incremental memory overhead** of streaming ingestion is strictly bounded at $\approx 14\text{--}17\text{ MiB}$.
  - Scan time is consistent across the file stream ($\approx 8.9\text{--}9.3\text{ s}$ for random leaf access, and $\approx 20.9\text{ s}$ for full sequential extraction).

* **ENGINEERING DECISION:**
  - Adopt [`src/manysig_streamer.py`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/src/manysig_streamer.py) as the verified core ingestion engine for ManySig.
  - Implement the full Track-B feature extraction pipeline as a single-pass streaming consumer using this unpickler.

* **SCIENTIFIC STATUS:**
  - **Implemented and Tested Engineering POC.**
  - **NOT Track-B Scientific Validation.** Model training, feature extraction, cross-receiver holdouts, and scientific validation remain pending explicit user approval.
