# CLAUDE_CONCEPT_HANDOFF_FORMAT.md

## Document Identity

* **System:** ARCHON_PRIME
* **Platform:** Claude (receiving) / GPT (sending)
* **Artifact Type:** Handoff Format Specification
* **Status:** Draft v1
* **Intent:** Define the standardized format for concept submissions from GPT/Architect to Claude.

---

## Purpose

This document defines how GPT or the Architect must structure concept drafts when submitting them to Claude for audit, formalization, or research.

Standardized handoff reduces ambiguity and prevents Claude from having to reconstruct intent from unstructured input.

---

## Section 1 — Handoff Artifact Structure

Every concept handoff to Claude must include the following sections:

### 1.1 — Concept Identity

```
Concept Name: [name]
Version: [vN]
Source: [GPT brainstorm / Architect direct / prior Claude output]
Handoff Type: [audit / formalization / research / fast-track]
Date: [YYYY-MM-DD]
```

### 1.2 — Concept Summary

A concise description of what the concept is and what it is intended to do.

Maximum: one paragraph for simple concepts, three paragraphs for complex systems.

### 1.3 — Core Objectives

What must this concept achieve? Listed as functional requirements.

### 1.4 — Functional Requirements

Specific behaviors the concept must exhibit.

### 1.5 — Stated Constraints

What must this concept NOT do? What boundaries must it respect?

Include:
- Governance constraints
- Phase constraints
- Deferments
- Scope exclusions

### 1.6 — Candidate Mechanisms

How does the Architect/GPT think this should work? What approaches were considered?

This section may include speculative or provisional ideas. Claude should treat them as input, not as binding.

### 1.7 — Adjacent Subsystems

What other subsystems does this concept interact with? What integration surfaces are expected?

### 1.8 — Open Questions

What is the Architect/GPT uncertain about? What requires Claude's analysis?

### 1.9 — Requested Claude Action

Explicit instruction for which Claude mode to activate:

- `AUDIT` — Concept_Auditor pass
- `FORMALIZE` — Formalization_Expert pass
- `RESEARCH` — Research_Specialist analog search
- `FAST_TRACK` — Combined audit + refinement
- `FULL_PIPELINE` — Audit → Research (if needed) → Formalize

---

## Section 2 — Minimal Handoff

When a full structured handoff is not practical (informal session, voice-to-text, rapid iteration), the minimum viable handoff must include:

1. Concept summary (what it is)
2. Requested action (what Claude should do)
3. Any active constraints or deferments

Claude may request additional information if the minimal handoff is insufficient for the requested action.

---

## Section 3 — Handoff from Claude Back to GPT

When Claude returns a refined concept or critique to GPT/Architect:

### Structure

```
Concept Name: [name]
Version: [vN → vN+1]
Claude Action Performed: [audit / formalization / research]
Date: [YYYY-MM-DD]
```

Followed by the relevant output artifact:
- `Concept_Critique_Report.md` (for audit)
- `Analog_Candidate_Report.md` (for research)
- `Design_Specification.md` (for formalization)
- `Implementation_Guide.md` (for formalization)

---

## Section 4 — Handoff Validation

Before acting on a handoff, Claude must verify:

1. Is the handoff type specified?
2. Are the functional requirements present (even if incomplete)?
3. Are active constraints and deferments stated?
4. Is there enough information to perform the requested action?

If validation fails, Claude must request the missing information before proceeding.

---

## End of Format Specification
