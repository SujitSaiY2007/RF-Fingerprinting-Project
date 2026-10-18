from pathlib import Path
import os
import pickle
import unittest
import zipfile
import numpy as np

from src.manysig_streamer import (
    TOTAL_LEAVES,
    BURSTS_PER_LEAF,
    SAMPLES_PER_BURST,
    CHANNELS_PER_SAMPLE,
    coordinate_from_index,
    extract_single_leaf,
    stream_all_leaves,
)


class TestManySigStreamer(unittest.TestCase):
    def test_coordinate_from_index_bounds(self):
        tx_list = ["tx0", "tx1", "tx2", "tx3", "tx4", "tx5"]
        rx_list = [f"rx{i}" for i in range(12)]
        date_list = ["d0", "d1", "d2", "d3"]
        eq_list = [0, 1]

        c0 = coordinate_from_index(0, tx_list, rx_list, date_list, eq_list)
        self.assertEqual(c0.leaf_index, 0)
        self.assertEqual(c0.tx_index, 0)
        self.assertEqual(c0.tx_id, "tx0")
        self.assertEqual(c0.rx_index, 0)
        self.assertEqual(c0.rx_id, "rx0")
        self.assertEqual(c0.date_index, 0)
        self.assertEqual(c0.date, "d0")
        self.assertEqual(c0.equalized_index, 0)
        self.assertFalse(c0.is_equalized)

        c_last = coordinate_from_index(TOTAL_LEAVES - 1, tx_list, rx_list, date_list, eq_list)
        self.assertEqual(c_last.leaf_index, 575)
        self.assertEqual(c_last.tx_index, 5)
        self.assertEqual(c_last.tx_id, "tx5")
        self.assertEqual(c_last.rx_index, 11)
        self.assertEqual(c_last.rx_id, "rx11")
        self.assertEqual(c_last.date_index, 3)
        self.assertEqual(c_last.date, "d3")
        self.assertEqual(c_last.equalized_index, 1)
        self.assertTrue(c_last.is_equalized)

    def test_synthetic_manysig_unpickler(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            arr_target = np.ones((BURSTS_PER_LEAF, SAMPLES_PER_BURST, CHANNELS_PER_SAMPLE), dtype=np.float64) * 42.0
            arr_other = np.zeros((BURSTS_PER_LEAF, SAMPLES_PER_BURST, CHANNELS_PER_SAMPLE), dtype=np.float64)

            synthetic_dict = {
                "tx_list": ["14-10", "14-7"],
                "rx_list": ["1-1"],
                "capture_date_list": ["2021_03_01"],
                "equalized_list": [0],
                "max_sig": 1000,
                "data": [
                    [[[arr_target]]],
                    [[[arr_other]]],
                ],
            }

            zip_file = tmp_path / "synthetic_ManySig.zip"
            with zipfile.ZipFile(zip_file, "w") as z:
                z.writestr("ManySig.pkl", pickle.dumps(synthetic_dict, protocol=3))

            coord0, leaf0, meta0 = extract_single_leaf(zip_file, 0)
            self.assertEqual(coord0.leaf_index, 0)
            self.assertEqual(coord0.tx_id, "14-10")
            self.assertEqual(leaf0.shape, (1000, 256, 2))
            self.assertEqual(leaf0.dtype, np.float64)
            self.assertTrue(np.all(leaf0 == 42.0))

            coord1, leaf1, meta1 = extract_single_leaf(zip_file, 1)
            self.assertEqual(coord1.leaf_index, 1)
            self.assertEqual(coord1.tx_id, "14-7")
            self.assertEqual(leaf1.shape, (1000, 256, 2))
            self.assertTrue(np.all(leaf1 == 0.0))

    def test_real_manysig_leaf_0_if_available(self):
        real_zip = Path(r"C:\Users\sujit\Downloads\ManySig.pkl.zip")
        if not real_zip.exists():
            return

        coord, leaf, meta = extract_single_leaf(real_zip, 0)
        self.assertEqual(coord.leaf_index, 0)
        self.assertEqual(coord.tx_id, "14-10")
        self.assertEqual(coord.rx_id, "1-1")
        self.assertEqual(coord.date, "2021_03_01")
        self.assertFalse(coord.is_equalized)
        self.assertEqual(leaf.shape, (1000, 256, 2))
        self.assertEqual(leaf.dtype, np.float64)
        self.assertEqual(len(leaf), 1000)
        self.assertEqual(leaf.nbytes, 4_096_000)


if __name__ == "__main__":
    unittest.main()
