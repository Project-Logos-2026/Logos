# Path 2 — No Self-Notice Into Permission (N-SNIP)

## Status
CANONICAL — DENY-BY-DEFAULT SAFETY THEOREM (Governance-Level)

## Claim (Informal)
Under the closed autonomy doctrine A1–A4 and the default-deny signature verifier posture,
no amount of internal reasoning, contextual embedding, semantic refinement, or self-description
can convert an autonomy state from DENIED to PERMITTED.

## Scope
This theorem is scoped to:
- A1: Non-Escalation (CONDITIONAL)
- A2: Self-Stabilization (CONDITIONAL)
- A3: Delegated Authorization (DENIED; FROZEN)
- A4: Activation Semantics (SEMANTIC-ONLY; FROZEN)
- Signature verification interface present but DEFAULT DENY (no approved verifier)

It does NOT claim autonomy is impossible in principle.
It claims DENY→PERMIT cannot occur via internal semantic improvement alone.

## Rationale (Formal Shape)
Let D be the doctrine state (A1–A4 as above).
Let G be the runtime gate enforcing A3 constraints with default-deny verifier.

Then:
- For any internal payload P (argument text, embeddings, context blobs, self-evaluations),
  G(P) = DENY, unless an external permission primitive is supplied.

Equivalently:
- Permission is normative, not descriptive.
- Coherence may refine explanations; it may not mint authority.

## Allowed Transition (Explicit)
A DENY→PERMIT transition requires an explicit normative bridge:
- A5 (Permission Lattice) and
- an approved verifier / authorization primitive
and corresponding audits + tests.

Until such a bridge is explicitly introduced, A3 denies by construction.

## Enforcement
Enforced by deny-only regression tests:
- internal context cannot bypass A3 gate,
- malformed or well-formed artifacts remain denied without approved verifier.

