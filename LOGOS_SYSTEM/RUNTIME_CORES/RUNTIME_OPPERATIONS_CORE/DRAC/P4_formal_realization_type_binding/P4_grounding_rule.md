# PHASE_4_GROUNDING_RULE.md
Status: CANONICAL | DESIGN-ONLY
Execution: FORBIDDEN
Authority: Specification Only
Scope: Governs all Phase 4 Type Schema and artifact production

---

## Semantic Synopsis (GPT Handoff)

This artifact establishes the mandatory grounding rule for all Phase 4
Type Schema production. It prevents the introduction of ungrounded
structure — fields, types, or assertions not traceable to Phase 2/3
source material and not explicitly justified as Phase 4 derivations.
It belongs to the Orchestration layer (governance of the design process
itself). It does not define types or interfaces; it constrains how they
are produced. GPT should treat this as a standing constraint that applies
to every subsequent Phase 4 artifact.

---

## 1. Purpose

This rule governs the production of all Phase 4 Type Schemas and
related artifacts. It exists to prevent the introduction of ungrounded
structure — fields, types, or assertions that are not traceable to
Phase 2 or Phase 3 source material and are not explicitly justified
as Phase 4 derivations.

Phases 1–3 are CLOSED and CANONICAL. Phase 4 artifacts must derive
from them, not augment them with uninstructed invention.

---

## 2. The Grounding Rule

Every structural field, subordinate type, and capability assertion
in a Phase 4 Type Schema MUST satisfy exactly one of the following:

### (A) TRACE

The element traces directly to a declaration in a Phase 2 or Phase 3
artifact. The source must be cited by artifact name and section.

### (B) DERIVE

The element is explicitly labeled as a Phase 4 derivation WITH all
three of the following:

- Justification: why this element is necessary for Phase 4 closure
- Source anchor: the Phase 2/3 artifact section that motivates or
  implies the element, even if it does not explicitly declare it
- Explicit statement: "This is a Phase 4 derivation."

No third option exists. Silent invention of plausible structure is a
Phase 4 violation regardless of how reasonable the invented element
appears.

---

## 3. Traceability Table Requirement

Every Phase 4 Type Schema MUST include a Traceability Table as its
final substantive section. The table maps every field, subordinate
type, and non-trivial assertion in the schema to its grounding.

### Required Table Structure

| Element | Grounding | Justification | Source |
|---------|-----------|---------------|--------|

Column definitions:
- Element: field name, subordinate type name, or assertion text
- Grounding: TRACE or DERIVE
- Justification: "Direct declaration" for TRACE; derivation rationale
  for DERIVE
- Source: exact artifact name + section reference for TRACE;
  motivating source for DERIVE

A schema without this table is structurally incomplete and must not
be adopted.

---

## 4. Forbidden Patterns

The following patterns constitute Phase 4 violations:

(a) Invented metadata fields (e.g., session_id, timestamp, version
    numbers) without explicit Phase 2/3 source or Phase 4 derivation
    justification.

(b) Subordinate types introduced without either inline minimal
    structural definition or a compliant forward-reference declaration
    (see Section 5).

(c) Capability or constraint assertions (e.g., "must be immutable,"
    "authorizes execution") not traceable to Phase 2/3 invariants and
    not explicitly justified as Phase 4 derivations.

(d) Fields modeled from general software convention rather than from
    the declared function of the stage as specified in Phase 2/3.

(e) Schemas that model stage identity or operational metadata rather
    than the stage's declared input types, output types, and primary
    function as specified in Phase 2 and Phase 3.

---

## 5. Forward Reference Rule

If a subordinate type is referenced in a Type Schema but not defined
inline, the schema MUST include a forward-reference declaration for
that type. The declaration must have the following structure:

    Forward Reference: <type name>
    Definition artifact: <exact filename where it will be defined>
    Expected phase: <Phase 4 or later>

A forward reference that does not name a specific definition artifact
is a violation. Placeholders such as "TBD," "future artifact," or
"to be determined" are not acceptable.
