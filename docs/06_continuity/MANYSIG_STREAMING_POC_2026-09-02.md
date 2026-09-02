# ManySig Streaming Ingestion POC — 02 September 2026

## Purpose

This record documents the first controlled memory experiment performed before any final ManySig extractor is implemented.

The experiment is intentionally **not** a test of the real ManySig archive. The local ManySig archive is not available inside this execution environment, so the test uses a synthetic Protocol-3 pickle containing NumPy leaves with the same verified ManySig leaf shape and dtype: `(1000, 256, 2)` `float64`.

The purpose is to test a necessary engineering assumption: whether ordinary `pickle.load()` can provide leaf-wise bounded-memory processing when the dataset is represented as one top-level nested object.

## Experimental setup

- Python pickle protocol: 3
- Synthetic leaves: 24
- Leaf shape: `(1000, 256, 2)`
- Leaf dtype: `float64`
- Approximate leaf payload: 3.90625 MiB
- Total NumPy leaf payload: 93.75 MiB
- Two access modes:
  1. plain file + `pickle.load()`;
  2. compressed ZIP member + `zipfile.ZipFile.open()` + `pickle.load()`.
- Peak process RSS measured in an isolated child process using `psutil`.
- All leaves were touched after loading so their allocated storage contributed to resident memory.
- The original ManySig archive was not accessed, modified, extracted or copied.

Reproduction script:

`tools/manysig_streaming_poc.py`

## Observed result

The controlled synthetic experiment produced:

| Mode | Leaves | Leaf size | Total leaf payload | Peak RSS |
|---|---:|---:|---:|---:|
| Plain pickle | 24 | 3.90625 MiB | 93.75 MiB | ~184.88 MiB |
| ZIP member + pickle.load | 24 | 3.90625 MiB | 93.75 MiB | ~189.19 MiB |

The result is not a measurement of ManySig peak RAM. It is evidence about the behaviour of the standard Python pickle-loading mechanism on a representative nested NumPy-object structure.

## Interpretation

### Experimentally supported

1. Standard `pickle.load()` does **not** behave as a leaf-wise streaming database reader for a single top-level nested object. It reconstructs the object represented by the pickle before the caller receives the completed return value.
2. Reading the pickle through a ZIP member does not by itself make `pickle.load()` memory-bounded. The compressed archive can be streamed to the unpickler, but the resulting Python object is still materialized.
3. Therefore the previous proposed `<=25–30 MB` peak-RAM claim cannot be justified using ordinary `pickle.load()` on the verified single-object ManySig structure.

### Not established by this POC

1. The actual peak RAM of the real ManySig archive.
2. Whether a custom opcode-aware streaming parser can safely identify and extract one ManySig leaf at a time.
3. Whether such a parser can remain below 25–30 MB on the real archive.
4. Whether the compressed ZIP can be traversed robustly with the required custom parser without full extraction.
5. Whether the complete 576-leaf extraction can be made reliable enough for scientific use.

## Engineering consequence

The final extractor must **not** be implemented on the assumption that `pickle.load()` or a normal `pickle.Unpickler` provides leaf-wise bounded-memory access.

A real-archive proof-of-concept is still required in Antigravity IDE. That test must inspect the actual `ManySig.pkl` stream and experimentally establish the mechanism, peak RSS, correctness of selected-leaf recovery, and whether the ZIP can remain compressed during processing.

If a custom parser is required, it should first be implemented as a narrowly scoped read-only prototype that targets the known Protocol-3/NumPy structure. It must not modify the source archive and must not be promoted to the final extractor until correctness and memory behaviour are demonstrated.

## Scientific status

This POC is **engineering evidence only**.

It does not produce a ManySig scientific result, model result, D-stage completion claim, temporal-adaptation result, poisoning result or novelty claim.

Track-A SMoRFFI evidence remains frozen and unaffected.

## Reproduction

Run:

```bash
python tools/manysig_streaming_poc.py
```

The script creates temporary synthetic files only and removes them when the test exits.
