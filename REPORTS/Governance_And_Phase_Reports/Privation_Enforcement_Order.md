# Phase-2.3 Privation Enforcement Order (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)

## Evaluation Order
1) privation
2) provenance
3) role
4) read (per UWM read-only spec)
5) planning (if ever reached)

## Rules
- Any privation match terminates evaluation with denial; no overrides or exceptions.
- Steps are not skippable; absence of data at any step results in denial.
- Planning is unreachable if any prior step denies.

This ordering is declarative; it introduces no executable pipeline.
