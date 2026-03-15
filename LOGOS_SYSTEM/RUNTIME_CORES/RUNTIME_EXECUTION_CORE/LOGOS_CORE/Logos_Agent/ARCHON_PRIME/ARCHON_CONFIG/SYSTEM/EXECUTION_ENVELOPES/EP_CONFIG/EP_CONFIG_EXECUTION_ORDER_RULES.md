SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: EP_Configuration
ARTIFACT_NAME: EP_CONFIG_EXECUTION_ORDER_RULES
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelopes / EP_CONFIG
STATUS: Active

---------------------------------------------------------------------

# EP_CONFIG — Execution Order Rules

## Purpose

This document defines the deterministic ordering requirements for
ARCHON_PRIME Execution Plan (EP) artifacts. It specifies phase
dependency chains, prohibited skip conditions, and the mandatory
validation checkpoints that must appear at defined points in the
pipeline.

These rules enforce EA-003 (Deterministic Execution Ordering) and
ensure that no EP may define an execution sequence that permits
non-deterministic, skipped, or improperly guarded phases.

---------------------------------------------------------------------

## RULE SET 1 — PHASE DEPENDENCY RULES

### Rule EOR-001 — Canonical Phase Dependency Chain

**Rule ID:** EOR-001
**Category:** Dependency
**Severity:** CRITICAL
**EA Authority:** EA-003
**Auto-enforceable:** Yes

**Rule:**
Each phase has a mandatory predecessor. No phase may begin unless
its predecessor has completed with a recorded completion status.

The canonical dependency chain is:

```
PHASE-01 → PHASE-02 → PHASE-03 → PHASE-04
                                      ↓
                                  PHASE-05 → PHASE-06
                                                 ↓
                                             [MUTATION GATE]
                                                 ↓
                                             PHASE-07 → PHASE-08 → PHASE-09
                                                                        ↓
                                                                    PHASE-10
```

**Phase Predecessor Table:**

| Phase     | Canonical Name              | Required Predecessor | Required Predecessor Status |
|-----------|-----------------------------|----------------------|-----------------------------|
| PHASE-01  | Environment Initialization  | None (entry phase)   | N/A                         |
| PHASE-02  | Artifact Discovery          | PHASE-01             | COMPLETED                   |
| PHASE-03  | Structural Analysis         | PHASE-02             | COMPLETED                   |
| PHASE-04  | Dependency Graph Construction | PHASE-03           | COMPLETED                   |
| PHASE-05  | Simulation Pass             | PHASE-04             | COMPLETED                   |
| PHASE-06  | Simulation Validation       | PHASE-05             | COMPLETED                   |
| PHASE-07  | Mutation Planning           | PHASE-06             | COMPLETED + AUTHORIZED       |
| PHASE-08  | Controlled Mutation         | PHASE-07             | COMPLETED                   |
| PHASE-09  | Post-Mutation Validation    | PHASE-08             | COMPLETED                   |
| PHASE-10  | Reporting                   | PHASE-09             | COMPLETED (any outcome)     |

**Pass Condition:**
Each phase's predecessor check passes with the required status
before the phase is allowed to begin.

**Failure Action:**
`DEPENDENCY_VIOLATION`. Execution is halted. The phase that
attempted to begin without an authorized predecessor is logged.

---

### Rule EOR-002 — Single-Predecessor Constraint

**Rule ID:** EOR-002
**Category:** Dependency
**Severity:** HIGH
**EA Authority:** EA-003
**Auto-enforceable:** Yes

**Rule:**
No phase may have more than one active predecessor requirement.
Parallel execution of phases in the same pipeline run is prohibited.
The execution model is strictly sequential.

**Failure Action:**
`PARALLEL_EXECUTION_VIOLATION`. Any attempt to initialize two
phases simultaneously must be rejected.

---

### Rule EOR-003 — Phase Completion Status Must Be Persisted

**Rule ID:** EOR-003
**Category:** Dependency
**Severity:** HIGH
**EA Authority:** EA-006
**Auto-enforceable:** Yes

**Rule:**
When a phase completes (success or failure), its completion status
must be written to the execution log before the pipeline controller
evaluates the next phase's predecessor condition.

Status values that may be recorded:
- `COMPLETED` — phase ran to end without critical failure
- `FAILED` — phase encountered a critical failure
- `SKIPPED` — explicitly prohibited (see EOR-004)
- `ROLLED_BACK` — phase was undone by rollback protocol

**Failure Action:**
If a phase's completion status cannot be read from the execution
log, the pipeline must treat that phase as not completed and refuse
to advance.

---------------------------------------------------------------------

## RULE SET 2 — PROHIBITED PHASE SKIPPING

### Rule EOR-010 — Absolute Skip Prohibition for Simulation Phases

**Rule ID:** EOR-010
**Category:** Skip Prohibition
**Severity:** CRITICAL
**EA Authority:** EA-004
**Auto-enforceable:** Yes

**Rule:**
PHASE-05 (Simulation Pass) and PHASE-06 (Simulation Validation)
must never be skipped under any conditions.

There is no configuration flag, runtime argument, or operator
override that may bypass these phases. Any EP artifact that
declares a phase sequence omitting PHASE-05 or PHASE-06 is
structurally invalid and must be rejected before execution begins.

**Failure Action:**
`SIMULATION_SKIP_PROHIBITED`. EP is rejected at validation time.
Execution cannot begin.

---

### Rule EOR-011 — Analysis Phase Skip Prohibition

**Rule ID:** EOR-011
**Category:** Skip Prohibition
**Severity:** CRITICAL
**EA Authority:** EA-003
**Auto-enforceable:** Yes

**Rule:**
PHASE-02 (Artifact Discovery), PHASE-03 (Structural Analysis), and
PHASE-04 (Dependency Graph Construction) must not be skipped. These
phases produce inputs that are required by PHASE-05. An EP that
omits any analysis phase is structurally invalid.

**Exception:**
If an envelope's DS explicitly declares that dependency graph
construction is out of scope (because the envelope targets only
non-code artifacts with no dependency relationships), PHASE-04
may be replaced with a `PHASE-04-STUB` that records its own
completion with an explanation. PHASE-04 may not simply be absent.

**Failure Action:**
`ANALYSIS_PHASE_MISSING`. EP is rejected at validation time.

---

### Rule EOR-012 — Validation Phase Skip Prohibition

**Rule ID:** EOR-012
**Category:** Skip Prohibition
**Severity:** CRITICAL
**EA Authority:** EA-005, EA-007
**Auto-enforceable:** Yes

**Rule:**
PHASE-09 (Post-Mutation Validation) must never be skipped. Even if
PHASE-08 completes with no mutation operations (because no targets
required change), PHASE-09 must still execute and record its
validation result. A zero-mutation execution is still subject to
post-execution validation.

**Failure Action:**
`VALIDATION_SKIP_PROHIBITED`. EP is rejected at validation time
if PHASE-09 is absent from the declared phase sequence.

---

### Rule EOR-013 — PHASE-10 Skip Prohibition

**Rule ID:** EOR-013
**Category:** Skip Prohibition
**Severity:** HIGH
**EA Authority:** EA-006
**Auto-enforceable:** Yes

**Rule:**
PHASE-10 (Reporting) must always execute, regardless of execution
outcome in prior phases. Reporting is unconditional. No failure in
any prior phase may cause the reporting phase to be bypassed.

**Failure Action:**
If PHASE-10 is absent from an EP's declared phase sequence, the EP
is flagged `REPORTING_OMITTED` and is not permitted to govern an
execution envelope.

---

### Rule EOR-014 — STATUS Value `SKIPPED` Is Prohibited in EP Logs

**Rule ID:** EOR-014
**Category:** Skip Prohibition
**Severity:** CRITICAL
**EA Authority:** EA-003, EA-006
**Auto-enforceable:** Yes

**Rule:**
The phase completion status value `SKIPPED` must never appear in
an EP execution log for phases PHASE-01 through PHASE-10. A phase
is either `COMPLETED`, `FAILED`, or `ROLLED_BACK`. There is no
legitimate skip condition for any canonical phase.

**Failure Action:**
If `SKIPPED` is detected in an EP execution log for any canonical
phase, the log is flagged as non-compliant and the execution record
is considered invalid. The envelope must be re-run from the point
of the skipped phase.

---------------------------------------------------------------------

## RULE SET 3 — REQUIRED VALIDATION CHECKPOINTS

### Rule EOR-020 — Checkpoint: Post-Initialization Verification

**Rule ID:** EOR-020
**Category:** Validation Checkpoint
**Severity:** CRITICAL
**Position:** Between PHASE-01 and PHASE-02
**EA Authority:** EA-001, EA-005, EA-007

**Checkpoint Conditions (all must pass):**

1. All artifact hashes match manifest records (EA-001 check)
2. All bundle artifact schemas validated (EA-007 check)
3. Governance consistency check passed (EA-005 check)
4. Execution context configuration verified:
   - `artifact_router_required: true` — router active
   - `simulation_required: true` — simulation layer available
   - `rollback_enabled: true` — rollback mechanism armed

**Failure Action:**
Any failing condition halts progression to PHASE-02. All failures
are logged. Execution may not resume until the environment is
corrected and PHASE-01 is re-run.

---

### Rule EOR-021 — Checkpoint: Pre-Simulation Gate

**Rule ID:** EOR-021
**Category:** Validation Checkpoint
**Severity:** CRITICAL
**Position:** Between PHASE-04 and PHASE-05
**EA Authority:** EA-003, EA-004

**Checkpoint Conditions (all must pass):**

1. Dependency graph artifact exists and is non-empty
2. Module execution order is derived and recorded
3. Unresolvable circular dependencies have been reported
   (their presence does not block the checkpoint — they must
   simply be documented)
4. Simulation layer is confirmed active and ready

**Failure Action:**
If the simulation layer is unavailable, progression to PHASE-05
is prohibited. All other failures must be logged; unresolvable
circulars that would block the entire pipeline halt execution.

---

### Rule EOR-022 — Checkpoint: Mutation Authorization Gate

**Rule ID:** EOR-022
**Category:** Validation Checkpoint
**Severity:** CRITICAL
**Position:** Between PHASE-06 and PHASE-07
**EA Authority:** EA-004 (primary), EA-005

**This is the primary mutation gate. See EP_CONFIG_MUTATION_GATE_RULES.md
for the full definition of mutation authorization conditions.**

**Checkpoint Summary:**
PHASE-07 and PHASE-08 may not begin unless PHASE-06 has produced
a Mutation Authorization Verdict of `AUTHORIZED`.

A verdict of `BLOCKED` terminates the pipeline at this point and
routes execution directly to PHASE-10 for failure reporting.

**Failure Action:**
`MUTATION_GATE_BLOCKED`. No mutations occur. Pipeline proceeds
to PHASE-10. Failure report documents the blocked verdict.

---

### Rule EOR-023 — Checkpoint: Pre-Reporting Validation Consolidation

**Rule ID:** EOR-023
**Category:** Validation Checkpoint
**Severity:** HIGH
**Position:** Between PHASE-09 and PHASE-10
**EA Authority:** EA-006, EA-008

**Checkpoint Conditions:**

1. PHASE-09 validation report artifact exists
2. PHASE-09 overall verdict is recorded (PASSED or FAILED)
3. Rollback state is resolved:
   - If rollback occurred: rollback completion status is COMPLETE
   - If no rollback: rollback state field is `NOT_TRIGGERED`
4. All phase logs from PHASE-01 through PHASE-09 are present
   in the log store

**Failure Action:**
If any phase log is missing, PHASE-10 must note the gap in the
execution summary. Missing logs do not prevent reporting from
executing.

---------------------------------------------------------------------

## RULE SET 4 — PHASE SEQUENCE VALIDATION

### Rule EOR-030 — EP Artifact Must Declare Phase Sequence

**Rule ID:** EOR-030
**Category:** Structural
**Severity:** CRITICAL
**EA Authority:** EA-003
**Auto-enforceable:** Yes

**Rule:**
Every EP artifact must contain an explicit, ordered phase sequence
declaration, listing all ten canonical phase codes (PHASE-01 through
PHASE-10) in canonical order.

**Valid Declaration Format (example):**
```
Execution_Phases:
  1. PHASE-01 — Environment Initialization
  2. PHASE-02 — Artifact Discovery
  3. PHASE-03 — Structural Analysis
  4. PHASE-04 — Dependency Graph Construction
  5. PHASE-05 — Simulation Pass
  6. PHASE-06 — Simulation Validation
  7. PHASE-07 — Mutation Planning
  8. PHASE-08 — Controlled Mutation
  9. PHASE-09 — Post-Mutation Validation
  10. PHASE-10 — Reporting
```

**Failure Action:**
An EP that does not declare this sequence is rejected at structural
validation time. `EP_PHASE_SEQUENCE_MISSING`.

---

### Rule EOR-031 — Phase Sequence Must Match Manifest

**Rule ID:** EOR-031
**Category:** Structural
**Severity:** HIGH
**EA Authority:** EA-003, EA-008
**Auto-enforceable:** Yes

**Rule:**
The `execution_phases` array declared in `ENVELOPE_MANIFEST.json`
must be consistent with the phase sequence in the EP artifact.
The manifest does not need to use full phase codes but must
reference the same phases in the same order.

**Failure Action:**
`EP_MANIFEST_PHASE_MISMATCH`. DS validation rule DSV-012 will
also flag this condition independently.

---------------------------------------------------------------------

## RULE REGISTRY

| Rule ID   | Category              | Severity | EA Authority       |
|-----------|-----------------------|----------|--------------------|
| EOR-001   | Dependency            | CRITICAL | EA-003             |
| EOR-002   | Dependency            | HIGH     | EA-003             |
| EOR-003   | Dependency            | HIGH     | EA-006             |
| EOR-010   | Skip Prohibition      | CRITICAL | EA-004             |
| EOR-011   | Skip Prohibition      | CRITICAL | EA-003             |
| EOR-012   | Skip Prohibition      | CRITICAL | EA-005, EA-007     |
| EOR-013   | Skip Prohibition      | HIGH     | EA-006             |
| EOR-014   | Skip Prohibition      | CRITICAL | EA-003, EA-006     |
| EOR-020   | Validation Checkpoint | CRITICAL | EA-001, EA-005, EA-007 |
| EOR-021   | Validation Checkpoint | CRITICAL | EA-003, EA-004     |
| EOR-022   | Validation Checkpoint | CRITICAL | EA-004, EA-005     |
| EOR-023   | Validation Checkpoint | HIGH     | EA-006, EA-008     |
| EOR-030   | Structural            | CRITICAL | EA-003             |
| EOR-031   | Structural            | HIGH     | EA-003, EA-008     |

---------------------------------------------------------------------

## VERSION HISTORY

| Version | Date       | Author    | Change Summary            |
|---------|------------|-----------|---------------------------|
| 1.0     | 2026-03-12 | Architect | Initial canonical release |
