# PHASE 5 — TEMPLATE ARTIFACT SCHEMA

## 1. Purpose and Authority

This document defines the canonical artifact schema for all Phase 5 Natural Language Externalization templates in the LOGOS system.

It governs structure, required metadata, allowed content, prohibited constructs, and routing rules.

This schema is design-time authoritative, fail-closed, and immutable once approved.

All template artifacts under Phase 5 MUST conform exactly to this schema.

## 2. Scope

This schema applies only to:
- Phase 5
- Primitive (axiomatic) natural-language templates
- Projection-only artifacts
- Non-authoritative, downstream externalization

It does not apply to runtime logic, meaning translation, proof artifacts, context overlays, or template modulators.

## 3. Canonical Location

All template artifacts governed by this schema MUST be stored at:

 /workspaces/Logos/LOGOS_EXTERNALIZATION/templates/

The directory MUST remain flat. No subdirectories are permitted at the primitive layer.

## 4. File Naming Convention

Each template MUST be stored as a single Markdown file named:

 TEMPLATE_<PRIMITIVE_IDENTIFIER>.md

Where the primitive identifier is uppercase snake case and matches an allowed primitive exactly.

## 5. Required Document Structure

Each template file MUST contain the following sections in order:
1. Title Header
2. Governance Header
3. Primitive Declaration
4. Slot Declaration
5. Template Body
6. Constraints

No additional sections are permitted.

## 6. Allowed Primitive Identifiers (Locked)

ASSERTION_CONFIRMED
ASSERTION_NEGATED
ASSERTION_UNPROVEN
CONDITIONAL_SATISFIED
CONDITIONAL_UNSATISFIED
PROOF_CONFIRMED
PROOF_FAILED
VALIDATION_INCOMPLETE
SCOPE_LIMITATION
SCOPE_VIOLATION
DEPENDENCY_DISCLOSURE
DEPENDENCY_UNSATISFIED
PRECONDITIONS_REQUIRED
PRECONDITIONS_UNMET
CONSTRAINT_DISCLOSURE
CONSTRAINT_VIOLATED
AUDIT_PASSED
AUDIT_FAILED
ARTIFACT_REFERENCE
TECHNICAL_EXPLANATION
DECLARATIVE_EXPLANATION
PEDAGOGICAL_EXPLANATION

No other primitives may be introduced without a new schema revision.

## 7. Governance Header (Required)

Each template MUST include:

- Phase: 5
- Layer: Natural Language Externalization
- Artifact_Type: Template_Primitive
- Authority: LOGOS_Phase_5
- Mutability: Immutable
- Execution_Status: Non_Executable

## 8. Primitive Declaration

Each template MUST declare exactly one primitive matching its filename.

## 9. Slot Declaration

Slots MUST use {UPPER_SNAKE_CASE} syntax.
All slots MUST be explicitly declared.
No optional slots, defaults, or inferred values are permitted.

If no slots are required, the section MUST explicitly state "None".

## 10. Template Body

The body MUST:
- Use a single deterministic phrasing
- Contain no stylistic variation
- Contain no branching or optional language
- Introduce no new facts

Examples, summaries, and inferences are prohibited.

## 11. Constraints

Each template MUST restate:
- No inference
- No summarization
- No stylistic variation
- No contextual assumptions

## 12. Validation Rules

Any artifact that violates this schema is invalid and MUST NOT be loaded, indexed, or deployed.

## 13. Final Invariant

Governance overrides convenience.
Determinism overrides expressiveness.
Failure is preferred to silent correction.
