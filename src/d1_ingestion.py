"""D1 raw-RF ingestion primitives.

This module deliberately separates dataset metadata ingestion from raw signal
interpretation. Dataset-specific loaders normalize source metadata into a
common schema without inventing values that are absent from the source.

Large RF files stay outside Git. A manifest row references a local signal file
(or another source-specific identifier) and records provenance/metadata.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import hashlib
import json
from typing import Iterable, Mapping, Optional


COMMON_FIELDS = (
    "signal_reference",
    "device_id",
    "session_id",
    "day",
    "date",
    "receiver",
    "environment",
    "location",
    "channel",
    "frequency_hz",
    "source_dataset",
    "raw_shape",
    "raw_dtype",
    "preprocessing_status",
)


@dataclass(frozen=True)
class RFRecord:
    signal_reference: str
    device_id: Optional[str] = None
    session_id: Optional[str] = None
    day: Optional[str] = None
    date: Optional[str] = None
    receiver: Optional[str] = None
    environment: Optional[str] = None
    location: Optional[str] = None
    channel: Optional[str] = None
    frequency_hz: Optional[float] = None
    source_dataset: Optional[str] = None
    raw_shape: Optional[str] = None
    raw_dtype: Optional[str] = None
    preprocessing_status: str = "raw/unprocessed"

    def to_dict(self) -> dict:
        return asdict(self)


def _clean(value: object) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def _float_or_none(value: object) -> Optional[float]:
    text = _clean(value)
    if text is None:
        return None
    try:
        return float(text)
    except ValueError as exc:
        raise ValueError(f"frequency_hz must be numeric, got {value!r}") from exc


def _first(row: Mapping[str, object], aliases: Iterable[str]) -> Optional[object]:
    for key in aliases:
        if key in row and _clean(row[key]) is not None:
            return row[key]
    return None


class ManifestLoader:
    """Load a CSV manifest and normalize it to the project D1 schema."""

    dataset_name = "generic"
    aliases: Mapping[str, tuple[str, ...]] = {
        "signal_reference": ("signal_reference", "signal_path", "path", "file", "filename"),
        "device_id": ("device_id", "device", "tx", "transmitter", "tx_id"),
        "session_id": ("session_id", "session", "capture_id", "capture"),
        "day": ("day", "capture_day"),
        "date": ("date", "capture_date"),
        "receiver": ("receiver", "rx", "rx_id"),
        "environment": ("environment", "scenario", "setup"),
        "location": ("location", "site"),
        "channel": ("channel", "wifi_channel"),
        "frequency_hz": ("frequency_hz", "frequency", "center_frequency_hz"),
        "raw_shape": ("raw_shape", "shape"),
        "raw_dtype": ("raw_dtype", "dtype"),
        "preprocessing_status": ("preprocessing_status", "status"),
    }

    def normalize_row(self, row: Mapping[str, object]) -> RFRecord:
        signal_reference = _clean(_first(row, self.aliases["signal_reference"]))
        if signal_reference is None:
            raise ValueError("manifest row is missing a signal reference")

        return RFRecord(
            signal_reference=signal_reference,
            device_id=_clean(_first(row, self.aliases["device_id"])),
            session_id=_clean(_first(row, self.aliases["session_id"])),
            day=_clean(_first(row, self.aliases["day"])),
            date=_clean(_first(row, self.aliases["date"])),
            receiver=_clean(_first(row, self.aliases["receiver"])),
            environment=_clean(_first(row, self.aliases["environment"])),
            location=_clean(_first(row, self.aliases["location"])),
            channel=_clean(_first(row, self.aliases["channel"])),
            frequency_hz=_float_or_none(_first(row, self.aliases["frequency_hz"])),
            source_dataset=self.dataset_name,
            raw_shape=_clean(_first(row, self.aliases["raw_shape"])),
            raw_dtype=_clean(_first(row, self.aliases["raw_dtype"])),
            preprocessing_status=_clean(_first(row, self.aliases["preprocessing_status"]))
            or "raw/unprocessed",
        )

    def load_csv(self, manifest_path: str | Path) -> list[RFRecord]:
        path = Path(manifest_path)
        with path.open("r", encoding="utf-8", newline="") as handle:
            return [self.normalize_row(row) for row in csv.DictReader(handle)]


class WiSigLoader(ManifestLoader):
    """WiSig metadata loader.

    The loader intentionally does not assume a particular compact-subset file
    layout. The official dataset offers multiple prepackaged subsets and a
    much larger raw archive; local signal paths therefore belong in the
    project-generated manifest rather than in code.
    """

    dataset_name = "WiSig"


class OregonStateWiFiLoader(ManifestLoader):
    """Oregon State WiFi RFFP metadata loader.

    The public release uses per-recording metadata and raw I/Q files. The
    loader keeps source metadata intact while mapping common aliases into the
    project schema.
    """

    dataset_name = "Oregon State WiFi RFFP"


def manifest_checksum(path: str | Path, algorithm: str = "sha256") -> str:
    """Return a checksum for a manifest or other local text/binary artifact."""
    digest = hashlib.new(algorithm)
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_normalized_jsonl(records: Iterable[RFRecord], output_path: str | Path) -> None:
    """Write normalized metadata without copying the underlying RF samples."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record.to_dict(), sort_keys=True) + "\n")


def validate_records(records: Iterable[RFRecord]) -> list[str]:
    """Return deterministic D1 validation errors; an empty list means valid."""
    errors: list[str] = []
    seen: set[str] = set()
    for index, record in enumerate(records, start=1):
        if not record.signal_reference:
            errors.append(f"row {index}: empty signal_reference")
        if record.signal_reference in seen:
            errors.append(f"row {index}: duplicate signal_reference")
        seen.add(record.signal_reference)
        if record.frequency_hz is not None and record.frequency_hz <= 0:
            errors.append(f"row {index}: frequency_hz must be positive")
    return errors
