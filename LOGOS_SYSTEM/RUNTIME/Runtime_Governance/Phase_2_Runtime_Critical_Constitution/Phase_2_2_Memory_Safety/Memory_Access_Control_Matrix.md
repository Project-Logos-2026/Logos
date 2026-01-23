# Phase-2.2 Memory Access Control Matrix (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)
Scope: Descriptive role × memory-scope visibility table for read-only UWM. Unspecified entries are DENY.

| Role                | Metadata Only | Redacted Payload | Full Payload | Notes |
|---------------------|---------------|------------------|--------------|-------|
| Governance          | ALLOW         | ALLOW            | ALLOW        | Must verify requester provenance; privation_compatibility governs redaction. |
| Audit               | ALLOW         | ALLOW            | ALLOW        | Read for compliance only; no mutation or persistence beyond governed logs. |
| Observability/Ops   | ALLOW         | ALLOW            | DENY         | Redacted views only; no inference/aggregation; provenance required. |
| Development         | ALLOW         | DENY             | DENY         | Metadata-only for diagnostics; no payload content; provenance required. |
| Any other role      | DENY          | DENY             | DENY         | Default posture; absence of explicit allowance = DENY. |

Explicit denials apply to writes, mutation, caching, aggregation, inference, activation, scheduling, and autonomy for all roles.
This matrix is descriptive only; it is not an authorization object and carries no executable effect.
