from pathlib import Path

from src.smorffi_d2 import (
    CANONICAL_PREAMBLE_SAMPLES,
    deterministic_split,
    parse_canonical_preamble,
)


def test_canonical_extraction_preserves_complex_iq() -> None:
    text = "[" + " ".join(
        ["1+2j", "3-4j"] + ["0+0j"] * (CANONICAL_PREAMBLE_SAMPLES - 2)
    ) + "]"
    parsed = parse_canonical_preamble(text)
    assert parsed.original_length == CANONICAL_PREAMBLE_SAMPLES
    assert parsed.discarded_tail_samples == 0
    assert parsed.iq[0] == (1.0, 2.0)
    assert parsed.iq[1] == (3.0, -4.0)


def test_extra_samples_are_recorded() -> None:
    text = "[" + " ".join(
        ["1+0j"] * (CANONICAL_PREAMBLE_SAMPLES + 5)
    ) + "]"
    parsed = parse_canonical_preamble(text)
    assert parsed.original_length == CANONICAL_PREAMBLE_SAMPLES + 5
    assert parsed.discarded_tail_samples == 5
    assert len(parsed.iq) == CANONICAL_PREAMBLE_SAMPLES


def test_short_preamble_is_rejected() -> None:
    try:
        parse_canonical_preamble("[1+0j 2+0j]")
    except ValueError as exc:
        assert "at least 288" in str(exc)
    else:
        raise AssertionError("short preamble should be rejected")


def test_split_is_deterministic() -> None:
    split = deterministic_split("101", 1)
    assert split == deterministic_split("101", 1)
    assert split in {"train", "validation", "test"}
