# RF Fingerprinting Research Demonstrator UI

## Purpose

This UI is a demonstrator and control surface for the RF fingerprinting engine. It does not contain scientific decision logic.

## Planned surfaces

- Dashboard — Version A/B metrics, system state and recent events.
- Identify — submit/select an observation and display recognition, novelty, consistency and ACCEPT/HOLD/REJECT evidence.
- Profiles — persistent device profiles, versions, statistics and evolution history.
- Security — open-set operating points, update authorization and suspicious events.
- Evaluation — frozen experiment results and policy/model comparisons.
- Audit — chronological provenance, model/profile versions and decision/update records.
- Attack Lab — D9 controlled poisoning/replay demonstrations, clearly labelled synthetic/derived/controlled.

## Architectural rule

```text
UI -> API -> RF engine -> profile manager -> audit store
```

The browser must never mutate profiles directly and must never independently calculate the authoritative security decision.

## Version-A / Version-B presentation

Version A remains the frozen reference. The UI may display Version A and Version B side-by-side, but must preserve the experiment configuration and provenance for every metric.

Version-B headline metrics are blank/marked unavailable until their corresponding frozen experiment is complete. The UI must never substitute preliminary or under-trained results as final results.

## Data truthfulness

Every experiment/result displayed by the UI must identify its data class:

- `REAL_SOURCE_DATA`
- `DERIVED_CONTROLLED_DATA`
- `PAPER_REPRODUCTION_SCENARIO`

Synthetic/derived scenarios must never be presented as measurements from the source dataset or cited paper.

## D8-specific interaction model

For an observation the UI should display:

1. recognized identity / recognition evidence;
2. novelty/open-set evidence;
3. profile consistency;
4. update authorization;
5. final ACCEPT / HOLD / REJECT state;
6. whether the persistent profile changed;
7. resulting profile version;
8. audit event.

This preserves the distinction between recognition and authorization.

## Development order

The UI is developed in parallel with D8, but implementation follows stable backend contracts. Start with a functional shell and read-only mock/API adapters, then connect real D8 records once their schemas stabilize. Avoid building a large visual layer before the research engine contracts are stable.
