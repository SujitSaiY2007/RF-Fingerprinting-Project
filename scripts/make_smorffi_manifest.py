"""Create a reproducibility manifest for a local SMoRFFI CSV snapshot.

Usage:
  python scripts/make_smorffi_manifest.py /path/to/data manifest.json

The repository intentionally does not commit the large raw SMoRFFI release.
This tool records exact file names, byte sizes and SHA-256 hashes plus row/device
counts so a run can be tied to a concrete local snapshot.
"""
from __future__ import annotations

import csv
import hashlib
import json
import pathlib
import sys
from collections import Counter

REQUIRED = {"Device Number", "MAC_address", "preamble"}


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inspect_csv(path: pathlib.Path) -> dict:
    rows = 0
    devices = Counter()
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError(f"{path}: required columns missing")
        for row in reader:
            rows += 1
            devices[str(row["Device Number"])] += 1
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256_file(path),
            "rows": rows, "devices": dict(sorted(devices.items()))}


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: make_smorffi_manifest.py DATA_ROOT OUTPUT_JSON", file=sys.stderr)
        return 2
    root, out = pathlib.Path(argv[1]), pathlib.Path(argv[2])
    files = sorted(root.rglob("*.csv"))
    manifest = {
        "dataset": "SMoRFFI",
        "track": "A",
        "snapshot_status": "locally-generated",
        "input_contract": "complex[288] -> float32[2,288] I/Q",
        "split": "sha256(device_id|source_row_index): 70/15/15",
        "files": [inspect_csv(p) for p in files],
    }
    manifest["file_count"] = len(files)
    manifest["row_count"] = sum(x["rows"] for x in manifest["files"])
    manifest["device_count"] = len({d for x in manifest["files"] for d in x["devices"]})
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: manifest[k] for k in ("file_count", "row_count", "device_count")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
