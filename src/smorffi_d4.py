"""Minimal reproducible Track-A D4 learned embedding.

Input contract is frozen by D2: float32 [N, 2, 288], channels I/Q.
The encoder is deliberately small: two 1-D convolution blocks followed by
an embedding layer and a closed-set classifier head. Device/MAC identifiers
are labels only and never enter the tensor.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable

import numpy as np

EMBEDDING_DIM = 32


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
        torch.use_deterministic_algorithms(True)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass


def iq_to_tensor(iq: Iterable[tuple[float, float]]) -> np.ndarray:
    arr = np.asarray(list(iq), dtype=np.float32)
    if arr.shape != (288, 2):
        raise ValueError(f"expected 288 I/Q pairs, got {arr.shape}")
    return np.ascontiguousarray(arr.T)


@dataclass(frozen=True)
class D4Config:
    seed: int = 20260830
    embedding_dim: int = EMBEDDING_DIM
    channels: int = 2
    samples: int = 288
    epochs: int = 12
    batch_size: int = 128
    learning_rate: float = 1e-3
    weight_decay: float = 1e-4


def build_model(num_classes: int, embedding_dim: int = EMBEDDING_DIM):
    """Return the fixed D4 CNN encoder + classifier head."""
    import torch.nn as nn

    if num_classes < 2:
        raise ValueError("closed-set training requires at least two devices")

    class Encoder(nn.Module):
        def __init__(self):
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv1d(2, 16, kernel_size=7, padding=3),
                nn.ReLU(),
                nn.MaxPool1d(2),
                nn.Conv1d(16, 32, kernel_size=5, padding=2),
                nn.ReLU(),
                nn.AdaptiveAvgPool1d(1),
            )
            self.embedding = nn.Linear(32, embedding_dim)
            self.classifier = nn.Linear(embedding_dim, num_classes)

        def forward(self, x):
            h = self.features(x).squeeze(-1)
            z = self.embedding(h)
            return z, self.classifier(z)

    return Encoder()
