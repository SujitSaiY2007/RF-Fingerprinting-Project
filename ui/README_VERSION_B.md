# Version-B UI — Research Demonstrator

This is the parallel application workstream for Version B. The UI is a presentation/control layer and never owns RF recognition, novelty, authorization, profile mutation, or scientific evaluation logic.

## Screens

- **Dashboard:** Version-A reference vs Version-B results, device/profile counts, security events.
- **Identify:** observation input, identity evidence, novelty evidence, final ACCEPT/HOLD/REJECT.
- **Profiles:** persistent device profiles, profile version, observation count, dispersion and evolution history.
- **Open-Set Security:** known acceptance, unknown rejection, false acceptance and operating curves.
- **Security / Attack Lab:** controlled replay, unknown contamination and poisoning demonstrations; every generated scenario is visibly marked synthetic/derived/controlled.
- **Evaluation:** frozen experiment configuration, metrics, stress curves and provenance.
- **Audit:** chronological observations, decisions, profile updates and rollback/checkpoint events.

## Boundary

`UI -> API -> RF engine/profile manager -> audit`

A classifier confidence score is evidence, not proof of authenticity. The UI must show the engine's decision and evidence rather than independently reimplementing the decision.

## Development order

1. Static navigation and page shell.
2. Versioned API data contracts with mock records explicitly marked `MOCK`.
3. Connect Identify/Profiles/Audit to the D8 backend.
4. Connect Open-Set/Evaluation to frozen experiment artifacts.
5. Connect Attack Lab only to controlled/derived experiments.

## Truthfulness

Every displayed result carries model/version and provenance information where available. Real SMoRFFI measurements, derived controlled data, paper-reproduction scenarios and mock UI records must never be visually conflated.
