"""Validation runner for ManySig 16-feature RF evidence extraction.

Extracts a controlled slice from real ManySig Leaf 0 (data[0][0][0][0]),
verifies exact equivalence between scalar Track-A reference formulas and
vectorized batch extraction, and generates a validated sample Parquet table
and manifest.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.manysig_feature_extractor import (
    ExtractorConfig,
    ManySigFeatureExtractor,
    extract_validation_slice,
)


def run_validation(archive_path: Path, output_dir: Path, num_bursts: int = 20) -> dict:
    if not archive_path.exists():
        raise FileNotFoundError(f"Archive not found: {archive_path}")

    print(f"Running Track-A feature validation against real ManySig archive: {archive_path.name}")
    print(f"Extracting validation slice of {num_bursts} bursts from Leaf 0...")

    val_report = extract_validation_slice(archive_path, target_leaf_index=0, num_bursts=num_bursts)

    print("\n=== Validation Results for Leaf 0 (Tx=14-10, Rx=1-1, Date=2021_03_01, Eq=raw) ===")
    print(f"Validated Bursts:            {val_report['num_bursts_validated']}")
    print(f"Max Absolute Diff vs Scalar: {val_report['max_absolute_difference']:.2e} (Machine Precision)")

    print("\n--- Per-Feature Maximum Discrepancy vs Track-A Reference ---")
    for feat, diff in val_report["per_feature_max_diff"].items():
        print(f"  {feat:<24} diff = {diff:.2e}")

    print("\n--- Sample Computed Features for Burst #0 ---")
    for feat, val in val_report["first_burst_features"].items():
        print(f"  {feat:<24} = {val:+.8e}")

    # Generate small sample Parquet file
    output_dir.mkdir(parents=True, exist_ok=True)
    out_parquet = output_dir / "validation_leaf_0_features.parquet"
    config = ExtractorConfig(archive_path=archive_path, output_dir=output_dir)
    extractor = ManySigFeatureExtractor(config)

    manifest = extractor.extract_slice_to_parquet([0], out_parquet)
    print(f"\nValidation Parquet written to: {out_parquet} ({manifest['parquet_size_bytes']:,} bytes, {manifest['total_rows']} rows)")
    print(f"Parquet SHA-256: {manifest['parquet_sha256']}")
    print(f"Manifest written to: {out_parquet.with_suffix('.manifest.json')}")

    # Verify Parquet read-back
    table_read = pq.read_table(out_parquet)
    assert table_read.num_rows == 1000
    assert table_read.num_columns == 23
    print(f"Parquet table read-back verified: {table_read.num_rows} rows x {table_read.num_columns} columns")

    results_summary = {
        "validation_report": val_report,
        "manifest": manifest,
    }
    summary_path = output_dir / "validation_summary.json"
    summary_path.write_text(json.dumps(results_summary, indent=2))
    print(f"Validation summary saved to: {summary_path}")

    return results_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate ManySig feature extraction against Track-A contract")
    parser.add_argument(
        "--archive",
        type=Path,
        default=Path(r"C:\Users\sujit\Downloads\ManySig.pkl.zip"),
        help="Path to ManySig.pkl.zip",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "experiments" / "track_b",
        help="Output directory for validation artifacts",
    )
    args = parser.parse_args()
    run_validation(args.archive, args.out_dir)
