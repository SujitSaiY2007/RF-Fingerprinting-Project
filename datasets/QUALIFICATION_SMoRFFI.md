# SMoRFFI — Preliminary Qualification

## Identity

- Dataset: SMoRFFI — large-scale same-model 2.4 GHz Wi-Fi RF fingerprinting dataset
- Publication: Computer Networks, 2026, DOI 10.1016/j.comnet.2026.112309
- Intended D-stages: D3, D4, D5, D6; possible D8/D10 after metadata inspection
- Decision: **KEEP**

## Evidence

The 2026 data article reports 123 same-model commercial IEEE 802.11g devices, 35.42 million raw I/Q samples from preambles and 1.85 million corresponding RF features. An accompanying open-source framework provides a reproducible data-collection-to-evaluation pipeline. The paper reports a Random Forest baseline on the dataset.

## Qualification

- D1: Strong — raw I/Q is explicitly reported.
- D2: Strong candidate — preamble I/Q is directly usable, but exact acquisition metadata must be inspected.
- D3: Excellent — 123 same-model devices directly target the difficult same-model fingerprinting problem.
- D4: Excellent candidate — large same-model identity population and raw I/Q.
- D5: Excellent candidate — high identity count and repeated samples.
- D6: Strong candidate — many device identities permit explicit unknown-device holdout.
- D7: Currently unproven — current retrieved evidence does not establish enough receiver/day/environment variation.
- D8: Currently unproven — temporal/sequential metadata must be inspected before using it as the primary continual-learning dataset.
- D9: Suitable legitimate RF base data; poisoning can be injected synthetically.
- D10: Strong same-model component of the final portfolio.

## Important limitation

The dataset's most important strength is also its intended scope: same-model discrimination. It should not be assumed to provide receiver/channel/domain variation merely because it is large. That information must be confirmed from the actual data package and documentation.

## Decision rationale

KEEP because same-model device discrimination is a core requirement that WiSig alone does not guarantee. SMoRFFI should become a primary candidate for D3–D6 once direct data-access and metadata checks are completed.

## License note

The associated publication is reported as open access under a Creative Commons license; direct confirmation of the dataset's own redistribution/use terms is still required before final portfolio lock.
