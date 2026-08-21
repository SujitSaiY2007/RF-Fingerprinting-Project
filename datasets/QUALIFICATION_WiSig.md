# WiSig — Preliminary Qualification

## Identity

- Dataset: WiSig RF Fingerprinting Dataset
- Source: UCLA CORES / WiSig-dataset resources
- Intended D-stages: D4, D5, D6, D7, supporting D1/D2/D10
- Decision: **KEEP**

## Evidence

The official UCLA dataset page reports 10 million packets from 174 off-the-shelf WiFi transmitters and 41 USRP receivers across four captures spanning one month. It provides raw captures, processed identification signals and compact subsets. The compact subsets include ManyTx (150 Tx, 18 Rx, 4 days), ManyRx (10 Tx, 32 Rx, 4 days), ManySig (6 Tx, 12 Rx, 4 days) and SingleDay (28 Tx, 10 Rx, 1 day).

The raw archive is approximately 1.4 TB; Full WiSig is approximately 70+ GB. Processing scripts and capture-replication code are public.

## Qualification

- D1: Strong — genuine RF captures and transmitter/receiver structure.
- D2: Strong — raw IQ and packet-processing pipeline are available.
- D3: Strong for RF-feature research, but same-model suitability is not established as a defining property.
- D4: Strong — many transmitters and repeated observations; session/day-aware splitting is feasible.
- D5: Strong — large identity count and repeated observations.
- D6: Strong candidate — many identities permit explicit identity-level holdouts, but open-set validation must be designed by the project.
- D7: Excellent — multiple receivers and four capture days over a month directly support receiver/day/channel variation studies.
- D8: Promising — repeated captures over multiple days provide temporal observations, but the project's exact sequential-profile protocol still must be defined.
- D9: Suitable as legitimate RF base data; poisoning remains controlled/synthetic under DEC-005.
- D10: Strong supporting dataset, especially for scalability and acquisition robustness.

## Limitations

WiSig is not a purpose-built same-model benchmark, so it should not be the sole basis for subtle same-model fingerprint claims. The large raw archive is operationally expensive. The public compact subsets are easier to reproduce but may not cover every requirement simultaneously.

## Decision rationale

KEEP because WiSig uniquely provides strong receiver and multi-day scale and is explicitly designed for receiver/channel-agnostic RF fingerprinting. It should be paired with a same-model dataset such as SMoRFFI and a domain/temporal dataset such as Oregon State RFFP.
