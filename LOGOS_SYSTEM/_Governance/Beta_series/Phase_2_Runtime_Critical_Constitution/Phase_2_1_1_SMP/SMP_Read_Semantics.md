# Phase-2.1.1 SMP Read Semantics (Design-Only)

Status: DESIGN_ONLY
Authority: Protopraxic Logic (PXL)

## Role-Scoped Visibility (Design-Only)
- Governance roles may read SMP metadata and payload only after provenance verification.
- Observability roles may read redacted payload views according to privation_compatibility flags.
- Audit roles may read full SMP plus provenance for compliance review.
- AA catalog visibility is limited to AA hash references; AA content reads require separate governed authorization.
- No other roles are permitted by default; all non-listed roles are denied.

## Provenance-Aware Access Requirements
- Provenance must be present, well-formed, and validated prior to any read.
- Reads must bind to the validated provenance record and record a read audit trail (design-only, non-executable requirement).
- Privation_compatibility must be evaluated to determine redaction level; absence triggers deny.

## Explicit Denials
- No implicit aggregation, inference, or cross-SMP joins without explicit governed approval.
- No caching, persistence, or replication of SMP contents outside governed storage.
- No transformation or enrichment steps; reads are non-mutating and non-persistent.
- No implicit AA expansion or inline AA content injection during SMP reads.
- No escalation to execution, autonomy, scheduling, or continuation.

All semantics are inert and declarative. No runtime code is introduced.
