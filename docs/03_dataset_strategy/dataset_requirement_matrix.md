# Dataset Requirement Matrix — Operational Copy

## D1-D10 Master Stages

| ID | Stage | Main Question |
|---|---|---|
| D1 | Raw RF Data / Ingestion | Do we have genuine RF observations with reliable labels? |
| D2 | Synchronization & DSP | Can we reliably preprocess the RF signal? |
| D3 | Physics-Based RF Features | Are device-specific hardware imperfections observable? |
| D4 | Device Representation / Embedding | Can same-device observations form a stable representation? |
| D5 | Closed-Set Identification | Can we identify known devices? |
| D6 | Open-Set Recognition | Can we reject devices that were never enrolled? |
| D7 | Robustness / Domain Shift | Does identification survive environmental/acquisition changes? |
| D8 | Continual Learning / Profile Evolution | Can the profile adapt without losing identity? |
| D9 | Poisoning / Adversarial Protection | Can malicious observations be prevented from corrupting profiles? |
| D10 | End-to-End Validation | Does the complete pipeline work as an integrated system? |

## Core Requirements

### D1
Mandatory: real physical RF captures, raw complex IQ, transmitter/device ID, multiple physical transmitters, sampling rate, center frequency, signal/waveform information, documentation.

Strongly preferred: burst/segmentation information, receiver information, timestamp/session information.

Useful later: distance/environment metadata.

Reject datasets that are only spectrogram images, only extracted features, only embeddings, lack transmitter labels, are simulation-only, or have undocumented capture methodology.

### D2
Require raw IQ, known sampling rate and center frequency, detectable transmissions/bursts, sufficient duration. Waveform/protocol, preamble structure, receiver metadata and SNR information are useful where available.

Test timing alignment, CFO, filtering, normalization, burst detection, signal quality and PSD.

### D3
Require raw IQ, multiple physical devices, multiple observations/device, device labels, consistent acquisition information and sufficient signal quality. Same-model devices and multiple sessions are especially valuable.

Investigate CFO, IQ/amplitude/phase imbalance, EVM, spectral and transient characteristics, and phase/amplitude statistics where justified by the data.

### D4
Require several physical transmitters, many observations/device, suitable raw IQ/features, reliable labels and independent sessions. Same-model devices and multiple capture conditions are especially valuable.

Prefer session/day based train-validation-test separation over random samples from the same session.

### D5
Require multiple devices, labels, multiple observations/device and independent train/test observations. Same-model physical devices are particularly valuable because heterogeneous hardware can create trivial distinctions unrelated to subtle fingerprinting.

### D6
Require multiple genuine transmitters, device-level labels, sufficient observations/device, ability to hold out devices, and genuine unseen transmitters. Raw IQ and multiple sessions are preferred.

Metrics: FAR, FRR, unknown detection rate, AUROC, AUPR, F1 and threshold sensitivity.

### D7
Seek multiple sessions/days, receiver variation, distance variation, environmental variation, SNR/channel variation. Do not claim temperature robustness or hardware aging unless metadata supports it.

### D8
Require sequential observations, identity, multiple observations over time, multiple sessions, raw IQ/features and timestamps. Environmental metadata is useful; temperature and aging are especially valuable but uncommon.

Compare static versus continual models and measure identity accuracy over time, profile drift, adaptation speed, FAR/FRR and forgetting.

### D9
Use a legitimate RF base dataset and controlled/synthetic poisoning rather than forcing a public dataset to represent an attack it was not designed to capture.

Measure poisoning acceptance, profile drift, identity degradation, false acceptance, legitimate update acceptance, recovery time and attack effort.

### D10
Use a final evaluation configuration that is not simply the same data used to tune every component. Ideally include raw IQ, multiple devices, sessions, temporal variation, acquisition metadata and known/unknown-device capability across the portfolio.

## Dataset Quality / Provenance

Every candidate also receives explicit assessment for:

- real hardware
- raw data availability
- ground-truth labels
- capture methodology
- metadata completeness
- documentation
- reproducibility
- license
- download/access availability
- citation/publication support
- community/research usage
- data integrity

## Selection Principle

The project uses a dataset portfolio. One dataset does not need to provide every property. Each selected dataset must have a defined experimental responsibility.
