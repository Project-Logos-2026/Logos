# Phase-2.1.1 Storage Stratification (Design-Only)

Status: DESIGN_ONLY
Authority: Protopraxic Logic (PXL)
Source: BUILDING_BLOCKS/SMP-AA-Complete_design_packet/STORAGE_STRATIFICATION.md

## Storage Boundaries
- Canonical SMPs live only in CSP.
- Non-canonical SMPs live in MTP Core.
- All AAs live in MTP Core.

## Epistemic Library Layout (Design-Only)
Epistemic_Library/
- Non_Canonical_SMPs/
- Agent_Generated_AAs/
- Protocol_Generated_AAs/

## Constraints
- Storage rules are governance constraints; no runtime authority is granted here.
- Cross-tier copying must preserve provenance and AA lineage references.
