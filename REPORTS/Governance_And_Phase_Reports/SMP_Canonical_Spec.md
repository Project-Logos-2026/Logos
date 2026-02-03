# Phase-2.1.1 SMP Canonical Specification (Design-Only)

Status: DESIGN_ONLY
Authority: Protopraxic Logic (PXL)
Scope: Single canonical Structured Memory Packet (SMP) schema; inert, non-executable; deny-by-default.

## Canonical SMP Schema (Design-Only)
- identity: unique, immutable identifier for the SMP (opaque string; no self-generation authority).
- type: declarative category of SMP (e.g., observation, plan_fragment, audit_event); enumeration governed externally.
- provenance: mandatory structured provenance envelope (source, acquisition path, cryptographic hash, timestamp, authority scope, chain-of-custody).
- temporal_context: declared time metadata (observation time, valid_from/valid_until, sequencing hints); no scheduling authority, no ticks.
- status_confidence: declarative status + confidence bounds (e.g., draft/asserted/revoked, confidence in [0,1]); no self-updates.
- privation_compatibility: declarative flags indicating how the SMP behaves under privation handling (redaction, quarantine, revocation compatibility, partial elision allowances); no automatic redaction logic.
- payload: structured, bounded, schema-conformant content; must be inert; no embedded code, scripts, or executable expressions.

## Explicit Prohibitions (Never Permitted)
- No execution, scheduling, ticking, continuation, or activation.
- No autonomy, goal authority, planning authority, or self-direction.
- No write, mutation, learning, adaptation, or persistence enablement.
- No implicit aggregation, inference, or cross-SMP binding without explicit governed process.
- No embedded code, templates with execution hooks, or self-modifying payloads.
- No cryptographic operations that grant authority (signing/attestation must be external and governed).

## Guardrails
- Deny-by-default for all operations beyond read-only inspection.
- Provenance is required and must be validated before any read is honored.
- Any attempt to write/mutate must fail-closed and be auditable.
- Compatibility with privation flows is mandatory; absence of privation metadata is a hard error.
- Phase-Z remains CLOSED_DESIGN_ONLY; this spec does not reopen or grant runtime capability.
