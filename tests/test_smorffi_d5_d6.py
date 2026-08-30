import numpy as np

from src.smorffi_d5 import nearest_centroid_fit, nearest_centroid_predict, nearest_neighbour_predict
from src.smorffi_d6 import select_threshold, predict_with_rejection


def test_nearest_centroid_identity():
    z = np.array([[0, 0], [0.1, 0], [5, 5], [5.1, 5]])
    y = np.array(["A", "A", "B", "B"])
    c = nearest_centroid_fit(z, y)
    assert list(nearest_centroid_predict(np.array([[0.2, 0], [5.2, 5]]), c)) == ["A", "B"]
    assert list(nearest_neighbour_predict(z, y, np.array([[0.2, 0], [5.2, 5]]))) == ["A", "B"]


def test_open_set_threshold_is_validation_only():
    t = select_threshold(np.array([1.0, 1.0, 2.0, 2.0]), quantile=0.95)
    assert t >= 2.0
    c = {"A": np.array([0.0, 0.0])}
    assert predict_with_rejection(np.array([[0.1, 0], [10, 0]]), c, 1.0).tolist() == ["A", "UNKNOWN"]
