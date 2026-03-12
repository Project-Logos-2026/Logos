# Phase-2.3 Privation Ontology (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)

## Canonical Privation Types
- forbidden: explicitly barred; immutable denial.
- impossible: structurally unrealizable given system constraints; treated as denial.
- revoked: previously allowed but withdrawn; denial dominates any stale positive reference.
- unsafe: prohibited due to safety risk; denial until explicitly re-evaluated under governance.
- out-of-scope: outside declared mission or authority; denial by boundary.

## Relationships and Dominance
- All privation types dominate any positive knowledge or request.
- If multiple privation types apply, the strongest denial (forbidden/impossible) dominates; ties resolve to denial.
- Absence of an explicit positive allowance does not weaken privation; denial remains.

## Application Surface
- Applies to SMPs, UWM reads, planning, and external interaction.
- Privation is structural and precedes provenance, role, read, or planning checks.
- No overrides or discretionary exceptions; deny-by-default.

This ontology is declarative and adds no executable behavior.
