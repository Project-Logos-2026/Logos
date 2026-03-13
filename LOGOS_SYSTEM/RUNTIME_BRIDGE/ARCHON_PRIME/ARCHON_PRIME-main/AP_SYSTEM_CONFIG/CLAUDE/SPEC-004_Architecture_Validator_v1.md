# SPEC-004 — Architecture Validator
## Design Specification: `validate_architecture.py`

---

## Specification Identity

| Field | Value |
|---|---|
| Artifact ID | SPEC-004 |
| System | ARCHON_PRIME |
| Platform | Python 3.11 / Codespaces |
| Artifact Type | Design Specification |
| Version | v1 |
| Status | Draft |
| Schema | AP_MASTER_SPEC_V2_SCHEMA.json |
| Authority Source | Architect |
| Source Concept | Architecture validation requirement derived from AP_MASTER_SPEC_V2_SCHEMA.json §14 and AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json §11 |
| Author | Claude / Formalization_Expert |
| Date | 2026-03-09 |
| Approved By | |
| Phase | Phase 2 — Specification Production (active) |
| DRAC Status | Deferred — not targeted by this spec |

---

## Lineage

| Field | Value |
|---|---|
| Concept Origin | Derived from V2 schema gate conditions and IMPL-002 §11 |
| Analog Origin | null |
| Prior Version | null |
| Supersedes | null |

---

## Purpose

This specification defines `validate_architecture.py`, the canonical architecture validation module for ARCHON_PRIME. It is the module referenced as the `validator_module` in every V2 Implementation Guide's `architecture_validation_gate` section.

`validate_architecture.py` performs a deterministic scan of the repository against the canonical module registry, header schema, subsystem contracts, and artifact surface definitions declared in an approved Design Specification. It produces a machine-readable `architecture_validation_report.json` that drives pipeline gate decisions and feeds Claude's `CLAUDE_VALIDATION_REPORT_PROTOCOL.md` interpretation workflow.

This module is the single source of truth for whether the repository is in a valid architectural state. All pipeline stages gated on `architecture_valid == true` depend entirely on this module's correctness. A broken validator produces false-pass results that allow drift to accumulate silently — this makes its correctness the highest-leverage compliance guarantee in the AP toolchain.

---

## Governance Constraints

| Constraint | Source | Effect |
|---|---|---|
| Governance-first | `CLAUDE_GOVERNANCE_PROTOCOL.md §3` | Validator must run before any gated stage — it is part of governance enforcement, not a post-check |
| Fail-closed | `CLAUDE_GOVERNANCE_PROTOCOL.md §3` | If validator cannot complete its scan (missing registry, unreadable files), it must report `architecture_valid: false`, never omit the report |
| No source_snapshot mutation | `AI_FAILURE_PROTOCOL.md §1A` | Validator is read-only. It must never write to `logos_analysis/source_snapshot/` |
| Four-layer separation | `CLAUDE_OPERATIONAL_CONSTRAINTS.md §7` | Validation report must not conflate conceptual completeness with spec completeness |
| Deferment obedience | `CLAUDE_GOVERNANCE_PROTOCOL.md §8` | DRAC and all deferred subsystems must be excluded from active validation scope |
| Phase constraint | `CLAUDE_PHASE_PARTICIPATION.md §2` | Spec campaign active; validator is in scope for Phase 2 specification |

---

## Functional Requirements

| ID | Requirement | Source | Testable |
|---|---|---|---|
| FR-001 | Validator reads the canonical module registry from the source Design Specification and builds an expected module set | AP_MASTER_SPEC_V2_SCHEMA.json §8 | Yes |
| FR-002 | Validator scans all directories classified as `runtime_surface` in the source Design Specification and builds an actual module set | AP_MASTER_SPEC_V2_SCHEMA.json §11 | Yes |
| FR-003 | Validator computes set difference: registry modules absent from repo (missing_spec_modules) | FR-001, FR-002 | Yes |
| FR-004 | Validator computes set difference: repo modules absent from registry (unexpected_modules) | FR-001, FR-002 | Yes |
| FR-005 | Validator checks every repo module for presence of a header block at file top | AP_MASTER_SPEC_V2_SCHEMA.json §13 | Yes |
| FR-006 | Validator checks every header block for presence of all 13 required fields | AP_MASTER_SPEC_V2_SCHEMA.json §13.1 | Yes |
| FR-007 | Validator checks all `must_match_registry: true` header fields against registry values; reports mismatches | AP_MASTER_SPEC_V2_SCHEMA.json §13.1 | Yes |
| FR-008 | Validator checks every module's `canonical_path` in the registry against its actual filesystem path | AP_MASTER_SPEC_V2_SCHEMA.json §9 IC-002 | Yes |
| FR-009 | Validator checks every module's declared imports against `allowed_imports` and `forbidden_imports` in the subsystem contract | AP_MASTER_SPEC_V2_SCHEMA.json §10 | Yes |
| FR-010 | Validator checks that no module's header `subsystem` value conflicts with its registry subsystem assignment | AP_MASTER_SPEC_V2_SCHEMA.json §9 IC-003 | Yes |
| FR-011 | Validator checks that no runtime code exists in non-runtime surface directories | AP_MASTER_SPEC_V2_SCHEMA.json §11 | Yes |
| FR-012 | Validator checks that no design/audit/export artifacts exist in runtime surface directories | AP_MASTER_SPEC_V2_SCHEMA.json §11 | Yes |
| FR-013 | Validator writes a complete `architecture_validation_report.json` to the audit surface path declared in the spec | AP_MASTER_SPEC_V2_SCHEMA.json §14.3 | Yes |
| FR-014 | Validator sets `architecture_valid: true` only when all eight check categories return zero findings | All FR | Yes |
| FR-015 | Validator sets `architecture_valid: false` and completes its full scan when any check returns findings — it does not halt on first error | Fail-closed principle | Yes |
| FR-016 | Validator accepts the path to a Design Specification's module registry and surface definitions as runtime input; it is not hardcoded to a single spec | Generality requirement | Yes |
| FR-017 | Validator excludes all modules in subsystems marked as deferred in the active spec | CLAUDE_GOVERNANCE_PROTOCOL.md §8 | Yes |
| FR-018 | Validator run duration is logged to the validation report | Auditability | Yes |

---

## Constraints

| ID | Constraint | Rationale | Enforcement Mechanism |
|---|---|---|---|
| C-001 | Validator is read-only. It must never write any file other than the designated output report | Source snapshot protection; no side effects | Module-level write interception; CIH header declares mutation_policy: NONE |
| C-002 | Validator must not halt on a single check failure; it must complete all checks before reporting | Partial reports produce false-pass impressions | Error accumulation pattern — all checks run; exceptions are caught per check and appended to findings |
| C-003 | Validator output path must come from the spec's `architecture_validation_gate.validator_module.output_artifact` field — never hardcoded | Hardcoded paths break multi-spec operation | Path injected at call time via CLI argument or config |
| C-004 | Validator must not scan `logos_analysis/source_snapshot/` directly — it scans the registry-declared runtime surface paths only | Source snapshot separation | Explicit path exclusion list in startup validation |
| C-005 | If the canonical module registry is unavailable or unreadable, validator must report `architecture_valid: false` with a single `REGISTRY_UNAVAILABLE` finding rather than raising an unhandled exception | Fail-closed behavior on missing inputs | Try/except around registry load with structured error report |
| C-006 | Deferred subsystems (DRAC and any others declared in the active spec's `deferments` section) must be excluded from the expected module set before computing missing_spec_modules | Deferment obedience | Pre-scan deferment filter applied to registry before set comparison |
| C-007 | Validator must be invocable from the command line with a single command: `python validate_architecture.py --spec [SPEC-NNNN] --registry [path] --output [path]` | GPT/VS Code consumption requirement | CLI argument parser required |
| C-008 | The validation report schema must match the `architecture_validation_gate.validator_module.validation_checks` contract declared in the Implementation Guide that references this validator | Schema contract | Report schema is frozen in this spec (Section: Validation Report Schema) |

---

## Formal Model

### Primitives

```
M_registry  = finite set of module descriptors declared in the canonical registry
M_repo      = finite set of modules found on the runtime surface of the filesystem
H(m)        = header block extracted from module m ∈ M_repo
F_required  = ordered set of 13 required header fields
S(sub)      = subsystem contract for subsystem sub
D           = set of deferred subsystems declared in the active spec
```

### Operations

```
expected(registry, D) = { m ∈ M_registry | m.subsystem ∉ D }
  -- builds expected module set, excluding deferred subsystems

actual(surface_paths)  = { m | m exists at a path under any declared runtime surface path }
  -- builds actual module set from filesystem scan

missing(E, A)          = E \ A
  -- modules in expected set absent from actual set

unexpected(E, A)       = A \ E
  -- modules in actual set absent from expected set

misplaced(E, A)        = { m ∈ E ∩ A | m.canonical_path ≠ m.actual_path }
  -- modules present in both sets but at wrong path

header_violations(A)   = { (m, field_errors) | m ∈ A, header_check(m) returns errors }
  -- header check: presence, completeness, registry match, enum validity

import_violations(A, S) = { (m, import_errors) | m ∈ A, import_check(m, S(m.subsystem)) returns errors }
  -- import check: declared imports vs. allowed/forbidden in subsystem contract

surface_violations(A, surfaces) = { m | m ∈ A, m.path ∈ non_runtime_surface(surfaces) }
  -- modules in wrong surface
```

### Axioms

```
A1: architecture_valid = true ⟺
    |missing(E,A)| = 0 ∧
    |unexpected(E,A)| = 0 ∧
    |misplaced(E,A)| = 0 ∧
    |header_violations(A)| = 0 ∧
    |import_violations(A,S)| = 0 ∧
    |surface_violations(A,surfaces)| = 0

A2: ∀ m ∈ expected(registry, D): m.subsystem ∉ D
  -- deferred modules are never in expected set

A3: validator completes all checks before setting architecture_valid
  -- no early exit on first failure

A4: output report is written ⟺ validator execution completes (including failure paths)
  -- fail-closed: report always produced
```

### Properties

- **Completeness:** Every module in scope is checked against every applicable rule. No module is skipped silently.
- **Monotonicity:** Adding a finding never removes another finding. Finding accumulation is append-only.
- **Determinism:** For the same registry and filesystem state, the validator always produces the same report.
- **Idempotence:** Running the validator twice with no repo changes produces identical reports.

---

## Validation Report Schema

This schema is frozen. GPT-derived prompts and Claude's `CLAUDE_VALIDATION_REPORT_PROTOCOL.md` both depend on it. Changes to this schema require a new spec version and Architect authorization.

```json
{
  "schema_version": "1.0",
  "spec_reference": "SPEC-004",
  "registry_reference": "[SPEC-NNNN.section.8]",
  "validation_timestamp": "<ISO8601>",
  "run_duration_seconds": "<float>",
  "summary": {
    "modules_scanned": "<int>",
    "registry_modules": "<int>",
    "deferred_modules_excluded": "<int>",
    "missing_spec_modules": "<int>",
    "unexpected_modules": "<int>",
    "misplaced_modules": "<int>",
    "header_schema_violations": "<int>",
    "import_rule_violations": "<int>",
    "subsystem_boundary_violations": "<int>",
    "artifact_surface_violations": "<int>"
  },
  "missing_spec_modules": [
    {
      "module_id": "<str>",
      "module_name": "<str>",
      "canonical_path": "<str>",
      "subsystem": "<str>",
      "implementation_phase": "<str>"
    }
  ],
  "unexpected_modules": [
    {
      "actual_path": "<str>",
      "filename": "<str>",
      "surface": "<str>",
      "closest_registry_match": "<str | null>",
      "classification_candidate": "<ANALOG_IMPLEMENTATION | ENHANCEMENT_MODULE | LEGACY_MODULE | UNKNOWN_MODULE>"
    }
  ],
  "misplaced_modules": [
    {
      "module_id": "<str>",
      "module_name": "<str>",
      "canonical_path": "<str>",
      "actual_path": "<str>"
    }
  ],
  "header_schema_violations": [
    {
      "module_name": "<str>",
      "actual_path": "<str>",
      "violation_type": "<MISSING_HEADER | MISSING_FIELDS | REGISTRY_MISMATCH | INVALID_ENUM>",
      "missing_fields": ["<field_name>"],
      "mismatched_fields": [
        {
          "field": "<str>",
          "expected": "<str>",
          "actual": "<str>"
        }
      ]
    }
  ],
  "import_rule_violations": [
    {
      "module_name": "<str>",
      "actual_path": "<str>",
      "violation_type": "<FORBIDDEN_IMPORT | UNDECLARED_IMPORT>",
      "violating_import": "<str>",
      "subsystem_contract_ref": "<str>"
    }
  ],
  "subsystem_boundary_violations": [
    {
      "module_name": "<str>",
      "actual_path": "<str>",
      "declared_subsystem": "<str>",
      "registry_subsystem": "<str>"
    }
  ],
  "artifact_surface_violations": [
    {
      "path": "<str>",
      "filename": "<str>",
      "actual_surface": "<str>",
      "correct_surface": "<str>",
      "violation_type": "<RUNTIME_IN_NON_RUNTIME | NON_RUNTIME_IN_RUNTIME>"
    }
  ],
  "architecture_valid": "<bool>",
  "gate_decision": "<PASS | FAIL>",
  "blocking_findings": "<int>"
}
```

---

## Canonical Architecture Definition

| Path | Subsystem | Surface | Allowed File Types |
|---|---|---|---|
| `ARCHON_PRIME/tools/validation/` | AP_Validation | runtime_surface | `.py` |
| `ARCHON_PRIME/sources/validation_reports/` | AP_Validation | audit_surface | `.json` |
| `ARCHON_PRIME/AP_SYSTEM_CONFIG/schemas/` | AP_Config | design_surface | `.json` |

### Placement Rules

| Rule ID | Rule |
|---|---|
| PR-001 | `validate_architecture.py` must reside in `ARCHON_PRIME/tools/validation/` |
| PR-002 | All output reports must be written to `ARCHON_PRIME/sources/validation_reports/` |
| PR-003 | No configuration files, schemas, or design artifacts may reside in `ARCHON_PRIME/tools/validation/` |

---

## Canonical Module Registry

**Registry Mode:** inline

| Module ID | Module Name | Canonical Path | Subsystem | Responsibility | Runtime Stage | Implementation Phase |
|---|---|---|---|---|---|---|
| M-VAL-01 | validate_architecture | `ARCHON_PRIME/tools/validation/validate_architecture.py` | AP_Validation | Execute full architecture validation scan and produce validation report | validation | PHASE_2 |

**Imports Allowed:** `os`, `sys`, `json`, `pathlib`, `argparse`, `datetime`, `dataclasses`, `typing`, `re`

**Imports Forbidden:** Any LOGOS runtime module; any module that performs file writes other than the designated output path; `logos_analysis.source_snapshot.*`

---

## Module Identity Rules

| Rule ID | Validity Condition | Enforcement Point |
|---|---|---|
| IC-001 | `filename == "validate_architecture.py"` | pre_scan_identity_check |
| IC-002 | `path == "ARCHON_PRIME/tools/validation/validate_architecture.py"` | pre_scan_identity_check |
| IC-003 | `header.module_id == "M-VAL-01"` | header_validation_check |

**Violation Classification:** Any module failing IC-001 or IC-002 is classified as `MISPLACED_MODULE`. Any module failing IC-003 is classified as `HEADER_SCHEMA_VIOLATION`.

---

## Subsystem Contracts

| Field | Value |
|---|---|
| Subsystem ID | AP_Validation |
| Subsystem Name | Architecture Validation Subsystem |
| Runtime Role | Scan repository state and produce architecture_validation_report.json |
| Controller Role | No |
| Allowed Modules | M-VAL-01 |
| Allowed Imports | Standard library only (os, sys, json, pathlib, argparse, datetime, dataclasses, typing, re) |
| Forbidden Cross-Imports | All LOGOS runtime modules; all other AP subsystem modules during validation execution |

---

## Artifact Surface Definition

| Surface ID | Surface Name | Directories | Runtime Code Permitted |
|---|---|---|---|
| S-01 | runtime_surface | `ARCHON_PRIME/tools/validation/` | Yes |
| S-02 | audit_surface | `ARCHON_PRIME/sources/validation_reports/` | No |
| S-03 | design_surface | `ARCHON_PRIME/AP_SYSTEM_CONFIG/schemas/` | No |

**Isolation Rules:**
- No `.json` report files may reside in `runtime_surface`
- No `.py` module files may reside in `audit_surface`
- Crossing surface boundaries without Architect authorization is an artifact_surface_violation

---

## Module Classification Types

| Label | Disposition | Architect Review Required |
|---|---|---|
| SPEC_REQUIRED | Expected in repo; generates missing_spec_modules finding if absent | No |
| SPEC_PRESENT | In registry and found at canonical path; passes all checks | No |
| SPEC_MISSING | In registry but absent from runtime surface | Yes |
| ANALOG_IMPLEMENTATION | Present in runtime surface, not in registry, structurally corresponds to a spec module | Yes |
| ENHANCEMENT_MODULE | Present in runtime surface, not in registry, implements non-spec functionality | Yes |
| LEGACY_MODULE | Present in runtime surface, no clear current role | Yes |
| UNKNOWN_MODULE | Present in runtime surface, cannot be classified | Yes — immediate escalation |

---

## Header Schema Definition

**Required Fields (13):**

| Field | Type | Must Match Registry | Description |
|---|---|---|---|
| module_id | string | Yes | Canonical module ID (M-VAL-01) |
| module_name | string | Yes | Filename without extension |
| subsystem | string | Yes | Subsystem name (AP_Validation) |
| canonical_path | string | Yes | Full path from repo root |
| responsibility | string | No | One-sentence functional description |
| runtime_stage | enum | No | `validation` |
| allowed_imports | list | No | Standard library modules |
| forbidden_imports | list | No | LOGOS runtime modules; other AP modules |
| spec_reference | string | No | `SPEC-004.section.8` |
| implementation_phase | string | No | `PHASE_2` |
| authoring_authority | string | No | `ARCHON_PRIME` |
| version | string | No | Semver `N.N` |
| status | enum | No | `canonical`, `draft`, or `deprecated` |

**Header Format:**
```
# ARCHON PRIME MODULE HEADER
# module_id: M-VAL-01
# module_name: validate_architecture
# subsystem: AP_Validation
# canonical_path: ARCHON_PRIME/tools/validation/validate_architecture.py
# responsibility: Execute full architecture validation scan and produce validation report
# runtime_stage: validation
# allowed_imports: [os, sys, json, pathlib, argparse, datetime, dataclasses, typing, re]
# forbidden_imports: [logos_analysis.source_snapshot.*, all LOGOS runtime modules]
# spec_reference: SPEC-004.section.8
# implementation_phase: PHASE_2
# authoring_authority: ARCHON_PRIME
# version: 1.0
# status: canonical
```

**Header Placement:** File top, before all imports.

**Header Validation Rules:**

| Rule ID | Rule |
|---|---|
| HVR-001 | Header block must be present as the first content block in the file |
| HVR-002 | All 13 fields must be present; missing fields are violations |
| HVR-003 | `module_id`, `module_name`, `subsystem`, `canonical_path` must exactly match registry values |
| HVR-004 | `runtime_stage` must be one of the declared enum values: `initialization`, `analysis`, `processing`, `validation`, `repair`, `audit`, `reporting`, `utility` |

---

## Architecture Validation Rules

| Rule ID | Check | Blocking | Report Field |
|---|---|---|---|
| AVR-001 | Module registry completeness — all registry modules (minus deferred) are present in runtime surface | Yes | missing_spec_modules |
| AVR-002 | No unexpected modules in runtime surface | Yes | unexpected_modules |
| AVR-003 | All modules reside at canonical paths | Yes | misplaced_modules |
| AVR-004 | All modules carry a valid header block | Yes | header_schema_violations |
| AVR-005 | All header fields present and registry-match fields correct | Yes | header_schema_violations |
| AVR-006 | No forbidden imports present in any module | Yes | import_rule_violations |
| AVR-007 | No subsystem boundary violations (header subsystem matches registry) | Yes | subsystem_boundary_violations |
| AVR-008 | No runtime code in non-runtime surface directories | Yes | artifact_surface_violations |

**Validation Gate Conditions:**

| Stage | Gate Condition |
|---|---|
| module_generation | architecture_valid == true |
| enhancement_integration | architecture_valid == true |
| release_build | architecture_valid == true |
| repository_packaging | architecture_valid == true |
| spec_update | architecture_valid == true |

---

## Governance Rules

**Non-Deletion Policy:** `validate_architecture.py` may not be deleted from the repository without Architect authorization. Deletion of the validator while gated pipeline stages exist is a governance violation (Category C: Governance Conflict).

**Override Mechanism:** Architect may authorize a one-time skip of the validation gate by providing explicit written instruction in the session. The skip must be logged.

**Spec Change Process:** Any change to the validation report schema (Section: Validation Report Schema) requires a new spec version. Schema changes are not compatible with prior versions of `CLAUDE_VALIDATION_REPORT_PROTOCOL.md` — both must be updated together.

**Enhancement Proposal Process:** Enhancements to the validator (additional checks, new report fields) must follow the full enhancement lifecycle. **Blocking rule:** No enhancement may be implemented before updating this spec and its associated Implementation Guide.

---

## Implementation Sequence

| Phase ID | Phase Name | Modules | Entry Condition | Exit Condition | Enhancements Permitted |
|---|---|---|---|---|---|
| PHASE_1 | Core Validator | M-VAL-01 | Spec approved; output path exists | Validator runs without exceptions; produces valid report against known-good fixture | No |

---

## Enhancement Lifecycle

| Stage ID | Stage | Required Output |
|---|---|---|
| EL-001 | proposal | Enhancement proposal document |
| EL-002 | architect_review | Architect decision |
| EL-003 | design_spec_update | Updated SPEC-004 |
| EL-004 | implementation_guide_update | Updated IMPL-004 |
| EL-005 | implementation | Implementation in repo |

**Pre-Implementation Gate:** Spec updated AND approved; Implementation Guide updated AND approved; prior validation pass confirms no existing violations.

**Bypass Rule:** Not bypassable.

---

## Integration Surfaces

| Adjacent Subsystem | Interface Type | Data Flow |
|---|---|---|
| AP_Config / canonical module registry | Input — file read | Registry consumed at scan start; not modified |
| AP_Config / Design Specification §11 surface definitions | Input — file read | Surface directories read at scan start |
| AP_Validation_Reports / `architecture_validation_report.json` | Output — file write | Report written to audit surface; consumed by Claude (CLAUDE_VALIDATION_REPORT_PROTOCOL.md) and pipeline gate logic |
| ARCHON_PRIME pipeline orchestrator | Invocation | Called at each gated stage; returns exit code 0 (architecture_valid: true) or 1 (architecture_valid: false) |

---

## Verification Criteria

| ID | Criterion | Method | Automated |
|---|---|---|---|
| V-001 | Validator detects a missing registry module when one is removed from the runtime surface | Unit test: remove a test module, run validator, assert module appears in missing_spec_modules | Yes |
| V-002 | Validator detects an unexpected module when one is added to the runtime surface without a registry entry | Unit test: add an unregistered test file, run validator, assert it appears in unexpected_modules | Yes |
| V-003 | Validator detects a header violation on a module with a missing or incorrect header | Unit test: corrupt a header field, run validator, assert violation appears in header_schema_violations | Yes |
| V-004 | Validator detects a forbidden import | Unit test: add a forbidden import to a test module, run validator, assert violation appears in import_rule_violations | Yes |
| V-005 | Validator sets `architecture_valid: false` when any finding exists | Integration test: introduce a single finding of each type; assert architecture_valid is false for each | Yes |
| V-006 | Validator sets `architecture_valid: true` on a clean registry/repo state | Integration test: clean fixture; assert architecture_valid: true and all finding arrays empty | Yes |
| V-007 | Validator does not halt on first error; all checks complete regardless of intermediate failures | Unit test: introduce multiple violations simultaneously; assert all appear in report | Yes |
| V-008 | Validator excludes deferred subsystems from missing_spec_modules | Unit test: mark a subsystem as deferred; remove its modules; assert no missing_spec_modules finding for those modules | Yes |
| V-009 | Validator does not write to logos_analysis/source_snapshot/ | Integration test: run validator; assert no files were written to source_snapshot/ | Yes |
| V-010 | Validator produces a report whose schema matches the frozen schema in this spec | Integration test: run validator; validate output against SPEC-004 report schema definition | Yes |

---

## Deferments

| Item | Reason | Deferred To |
|---|---|---|
| Multi-spec registry merge (validating across multiple Design Specifications simultaneously) | Out of scope for single-module implementation; requires registry federation design | Future SPEC-004 enhancement cycle |
| Incremental validation (only scanning changed files) | Optimization; correctness of full scan is prerequisite | Post-Phase 1 enhancement |
| Integration with CI/CD gate (GitHub Actions invocation) | Infrastructure concern; not a module design concern | AP_SYSTEM_CONFIG phase |

---

## Open Questions

| ID | Question | Blocking | Recommendation |
|---|---|---|---|
| OQ-001 | Should `validate_architecture.py` also validate JSON schema files in the design surface (e.g., verify `AP_MASTER_SPEC_V2_SCHEMA.json` is syntactically valid JSON Schema)? | No | Defer to enhancement cycle; out of scope for architecture validation |
| OQ-002 | Should the validator produce an exit code that distinguishes "blocking findings" from "no findings" vs. "non-blocking findings only"? | No | Recommend: exit code 0 = clean; exit code 1 = blocking findings; exit code 2 = non-blocking findings only. Architect to confirm. |

---

## Revision History

| Version | Date | Change | Author |
|---|---|---|---|
| v1 | 2026-03-09 | Initial specification | Claude / Formalization_Expert |

---

## End of Specification
