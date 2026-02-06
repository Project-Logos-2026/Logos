# ARP_REUSE_AND_REFACTOR_MAP.md

## Purpose
This document classifies **existing Advanced Reasoning Protocol (ARP) assets** into reuse, refactor, extension, or deprecation categories.
It mirrors the role-clarity approach used for MTP.

---

## REUSE AS-IS (Conceptual / Low Rewrite Cost)

- Existing reasoning engine prototypes (domain-scoped logic, probabilistic, symbolic)
- Early aggregation patterns across reasoning outputs
- Validation scaffolds (structure, coherence checks)
- Meta-reasoning conceptual modules (even if stubbed)

Action:
- Preserve conceptual logic
- Rewrap under new ARP/Core + Tools layering
- Add SMP-first and AA-first interfaces

---

## REFACTOR / NORMALIZE

- Reasoning engines not cleanly categorized by domain
- Aggregators with mixed responsibilities
- Validators conflating truth adjudication with admissibility
- Any reasoning logic operating outside SMP / AA structures

Action:
- Enforce strict domain categorization
- Separate reasoning → aggregation → validation
- Normalize outputs into SMP-AA artifacts

---

## EXTEND (NEW CAPABILITIES REQUIRED)

- Canonical SMP-AA schema compliance
- Dual-pass validation system (pre-meta / post-meta)
- Validator confidence metric framework
- Meta-reasoning diff generation and logging
- Passive runtime hooks for I₃ collaboration
- Promotion-trigger artifact class (I3AA)

---

## DEPRECATE / ISOLATE

- Legacy reasoning orchestration logic
- Any module declaring final truth
- Ad-hoc aggregation scripts
- Non-auditable reasoning outputs

---

END DOCUMENT
