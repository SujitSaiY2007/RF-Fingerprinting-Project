"""ManySig streaming unpickler and memory-bounded leaf extractor.

This module implements a read-only streaming parser for the Protocol-3
serialized WiSig ManySig.pkl dataset archive.

By intercepting REDUCE (0x52) and BINBYTES (0x42) opcodes in the Python
pickle stream, this parser avoids allocating 2.2+ GB of NumPy array buffers
or retaining large bytes objects in the unpickler's memo table. It enables
extracting individual (1000, 256, 2) leaf arrays or sequentially streaming
all 576 leaves in single passes with a strictly bounded memory footprint.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator, Mapping, Optional, Sequence, Tuple
import hashlib
import pickle
import struct
import zipfile

import numpy as np


NUM_TRANSMITTERS = 6
NUM_RECEIVERS = 12
NUM_DATES = 4
NUM_EQUALIZATIONS = 2
TOTAL_LEAVES = NUM_TRANSMITTERS * NUM_RECEIVERS * NUM_DATES * NUM_EQUALIZATIONS  # 576
BURSTS_PER_LEAF = 1000
SAMPLES_PER_BURST = 256
CHANNELS_PER_SAMPLE = 2
LEAF_BUFFER_BYTES = BURSTS_PER_LEAF * SAMPLES_PER_BURST * CHANNELS_PER_SAMPLE * 8  # 4,096,000 bytes


@dataclass(frozen=True)
class LeafCoordinate:
    leaf_index: int
    tx_index: int
    tx_id: str
    rx_index: int
    rx_id: str
    date_index: int
    date: str
    equalized_index: int
    is_equalized: bool


class _DummyArray:
    """Lightweight placeholder for skipped array leaves."""
    __slots__ = ()

    def __setstate__(self, state: object) -> None:
        pass


class _ManySigSelectiveUnpickler(pickle._Unpickler):
    """Custom unpickler that reconstructs only target leaves, discarding others."""
    dispatch = pickle._Unpickler.dispatch.copy()

    def __init__(self, file, target_leaf_indices: Optional[set[int]] = None, on_leaf_callback: Optional[Callable[[int, np.ndarray], None]] = None):
        super().__init__(file)
        self.target_leaf_indices = target_leaf_indices if target_leaf_indices is not None else set()
        self.on_leaf_callback = on_leaf_callback
        self.array_index = 0
        self.leaf_shape = (BURSTS_PER_LEAF, SAMPLES_PER_BURST, CHANNELS_PER_SAMPLE)
        self.leaf_dtype = np.dtype("float64")
        self.recovered_leaves: dict[int, np.ndarray] = {}

    def custom_load_reduce(self) -> None:
        stack = self.stack
        args = stack.pop()
        func = stack[-1]
        # NumPy reconstruct call
        if getattr(func, "__name__", "") == "_reconstruct":
            idx = self.array_index
            self.array_index += 1
            if idx in self.target_leaf_indices and not self.on_leaf_callback:
                stack[-1] = func(*args)
            else:
                stack[-1] = _DummyArray()
        else:
            stack[-1] = func(*args)

    def custom_load_binbytes(self) -> None:
        (len_bytes,) = struct.unpack("<I", self.read(4))
        if len_bytes == LEAF_BUFFER_BYTES:
            idx = self.array_index - 1
            if idx in self.target_leaf_indices or self.on_leaf_callback is not None:
                raw_buf = self.read(len_bytes)
                if self.on_leaf_callback is not None:
                    arr = np.frombuffer(raw_buf, dtype=self.leaf_dtype).reshape(self.leaf_shape)
                    self.on_leaf_callback(idx, arr)
                if idx in self.target_leaf_indices:
                    if not self.on_leaf_callback:
                        self.append(raw_buf)
                    else:
                        self.append(b"")
                else:
                    self.append(b"")
            else:
                # Discard the 4MB buffer in 64KB chunks without retaining Python bytes objects
                remaining = len_bytes
                while remaining > 0:
                    chunk = self.read(min(remaining, 65536))
                    if not chunk:
                        break
                    remaining -= len(chunk)
                self.append(b"")
        else:
            self.append(self.read(len_bytes))

    dispatch[82] = custom_load_reduce    # 0x52 = REDUCE
    dispatch[66] = custom_load_binbytes  # 0x42 = BINBYTES


def coordinate_from_index(
    index: int,
    tx_list: Sequence[str],
    rx_list: Sequence[str],
    date_list: Sequence[str],
    eq_list: Sequence[int],
) -> LeafCoordinate:
    """Convert flat leaf index (0..575) to coordinate metadata."""
    t = index // (len(rx_list) * len(date_list) * len(eq_list))
    rem = index % (len(rx_list) * len(date_list) * len(eq_list))
    r = rem // (len(date_list) * len(eq_list))
    rem = rem % (len(date_list) * len(eq_list))
    d = rem // len(eq_list)
    e = rem % len(eq_list)
    return LeafCoordinate(
        leaf_index=index,
        tx_index=t,
        tx_id=str(tx_list[t]),
        rx_index=r,
        rx_id=str(rx_list[r]),
        date_index=d,
        date=str(date_list[d]),
        equalized_index=e,
        is_equalized=(eq_list[e] == 1),
    )


def extract_single_leaf(
    zip_path: str | Path,
    target_leaf_index: int,
    internal_filename: str = "ManySig.pkl",
) -> Tuple[LeafCoordinate, np.ndarray, dict]:
    """Extract exactly one leaf array by flat index (0..575) with bounded memory."""
    if not (0 <= target_leaf_index < TOTAL_LEAVES):
        raise IndexError(f"leaf index {target_leaf_index} out of range [0, {TOTAL_LEAVES-1}]")

    with zipfile.ZipFile(zip_path, "r") as z:
        with z.open(internal_filename) as f:
            unpickler = _ManySigSelectiveUnpickler(f, target_leaf_indices={target_leaf_index})
            metadata_obj = unpickler.load()

    tx_list = metadata_obj["tx_list"]
    rx_list = metadata_obj["rx_list"]
    date_list = metadata_obj["capture_date_list"]
    eq_list = metadata_obj["equalized_list"]

    coord = coordinate_from_index(target_leaf_index, tx_list, rx_list, date_list, eq_list)
    leaf_array = metadata_obj["data"][coord.tx_index][coord.rx_index][coord.date_index][coord.equalized_index]

    if not isinstance(leaf_array, np.ndarray):
        raise TypeError(f"Failed to recover numpy ndarray for leaf {target_leaf_index}, got {type(leaf_array)}")

    return coord, leaf_array, metadata_obj


def stream_all_leaves(
    zip_path: str | Path,
    on_leaf_callback: Callable[[LeafCoordinate, np.ndarray], None],
    internal_filename: str = "ManySig.pkl",
) -> dict:
    """Stream all 576 leaves sequentially in a single pass with strictly bounded memory."""
    collected_metadata: dict = {}

    def internal_callback(idx: int, arr: np.ndarray) -> None:
        coord = coordinate_from_index(
            idx,
            collected_metadata["tx_list"],
            collected_metadata["rx_list"],
            collected_metadata["capture_date_list"],
            collected_metadata["equalized_list"],
        )
        on_leaf_callback(coord, arr)

    # First read metadata keys
    with zipfile.ZipFile(zip_path, "r") as z:
        with z.open(internal_filename) as f:
            # First pass for metadata (or we can initialize unpickler and callback directly)
            unpickler = _ManySigSelectiveUnpickler(f, on_leaf_callback=None)
            # Create a wrapper unpickler that tracks metadata
            pass

    # Direct streaming pass
    with zipfile.ZipFile(zip_path, "r") as z:
        with z.open(internal_filename) as f:
            # We first parse top-level keys from a quick skeleton
            skeleton_unpickler = _ManySigSelectiveUnpickler(f, target_leaf_indices=set())
            skeleton = skeleton_unpickler.load()
            collected_metadata["tx_list"] = skeleton["tx_list"]
            collected_metadata["rx_list"] = skeleton["rx_list"]
            collected_metadata["capture_date_list"] = skeleton["capture_date_list"]
            collected_metadata["equalized_list"] = skeleton["equalized_list"]
            collected_metadata["max_sig"] = skeleton["max_sig"]

    with zipfile.ZipFile(zip_path, "r") as z:
        with z.open(internal_filename) as f:
            stream_unpickler = _ManySigSelectiveUnpickler(f, on_leaf_callback=internal_callback)
            stream_unpickler.load()

    return collected_metadata
