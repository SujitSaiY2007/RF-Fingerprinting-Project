# Dataset Qualification Portfolio — 2026-08-21

## Status

**Preliminary portfolio — NOT LOCKED**

This record summarizes the first evidence-backed candidate qualification pass. Decisions remain subject to direct metadata/download inspection and, where needed, license/access confirmation.

## Qualification rule

A dataset is selected for a specific experimental responsibility; no dataset is required to satisfy D1–D10 alone. Public availability and a relevant paper are not sufficient by themselves to prove every requirement.

## Candidate portfolio

| Dataset | Preliminary decision | Primary responsibility | Strong evidence | Major limitations / verification required |
|---|---|---|---|---|
| WiSig | KEEP | D4–D7, D5/D6 scalability; D10 supporting dataset | 174 Tx, 41 USRP Rx, 4 captures over a month; raw captures plus processed subsets; multiple days/receivers | Same-model diversity is not established as a core property; full raw archive is very large; exact unknown-device protocol must be constructed by the project |
| Oregon State WiFi RFFP (50 Pycom) | KEEP | D3–D8, especially temporal/domain shift | 50 Pycom devices, 25 LoPy + 25 FiPy, raw I/Q, 5 consecutive days, indoor/outdoor, 25 MS/s, 2.412 GHz | One B210 receiver in the described setup; same-model groups are 25 each, not 50 identical devices; license/access terms require direct confirmation |
| Oregon State LoRa RFFP (25 identical Pycom) | KEEP | D3, D7 and controlled temporal/domain robustness | 25 identical Pycom devices; 915 MHz; 1 MS/s; seven scenarios; indoor/outdoor; different days/configurations; one scenario with a different receiver; SigMF + JSON metadata | Very large (~1.2 TB); license/access terms require direct confirmation; exact scenario-level split design must be inspected before D7/D8 claims |
| SMoRFFI | KEEP | D3–D6 same-model discrimination; potential D8 if temporal metadata supports it | 123 same-model commercial IEEE 802.11g devices; 35.42M raw I/Q samples; 1.85M RF features; reproducible framework | Current evidence retrieved does not yet establish receiver/session/day/environment coverage sufficiently for D7/D8; direct data package inspection is required |
| ORACLE | SECONDARY | D3–D5 controlled hardware-impairment / distance sensitivity; calibration/control study | 16 bit-similar X310 Tx, fixed B210 Rx, raw OTA IQ, 5 MS/s, 2.45 GHz, distances 2–62 ft; SigMF-compatible metadata | Only 16 Tx and one receiver; open-set and cross-receiver claims are weak; controlled setup limits ecological validity |
| Bluetooth smartphone RFF database | SECONDARY | D3/D5 protocol-diverse RF fingerprinting and cross-device technology check | 27 smartphones, six manufacturers, multiple models; public Zenodo dataset; CC-BY reported | Not a central WiFi/LoRa project substrate; metadata/temporal/domain structure must be inspected before using for D7/D8 |

## D-stage coverage assessment

### D1 — Raw RF / ingestion

Strong candidates: WiSig Raw/Full, Oregon WiFi, Oregon LoRa, SMoRFFI, ORACLE Dataset 1. The current portfolio has multiple genuine hardware-capture sources rather than relying on a single archive.

### D2 — Synchronization & DSP

Strong candidates: WiSig Raw, Oregon WiFi, Oregon LoRa, ORACLE. SMoRFFI should be checked for exact raw-sample framing and capture metadata before assigning it as a primary D2 source.

### D3 — Physics-based features

Best candidates: SMoRFFI for same-model scale; ORACLE for controlled transmitter hardware and distance; Oregon LoRa/WiFi for repeated physical devices and raw I/Q. The project must still demonstrate that the proposed physics features are actually observable and device-informative; dataset presence alone does not prove this.

### D4 — Device representation

Best candidates: WiSig, SMoRFFI, Oregon WiFi/LoRa. Session-aware splits are preferred over random sample splits.

### D5 — Closed-set identification

WiSig provides scale; SMoRFFI provides same-model difficulty; Oregon datasets provide repeated device observations under changing conditions.

### D6 — Open-set recognition

WiSig and SMoRFFI are promising because they contain many device identities, but the project must create identity-level holdout protocols. No public dataset is being treated as automatically proving open-set recognition.

### D7 — Robustness / domain shift

WiSig is strong for receiver/day/channel variation. Oregon WiFi and LoRa are strong for day/location/environment variation. ORACLE is useful for distance-controlled variation but not receiver variation.

### D8 — Continual learning / profile evolution

No candidate is yet fully qualified as a standalone D8 dataset. Oregon WiFi/LoRa and WiSig are the leading candidates because they provide repeated observations over time/days. Sequential ordering and timestamp/session semantics still require direct inspection and a defined protocol.

### D9 — Poisoning / adversarial protection

No candidate needs to contain real poisoning attacks. Per DEC-005, use a legitimate base RF dataset plus controlled/synthetic poisoning. WiSig or an Oregon dataset can provide the legitimate base population after the update protocol is defined.

### D10 — End-to-end

A portfolio-level evaluation is required. A defensible candidate configuration is likely to combine a large multi-receiver dataset (WiSig), a same-model dataset (SMoRFFI), and a temporal/domain-shift dataset (Oregon WiFi or LoRa). Final selection remains open.

## Current conclusion

A **multi-dataset portfolio is necessary**. No single candidate currently provides sufficiently strong evidence across same-model discrimination, receiver variation, multi-day/environment variation, scale, open-set construction and continual learning requirements.

The most strategically important candidates are **WiSig + Oregon WiFi + SMoRFFI**, with **Oregon LoRa** providing a valuable second technology/domain and **ORACLE** serving as a controlled secondary benchmark.

This is a portfolio recommendation, not a final lock. Direct metadata and access inspection remains mandatory before the portfolio is frozen.

## Evidence sources

- WiSig official UCLA dataset page and associated dataset repositories.
- WiSig publication / arXiv record.
- Oregon State University NetSTAR dataset page and release note.
- Oregon State public dataset index.
- 2024 LoRa RFFP survey for the Oregon LoRa dataset details.
- ORACLE official GENESYS dataset page.
- SMoRFFI 2026 Computer Networks data article and associated lab/public records.

External evidence was retrieved on 2026-08-21. URLs and citations are retained in the ChatGPT session record; repository records should be extended with direct source URLs where available.
