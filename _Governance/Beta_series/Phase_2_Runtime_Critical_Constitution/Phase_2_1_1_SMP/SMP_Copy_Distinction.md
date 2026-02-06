# Phase-2.1.1 SMP vs SMP-Copy Distinction (Design-Only)

Status: DESIGN_ONLY
Authority: Protopraxic Logic (PXL)
Source: BUILDING_BLOCKS/SMP-AA-Complete_design_packet/SMP_COPY_DISTINCTION.md

## Definitions
- SMP: Immutable, provenance-bound semantic packet governed by Phase-2.1.1.
- SMP-copy: Transient runtime view derived from an SMP for local processing.

## Rules
- SMPs are immutable and non-deletable.
- SMP-copies are ephemeral and may be discarded after use.
- SMP-copies are not authoritative and must never be promoted or stored as SMPs.
- Any persisted record must retain SMP identity and AA lineage references.
