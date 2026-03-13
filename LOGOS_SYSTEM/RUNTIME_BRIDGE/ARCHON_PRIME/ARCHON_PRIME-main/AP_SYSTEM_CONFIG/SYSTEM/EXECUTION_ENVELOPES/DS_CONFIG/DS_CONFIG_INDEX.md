SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: DS_Configuration
ARTIFACT_NAME: DS_CONFIG_INDEX
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelopes / DS_CONFIG
STATUS: Active

---------------------------------------------------------------------

# DS_CONFIG — Configuration Artifact Index

## Purpose

This index provides a complete reference for all artifacts in the
DS_CONFIG layer, all validation rules defined across those artifacts,
and a cross-reference map between rules, sections, and EA addenda.

---------------------------------------------------------------------

## ARTIFACT REGISTRY

| Artifact                              | Purpose                                              | Rules Defined |
|---------------------------------------|------------------------------------------------------|---------------|
| DS_CONFIG_DESIGN_SPEC_STRUCTURE.md    | Canonical section structure for DS artifacts         | (structural)  |
| DS_CONFIG_SECTION_REQUIREMENTS.md     | Section ordering, formatting, cross-reference rules  | SO, MO, FE, CR |
| DS_CONFIG_VALIDATION_RULES.md         | Machine-enforceable validation rules for DS artifacts | DSV-001–051  |
| DS_CONFIG_README.md                   | Layer overview, lifecycle, mandatory constraints     | (reference)   |
| DS_CONFIG_INDEX.md                    | This file — complete index                          | (index)       |

---------------------------------------------------------------------

## SECTION 1 — MANDATORY DS SECTION STRUCTURE

Defined in: `DS_CONFIG_DESIGN_SPEC_STRUCTURE.md`

| # | Section Name               | Label                        | Min Content                       |
|---|----------------------------|------------------------------|-----------------------------------|
| 1 | Envelope Overview          | `## 1. Envelope Overview`    | 3 sentences or 5 lines            |
| 2 | Problem Definition         | `## 2. Problem Definition`   | 4 sentences or structured evidence |
| 3 | Target Scope               | `## 3. Target Scope`         | Structured list with paths        |
| 4 | System Boundaries          | `## 4. System Boundaries`    | Permitted/prohibited targets      |
| 5 | Dependency Requirements    | `## 5. Dependency Requirements` | Deps with ID, version, state   |
| 6 | Execution Phases Overview  | `## 6. Execution Phases Overview` | Ordered phases list          |
| 7 | Artifact Bundle Definition | `## 7. Artifact Bundle Definition` | DS/EP/IG names + schema ref |
| 8 | Governance Compliance      | `## 8. Governance Compliance` | All EA-001–EA-010 references     |
| 9 | Safety Constraints         | `## 9. Safety Constraints`   | EA-004 + EA-010 references        |
| 10 | Success Criteria          | `## 10. Success Criteria`    | ≥3 numbered criteria              |

**Completeness threshold:** All 5 conditions in Section 4 of
`DS_CONFIG_DESIGN_SPEC_STRUCTURE.md` must be met.

---------------------------------------------------------------------

## SECTION 2 — SECTION REQUIREMENT RULES

Defined in: `DS_CONFIG_SECTION_REQUIREMENTS.md`

### Ordering Rules

| Rule ID | Rule Title                              | Severity |
|---------|-----------------------------------------|----------|
| SO-001  | Canonical Order Is Mandatory            | CRITICAL |
| SO-002  | No Sections May Be Interleaved          | CRITICAL |
| SO-003  | Header Block Precedes All Sections      | CRITICAL |

### Mandatory vs Optional Rules

| Rule ID | Rule Title                              | Severity |
|---------|-----------------------------------------|----------|
| MO-001  | Mandatory Sections Must Be Non-Empty    | CRITICAL |
| MO-002  | N/A Declarations Require Justification  | HIGH     |
| MO-003  | Optional Section Registration           | LOW      |

### Formatting Rules

| Rule ID | Rule Title                              | Severity |
|---------|-----------------------------------------|----------|
| FE-001  | Section Heading Format                  | HIGH     |
| FE-002  | List Formatting                         | MEDIUM   |
| FE-003  | Table Formatting                        | MEDIUM   |
| FE-004  | Code Block Formatting                   | LOW      |
| FE-005  | Section Dividers                        | MEDIUM   |
| FE-006  | Line Length                             | INFO     |

### Cross-Reference Rules

| Rule ID | Rule Title                              | Peer Artifact |
|---------|-----------------------------------------|---------------|
| CR-001  | EP Cross-Reference Requirement          | EP artifact   |
| CR-002  | IG Cross-Reference Requirement          | IG artifact   |
| CR-003  | EA Addenda Cross-Reference Requirement  | EA-001–EA-010 |
| CR-004  | Schema Cross-Reference Requirement      | DESIGN_SPEC_SCHEMA.json |
| CR-005  | Success Criteria to Phase Traceability  | Section 6 phases |

---------------------------------------------------------------------

## SECTION 3 — VALIDATION RULES (DSV)

Defined in: `DS_CONFIG_VALIDATION_RULES.md`

### Category 1 — Required Sections Present

| Rule ID  | Rule Title                          | Severity | Auto |
|----------|-------------------------------------|----------|------|
| DSV-001  | Mandatory Section Presence Check    | CRITICAL | Yes  |
| DSV-002  | Mandatory Section Non-Empty Check   | CRITICAL | Yes  |
| DSV-003  | Header Metadata Block Present       | CRITICAL | Yes  |
| DSV-004  | Success Criteria Minimum Count (≥3) | HIGH     | Yes  |

### Category 2 — Envelope Manifest Compatibility

| Rule ID  | Rule Title                                        | Severity | Auto |
|----------|---------------------------------------------------|----------|------|
| DSV-010  | Artifact Name Matches Manifest                    | CRITICAL | Yes  |
| DSV-011  | Artifact Hash Consistency (SHA-256)               | CRITICAL | Yes  |
| DSV-012  | Execution Phases Declared in DS Match Manifest    | HIGH     | Yes  |
| DSV-013  | Addenda References Consistent with Manifest       | MEDIUM   | Yes  |

### Category 3 — Schema Compatibility

| Rule ID  | Rule Title                                        | Severity | Auto |
|----------|---------------------------------------------------|----------|------|
| DSV-020  | DS Schema Version Declared                        | HIGH     | Yes  |
| DSV-021  | DS Header Metadata STATUS Enum Compliance         | HIGH     | Yes  |
| DSV-022  | VERSION Field Format Compliance (`N.N`)           | MEDIUM   | Yes  |
| DSV-023  | DATE Field Format Compliance (`YYYY-MM-DD`)       | MEDIUM   | Yes  |

### Category 4 — Artifact Naming Conventions

| Rule ID  | Rule Title                                        | Severity | Auto |
|----------|---------------------------------------------------|----------|------|
| DSV-030  | DS Filename Convention (`*_DS.md`)                | HIGH     | Yes  |
| DSV-031  | ARTIFACT_NAME Header Consistency                  | MEDIUM   | Yes  |

### Category 5 — Governance Rule References

| Rule ID  | Rule Title                                        | Severity | Auto |
|----------|---------------------------------------------------|----------|------|
| DSV-040  | Minimum EA Addenda Coverage (EA-001–EA-010)       | CRITICAL | Yes  |
| DSV-041  | Safety Constraint: Simulation-First Assertion     | CRITICAL | Yes  |
| DSV-042  | Safety Constraint: Rollback Protocol Reference    | HIGH     | Yes  |
| DSV-043  | Governance Authority Declared                     | HIGH     | Yes  |

### Category 6 — Validation Result Reporting

| Rule ID  | Rule Title                                        | Severity | Auto |
|----------|---------------------------------------------------|----------|------|
| DSV-050  | Validation Result Must Be Persisted               | HIGH     | No   |
| DSV-051  | Overall Verdict Classification                    | CRITICAL | Yes  |

**Verdict logic:**
- No failures → `VALID`
- MEDIUM only → `VALID_WITH_WARNINGS`
- Any HIGH or CRITICAL → `VALIDATION_FAILED`

---------------------------------------------------------------------

## SECTION 4 — VALIDATION RULE SEVERITY SUMMARY

| Severity | Count | Rule IDs                                              |
|----------|-------|-------------------------------------------------------|
| CRITICAL | 10    | DSV-001, DSV-002, DSV-003, DSV-010, DSV-011, DSV-040, DSV-041, DSV-051 + SO-001, SO-002 |
| HIGH     | 8     | DSV-004, DSV-012, DSV-020, DSV-021, DSV-030, DSV-042, DSV-043, DSV-050 |
| MEDIUM   | 4     | DSV-013, DSV-022, DSV-023, DSV-031                   |

---------------------------------------------------------------------

## SECTION 5 — EA ADDENDA DEPENDENCY MAP

| EA ID  | DS Sections That Must Reference It   | DSV Rules Enforcing the Reference |
|--------|--------------------------------------|-----------------------------------|
| EA-001 | Section 8 (Governance Compliance)    | DSV-040                           |
| EA-002 | Section 8                            | DSV-040                           |
| EA-003 | Section 8                            | DSV-040                           |
| EA-004 | Section 8 + Section 9 (Safety)       | DSV-040, DSV-041                  |
| EA-005 | Section 8                            | DSV-040                           |
| EA-006 | Section 8                            | DSV-040                           |
| EA-007 | Section 7 (Artifact Bundle) + Section 8 | DSV-020, DSV-040               |
| EA-008 | Section 7 + Section 8                | DSV-040                           |
| EA-009 | Section 8                            | DSV-040                           |
| EA-010 | Section 8 + Section 9                | DSV-040, DSV-042                  |

---------------------------------------------------------------------

## VERSION HISTORY

| Version | Date       | Author    | Change Summary            |
|---------|------------|-----------|---------------------------|
| 1.0     | 2026-03-12 | Architect | Initial canonical release |
