# Phase-2.3 Privation Failure Semantics (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)

## Failure Cases
- Privation violation (positive conflicts with privation): deny and log.
- Ambiguity (privation unclear or unresolved): deny and log.
- Conflict between positive and negative SMPs: privation dominates; deny and log.
- Missing privation linkage when required: deny and log.

## Requirements
- Denials are fail-closed; no fallback to permissive behavior.
- Audit logging is required (design-only requirement) for every denial event.
- No automatic reconciliation or override paths; human/governance review only.

Declarative only; no runtime code is added.
