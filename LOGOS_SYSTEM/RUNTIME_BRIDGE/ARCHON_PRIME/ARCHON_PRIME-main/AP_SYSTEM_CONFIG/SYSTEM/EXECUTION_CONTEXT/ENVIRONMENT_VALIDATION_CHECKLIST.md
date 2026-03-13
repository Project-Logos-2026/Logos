SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: Validation_Checklist
ARTIFACT_NAME: ENVIRONMENT_VALIDATION_CHECKLIST
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Context
STATUS: Canonical

---------------------------------------------------------------------

# ARCHON_PRIME — ENVIRONMENT VALIDATION CHECKLIST

**Version:** 1.0
**Date:** 2026-03-12
**Purpose:** Allow tooling and agents to confirm the execution environment
is valid before initiating any pipeline execution.

Reference specification: `EXECUTION_CONTEXT/ENVIRONMENT_SPEC.md`

---------------------------------------------------------------------

## HOW TO USE THIS CHECKLIST

Each item below represents a required environmental condition.
Before executing any pipeline phase, all items marked [REQUIRED] must
be confirmed PASS. Items marked [WARN] represent advisory checks.

Tooling should evaluate each item and report:
- `PASS` — condition satisfied
- `FAIL` — condition not satisfied (blocking)
- `WARN` — condition advisory (non-blocking)
- `SKIP` — check not applicable to current execution mode

Execution must not proceed past the environment verification phase if
any [REQUIRED] item reports FAIL.

---------------------------------------------------------------------

## SECTION A — ROOT VARIABLE CHECKS

| ID    | Priority  | Check Description                                    | Expected Value                                 |
|-------|-----------|------------------------------------------------------|------------------------------------------------|
| A-001 | REQUIRED  | AP_ROOT is set                                       | Non-empty string                               |
| A-002 | REQUIRED  | AP_ROOT resolves to ARCHON_PRIME repo root           | `$AP_ROOT/pyproject.toml` exists               |
| A-003 | REQUIRED  | AP_SYSTEM_CONFIG resolves to SYSTEM/                 | `$AP_SYSTEM_CONFIG/SCHEMAS/HEADER_POLICY_REGISTRY.json` exists |
| A-004 | REQUIRED  | AP_WORKFLOW_ROOT resolves to WORKFLOW_MUTATION_TOOLING/ | `$AP_WORKFLOW_ROOT/controllers/` exists     |
| A-005 | REQUIRED  | AP_EXECUTION_ENVELOPES resolves to ACTIVE_TARGET/    | `$AP_EXECUTION_ENVELOPES/ENVELOPE_MANIFEST.json` exists |
| A-006 | REQUIRED  | AP_REPORTS resolves to PROCESSING_REPORTS/           | Directory is writable                          |
| A-007 | REQUIRED  | AP_TOOLING_ROOT resolves to WORKFLOW_MUTATION_TOOLING/ | `$AP_TOOLING_ROOT/controllers/` exists      |

---------------------------------------------------------------------

## SECTION B — DIRECTORY EXISTENCE CHECKS

| ID    | Priority  | Directory Path                                             |
|-------|-----------|------------------------------------------------------------|
| B-001 | REQUIRED  | `$AP_SYSTEM_CONFIG`                                        |
| B-002 | REQUIRED  | `$AP_SYSTEM_CONFIG/EXECUTION_CONTEXT`                      |
| B-003 | REQUIRED  | `$AP_SYSTEM_CONFIG/EXECUTION_ENVELOPES`                    |
| B-004 | REQUIRED  | `$AP_SYSTEM_CONFIG/GOVERNANCE`                             |
| B-005 | REQUIRED  | `$AP_SYSTEM_CONFIG/WORKFLOW`                               |
| B-006 | REQUIRED  | `$AP_SYSTEM_CONFIG/SCHEMAS`                                |
| B-007 | REQUIRED  | `$AP_SYSTEM_CONFIG/CONFIG`                                 |
| B-008 | REQUIRED  | `$AP_SYSTEM_CONFIG/DESIGN_SPEC`                            |
| B-009 | REQUIRED  | `$AP_SYSTEM_CONFIG/REPORTS/STRUCTURE`                      |
| B-010 | REQUIRED  | `$AP_EXECUTION_ENVELOPES`                                  |
| B-011 | REQUIRED  | `$AP_ROOT/WORKFLOW_EXECUTION_ENVELOPES/INCOMING_TARGETS`   |
| B-012 | REQUIRED  | `$AP_TOOLING_ROOT/controllers`                             |
| B-013 | REQUIRED  | `$AP_TOOLING_ROOT/crawler`                                 |
| B-014 | REQUIRED  | `$AP_TOOLING_ROOT/simulation`                              |
| B-015 | REQUIRED  | `$AP_TOOLING_ROOT/repair`                                  |
| B-016 | REQUIRED  | `$AP_TOOLING_ROOT/utils`                                   |
| B-017 | REQUIRED  | `$AP_ROOT/AP_SYSTEM_AUDIT`                                 |
| B-018 | REQUIRED  | `$AP_ROOT/WORKFLOW_TARGET_AUDITS`                          |
| B-019 | REQUIRED  | `$AP_ROOT/WORKFLOW_TARGET_PROCESSING`                      |
| B-020 | REQUIRED  | `$AP_REPORTS`                                              |
| B-021 | REQUIRED  | `$AP_ROOT/WORKFLOW_TARGET_PROCESSING/COMPLETED`            |
| B-022 | REQUIRED  | `$AP_ROOT/WORKFLOW_TARGET_PROCESSING/PROCESSING`           |

---------------------------------------------------------------------

## SECTION C — PYTHON RUNTIME CHECKS

| ID    | Priority  | Check Description                                      | Expected                   |
|-------|-----------|--------------------------------------------------------|----------------------------|
| C-001 | REQUIRED  | python3 is available on PATH                           | `which python3` returns path |
| C-002 | REQUIRED  | Python version is 3.10 or higher                       | `python3 --version` >= 3.10 |
| C-003 | WARN      | Virtual environment is active                          | `$VIRTUAL_ENV` is set      |
| C-004 | WARN      | pip3 is available                                      | `which pip3` returns path  |

---------------------------------------------------------------------

## SECTION D — ENVELOPE MANIFEST CHECKS

| ID    | Priority  | Check Description                                       |
|-------|-----------|---------------------------------------------------------|
| D-001 | REQUIRED  | `ENVELOPE_MANIFEST.json` exists in ACTIVE_TARGET        |
| D-002 | REQUIRED  | Manifest is valid JSON                                  |
| D-003 | REQUIRED  | Manifest contains `artifact_bundle` key                 |
| D-004 | REQUIRED  | Manifest contains `addendum` key (not `addenda`)        |
| D-005 | REQUIRED  | Manifest does NOT contain `addenda` key                 |
| D-006 | REQUIRED  | `artifact_bundle.design_specification.artifact` file exists |
| D-007 | REQUIRED  | `artifact_bundle.implementation_guide.artifact` file exists |
| D-008 | REQUIRED  | `artifact_bundle.execution_plan.artifact` file exists   |
| D-009 | REQUIRED  | All `addendum` array path entries resolve to existing files |
| D-010 | REQUIRED  | SHA-256 hash of DS artifact matches declared hash       |
| D-011 | REQUIRED  | SHA-256 hash of IG artifact matches declared hash       |
| D-012 | REQUIRED  | SHA-256 hash of EP artifact matches declared hash       |

---------------------------------------------------------------------

## SECTION E — HEADER COMPLIANCE CHECKS

| ID    | Priority  | Check Description                                             |
|-------|-----------|---------------------------------------------------------------|
| E-001 | REQUIRED  | All `.md` files under `$AP_SYSTEM_CONFIG` contain `SYSTEM:`  |
| E-002 | REQUIRED  | All `.md` files under `$AP_SYSTEM_CONFIG` contain `ARTIFACT_TYPE:` |
| E-003 | REQUIRED  | All `.md` files under `$AP_SYSTEM_CONFIG` contain `ARTIFACT_NAME:` |
| E-004 | REQUIRED  | All `.md` files under `$AP_SYSTEM_CONFIG` contain `VERSION:` |
| E-005 | REQUIRED  | All `.md` files under `$AP_SYSTEM_CONFIG` contain `DATE:`    |
| E-006 | REQUIRED  | All `.md` files under `$AP_SYSTEM_CONFIG` contain `AUTHORITY:` |
| E-007 | REQUIRED  | All `.md` files under `$AP_SYSTEM_CONFIG` contain `SUBSYSTEM:` |

---------------------------------------------------------------------

## SECTION F — GOVERNANCE ARTIFACT CHECKS

| ID    | Priority  | Artifact                                                     |
|-------|-----------|--------------------------------------------------------------|
| F-001 | REQUIRED  | `EXECUTION_CONTEXT/ENVIRONMENT_SPEC.md` exists               |
| F-002 | REQUIRED  | `EXECUTION_CONTEXT/ARTIFACT_ROUTER_CONTRACT.md` exists       |
| F-003 | REQUIRED  | `EXECUTION_CONTEXT/EXECUTION_ENVIRONMENT.md` exists          |
| F-004 | REQUIRED  | `EXECUTION_CONTEXT/PROMPT_TO_ARTIFACT_TRACEABILITY_MAP.md` exists |
| F-005 | REQUIRED  | `GOVERNANCE/AP_PIPELINE_RUNTIME_CONTRACT.md` exists          |
| F-006 | REQUIRED  | `GOVERNANCE/AP_EXECUTION_STATE_MACHINE.md` exists            |
| F-007 | REQUIRED  | `WORKFLOW/AP_PIPELINE_PHASE_MODEL.md` exists                 |
| F-008 | REQUIRED  | `SCHEMAS/HEADER_POLICY_REGISTRY.json` exists and is valid JSON |
| F-009 | REQUIRED  | `EXECUTION_ENVELOPES/EA_CONFIG/EA-004_SIMULATION_FIRST_RULE.md` exists |
| F-010 | REQUIRED  | `EXECUTION_ENVELOPES/EA_CONFIG/EA-010_FAILURE_ROLLBACK_PROTOCOL.md` exists |

---------------------------------------------------------------------

## SECTION G — PROHIBITED PATTERNS CHECK

| ID    | Priority  | Check Description                                             |
|-------|-----------|---------------------------------------------------------------|
| G-001 | REQUIRED  | No directory named `addenda/` exists under AP_ROOT            |
| G-002 | REQUIRED  | No manifest JSON contains the key `"addenda"`                 |
| G-003 | REQUIRED  | No absolute hardcoded paths in tooling module source files    |

---------------------------------------------------------------------

## VALIDATION SCORING

| Score Threshold | Environment State                                    |
|-----------------|------------------------------------------------------|
| All REQUIRED = PASS | ENVIRONMENT VALID — Proceed with execution       |
| Any REQUIRED = FAIL | ENVIRONMENT INVALID — Block execution, report    |
| Any WARN = FAIL     | ADVISORY — Log warning, may proceed              |

Minimum passing state: 0 FAIL on all REQUIRED checks.

---------------------------------------------------------------------

## VALIDATION LOG FORMAT

When tooling executes this checklist, results must be recorded in the
following format:

```
VALIDATION_RUN:
  timestamp: <ISO-8601>
  environment: <AP_ROOT value>
  results:
    A-001: PASS
    A-002: PASS
    ...
  summary:
    total_checks: <n>
    passed: <n>
    failed: <n>
    warned: <n>
    skipped: <n>
  verdict: PASS | FAIL
```

Validation log artifacts must be written to:
```
$AP_SYSTEM_CONFIG/REPORTS/STRUCTURE/environment_validation_run_<timestamp>.md
```
