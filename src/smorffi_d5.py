"""D5 identity evaluation on frozen D4 embeddings."""
from __future__ import annotations

import numpy as np


def nearest_centroid_fit(z: np.ndarray, y: np.ndarray):
    z = np.asarray(z, dtype=np.float64)
    y = np.asarray(y)
    labels = np.unique(y)
    centroids = {label: z[y == label].mean(axis=0) for label in labels}
    return centroids


def nearest_centroid_predict(z: np.ndarray, centroids: dict):
    z = np.asarray(z, dtype=np.float64)
    labels = list(centroids)
    c = np.stack([centroids[k] for k in labels])
    d2 = ((z[:, None, :] - c[None, :, :]) ** 2).sum(axis=2)
    return np.asarray([labels[i] for i in np.argmin(d2, axis=1)])


def nearest_neighbour_predict(train_z: np.ndarray, train_y: np.ndarray, test_z: np.ndarray):
    a = np.asarray(train_z, dtype=np.float64)
    b = np.asarray(test_z, dtype=np.float64)
    d2 = ((b[:, None, :] - a[None, :, :]) ** 2).sum(axis=2)
    return np.asarray(train_y)[np.argmin(d2, axis=1)]


def classification_metrics(y_true, y_pred) -> dict:
    from sklearn.metrics import (
        accuracy_score, balanced_accuracy_score, confusion_matrix,
        f1_score, precision_recall_fscore_support,
    )
    labels = np.unique(np.concatenate([np.asarray(y_true), np.asarray(y_pred)]))
    p, r, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, zero_division=0
    )
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "labels": [str(x) for x in labels],
        "per_device": {
            str(label): {"precision": float(pp), "recall": float(rr), "f1": float(ff), "support": int(ss)}
            for label, pp, rr, ff, ss in zip(labels, p, r, f1, support)
        },
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=labels).tolist(),
    }
