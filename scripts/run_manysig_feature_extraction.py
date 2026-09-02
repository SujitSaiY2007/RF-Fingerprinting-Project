"""Production runner for complete ManySig streaming feature extraction.

This script executes the memory-bounded streaming extraction across all 576 leaves
(576,000 bursts) of ManySig.pkl.zip, writes partitioned Parquet tables, generates
cryptographic manifests, and performs complete post-extraction verification.
"""

from __future__ import annotations

import argparse
import ctypes
from ctypes import wintypes
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.manysig_feature_extractor import (
    ExtractorConfig,
    ManySigFeatureExtractor,
    compute_file_sha256,
)
from src.manysig_features import FEATURE_NAMES
from src.manysig_streamer import (
    BURSTS_PER_LEAF,
    NUM_DATES,
    NUM_EQUALIZATIONS,
    NUM_RECEIVERS,
    NUM_TRANSMITTERS,
    TOTAL_LEAVES,
)


class PROCESS_MEMORY_COUNTERS_EX(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("PageFaultCount", wintypes.DWORD),
        ("PeakWorkingSetSize", ctypes.c_size_t),
        ("WorkingSetSize", ctypes.c_size_t),
        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
        ("PagefileUsage", ctypes.c_size_t),
        ("PeakPagefileUsage", ctypes.c_size_t),
        ("PrivateUsage", ctypes.c_size_t),
    ]


psapi = ctypes.WinDLL("psapi")
kernel32 = ctypes.WinDLL("kernel32")
GetProcessMemoryInfo = psapi.GetProcessMemoryInfo
GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESS_MEMORY_COUNTERS_EX), wintypes.DWORD]
GetProcessMemoryInfo.restype = wintypes.BOOL
GetCurrentProcess = kernel32.GetCurrentProcess
GetCurrentProcess.restype = wintypes.HANDLE


def get_process_memory() -> dict[str, float]:
    """Return process RSS and peak RSS in MiB."""
    pmc = PROCESS_MEMORY_COUNTERS_EX()
    pmc.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS_EX)
    GetProcessMemoryInfo(GetCurrentProcess(), ctypes.byref(pmc), pmc.cb)
    return {
        "rss_mib": float(pmc.WorkingSetSize) / (1024.0 * 1024.0),
        "peak_rss_mib": float(pmc.PeakWorkingSetSize) / (1024.0 * 1024.0),
        "private_mib": float(pmc.PrivateUsage) / (1024.0 * 1024.0),
    }


def run_full_extraction(
    archive_path: Path,
    output_dir: Path,
    sample_rate_hz: float = 20_000_000.0,
) -> dict:
    if not archive_path.exists():
        raise FileNotFoundError(f"ManySig archive not found: {archive_path}")

    # Pre-flight archive snapshot
    pre_stat = archive_path.stat()
    pre_mtime = pre_stat.st_mtime
    pre_size = pre_stat.st_size
    print(f"Starting complete ManySig feature extraction:")
    print(f"  Source Archive:    {archive_path}")
    print(f"  Archive Size:      {pre_size:,} bytes ({pre_size / (1024**3):.2f} GiB)")
    print(f"  Target Leaves:     {TOTAL_LEAVES} ({NUM_TRANSMITTERS} TX x {NUM_RECEIVERS} RX x {NUM_DATES} Dates x {NUM_EQUALIZATIONS} Eq)")
    print(f"  Expected Bursts:   {TOTAL_LEAVES * BURSTS_PER_LEAF:,} feature records")
    print(f"  Output Directory:  {output_dir}")
    print(f"  Sample Rate:       {sample_rate_hz:,} Hz (REQUIRES VALIDATION)")

    config = ExtractorConfig(
        archive_path=archive_path,
        output_dir=output_dir,
        sample_rate_hz=sample_rate_hz,
        compression="SNAPPY",
    )
    extractor = ManySigFeatureExtractor(config)

    base_mem = get_process_memory()
    start_time = time.perf_counter()

    # Execute full single-pass streaming extraction
    manifest = extractor.extract_partitioned_dataset(output_dir)

    elapsed_time = time.perf_counter() - start_time
    end_mem = get_process_memory()

    print(f"\nExtraction pass completed in {elapsed_time:.2f} seconds ({manifest['total_rows'] / elapsed_time:,.1f} bursts/sec).")
    print(f"  Baseline Working Set: {base_mem['rss_mib']:.2f} MiB")
    print(f"  Peak Working Set:     {end_mem['peak_rss_mib']:.2f} MiB")
    print(f"  Memory Delta:         {end_mem['peak_rss_mib'] - base_mem['rss_mib']:.2f} MiB")

    # Post-extraction verification
    print("\n--- Running Independent Post-Extraction Verification ---")
    post_stat = archive_path.stat()
    archive_unmodified = (post_stat.st_mtime == pre_mtime and post_stat.st_size == pre_size)
    print(f"1. Raw Archive Unmodified Check: {archive_unmodified} (size={post_stat.st_size:,} bytes)")
    assert archive_unmodified, "CRITICAL: Raw archive was modified during extraction!"

    # Reopen and inspect every generated partition Parquet file
    total_reopened_rows = 0
    all_leaves_seen = set()
    all_burst_keys = set()
    tx_seen = set()
    rx_seen = set()
    dates_seen = set()
    eq_seen = set()
    total_parquet_bytes = 0

    partition_checks = []

    for part_key, part_meta in manifest["partitions"].items():
        part_file = output_dir / part_meta["relative_path"]
        assert part_file.exists(), f"Partition file missing: {part_file}"
        file_bytes = part_file.stat().st_size
        total_parquet_bytes += file_bytes

        # Verify streaming checksum
        calc_sha256 = compute_file_sha256(part_file)
        assert calc_sha256 == part_meta["sha256"], f"Checksum mismatch for {part_key}"

        # Reopen Parquet table using ParquetFile to avoid partition type inference conflict
        tbl = pq.ParquetFile(part_file).read()
        assert tbl.num_columns == 23, f"Expected 23 columns, got {tbl.num_columns}"
        part_rows = tbl.num_rows
        assert part_rows == part_meta["rows"], f"Row count mismatch in {part_key}: {part_rows} vs {part_meta['rows']}"
        total_reopened_rows += part_rows

        # Check coordinates and provenance
        leaf_indices = tbl["leaf_index"].to_numpy()
        burst_indices = tbl["burst_index"].to_numpy()
        tx_col = tbl["tx_id"].to_pylist()
        rx_col = tbl["rx_id"].to_pylist()
        date_col = tbl["capture_date"].to_pylist()
        eq_col = tbl["is_equalized"].to_pylist()

        for i in range(part_rows):
            l_idx = int(leaf_indices[i])
            b_idx = int(burst_indices[i])
            all_leaves_seen.add(l_idx)
            burst_key = (l_idx, b_idx)
            assert burst_key not in all_burst_keys, f"Duplicate burst record detected: {burst_key}"
            all_burst_keys.add(burst_key)

            tx_seen.add(tx_col[i])
            rx_seen.add(rx_col[i])
            dates_seen.add(date_col[i])
            eq_seen.add(eq_col[i])

        partition_checks.append({
            "partition": part_key,
            "rows": part_rows,
            "bytes": file_bytes,
            "sha256": calc_sha256,
        })

    print(f"2. Total Leaves Processed:       {len(all_leaves_seen)} (expected {TOTAL_LEAVES})")
    assert len(all_leaves_seen) == TOTAL_LEAVES, f"Expected {TOTAL_LEAVES} leaves, got {len(all_leaves_seen)}"

    print(f"3. Total Bursts / Feature Rows:  {total_reopened_rows:,} (expected {TOTAL_LEAVES * BURSTS_PER_LEAF:,})")
    assert total_reopened_rows == TOTAL_LEAVES * BURSTS_PER_LEAF, f"Expected {TOTAL_LEAVES * BURSTS_PER_LEAF} rows, got {total_reopened_rows}"

    print(f"4. Coordinate Cardinality:")
    print(f"   Transmitters (6 expected):   {sorted(list(tx_seen))}")
    print(f"   Receivers (12 expected):     {sorted(list(rx_seen))}")
    print(f"   Dates (4 expected):          {sorted(list(dates_seen))}")
    print(f"   Equalizations (2 expected):  {sorted(list(eq_seen))}")
    assert len(tx_seen) == NUM_TRANSMITTERS, f"Expected {NUM_TRANSMITTERS} TXs, got {len(tx_seen)}"
    assert len(rx_seen) == NUM_RECEIVERS, f"Expected {NUM_RECEIVERS} RXs, got {len(rx_seen)}"
    assert len(dates_seen) == NUM_DATES, f"Expected {NUM_DATES} dates, got {len(dates_seen)}"
    assert len(eq_seen) == NUM_EQUALIZATIONS, f"Expected {NUM_EQUALIZATIONS} eq states, got {len(eq_seen)}"

    print(f"5. Total Parquet Dataset Size:   {total_parquet_bytes:,} bytes ({total_parquet_bytes / (1024**2):.2f} MiB)")
    print(f"6. Partition Count:              {len(partition_checks)} partitions")
    print(f"7. Checksums Verified:           All {len(partition_checks)} partitions match manifest cryptographic digests.")

    summary = {
        "status": "COMPLETED_AND_VERIFIED",
        "dataset_name": "ManySig_TrackB_Features",
        "source_archive": str(archive_path.name),
        "source_archive_bytes": pre_size,
        "archive_unmodified": archive_unmodified,
        "total_leaves": len(all_leaves_seen),
        "total_rows": total_reopened_rows,
        "bursts_per_leaf": BURSTS_PER_LEAF,
        "tx_count": len(tx_seen),
        "rx_count": len(rx_seen),
        "date_count": len(dates_seen),
        "equalization_count": len(eq_seen),
        "tx_list": sorted(list(tx_seen)),
        "rx_list": sorted(list(rx_seen)),
        "date_list": sorted(list(dates_seen)),
        "equalized_list": sorted(list(eq_seen)),
        "sample_rate_hz": sample_rate_hz,
        "sample_rate_status": "REQUIRES VALIDATION (Engineering default)",
        "features": list(FEATURE_NAMES),
        "total_parquet_bytes": total_parquet_bytes,
        "partition_count": len(partition_checks),
        "elapsed_seconds": round(elapsed_time, 2),
        "bursts_per_second": round(total_reopened_rows / max(elapsed_time, 1e-6), 1),
        "baseline_rss_mib": round(base_mem["rss_mib"], 2),
        "peak_rss_mib": round(end_mem["peak_rss_mib"], 2),
        "delta_rss_mib": round(end_mem["peak_rss_mib"] - base_mem["rss_mib"], 2),
        "manifest_path": str((output_dir / "manifest.json").relative_to(Path(__file__).resolve().parents[1])),
    }

    summary_file = output_dir / "extraction_summary.json"
    summary_file.write_text(json.dumps(summary, indent=2))
    print(f"\nExecution summary saved to: {summary_file}")

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run complete ManySig streaming feature extraction")
    parser.add_argument(
        "--archive",
        type=Path,
        default=Path(r"C:\Users\sujit\Downloads\ManySig.pkl.zip"),
        help="Path to ManySig.pkl.zip",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "datasets" / "features" / "manysig",
        help="Target output directory for partitioned Parquet dataset",
    )
    parser.add_argument(
        "--sample-rate",
        type=float,
        default=20_000_000.0,
        help="Nominal baseband sample rate in Hz (default: 20 MHz)",
    )
    args = parser.parse_args()
    run_full_extraction(args.archive, args.out_dir, args.sample_rate)
