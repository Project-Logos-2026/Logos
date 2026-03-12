# Phase-2.2 UWM Read-Only API Specification (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)
Scope: Canonical, read-only interface for Unified Working/World Memory (UWM). No writes, no caching, no aggregation, no inference, no execution.

## Inputs (Required)
- role: declared requester role (governance/audit/observer/etc.); must map to Memory_Access_Control_Matrix.
- query_scope: bounded selection criteria (by SMP identity, type, temporal_context window, provenance hash). No open-ended queries.
- provenance_requirements: caller presents validated provenance chain for the request itself; target SMPs must also contain validated provenance.

## Behavior (Design-Only)
- Perform provenance verification before any read.
- Enforce role-scope check; unspecified roles are denied.
- Return SMP views only; no transformation or enrichment.
- Apply privation_compatibility rules to determine allowable view; absence triggers deny.
- Reads are non-persistent and non-mutating; no caching or replication.

## Outputs (Read-Only)
- Zero or more SMP view objects strictly conforming to SMP_Canonical_Spec fields.
- Each view is provenance-attested and may be redacted per privation_compatibility.

## Explicit Prohibitions (Never Permitted)
- Writes, mutation, persistence, learning, adaptation, continuation, or scheduling.
- Implicit aggregation, inference, or cross-SMP joining.
- Execution, activation, autonomy, or goal authority effects.
- Caching, replication, or offline copies outside governed storage.
- Authorization elevation or bypass; default posture is DENY.

This document is declarative and introduces no executable logic.
