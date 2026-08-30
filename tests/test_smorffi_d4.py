import numpy as np
import pytest

from src.smorffi_d2 import deterministic_split
from src.smorffi_d4 import iq_to_tensor, D4Config


def test_d4_input_shape_and_channel_order():
    iq = [(float(i), float(-i)) for i in range(288)]
    x = iq_to_tensor(iq)
    assert x.shape == (2, 288)
    assert x.dtype == np.float32
    assert x[0, 10] == 10.0
    assert x[1, 10] == -10.0


def test_split_is_deterministic_and_partitioned():
    values = [deterministic_split("17", i) for i in range(100)]
    assert values == [deterministic_split("17", i) for i in range(100)]
    assert set(values) <= {"train", "validation", "test"}


def test_d4_config_is_fixed_baseline():
    c = D4Config()
    assert (c.channels, c.samples, c.embedding_dim) == (2, 288, 32)
    assert c.seed == 20260830


def test_model_shape_if_torch_available():
    torch = pytest.importorskip("torch")
    from src.smorffi_d4 import build_model
    model = build_model(3, 32)
    z, logits = model(torch.zeros(4, 2, 288))
    assert tuple(z.shape) == (4, 32)
    assert tuple(logits.shape) == (4, 3)
