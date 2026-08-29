"""ORACLE-specific D1 ingestion for SigMF-compatible recordings.

The official ORACLE release describes each recording with a ``.sigmf-meta``
file and stores raw IQ in the paired ``.sigmf-data`` file. The publisher notes
that the binary samples are actually complex128 even though some metadata says
complex64; this loader therefore treats the metadata as provenance while
requiring the caller to opt into the published complex128 interpretation.

This module does not download or copy raw RF data. It discovers local ORACLE
metadata, validates the paired data file, extracts provenance fields and
produces the project's common RFRecord objects.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import json
from typing import Any, Iterable

from d1_ingestion import RFRecord, validate_records, write_normalized_jsonl


ORACLE_DATASET_NAME = "ORACLE Raw IQ Dataset #1"
ORACLE_SAMPLE_RATE_HZ = 5_000_000.0
ORACLE_CENTER_FREQUENCY_HZ = 2_450_000_000.0
ORACLE_ACTUAL_DTYPE = "complex128"


def _get(mapping: dict[str, Any], *keys: str) -> Any:
    """Return the first present key from a mapping."""
    for key in keys:
        if key in mapping:
            return mapping[key]
    return None


def _nested(mapping: dict[str, Any], namespace: str, key: str) -> Any:
    value = mapping.get(namespace, {})
    if isinstance(value, dict):
        return value.get(key)
    return None


def _device_id(annotation: dict[str, Any], filename: str) -> str | None:
    tx = _get(annotation, "transmitter_identification", "genesys:transmitter_identification")
    if isinstance(tx, dict):
        serial = _get(tx, "serial_number", "genesys:serial_number")
        if serial:
            return str(serial)

    # Fallback to the documented ORACLE filename convention:
    # WiFi_air_X310_<serial>_<distance>_run<id>
    stem = Path(filename).name
    parts = stem.split("_")
    if len(parts) >= 4 and parts[0].lower() == "wifi" and parts[1].lower() == "air":
        return parts[3]
    return None


def _annotation_for_capture(metadata: dict[str, Any]) -> dict[str, Any]:
    annotations = metadata.get("annotations", [])
    if isinstance(annotations, list) and annotations:
        first = annotations[0]
        if isinstance(first, dict):
            return first
    return {}


def parse_oracle_metadata(meta_path: str | Path, require_data_file: bool = True) -> RFRecord:
    """Parse one ORACLE ``.sigmf-meta`` file into the common D1 schema."""
    meta = Path(meta_path)
    with meta.open("r", encoding="utf-8") as handle:
        document = json.load(handle)

    if not isinstance(document, dict):
        raise ValueError(f"ORACLE metadata must be a JSON object: {meta}")

    global_obj = document.get("global", {})
    if not isinstance(global_obj, dict):
        raise ValueError(f"ORACLE metadata has invalid global object: {meta}")

    annotation = _annotation_for_capture(document)
    data_path = meta.with_suffix(".sigmf-data")
    if require_data_file and not data_path.is_file():
        raise FileNotFoundError(f"missing paired ORACLE data file: {data_path}")

    datatype = _get(global_obj, "core:datatype", "datatype")
    # ORACLE explicitly documents the released binary as complex128 despite
    # metadata that may declare complex64. Keep this discrepancy visible.
    raw_dtype = ORACLE_ACTUAL_DTYPE if datatype in {"cf32", "complex64", "complex128"} else datatype

    sample_rate = _get(global_obj, "core:sample_rate", "sample_rate")
    frequency = _get(global_obj, "core:frequency", "frequency", "core:center_frequency")
    if frequency is None:
        frequency = ORACLE_CENTER_FREQUENCY_HZ

    tx = _get(annotation, "transmitter_identification", "genesys:transmitter_identification")
    rx = _get(annotation, "receiver_identification", "genesys:receiver_identification")
    tx_name = tx.get("serial_number") if isinstance(tx, dict) else None
    rx_name = rx.get("serial_number") if isinstance(rx, dict) else None

    environment = _get(annotation, "environment", "genesys:environment")
    distance = _get(annotation, "distance", "genesys:distance")
    filename = data_path.name

    return RFRecord(
        signal_reference=str(data_path),
        device_id=str(tx_name or _device_id(annotation, filename)) if (tx_name or _device_id(annotation, filename)) else None,
        session_id=_get(annotation, "run", "run_id", "genesys:run"),
        day=None,
        date=_get(annotation, "datetime", "core:datetime"),
        receiver=str(rx_name) if rx_name else None,
        environment=str(environment) if environment is not None else None,
        location=str(distance) if distance is not None else None,
        channel=None,
        frequency_hz=float(frequency) if frequency is not None else None,
        source_dataset=ORACLE_DATASET_NAME,
        raw_shape=None,
        raw_dtype=str(raw_dtype) if raw_dtype is not None else None,
        preprocessing_status="raw/unprocessed",
    )


def discover_oracle_records(root: str | Path, require_data_file: bool = True) -> list[RFRecord]:
    """Discover and parse all ORACLE metadata files below ``root``."""
    base = Path(root)
    if not base.is_dir():
        raise NotADirectoryError(f"ORACLE root is not a directory: {base}")

    records: list[RFRecord] = []
    for meta_path in sorted(base.rglob("*.sigmf-meta")):
        records.append(parse_oracle_metadata(meta_path, require_data_file=require_data_file))

    if not records:
        raise FileNotFoundError(f"no .sigmf-meta files found below {base}")
    return records


def oracle_file_sha512(data_path: str | Path) -> str:
    """Compute SHA-512 for a raw ORACLE data file for provenance checking."""
    digest = hashlib.sha512()
    with Path(data_path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_oracle_records(records: Iterable[RFRecord]) -> list[str]:
    """Run common D1 validation plus ORACLE-specific invariants."""
    records = list(records)
    errors = validate_records(records)
    for index, record in enumerate(records, start=1):
        if record.source_dataset != ORACLE_DATASET_NAME:
            errors.append(f"row {index}: unexpected source_dataset")
        if record.raw_dtype != ORACLE_ACTUAL_DTYPE:
            errors.append(f"row {index}: ORACLE raw_dtype must be complex128")
        if record.frequency_hz is not None and record.frequency_hz <= 0:
            errors.append(f"row {index}: invalid ORACLE frequency")
    return errors


def write_oracle_manifest(root: str | Path, output_path: str | Path) -> None:
    """Discover, validate and write normalized ORACLE JSONL metadata."""
    records = discover_oracle_records(root)
    errors = validate_oracle_records(records)
    if errors:
        raise ValueError("ORACLE D1 validation failed:\n" + "\n".join(errors))
    write_normalized_jsonl(records, output_path)
