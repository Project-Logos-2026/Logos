# CLAUDE_MODULE_HEADER_PROTOCOL.md

## Document Identity

| Field | Value |
|---|---|
| Artifact ID | OPS-008 |
| System | ARCHON_PRIME |
| Platform | Claude |
| Artifact Type | Operational Protocol — Module Header Generation and Validation |
| Version | v1 |
| Status | Draft |
| Authority Source | Architect |
| Schema Reference | AP_MASTER_SPEC_V2_SCHEMA.json §13 |
| Supersedes | None — STANDALONE |

---

## Purpose

This protocol defines how Claude generates and validates module headers when operating in the AP workflow. Module headers are the machine-readable identity blocks that every runtime module must carry. They enable the architecture validator to verify canonical identity, enforce subsystem boundaries, detect drift, and generate dependency graphs without heuristic inference.

This protocol applies when Claude is:
- Generating a header block for a new module
- Validating an existing header against the canonical registry
- Interpreting header violations reported in an architecture validation report
- Producing a module generation specification that includes header requirements

---

## Section 1 — Header Generation Procedure

### 1.1 Inputs Required

Before generating a header, Claude must have access to:

1. The module's entry in the canonical module registry (from the relevant Design Specification §8)
2. The header schema definition from the same Design Specification (§13)
3. The subsystem contract for the module's subsystem (§10)

If any of these three inputs is missing, Claude must request them before generating the header. A header generated without the registry entry is not canonical.

### 1.2 Field Population Rules

Populate header fields in this order. All fields marked `must_match_registry: true` must exactly match the registry value — no paraphrasing, no abbreviation.

| Field | Source | Must Match Registry | Population Rule |
|-------|--------|--------------------|-|
| module_id | Registry entry | Yes | Copy exactly from `module_id` |
| module_name | Registry entry | Yes | Copy exactly from `module_name` (filename without extension) |
| subsystem | Registry entry | Yes | Copy exactly from `subsystem` |
| canonical_path | Registry entry | Yes | Copy exactly from `canonical_path` (full path from repo root including filename) |
| responsibility | Registry entry | No | Copy from `responsibility` or paraphrase if registry entry is brief |
| runtime_stage | Registry entry | No | Copy from `runtime_stage`; must be one of the declared enum values |
| allowed_imports | Subsystem contract | No | Derive from `allowed_imports` in subsystem contract; list one entry per line |
| forbidden_imports | Subsystem contract | No | Derive from `forbidden_cross_imports` in subsystem contract; list one entry per line |
| spec_reference | Current spec | No | Format: `[SPEC-NNNN.section.N]` — reference the spec section defining this module's behavior |
| implementation_phase | Registry entry | No | Copy from `implementation_phase` |
| authoring_authority | Fixed | No | Always: `ARCHON_PRIME` |
| version | Determined at generation | No | `1.0` for new modules; increment on substantive change |
| status | Determined at generation | No | `canonical` for spec-derived modules; `draft` for provisional modules |

### 1.3 Header Format

Generate the header block in exactly this format. Do not alter field names, spacing, or ordering.

```
# ARCHON PRIME MODULE HEADER
module_id: [M-ID]
module_name: [filename without extension]
subsystem: [subsystem name]
canonical_path: [path/from/repo/root/filename.py]
responsibility: [one-sentence functional description]
runtime_stage: [initialization | analysis | processing | validation | repair | audit | reporting | utility]
allowed_imports:
  - [subsystem or module name]
  - [subsystem or module name]
forbidden_imports:
  - [subsystem or module name]
spec_reference: [SPEC-NNNN.section.N]
implementation_phase: [PHASE_N]
authoring_authority: ARCHON_PRIME
version: [N.N]
status: [canonical | draft | deprecated]
```

If `allowed_imports` or `forbidden_imports` is empty (no entries), write:
```
allowed_imports: []
forbidden_imports: []
```

Do not omit these fields even if empty.

### 1.4 Header Placement

The header block must be placed at the top of the file, before any imports, docstrings, or executable code. In Python modules:

```python
# ARCHON PRIME MODULE HEADER
# module_id: M12
# module_name: import_extractor
# [remaining fields]

"""Module docstring (if any) goes here."""

import os
import sys
# [remaining imports]
```

The header comment block must be the first content in the file. No shebang or encoding declaration should precede it unless the execution environment requires it, in which case those lines appear first and the header immediately follows.

---

## Section 2 — Header Validation Procedure

### 2.1 When to Validate

Claude validates headers when:
- Reviewing an existing module for spec compliance
- Interpreting architecture validation report findings
- Auditing a module before recommending adoption of an analog implementation
- Responding to a Concept_Auditor or Formalization_Expert task that requires assessing existing code

### 2.2 Validation Inputs Required

1. The module file content (header block)
2. The module's entry in the canonical registry
3. The header schema definition from the relevant Design Specification §13

### 2.3 Validation Steps

Execute in order. Record findings for each step.

**Step V-1: Presence Check**
Is a header block present at the top of the file?
- Pass: Header block found, begins with `# ARCHON PRIME MODULE HEADER`
- Fail: No header block found → classify as `header_schema_violations`; severity: blocking

**Step V-2: Field Completeness Check**
Are all 13 required fields present in the header?
Required fields: `module_id`, `module_name`, `subsystem`, `canonical_path`, `responsibility`, `runtime_stage`, `allowed_imports`, `forbidden_imports`, `spec_reference`, `implementation_phase`, `authoring_authority`, `version`, `status`
- Pass: All 13 present
- Fail: Missing fields → classify as `header_schema_violations`; list missing fields

**Step V-3: Registry Match Check**
For each field where `must_match_registry: true`, does the header value exactly match the registry value?
Fields requiring registry match: `module_id`, `module_name`, `subsystem`, `canonical_path`
- Pass: Exact match on all four
- Fail: Mismatch → classify as `header_schema_violations`; state the expected vs. actual value for each mismatch

**Step V-4: Enum Validation**
Does `runtime_stage` contain a declared enum value?
Valid values: `initialization`, `analysis`, `processing`, `validation`, `repair`, `audit`, `reporting`, `utility`
- Pass: Value is one of the above
- Fail: Invalid value → classify as `header_schema_violations`

Does `status` contain a declared enum value?
Valid values: `canonical`, `draft`, `deprecated`
- Pass: Value is one of the above
- Fail: Invalid value → classify as `header_schema_violations`

**Step V-5: Import Compliance Check**
Do the declared `allowed_imports` and `forbidden_imports` align with the subsystem contract?
- Pass: Declared imports are consistent with contract (may be a subset, must not contradict)
- Fail: Header declares an import that the subsystem contract forbids → classify as `import_rule_violations`

**Step V-6: Path Integrity Check**
Does the module exist at the path declared in `canonical_path`?
- Pass: File found at canonical_path
- Fail: File not at canonical_path → classify as `misplaced_modules`

### 2.4 Validation Output Format

When reporting header validation results:

```
MODULE HEADER VALIDATION — [module_name]

Registry Reference: [SPEC-NNNN §8, M-ID]
Validation Date: [YYYY-MM-DD]

V-1 Presence Check:        [PASS / FAIL]
V-2 Field Completeness:    [PASS / FAIL — missing: list]
V-3 Registry Match:        [PASS / FAIL — mismatches: list expected/actual]
V-4 Enum Validation:       [PASS / FAIL — invalid values: list]
V-5 Import Compliance:     [PASS / FAIL — violations: list]
V-6 Path Integrity:        [PASS / FAIL]

Overall Result: [VALID / INVALID]
Classification: [SPEC_PRESENT / SPEC_MISSING / ANALOG_IMPLEMENTATION / HEADER_VIOLATION]
Blocking Issues: [list, or "None"]
Recommended Action: [retain / inject_header / reconcile / escalate]
```

---

## Section 3 — Scope Boundaries

Claude generates and validates headers. Claude does not:
- Execute header injection into repository files (that is VS Code / GPT domain)
- Generate the architecture validation script
- Modify the canonical module registry without Architect authorization

When Claude identifies a header violation in an existing module, the output is a validation report and a recommendation. Implementation of the fix belongs to GPT/VS Code.

---

## End of Protocol
