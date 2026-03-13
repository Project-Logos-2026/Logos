# CLAUDE_CONCEPT_REFINEMENT_WORKFLOW.md

## Document Identity

* **System:** ARCHON_PRIME
* **Platform:** Claude
* **Artifact Type:** Workflow Specification
* **Status:** Draft v1
* **Intent:** Define the iterative refinement loop between GPT/Architect and Claude for concept hardening.

---

## Purpose

This document defines the end-to-end workflow for the concept refinement cycle. It governs how concepts move between GPT/Architect brainstorming and Claude formalization, and defines the stop conditions for each cycle.

---

## Section 1 — Workflow Overview

```
Architect + GPT
    │
    ▼
Concept_Draft_vN.md
    │
    ▼
Claude: Concept_Auditor
    │
    ▼
Concept_Critique_Report.md
    │
    ▼
Architect + GPT: Review critique, apply revisions
    │
    ▼
Concept_Draft_v(N+1).md
    │
    ▼
Claude: Re-audit
    │
    ▼
[Loop until stop condition met]
    │
    ▼
Formal_Concept_Artifact.md (finalized)
    │
    ▼
Claude: Formalization_Expert
    │
    ▼
Design_Specification.md + Implementation_Guide.md
    │
    ▼
GPT: Prompt_Engineer
    │
    ▼
VS Code execution prompts
```

---

## Section 2 — Cycle Entry

A refinement cycle begins when:
- The Architect submits a concept draft to Claude for audit
- GPT hands off a matured concept using the `CLAUDE_CONCEPT_HANDOFF_FORMAT.md`
- The Architect directs Claude to analyze, overhaul, and fix errors in a concept

---

## Section 3 — Cycle Execution

### Pass 1 — Initial Audit

Claude performs a full audit per `CLAUDE_CONCEPT_AUDIT_PROTOCOL.md`:
1. Restatement
2. Functional requirements extraction
3. Constraint mapping
4. Coherence testing
5. Feasibility assessment
6. Risk surface mapping
7. Integration analysis
8. Refinement recommendations
9. Audit verdict

### Pass 2+ — Re-Audit

On subsequent passes:
1. Identify what changed since the last pass
2. Re-audit changed portions
3. Verify prior weaknesses are resolved
4. Check for new weaknesses introduced by revisions
5. Update the verdict

---

## Section 4 — Stop Conditions

The refinement loop terminates when any of the following is true:

1. **Diminishing returns** — Improvements between passes are marginal. No critical weaknesses remain. Refinements are aesthetic or optional rather than structural.

2. **Architect declaration** — The Architect explicitly declares the concept finalized and directs formalization.

3. **Audit passes** — The audit verdict reaches "ready for formalization" and the Architect concurs.

Claude must not unilaterally declare a concept finalized. The Architect must confirm.

---

## Section 5 — Cycle Exit

When the refinement loop terminates:

1. All prior drafts are superseded
2. The most advanced draft becomes the `Formal_Concept_Artifact.md`
3. This artifact becomes the authoritative input for formalization
4. Formalization_Expert mode activates (if the Architect directs)
5. GPT receives formalized outputs for prompt engineering (if applicable)

---

## Section 6 — Fast-Track Mode

Sometimes the Architect may skip iterative brainstorming with GPT and submit directly to Claude with instructions like:

- "Analyze, overhaul, and fix any errors"
- "Enhance where appropriate"
- "Harden this for spec generation"

In this case, Claude combines Concept_Auditor and partial Formalization_Expert functions in a single pass:
1. Audit the concept
2. Apply corrections directly (within the Architect's stated scope)
3. Produce a refined draft with changes clearly marked
4. Return for Architect review

Fast-track does not skip Architect approval. The output must still be reviewed before it becomes a formal specification.

---

## Section 7 — Version Control

Each concept draft must be versioned:
- `Concept_Draft_v1.md` — initial submission
- `Concept_Draft_v2.md` — post-first-audit revision
- `Concept_Draft_vN.md` — post-Nth-audit revision
- `Formal_Concept_Artifact.md` — finalized version

Prior versions are retained for traceability but are not authoritative.

---

## End of Workflow
