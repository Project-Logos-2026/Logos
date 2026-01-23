# Provenance (Plan → Policy → Tick)

Purpose: document audit-only provenance linkage across planning inputs, policy context, and tick execution traces. No authorization is implied; governance checks must occur upstream.

## Scope
- Capture which plan and policy informed a run.
- Record tick-by-tick events with references back to plan/policy.
- Remain append-only; consumers should not mutate historical entries.

## Schema
- See Plan_Policy_Tick_Schema.json for a minimal JSON Schema describing the expected shape.
- Fields are intentionally permissive (`additionalProperties: true`) to allow downstream enrichment without schema churn.

## Usage
- Attach plan context via `attach_plan_context` before executing ticks.
- Attach policy context via `attach_policy_context` after governance approval.
- Tick audits should include plan and policy references alongside remaining budget and event data.

## Notes
- This provenance is audit-only and must not be treated as evidence of authorization.
- Keep identifiers stable (e.g., plan id/version, policy id/version) to enable reliable cross-run joins.
