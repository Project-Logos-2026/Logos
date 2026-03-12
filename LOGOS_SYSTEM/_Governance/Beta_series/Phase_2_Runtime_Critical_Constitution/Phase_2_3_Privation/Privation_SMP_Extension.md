# Phase-2.3 Privation SMP Extension (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)

## Representation in SMPs
- Add privation_flags: list of privation types (forbidden, impossible, revoked, unsafe, out_of_scope).
- Add privation_links: references to SMP identities that this SMP negates or that negate this SMP; linkage is mandatory when a privation applies.
- Add privation_basis: rationale or governing clause identifiers; declarative only.

## Rules
- If an SMP is subject to privation, privation_flags and privation_links must be present; missing linkage is a fail-closed condition.
- Privation metadata travels with SMP views; redaction may not remove privation indicators.
- Any privation on a linked SMP dominates the positive SMP; positive content must not be acted upon.

No runtime logic is introduced; this is schema-level guidance only.
