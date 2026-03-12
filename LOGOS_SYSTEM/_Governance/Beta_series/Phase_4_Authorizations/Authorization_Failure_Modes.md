# Authorization Failure Modes (Design-Only)

Status: DESIGN_ONLY — NON-EXECUTABLE — NON-AUTHORIZING
Authority: DENY (default)

## Failure Cases and Outcomes
- Missing authorization: deny + audit.
- Ambiguous authorization: deny + audit.
- Expired authorization: deny + audit.
- Conflicting authorizations: deny + audit (revocation or stricter constraint dominates).

All failures are fail-closed; no fallback or permissive behavior. No execution or activation is enabled.
