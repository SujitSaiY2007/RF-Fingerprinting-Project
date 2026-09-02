# ManySig Inspection Record — 02 September 2026

## Purpose

Record the verified local inspection of the user-acquired WiSig ManySig archive before any full extraction or feature-engineering work. This document is an evidence/provenance record only; it does not claim D-stage completion.

## Acquisition state

The ManySig archive was acquired locally by the user and preserved outside the Git repository because the raw dataset is large and should not be committed to Git.

Known local copies reported during inspection:

- Primary working archive observed by Antigravity: `C:\Users\sujit\Downloads\ManySig.pkl.zip`
- Project-data backup: `C:\Users\sujit\OneDrive\Documents\RF-Fingerprinting-Project-Integration\RF-Fingerprinting-Data\ManySig.pkl.zip`
- A separate `C:\Users\sujit\Downloads\ManySig.pkl` directory was observed as empty and is treated as an extraction artifact, not as the canonical dataset.
- A multi-volume WiSig ManySig 7z archive was also observed under `C:\Users\sujit\OneDrive\Documents\RF-Datasets\WiSig\`.

The project must not delete or overwrite these copies merely because one is designated for working use. A checksum comparison should be performed before declaring the project-data copy and Downloads copy identical/canonical.

## Archive and pickle facts verified by non-destructive inspection

- ZIP entry: `ManySig.pkl`
- Compressed archive size: `1,454,577,503` bytes (~1.355 GB)
- Uncompressed `ManySig.pkl` size: `2,359,341,461` bytes (~2.197 GB)
- Internal archive timestamp: `2021-11-22 13:12:36`
- Serialization format: Python Pickle Protocol 3 (`\x80\x03`)
- Top-level object: Python `dict`
- Top-level keys: `tx_list`, `rx_list`, `capture_date_list`, `equalized_list`, `max_sig`, `data`

## Verified dataset schema

### Transmitters

Exactly 6 transmitter IDs:

`['14-10', '14-7', '20-15', '20-19', '6-15', '8-20']`

### Receivers

Exactly 12 USRP receiver IDs:

`['1-1', '1-19', '14-7', '18-2', '19-2', '2-1', '2-19', '20-1', '3-19', '7-14', '7-7', '8-8']`

### Capture dates

Exactly 4 weekly sessions:

`['2021_03_01', '2021_03_08', '2021_03_15', '2021_03_23']`

### Equalization

`equalized_list = [0, 1]`, interpreted in the inspected schema as raw/un-equalized and channel-equalized conditions respectively.

### Signal organization

The verified `data` hierarchy is:

`data[tx_index][rx_index][date_index][eq_index] -> numpy.ndarray`

There are:

`6 × 12 × 4 × 2 = 576` leaf arrays.

Every inspected leaf array was verified as:

- type: `numpy.ndarray`
- shape: `(1000, 256, 2)`
- dtype: `float64`

Thus the dataset contains:

`576 × 1000 = 576,000` signal bursts.

Each burst contains 256 I/Q sample pairs:

- `[:, 0]` = I samples
- `[:, 1]` = Q samples

The equivalent complex representation is `I + jQ` when required by downstream processing.

## Observation counts

- Per transmitter: 96,000 bursts
- Per receiver: 48,000 bursts
- Per capture date: 144,000 bursts
- Raw/un-equalized (`eq=0`): 288,000 bursts
- Channel-equalized (`eq=1`): 288,000 bursts
- Entire dataset: 576,000 bursts

These counts follow directly from the verified hierarchy and `max_sig=1000`.

## Important distinction: verified vs inferred

### Verified

The archive size, pickle protocol, dictionary keys, list lengths/values, hierarchy, leaf shape/dtype and resulting observation counts were established by non-destructive inspection.

### Not yet independently verified

The following should remain labelled as dataset-context inference until supported by direct source documentation or further inspection:

- that the 256 samples specifically correspond to an IEEE 802.11 preamble/packet burst;
- the exact sample rate and capture configuration;
- the precise implementation of the equalization procedure;
- the full scientific meaning of every metadata dimension beyond the observed labels.

## Streaming/chunked processing status

Antigravity reported that incremental processing appears feasible because the ZIP contains a nested pickle whose leaf arrays are only ~4.096 MB each. However, the claim that a custom streaming unpickling mechanism can traverse the complete pickle with <=25–30 MB peak RAM has **not yet been independently demonstrated**.

Standard Python pickle loading should not be assumed to be a row-wise or leaf-wise streaming database reader. Before final extractor implementation, a small controlled proof-of-concept must measure the actual memory behaviour and verify whether the compressed ZIP can be processed without full extraction/materialization.

## Current extraction boundary

No final feature extractor has been implemented from this inspection.

The eventual Track-B ManySig preparation should preserve the raw archive unchanged and extract only the information required by an explicitly defined experiment. Candidate metadata to retain includes:

- transmitter ID;
- receiver ID;
- capture date/session;
- equalization state;
- burst index;
- the 256 I/Q samples when raw signal access is required.

Feature selection must be tied to the frozen D2 contract and the explicitly opened Track-B experiment. It must not silently replace the Track-A SMoRFFI baseline or change frozen Track-A evidence.

## Scientific status

This inspection is **dataset understanding/provenance progress**, not D1/D7/D8/D9 scientific validation.

No ManySig experimental result, model accuracy, poisoning result, temporal-adaptation result or novelty result has been produced by this inspection.
