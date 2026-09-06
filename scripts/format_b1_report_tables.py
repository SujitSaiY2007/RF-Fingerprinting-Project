"""Generate formatted Markdown tables from B1 validation results."""

import json
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding="utf-8")

results_file = Path("experiments/track_b/manysig_b1_validation_results.json")
with open(results_file, "r", encoding="utf-8") as f:
    data = json.load(f)

print("### 1. Feature Sanity and Statistical Summary Table\n")
print("| Feature Name | Data Type | Observations | Mean | Std Dev | Median | IQR | Min | Max | Outliers (>5σ) | Status |")
print("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
for feat, s in data["feature_sanity"].items():
    mean_str = f"{s['mean']:+.4e}"
    std_str = f"{s['std']:.4e}"
    med_str = f"{s['median']:+.4e}"
    iqr_str = f"{s['iqr']:.4e}"
    min_str = f"{s['min']:+.4e}"
    max_str = f"{s['max']:+.4e}"
    outlier_str = f"{s['outlier_z5_count']} ({s['outlier_z5_pct']:.2f}%)"
    status = "NON-DEGENERATE" if not s["is_degenerate"] and not s["is_effectively_constant"] else "FLAGGED"
    print(f"| `{feat}` | `{s['dtype']}` | {s['observations']:,} | `{mean_str}` | `{std_str}` | `{med_str}` | `{iqr_str}` | `{min_str}` | `{max_str}` | {outlier_str} | **{status}** |")

print("\n\n### 2. Factor Variance Decomposition (ANOVA $\\eta^2$)\n")
print("| Feature Name | $\\eta^2(\\text{TX})$ | $\\eta^2(\\text{RX})$ | $\\eta^2(\\text{Date})$ | $\\eta^2(\\text{Equalization})$ | Dominant Variance Source | TX / RX Variance Ratio |")
print("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")
for feat, eff in data["factor_effects"].items():
    eta_tx = eff["eta_squared_tx"]
    eta_rx = eff["eta_squared_rx"]
    eta_date = eff["eta_squared_date"]
    eta_eq = eff["eta_squared_eq"]
    dom = eff["dominant_factor"]
    ratio_str = f"{eff['tx_to_rx_variance_ratio']:.3f}" if eta_rx > 0 else "N/A"
    dom_label = {
        "is_equalized": "**Equalization Preprocessing**",
        "rx_id": "**Receiver Hardware / Channel**",
        "tx_id": "**Transmitter Identity**",
        "capture_date": "**Temporal Session Drift**",
    }.get(dom, dom)
    print(f"| `{feat}` | {eta_tx:6.4f} | {eta_rx:6.4f} | {eta_date:6.4f} | {eta_eq:6.4f} | {dom_label} | {ratio_str} |")

print("\n\n### 3. Confounding & Metric Separation (Normalized Euclidean Distance in $\\mathbb{R}^{16}$)\n")
cm = data["confounding_analysis"]
print("| Evaluation Condition | Mean Distance | Std Dev | Ratio vs Matched Inter-TX | Scientific Confounding Implication |")
print("| :--- | :---: | :---: | :---: | :--- |")
print(f"| **Inter-TX Distance** (Matched RX, Date, Eq) | **{cm['inter_tx_matched_distance_mean']:.3f}** | {cm['inter_tx_matched_distance_std']:.3f} | **1.00x** (Baseline) | Baseline separation between distinct transmitter identities under controlled identical receiver/date/equalization conditions. |")
print(f"| **Intra-TX Distance across Receivers** (Same TX, Date, Eq) | **{cm['intra_tx_cross_rx_distance_mean']:.3f}** | {cm['intra_tx_cross_rx_distance_std']:.3f} | **{cm['ratio_intra_tx_rx_to_inter_tx_matched']:.2f}x** | Receiver switch introduces **equal magnitude drift** as switching transmitter identity ($1.00\\times$). Features without domain adaptation are receiver-locked. |")
print(f"| **Intra-TX Distance across Dates** (Same TX, RX, Eq) | **{cm['intra_tx_cross_date_distance_mean']:.3f}** | {cm['intra_tx_cross_date_distance_std']:.3f} | **{cm['ratio_intra_tx_date_to_inter_tx_matched']:.2f}x** | Temporal session drift creates substantial feature shift ($0.37\\times$ of inter-TX distance), indicating long-term temporal instability. |")
print(f"| **Intra-TX Distance across Equalization** (Same TX, RX, Date) | **{cm['intra_tx_cross_eq_distance_mean']:.3f}** | {cm['intra_tx_cross_eq_distance_std']:.3f} | **{cm['ratio_intra_tx_eq_to_inter_tx_matched']:.2f}x** | Equalization shift is **2.41x larger** than transmitter identity differences! Raw and equalized bursts inhabit distinct manifolds. |")

print("\n\n### 4. Sample-Rate Scaling Sensitivity Table\n")
sra = data["sample_rate_audit"]
print(f"Status: **{sra['status']}** (Nominal: {sra['nominal_sample_rate_hz'] / 1e6:.1f} MHz)\n")
print("| Assumed Sample Rate ($F_s$) | Scale Factor | Spectral Centroid Mean (Hz) | Spectral Spread Mean (Hz) | Status |")
print("| :---: | :---: | :---: | :---: | :---: |")
for k, v in sra["scaling_table"].items():
    print(f"| **{k}** ({v['sample_rate_hz']/1e6:.1f} MHz) | {v['scale_factor_vs_20mhz']:.2f}x | `{v['spectral_centroid_mean_hz']:+.4e}` | `{v['spectral_spread_mean_hz']:+.4e}` | {'Nominal Engineering Default' if v['scale_factor_vs_20mhz'] == 1.0 else 'Hypothetical Rescaled'} |")
