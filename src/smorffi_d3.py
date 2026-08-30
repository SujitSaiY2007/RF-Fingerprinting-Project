"""D3 interpretable RF-evidence features for the SMoRFFI Track-A baseline.

Input: canonical 288-sample complex preamble from src.smorffi_d2.
Output: deterministic, label-free scalar RF evidence features.

These are evidence descriptors, not claims that any single feature is a unique
transmitter fingerprint. Receiver/channel effects can contribute to them.
"""

from __future__ import annotations

import numpy as np

SAMPLE_RATE_HZ = 20_000_000.0


def extract_rf_features(samples: np.ndarray, sample_rate_hz: float = SAMPLE_RATE_HZ) -> dict[str, float]:
    x = np.asarray(samples, dtype=np.complex128)
    if x.ndim != 1 or len(x) != 288:
        raise ValueError("expected exactly 288 complex samples")
    if sample_rate_hz <= 0:
        raise ValueError("sample rate must be positive")

    i = x.real
    q = x.imag
    amp = np.abs(x)
    power = amp ** 2

    # Local phase-change descriptors. These are intentionally NOT named CFO:
    # a 288-sample Wi-Fi preamble contains signal structure, so phase slope is
    # not a calibrated carrier-frequency-offset estimate by itself.
    phase_step = np.angle(x[1:] * np.conj(x[:-1]))

    # Complex FFT descriptors. Frequency values are relative to the sampled
    # complex-baseband representation and are not asserted to be absolute RF.
    spectrum = np.fft.fftshift(np.fft.fft(x))
    psd = np.abs(spectrum) ** 2
    psd_sum = float(psd.sum())
    if psd_sum <= 0:
        psd_norm = np.full_like(psd, 1.0 / len(psd))
    else:
        psd_norm = psd / psd_sum
    freqs = np.fft.fftshift(np.fft.fftfreq(len(x), d=1.0 / sample_rate_hz))
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
