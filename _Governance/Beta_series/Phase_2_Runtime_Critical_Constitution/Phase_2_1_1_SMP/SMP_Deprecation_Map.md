# Phase-2.1.1 SMP Deprecation Map (Design-Only)

Status: DESIGN_ONLY
Authority: Protopraxic Logic (PXL)

## Legacy / Conflicting Artifacts
- logos/uwm.py — legacy stub for unified working memory; non-authoritative and superseded for SMP schema purposes.
- _Dev_Resources/Dev_Scripts/smoke_tests/test_logos_runtime_smoke.py — legacy test constructing minimal SMP; informational only, not authoritative.
- _Dev_Resources/Dev_Invariables/runtime_spine_contract_v1.json — historical contract describing SMP processing; informational; superseded.
- _Dev_Resources/Dev_Invariables/Finished_Contracts/* (UWM_Ingestion_Contract, 3PDN_Constraint_Contract, 3PDN_Validator_Contract, Runtime_Input_Sanitizer_Contract) — legacy intake/validation contracts; informational; not canonical for SMP schema.
- _Dev_Resources/SYSTEM_STACK_AUTOMATED_GROUPING.json entries pointing to System_Stack/Unified_Working_Memory/SMP/* — grouping metadata; non-authoritative; superseded.
- _Dev_Resources/Dev_Invariables/Abbreviations.json — terminology only; not a schema.

## Canonicalization Decision
- The canonical SMP schema is defined in this phase: SMP_Canonical_Spec.md.
- All legacy or conflicting artifacts are classified as deprecated or informational; they must not be used as schema sources.
- Any future SMP-related work must reference the canonical spec and invariants in this Phase-2.1.1 folder.

## Authoritative SMP-AA Governance (Design-Only)
- SMP_AA_Session_Epistemic_Substrate.md
- SMP_AA_Shared_Schema_Appendix.md
- SMP_AA_Cataloging_Concept.md
- SMP_AA_Definition_Hashing.md
- SMP_Agent_AA_Schemas.md
- SMP_Logos_Promotion_Schema.md
- SMP_Non_Deletion_Principle.md
- SMP_Classification_Ladder.md
- SMP_Copy_Distinction.md
- SMP_Storage_Stratification.md

## Design Packet Provenance (Non-Governance Source)
- BUILDING_BLOCKS/SMP-AA-Complete_design_packet/* provides design-only source material; governance authority is established by the documents in this Phase-2.1.1 folder.

No runtime behavior is introduced; this map is declarative only.
