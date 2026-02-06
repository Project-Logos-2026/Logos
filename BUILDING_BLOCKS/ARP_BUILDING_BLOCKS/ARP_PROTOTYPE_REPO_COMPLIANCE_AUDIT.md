# ARP Prototype → Repo Compliance Audit (Design-Only)

## Scope
Audit the following prototype engines against existing LOGOS axioms,
contextual embeddings, and application-function boundaries.

Prototype location:
DEV_RESOURCES/IN_DEV_BLUEPRINTS/INTEGRATIONS/PROTOTYPES
- pxl_engine.py
- iel_engine.py
- math_engine.py
- unified_reasoning.py

Authoritative references:
- PXL axioms (existing Coq corpus)
- IEL domains and contextual embeddings
- Runtime application-function architecture
- ARP_HEURISTIC_CLASSIFICATION.md

## Audit Questions

### 1. Repo Compliance
For each prototype file:
- Does it respect layering (no direct authority, no runtime control bypass)?
- Does it avoid epistemic overclaims?
- Does it avoid embedding application logic that should be externalized?

Record: PASS / FAIL with notes.

### 2. Axiomatic Sufficiency
For each logical operation:
- Identify which existing axiom(s) it relies on, if any.
- Flag any operation that assumes an axiom not present in the repo.

Explicit rule:
- New axioms are NOT permitted at this stage.
- Any such finding must be flagged as NON-COMPLIANT.

### 3. Contextual Embedding Sufficiency
For each domain/lens usage:
- Map it to an existing IEL domain or embedding.
- Flag any implicit or novel context not already defined.

Explicit rule:
- New contextual embeddings require justification and separate approval.

### 4. Application Function Gaps
Identify any logic that:
- Should exist as a governed application function,
- But is currently embedded directly in prototype code.

This is the ONLY permitted expansion surface.

## Findings Format
For each file:
- Compliance summary
- Axioms used (explicit / implicit / none)
- Contextual embeddings used
- Required changes (if any):
  - Rewrite
  - Downgrade to heuristic
  - Extract to application function
  - Reject

## Output
This document serves as the authoritative gate for:
- Prototype normalization,
- Proof projection eligibility,
- Future ARP integration.

No code changes are authorized in this step.