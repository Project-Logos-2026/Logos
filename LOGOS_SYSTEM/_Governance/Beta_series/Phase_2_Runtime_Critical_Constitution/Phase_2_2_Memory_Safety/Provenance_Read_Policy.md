# Phase-2.2 Provenance Read Policy (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)

## Requirements
- Every read request must carry request-level provenance (who, when, purpose, authority scope) and must validate successfully before any data access.
- Target SMPs must contain valid provenance per SMP_Canonical_Spec; absence or mismatch is a hard failure.
- Provenance must bind to the role asserted in the request; role mismatch triggers deny.

## Failure Semantics (Fail-Closed)
- Missing or invalid request provenance: DENY + audit log (design-only requirement).
- Missing or invalid target provenance: DENY + audit log.
- Insufficient role authority relative to provenance scope: DENY + audit log.

## Additional Constraints
- No inferred or default provenance; silence equals denial.
- No caching of provenance evaluations; each read is independently validated.
- No transformation or enrichment based on provenance; read-only views only.

This policy is declarative and introduces no executable logic or authorization tokens.
