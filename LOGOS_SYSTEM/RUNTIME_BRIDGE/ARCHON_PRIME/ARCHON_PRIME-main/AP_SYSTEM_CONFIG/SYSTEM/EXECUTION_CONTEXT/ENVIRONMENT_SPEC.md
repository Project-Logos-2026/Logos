SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: Environment_Specification
ARTIFACT_NAME: ENVIRONMENT_SPEC
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Context
STATUS: Canonical

---------------------------------------------------------------------

# ARCHON_PRIME — CANONICAL ENVIRONMENT SPECIFICATION

**Version:** 1.0
**Date:** 2026-03-12
**Status:** AUTHORITATIVE — Runtime Environment Contract

This document defines the canonical runtime environment contract required
for all Archon Prime execution operations. All tooling, crawlers, and
execution agents must conform to the definitions herein.

---------------------------------------------------------------------

## SECTION 1 — RUNTIME ROOT VARIABLES

The following environment variables define the canonical filesystem
anchors for the Archon Prime execution environment.

These variables must be established prior to any pipeline execution.
They are the authoritative source for all path resolution within the
system.

### Canonical Variable Definitions

| Variable                 | Required | Description                                             |
|--------------------------|----------|---------------------------------------------------------|
| `AP_ROOT`                | YES      | Absolute path to the ARCHON_PRIME repository root       |
| `AP_SYSTEM_CONFIG`       | YES      | Absolute path to the system configuration layer         |
| `AP_WORKFLOW_ROOT`       | YES      | Absolute path to the workflow mutation tooling root     |
| `AP_EXECUTION_ENVELOPES` | YES      | Absolute path to the active execution envelope directory|
| `AP_REPORTS`             | YES      | Absolute path to the runtime report output root         |
| `AP_TOOLING_ROOT`        | YES      | Absolute path to the workflow mutation tooling modules  |

### Canonical Variable Values

```
AP_ROOT                = /workspaces/ARCHON_PRIME
AP_SYSTEM_CONFIG       = $AP_ROOT/AP_SYSTEM_CONFIG/SYSTEM
AP_WORKFLOW_ROOT       = $AP_ROOT/WORKFLOW_MUTATION_TOOLING
AP_EXECUTION_ENVELOPES = $AP_ROOT/WORKFLOW_EXECUTION_ENVELOPES/ACTIVE_TARGET
AP_REPORTS             = $AP_ROOT/WORKFLOW_TARGET_PROCESSING/PROCESSING_REPORTS
AP_TOOLING_ROOT        = $AP_ROOT/WORKFLOW_MUTATION_TOOLING
```

### Variable Derivation Rules

1. `AP_ROOT` must be set explicitly. It is the sole manually-configured anchor.
2. All other variables must be derived from `AP_ROOT` using the canonical
   relative offsets defined above.
3. No tooling module may hardcode absolute paths. All paths must resolve
   through these variables.
4. Environment variables must be available to all subprocess invocations.

---------------------------------------------------------------------

## SECTION 2 — DIRECTORY EXPECTATIONS

The following directories must exist and be accessible at runtime.
The system is not considered operational if any required directory is absent.

### System Configuration

| Directory                                        | Required | Purpose                               |
|--------------------------------------------------|----------|---------------------------------------|
| `$AP_SYSTEM_CONFIG`                              | YES      | SYSTEM config root                    |
| `$AP_SYSTEM_CONFIG/EXECUTION_CONTEXT`            | YES      | Runtime contracts and specs           |
| `$AP_SYSTEM_CONFIG/EXECUTION_ENVELOPES`          | YES      | Envelope governance configuration     |
| `$AP_SYSTEM_CONFIG/GOVERNANCE`                   | YES      | Pipeline runtime governance           |
| `$AP_SYSTEM_CONFIG/WORKFLOW`                     | YES      | Pipeline phase model definitions      |
| `$AP_SYSTEM_CONFIG/SCHEMAS`                      | YES      | Header and schema policy registries   |
| `$AP_SYSTEM_CONFIG/CONFIG`                       | YES      | Platform configuration references     |
| `$AP_SYSTEM_CONFIG/DESIGN_SPEC`                  | YES      | Master system design specification    |
| `$AP_SYSTEM_CONFIG/REPORTS/STRUCTURE`            | YES      | Audit and report outputs              |

### Execution Envelopes

| Directory                                              | Required | Purpose                                |
|--------------------------------------------------------|----------|----------------------------------------|
| `$AP_EXECUTION_ENVELOPES`                              | YES      | Active target envelope directory       |
| `$AP_ROOT/WORKFLOW_EXECUTION_ENVELOPES/INCOMING_TARGETS` | YES    | Incoming workflow targets              |

### Workflow Tooling

| Directory                             | Required | Purpose                                        |
|---------------------------------------|----------|------------------------------------------------|
| `$AP_TOOLING_ROOT`                    | YES      | Root of all workflow mutation tooling          |
| `$AP_TOOLING_ROOT/controllers`        | YES      | Pipeline execution controllers                 |
| `$AP_TOOLING_ROOT/crawler`            | YES      | Crawler subsystem modules                      |
| `$AP_TOOLING_ROOT/simulation`         | YES      | Simulation framework                           |
| `$AP_TOOLING_ROOT/repair`             | YES      | Repair subsystem                               |
| `$AP_TOOLING_ROOT/utils`              | YES      | Shared utility modules                         |

### Audit Artifacts

| Directory                                | Required | Purpose                                     |
|------------------------------------------|----------|---------------------------------------------|
| `$AP_ROOT/AP_SYSTEM_AUDIT`               | YES      | Audit scan results and reports              |
| `$AP_ROOT/WORKFLOW_TARGET_AUDITS`        | YES      | Per-target audit logs and modules           |
| `$AP_ROOT/WORKFLOW_TARGET_PROCESSING`    | YES      | Processing outputs and completion logs      |

### Processing Outputs

| Directory                                         | Required | Purpose                               |
|---------------------------------------------------|----------|---------------------------------------|
| `$AP_REPORTS`                                     | YES      | Reports written during execution      |
| `$AP_ROOT/WORKFLOW_TARGET_PROCESSING/COMPLETED`   | YES      | Completed envelope archives           |
| `$AP_ROOT/WORKFLOW_TARGET_PROCESSING/PROCESSING`  | YES      | In-progress processing workspace      |

---------------------------------------------------------------------

## SECTION 3 — RUNTIME EXECUTION REQUIREMENTS

### Python Runtime

| Requirement           | Specification                                |
|-----------------------|----------------------------------------------|
| Python version        | 3.10 or higher                               |
| Interpreter           | CPython (system or virtual environment)      |
| Package manager       | pip (pip3)                                   |
| Execution mode        | Module-level invocation via `python3 <file>` |
| Import resolution     | Must resolve from `$AP_ROOT` as package root |

### Filesystem Assumptions

1. All directories listed in Section 2 must exist before execution begins.
2. The filesystem must support read/write access to `$AP_ROOT`.
3. File paths must use POSIX separators (`/`) regardless of platform.
4. File names are case-sensitive and must match declared artifact names exactly.
5. No symlink aliasing of canonical directories is permitted.
6. The execution agent must have permission to create files under `$AP_REPORTS`.

### Execution Environment Assumptions

1. The execution agent is GitHub Copilot in VS Code (or an equivalent agent
   conforming to the VS Code Envelope Loader Spec).
2. Only one active execution envelope exists at a time under `$AP_EXECUTION_ENVELOPES`.
3. A valid `ENVELOPE_MANIFEST.json` must be present in `$AP_EXECUTION_ENVELOPES`
   before any execution phase begins.
4. Simulation mode must be executed and validated before any mutation phase.
5. The pipeline must follow the phase model defined in
   `$AP_SYSTEM_CONFIG/WORKFLOW/AP_PIPELINE_PHASE_MODEL.md`.

---------------------------------------------------------------------

## SECTION 4 — ARTIFACT ROUTING REQUIREMENTS

All runtime artifacts produced during execution must be written to
designated locations. Arbitrary write locations are prohibited.

### Routing Table

| Artifact Type              | Required Write Location                                       |
|----------------------------|---------------------------------------------------------------|
| Processing reports         | `$AP_REPORTS/`                                                |
| Simulation reports         | `$AP_REPORTS/simulation/` or `$AP_REPORTS/`                   |
| Audit reports (structure)  | `$AP_SYSTEM_CONFIG/REPORTS/STRUCTURE/`                        |
| Target audit logs          | `$AP_ROOT/WORKFLOW_TARGET_AUDITS/AUDIT_LOGS/`                 |
| Completed envelope archive | `$AP_ROOT/WORKFLOW_TARGET_PROCESSING/COMPLETED/`              |
| Completion logs            | `$AP_ROOT/WORKFLOW_TARGET_PROCESSING/COMPLETION_LOGS/`        |
| Crawler outputs            | `$AP_ROOT/AP_SYSTEM_AUDIT/CRAWLER_OUTPUTS/`                   |

### Routing Contract Reference

The full artifact routing contract is defined in:
```
$AP_SYSTEM_CONFIG/EXECUTION_CONTEXT/ARTIFACT_ROUTER_CONTRACT.md
```

All tooling must consult this contract before determining write targets.

---------------------------------------------------------------------

## SECTION 5 — GOVERNANCE CONSTRAINTS

Execution is governed by the following canonical documents. Tooling must
not contradict or override these without Architect authorization.

| Document                                                     | Scope                                      |
|--------------------------------------------------------------|--------------------------------------------|
| `EXECUTION_CONTEXT/EXECUTION_ENVIRONMENT.md`                 | Runtime environment baseline               |
| `GOVERNANCE/AP_PIPELINE_RUNTIME_CONTRACT.md`                 | Platform runtime responsibilities          |
| `GOVERNANCE/AP_EXECUTION_STATE_MACHINE.md`                   | Legal execution state transitions          |
| `WORKFLOW/AP_PIPELINE_PHASE_MODEL.md`                        | Canonical phase ordering                   |
| `EXECUTION_ENVELOPES/EA_CONFIG/EA-001_ENVELOPE_TARGET_INTEGRITY.md` | Envelope target integrity rule      |
| `EXECUTION_ENVELOPES/EA_CONFIG/EA-004_SIMULATION_FIRST_RULE.md`     | Simulation-before-mutation rule     |
| `EXECUTION_ENVELOPES/EA_CONFIG/EA-008_ENVELOPE_MANIFEST_CONTRACT.md` | Manifest structure contract        |
| `EXECUTION_ENVELOPES/EA_CONFIG/EA-010_FAILURE_ROLLBACK_PROTOCOL.md` | Rollback protocol on failure       |

### Key Governance Rules

1. **Simulation-first:** No mutation may occur before simulation pass is complete
   and validated (EA-004).
2. **Envelope integrity:** The active envelope must remain unmodified after
   the execution agent loads it (EA-001).
3. **Manifest contract:** ENVELOPE_MANIFEST.json must conform to the schema
   defined in EA-008 and EE_SCHEMAS.
4. **Rollback on failure:** Any unrecoverable execution failure must trigger
   the rollback protocol in EA-010.
5. **Artifact routing:** All writes must pass through the artifact router
   defined in EA-002 and ARTIFACT_ROUTER_CONTRACT.md.

---------------------------------------------------------------------

## SECTION 6 — VALIDATION REQUIREMENTS

Environment compliance can be verified by checking the following conditions.
The companion `ENVIRONMENT_VALIDATION_CHECKLIST.md` provides a
machine-readable checklist for tooling use.

### Validation Criteria

| Criterion                                | Validation Method                                          |
|------------------------------------------|------------------------------------------------------------|
| AP_ROOT resolves to repo root            | Check `$AP_ROOT/pyproject.toml` exists                     |
| All required directories exist           | Check each directory listed in Section 2                   |
| Python 3.10+ available                   | `python3 --version` >= 3.10                               |
| ENVELOPE_MANIFEST.json valid             | Parse JSON and verify `addendum`, `artifact_bundle` keys   |
| Manifest paths resolve                   | Check each path in `artifact_bundle` and `addendum`       |
| Manifest hashes match                    | Compute SHA-256 for each artifact_bundle file              |
| All SYSTEM/ .md headers complete         | Scan for SYSTEM, ARTIFACT_TYPE, ARTIFACT_NAME, VERSION,    |
|                                          | DATE, AUTHORITY, SUBSYSTEM fields in each file             |
| No `addenda` key in manifest             | Verify manifest JSON does not contain key `"addenda"`      |
| Traceability map present                 | Check EXECUTION_CONTEXT/PROMPT_TO_ARTIFACT_TRACEABILITY_MAP.md |
| Artifact router contract present         | Check EXECUTION_CONTEXT/ARTIFACT_ROUTER_CONTRACT.md        |

### Validation Entry Point

The validation checklist document:
```
$AP_SYSTEM_CONFIG/EXECUTION_CONTEXT/ENVIRONMENT_VALIDATION_CHECKLIST.md
```

---------------------------------------------------------------------

## CHANGE LOG

| Version | Date       | Author     | Change                        |
|---------|------------|------------|-------------------------------|
| 1.0     | 2026-03-12 | Architect  | Initial canonical specification |
