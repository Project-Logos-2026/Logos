# Phase-2.1.1 Logos Promotion Decision Schema (Design-Only)

Status: DESIGN_ONLY
Authority: Protopraxic Logic (PXL)
Source: BUILDING_BLOCKS/SMP-AA-Complete_design_packet/LOGOS_PROMOTION_SCHEMA.md

## Mechanical Promotion Model
- Promotion decisions are non-discretionary and criteria-driven.
- Logos evaluates the presence of required AA types and required proofs.
- Logos evaluates convergence metrics and unresolved conflicts.
- Promotion never mutates the original SMP payload.

## Promotion Outcomes
- Update SMP classification metadata, or
- Create a new Canonical SMP (C-SMP) derived from the SMP + AA set + proof artifacts.

## Constraints
- Agents never promote SMPs directly.
- AAs inform promotion but do not cause promotion.
- Canonicalization is terminal; canonical SMPs are closed to further AAs.
