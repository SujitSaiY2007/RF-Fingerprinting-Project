"""SMoRFFI-specific D1 ingestion helpers.

This module is intentionally metadata-first. It does not infer chronology,
receiver variation, environment variation, or session boundaries that the
published dataset does not expose. Large CSV files remain outside Git.

The published SMoRFFI release contains one CSV per device in two variants:
IQ-only and IQ-plus-RF-features. The loader records source-file provenance and
normalizes the fields that are explicitly present while preserving the full
source row for later D2/D3 processing.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import hashlib
from typing import Iterator, Mapping, Optional


@dataclass(frozen=True)
class SMoRFFIRecord:
    source_file: str
    row_index: int
    device_id: Optional[str]
    mac_address: Optional[str]
    raw_preamble: Optional[str]
    source_row: Mapping[str, str]


def _clean(value: object) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def _first(row: Mapping[str, str], names: tuple[str, ...]) -> Optional[str]:
    for name in names:
        if name in row:
            value = _clean(row[name])
            if value is not None:
                return value
    return None


def _device_id(row: Mapping[str, str], fallback: Optional[str]) -> Optional[str]:
    return _first(row, ("device_number", "device_id", "device", "tx_id")) or fallback


def _mac(row: Mapping[str, str]) -> Optional[str]:
    return _first(row, ("mac_address", "mac", "MAC", "MacAddress"))


def _preamble(row: Mapping[str, str]) -> Optional[str]:
    return _first(row, ("preamble", "raw_preamble", "raw_samples"))


def iter_csv_records(path: str | Path, device_id_fallback: Optional[str] = None) -> Iterator[SMoRFFIRecord]:
    """Yield normalized records from one published SMoRFFI CSV file."""
    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"SMoRFFI CSV has no header: {csv_path}")
        for row_index, row in enumerate(reader, start=1):
            normalized = {str(k).strip(): (v or "") for k, v in row.items() if k is not None}
            yield SMoRFFIRecord(
                source_file=str(csv_path),
                row_index=row_index,
                device_id=_device_id(normalized, device_id_fallback),
                mac_address=_mac(normalized),
                raw_preamble=_preamble(normalized),
                source_row=normalized,
            )


def iter_dataset_records(root: str | Path) -> Iterator[SMoRFFIRecord]:
    """Yield records from all CSV files below a local SMoRFFI data root."""
    root_path = Path(root)
    if not root_path.is_dir():
        raise FileNotFoundError(f"SMoRFFI data root does not exist: {root_path}")
    for csv_path in sorted(root_path.rglob("*.csv")):
        yield from iter_csv_records(csv_path)


def file_sha256(path: str | Path) -> str:
    """Return a deterministic SHA-256 checksum for a local dataset file."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_records(records: Iterator[SMoRFFIRecord]) -> list[str]:
    """Run metadata-only D1 checks without assuming unavailable metadata."""
    errors: list[str] = []
    count = 0
    for record in records:
        count += 1
        if not record.device_id:
            errors.append(f"{record.source_file}:{record.row_index}: missing device identifier")
        if not record.mac_address:
            errors.append(f"{record.source_file}:{record.row_index}: missing MAC address")
    if count == 0:
        errors.append("SMoRFFI input contains no records")
    return errors
