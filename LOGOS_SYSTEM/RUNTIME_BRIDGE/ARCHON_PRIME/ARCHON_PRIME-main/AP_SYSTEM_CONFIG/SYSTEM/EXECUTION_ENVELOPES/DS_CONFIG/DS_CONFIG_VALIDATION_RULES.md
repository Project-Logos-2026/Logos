SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: DS_Configuration
ARTIFACT_NAME: DS_CONFIG_VALIDATION_RULES
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelopes / DS_CONFIG
STATUS: Active

---------------------------------------------------------------------

# DS_CONFIG — Validation Rules

## Purpose

This document defines the complete set of validation conditions that
must be satisfied before a Design Specification (DS) artifact is
considered valid within an ARCHON_PRIME Execution Envelope. These
rules are machine-enforceable where indicated and must be applied
at all DS review and promotion gates.

---------------------------------------------------------------------

## RULE CATEGORY 1 — REQUIRED SECTIONS PRESENT

### Rule DSV-001 — Mandatory Section Presence Check

**Check ID:** DSV-001
**Category:** Structural
**Severity:** CRITICAL
**Auto-enforceable:** Yes

**Condition:**
All ten mandatory sections must be present in the DS artifact.

**Method:**
Scan the DS markdown file for the following headings in order:

```
## 1. Envelope Overview
## 2. Problem Definition
## 3. Target Scope
## 4. System Boundaries
## 5. Dependency Requirements
## 6. Execution Phases Overview
## 7. Artifact Bundle Definition
## 8. Governance Compliance
## 9. Safety Constraints
## 10. Success Criteria
```

**Pass Condition:**
All ten headings are detected in the correct canonical order.

**Failure Action:**
DS artifact is flagged `VALIDATION_FAILED`. Execution against this
DS is blocked. EP compilation is prohibited until the failure is
resolved.

---

### Rule DSV-002 — Mandatory Section Non-Empty Check

**Check ID:** DSV-002
**Category:** Structural
**Severity:** CRITICAL
**Auto-enforceable:** Yes

**Condition:**
Each mandatory section must contain substantive content, not only
a heading or a placeholder.

**Method:**
For each detected mandatory section, extract all content between
the section heading and the next `##`-level heading. Content is
considered present if:
- Character length of stripped content exceeds 100 characters, OR
- A structured list with two or more items is detected, OR
- A table with at least one data row is detected.

**Pass Condition:**
All ten mandatory sections contain content meeting the threshold.

**Failure Action:**
Each empty or placeholder section is individually flagged.
Aggregate result: `VALIDATION_FAILED` if any mandatory section fails.

---

### Rule DSV-003 — Header Metadata Block Present

**Check ID:** DSV-003
**Category:** Structural
**Severity:** CRITICAL
**Auto-enforceable:** Yes

**Condition:**
The DS artifact must begin with a header metadata block containing
all eight required keys:

- `SYSTEM`
- `ARTIFACT_TYPE`
- `ARTIFACT_NAME`
- `VERSION`
- `DATE`
- `AUTHORITY`
- `SUBSYSTEM`
- `STATUS`

**Method:**
Parse the first N lines of the file up to the first blank line
followed by a `#`-level heading. Extract key-value pairs and verify
all eight keys are present and non-empty.

**Pass Condition:**
All eight keys present with non-empty values.

**Failure Action:**
`HEADER_VALIDATION_FAILED`. File may not be registered as a valid
DS artifact until the header block is corrected.

---

### Rule DSV-004 — Success Criteria Minimum Count

**Check ID:** DSV-004
**Category:** Structural
**Severity:** HIGH
**Auto-enforceable:** Yes

**Condition:**
Section 10 (Success Criteria) must contain a minimum of three
individually numbered criteria.

**Method:**
Within Section 10 content, count ordered list items (`1.`, `2.`,
etc.) or criterion identifiers matching the pattern `Criterion_N`.

**Pass Condition:**
Count >= 3.

**Failure Action:**
`CRITERIA_INSUFFICIENT`. DS artifact is flagged for mandatory
revision before it may be used to compile an EP.

---------------------------------------------------------------------

## RULE CATEGORY 2 — ENVELOPE MANIFEST COMPATIBILITY

### Rule DSV-010 — Artifact Name Matches Manifest

**Check ID:** DSV-010
**Category:** Manifest Compatibility
**Severity:** CRITICAL
**Auto-enforceable:** Yes

**Condition:**
The DS artifact filename and `ARTIFACT_NAME` header key value must
match the `design_specification.artifact` field in the envelope's
`ENVELOPE_MANIFEST.json`.

**Method:**
Load the `ENVELOPE_MANIFEST.json` associated with this envelope.
Compare `artifact_bundle.design_specification.artifact` value
against the DS file being validated.

**Pass Condition:**
Both values resolve to the same canonical filename.

**Failure Action:**
`MANIFEST_MISMATCH`. Execution is blocked by EA-001 (Envelope
Target Integrity). Artifact identity mismatch must be resolved
before any further validation proceeds.

---

### Rule DSV-011 — Artifact Hash Consistency

**Check ID:** DSV-011
**Category:** Manifest Compatibility
**Severity:** CRITICAL
**Auto-enforceable:** Yes

**Condition:**
The SHA-256 hash of the DS artifact at runtime must match the hash
recorded in `ENVELOPE_MANIFEST.json` at the key
`artifact_bundle.design_specification.hash`.

**Method:**
Compute SHA-256 of the DS artifact file content. Compare against
the manifest-recorded hash value.

**Pass Condition:**
Hashes match exactly.

**Failure Action:**
`ARTIFACT_HASH_MISMATCH`. Per EA-001, execution must halt
immediately. No mutations may proceed. Incident must be logged.

---

### Rule DSV-012 — Execution Phases Declared in DS Match Manifest

**Check ID:** DSV-012
**Category:** Manifest Compatibility
**Severity:** HIGH
**Auto-enforceable:** Yes

**Condition:**
The execution phases listed in DS Section 6 (Execution Phases
Overview) must be consistent with the `execution_phases` array in
`ENVELOPE_MANIFEST.json`. All phases declared in the manifest must
appear in Section 6.

**Method:**
Extract ordered phase names from Section 6 (ordered list items).
Compare against the `execution_phases` array in the manifest.
Order must be preserved.

**Pass Condition:**
All manifest-declared phases appear in Section 6 in the same order.

**Failure Action:**
`PHASE_ALIGNMENT_FAILURE`. DS must be updated to reflect the
manifest's authoritative phase list before EP compilation.

---

### Rule DSV-013 — Addenda References Consistent with Manifest

**Check ID:** DSV-013
**Category:** Manifest Compatibility
**Severity:** MEDIUM
**Auto-enforceable:** Yes

**Condition:**
EA addenda listed in DS Section 8 (Governance Compliance) must
include all EA identifiers listed in the `addenda` array of
`ENVELOPE_MANIFEST.json`.

**Method:**
Extract EA identifiers from the manifest `addenda` field. Verify
each identifier appears in Section 8 content.

**Pass Condition:**
All manifest-listed EA IDs are referenced in Section 8.

**Failure Action:**
`ADDENDA_REFERENCE_GAP`. Missing EA references flagged. DS must
be updated to include all addenda references.

---------------------------------------------------------------------

## RULE CATEGORY 3 — SCHEMA COMPATIBILITY

### Rule DSV-020 — DS Schema Version Declared

**Check ID:** DSV-020
**Category:** Schema Compatibility
**Severity:** HIGH
**Auto-enforceable:** Yes

**Condition:**
DS Section 7 (Artifact Bundle Definition) must declare the schema
version used to validate the DS artifact, referencing the file:

```
DESIGN_SPEC_SCHEMA.json
```

located at:

```
AP_SYSTEM_CONFIG/SYSTEM/EXECUTION_ENVELOPES/EE_SCHEMAS/
```

**Method:**
Scan Section 7 content for the string `DESIGN_SPEC_SCHEMA.json`.
Verify version reference is present alongside the schema name.

**Pass Condition:**
Schema filename and version are present in Section 7.

**Failure Action:**
`SCHEMA_REFERENCE_MISSING`. DS must declare its schema reference.

---

### Rule DSV-021 — DS Header Metadata STATUS Enum Compliance

**Check ID:** DSV-021
**Category:** Schema Compatibility
**Severity:** HIGH
**Auto-enforceable:** Yes

**Condition:**
The `STATUS` value in the DS header block must be one of the
canonical status values defined in `DESIGN_SPEC_SCHEMA.json`:

```
draft | under_review | approved | locked | superseded | deprecated | rejected
```

**Method:**
Extract `STATUS` from the header block. Check against the enum.

**Pass Condition:**
`STATUS` value matches one of the permitted enum values.

**Failure Action:**
`INVALID_STATUS_VALUE`. Header block must be corrected.

---

### Rule DSV-022 — VERSION Field Format Compliance

**Check ID:** DSV-022
**Category:** Schema Compatibility
**Severity:** MEDIUM
**Auto-enforceable:** Yes

**Condition:**
The `VERSION` field in the DS header block must conform to the
pattern: `<major>.<minor>` (e.g., `1.0`, `2.3`).

**Method:**
Apply regex pattern `^\d+\.\d+$` against the VERSION header value.

**Pass Condition:**
Pattern matches.

**Failure Action:**
`VERSION_FORMAT_INVALID`. Header block must be corrected.

---

### Rule DSV-023 — DATE Field Format Compliance

**Check ID:** DSV-023
**Category:** Schema Compatibility
**Severity:** MEDIUM
**Auto-enforceable:** Yes

**Condition:**
The `DATE` field in the DS header block must conform to ISO 8601
date format: `YYYY-MM-DD`.

**Method:**
Apply regex pattern `^\d{4}-\d{2}-\d{2}$` against the DATE header
value.

**Pass Condition:**
Pattern matches.

**Failure Action:**
`DATE_FORMAT_INVALID`. Header block must be corrected.

---------------------------------------------------------------------

## RULE CATEGORY 4 — ARTIFACT NAMING CONVENTIONS

### Rule DSV-030 — DS Filename Convention

**Check ID:** DSV-030
**Category:** Naming Convention
**Severity:** HIGH
**Auto-enforceable:** Yes

**Condition:**
DS artifact filenames must conform to the pattern:

```
<ENVELOPE_NAME>_DS.md
```

Where `ENVELOPE_NAME` is the canonical envelope identifier in
UPPER_SNAKE_CASE.

**Examples of valid filenames:**
```
AP_V2_TOOLING_DS.md
MODULE_REPAIR_DS.md
HEADER_NORMALIZATION_DS.md
```

**Method:**
Apply regex pattern `^[A-Z0-9_]+_DS\.md$` against the filename.

**Pass Condition:**
Pattern matches.

**Failure Action:**
`FILENAME_CONVENTION_VIOLATION`. File must be renamed before
it can be registered as a valid DS artifact.

---

### Rule DSV-031 — ARTIFACT_NAME Header Consistency

**Check ID:** DSV-031
**Category:** Naming Convention
**Severity:** MEDIUM
**Auto-enforceable:** Yes

**Condition:**
The `ARTIFACT_NAME` value in the DS header block must match the
DS filename without the `.md` extension.

**Example:**
Filename `AP_V2_TOOLING_DS.md` requires:
```
ARTIFACT_NAME: AP_V2_TOOLING_DS
```

**Method:**
Strip `.md` from the filename. Compare against `ARTIFACT_NAME`
header value.

**Pass Condition:**
Values match exactly.

**Failure Action:**
`ARTIFACT_NAME_MISMATCH`. Header block must be corrected.

---------------------------------------------------------------------

## RULE CATEGORY 5 — GOVERNANCE RULE REFERENCES

### Rule DSV-040 — Minimum EA Addenda Coverage

**Check ID:** DSV-040
**Category:** Governance
**Severity:** CRITICAL
**Auto-enforceable:** Yes

**Condition:**
DS Section 8 (Governance Compliance) must reference all ten
canonical EA addenda (EA-001 through EA-010).

**Required EA References:**

| EA ID  | Title                                  |
|--------|----------------------------------------|
| EA-001 | Envelope Target Integrity              |
| EA-002 | Artifact Router Enforcement            |
| EA-003 | Deterministic Execution Ordering       |
| EA-004 | Simulation First Rule                  |
| EA-005 | Governance Consistency Check           |
| EA-006 | Execution Logging Requirements         |
| EA-007 | Artifact Metadata Schema Enforcement   |
| EA-008 | Envelope Manifest Contract             |
| EA-009 | Prompt Compiler Integration            |
| EA-010 | Failure Rollback Protocol              |

**Method:**
Scan Section 8 content for each EA identifier string
(`EA-001`, `EA-002`, ..., `EA-010`).

**Pass Condition:**
All ten EA identifiers are detected in Section 8.

**Failure Action:**
`GOVERNANCE_REFERENCE_INCOMPLETE`. Each missing EA reference
is individually flagged. DS cannot be promoted to `approved`
status until all EA references are present.

---

### Rule DSV-041 — Safety Constraint: Simulation-First Assertion

**Check ID:** DSV-041
**Category:** Governance
**Severity:** CRITICAL
**Auto-enforceable:** Yes

**Condition:**
DS Section 9 (Safety Constraints) must contain an explicit
assertion of the simulation-first requirement, referencing EA-004.

**Method:**
Scan Section 9 content for the string `EA-004` or
`Simulation First Rule` (case-insensitive).

**Pass Condition:**
At least one of the target strings is detected in Section 9.

**Failure Action:**
`SIMULATION_ASSERTION_MISSING`. DS must be updated to declare
the simulation-first safety constraint before it may govern
a live execution envelope.

---

### Rule DSV-042 — Safety Constraint: Rollback Protocol Reference

**Check ID:** DSV-042
**Category:** Governance
**Severity:** HIGH
**Auto-enforceable:** Yes

**Condition:**
DS Section 9 (Safety Constraints) must reference the rollback
protocol (EA-010).

**Method:**
Scan Section 9 content for the string `EA-010` or
`Failure Rollback Protocol` (case-insensitive).

**Pass Condition:**
At least one of the target strings is detected in Section 9.

**Failure Action:**
`ROLLBACK_REFERENCE_MISSING`. DS must include rollback protocol
reference in Section 9.

---

### Rule DSV-043 — Governance Authority Declared

**Check ID:** DSV-043
**Category:** Governance
**Severity:** HIGH
**Auto-enforceable:** Yes

**Condition:**
DS Section 8 (Governance Compliance) must declare the governing
authority for the envelope. The `AUTHORITY` header value must
also match the authority declared in Section 8 content.

**Method:**
Extract `AUTHORITY` from the header block. Scan Section 8 for
the same authority string.

**Pass Condition:**
Header `AUTHORITY` value appears in Section 8 content.

**Failure Action:**
`AUTHORITY_MISMATCH`. Header and Section 8 authority declarations
must be reconciled.

---------------------------------------------------------------------

## RULE CATEGORY 6 — VALIDATION RESULT REPORTING

### Rule DSV-050 — Validation Result Must Be Persisted

**Check ID:** DSV-050
**Category:** Reporting
**Severity:** HIGH
**Auto-enforceable:** No (process requirement)

**Condition:**
The result of DS validation must be persisted as a validation
report artifact in the envelope's `VALIDATION/` directory.

**Required Report Content:**
- Envelope name
- DS artifact name and hash validated
- Validation timestamp
- List of checks executed (DSV-001 through DSV-043)
- Pass / Fail result per check
- Overall validation verdict: `VALID` or `VALIDATION_FAILED`

**Pass Condition:**
Validation report artifact exists and contains all required fields.

---

### Rule DSV-051 — Overall Verdict Classification

**Check ID:** DSV-051
**Category:** Reporting
**Severity:** CRITICAL
**Auto-enforceable:** Yes

**Condition:**
The overall validation verdict is determined by the highest-
severity failure among all checks executed.

**Verdict Logic:**

| Highest Failure Severity | Overall Verdict     |
|--------------------------|---------------------|
| No failures              | VALID               |
| MEDIUM only              | VALID_WITH_WARNINGS |
| HIGH (any)               | VALIDATION_FAILED   |
| CRITICAL (any)           | VALIDATION_FAILED   |

A DS artifact with overall verdict `VALIDATION_FAILED` must not
be used to compile an EP, and execution against it is prohibited.

---------------------------------------------------------------------

## SECTION 7 — VALIDATION RULE REGISTRY

| Rule ID  | Category               | Severity | Auto-Enforceable |
|----------|------------------------|----------|------------------|
| DSV-001  | Required Sections      | CRITICAL | Yes              |
| DSV-002  | Required Sections      | CRITICAL | Yes              |
| DSV-003  | Required Sections      | CRITICAL | Yes              |
| DSV-004  | Required Sections      | HIGH     | Yes              |
| DSV-010  | Manifest Compatibility | CRITICAL | Yes              |
| DSV-011  | Manifest Compatibility | CRITICAL | Yes              |
| DSV-012  | Manifest Compatibility | HIGH     | Yes              |
| DSV-013  | Manifest Compatibility | MEDIUM   | Yes              |
| DSV-020  | Schema Compatibility   | HIGH     | Yes              |
| DSV-021  | Schema Compatibility   | HIGH     | Yes              |
| DSV-022  | Schema Compatibility   | MEDIUM   | Yes              |
| DSV-023  | Schema Compatibility   | MEDIUM   | Yes              |
| DSV-030  | Naming Convention      | HIGH     | Yes              |
| DSV-031  | Naming Convention      | MEDIUM   | Yes              |
| DSV-040  | Governance             | CRITICAL | Yes              |
| DSV-041  | Governance             | CRITICAL | Yes              |
| DSV-042  | Governance             | HIGH     | Yes              |
| DSV-043  | Governance             | HIGH     | Yes              |
| DSV-050  | Reporting              | HIGH     | No               |
| DSV-051  | Reporting              | CRITICAL | Yes              |

---------------------------------------------------------------------

## SECTION 8 — VERSION HISTORY

| Version | Date       | Author    | Change Summary            |
|---------|------------|-----------|---------------------------|
| 1.0     | 2026-03-12 | Architect | Initial canonical release |
