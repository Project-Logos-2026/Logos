SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: IG_Configuration
ARTIFACT_NAME: IG_CONFIG_TOOLING_REQUIREMENTS
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelopes / IG_CONFIG
STATUS: Active

---------------------------------------------------------------------

# IG_CONFIG — Tooling Requirements

## Purpose

This document defines the code-level tooling requirements that all
ARCHON_PRIME Implementation Guide (IG) artifacts must specify for
their associated tooling. Where IG_CONFIG_IMPLEMENTATION_REQUIREMENTS.md
defines what tooling must accomplish (functional requirements), this
document defines how tooling must be built (architectural and
behavioral requirements).

---------------------------------------------------------------------

## REQUIREMENT CATEGORY 1 — MODULE ARCHITECTURE

### Rule TR-001 — Pipeline Controller Pattern Required

**Rule ID:** TR-001
**Category:** Module Architecture
**Severity:** CRITICAL
**EA Authority:** EA-003
**Auto-enforceable:** No (design review)

**Requirement:**
Every envelope implementation must be organized around a central
pipeline controller module. The pipeline controller is the sole
authority for:

- Initializing phases in canonical order
- Reading phase completion status before advancing
- Evaluating gate conditions (pre-simulation, mutation gate)
- Issuing AUTHORIZED or BLOCKED verdicts
- Triggering rollback on failure

No module other than the pipeline controller may determine phase
sequencing or advancement. Individual implementation modules must
expose an explicit entry-point function and return a structured
result that the controller reads to determine completion status.

**Required Pipeline Controller Interface:**
The IG must describe the controller's interface, which must include
at minimum:

```
run_phase(phase_code: str) → PhaseResult
get_phase_status(phase_code: str) → str
evaluate_gate(gate_id: str) → GateVerdict
trigger_rollback(phase_code: str) → RollbackResult
```

---

### Rule TR-002 — Phase Module Interface Contract

**Rule ID:** TR-002
**Category:** Module Architecture
**Severity:** HIGH
**EA Authority:** EA-003
**Auto-enforceable:** No (design review)

**Requirement:**
Each phase implementation module must expose a standardized
interface that the pipeline controller can call uniformly. The
IG must define this interface. At minimum it must include:

```
execute(context: ExecutionContext) → PhaseResult
```

Where `PhaseResult` is a structured object containing:

| Field            | Type    | Description                                  |
|------------------|---------|----------------------------------------------|
| `phase_code`     | string  | Canonical phase code (PHASE-01, etc.)        |
| `status`         | string  | COMPLETED / FAILED / ROLLED_BACK             |
| `artifacts`      | list    | Paths of all artifacts produced              |
| `errors`         | list    | Structured error records (empty if none)     |
| `gate_data`      | object  | Data relevant to subsequent gate evaluation  |
| `log_ref`        | string  | Reference to the phase execution log entry   |

---

### Rule TR-003 — Execution Context Object Required

**Rule ID:** TR-003
**Category:** Module Architecture
**Severity:** HIGH
**EA Authority:** EA-005
**Auto-enforceable:** No (design review)

**Requirement:**
The IG must define an `ExecutionContext` object that is passed
to all phase modules. The context object must carry:

- Envelope name and version
- Active artifact bundle references (DS, EP, IG paths and hashes)
- Current phase code
- Artifact router instance reference
- Logger instance reference
- Rollback registry reference
- Simulation mode flag (`True` during PHASE-05, `False` otherwise)
- Configuration values (loaded from `AP_SYSTEM_CONFIG/`)

The context object must be treated as read-only by all phase
modules except the pipeline controller, which alone may update
the current phase code and simulation mode flag.

---

### Rule TR-004 — No Global State Permitted

**Rule ID:** TR-004
**Category:** Module Architecture
**Severity:** HIGH
**EA Authority:** EA-003
**Auto-enforceable:** No (design review)

**Requirement:**
Implementation modules must not use global mutable state outside
of the `ExecutionContext` object. All state relevant to execution
must be carried in the context or in explicitly declared module
instance state. Global module-level variables that change during
execution are prohibited, as they prevent deterministic replay
and create non-deterministic behavior on re-run.

---

### Rule TR-005 — Single Responsibility per Module

**Rule ID:** TR-005
**Category:** Module Architecture
**Severity:** MEDIUM
**EA Authority:** EA-003
**Auto-enforceable:** No (design review)

**Requirement:**
Each implementation module must map to exactly one module category
(MOD-ENV, MOD-DISC, etc.). A module that spans multiple categories
must be split before the IG may be approved. The IG must include
a module registry table that maps each module name to its category
and phase(s).

---------------------------------------------------------------------

## REQUIREMENT CATEGORY 2 — CONFIGURATION LOADING

### Rule TR-010 — Configuration Loaded at Initialization Only

**Rule ID:** TR-010
**Category:** Configuration Loading
**Severity:** HIGH
**EA Authority:** EA-005
**Auto-enforceable:** No (design review)

**Requirement:**
All configuration values must be loaded once — at pipeline
initialization (during PHASE-01) — from files under
`AP_SYSTEM_CONFIG/`. Configuration must not be re-loaded or
modified during subsequent phases. Any phase that requires a
configuration value must read it from the `ExecutionContext`
object, which carries the pre-loaded configuration.

---

### Rule TR-011 — Configuration Schema Validation at Load Time

**Rule ID:** TR-011
**Category:** Configuration Loading
**Severity:** CRITICAL
**EA Authority:** EA-007
**Auto-enforceable:** Yes

**Requirement:**
Every configuration file loaded during PHASE-01 must be validated
against its declared schema before values are admitted to the
`ExecutionContext`. A configuration file that fails schema
validation must cause PHASE-01 to fail with a
`CONFIG_SCHEMA_VIOLATION` error. Execution must not proceed
with invalid configuration.

**Validation Flow:**
```
load_config_file(path)
  → parse JSON / YAML
  → identify schema reference
  → validate against schema (EE_SCHEMAS/ or AP_SYSTEM_CONFIG/SCHEMAS/)
  → on failure: raise CONFIG_SCHEMA_VIOLATION
  → on success: admit values to ExecutionContext
```

---

### Rule TR-012 — Configuration Values Must Be Typed

**Rule ID:** TR-012
**Category:** Configuration Loading
**Severity:** MEDIUM
**EA Authority:** EA-007
**Auto-enforceable:** No (design review)

**Requirement:**
The IG must declare the type and valid range/enum for every
configuration value consumed by the tooling. Values must be
type-checked at load time. A configuration value of the wrong
type must cause a `CONFIG_TYPE_ERROR` and halt initialization.

---

### Rule TR-013 — No Configuration Mutation After Load

**Rule ID:** TR-013
**Category:** Configuration Loading
**Severity:** HIGH
**EA Authority:** EA-003
**Auto-enforceable:** No (design review)

**Requirement:**
Once configuration values are loaded into the `ExecutionContext`,
no module may modify them. Configuration values must be treated as
immutable throughout the execution run. Any module that writes
to configuration values in the context must be redesigned.

---------------------------------------------------------------------

## REQUIREMENT CATEGORY 3 — ERROR HANDLING

### Rule TR-020 — Structured Error Type Required

**Rule ID:** TR-020
**Category:** Error Handling
**Severity:** HIGH
**EA Authority:** EA-006
**Auto-enforceable:** No (design review)

**Requirement:**
The IG must define a canonical error type used by all modules.
The error type must include at minimum:

| Field          | Type    | Description                                     |
|----------------|---------|-------------------------------------------------|
| `error_id`     | string  | Unique error identifier (auto-generated UUID)   |
| `error_code`   | string  | Categorical error code (e.g., CONFIG_SCHEMA_VIOLATION) |
| `severity`     | string  | CRITICAL / HIGH / MEDIUM / LOW                  |
| `phase_code`   | string  | Phase in which the error occurred               |
| `artifact_ref` | string  | Artifact or module where the error originated   |
| `message`      | string  | Human-readable error description                |
| `timestamp`    | string  | ISO 8601 UTC timestamp                         |
| `recoverable`  | bool    | Whether the error permits pipeline continuation |

---

### Rule TR-021 — CRITICAL Errors Halt the Pipeline

**Rule ID:** TR-021
**Category:** Error Handling
**Severity:** CRITICAL
**EA Authority:** EA-010
**Auto-enforceable:** No (design review)

**Requirement:**
Any error with `severity: CRITICAL` must cause the pipeline
controller to halt further phase advancement. The controller must:
1. Record the CRITICAL error in the execution log
2. Evaluate whether rollback is required (if PHASE-08 had begun)
3. Route execution to PHASE-10 for failure reporting
4. Never attempt to continue phase advancement past a CRITICAL error

---

### Rule TR-022 — HIGH Errors Are Evaluated Before Gate Advancement

**Rule ID:** TR-022
**Category:** Error Handling
**Severity:** HIGH
**EA Authority:** EA-005
**Auto-enforceable:** No (design review)

**Requirement:**
Any error with `severity: HIGH` encountered before the mutation
gate (PHASE-06) must be evaluated by the gate. Unreviewed HIGH
errors contribute to a BLOCKED gate verdict (see MGR-013 in
EP_CONFIG_MUTATION_GATE_RULES.md). HIGH errors encountered
during or after PHASE-08 must trigger post-mutation validation
of the affected artifacts.

---

### Rule TR-023 — Errors Must Not Be Silently Swallowed

**Rule ID:** TR-023
**Category:** Error Handling
**Severity:** CRITICAL
**EA Authority:** EA-006
**Auto-enforceable:** No (design review)

**Requirement:**
No implementation module may catch an exception and continue
execution without logging the error via the canonical logging
module (MOD-LOG). Any `try/except` or equivalent construct that
does not produce a log entry with the canonical error type is
non-compliant. The IG must explicitly document the error
propagation contract for each module.

---

### Rule TR-024 — Recoverable Errors Permit Continuation with Record

**Rule ID:** TR-024
**Category:** Error Handling
**Severity:** MEDIUM
**EA Authority:** EA-006
**Auto-enforceable:** No (design review)

**Requirement:**
Errors marked `recoverable: True` may allow the pipeline to
continue after the error is recorded. However:
- The error must be logged with full structured fields
- The affected artifact or operation must be flagged in the
  phase result
- The accumulation of more than five recoverable errors in a
  single phase must be escalated to `severity: HIGH` and treated
  as a non-recoverable phase result

---------------------------------------------------------------------

## REQUIREMENT CATEGORY 4 — DETERMINISTIC EXECUTION SUPPORT

### Rule TR-030 — Deterministic Input Ordering Required

**Rule ID:** TR-030
**Category:** Deterministic Execution
**Severity:** CRITICAL
**EA Authority:** EA-003
**Auto-enforceable:** No (design review)

**Requirement:**
All artifact discovery, analysis, and mutation operations must
process their input sets in a deterministic, reproducible order.
The following ordering conventions must be enforced:

- File system traversals must use lexicographic sort by path
- Module execution order must follow the dependency-resolved order
  from PHASE-04 (not file system order)
- Set-typed data structures must be converted to sorted lists
  before iteration in any context where order affects outcomes

The IG must document the ordering convention applied by each
module category.

---

### Rule TR-031 — No Timestamp-Dependent Control Flow

**Rule ID:** TR-031
**Category:** Deterministic Execution
**Severity:** HIGH
**EA Authority:** EA-003
**Auto-enforceable:** No (design review)

**Requirement:**
Module control flow must not depend on runtime timestamps.
Timestamps are permitted only in log entries and artifact
metadata (for human traceability). Decisions such as "should
this artifact be processed" or "has this phase expired" must
not be based on wall-clock time comparisons.

---

### Rule TR-032 — Idempotent Phase Design Required

**Rule ID:** TR-032
**Category:** Deterministic Execution
**Severity:** HIGH
**EA Authority:** EA-003
**Auto-enforceable:** No (design review)

**Requirement:**
Analysis and discovery phase modules (PHASE-02, PHASE-03,
PHASE-04) must be designed to be idempotent: running the same
phase with the same inputs must produce identical outputs on
repeated invocations. This property enables reliable re-run
after failure.

Mutation phase modules (PHASE-08) are explicitly exempt from
this requirement — mutation modules must detect already-applied
mutations and skip re-application rather than applying them
twice.

---

### Rule TR-033 — Simulation and Live Execution Must Produce Identical Plans

**Rule ID:** TR-033
**Category:** Deterministic Execution
**Severity:** CRITICAL
**EA Authority:** EA-004
**Auto-enforceable:** No (design review)

**Requirement:**
The mutation plan produced by PHASE-07 (Mutation Planning) must
be identical regardless of whether it was generated after a
simulation run or in isolation. The simulation pass must not
alter the state of inputs that feed into the mutation plan.
Any implementation where the simulation pass has side effects
that change the mutation plan is non-compliant.

---

### Rule TR-034 — Prompt Compiler Compatibility Required

**Rule ID:** TR-034
**Category:** Deterministic Execution
**Severity:** HIGH
**EA Authority:** EA-009
**Auto-enforceable:** No (design review)

**Requirement:**
The IG must describe how the implementation's phase structure
and step descriptions are formatted to be consumable by the
ARCHON_PRIME prompt compiler (per EA-009). Specifically:

- Phase entry points must be individually nameable
- Step descriptions within each phase must be structured
  (not inline prose)
- Mutation targets must be enumerable from the mutation plan
  artifact without executing the implementation

---------------------------------------------------------------------

## TOOLING REQUIREMENT REGISTRY

| Rule ID | Category                   | Severity | EA Authority     |
|---------|----------------------------|----------|------------------|
| TR-001  | Module Architecture        | CRITICAL | EA-003           |
| TR-002  | Module Architecture        | HIGH     | EA-003           |
| TR-003  | Module Architecture        | HIGH     | EA-005           |
| TR-004  | Module Architecture        | HIGH     | EA-003           |
| TR-005  | Module Architecture        | MEDIUM   | EA-003           |
| TR-010  | Configuration Loading      | HIGH     | EA-005           |
| TR-011  | Configuration Loading      | CRITICAL | EA-007           |
| TR-012  | Configuration Loading      | MEDIUM   | EA-007           |
| TR-013  | Configuration Loading      | HIGH     | EA-003           |
| TR-020  | Error Handling             | HIGH     | EA-006           |
| TR-021  | Error Handling             | CRITICAL | EA-010           |
| TR-022  | Error Handling             | HIGH     | EA-005           |
| TR-023  | Error Handling             | CRITICAL | EA-006           |
| TR-024  | Error Handling             | MEDIUM   | EA-006           |
| TR-030  | Deterministic Execution    | CRITICAL | EA-003           |
| TR-031  | Deterministic Execution    | HIGH     | EA-003           |
| TR-032  | Deterministic Execution    | HIGH     | EA-003           |
| TR-033  | Deterministic Execution    | CRITICAL | EA-004           |
| TR-034  | Deterministic Execution    | HIGH     | EA-009           |

---------------------------------------------------------------------

## VERSION HISTORY

| Version | Date       | Author    | Change Summary            |
|---------|------------|-----------|---------------------------|
| 1.0     | 2026-03-12 | Architect | Initial canonical release |
