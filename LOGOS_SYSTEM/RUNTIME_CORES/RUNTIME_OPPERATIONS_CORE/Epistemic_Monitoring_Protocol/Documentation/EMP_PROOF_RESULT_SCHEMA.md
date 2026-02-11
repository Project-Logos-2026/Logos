# EMP Proof Result Schema

Status: DESIGN_ONLY — NON-EXECUTABLE — NON-AUTHORIZING
Authority: Epistemic_Monitoring_Protocol governance scope
Binding: Shared AA Schema Appendix (Phase-2.1.1)

## Purpose

Defines the canonical structured output format for EMP proof verification results.
Every EMP proof verification produces an AA conforming to this schema.

## AA Envelope

- aa_type: ProtocolAA
- originating_entity: EMP
- aa_origin_type: protocol

## Proof Result Fields

### classification
- Type: string
- Enum: UNVERIFIED | PROVISIONAL | PARTIAL | VERIFIED_AXIOMATIC | VERIFIED_PXL | CANONICAL_CANDIDATE
- Monotonic ordering: UNVERIFIED < PROVISIONAL < PARTIAL < VERIFIED_AXIOMATIC < VERIFIED_PXL < CANONICAL_CANDIDATE
- No artifact may skip classification levels.

### classification_ordinal
- Type: integer
- Range: 0-5
- Maps directly to classification enum.

### confidence_uplift
- Type: float
- Range: 0.00-0.20
- Graduated by classification tier:
  - UNVERIFIED: 0.00
  - PROVISIONAL: 0.02
  - PARTIAL: 0.05
  - VERIFIED_AXIOMATIC: 0.10
  - VERIFIED_PXL: 0.15
  - CANONICAL_CANDIDATE: 0.20

### coq_verification
- verified: bool
- admits_count: integer (>= 0)
- axiom_dependencies: array of string
- axioms_within_pxl_kernel: bool
- proof_steps: integer
- compilation_time_ms: integer
- error_message: string or null

### mspc_coherence
- Type: bool or null
- null indicates MSPC witness unavailable or not applicable.
- true required for CANONICAL_CANDIDATE classification.
- false halts classification at VERIFIED_PXL.

### budget_consumed
- Type: integer
- Reasoning steps consumed during this classification.

### budget_remaining
- Type: integer
- Reasoning steps remaining after this classification.

### artifact_hash
- Type: string
- SHA-256 truncated to 16 characters.
- Computed from artifact content at classification time.

### timestamp
- Type: float
- Unix epoch seconds at classification time.

## Validation Rules

A proof result AA is invalid if:
- classification is not in the defined enum
- classification_ordinal does not match classification
- confidence_uplift does not match classification tier
- CANONICAL_CANDIDATE is set but mspc_coherence is not true
- admits_count > 0 but classification is VERIFIED_AXIOMATIC or higher
- coq_verification.verified is false but classification is PARTIAL or higher

Invalid proof result AAs are rejected without escalation.

## Governance

This schema introduces no runtime logic or authority.
Violations are epistemic integrity failures and SOP triggers.
