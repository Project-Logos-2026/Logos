# Phase-2.1.1 SMP-AA Cataloging Concept (Design-Only)

Status: DESIGN_ONLY
Authority: Protopraxic Logic (PXL)
Source: BUILDING_BLOCKS/SMP-AA-Complete_design_packet/AA_CATALOGING_CONCEPT.md

## Catalog Rules
- Each SMP maintains a hash-indexed catalog of associated AAs.
- Catalog fields: aa_hashes, aa_count, last_aa_added_at.
- The catalog is append-only and never shrinks.
- AA references are by hash only; AA content is stored separately.

## Constraints
- Catalog entries must reference immutable AA hashes.
- Catalog mutation is limited to append operations.
- Catalog state does not imply promotion or semantic mutation.
