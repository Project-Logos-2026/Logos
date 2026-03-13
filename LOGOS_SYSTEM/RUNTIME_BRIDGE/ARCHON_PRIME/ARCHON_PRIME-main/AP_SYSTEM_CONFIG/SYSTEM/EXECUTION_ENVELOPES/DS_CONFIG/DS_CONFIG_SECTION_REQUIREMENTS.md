SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: DS_Configuration
ARTIFACT_NAME: DS_CONFIG_SECTION_REQUIREMENTS
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelopes / DS_CONFIG
STATUS: Active

---------------------------------------------------------------------

# DS_CONFIG — Section Requirements

## Purpose

This document specifies the rules governing section completeness,
ordering, formatting, and cross-referencing for all Design Specification
(DS) artifacts across all ARCHON_PRIME Execution Envelopes.

DS_CONFIG_DESIGN_SPEC_STRUCTURE.md defines what sections must exist.
This document defines the rules that govern how those sections must
be completed, formatted, and linked.

---------------------------------------------------------------------

## RULE SET 1 — SECTION ORDERING RULES

### Rule SO-001 — Canonical Order Is Mandatory

Sections must appear in the DS artifact in the following canonical
order. Reordering is a structural violation.

```
1.  Envelope Overview
2.  Problem Definition
3.  Target Scope
4.  System Boundaries
5.  Dependency Requirements
6.  Execution Phases Overview
7.  Artifact Bundle Definition
8.  Governance Compliance
9.  Safety Constraints
10. Success Criteria
```

**Enforcement:**
Section order is verified by sequential heading scan. Any section
appearing out of canonical order causes the ordering check to fail.

---

### Rule SO-002 — No Sections May Be Interleaved

Optional extension sections (Section 11 and above) must appear after
Section 10 (Success Criteria). Optional sections must not be inserted
between any two mandatory sections.

---

### Rule SO-003 — Header Block Precedes All Sections

Every DS artifact must begin with a metadata header block before the
first markdown heading. The header block must contain the following
keys, one per line:

```
SYSTEM: <value>
ARTIFACT_TYPE: Design_Specification
ARTIFACT_NAME: <value>
VERSION: <value>
DATE: <YYYY-MM-DD>
AUTHORITY: <value>
SUBSYSTEM: <value>
STATUS: <value>
```

The header block terminates at the first blank line followed by a
markdown heading (`#`). Any DS artifact missing this header block
will fail header validation before section validation begins.

---------------------------------------------------------------------

## RULE SET 2 — MANDATORY VS OPTIONAL SECTIONS

### Rule MO-001 — Mandatory Sections Must Be Non-Empty

Sections 1 through 10 are mandatory. A section is considered
non-empty if it contains at least one of the following:
- A prose paragraph of three or more sentences, or
- A structured list with a minimum of two items, or
- A table with a minimum of two rows (header row + one data row).

A section containing only a heading or a placeholder (`TBD`, `TODO`,
`N/A` without justification) is treated as empty and will fail the
completeness check.

---

### Rule MO-002 — N/A Declarations Require Justification

If a mandatory section is genuinely not applicable to a specific
envelope, it must still be present and must contain a justification
statement of the form:

```
This section is not applicable to this envelope because [reason].
```

An unexplained `N/A` entry is treated as an incomplete section.

---

### Rule MO-003 — Optional Section Registration

Optional sections (11 and above) used in a DS artifact must be
registered in a section index at the end of the artifact, if the
DS contains three or more optional sections. The index format is:

```
## Section Index — Optional Sections
| Section | Title              | Purpose                   |
|---------|--------------------|---------------------------|
| 11      | Implementation Notes | ...                     |
| 12      | Known Risks          | ...                     |
```

---------------------------------------------------------------------

## RULE SET 3 — FORMATTING EXPECTATIONS

### Rule FE-001 — Section Heading Format

All mandatory section headings must use the pattern:

```
## N. Section Name
```

Where N is 1–10. Sub-section headings must use:

```
### N.M Sub-section Name
```

Heading deviations (e.g., bold text used as a heading, missing number
prefix, wrong heading level) will cause the heading parser to reject
the section as non-conformant.

---

### Rule FE-002 — List Formatting

Structured lists within DS sections must use either:
- Unordered lists (` - item` or `* item`)
- Ordered lists (`1. item`)

Nested lists are permitted to a maximum depth of two levels.
Tab-indented lists without markers are not permitted.

---

### Rule FE-003 — Table Formatting

Tables must include a header row with pipe-separated columns and a
separator row of dashes:

```
| Column A | Column B |
|----------|----------|
| value    | value    |
```

Tables without a separator row are not considered valid structured
tables for the purposes of section completeness evaluation.

---

### Rule FE-004 — Code Block Formatting

Inline code must use single backtick delimiters: `` `value` ``.
Multi-line code or config blocks must use fenced code blocks with
triple backticks and a language hint where applicable:

```
```json
{ "key": "value" }
```
```

---

### Rule FE-005 — Section Dividers

Mandatory sections must be preceded by a horizontal rule using the
separator pattern:

```
---------------------------------------------------------------------
```

This separator is used by section-boundary parsers to delimit section
start positions. Deviation from this pattern may prevent section
detection.

---

### Rule FE-006 — Line Length

Prose lines should not exceed 72 characters, consistent with the
existing ARCHON_PRIME artifact formatting standard. This is a style
recommendation, not a hard validation failure condition.

---------------------------------------------------------------------

## RULE SET 4 — CROSS-REFERENCE REQUIREMENTS

### Rule CR-001 — EP Cross-Reference Requirement

Every DS artifact must contain at least one explicit reference to
its paired Execution Plan (EP) artifact. The reference must appear
in Section 6 (Execution Phases Overview) or Section 7 (Artifact
Bundle Definition), using the artifact's canonical name.

**Valid Reference Pattern:**
```
EP Artifact: <ENVELOPE_NAME>_EP.md (v<version>)
```

---

### Rule CR-002 — IG Cross-Reference Requirement

Every DS artifact must contain at least one explicit reference to
its paired Implementation Guide (IG) artifact. The reference must
appear in Section 7 (Artifact Bundle Definition).

**Valid Reference Pattern:**
```
IG Artifact: <ENVELOPE_NAME>_IG.md (v<version>)
```

---

### Rule CR-003 — EA Addenda Cross-Reference Requirement

Section 8 (Governance Compliance) must list all EA addenda that
govern this envelope. Minimum required EA references:

| EA ID  | Title                              |
|--------|------------------------------------|
| EA-001 | Envelope Target Integrity          |
| EA-002 | Artifact Router Enforcement        |
| EA-003 | Deterministic Execution Ordering   |
| EA-004 | Simulation First Rule              |
| EA-005 | Governance Consistency Check       |
| EA-006 | Execution Logging Requirements     |
| EA-007 | Artifact Metadata Schema Enforcement |
| EA-008 | Envelope Manifest Contract         |
| EA-009 | Prompt Compiler Integration        |
| EA-010 | Failure Rollback Protocol          |

Envelopes claiming a governance exception must document the exception
in Section 8 with explicit justification.

---

### Rule CR-004 — Schema Cross-Reference Requirement

Section 7 (Artifact Bundle Definition) must reference the schema
artifact used to validate the DS itself:

```
DS Schema: DESIGN_SPEC_SCHEMA.json (v<version>)
```

The schema version referenced must match the schema file present in
`EE_SCHEMAS/` at the time of envelope compilation.

---

### Rule CR-005 — Success Criteria to Execution Phase Traceability

Section 10 (Success Criteria) must include at least one criterion
that is traceable to an execution phase declared in Section 6
(Execution Phases Overview). The traceability link must be explicit,
either by naming the phase or by criterion ID reference.

---------------------------------------------------------------------

## RULE SET 5 — SECTION COMPLETENESS SCORING

Section completeness is evaluated as a score for audit purposes.

| Condition                          | Score Delta |
|------------------------------------|-------------|
| Section present                    | +10         |
| Section non-empty (content passes) | +10         |
| Heading format correct             | +5          |
| Cross-references present           | +5          |
| Section divider present            | +2          |

**Maximum score per section:** 32 points
**Total maximum score (10 mandatory sections):** 320 points

**Score thresholds:**

| Score         | Classification |
|---------------|----------------|
| 288–320       | COMPLETE       |
| 224–287       | ACCEPTABLE     |
| 160–223       | MARGINAL       |
| Below 160     | INCOMPLETE     |

A DS artifact scored INCOMPLETE must not be promoted to APPROVED
status and must not be used as the basis for EP compilation.

---------------------------------------------------------------------

## SECTION 6 — VERSION HISTORY

| Version | Date       | Author    | Change Summary            |
|---------|------------|-----------|---------------------------|
| 1.0     | 2026-03-12 | Architect | Initial canonical release |
