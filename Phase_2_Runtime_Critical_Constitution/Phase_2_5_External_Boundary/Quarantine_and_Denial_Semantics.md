# Phase-2.5 Quarantine and Denial Semantics (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)

## Denial Conditions
- Malformed external outputs.
- Provenance missing, invalid, or unverifiable.
- Privation conflicts or safety violations.
- Schema mismatch or ambiguity.

## Behavior
- Default outcome: deny and log (design-only requirement).
- Quarantine is allowed as an inert holding pattern; no execution or transformation.
- No automatic repair, enrichment, or retry; human/governance review only.

Declarative only; no runtime code or side effects.
