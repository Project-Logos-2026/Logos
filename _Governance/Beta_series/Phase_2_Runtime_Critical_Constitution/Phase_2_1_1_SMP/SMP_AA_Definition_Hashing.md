# Phase-2.1.1 SMP-AA Definition and Hashing (Design-Only)

Status: DESIGN_ONLY
Authority: Protopraxic Logic (PXL)
Source: BUILDING_BLOCKS/SMP-AA-Complete_design_packet/SMP_AA_DEFINITION_HASHING.md

## AA Hashing Rules
- Each AA must include aa_hash and bound_smp_hash.
- aa_hash is computed over a canonical representation of AA core fields, AA content fields, and diff references.
- The hash must bind the AA to the SMP identity and SMP hash.
- aa_hash is immutable; any change yields a new AA with a new hash.

## Canonicalization Requirements
- Canonical representation must use stable ordering for all fields.
- Hash computation is non-authoritative; it grants no execution or promotion rights.
- Hash verification is required before cataloging or promotion evaluation.
