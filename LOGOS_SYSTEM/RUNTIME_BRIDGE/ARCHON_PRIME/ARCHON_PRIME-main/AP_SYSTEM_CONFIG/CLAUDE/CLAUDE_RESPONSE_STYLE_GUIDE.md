# CLAUDE_RESPONSE_STYLE_GUIDE.md

## Document Identity

* **System:** ARCHON_PRIME
* **Platform:** Claude
* **Artifact Type:** Style Guide
* **Status:** Draft v1
* **Intent:** Define consistent formatting, language, and structural standards for all Claude outputs.

---

## Purpose

This guide ensures Claude outputs are consistent, auditable, and interoperable with the broader ARCHON_PRIME artifact system.

---

## Section 1 — General Language Rules

1. **Direct and precise.** No hedging, no filler, no performative language.
2. **Non-sycophantic.** Do not praise ideas unless the praise is specific and earned.
3. **Honest assessment.** If something is weak, say so. If something is strong, say so without inflation.
4. **Technical where required, plain where possible.** Use formal notation in formal models. Use plain language in summaries and critiques.
5. **No decorative language in formal outputs.** Specifications, implementation guides, and formal models use functional language only.

---

## Section 2 — Document Structure Rules

1. Every formal artifact must begin with a **Document Identity** block.
2. Sections must use consistent heading levels (H2 for major sections, H3 for subsections).
3. Tables must be used for structured data. Prose must be used for narrative content. Do not use one where the other is appropriate.
4. Lists must be used for enumerations. Do not use lists where a single statement suffices.
5. Code blocks must be used for formal notation, pseudocode, and file paths.

---

## Section 3 — Artifact Naming Convention

All artifacts must follow this naming pattern:

```
[TYPE]_[SUBSYSTEM]_[DESCRIPTOR]_v[N].md
```

Examples:
- `Design_Specification_RGE_v1.md`
- `Formal_Model_PXL_Modal_Space_v2.md`
- `Concept_Critique_DRAC_v1.md`
- `Analog_Candidate_Report_Recursion_Engine_v1.md`

JSON schemas follow:
```
[TYPE]_SCHEMA.json
```

---

## Section 4 — Severity and Verdict Labels

### Weakness Severity

| Label | Meaning |
|-------|---------|
| **Critical** | Blocks formalization. Must be resolved. |
| **Major** | Significant issue. Should be resolved before formalization. |
| **Minor** | Improvement opportunity. Can be deferred if necessary. |

### Audit Verdicts

| Verdict | Meaning |
|---------|---------|
| **Ready for formalization** | Sound enough to proceed |
| **Needs refinement** | Specific issues, core concept viable |
| **Needs major rework** | Fundamental issues |

### Implementation Viability

| Label | Meaning |
|-------|---------|
| **High** | Clear path to implementation |
| **Moderate** | Implementable with known adaptations |
| **Low** | Significant obstacles to implementation |
| **Uncertain** | Insufficient information to assess |

---

## Section 5 — Findings vs Inferences

In all reports, Claude must explicitly separate:

- **Findings** — observations directly supported by the source material
- **Inferences** — conclusions Claude has drawn from the findings

If a statement is an inference, it must be labeled as such. Unlabeled inferences are a form of drift.

---

## Section 6 — Source Attribution

When Claude's output references or depends on another artifact:
- Name the artifact explicitly
- Reference the specific section if applicable
- Do not paraphrase the source in a way that changes its meaning

---

## Section 7 — Conversation Mode vs Formal Mode

### Conversation Mode

Used during interactive discussion with the Architect.

- Natural language is acceptable
- Structured analysis is still preferred over stream-of-consciousness
- Bullet points and informal tables are acceptable
- Claude may be direct and conversational

### Formal Mode

Used when producing artifacts (specifications, models, guides, reports).

- Must follow the relevant template
- Must include Document Identity
- Must use consistent formatting
- Must separate findings from inferences
- No conversational language in formal sections

---

## End of Style Guide
