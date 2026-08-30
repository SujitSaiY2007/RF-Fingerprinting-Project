"""D6 open-set rejection helpers using frozen D4 embeddings."""
from __future__ import annotations

import numpy as np


def fit_centroids(z_train, y_train):
    labels = np.unique(y_train)
    return {label: np.asarray(z_train)[np.asarray(y_train) == label].mean(axis=0) for label in labels}


def centroid_distances(z, centroids):
    labels = list(centroids)
    c = np.stack([centroids[k] for k in labels])
    return ((np.asarray(z)[:, None, :] - c[None, :, :]) ** 2).sum(axis=2) ** 0.5


def predict_with_rejection(z, centroids, threshold: float):
    labels = list(centroids)
    d = centroid_distances(z, centroids)
    idx = np.argmin(d, axis=1)
    pred = np.asarray([labels[i] for i in idx], dtype=object)
    pred[d[np.arange(len(pred)), idx] > threshold] = "UNKNOWN"
    return pred


def select_threshold(validation_distances, quantile: float = 0.95) -> float:
    """Select a threshold from validation distances only; test data is forbidden."""
    if not 0 < quantile < 1:
        raise ValueError("quantile must be between 0 and 1")
    return float(np.quantile(np.asarray(validation_distances), quantile))
