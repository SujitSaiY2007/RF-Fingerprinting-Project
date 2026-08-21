# Oregon State RFFP — Preliminary Qualification

## Identity

This record covers two public Oregon State University NetSTAR datasets because they serve complementary responsibilities:

1. **WiFi RFFP** — 50 Pycom devices (25 LoPy + 25 FiPy), IEEE 802.11b, 2.412 GHz, 25 MS/s, five consecutive days, indoor/outdoor.
2. **LoRa RFFP** — 25 identical Pycom devices, 915 MHz, SF7, 125 kHz BW, CR 4/5, 1 MS/s, seven environmental/configuration scenarios.

Decision for both: **KEEP**.

## WiFi evidence

The official Oregon State release note reports 50 Pycom transmitters, 25 LoPy and 25 FiPy, with an Ettus USRP B210 receiver. Signals were captured at 2.412 GHz and 25 MS/s over five consecutive days in indoor and outdoor environments. Five transmissions per device were captured each day in round-robin order, with approximately five minutes between consecutive captures of the same device. Each capture contains 50 million complex-valued I/Q samples.

The public dataset index provides the WiFi dataset and related Stable-WiFi variants. The Stable-WiFi dataset includes wired, wireless and location scenarios.

### WiFi D-stage mapping

- D1/D2: Strong — raw time-domain I/Q and known acquisition parameters.
- D3: Strong — repeated physical devices and raw I/Q; 25 LoPy and 25 FiPy create same-model groups.
- D4/D5: Strong — many observations/device and multi-day structure.
- D6: Strong candidate — 50 identities allow explicit held-out-device protocols.
- D7: Strong — day and indoor/outdoor variation; Stable-WiFi adds wired/wireless/location configurations.
- D8: Strong candidate — repeated observations across five consecutive days and known temporal ordering, subject to direct metadata validation.
- D9: Suitable legitimate base data; use controlled/synthetic poisoning.
- D10: Strong complementary dataset.

### WiFi limitations

The primary described setup uses a single B210 receiver, so it is not a substitute for WiSig's receiver-variation capability. The 25+25 device composition is not equivalent to 50 identical devices. License/access terms need direct confirmation before final portfolio lock.

## LoRa evidence

The Oregon State dataset is described as containing 25 identical Pycom IoT transmitters and one B210 receiver. It uses 915 MHz LoRa, SF7, 125 kHz bandwidth, coding rate 4/5 and 1 MS/s sampling. Seven scenarios cover indoor/outdoor, different days/configurations, changed device locations and one scenario with a different receiver. The dataset includes time-domain IQ and FFT representations, with SigMF-format binary files and JSON metadata. Public dataset documentation reports approximately 16,300 files and about 1.2 TB.

### LoRa D-stage mapping

- D1/D2: Strong.
- D3: Excellent same-model candidate.
- D4/D5: Strong.
- D6: Strong candidate, subject to identity-holdout protocol.
- D7: Excellent candidate for environmental/location/domain variation.
- D8: Promising because of multi-day/scenario structure; exact sequence semantics must be checked.
- D9: Suitable legitimate base data.
- D10: Strong complementary non-WiFi technology dataset.

### LoRa limitations

The archive is very large. The primary receiver is common across most scenarios, with receiver variation limited to one scenario. Direct inspection of scenario metadata and license/access terms is required before final lock.

## Decision rationale

KEEP both as complementary datasets. The WiFi dataset is especially valuable for temporal/domain adaptation, while the LoRa dataset is unusually valuable for same-model and environmental robustness evaluation outside WiFi.
