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

The following are not solved by dataset selection and must be addressed experimentally: leakage-safe identity/session/day splits; formal D6 unknown-device construction; formal chronological D8 stream and frozen evaluation population; trusted profile-update policy and rollback; controlled/synthetic poisoning; cross-dataset normalization; later hardware-transfer validation.

## Portfolio lock rule

The portfolio is **locked for development-substrate selection**, not protected from later scientific revision. A dataset may be downgraded or replaced if implementation-level inspection reveals a material contradiction.

No raw RF archive should be committed to Git. Store source URLs, package identifiers, metadata summaries, checksums/manifests and acquisition instructions instead.

## Final Phase-1 dataset conclusion

The project does **not** require another broad dataset hunt before D1. Further dataset searching should be triggered only by an observed experimental gap or reproducibility/licensing failure.

Therefore the next project gate is **D1 implementation and validation**, not additional open-ended dataset discovery.
