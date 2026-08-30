import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.smorffi_d3 import extract_rf_features

def test_d3_rf_feature_contract():
    x = np.ones(288, dtype=np.complex128) + 1j*np.arange(288)
    features = extract_rf_features(x)
    assert len(features) == 16
    assert all(np.isfinite(v) for v in features.values())

def test_d3_feature_order_is_stable():
    x = np.exp(1j*np.linspace(0, 1, 288))
    a = list(extract_rf_features(x).keys())
    b = list(extract_rf_features(x).keys())
    assert a == b
