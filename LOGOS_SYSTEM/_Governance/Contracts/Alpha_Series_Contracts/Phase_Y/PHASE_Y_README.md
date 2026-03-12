# Phase-Y — Autonomy Policy & Mediation Layer

Status: DESIGN_ONLY

Phase-Y defines the policy surface governing *how* autonomy could be mediated
if and only if authorized elsewhere. Phase-Y does not grant autonomy.

## Authoritative Artifacts

- PHASE_Y_ENTRY.json
- autonomy_policy_schema.json
- autonomy_classes.json
- mediation_rules.json
- revocation_conditions.json
- autonomy_policy_invariants.json
- autonomy_policy_denial_conditions.json
- PHASE_Y_AUDIT_CLOSURE_CRITERIA.md

## Guarantees

- No autonomy is granted
- No execution or scheduling
- No continuation or ticks
- No persistence or goal authority
- Emergency halt (Phase-X) always supersedes Phase-Y

All artifacts are declarative, inert, and fail-closed.
