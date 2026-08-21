# CURRENT OBJECTIVE

## Objective

Dataset Search & Validation / Qualification for Phase 1.

## Status

**COMPLETE AS A DEVELOPMENT-SUBSTRATE SELECTION GATE.**

This does not mean D1–D10 are scientifically validated. It means the current evidence is sufficient to begin D1 without an undocumented dependency on an unqualified dataset.

## Locked development portfolio

### KEEP — primary

- WiSig — scale, receiver variation, multi-day robustness.
- Oregon State WiFi RFFP — temporal/domain variation and repeated Pycom devices.
- Oregon State LoRa RFFP — same-model, environment/location/distance/receiver variation.
- SMoRFFI — large-scale same-model discrimination.

### SECONDARY

- ORACLE — controlled hardware-impairment/distance benchmark.
- Bluetooth smartphone RF database — optional cross-technology benchmark; non-blocking.

## D1–D10 coverage

The portfolio provides a defensible data substrate for all D1–D10 responsibilities, but several responsibilities are **protocol-construction problems rather than dataset-availability problems**:

- D6 requires explicit unseen-identity holdouts, thresholds and open-set metrics.
- D8 requires a formal chronological update stream, frozen evaluation population, profile acceptance and rollback rules.
- D9 requires controlled/synthetic poisoning over legitimate RF data.
- D10 requires the integrated end-to-end experiment.

## Remaining gaps

- Implement leakage-safe session/day/device splitting.
- Verify exact package metadata during D1 ingestion and record checksums.
- Define D6 open-set protocol.
- Define D8 continual profile evolution protocol.
- Define D9 poisoning protocol.
- Establish cross-dataset common RF representation.
- Perform later hardware-transfer validation.

## Next gate

Move to **D1 implementation and validation**, beginning with WiSig and Oregon State WiFi. Reopen dataset search only if implementation reveals a material data, access, license or reproducibility contradiction.
