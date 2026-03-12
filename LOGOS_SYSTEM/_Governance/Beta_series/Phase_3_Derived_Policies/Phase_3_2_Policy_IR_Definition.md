# Phase-3.2 Policy IR Definition (Design-Only)

Status: DESIGN_ONLY — NON-EXECUTABLE — NON-AUTHORIZING
Authority: DENY (default)

## Purpose of the Policy IR
- Exists solely to support compliance checking and audit; it cannot act, authorize, or drive runtime behavior.
- Explicitly prohibits execution, authorization, runtime consumption, or side effects.

## Normative Authority Relationship
- Markdown governance artifacts remain the sole source of truth.
- The Policy IR is a non-authoritative, derived mirror and is discardable without effect.

## IR Structural Constraints
- Purely declarative; no executable logic.
- No loops, callbacks, timers, external calls, or side effects.
- No mutable state; no state transitions.
- No conditionals that cause action; no embedded control flow.

## IR Content Model (Conceptual Schema)
Allowed elements:
- Policy identifiers (referencing source Markdown sections).
- Constraint identifiers and invariant declarations.
- Denial conditions and explicit prohibitions.
- Required provenance assertions.
- Negative/privation rules that enforce deny-by-default.

Forbidden elements:
- Any “allow” semantics or permissive defaults (only explicit denials and requirements).
- Implicit defaults other than DENY.
- Escalation or delegation logic; no authority inference.

## Determinism Requirements
- IR generation must be deterministic and reproducible.
- Identical Markdown input must produce identical IR output (ordering, naming, structure stable).
- No nondeterministic formatting or parametric variation.

## Hash Binding & Traceability
- Every IR artifact must embed cryptographic binding to the source Markdown (hash of source and source references).
- IR without a valid binding to its source is invalid and must be rejected.

## Failure Semantics
- Missing fields, ambiguity, hash mismatch, or absent proof-of-equivalence ⇒ IR invalid.
- Invalid IR ⇒ denial; no fallback, reconciliation, or repair paths.

## Consumption Rules
- IR may be read by non-executing validators only.
- IR must never be consumed by runtime systems or used to grant permission.
- IR may be discarded at any time with no effect on governance.

## Phase Boundary Statement
- Phase-3.2 does not unlock execution, authorization, autonomy, persistence, scheduling, or continuation.
- This phase defines shape only; it does not define or permit use.

## Designation
This document is DESIGN_ONLY, NON-EXECUTABLE, NON-AUTHORIZING, and maintains a deny-by-default posture.
