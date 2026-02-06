# MTP_REUSE_AND_REFACTOR_MAP.md

## Purpose
This document enumerates **existing Meaning Translation Protocol (MTP) assets** and classifies them for:
- Reuse
- Refactor / Normalize
- Extend
- Deprecate

It is an implementation-facing companion to `MTP_BLUEPRINT_DRAFT.md`.

---

## REUSE AS-IS (Minimal or No Change)

These components are structurally sound and aligned with the new MTP role.

- Lambda calculus translation engines (NL → λ → symbolic)
- Symbolic math translation utilities
- Core semantic enrichment pipelines (tokenization, parsing, expansion)
- Sentence transformers / semantic extractors
- Existing natural-language translation helpers

Action:
- Wrap with SMP-first interfaces
- Add provenance metadata hooks

---

## REFACTOR / NORMALIZE

These components are valuable but require restructuring to meet new invariants.

- SMP generation logic (must become absolute primitive)
- Metadata handling (centralize into SMP header)
- Translation output handling (route through Translation Compiler)
- Tool-layer NLP processors (standardize inputs/outputs)
- Existing AA-like outputs (convert to canonical AA schema)

Action:
- Enforce SMP-first processing
- Add header injection
- Normalize outputs into AA-compatible structures

---

## EXTEND (NEW CAPABILITIES REQUIRED)

These capabilities are required but not fully present.

- SMP Header Injection System
- AA Storage Container (authoritative workspace)
- AA Catalog management inside SMP header
- I2AA artifact class (promotion-request artifacts)
- Formal logic projection layer:
  - PXL encoders
  - IEL overlay generators
- Passive runtime orchestration hooks (MTP + I₂)
- Promotion-condition tagging and tracking

Action:
- Design and implement per blueprint
- No legacy constraints

---

## DEPRECATE / ISOLATE

These elements should not be part of MTP going forward.

- Any tool operating outside SMP context
- Implicit or undocumented metadata mutation
- Free-floating semantic outputs not tied to SMP or AA
- Legacy experiment scripts not wired to runtime

Action:
- Archive or remove from runtime path

---

END DOCUMENT
