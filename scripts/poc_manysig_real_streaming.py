"""Proof-of-concept runner for real ManySig.pkl streaming ingestion.

This script benchmarks memory boundedness, throughput, and cryptographic
correctness of the custom streaming unpickler against the actual ManySig
archive on the local filesystem.
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

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.manysig_streamer import (
    TOTAL_LEAVES,
    BURSTS_PER_LEAF,
    coordinate_from_index,
    extract_single_leaf,
    stream_all_leaves,
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


def run_benchmark(zip_path: Path, output_path: Optional[Path] = None) -> dict:
    if not zip_path.exists():
        raise FileNotFoundError(f"ManySig zip archive not found at: {zip_path}")

    results = {
        "stage": "Track-B Pre-Ingestion Streaming POC",
        "archive_path": str(zip_path),
        "archive_size_bytes": zip_path.stat().st_size,
        "single_leaf_tests": [],
        "full_stream_benchmark": {},
    }

    # 1. Single leaf tests across the stream
    test_indices = [0, 288, 575]
    for idx in test_indices:
        base_mem = get_process_memory()
        start = time.perf_counter()
        coord, leaf, meta = extract_single_leaf(zip_path, idx)
        elapsed = time.perf_counter() - start
        end_mem = get_process_memory()

        sha256 = hashlib.sha256(leaf.tobytes()).hexdigest()
        mean_i = float(np.mean(leaf[:, :, 0]))
        mean_q = float(np.mean(leaf[:, :, 1]))
        rms = float(np.sqrt(np.mean(leaf[:, :, 0] ** 2 + leaf[:, :, 1] ** 2)))

        leaf_result = {
            "leaf_index": idx,
            "tx_id": coord.tx_id,
            "rx_id": coord.rx_id,
            "date": coord.date,
            "is_equalized": coord.is_equalized,
            "shape": list(leaf.shape),
            "dtype": str(leaf.dtype),
            "byte_length": int(leaf.nbytes),
            "sha256": sha256,
            "mean_i": mean_i,
            "mean_q": mean_q,
            "rms_amplitude": rms,
            "baseline_rss_mib": round(base_mem["rss_mib"], 2),
            "peak_rss_mib": round(end_mem["peak_rss_mib"], 2),
            "current_rss_mib": round(end_mem["rss_mib"], 2),
            "delta_rss_mib": round(end_mem["peak_rss_mib"] - base_mem["rss_mib"], 2),
            "elapsed_seconds": round(elapsed, 2),
        }
        results["single_leaf_tests"].append(leaf_result)
        print(f"[Single Leaf {idx:3d}] Tx={coord.tx_id} Rx={coord.rx_id} Date={coord.date} Eq={coord.is_equalized} | "
              f"Peak RSS: {leaf_result['peak_rss_mib']} MiB (Delta: {leaf_result['delta_rss_mib']} MiB) | "
              f"Time: {leaf_result['elapsed_seconds']}s | SHA256: {sha256[:16]}...")

    # 2. Full sequential stream of all 576 leaves
    base_stream_mem = get_process_memory()
    start_stream = time.perf_counter()

    leaves_seen = 0
    bursts_seen = 0

    def stream_callback(c, arr):
        nonlocal leaves_seen, bursts_seen
        leaves_seen += 1
        bursts_seen += len(arr)

    meta = stream_all_leaves(zip_path, stream_callback)
    elapsed_stream = time.perf_counter() - start_stream
    end_stream_mem = get_process_memory()

    results["full_stream_benchmark"] = {
        "total_leaves_processed": leaves_seen,
        "total_signal_bursts": bursts_seen,
        "tx_count": len(meta["tx_list"]),
        "rx_count": len(meta["rx_list"]),
        "date_count": len(meta["capture_date_list"]),
        "baseline_rss_mib": round(base_stream_mem["rss_mib"], 2),
        "peak_rss_mib": round(end_stream_mem["peak_rss_mib"], 2),
        "current_rss_mib": round(end_stream_mem["rss_mib"], 2),
        "delta_rss_mib": round(end_stream_mem["peak_rss_mib"] - base_stream_mem["rss_mib"], 2),
        "elapsed_seconds": round(elapsed_stream, 2),
        "bursts_per_second": round(bursts_seen / max(elapsed_stream, 1e-6), 1),
    }

    print(f"\n[Full Stream] Processed {leaves_seen} leaves ({bursts_seen:,} bursts) in {results['full_stream_benchmark']['elapsed_seconds']}s "
          f"({results['full_stream_benchmark']['bursts_per_second']:,} bursts/s)")
    print(f"[Full Stream Memory] Baseline: {results['full_stream_benchmark']['baseline_rss_mib']} MiB | "
          f"Peak: {results['full_stream_benchmark']['peak_rss_mib']} MiB | "
          f"Delta: {results['full_stream_benchmark']['delta_rss_mib']} MiB")

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(results, indent=2))
        print(f"\nResults written to: {output_path}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ManySig Real Streaming POC Runner")
    parser.add_argument(
        "--archive",
        type=Path,
        default=Path(r"C:\Users\sujit\Downloads\ManySig.pkl.zip"),
        help="Path to ManySig.pkl.zip",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "experiments" / "track_b" / "poc_manysig_streaming_results.json",
        help="Output results JSON path",
    )
    args = parser.parse_args()
    run_benchmark(args.archive, args.out)
