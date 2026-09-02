# ManySig Complete 576-Leaf Feature Extraction & Verification Report

**Date:** 2026-09-02  
**Branch:** `task/manysig-feature-extraction-runner-2026-09-02`  
**Status:** **FIRST COMPLETE MANYSIG EXTRACTION COMPLETED & INDEPENDENTLY VERIFIED; Track-B Scientific Validation NOT Performed**

---

## 1. Executive Summary

This continuity record documents the successful execution and rigorous post-extraction verification of the **first complete ManySig feature-extraction run** on the local 2.2 GB `ManySig.pkl.zip` archive.

Using the single-pass streaming extractor ([`src/manysig_streamer.py`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/src/manysig_streamer.py), [`src/manysig_features.py`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/src/manysig_features.py), [`src/manysig_feature_extractor.py`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/src/manysig_feature_extractor.py)), all **576 leaves** (comprising **576,000 bursts**) were transformed into structured 23-column feature records and written to a partitioned Apache Parquet dataset in **72.59 seconds** ($7,935.1\text{ bursts/s}$) with process working set peaking at **132.59 MiB** (Delta: **90.61 MiB**).

Independent post-extraction verification confirmed that all 576,000 expected burst records are present without omissions or duplicates, all 24 partition files reopen cleanly, all partition cryptographic digests match the root manifest, and the source archive was not modified.

---

## 2. Extraction Execution & Memory Metrics

- **Execution Command:** `python scripts/run_manysig_feature_extraction.py`
- **Source Archive:** `C:\Users\sujit\Downloads\ManySig.pkl.zip` ($1,454,577,503\text{ bytes}$)
- **Extraction Pass Time:** **$72.59\text{ seconds}$**
- **Throughput:** **$7,935.1\text{ bursts/second}$**
- **Baseline Working Set (RSS):** $41.98\text{ MiB}$
- **Peak Working Set (RSS):** **$132.59\text{ MiB}$**
- **Working Set Delta ($\Delta$RSS):** **$90.61\text{ MiB}$**
- **Total Parquet Dataset Size:** **$90,408,596\text{ bytes}$** ($86.22\text{ MiB}$)
- **Output Directory:** [`datasets/features/manysig/`](file:///c:/Users/sujit/OneDrive/Documents/RF-Fingerprinting-Project-Intergration/RF-Fingerprinting-Project/datasets/features/manysig)

---

## 3. Independent Post-Extraction Verification Results

| Verification Check | Target / Expected | Actual Measured | Status |
| :--- | :---: | :---: | :---: |
| **Raw Archive Integrity** | Unmodified ($1,454,577,503\text{ B}$) | Modification time & byte size identical | **PASS** |
| **Total Leaves Processed** | 576 leaves | 576 leaves | **PASS** |
| **Total Bursts / Rows Extracted**| 576,000 records | 576,000 records | **PASS** |
| **Records Per Leaf** | Exactly 1,000 records/leaf | 1,000 records/leaf across all 576 leaves | **PASS** |
| **Transmitter Cardinality** | 6 TXs (`14-10`, `14-7`, `20-15`, `20-19`, `6-15`, `8-20`) | All 6 TXs present | **PASS** |
| **Receiver Cardinality** | 12 RXs (`1-1`, `1-19`, `14-7`, `18-2`, `19-2`, `2-1`, `2-19`, `20-1`, `3-19`, `7-14`, `7-7`, `8-8`) | All 12 RXs present | **PASS** |
| **Capture Date Cardinality** | 4 Dates (`2021_03_01`, `2021_03_08`, `2021_03_15`, `2021_03_23`) | All 4 dates present | **PASS** |
| **Equalization Cardinality** | 2 States (`raw [0]`, `equalized [1]`) | Both states present | **PASS** |
| **Duplicate Check** | Zero duplicate `(leaf_index, burst_index)` | 576,000 unique coordinate keys | **PASS** |
| **Column Count & Types** | 23 columns (7 metadata + 16 features) | Exactly 23 typed columns in all partitions | **PASS** |
| **Partition Count** | 24 partitions (12 RX $\times$ 2 Equalizations) | 24 Parquet partition files | **PASS** |
| **Cryptographic Digest Match** | All partition SHA-256 match manifest | All 24 partition digests verified | **PASS** |

---

## 4. Partition Registry (24 Parquet Partitions)

All partitions are stored under `datasets/features/manysig/` with layout `rx_id=<rx>/is_equalized=<0|1>/data.parquet`:

| Partition Path | Rows | Size (Bytes) | Streaming SHA-256 Digest |
| :--- | :---: | :---: | :--- |
| `rx_id=1-1/is_equalized=0/data.parquet` | 24,000 | 3,749,825 | `847c4cbd628d2c80f0bdb2ad44e3937b3457b94121129964eec5f0bf2ff9b48a` |
| `rx_id=1-1/is_equalized=1/data.parquet` | 24,000 | 3,787,477 | `30a356abd68bd2e5ea69ff50c1bcc3ba8e0179f886f53b04ff23a0443da71b58` |
| `rx_id=1-19/is_equalized=0/data.parquet` | 24,000 | 3,750,633 | `b2e994a2e03c30b95b6e5d85de48a44905b80081f8620b812eba6f2b0f285d28` |
| `rx_id=1-19/is_equalized=1/data.parquet` | 24,000 | 3,787,626 | `5c545726896d3639d91d7087f175c5074a1b79601a0244d17a6d5f2404e43b8a` |
| `rx_id=14-7/is_equalized=0/data.parquet` | 24,000 | 3,754,962 | `a15bf597a844d4374a6d42daf0afd645011eb880eeb96afb03fefdf223d3dfce` |
| `rx_id=14-7/is_equalized=1/data.parquet` | 24,000 | 3,787,623 | `7487aedb64028d145704c15e40da236243b889d761282de3ede0b4fe96e3e894` |
| `rx_id=18-2/is_equalized=0/data.parquet` | 24,000 | 3,714,995 | `4d207042a8fdc1a557bb9df1a0073e9b9a3d7c25ceb039cdeb6233858e5627e3` |
| `rx_id=18-2/is_equalized=1/data.parquet` | 24,000 | 3,787,621 | `d8c04134202d7444ca34ec754a94c2c8b8c2cfeb18435f8827864b5b659a56ad` |
| `rx_id=19-2/is_equalized=0/data.parquet` | 24,000 | 3,754,336 | `bdc72231c6a62829c32eb74d08958187d7611713fcc67e7fcc95b9f4a2d026e7` |
| `rx_id=19-2/is_equalized=1/data.parquet` | 24,000 | 3,787,620 | `359d2af5bc9295f8c5618750d13c7cdf82ac181622d2806c5cc5adca7aaf0c1f` |
| `rx_id=2-1/is_equalized=0/data.parquet` | 24,000 | 3,749,860 | `66461caca502ff4ae7381e73b087a11d080d91eabc685ec7562a61796491ae2f` |
| `rx_id=2-1/is_equalized=1/data.parquet` | 24,000 | 3,787,478 | `6a6b7c8692664c3f4af91bad7a0284348027f0e4057c43539f3e024eb7262f03` |
| `rx_id=2-19/is_equalized=0/data.parquet` | 24,000 | 3,753,339 | `9aca8323031c6f1160325b1b9662689e9cd9b100534c0226a2d8bb36d7506bf3` |
| `rx_id=2-19/is_equalized=1/data.parquet` | 24,000 | 3,787,625 | `0f4ad795a763f10d630cbd111268f5c2bbb1b36c608aa413db77bb6917c1ece0` |
| `rx_id=20-1/is_equalized=0/data.parquet` | 24,000 | 3,751,301 | `58c34520892831277a8634e4e19e11b3001f8027fde8c8c8b0a436056fdcc2a0` |
| `rx_id=20-1/is_equalized=1/data.parquet` | 24,000 | 3,787,621 | `926bf4a2e410a08081fde624bf64f37f90faf3e26a38987791f284e60dd1708e` |
| `rx_id=3-19/is_equalized=0/data.parquet` | 24,000 | 3,723,245 | `e24f90f3b68c6925454ba8e6d922666753ab5be4bb92ad6b47af6b00311e95f9` |
| `rx_id=3-19/is_equalized=1/data.parquet` | 24,000 | 3,787,621 | `538103ab6c10f9a3f5e0d2a74761db38c1b37932f208ba741613650c434e45c8` |
| `rx_id=7-14/is_equalized=0/data.parquet` | 24,000 | 3,753,095 | `52a44e2f9aec1caea5a5ed82dec61aa2990e156767b63f4c5a82437b0ce58f36` |
| `rx_id=7-14/is_equalized=1/data.parquet` | 24,000 | 3,787,623 | `a14b4715b15b041b328e8909aeb46eae9c41983c8bdafc7de572c4eeda95b05b` |
| `rx_id=7-7/is_equalized=0/data.parquet` | 24,000 | 3,751,810 | `8df82ac8d484c1d92eeb60816401adbdd249074994598a04de00fe9672c73021` |
| `rx_id=7-7/is_equalized=1/data.parquet` | 24,000 | 3,787,479 | `87251f2a8e00d6a38ba355fe4984e40fa2aefe8073521e1adb506f53bf9d316d` |
| `rx_id=8-8/is_equalized=0/data.parquet` | 24,000 | 3,750,298 | `b6f43b9537bfe02b40231d75b93354d1403283040989f73309f72d1039c3e5a4` |
| `rx_id=8-8/is_equalized=1/data.parquet` | 24,000 | 3,787,483 | `192513e8f4f490ecdc9367ce8fd51ba9e253a87580d7c09efc86820ce8ac8dae` |

---

## 5. Evidentiary & Scope Boundaries

### VERIFIED FACTS
1. Exactly **576,000 feature records** were extracted across all **576 leaves** from `ManySig.pkl.zip`.
2. Process peak memory was bounded at **$132.59\text{ MiB}$** (working set delta: **$90.61\text{ MiB}$**), completely avoiding full-pickle RAM deserialization.
3. The dataset is structured into 24 Snappy-compressed Parquet files totaling **$86.22\text{ MiB}$**.
4. The raw source archive remained untouched and unmodified throughout the extraction.

### REQUIRES VALIDATION (Engineering Assumptions)
1. **Nominal Sample Rate ($F_s = 20.0\text{ MHz}$):** Inherited from Track-A as an engineering default. Recorded in manifest as `"REQUIRES VALIDATION (Engineering default)"`.

### NOT YET DEMONSTRATED
- **Zero machine learning models** have been trained on ManySig features.
- **Zero cross-receiver holdout evaluations** or classification accuracy claims have been made.
- **Track-B scientific validation has NOT been performed.**

> **Explicit Statement:** Complete ManySig feature extraction and data integrity verification are complete; Track-B scientific experimentation and evaluation remain future work.
