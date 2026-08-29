import tempfile
import unittest
from pathlib import Path

from src.d1_ingestion import (
    OregonStateWiFiLoader,
    WiSigLoader,
    manifest_checksum,
    validate_records,
    write_normalized_jsonl,
)


class D1IngestionTests(unittest.TestCase):
    def test_wisig_loader_normalizes_common_metadata(self):
        loader = WiSigLoader()
        records = loader.load_csv(self._write_manifest(
            "signal_path,device,rx,capture_day,frequency_hz,dtype\n"
            "data/a.bin,tx07,rx03,day2,2462000000,complex64\n"
        ))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].source_dataset, "WiSig")
        self.assertEqual(records[0].device_id, "tx07")
        self.assertEqual(records[0].receiver, "rx03")
        self.assertEqual(records[0].frequency_hz, 2462000000.0)
        self.assertEqual(records[0].raw_dtype, "complex64")
        self.assertEqual(validate_records(records), [])

    def test_oregon_loader_preserves_source_dataset(self):
        loader = OregonStateWiFiLoader()
        records = loader.load_csv(self._write_manifest(
            "filename,tx_id,session,scenario,channel\n"
            "capture_001.dat,device_12,session_4,indoor,1\n"
        ))
        self.assertEqual(records[0].source_dataset, "Oregon State WiFi RFFP")
        self.assertEqual(records[0].device_id, "device_12")
        self.assertEqual(records[0].session_id, "session_4")
        self.assertEqual(records[0].environment, "indoor")
        self.assertEqual(records[0].channel, "1")

    def test_validation_rejects_duplicate_signal_reference(self):
        loader = WiSigLoader()
        records = loader.load_csv(self._write_manifest(
            "signal_reference,device\n"
            "a.bin,tx1\n"
            "a.bin,tx2\n"
        ))
        errors = validate_records(records)
        self.assertTrue(any("duplicate signal_reference" in error for error in errors))

    def test_normalized_jsonl_is_reproducible_text(self):
        loader = WiSigLoader()
        records = loader.load_csv(self._write_manifest(
            "signal_reference,device\n"
            "a.bin,tx1\n"
        ))
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "normalized.jsonl"
            write_normalized_jsonl(records, output)
            first = output.read_text(encoding="utf-8")
            write_normalized_jsonl(records, output)
            second = output.read_text(encoding="utf-8")
            self.assertEqual(first, second)
            self.assertEqual(len(manifest_checksum(output)), 64)

    @staticmethod
    def _write_manifest(content: str) -> str:
        handle = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8")
        handle.write(content)
        handle.close()
        return handle.name


if __name__ == "__main__":
    unittest.main()
