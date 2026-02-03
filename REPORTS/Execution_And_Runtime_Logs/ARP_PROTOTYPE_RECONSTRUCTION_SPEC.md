# ARP Prototype Reconstruction Specification (AUTHORITATIVE)

## Purpose
This document defines the **only authorized axioms, contextual embeddings, and architectural constraints**
that may be used to reconstruct ARP prototype modules.

It is intended to be supplied verbatim to an external model (e.g., Claude)
to regenerate prototype Python modules in a **repo-compliant, design-only** form.

No assumptions outside this document are permitted.

---

## Reconstruction Scope

Target modules (design-only prototypes):
- pxl_engine.py
- iel_engine.py
- math_engine.py
- unified_reasoning.py

Location:
DEV_RESOURCES/IN_DEV_BLUEPRINTS/INTEGRATIONS/PROTOTYPES_NORMALIZED/

---

## Global Constraints (NON-NEGOTIABLE)

- **No autonomy**
- **No execution**
- **No authority**
- **No runtime wiring**
- **No proof projection**
- **No new axioms**
- **No new IEL domains**
- **No epistemic overclaims**

All outputs must be explicitly labeled **heuristic_only**.

Any claim of:
- validity
- soundness
- necessity
- consistency

is FORBIDDEN unless explicitly tied to a proof reference (which currently does not exist).

---

## Authoritative Axiomatic Sources

The following are the ONLY permitted logical foundations:

- Existing PXL axioms already present in the repo’s Coq corpus
- No extension, reinterpretation, or inference beyond those axioms is allowed

If a logical operation cannot be grounded in existing axioms:
- it MUST be treated as heuristic
- or deferred to an Application Function

---

## Authoritative IEL Contextual Embeddings

Only existing IEL domains may be referenced.

Permitted domains (non-exhaustive but authoritative):
- AxioPraxis
- GnosiPraxis
- ChronoPraxis
- ModalPraxis / TopoPraxis
- (as already defined under LOGOS_SYSTEM/.../IEL)

No new domains, lenses, or semantic frames may be introduced.

All domain usage must be:
- explicit
- labeled
- non-authoritative

---

## Application Function Boundary (CRITICAL)

ALL non-trivial logic MUST be externalized into governed Application Functions.

Prototypes MAY:
- declare AF dependencies
- describe AF responsibilities
- reference AF interfaces

Prototypes MUST NOT:
- implement AF logic
- simulate AF behavior
- imply AF correctness

Authoritative AF list:
- AF-PXL-VALIDATE
- AF-PXL-CACHE-POLICY
- AF-IEL-DOMAIN-SELECT
- AF-IEL-SYNTHESIZE
- AF-MATH-SIMILARITY
- AF-UNIFIED-AGGREGATE
- AF-EPISTEMIC-DOWNGRADE

AF interfaces are defined in:
LOGOS_SYSTEM/RUNTIME/Runtime_Reasoning/ARP/Application_Functions/INTERFACES.md

---

## Module Responsibilities (Allowed)

### pxl_engine.py
- Declare PXL relation structures
- Route validation requests to AF-PXL-VALIDATE
- Return labeled heuristic outputs only

### iel_engine.py
- Reference existing IEL domains
- Route synthesis to AF-IEL-SYNTHESIZE
- No narrative authority

### math_engine.py
- Provide structural scaffolding only
- Delegate similarity to AF-MATH-SIMILARITY

### unified_reasoning.py
- Aggregate labeled heuristic outputs
- Enforce weakest-epistemic dominance
- Must route final downgrade to AF-EPISTEMIC-DOWNGRADE

---

## Forbidden Patterns

The reconstructed code MUST NOT include:
- default-true validity flags
- implicit necessity inference
- cached truth claims
- hidden heuristics
- silent fallbacks
- autonomous control flow

---

## Required Headers

Each reconstructed module MUST include:
- Canonical LOGOS production header
- Design-only declaration
- Deny-by-default posture
- Explicit note: "No proof-backed claims are made in this module."

---

## Acceptance Criteria

A reconstructed module is ACCEPTABLE iff:
- It compiles
- It contains no logic beyond routing/scaffolding
- All reasoning is delegated to AFs
- All outputs are explicitly heuristic
- No new axioms or contexts appear

Anything else is NON-COMPLIANT.

---

## Status

- ARP Design Phase: CLOSED
- Reconstruction: AUTHORIZED (design-only)
- Implementation: NOT AUTHORIZED
- Proof Projection: BLOCKED

