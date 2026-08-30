# D10 — Auditable Track-A RF Lifecycle

**Date:** 2026-08-30  
**Track:** A  
**Status:** **IMPLEMENTED / TESTED / DEMONSTRATED; not scientifically validated.**

## Integrated path
`SMoRFFI/raw observation -> D2 representation -> D3 RF evidence + D4 embedding -> D5 identity -> D6 known/unknown -> D8 profile lookup -> update authorization -> D9 poisoning controls -> audit/final decision`

The current demonstrator wires the executable portions available in the repository and records the profile lifecycle independently of classifier retraining.

## Demonstrated lifecycle
1. **Known legitimate observation:** frozen recognition produced identity 1 with confidence 0.88; multi-evidence authorization returned `ACCEPT_UPDATE`.
2. **Legitimate profile evolution:** a later training observation of the same identity produced confidence 1.00 and `ACCEPT_UPDATE`.
3. **Unknown observation:** a real SMoRFFI device-34 observation with confidence 0.23 was rejected by the frozen D6 threshold before profile mutation.
4. **Suspicious replay:** an unknown observation recognized as identity 1 at confidence 0.34 was admitted once by the current feature/confidence policy, then its exact repetition was `HOLD_QUARANTINE` with reason `replay_detected`.
5. **Auditability:** every authorization records source ID, identity, policy, confidence, consistency distance, synthetic flag and profile-version transition; the profile manager exposes a state digest.

## Important limitation
The first suspicious sample can still be admitted when an unknown observation is close enough to the known profile and passes recognition confidence. The replay guard blocks repetition, but it does not solve target-like unknown contamination. Therefore D10 is an auditable lifecycle demonstration, **not a security guarantee**.

## Frozen evaluation protection
The D10 scenario never uses the frozen known-device test partition as an update source. Validation is used only for the consistency threshold. This preserves the D8/D9 leakage boundary.

## Completion level
- Implemented: **PASS**
- Tested: **PASS**
- Demonstrated: **PASS**
- Scientifically Validated: **NO**

## Track-B boundary
Claims about real temporal/session/environment/receiver robustness and real attack traffic remain outside this Track-A demonstration and require independently collected/qualified datasets with trustworthy condition metadata.
