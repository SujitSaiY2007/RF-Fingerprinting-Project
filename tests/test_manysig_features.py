import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pyarrow.parquet as pq

from src.manysig_features import (
    FEATURE_NAMES,
    extract_burst_features_batch,
    extract_burst_features_scalar,
    get_feature_arrow_schema,
)
from src.manysig_feature_extractor import (
    ExtractorConfig,
    ManySigFeatureExtractor,
    build_arrow_table_from_leaf,
)
from src.manysig_streamer import LeafCoordinate
from src.smorffi_d3 import extract_rf_features as smorffi_extract_features


class TestManySigFeatures(unittest.TestCase):
    def test_feature_names_match_track_a(self):
        # Generate dummy 288-sample complex array for Track-A smorffi_d3
        dummy_288 = np.ones(288, dtype=np.complex128) + 1j * np.ones(288, dtype=np.complex128)
        track_a_dict = smorffi_extract_features(dummy_288)

        self.assertEqual(len(FEATURE_NAMES), 16)
        self.assertEqual(len(track_a_dict), 16)
        for name in FEATURE_NAMES:
            self.assertIn(name, track_a_dict)

    def test_scalar_vs_batch_mathematical_identity(self):
        np.random.seed(12345)
        # 50 bursts of shape (50, 256, 2)
        bursts = np.random.randn(50, 256, 2)
        batch_results = extract_burst_features_batch(bursts)

        for b in range(50):
            scalar_results = extract_burst_features_scalar(bursts[b])
            for feat in FEATURE_NAMES:
                batch_val = batch_results[feat][b]
                scalar_val = scalar_results[feat]
                self.assertAlmostEqual(
                    batch_val,
                    scalar_val,
                    places=12,
                    msg=f"Mismatch on burst {b}, feature {feat}: batch={batch_val}, scalar={scalar_val}",
                )

    def test_arrow_schema_definition(self):
        schema = get_feature_arrow_schema()
        self.assertEqual(len(schema), 23)  # 7 coordinate/provenance + 16 features
        expected_meta = ["leaf_index", "burst_index", "tx_id", "rx_id", "capture_date", "is_equalized", "sample_count"]
        for m in expected_meta:
            self.assertIn(m, schema.names)
        for f in FEATURE_NAMES:
            self.assertIn(f, schema.names)

    def test_build_arrow_table_from_leaf(self):
        coord = LeafCoordinate(
            leaf_index=42,
            tx_index=1,
            tx_id="14-7",
            rx_index=2,
            rx_id="14-7",
            date_index=0,
            date="2021_03_01",
            equalized_index=0,
            is_equalized=False,
        )
        leaf_array = np.random.randn(1000, 256, 2)
        table = build_arrow_table_from_leaf(coord, leaf_array)

        self.assertEqual(table.num_rows, 1000)
        self.assertEqual(table.num_columns, 23)
        self.assertEqual(table["leaf_index"][0].as_py(), 42)
        self.assertEqual(table["burst_index"][999].as_py(), 999)
        self.assertEqual(table["tx_id"][0].as_py(), "14-7")
        self.assertEqual(table["rx_id"][0].as_py(), "14-7")
        self.assertEqual(table["capture_date"][0].as_py(), "2021_03_01")
        self.assertEqual(table["is_equalized"][0].as_py(), False)
        self.assertEqual(table["sample_count"][0].as_py(), 256)

    def test_parquet_roundtrip(self):
        coord = LeafCoordinate(
            leaf_index=0,
            tx_index=0,
            tx_id="14-10",
            rx_index=0,
            rx_id="1-1",
            date_index=0,
            date="2021_03_01",
            equalized_index=0,
            is_equalized=False,
        )
        leaf_array = np.random.randn(100, 256, 2)
        table = build_arrow_table_from_leaf(coord, leaf_array)

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "test_leaf.parquet"
            pq.write_table(table, out_file)

            read_table = pq.read_table(out_file)
            self.assertEqual(read_table.num_rows, 100)
            self.assertEqual(read_table.num_columns, 23)
            self.assertTrue(np.allclose(read_table["i_mean"].to_numpy(), table["i_mean"].to_numpy()))
            self.assertTrue(np.allclose(read_table["spectral_entropy_bits"].to_numpy(), table["spectral_entropy_bits"].to_numpy()))

    def test_invalid_burst_shape_error_handling(self):
        with self.assertRaises(ValueError):
            extract_burst_features_scalar(np.zeros((256, 3)))
        with self.assertRaises(ValueError):
            extract_burst_features_batch(np.zeros((10, 256, 4)))


if __name__ == "__main__":
    unittest.main()
