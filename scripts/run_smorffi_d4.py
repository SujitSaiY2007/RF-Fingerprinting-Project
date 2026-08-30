"""Track-A D4 baseline runner.

The runner consumes local SMoRFFI CSVs, applies the frozen D2 representation and
hash split, trains the fixed D4 CNN, and writes embeddings/metrics. It never
uses MAC/device identifiers as signal features.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from src.smorffi_d2 import parse_canonical_preamble, deterministic_split
from src.smorffi_d4 import D4Config, build_model, set_seed, iq_to_tensor


def load_rows(root: Path):
    X, y, split = [], [], []
    for path in sorted(root.rglob("*.csv")):
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row_index, row in enumerate(reader):
                p = parse_canonical_preamble(row["preamble"])
                X.append(iq_to_tensor(p.iq))
                y.append(str(row["Device Number"]))
                split.append(deterministic_split(str(row["Device Number"]), row_index))
    if not X:
        raise ValueError("no SMoRFFI CSV observations found")
    return np.stack(X), np.asarray(y), np.asarray(split)


def train(root: Path, output: Path, config: D4Config):
    import torch
    from torch import nn
    from torch.utils.data import DataLoader, TensorDataset

    set_seed(config.seed)
    X, y_text, split = load_rows(root)
    labels = sorted(np.unique(y_text))
    label_to_int = {label: i for i, label in enumerate(labels)}
    y = np.asarray([label_to_int[v] for v in y_text], dtype=np.int64)
    train_mask, val_mask, test_mask = split == "train", split == "validation", split == "test"
    model = build_model(len(labels), config.embedding_dim)
    opt = torch.optim.Adam(model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay)
    loss_fn = nn.CrossEntropyLoss()
    ds = TensorDataset(torch.from_numpy(X[train_mask]), torch.from_numpy(y[train_mask]))
    loader = DataLoader(ds, batch_size=config.batch_size, shuffle=True, generator=torch.Generator().manual_seed(config.seed))
    history = []
    for epoch in range(config.epochs):
        model.train(); total = 0.0
        for xb, yb in loader:
            opt.zero_grad(set_to_none=True)
            _, logits = model(xb)
            loss = loss_fn(logits, yb)
            loss.backward(); opt.step(); total += float(loss)
        model.eval()
        with torch.no_grad():
            _, lv = model(torch.from_numpy(X[val_mask]))
            val_acc = float((lv.argmax(1).numpy() == y[val_mask]).mean())
        history.append({"epoch": epoch + 1, "train_loss": total / max(1, len(loader)), "validation_accuracy": val_acc})
    model.eval()
    with torch.no_grad():
        zt, lt = model(torch.from_numpy(X[test_mask]))
    test_pred = lt.argmax(1).numpy()
    test_acc = float((test_pred == y[test_mask]).mean())
    output.mkdir(parents=True, exist_ok=True)
    torch.save({"state_dict": model.state_dict(), "labels": labels, "config": config.__dict__}, output / "d4_model.pt")
    np.savez_compressed(output / "d4_test_embeddings.npz", embedding=zt.numpy(), y=y[test_mask], labels=np.asarray(labels))
    result = {"status": "reproduced", "dataset": {"rows": int(len(X)), "devices": len(labels)},
              "split_counts": {k: int((split == k).sum()) for k in ("train", "validation", "test")},
              "embedding_dim": config.embedding_dim, "test_accuracy": test_acc, "history": history}
    (output / "d4_result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("data_root", type=Path)
    ap.add_argument("--output", type=Path, default=Path("experiments/track_a/d4"))
    args = ap.parse_args()
    print(json.dumps(train(args.data_root, args.output, D4Config()), indent=2))
