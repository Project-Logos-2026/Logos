# Phase-2.1.1 SMP Classification Ladder (Design-Only)

Status: DESIGN_ONLY
Authority: Protopraxic Logic (PXL)
Source: BUILDING_BLOCKS/SMP-AA-Complete_design_packet/SMP_CLASSIFICATION_LADDER.md

## Ladder States
- rejected
- conditional
- provisional
- canonical

## Invariants
- Classification moves are monotonic and never regress.
- Promotion decisions are Logos-only and follow governed AA evaluation.
- Reclassification below canonical is not permitted; canonicalization is terminal.

## Notes
- Classification metadata is stored on the SMP header.
- Classification changes do not mutate SMP payloads.
