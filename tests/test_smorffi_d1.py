from pathlib import Path

from src.smorffi_d1 import iter_csv_records, validate_records


def test_smorffi_iq_style_csv(tmp_path: Path) -> None:
    path = tmp_path / "24:d7:eb:38:c7:e8_pre.csv"
    path.write_text(
        "device_number,mac_address,preamble\n"
        "24,24:d7:eb:38:c7:e8,1+2j;3+4j\n",
        encoding="utf-8",
    )

    records = list(iter_csv_records(path))

    assert len(records) == 1
    assert records[0].device_id == "24"
    assert records[0].mac_address == "24:d7:eb:38:c7:e8"
    assert records[0].raw_preamble == "1+2j;3+4j"
    assert validate_records(iter(records)) == []


def test_smorffi_feature_style_csv(tmp_path: Path) -> None:
    path = tmp_path / "device.csv"
    path.write_text(
        "device_number,mac_address,short_freq,long_freq,CFO,phase_error_mean\n"
        "7,aa:bb:cc:dd:ee:ff,0.1,0.2,0.3,0.4\n",
        encoding="utf-8",
    )

    record = next(iter_csv_records(path))

    assert record.device_id == "7"
    assert record.mac_address == "aa:bb:cc:dd:ee:ff"
    assert record.source_row["CFO"] == "0.3"
    assert record.raw_preamble is None


def test_missing_identity_is_reported(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    path.write_text(
        "device_number,mac_address,preamble\n"
        ",,1+2j\n",
        encoding="utf-8",
    )

    records = list(iter_csv_records(path))
    errors = validate_records(iter(records))

    assert any("missing device identifier" in error for error in errors)
    assert any("missing MAC address" in error for error in errors)
