# CLAUDE_FEEDBACK_REPORT_FORMAT.md

## Document Identity

* **System:** ARCHON_PRIME
* **Platform:** Claude
* **Artifact Type:** Output Format Specification
* **Status:** Draft v1
* **Intent:** Define the standardized structure for Claude's feedback, critique, and analysis reports.

---

## Purpose

This document defines how Claude must structure its output reports when returning analysis, critique, or refinement recommendations to the Architect or GPT.

---

## Section 1 — Standard Feedback Report Structure

All Claude feedback reports follow this structure:

### 1. Report Identity

```
Report Type: [Concept Critique / Analog Analysis / Formalization Review / Gap Analysis]
Concept: [concept name]
Input Version: [vN]
Date: [YYYY-MM-DD]
Claude Mode: [Concept_Auditor / Research_Specialist / Formalization_Expert]
```

### 2. Concept Restatement

Claude's restatement of the concept in its own terms. This confirms understanding before critique begins.

### 3. Strengths

What works well in the current concept. Specific, not general. Each strength should identify what it enables or protects.

### 4. Weaknesses

What does not work or is fragile. Each weakness must include:
- Description of the problem
- Why it matters (impact)
- Severity: **Critical** / **Major** / **Minor**

### 5. Gaps

What is missing. Each gap must include:
- What is absent
- Why it is needed
- What fails without it

### 6. Risks

What could fail catastrophically at runtime or during integration. Each risk must include:
- Risk description
- Trigger condition
- Potential impact
- Suggested mitigation

### 7. Integration Assessment

How the concept relates to adjacent subsystems:
- Expected integration surfaces
- Identified conflicts
- Overlooked integration opportunities

### 8. Refinement Recommendations

For each weakness, gap, or risk, a specific recommended change:
- What to change
- Why
- Whether the change requires Architect authorization (scope change, new dependency, etc.)

### 9. Audit Verdict

One of:
- **Ready for formalization** — concept is sound
- **Needs refinement** — specific issues identified, core concept viable
- **Needs major rework** — fundamental issues require significant revision

### 10. Open Questions

Questions Claude cannot resolve without Architect input. These must be specific and actionable.

---

## Section 2 — Analog Candidate Report Structure

When Claude is in Research_Specialist mode:

### 1. Report Identity

(same as above, with Report Type: Analog Analysis)

### 2. Concept Summary

What abstract system the analog search targeted.

### 3. Candidate Analogs

For each candidate:

```
Analog: [name / description]
Domain: [mathematical domain]
Structural Correspondence: [what matches]
Adaptation Required: [what needs modification]
Limitations: [where it breaks down]
Implementation Viability: [assessment]
```

### 4. Comparative Ranking

Candidates ranked by structural fidelity and implementation viability.

### 5. Recommendation

Which candidate Claude recommends and why, with honest statement of tradeoffs.

---

## Section 3 — Formalization Report Structure

When Claude produces formal models or specifications, the output follows the relevant template (`DESIGN_SPEC_TEMPLATE.md`, `FORMAL_MODEL_TEMPLATE.md`, etc.) rather than this feedback format.

However, if a formalization pass includes a verification review, the review portion follows this format with Report Type: Formalization Review.

---

## Section 4 — Formatting Rules

1. Use headers consistently per the structures defined above
2. Severity labels must be present on all weaknesses
3. Findings must be separated from inferences — if Claude is inferring rather than directly observing, it must say so
4. Recommendations must be specific enough to act on
5. No decorative language in formal reports
6. No hedging that obscures the assessment — state the verdict clearly

---

## End of Format Specification
