# Phase-2.1.1 SMP Invariants (Design-Only)

Status: DESIGN_ONLY
Authority: Protopraxic Logic (PXL)

## Must-Always
- Every SMP carries validated provenance (source, hash, timestamp, authority scope, chain-of-custody).
- Schema fields are complete: identity, type, provenance, temporal_context, status_confidence, privation_compatibility, payload.
- Reads are gated by provenance verification and role-scoped visibility rules.
- Fail-closed behavior on any schema, provenance, or privilege violation.
- Privation metadata is present and honored in downstream governed processes.

## Must-Never
- No execution, scheduling, ticks, continuation, activation, or autonomy.
- No writes, mutation, learning, adaptation, or persistence.
- No implicit aggregation, inference, or cross-linking without explicit governed approval.
- No self-authorization or embedded policy bypass.
- No embedded code, macros, or executable templates inside payload.

## Failure Semantics (Fail-Closed)
- On validation failure: deny access, emit auditable event, do not mutate state.
- On provenance failure: deny access, emit auditable event, quarantine request context.
- On privilege mismatch: deny access, emit auditable event, do not degrade invariants.
- On privation metadata absence: treat as violation; deny and log.

This document is design-only; it introduces no runtime logic and does not reopen any phase.
