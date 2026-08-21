# Dataset Portfolio Lock & D1–D10 Gap Analysis — 2026-08-21

## Status

**Initial dataset portfolio QUALIFIED FOR IMPLEMENTATION — with explicit non-dataset gaps.**

This does **not** mean D1–D10 are scientifically validated. It means the available public-data portfolio is sufficiently defensible to begin D1 implementation without an undocumented dataset assumption.

## Portfolio

### KEEP — primary datasets

1. **WiSig** — primary scale, receiver variation and multi-day/channel robustness dataset.
2. **Oregon State WiFi RFFP** — primary temporal/domain-shift dataset.
3. **Oregon State LoRa RFFP** — primary same-model/environment/distance/location robustness dataset and cross-technology RF substrate.
4. **SMoRFFI** — primary same-model large-scale identification dataset.

### SECONDARY — controlled/supporting datasets

5. **ORACLE** — controlled transmitter-hardware/distance benchmark.
6. **Bluetooth smartphone RF database** — optional cross-technology benchmark; not required for the core portfolio.

## Evidence status

### WiSig
- Official UCLA source states 10M packets, 174 WiFi transmitters, 41 USRP receivers and four captures over a month.
- Official documentation provides raw, processed and compact subsets, preprocessing code and Tx/Rx hardware descriptions.
- Compact subsets explicitly expose Tx count, Rx count and multi-day dimensions.
- Dataset license is CC BY-NC-SA 4.0.
- **Qualification:** KEEP.

### Oregon State WiFi RFFP
- Official release note states 50 Pycom devices (25 LoPy + 25 FiPy), raw time-domain I/Q, 2.412 GHz, 25 MS/s, five consecutive days, indoor and outdoor scenarios, and five transmissions per device per day with five-minute gaps between consecutive captures of the same device.
- **Qualification:** KEEP.
- This supports a defensible temporal/domain-shift dataset role. It does not establish receiver variation because the primary release describes one B210 receiver.

### Oregon State LoRa RFFP
- Official release note states 25 identical Pycom devices, USRP B210 receivers, 915 MHz, 1 MS/s, raw I/Q and FFT representations, SigMF-adapted metadata, and seven explicit scenarios: five days indoor, five days outdoor, five days wired, four distances, four configurations, three locations and two receivers.
- Official file index exposes device/day/scenario structure and actual IQ files.
- **Qualification:** KEEP.
- This is the strongest controlled public candidate for same-model plus environment/location/distance/receiver variation.

### SMoRFFI
- 2026 Computer Networks data article states 123 same-model commercial IEEE 802.11g devices, 35.42M raw I/Q samples and 1.85M RF features, with a reproducible collection-to-evaluation framework.
- The article is open access; public records report CC BY 4.0.
- **Qualification:** KEEP for same-model D3–D6.
- D7/D8 are deliberately not assigned as primary responsibilities until package-level metadata confirms receiver/session/day/environment dimensions.

### ORACLE
- Public research records describe 16 USRP X310 transmitters, one USRP B210 receiver, 2.45 GHz 802.11a, raw OTA data, and controlled receiver distances. Derived runs contain eight usable distance domains after insufficient-frame domains were removed.
- **Qualification:** SECONDARY.

### Bluetooth smartphone RF database
- Oregon State's current dataset page confirms Bluetooth RF fingerprint datasets covering different locations/channels/receivers and wired/wireless scenarios; the candidate Zenodo record requires package-level verification before core use.
- **Qualification:** SECONDARY and non-blocking.

## D1–D10 coverage decision

| Stage | Portfolio support | Status before implementation | Remaining experimental work |
|---|---|---|---|
| D1 Raw RF/Ingestion | WiSig, Oregon WiFi, Oregon LoRa, SMoRFFI, ORACLE | **Covered** | Implement common ingestion and provenance checks |
| D2 Sync/DSP | WiSig Raw, Oregon WiFi, Oregon LoRa, ORACLE | **Covered** | Define synchronization/packet extraction protocol and test it |
| D3 Physics RF Features | SMoRFFI, Oregon LoRa/WiFi, ORACLE | **Covered** | Demonstrate candidate feature observability/device informativeness |
| D4 Device Representation | WiSig, SMoRFFI, Oregon datasets | **Covered** | Build representations and leakage-safe evaluation |
| D5 Closed-Set Identification | WiSig, SMoRFFI, Oregon datasets | **Covered** | Define training/test protocol and metrics |
| D6 Open-Set Recognition | WiSig/SMoRFFI/Oregon identity populations | **Covered by constructible protocol** | Explicit unseen-identity holdout, thresholds and metrics must be implemented |
| D7 Robustness/Domain Shift | WiSig + Oregon WiFi/LoRa + ORACLE | **Covered** | Define domain-specific holdouts and quantify degradation/recovery |
| D8 Continual Profile Evolution | Oregon WiFi/LoRa + WiSig repeated observations | **Data support adequate; protocol not validated** | Define chronological update stream, frozen evaluation set, update acceptance and rollback rules |
| D9 Poisoning Protection | Any legitimate primary dataset + controlled/synthetic poisoning | **Covered by project decision** | Implement controlled attack generation and secure update protocol |
| D10 End-to-End | Portfolio combination | **Covered** | Integrate D1–D9 and execute final validation |

## Remaining data gaps

No data gap currently blocks the beginning of D1 implementation.

The following are **not solved by dataset selection** and must be addressed experimentally:

1. Leakage-safe identity/session/day splits.
2. A formal D6 unknown-device construction.
3. A formal chronological D8 stream and frozen evaluation population.
4. A trusted profile-update policy and rollback mechanism for D8/D9.
5. Controlled/synthetic poisoning generation under DEC-005.
6. Cross-dataset normalization and representation compatibility.
7. Hardware-transfer validation after software/data validation.

## Portfolio lock rule

The portfolio is considered **locked for the purpose of selecting development substrates**, not locked against later scientific reconsideration. A dataset may be downgraded or replaced if implementation-level inspection reveals a material contradiction.

No raw RF archive should be committed to Git. Store source URLs, package identifiers, metadata summaries, checksums/manifests and acquisition instructions instead.

## Final Phase-1 dataset conclusion

The project does **not** require another broad dataset hunt before D1. The current portfolio covers the principal data dimensions needed by D1–D10 with complementary responsibilities. Further dataset searching should be triggered only by an observed experimental gap or a reproducibility/licensing failure.

Therefore the next project gate is **D1 implementation and validation**, not additional open-ended dataset discovery.
