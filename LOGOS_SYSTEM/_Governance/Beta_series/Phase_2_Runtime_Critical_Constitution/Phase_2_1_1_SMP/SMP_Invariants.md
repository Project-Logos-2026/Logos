# Phase-2.1.1 SMP Invariants (Design-Only)

Status: DESIGN_ONLY
Authority: Protopraxic Logic (PXL)

## Must-Always
- Every SMP carries validated provenance (source, hash, timestamp, authority scope, chain-of-custody).
- Schema fields are complete: identity, type, provenance, temporal_context, status_confidence, privation_compatibility, payload.
- classification_state follows the monotonic ladder: rejected -> conditional -> provisional -> canonical.
- append_artifacts is append-only and stores AA hash references; catalog never shrinks.
- Reads are gated by provenance verification and role-scoped visibility rules.
- Fail-closed behavior on any schema, provenance, or privilege violation.
- Privation metadata is present and honored in downstream governed processes.
- No SMP or AA is deleted; reclassification, supersedence, and archival are the only allowed lifecycle changes.

## Must-Never
- No execution, scheduling, ticks, continuation, activation, or autonomy.
- No writes, mutation, learning, adaptation, or persistence.
- No semantic mutation of SMP payloads; all cognition is append-only via AAs.
- No implicit aggregation, inference, or cross-linking without explicit governed approval.
- No self-authorization or embedded policy bypass.
- No embedded code, macros, or executable templates inside payload.

## Failure Semantics (Fail-Closed)
- On validation failure: deny access, emit auditable event, do not mutate state.
- On provenance failure: deny access, emit auditable event, quarantine request context.
- On privilege mismatch: deny access, emit auditable event, do not degrade invariants.
- On privation metadata absence: treat as violation; deny and log.

This document is design-only; it introduces no runtime logic and does not reopen any phase.
