# Oregon State RFFP — Dataset Qualification

## Decision
**KEEP — primary datasets**

This record covers complementary Oregon State WiFi and LoRa RFFP datasets.

## WiFi RFFP
50 Pycom devices (25 LoPy + 25 FiPy), raw time-domain I/Q, 2.412 GHz, 25 MS/s, five consecutive days, indoor/outdoor scenarios and repeated device observations. Primary responsibility: D3–D8, especially temporal/domain shift. The described primary setup uses one B210 receiver, so it does not replace WiSig for receiver variation.

## LoRa RFFP
25 identical Pycom devices, 915 MHz LoRa, 1 MS/s, raw I/Q/FFT representations and explicit scenario variation involving days, environments, locations, configurations, distance and a limited receiver variation. Primary responsibility: D3, D5–D8 and cross-technology robustness.

## Limitations
Exact scenario-level sequencing, package metadata and dataset-specific access/licensing terms must remain verified during D1 ingestion. Large archives should not be committed to Git.

## Scientific boundary
KEEP is a development-substrate decision, not D-stage validation.
