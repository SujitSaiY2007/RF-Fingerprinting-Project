"""D2 deterministic SMoRFFI signal representation and split helpers.

D2.2 observation is based on the inspected IQ-only SMoRFFI CSVs:
- the `preamble` field is a whitespace-separated serialized complex sequence;
- every inspected observation contains at least 288 complex samples;
- the published SMoRFFI definition specifies a 288-sample canonical preamble;
- extra samples in the stored field are preserved as raw provenance but are not
  fed to the baseline representation.

The baseline does not apply amplitude normalization because amplitude may carry
RF fingerprint information. Normalization remains an explicit future ablation.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re

CANONICAL_PREAMBLE_SAMPLES = 288
_TOKEN_RE = re.compile(r"[^\s,]+")


@dataclass(frozen=True)
class ParsedPreamble:
    samples: tuple[complex, ...]
    original_length: int
    canonical_length: int
    discarded_tail_samples: int

    @property
    def iq(self) -> tuple[tuple[float, float], ...]:
        """Return canonical samples as (I, Q) pairs without normalization."""
        return tuple(
            (float(x.real), float(x.imag))
            for x in self.samples[: self.canonical_length]
        )


def parse_preamble(text: str) -> tuple[complex, ...]:
    """Parse a serialized SMoRFFI complex-sample sequence."""
    if text is None:
        raise ValueError("preamble is missing")
    body = str(text).strip()
    if body.startswith("[") and body.endswith("]"):
        body = body[1:-1]
    tokens = _TOKEN_RE.findall(body)
    if not tokens:
        raise ValueError("preamble contains no samples")
    try:
        return tuple(complex(token) for token in tokens)
    except ValueError as exc:
        raise ValueError(f"invalid complex sample in preamble: {exc}") from exc


def parse_canonical_preamble(text: str) -> ParsedPreamble:
    """Parse a preamble and select the source-defined 288-sample window."""
    samples = parse_preamble(text)
    if len(samples) < CANONICAL_PREAMBLE_SAMPLES:
        raise ValueError(
            f"preamble has {len(samples)} samples; at least "
            f"{CANONICAL_PREAMBLE_SAMPLES} are required"
        )
    return ParsedPreamble(
        samples=samples,
        original_length=len(samples),
        canonical_length=CANONICAL_PREAMBLE_SAMPLES,
        discarded_tail_samples=len(samples) - CANONICAL_PREAMBLE_SAMPLES,
    )


def deterministic_split(device_id: str, row_index: int) -> str:
    """Assign a source row to train/validation/test deterministically.

    This is an engineering split for the current SMoRFFI Track-A demonstration.
    It is not claimed to be a temporal/session holdout because those boundaries
    are not exposed by the inspected dataset.
    """
    key = f"{device_id}|{row_index}".encode("utf-8")
    u = int.from_bytes(hashlib.sha256(key).digest()[:8], "big") / 2**64
    if u < 0.70:
        return "train"
    if u < 0.85:
        return "validation"
    return "test"
