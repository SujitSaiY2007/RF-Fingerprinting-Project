import numpy as np

from src.smorffi_d3 import extract_rf_features


def test_d3_feature_schema_is_deterministic() -> None:
    x = np.exp(1j * np.linspace(0.0, 1.0, 288))
    a = extract_rf_features(x)
    b = extract_rf_features(x)
    assert a == b
    assert len(a) == 15
    assert all(np.isfinite(v) for v in a.values())


def test_d3_rejects_wrong_length() -> None:
    try:
        extract_rf_features(np.ones(287, dtype=np.complex128))
    except ValueError as exc:
        assert "288" in str(exc)
    else:
        raise AssertionError("wrong-length input should be rejected")
