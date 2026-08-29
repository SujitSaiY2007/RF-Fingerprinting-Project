import json

import pytest

from src.oracle_d1 import (
    ORACLE_ACTUAL_DTYPE,
    ORACLE_DATASET_NAME,
    discover_oracle_records,
    parse_oracle_metadata,
    validate_oracle_records,
)


def _write_recording(tmp_path):
    meta = tmp_path / "2ft" / "WiFi_air_X310_3123D7B_2ft_run1.sigmf-meta"
    meta.parent.mkdir()
    data = meta.with_suffix(".sigmf-data")
    data.write_bytes(b"placeholder")
    meta.write_text(
        json.dumps(
            {
                "global": {
                    "core:datatype": "cf32",
                    "core:sample_rate": 5000000.0,
                    "core:frequency": 2450000000.0,
                },
                "annotations": [
                    {
                        "environment": "outdoor",
                        "distance": "2ft",
                        "transmitter_identification": {"serial_number": "3123D7B"},
                        "receiver_identification": {"serial_number": "B210-1"},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return meta, data


def test_parse_oracle_metadata_normalizes_documented_fields(tmp_path):
    meta, data = _write_recording(tmp_path)

    record = parse_oracle_metadata(meta)

    assert record.signal_reference == str(data)
    assert record.device_id == "3123D7B"
    assert record.receiver == "B210-1"
    assert record.environment == "outdoor"
    assert record.location == "2ft"
    assert record.frequency_hz == 2450000000.0
    assert record.source_dataset == ORACLE_DATASET_NAME
    assert record.raw_dtype == ORACLE_ACTUAL_DTYPE


def test_discovery_and_validation_pass_for_valid_fixture(tmp_path):
    _write_recording(tmp_path)

    records = discover_oracle_records(tmp_path)

    assert len(records) == 1
    assert validate_oracle_records(records) == []


def test_missing_data_file_is_rejected(tmp_path):
    meta, data = _write_recording(tmp_path)
    data.unlink()

    with pytest.raises(FileNotFoundError):
        parse_oracle_metadata(meta)
