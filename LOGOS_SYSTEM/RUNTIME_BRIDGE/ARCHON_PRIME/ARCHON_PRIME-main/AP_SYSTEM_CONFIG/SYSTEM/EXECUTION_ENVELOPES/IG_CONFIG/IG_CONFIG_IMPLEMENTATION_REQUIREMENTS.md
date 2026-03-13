SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: IG_Configuration
ARTIFACT_NAME: IG_CONFIG_IMPLEMENTATION_REQUIREMENTS
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelopes / IG_CONFIG
STATUS: Active

---------------------------------------------------------------------

# IG_CONFIG — Implementation Requirements

## Purpose

This document defines the implementation requirements that all
ARCHON_PRIME Implementation Guide (IG) artifacts must specify for
their associated tooling. An IG that does not address all four
requirement categories defined here is considered incomplete and
must not be used to authorize implementation work.

Implementation requirements govern what tooling must do. Tooling
architecture and code-level conventions are addressed in
IG_CONFIG_TOOLING_REQUIREMENTS.md.

---------------------------------------------------------------------

## REQUIREMENT CATEGORY 1 — MODULE CATEGORIES

### Rule IR-001 — Required Module Category Declaration

**Rule ID:** IR-001
**Category:** Module Structure
**Severity:** CRITICAL
**EA Authority:** EA-007
**Auto-enforceable:** Yes

**Requirement:**
Every IG artifact must declare the complete set of module categories
that the implementation is organized into. All implementations across
all envelopes must cover the following canonical module categories.

**Canonical Module Categories:**

| Category Code | Category Name            | Purpose                                                   |
|---------------|--------------------------|-----------------------------------------------------------|
| MOD-ENV       | Environment Modules      | Initialize and verify the execution environment           |
| MOD-DISC      | Discovery Modules        | Locate and inventory in-scope artifacts                   |
| MOD-ANAL      | Analysis Modules         | Perform structural, dependency, and schema analysis       |
| MOD-SIM       | Simulation Modules       | Execute dry-run simulation of all planned mutations       |
| MOD-VAL       | Validation Modules       | Validate simulation results and post-mutation state       |
| MOD-PLAN      | Planning Modules         | Construct the deterministic mutation plan                 |
| MOD-MUT       | Mutation Modules         | Execute controlled, authorized file system mutations      |
| MOD-ROUTE     | Artifact Router Module   | Route all artifact writes to canonical output paths       |
| MOD-LOG       | Logging Modules          | Produce structured execution logs per EA-006              |
| MOD-REPORT    | Reporting Modules        | Generate execution summary and outcome reports            |
| MOD-ROLL      | Rollback Modules         | Restore pre-mutation state on failure per EA-010          |

**Pass Condition:**
The IG artifact declares all eleven module categories and maps
each category to at least one named implementation module.

**Failure Action:**
`MODULE_CATEGORY_INCOMPLETE`. IG must be revised to cover all
required module categories before implementation proceeds.

---

### Rule IR-002 — Module Category to Phase Alignment

**Rule ID:** IR-002
**Category:** Module Structure
**Severity:** HIGH
**EA Authority:** EA-003
**Auto-enforceable:** Yes

**Requirement:**
Each module category must be mapped to the canonical execution
phase(s) in which it operates, consistent with the Phase Model
defined in EP_CONFIG_PHASE_MODEL.md.

**Expected Mappings:**

| Module Category | Operating Phases            |
|-----------------|-----------------------------|
| MOD-ENV         | PHASE-01                    |
| MOD-DISC        | PHASE-02                    |
| MOD-ANAL        | PHASE-03, PHASE-04          |
| MOD-SIM         | PHASE-05                    |
| MOD-VAL         | PHASE-06, PHASE-09          |
| MOD-PLAN        | PHASE-07                    |
| MOD-MUT         | PHASE-08                    |
| MOD-ROUTE       | PHASE-02, PHASE-08, PHASE-10|
| MOD-LOG         | All phases                  |
| MOD-REPORT      | PHASE-10                    |
| MOD-ROLL        | PHASE-08, PHASE-09 (trigger)|

Modules must not operate in phases outside their mapped range
without explicit justification in the IG.

---

### Rule IR-003 — Prohibited Module Coupling

**Rule ID:** IR-003
**Category:** Module Structure
**Severity:** HIGH
**EA Authority:** EA-003
**Auto-enforceable:** No (design review)

**Requirement:**
The following module couplings are prohibited across all
implementations:

1. MOD-MUT must not directly call MOD-VAL. Validation of
   mutations must be initiated by the pipeline controller,
   not by mutation modules themselves.
2. MOD-SIM must not share state with MOD-MUT. Simulation
   and live mutation contexts must be completely isolated.
3. MOD-ROUTE must not be bypassed by any module. Every
   artifact write must pass through MOD-ROUTE.

**Failure Action:**
`PROHIBITED_MODULE_COUPLING`. Implementation must be redesigned
before the IG may be approved.

---------------------------------------------------------------------

## REQUIREMENT CATEGORY 2 — EXECUTION ENVIRONMENT COMPATIBILITY

### Rule IR-010 — Canonical Environment Declaration

**Rule ID:** IR-010
**Category:** Environment Compatibility
**Severity:** CRITICAL
**EA Authority:** EA-001, EA-005
**Auto-enforceable:** Yes

**Requirement:**
Every IG must declare the canonical execution environment
specification for the tooling it describes. The declaration must
include all of the following:

- Runtime language and version (e.g., Python 3.11+)
- Required external dependencies with minimum versions
- Required ARCHON_PRIME system modules (with canonical paths)
- Filesystem access requirements (read-only vs read-write per path)
- Required environment variables or configuration keys
- Git state requirements (e.g., clean working tree required)

**Pass Condition:**
All six environment declaration fields are present and non-empty
in the IG artifact.

---

### Rule IR-011 — Environment Verification Module Required

**Rule ID:** IR-011
**Category:** Environment Compatibility
**Severity:** CRITICAL
**EA Authority:** EA-001
**Auto-enforceable:** Yes

**Requirement:**
The IG must describe an environment verification module (MOD-ENV)
that is always the first module invoked in the pipeline. The
module must verify:

1. Runtime version meets minimum requirement
2. All required dependencies are importable
3. Required ARCHON_PRIME system modules are present at declared paths
4. Execution context flags are correctly set:
   - `artifact_router_required` → router module is active
   - `simulation_required` → simulation layer is loadable
   - `rollback_enabled` → rollback mechanism is armed
5. All envelope artifact hashes match manifest records (EA-001)

**Pass Condition:**
All five verification checks are described in the IG's MOD-ENV
specification and are mapped to distinct verification steps.

---

### Rule IR-012 — Configuration Loading from Canonical Config Path

**Rule ID:** IR-012
**Category:** Environment Compatibility
**Severity:** HIGH
**EA Authority:** EA-005
**Auto-enforceable:** No (design review)

**Requirement:**
The IG must specify that all tooling configuration is loaded from
the canonical configuration path:

```
AP_SYSTEM_CONFIG/
```

No configuration values may be hardcoded in implementation modules.
Configuration must be sourced from config files under the canonical
path, loaded at initialization time, and validated against their
schemas before use.

---

### Rule IR-013 — Isolation of Simulation from Live Execution Context

**Rule ID:** IR-013
**Category:** Environment Compatibility
**Severity:** CRITICAL
**EA Authority:** EA-004
**Auto-enforceable:** No (design review)

**Requirement:**
The IG must specify that the simulation execution context is
completely isolated from the live mutation execution context.
This requires:

- Separate in-memory or on-disk state for simulation vs live runs
- Simulation writes must target a designated simulation output
  path (not the live artifact targets)
- No file system state from a simulation run may persist into
  a live mutation run without explicit re-initialization

---------------------------------------------------------------------

## REQUIREMENT CATEGORY 3 — LOGGING REQUIREMENTS

### Rule IR-020 — Structured Log Format Required

**Rule ID:** IR-020
**Category:** Logging
**Severity:** CRITICAL
**EA Authority:** EA-006
**Auto-enforceable:** Yes

**Requirement:**
The IG must specify use of a structured log format for all
execution log entries. Each log entry must include the following
fields, consistent with EA-006:

| Field              | Type     | Description                              |
|--------------------|----------|------------------------------------------|
| `timestamp`        | ISO 8601 | UTC timestamp of the log event           |
| `phase`            | string   | Canonical phase code (PHASE-01, etc.)    |
| `artifact_reference` | string | Path or identifier of the artifact       |
| `execution_status` | string   | Status value at time of log event        |
| `event_type`       | string   | Canonical event type (see table below)   |
| `message`          | string   | Human-readable description               |

**Canonical Event Types (EA-006):**

| Event Type                | Phase(s)       |
|---------------------------|----------------|
| `envelope_initialization` | PHASE-01       |
| `environment_verification`| PHASE-01       |
| `artifact_discovery`      | PHASE-02       |
| `simulation_start`        | PHASE-05       |
| `simulation_complete`     | PHASE-05       |
| `mutation_start`          | PHASE-08       |
| `mutation_complete`       | PHASE-08       |
| `validation_start`        | PHASE-06, PHASE-09 |
| `validation_complete`     | PHASE-06, PHASE-09 |
| `envelope_termination`    | PHASE-10       |

---

### Rule IR-021 — Log Output Path Compliance

**Rule ID:** IR-021
**Category:** Logging
**Severity:** HIGH
**EA Authority:** EA-006
**Auto-enforceable:** Yes

**Requirement:**
All execution logs must be written to the canonical log output
path:

```
REPORTS/execution_logs/
```

Log filenames must follow the pattern:

```
<ENVELOPE_NAME>_<PHASE_CODE>_<timestamp>.log
```

Logs must not be written to any other location. All log writes
must be routed through MOD-ROUTE per EA-002.

---

### Rule IR-022 — Log Entry Immutability

**Rule ID:** IR-022
**Category:** Logging
**Severity:** HIGH
**EA Authority:** EA-006
**Auto-enforceable:** No (design review)

**Requirement:**
Log entries must be append-only. Once written, a log entry must
not be modified, overwritten, deleted, or suppressed. Any tooling
that modifies existing log entries is non-compliant.

---

### Rule IR-023 — Rollback Events Must Be Logged

**Rule ID:** IR-023
**Category:** Logging
**Severity:** CRITICAL
**EA Authority:** EA-006, EA-010
**Auto-enforceable:** Yes

**Requirement:**
Any rollback event triggered by MOD-ROLL must produce:
1. A log entry with `event_type: rollback_triggered`
2. A log entry with `event_type: rollback_complete` or
   `event_type: rollback_failed` upon completion
3. A reference to the artifact or operation that triggered rollback

Rollback events must not be silent or suppressed.

---------------------------------------------------------------------

## REQUIREMENT CATEGORY 4 — ARTIFACT ROUTING REQUIREMENTS

### Rule IR-030 — All Writes Must Pass Through the Artifact Router

**Rule ID:** IR-030
**Category:** Artifact Routing
**Severity:** CRITICAL
**EA Authority:** EA-002
**Auto-enforceable:** No (design review)

**Requirement:**
Every artifact write operation performed by any implementation
module must be mediated by the artifact router module (MOD-ROUTE).
Direct filesystem writes using standard file I/O calls that bypass
the router are prohibited. The IG must explicitly document this
constraint and show how the artifact router is invoked for each
write operation category in the pipeline.

---

### Rule IR-031 — Canonical Output Path Declaration

**Rule ID:** IR-031
**Category:** Artifact Routing
**Severity:** HIGH
**EA Authority:** EA-002
**Auto-enforceable:** Yes

**Requirement:**
The IG must declare the canonical output path for every artifact
type produced by the envelope tooling. At minimum, the following
output artifact types must have declared canonical paths:

| Artifact Type             | Required Canonical Path               |
|---------------------------|---------------------------------------|
| Execution logs            | `REPORTS/execution_logs/`             |
| Simulation reports        | `REPORTS/simulation/`                 |
| Mutation plans            | `REPORTS/mutation_plans/`             |
| Post-mutation reports     | `REPORTS/validation/`                 |
| Execution summary reports | `REPORTS/`                            |
| Rollback state records    | `REPORTS/rollback/`                   |

The IG must map each artifact type to its path, and the router
must enforce the mapping at runtime.

---

### Rule IR-032 — Write Path Validation Before Execution

**Rule ID:** IR-032
**Category:** Artifact Routing
**Severity:** HIGH
**EA Authority:** EA-002
**Auto-enforceable:** Yes

**Requirement:**
Before the first write operation of any phase, the artifact router
must validate that:
1. The target write path is within the router's allowed paths
2. The target directory exists or can be created safely
3. No existing artifact at the target path is protected (read-only
   or locked status)

Any write that fails these checks must be rejected, logged, and
treated as a non-fatal routing error (the operation is skipped;
the pipeline continues with the failure recorded).

---

### Rule IR-033 — Artifact Identity Recorded at Write Time

**Rule ID:** IR-033
**Category:** Artifact Routing
**Severity:** HIGH
**EA Authority:** EA-002, EA-007
**Auto-enforceable:** Yes

**Requirement:**
When the artifact router writes an artifact, it must immediately
compute and record the SHA-256 hash of the written content and
store it in an artifact identity registry. This registry is the
authoritative source of artifact hashes for post-execution
validation and future envelope manifest checks.

---------------------------------------------------------------------

## IMPLEMENTATION REQUIREMENT REGISTRY

| Rule ID | Category               | Severity | EA Authority       |
|---------|------------------------|----------|--------------------|
| IR-001  | Module Structure       | CRITICAL | EA-007             |
| IR-002  | Module Structure       | HIGH     | EA-003             |
| IR-003  | Module Structure       | HIGH     | EA-003             |
| IR-010  | Environment Compat.    | CRITICAL | EA-001, EA-005     |
| IR-011  | Environment Compat.    | CRITICAL | EA-001             |
| IR-012  | Environment Compat.    | HIGH     | EA-005             |
| IR-013  | Environment Compat.    | CRITICAL | EA-004             |
| IR-020  | Logging                | CRITICAL | EA-006             |
| IR-021  | Logging                | HIGH     | EA-006             |
| IR-022  | Logging                | HIGH     | EA-006             |
| IR-023  | Logging                | CRITICAL | EA-006, EA-010     |
| IR-030  | Artifact Routing       | CRITICAL | EA-002             |
| IR-031  | Artifact Routing       | HIGH     | EA-002             |
| IR-032  | Artifact Routing       | HIGH     | EA-002             |
| IR-033  | Artifact Routing       | HIGH     | EA-002, EA-007     |

---------------------------------------------------------------------

## VERSION HISTORY

| Version | Date       | Author    | Change Summary            |
|---------|------------|-----------|---------------------------|
| 1.0     | 2026-03-12 | Architect | Initial canonical release |
