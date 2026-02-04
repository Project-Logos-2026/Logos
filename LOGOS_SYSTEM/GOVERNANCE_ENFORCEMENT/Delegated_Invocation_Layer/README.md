# Delegated Invocation Layer (DIL)

DIL defines how protocol invocation *could* be structurally contained
in principle. It does not invoke, authorize, schedule, or execute tools.

Key properties:
- No agent holds invocation authority
- Invocation is hypothetical, single-use, revocable, and non-persistent
- This layer is design-only and non-executable

Any attempt to implement execution without explicit authorization
is a governance violation.
