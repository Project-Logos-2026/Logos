# Authorization Object Model (Design-Only)

Status: DESIGN_ONLY — NON-EXECUTABLE — NON-AUTHORIZING
Authority: DENY (default)

This document defines the conceptual structure of an authorization object. It grants no authority and introduces no executable logic.

## Required Fields (Conceptual)
- authorization_id: unique identifier for the authorization record.
- issuer_identity: identity of the issuing authority (must be external/human-governed; no self-issuance).
- subject_identity: identity of the subject receiving the authorization (cannot be the issuer).
- permitted_capabilities: explicit, enumerated capabilities; no wildcards; no implicit permissions.
- prohibited_capabilities: explicit denials that override any permissive intent.
- scope_bounds: explicit bounds (time window, domain, resource constraints); no implicit or unbounded scopes.
- revocation_conditions: explicit conditions under which authorization is terminated.
- audit_requirements: required audit artifacts/events for issuance and use.
- status: DESIGN_ONLY (conceptual placeholder; non-operational).

## Explicit Prohibitions
- No implicit permissions or defaults to allow.
- No wildcard scopes or open-ended grants.
- No self-issued authorizations; issuer ≠ subject.
- No persistence, scheduling, execution, or activation implied by the object.
