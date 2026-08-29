# ORACLE — Dataset Qualification

## Track-A decision
**TRACK A — working development substrate; secondary controlled benchmark for Track-B validation**

## Responsibility
Primary fast-path substrate for D1–D10 implementation and demonstration. Particularly useful for D2/D3/D5/D7 and controlled distance/hardware-variation studies.

## Evidence summary
The GENESYS release provides raw over-the-air IQ from 16 bit-similar USRP X310 transmitters with a fixed USRP B210 receiver. The recordings use IEEE 802.11a at 5 MS/s centered at 2.45 GHz, cover transmitter-receiver distances from 2 ft to 62 ft, and are distributed as paired `.sigmf-data` / `.sigmf-meta` files. The publisher states that the released binary samples are stored as 64-bit floating point and should be parsed as `complex128`, despite metadata that may declare `cf32`. The release is SigMF-compatible and provides source documentation and provenance. 

## Track-A strengths
- Real raw OTA IQ rather than simulated data.
- 16 bit-similar transmitters provide a genuine RF fingerprinting identity task.
- Explicit transmitter serial identifiers in the documented naming/metadata convention.
- Controlled distance variation provides an immediate domain-shift axis for the fast implementation.
- Paired metadata/data files make D1 provenance and deterministic ingestion practical.
- Public source documentation provides enough information to implement a reproducible parser without requiring user-side dataset re-upload for the development path.

## Limitations
- One primary B210 receiver and controlled collection environment limit ecological diversity.
- Only 16 transmitters; this is not the project's final scale/generalization dataset.
- Track-A results must not be presented as complete cross-dataset scientific validation.
- The raw archive still needs to be locally accessible to the execution environment before real binary loadability can be claimed.

## Qualification boundary
The decision changes the execution role, not the scientific standard. ORACLE is the first Track-A working substrate because it minimizes acquisition friction and supports the planned vertical implementation. ManySig and the broader qualified portfolio remain preserved for stronger validation when justified.
