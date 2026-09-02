"""Controlled memory POC for ManySig-style nested pickle ingestion.

This is NOT the final ManySig extractor. It intentionally uses a synthetic
pickle with the same approximate leaf-array size as the inspected ManySig
schema to test an important engineering claim: whether standard
pickle.load()/Unpickler can keep memory bounded by processing one leaf at a
time.

The test is deliberately conservative: it measures process RSS in a child
process and compares a plain pickle file with the same pickle streamed from a
ZIP member. It does not touch or require the real ManySig archive.
"""

from __future__ import annotations

import gc
import json
import os
import pickle
import subprocess
import sys
import tempfile
import zipfile

import numpy as np
import psutil

LEAVES = 24
LEAF_SHAPE = (1000, 256, 2)
SEED = 20260902


def build_synthetic_pickle(path: str) -> None:
    rng = np.random.default_rng(SEED)
    obj = {
        "meta": {
            "tx_list": ["tx0"],
            "rx_list": ["rx0"],
            "capture_date_list": ["date0"],
            "equalized_list": [0, 1],
        },
        "data": [
            rng.standard_normal(LEAF_SHAPE).astype(np.float64)
            for _ in range(LEAVES)
        ],
    }
    with open(path, "wb") as handle:
        pickle.dump(obj, handle, protocol=3)


def measure_child(path: str, mode: str) -> dict[str, float | int | str]:
    process = psutil.Process(os.getpid())
    peak_rss = process.memory_info().rss

    def sample() -> None:
        nonlocal peak_rss
        peak_rss = max(peak_rss, process.memory_info().rss)

    if mode == "plain":
        with open(path, "rb") as handle:
            obj = pickle.load(handle)
        sample()
    elif mode == "zip":
        with zipfile.ZipFile(path, "r") as archive:
            with archive.open("ManySig.pkl", "r") as handle:
                obj = pickle.load(handle)
        sample()
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    # Touch all leaves so their allocated storage is reflected in RSS.
    total_bytes = sum(array.nbytes for array in obj["data"])
    sample()

    del obj
    gc.collect()
    sample()

    return {
        "mode": mode,
        "leaves": LEAVES,
        "leaf_bytes": int(np.prod(LEAF_SHAPE) * 8),
        "leaf_mib": float(np.prod(LEAF_SHAPE) * 8 / 2**20),
        "payload_mib": float(total_bytes / 2**20),
        "peak_rss_mib": float(peak_rss / 2**20),
    }


def main() -> None:
    if len(sys.argv) == 4 and sys.argv[1] == "--child":
        result = measure_child(sys.argv[2], sys.argv[3])
        print(json.dumps(result, sort_keys=True))
        return

    with tempfile.TemporaryDirectory(prefix="manysig_streaming_poc_") as directory:
        pickle_path = os.path.join(directory, "synthetic.pkl")
        zip_path = os.path.join(directory, "synthetic.zip")
        build_synthetic_pickle(pickle_path)
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(pickle_path, arcname="ManySig.pkl")

        for mode, path in (("plain", pickle_path), ("zip", zip_path)):
            output = subprocess.check_output(
                [sys.executable, __file__, "--child", path, mode],
                text=True,
            )
            print(output.strip())


if __name__ == "__main__":
    main()
