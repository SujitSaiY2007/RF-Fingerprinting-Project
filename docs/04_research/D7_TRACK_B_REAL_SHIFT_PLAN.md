# D7 — Track-B Real Distribution-Shift Validation Plan

**Date:** 2026-08-30  
**Status:** **PLANNED / DATA REQUIRED; not yet experimentally demonstrated**

## Question
Can the current RF fingerprinting system distinguish device-specific evidence from acquisition-dependent evidence, and does the resulting representation remain useful under real temporal, receiver and domain shifts?

## Why Track B is required
The supplied SMoRFFI metadata does not expose trustworthy session/day/receiver/environment boundaries. Its Track-A synthetic gain/AWGN stress tests therefore demonstrate sensitivity but cannot establish real-world temporal, receiver or environmental robustness.

The project rule is: do not claim robustness to a factor the dataset does not actually measure.

## Dataset decision
### Required first: Oregon State WiFi RFFP
Use the WiFi RFFP dataset for real temporal/domain shift because it provides repeated observations of 50 Pycom devices over five consecutive days, with indoor and outdoor scenarios. The primary setup uses an Ettus B210 receiver. This makes it suitable for **day/environment shift**, but not sufficient alone for receiver-agnostic claims.

Official source: NetSTAR Laboratory, Oregon State University.

### Required complementary: WiSig / ManySig
Use WiSig for **receiver/day/channel variation**. The official WiSig dataset contains 174 transmitters and 41 USRP receivers across four captures spanning a month, with compact subsets including ManySig. The existing project record keeps the user's ManySig copy as Track B material.

### Not required for the first D7 real-shift experiment
- Oregon State LoRa: useful later for same-model cross-technology/domain evidence, but not necessary to answer the first WiFi temporal/domain question.
- ORACLE: useful for controlled hardware/distance experiments, not the primary D7 need.
- New dataset search: prohibited unless a specific unresolved gap appears.

## D7 experimental hierarchy
### D7.1 — Real day shift (Oregon State WiFi)
Train on earlier day(s), validate without future leakage, test on a later day. Preserve device identities across days where possible. Report closed-set accuracy, macro-F1, balanced accuracy and per-device metrics.

### D7.2 — Real environment shift (Oregon State WiFi)
Train on indoor, test on outdoor, and reverse where sample counts permit. Keep the same device identities. Do not mix captures across the boundary.

### D7.3 — Real receiver shift (WiSig)
Use transmitters observed across multiple receivers. Train on one receiver set and test on disjoint receiver(s), with transmitter overlap required. This is the key test of whether the classifier has learned transmitter evidence versus receiver/channel signatures.

### D7.4 — Day + receiver combined shift (WiSig)
Where metadata supports it, train on earlier capture/day and receiver subset, test on later capture and/or disjoint receiver. This is the strongest D7 Track-B stress test.

## Models to compare
1. Frozen D5 Random Forest using the deterministic D3 RF features.
2. Frozen D4 learned embedding + 1-NN/centroid readout.
3. If needed, a separately trained domain-shift model, clearly labelled as a new experiment.

The original D5 frozen test set must remain untouched as the baseline reference.

## Required analyses
- absolute performance and degradation from matched-domain baseline
- macro-F1 and balanced accuracy
- per-device degradation
- confusion matrices
- confidence/rejection behavior
- feature importance stability where RF is used
- identify features that change strongly with receiver/day/environment
- compare device-discriminative versus condition-discriminative behavior

## Scientific interpretation
A large performance drop under real shift is not a failed experiment; it is evidence of acquisition dependence. A robust method must retain device discrimination while reducing condition dependence.

Feature importance alone cannot prove a feature is transmitter-intrinsic. The evidence must come from cross-condition behavior and, where possible, controlled comparisons.

## D8 dependency
D8 should not be treated as scientifically meaningful until D7 establishes at least one real sequential/condition boundary suitable for profile evolution. The chronological-update protocol requires ordered observations, frozen evaluation, profile acceptance rules, monitoring and rollback protection.

## Data request
Before executing D7.1–D7.4, obtain/attach the relevant Track-B data package(s):
1. **Oregon State WiFi RFFP** — first priority.
2. **WiSig ManySig** — second priority if the existing copy is not programmatically available.

Do not re-upload the 123-file SMoRFFI archive for D7; it is already sufficient for Track-A stress tests and D3–D6.

## Status
- Track-A synthetic D7 stress: **Implemented / Tested / Demonstrated**.
- Track-B real temporal/domain/receiver D7: **Not yet demonstrated — dataset acquisition/verification required**.
- Scientific validation: **Not yet**.
