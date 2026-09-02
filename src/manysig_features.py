"""Track-B ManySig 16-feature RF evidence extraction module.

This module implements the frozen 16-feature RF evidence representation
defined in Track-A (src/smorffi_d3.py), adapted for ManySig's (1000, 256, 2)
burst tensors.

Mathematical Invariant:
All 16 physical formulas are preserved identically without filtering,
clipping, artificial resampling, or arbitrary amplitude normalization.
"""

from __future__ import annotations

from typing import Mapping, Sequence, Tuple
import numpy as np
import pyarrow as pa

# The authoritative 16 Track-A RF evidence features
FEATURE_NAMES: Tuple[str, ...] = (
    "i_mean",
    "i_std",
    "q_mean",
    "q_std",
    "amplitude_mean",
    "amplitude_std",
    "rms_amplitude",
    "crest_factor",
    "mean_power",
    "iq_variance_ratio_db",
    "iq_correlation",
    "mean_phase_step_rad",
    "std_phase_step_rad",
    "spectral_centroid_hz",
    "spectral_spread_hz",
    "spectral_entropy_bits",
)

# Engineering default inherited from Track-A; NOT verified from ManySig metadata (REQUIRES VALIDATION)
DEFAULT_SAMPLE_RATE_HZ: float = 20_000_000.0


def extract_burst_features_scalar(
    burst: np.ndarray,
    sample_rate_hz: float = DEFAULT_SAMPLE_RATE_HZ,
) -> dict[str, float]:
    """Calculate 16 RF evidence features for a single (256, 2) or (256,) complex burst.

    This function is the exact scalar reference implementation adhering strictly
    to the Track-A mathematical contract in src/smorffi_d3.py.
    """
    if burst.ndim == 2 and burst.shape[1] == 2:
        x = burst[:, 0].astype(np.float64) + 1j * burst[:, 1].astype(np.float64)
    elif burst.ndim == 1:
        x = np.asarray(burst, dtype=np.complex128)
    else:
        raise ValueError(f"expected burst shape (N, 2) or (N,), got {burst.shape}")

    n_samples = len(x)
    if n_samples < 2:
        raise ValueError("burst must contain at least 2 samples")
    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive")

    i = x.real
    q = x.imag
    amp = np.abs(x)
    power = amp ** 2

    # Phase step descriptors (local phase transitions)
    phase_step = np.angle(x[1:] * np.conj(x[:-1]))

    # Complex FFT spectrum descriptors
    spectrum = np.fft.fftshift(np.fft.fft(x))
    psd = np.abs(spectrum) ** 2
    psd_sum = float(psd.sum())
    if psd_sum <= 0:
        psd_norm = np.full_like(psd, 1.0 / n_samples)
    else:
        psd_norm = psd / psd_sum

    freqs = np.fft.fftshift(np.fft.fftfreq(n_samples, d=1.0 / sample_rate_hz))
    centroid = float(np.sum(freqs * psd_norm))
    spectral_spread = float(np.sqrt(np.sum((freqs - centroid) ** 2 * psd_norm)))
    spectral_entropy = float(-np.sum(psd_norm * np.log2(psd_norm + 1e-15)))

    i_var = float(np.var(i))
    q_var = float(np.var(q))
    iq_var_ratio_db = float(10.0 * np.log10((i_var + 1e-15) / (q_var + 1e-15)))
    iq_corr = float(np.corrcoef(i, q)[0, 1]) if i_var > 0 and q_var > 0 else 0.0

    rms = float(np.sqrt(np.mean(power)))

    return {
        "i_mean": float(np.mean(i)),
        "i_std": float(np.std(i)),
        "q_mean": float(np.mean(q)),
        "q_std": float(np.std(q)),
        "amplitude_mean": float(np.mean(amp)),
        "amplitude_std": float(np.std(amp)),
        "rms_amplitude": rms,
        "crest_factor": float(np.max(amp) / (rms + 1e-15)),
        "mean_power": float(np.mean(power)),
        "iq_variance_ratio_db": iq_var_ratio_db,
        "iq_correlation": iq_corr,
        "mean_phase_step_rad": float(np.mean(phase_step)),
        "std_phase_step_rad": float(np.std(phase_step)),
        "spectral_centroid_hz": centroid,
        "spectral_spread_hz": spectral_spread,
        "spectral_entropy_bits": spectral_entropy,
    }


def extract_burst_features_batch(
    bursts: np.ndarray,
    sample_rate_hz: float = DEFAULT_SAMPLE_RATE_HZ,
) -> dict[str, np.ndarray]:
    """Vectorized calculation of 16 RF features across (B, 256, 2) or (B, 256) bursts.

    Produces mathematically identical results to extract_burst_features_scalar
    to within machine precision while executing in a single vectorized SIMD pass.
    """
    if bursts.ndim == 3 and bursts.shape[2] == 2:
        # bursts: (B, N, 2) -> complex (B, N)
        X = bursts[:, :, 0].astype(np.float64) + 1j * bursts[:, :, 1].astype(np.float64)
    elif bursts.ndim == 2:
        X = np.asarray(bursts, dtype=np.complex128)
    else:
        raise ValueError(f"expected bursts shape (B, N, 2) or (B, N), got {bursts.shape}")

    B, N = X.shape
    if N < 2:
        raise ValueError("burst length N must be at least 2")
    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive")

    i = X.real
    q = X.imag
    amp = np.abs(X)
    power = amp ** 2

    # Phase step: (B, N-1)
    phase_step = np.angle(X[:, 1:] * np.conj(X[:, :-1]))

    # FFT spectrum: (B, N)
    spectrum = np.fft.fftshift(np.fft.fft(X, axis=1), axes=1)
    psd = np.abs(spectrum) ** 2
    psd_sum = np.sum(psd, axis=1, keepdims=True)
    psd_norm = np.where(psd_sum > 0, psd / psd_sum, 1.0 / N)

    freqs = np.fft.fftshift(np.fft.fftfreq(N, d=1.0 / sample_rate_hz))  # (N,)
    centroid = np.sum(psd_norm * freqs, axis=1)                          # (B,)
    spread = np.sqrt(np.sum(psd_norm * ((freqs - centroid[:, None]) ** 2), axis=1))  # (B,)
    entropy = -np.sum(psd_norm * np.log2(psd_norm + 1e-15), axis=1)     # (B,)

    i_mean = np.mean(i, axis=1)
    i_std = np.std(i, axis=1)
    q_mean = np.mean(q, axis=1)
    q_std = np.std(q, axis=1)

    amp_mean = np.mean(amp, axis=1)
    amp_std = np.std(amp, axis=1)
    rms = np.sqrt(np.mean(power, axis=1))
    crest = np.max(amp, axis=1) / (rms + 1e-15)
    mean_pwr = np.mean(power, axis=1)

    i_var = np.var(i, axis=1)
    q_var = np.var(q, axis=1)
    iq_var_ratio_db = 10.0 * np.log10((i_var + 1e-15) / (q_var + 1e-15))

    # Pearson correlation per burst: Cov(i, q) / (std_i * std_q)
    i_centered = i - i_mean[:, None]
    q_centered = q - q_mean[:, None]
    cov_iq = np.mean(i_centered * q_centered, axis=1)
    denom = i_std * q_std
    iq_corr = np.where(denom > 0, cov_iq / denom, 0.0)

    mean_phase_step = np.mean(phase_step, axis=1)
    std_phase_step = np.std(phase_step, axis=1)

    return {
        "i_mean": i_mean,
        "i_std": i_std,
        "q_mean": q_mean,
        "q_std": q_std,
        "amplitude_mean": amp_mean,
        "amplitude_std": amp_std,
        "rms_amplitude": rms,
        "crest_factor": crest,
        "mean_power": mean_pwr,
        "iq_variance_ratio_db": iq_var_ratio_db,
        "iq_correlation": iq_corr,
        "mean_phase_step_rad": mean_phase_step,
        "std_phase_step_rad": std_phase_step,
        "spectral_centroid_hz": centroid,
        "spectral_spread_hz": spread,
        "spectral_entropy_bits": entropy,
    }


def get_feature_arrow_schema() -> pa.Schema:
    """Return the formal Apache Arrow Schema for the ManySig feature table."""
    fields = [
        # Provenance / Coordinate fields
        pa.field("leaf_index", pa.int16(), nullable=False),
        pa.field("burst_index", pa.int16(), nullable=False),
        pa.field("tx_id", pa.string(), nullable=False),
        pa.field("rx_id", pa.string(), nullable=False),
        pa.field("capture_date", pa.string(), nullable=False),
        pa.field("is_equalized", pa.bool_(), nullable=False),
        pa.field("sample_count", pa.int16(), nullable=False),
    ]
    # 16 physical RF evidence features (float64 precision)
    for feat in FEATURE_NAMES:
        fields.append(pa.field(feat, pa.float64(), nullable=False))

    return pa.schema(fields)
