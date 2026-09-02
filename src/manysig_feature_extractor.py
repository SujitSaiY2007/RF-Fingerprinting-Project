"""Streaming Feature-Extraction Runner for WiSig ManySig.

This module consumes raw (1000, 256, 2) I/Q burst leaves from the memory-bounded
ManySig streaming unpickler (src.manysig_streamer), extracts the 16 Track-A
RF evidence features per burst, and writes partitioned Parquet tables with
cryptographic manifest provenance.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Callable, Optional, Sequence, Tuple
import time

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from src.manysig_features import (
    DEFAULT_SAMPLE_RATE_HZ,
    FEATURE_NAMES,
    extract_burst_features_batch,
    extract_burst_features_scalar,
    get_feature_arrow_schema,
)
from src.manysig_streamer import (
    BURSTS_PER_LEAF,
    SAMPLES_PER_BURST,
    TOTAL_LEAVES,
    LeafCoordinate,
    extract_single_leaf,
    stream_all_leaves,
)


def compute_file_sha256(file_path: Path, chunk_size: int = 65536) -> str:
    """Compute SHA-256 digest of a file in streaming chunks without loading the entire file into RAM."""
    hasher = hashlib.sha256()
    with file_path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


@dataclass(frozen=True)
class ExtractorConfig:
    archive_path: Path
    output_dir: Path
    sample_rate_hz: float = DEFAULT_SAMPLE_RATE_HZ
    compression: str = "SNAPPY"
    partition_columns: Tuple[str, ...] = ("rx_id", "is_equalized")


def build_arrow_table_from_leaf(
    coord: LeafCoordinate,
    leaf_array: np.ndarray,
    sample_rate_hz: float = DEFAULT_SAMPLE_RATE_HZ,
    max_bursts: Optional[int] = None,
) -> pa.Table:
    """Transform a (1000, 256, 2) leaf array into a typed PyArrow Table of feature records."""
    if leaf_array.ndim != 3 or leaf_array.shape[1] != SAMPLES_PER_BURST or leaf_array.shape[2] != 2:
        raise ValueError(f"expected leaf array shape (N, {SAMPLES_PER_BURST}, 2), got {leaf_array.shape}")

    n_bursts = len(leaf_array) if max_bursts is None else min(len(leaf_array), max_bursts)
    burst_slice = leaf_array[:n_bursts]

    # Compute 16 RF evidence features in one vectorized pass
    feats = extract_burst_features_batch(burst_slice, sample_rate_hz=sample_rate_hz)

    # Build columnar arrays
    arrays = [
        pa.array(np.full(n_bursts, coord.leaf_index, dtype=np.int16), type=pa.int16()),
        pa.array(np.arange(n_bursts, dtype=np.int16), type=pa.int16()),
        pa.array([coord.tx_id] * n_bursts, type=pa.string()),
        pa.array([coord.rx_id] * n_bursts, type=pa.string()),
        pa.array([coord.date] * n_bursts, type=pa.string()),
        pa.array([coord.is_equalized] * n_bursts, type=pa.bool_()),
        pa.array(np.full(n_bursts, SAMPLES_PER_BURST, dtype=np.int16), type=pa.int16()),
    ]

    for feat_name in FEATURE_NAMES:
        arrays.append(pa.array(feats[feat_name], type=pa.float64()))

    schema = get_feature_arrow_schema()
    return pa.Table.from_arrays(arrays, schema=schema)


def extract_validation_slice(
    archive_path: Path,
    target_leaf_index: int = 0,
    num_bursts: int = 10,
    sample_rate_hz: float = DEFAULT_SAMPLE_RATE_HZ,
) -> dict:
    """Extract a small validation slice and verify exact mathematical equivalence between scalar and batch implementations."""
    coord, leaf_array, meta = extract_single_leaf(archive_path, target_leaf_index)
    table = build_arrow_table_from_leaf(coord, leaf_array, sample_rate_hz=sample_rate_hz, max_bursts=num_bursts)

    # Verify each burst against the scalar reference function
    max_abs_diff = 0.0
    diff_report = {}
    for b in range(num_bursts):
        scalar_dict = extract_burst_features_scalar(leaf_array[b], sample_rate_hz=sample_rate_hz)
        for feat in FEATURE_NAMES:
            table_val = table[feat][b].as_py()
            scalar_val = scalar_dict[feat]
            diff = abs(table_val - scalar_val)
            if diff > max_abs_diff:
                max_abs_diff = diff
            diff_report[feat] = max(diff_report.get(feat, 0.0), diff)

    return {
        "leaf_index": target_leaf_index,
        "tx_id": coord.tx_id,
        "rx_id": coord.rx_id,
        "date": coord.date,
        "is_equalized": coord.is_equalized,
        "num_bursts_validated": num_bursts,
        "max_absolute_difference": max_abs_diff,
        "per_feature_max_diff": diff_report,
        "first_burst_features": {f: table[f][0].as_py() for f in FEATURE_NAMES},
    }


class ManySigFeatureExtractor:
    """Manages streaming feature extraction, partitioned writing, and manifest generation."""

    def __init__(self, config: ExtractorConfig):
        self.config = config

    def extract_slice_to_parquet(
        self,
        target_leaf_indices: Sequence[int],
        output_file: Path,
    ) -> dict:
        """Extract a designated sequence of leaves and write a single validated Parquet file with streaming manifest."""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        schema = get_feature_arrow_schema()

        total_rows = 0
        leaves_processed = 0
        start_time = time.perf_counter()

        with pq.ParquetWriter(output_file, schema=schema, compression=self.config.compression) as writer:
            for idx in target_leaf_indices:
                coord, leaf, _ = extract_single_leaf(self.config.archive_path, idx)
                tbl = build_arrow_table_from_leaf(coord, leaf, sample_rate_hz=self.config.sample_rate_hz)
                writer.write_table(tbl)
                total_rows += len(tbl)
                leaves_processed += 1

        elapsed = time.perf_counter() - start_time
        file_bytes = output_file.stat().st_size
        file_sha256 = compute_file_sha256(output_file)

        manifest = {
            "dataset_name": "ManySig_Validation_Slice",
            "source_archive": str(self.config.archive_path.name),
            "target_leaves": list(target_leaf_indices),
            "total_leaves_processed": leaves_processed,
            "total_rows": total_rows,
            "sample_rate_hz": self.config.sample_rate_hz,
            "sample_rate_status": "REQUIRES VALIDATION (Engineering default)",
            "features": list(FEATURE_NAMES),
            "parquet_file": str(output_file.name),
            "parquet_size_bytes": file_bytes,
            "parquet_sha256": file_sha256,
            "elapsed_seconds": round(elapsed, 2),
        }

        manifest_path = output_file.with_suffix(".manifest.json")
        manifest_path.write_text(json.dumps(manifest, indent=2))

        return manifest

    def extract_partitioned_dataset(
        self,
        output_dir: Path,
        target_leaf_indices: Optional[Sequence[int]] = None,
    ) -> dict:
        """Extract leaves into a partitioned Parquet layout (by rx_id and is_equalized) with streaming manifests."""
        output_dir.mkdir(parents=True, exist_ok=True)
        schema = get_feature_arrow_schema()

        open_writers: dict[str, pq.ParquetWriter] = {}
        partition_files: dict[str, Path] = {}
        partition_row_counts: dict[str, int] = {}
        leaves_processed = 0
        total_rows = 0
        start_time = time.perf_counter()

        def process_leaf_record(coord: LeafCoordinate, leaf_arr: np.ndarray):
            nonlocal leaves_processed, total_rows
            tbl = build_arrow_table_from_leaf(coord, leaf_arr, sample_rate_hz=self.config.sample_rate_hz)

            # Determine partition path: rx_id=<rx>/is_equalized=<0|1>
            eq_str = "1" if coord.is_equalized else "0"
            part_key = f"rx_id={coord.rx_id}/is_equalized={eq_str}"
            part_dir = output_dir / part_key

            if part_key not in open_writers:
                part_dir.mkdir(parents=True, exist_ok=True)
                part_file = part_dir / "data.parquet"
                open_writers[part_key] = pq.ParquetWriter(
                    part_file,
                    schema=schema,
                    compression=self.config.compression,
                )
                partition_files[part_key] = part_file
                partition_row_counts[part_key] = 0

            open_writers[part_key].write_table(tbl)
            partition_row_counts[part_key] += len(tbl)
            total_rows += len(tbl)
            leaves_processed += 1

        try:
            if target_leaf_indices is None:
                # High-performance single-pass streaming across all 576 leaves
                stream_all_leaves(self.config.archive_path, on_leaf_callback=process_leaf_record)
            else:
                for idx in target_leaf_indices:
                    coord, leaf, _ = extract_single_leaf(self.config.archive_path, idx)
                    process_leaf_record(coord, leaf)
        finally:
            # Close all writers safely
            for writer in open_writers.values():
                writer.close()

        elapsed = time.perf_counter() - start_time

        # Calculate partition file sizes and streaming SHA-256 digests
        partitions_manifest = {}
        for part_key, part_file in partition_files.items():
            partitions_manifest[part_key] = {
                "relative_path": str(part_file.relative_to(output_dir)),
                "rows": partition_row_counts[part_key],
                "size_bytes": part_file.stat().st_size,
                "sha256": compute_file_sha256(part_file),
            }

        root_manifest = {
            "dataset_name": "ManySig_Partitioned_Features",
            "source_archive": str(self.config.archive_path.name),
            "partition_columns": list(self.config.partition_columns),
            "sample_rate_hz": self.config.sample_rate_hz,
            "sample_rate_status": "REQUIRES VALIDATION (Engineering default)",
            "total_leaves_processed": leaves_processed,
            "total_rows": total_rows,
            "features": list(FEATURE_NAMES),
            "partitions": partitions_manifest,
            "elapsed_seconds": round(elapsed, 2),
        }

        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(json.dumps(root_manifest, indent=2))

        return root_manifest
