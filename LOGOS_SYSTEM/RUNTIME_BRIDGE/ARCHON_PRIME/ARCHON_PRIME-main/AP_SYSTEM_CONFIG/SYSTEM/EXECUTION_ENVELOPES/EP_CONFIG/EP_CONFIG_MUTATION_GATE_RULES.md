SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: EP_Configuration
ARTIFACT_NAME: EP_CONFIG_MUTATION_GATE_RULES
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelopes / EP_CONFIG
STATUS: Active

---------------------------------------------------------------------

# EP_CONFIG — Mutation Gate Rules

## Purpose

This document defines the complete set of conditions that must be
satisfied before any mutation phase (PHASE-08: Controlled Mutation)
is permitted to execute within an ARCHON_PRIME Execution Envelope.

The mutation gate is the most critical control point in the
execution pipeline. It enforces the principle that file system
mutations are a consequence of successful analysis, simulation,
and validation — never a starting assumption.

The mutation gate is implemented between PHASE-06 (Simulation
Validation) and PHASE-07 (Mutation Planning). No mutation planning
or execution may proceed without a gate AUTHORIZED verdict.

---------------------------------------------------------------------

## SECTION 1 — GATE ARCHITECTURE

### 1.1 Gate Position in Pipeline

```
PHASE-05: Simulation Pass
          ↓
PHASE-06: Simulation Validation
          ↓
    ┌─────────────┐
    │ MUTATION    │
    │    GATE     │
    └──────┬──────┘
           │
    ┌──────┴──────┐
    │             │
AUTHORIZED     BLOCKED
    │             │
PHASE-07      PHASE-10
(Mutation    (Failure
 Planning)    Report)
```

### 1.2 Gate Verdict Values

| Verdict    | Meaning                                              | Next Phase |
|------------|------------------------------------------------------|------------|
| AUTHORIZED | All gate conditions passed — mutations may proceed   | PHASE-07   |
| BLOCKED    | One or more gate conditions failed — no mutations    | PHASE-10   |

There is no partial authorization. The verdict is binary. A gate
verdict of BLOCKED routes the pipeline directly to PHASE-10 for
failure reporting. No mutations occur and no mutation planning
is performed.

### 1.3 Gate Verdict Persistence

The gate verdict must be persisted as a named artifact in the
envelope's execution log before PHASE-07 is allowed to initialize.
The artifact must record:
- The verdict value
- The timestamp of gate evaluation
- The pass/fail status of each individual gate condition

---------------------------------------------------------------------

## SECTION 2 — GATE CONDITION: SUCCESSFUL SIMULATION

### Rule MGR-001 — Simulation Pass Must Be Recorded As Completed

**Rule ID:** MGR-001
**Category:** Simulation Requirement
**Severity:** CRITICAL
**EA Authority:** EA-004

**Condition:**
PHASE-05 (Simulation Pass) must have completed with status
`COMPLETED` in the execution log. A simulation phase that:
- was not executed
- was interrupted before completion
- has no recorded completion status

...does not satisfy this condition.

**Verification Method:**
Read the PHASE-05 completion record from the execution log.
Verify status field equals `COMPLETED`.

**Pass Condition:**
PHASE-05 status = `COMPLETED`.

**Gate Impact:**
CRITICAL — failure of this condition produces a BLOCKED verdict
regardless of all other condition results.

---

### Rule MGR-002 — No Critical Simulation Failures

**Rule ID:** MGR-002
**Category:** Simulation Requirement
**Severity:** CRITICAL
**EA Authority:** EA-004

**Condition:**
The PHASE-05 simulation outcome records must contain zero
CRITICAL-severity simulation failures.

Critical simulation failures are defined as simulation outcomes
where the predicted mutation operation would:
- Corrupt or permanently delete a protected artifact
- Produce a schema-invalid output artifact
- Violate a system boundary declared in DS Section 4
- Trigger an unrecoverable state in a dependent module

**Verification Method:**
Scan the PHASE-05 simulation outcome list for entries where
severity = `CRITICAL` and result = `FAILURE`.

**Pass Condition:**
Count of CRITICAL-severity FAILURE entries = 0.

**Gate Impact:**
CRITICAL — any CRITICAL simulation failure produces a BLOCKED
verdict.

---

### Rule MGR-003 — Simulation Coverage Threshold Met

**Rule ID:** MGR-003
**Category:** Simulation Requirement
**Severity:** HIGH
**EA Authority:** EA-004

**Condition:**
The simulation pass must have produced an outcome record for
every in-scope target declared in the PHASE-02 artifact inventory.
Uncovered targets (targets in scope that have no simulation
outcome record) indicate incomplete simulation coverage.

**Verification Method:**
Cross-reference PHASE-02 artifact inventory against PHASE-05
simulation outcome records. Count targets with no outcome record.

**Pass Condition:**
Uncovered target count = 0.

**Gate Impact:**
HIGH — uncovered targets produce a BLOCKED verdict if count > 0.

**Exception:**
If a target was removed from scope between PHASE-02 and PHASE-05
due to a recorded scope reduction event (documented in PHASE-03
or PHASE-04), the target is excluded from coverage measurement
provided the scope reduction is logged.

---

### Rule MGR-004 — Simulation Execution Log Exists and Is Non-Empty

**Rule ID:** MGR-004
**Category:** Simulation Requirement
**Severity:** CRITICAL
**EA Authority:** EA-004, EA-006

**Condition:**
A simulation execution log artifact must exist with at least one
recorded log entry from PHASE-05.

**Verification Method:**
Verify the simulation execution log file exists and has a non-zero
entry count.

**Pass Condition:**
Log exists and entry count >= 1.

**Gate Impact:**
CRITICAL — no simulation log means no verifiable simulation.
Produces BLOCKED verdict.

---------------------------------------------------------------------

## SECTION 3 — GATE CONDITION: VALIDATION PASS

### Rule MGR-010 — Simulation Validation Must Be Recorded As Completed

**Rule ID:** MGR-010
**Category:** Validation Requirement
**Severity:** CRITICAL
**EA Authority:** EA-004, EA-005

**Condition:**
PHASE-06 (Simulation Validation) must have completed with status
`COMPLETED` in the execution log.

**Pass Condition:**
PHASE-06 status = `COMPLETED`.

**Gate Impact:**
CRITICAL.

---

### Rule MGR-011 — Simulated Outcomes Meet DS Success Criteria

**Rule ID:** MGR-011
**Category:** Validation Requirement
**Severity:** CRITICAL
**EA Authority:** EA-005

**Condition:**
The PHASE-06 validation must confirm that the simulated execution
outcomes satisfy the numbered success criteria declared in DS
Section 10.

Each DS Section 10 criterion that is traceable to a simulation
outcome must have a recorded pass result. Criteria with no
traceable simulation outcome must be recorded as deferred to
PHASE-09.

**Verification Method:**
For each DS Section 10 criterion marked as simulation-traceable,
verify a corresponding PHASE-06 criterion evaluation record with
result = `PASS`.

**Pass Condition:**
All simulation-traceable criteria evaluated = PASS.
Count of simulation-traceable criteria with FAIL result = 0.

**Gate Impact:**
CRITICAL — any FAIL result against a simulation-traceable
success criterion produces a BLOCKED verdict.

---

### Rule MGR-012 — Simulation Validation Report Artifact Exists

**Rule ID:** MGR-012
**Category:** Validation Requirement
**Severity:** HIGH
**EA Authority:** EA-006

**Condition:**
PHASE-06 must have produced a named simulation validation report
artifact. The report must be locatable via the artifact router
(EA-002).

**Pass Condition:**
Report artifact exists and is non-empty.

**Gate Impact:**
HIGH — missing report produces BLOCKED verdict.

---

### Rule MGR-013 — No HIGH-Severity Simulation Failures in Validation Record

**Rule ID:** MGR-013
**Category:** Validation Requirement
**Severity:** HIGH
**EA Authority:** EA-005

**Condition:**
The PHASE-06 validation record must not contain any unreviewed
HIGH-severity simulation failure entries.

A HIGH-severity failure that has been reviewed, documented, and
accepted with a recorded justification does not block the gate.
An unreviewed HIGH-severity failure does.

**Pass Condition:**
Count of unreviewed HIGH-severity failures in PHASE-06 record = 0.

**Gate Impact:**
HIGH — any unreviewed HIGH-severity failure produces BLOCKED verdict.

---------------------------------------------------------------------

## SECTION 4 — GATE CONDITION: GOVERNANCE COMPLIANCE

### Rule MGR-020 — EA-005 Governance Consistency Check Passed

**Rule ID:** MGR-020
**Category:** Governance Requirement
**Severity:** CRITICAL
**EA Authority:** EA-005

**Condition:**
The EA-005 governance consistency check must have passed during
PHASE-01 (Environment Initialization) or PHASE-06 (Simulation
Validation). The check must verify:

1. Execution envelope artifacts are consistent with manifest
2. Workflow configuration artifacts are consistent
3. Governance protocol artifacts are consistent
4. No schema conflicts or unresolved cross-references exist

**Verification Method:**
Read the EA-005 governance check result from the PHASE-01 or
PHASE-06 log.

**Pass Condition:**
EA-005 check result = `PASSED`.

**Gate Impact:**
CRITICAL.

---

### Rule MGR-021 — EA-001 Artifact Hash Integrity Confirmed

**Rule ID:** MGR-021
**Category:** Governance Requirement
**Severity:** CRITICAL
**EA Authority:** EA-001

**Condition:**
The EA-001 artifact identity check must have passed during
PHASE-01. All DS, EP, and IG artifact hashes must match the
manifest at the time of gate evaluation.

If any artifact has been modified since PHASE-01 ran its hash
check, the gate must re-evaluate the hash for that artifact
before issuing an AUTHORIZED verdict.

**Pass Condition:**
All artifact hashes match manifest records at gate evaluation time.

**Gate Impact:**
CRITICAL — any hash mismatch produces an immediate BLOCKED verdict
and must trigger incident logging.

---

### Rule MGR-022 — EA-002 Artifact Router Confirmed Active

**Rule ID:** MGR-022
**Category:** Governance Requirement
**Severity:** HIGH
**EA Authority:** EA-002

**Condition:**
The artifact router must be confirmed active and able to route
mutation outputs to their canonical target directories before
mutation planning begins.

**Pass Condition:**
Artifact router health check = `ACTIVE`.

**Gate Impact:**
HIGH — unavailable artifact router produces BLOCKED verdict, as
there is no safe destination for mutation outputs.

---

### Rule MGR-023 — EA-010 Rollback Mechanism Confirmed Armed

**Rule ID:** MGR-023
**Category:** Governance Requirement
**Severity:** CRITICAL
**EA Authority:** EA-010

**Condition:**
The rollback mechanism must be confirmed armed and operational
before mutation is authorized. This requires:
- Pre-mutation artifact state snapshot mechanism is ready
- Rollback log is writable
- Rollback trigger is bound to the mutation executor

**Pass Condition:**
Rollback mechanism status = `ARMED`.

**Gate Impact:**
CRITICAL — mutations must never begin without a confirmed rollback
mechanism. Any rollback readiness failure produces a BLOCKED verdict.

---

### Rule MGR-024 — EA-003 Deterministic Order Lock Confirmed

**Rule ID:** MGR-024
**Category:** Governance Requirement
**Severity:** HIGH
**EA Authority:** EA-003

**Condition:**
The deterministic execution order from PHASE-04 (dependency-ordered
module list) must be locked and immutable before the gate evaluates.
No changes to the execution order may occur after the dependency
graph is constructed.

**Pass Condition:**
Execution order lock status = `LOCKED`.

**Gate Impact:**
HIGH — an unlocked or mutable execution order produces BLOCKED
verdict.

---------------------------------------------------------------------

## SECTION 5 — GATE EVALUATION PROCEDURE

The mutation gate must be evaluated in the following sequence:

```
Step 1: Read PHASE-05 completion record (MGR-001)
Step 2: Read PHASE-06 completion record (MGR-010)
Step 3: Check simulation execution log existence (MGR-004)
Step 4: Count CRITICAL simulation failures (MGR-002)
Step 5: Check simulation coverage (MGR-003)
Step 6: Evaluate DS criteria against simulation outcomes (MGR-011)
Step 7: Check simulation validation report (MGR-012)
Step 8: Count unreviewed HIGH failures (MGR-013)
Step 9: Check EA-005 governance consistency (MGR-020)
Step 10: Re-verify artifact hashes (MGR-021)
Step 11: Check artifact router status (MGR-022)
Step 12: Check rollback mechanism status (MGR-023)
Step 13: Check execution order lock (MGR-024)
Step 14: Consolidate results → Issue AUTHORIZED or BLOCKED verdict
Step 15: Persist gate verdict artifact with timestamp and detail
```

Steps 1–13 must all be evaluated before issuing a verdict. A
verdict must not be issued after only a subset of checks.

---------------------------------------------------------------------

## SECTION 6 — GATE FAILURE REPORTING

When the gate issues a BLOCKED verdict, the failure report produced
by PHASE-10 must include:

- Gate verdict: `BLOCKED`
- Timestamp of gate evaluation
- List of all gate conditions with individual pass/fail status
- For each failed condition:
  - Rule ID
  - Failure description
  - Recommended remediation
- Count of mutations that did NOT occur as a result of the block
- Confirmation that rollback was or was not required
  (if PHASE-08 never ran, rollback is `NOT_REQUIRED`)

---------------------------------------------------------------------

## SECTION 7 — MUTATION GATE RULE REGISTRY

| Rule ID   | Category                | Severity | EA Authority           |
|-----------|-------------------------|----------|------------------------|
| MGR-001   | Simulation Requirement  | CRITICAL | EA-004                 |
| MGR-002   | Simulation Requirement  | CRITICAL | EA-004                 |
| MGR-003   | Simulation Requirement  | HIGH     | EA-004                 |
| MGR-004   | Simulation Requirement  | CRITICAL | EA-004, EA-006         |
| MGR-010   | Validation Requirement  | CRITICAL | EA-004, EA-005         |
| MGR-011   | Validation Requirement  | CRITICAL | EA-005                 |
| MGR-012   | Validation Requirement  | HIGH     | EA-006                 |
| MGR-013   | Validation Requirement  | HIGH     | EA-005                 |
| MGR-020   | Governance Requirement  | CRITICAL | EA-005                 |
| MGR-021   | Governance Requirement  | CRITICAL | EA-001                 |
| MGR-022   | Governance Requirement  | HIGH     | EA-002                 |
| MGR-023   | Governance Requirement  | CRITICAL | EA-010                 |
| MGR-024   | Governance Requirement  | HIGH     | EA-003                 |

**Total CRITICAL rules:** 7
**Total HIGH rules:** 6

A BLOCKED verdict is issued if ANY CRITICAL rule fails.
A BLOCKED verdict is issued if ANY HIGH rule fails.
An AUTHORIZED verdict requires ALL 13 rules to pass.

---------------------------------------------------------------------

## SECTION 8 — VERSION HISTORY

| Version | Date       | Author    | Change Summary            |
|---------|------------|-----------|---------------------------|
| 1.0     | 2026-03-12 | Architect | Initial canonical release |
