SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: IG_Configuration
ARTIFACT_NAME: IG_CONFIG_VALIDATION_REQUIREMENTS
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelopes / IG_CONFIG
STATUS: Active

---------------------------------------------------------------------

# IG_CONFIG — Validation Requirements

## Purpose

This document defines the validation requirements that every
ARCHON_PRIME Implementation Guide (IG) artifact must specify for
its associated tooling. Validation is not optional — it is a
structural obligation at every phase transition and at every
mutation boundary.

Where IG_CONFIG_IMPLEMENTATION_REQUIREMENTS.md defines what
tooling must accomplish and IG_CONFIG_TOOLING_REQUIREMENTS.md
defines how tooling must be built, this document defines what
the tooling must verify before, during, and after execution.

---------------------------------------------------------------------

## REQUIREMENT CATEGORY 1 — SIMULATION VALIDATION

### Rule VR-001 — Simulation Layer Must Be Independently Verifiable

**Rule ID:** VR-001
**Category:** Simulation Validation
**Severity:** CRITICAL
**EA Authority:** EA-004
**Auto-enforceable:** No (architecture review)

**Requirement:**
The simulation layer must be implemented as a component distinct
from the mutation executor. The simulation layer must be capable
of running in full isolation — producing its outcome records
without invoking any write operation against the live artifact
set.

Every IG must specify which module or class provides the simulation
layer and must confirm that the simulation layer and the mutation
executor do not share a write-capable file handle at runtime.

---

### Rule VR-002 — Simulation Must Cover All In-Scope Targets

**Rule ID:** VR-002
**Category:** Simulation Validation
**Severity:** CRITICAL
**EA Authority:** EA-004
**Auto-enforceable:** Yes (coverage check)

**Requirement:**
The simulation pass must produce an outcome record for every
artifact in the PHASE-02 discovery inventory that falls within
the envelope's declared scope. The tooling must implement a
coverage verification step comparing the discovery inventory
against the simulation outcome list.

An IG must specify the coverage verification mechanism and define
the threshold: zero uncovered in-scope targets.

**Pass Condition:**
`len(simulation_outcomes) == len(discovery_inventory_in_scope)`

---

### Rule VR-003 — Simulation Outcome Severity Classification

**Rule ID:** VR-003
**Category:** Simulation Validation
**Severity:** HIGH
**EA Authority:** EA-004, EA-005
**Auto-enforceable:** Yes

**Requirement:**
Every simulation outcome record must include a severity field
classified as one of:

```
CRITICAL | HIGH | MEDIUM | LOW | INFO
```

The severity classification must be determined by rule, not
by operator judgment. Every IG must specify the severity
assignment rules for its simulation outcomes.

Minimum severity assignment rules that must be specified:

| Condition                                        | Minimum Severity |
|--------------------------------------------------|------------------|
| Predicted outcome would corrupt a protected artifact | CRITICAL     |
| Predicted outcome produces schema-invalid output  | CRITICAL         |
| Predicted outcome violates a system boundary      | CRITICAL         |
| Predicted outcome triggers unresolvable dependency | HIGH            |
| Predicted outcome produces unreachable dead code  | MEDIUM           |
| Predicted outcome is a no-op (no change expected) | INFO             |

---

### Rule VR-004 — Simulation Results Must Not Be Mutably Cached

**Rule ID:** VR-004
**Category:** Simulation Validation
**Severity:** HIGH
**EA Authority:** EA-004
**Auto-enforceable:** No (code review)

**Requirement:**
Simulation outcome records must be treated as immutable once
written. Tooling must not provide a mechanism to amend simulation
results in place. If a simulation outcome is found to be incorrect,
the simulation pass must be re-run in full. Partial re-simulation
of individual targets without a full re-run is prohibited.

Every IG must confirm this constraint in its simulation layer
specification.

---

### Rule VR-005 — Simulation Validation Report Is a Mandatory Artifact

**Rule ID:** VR-005
**Category:** Simulation Validation
**Severity:** CRITICAL
**EA Authority:** EA-004, EA-006
**Auto-enforceable:** Yes

**Requirement:**
PHASE-06 (Simulation Validation) must produce a named report
artifact that is routed through the artifact router. The report
is not a log entry — it is a first-class artifact with a canonical
filename and a defined schema.

Every IG must specify:
- The canonical filename pattern for the simulation validation report
- The schema it conforms to
- The artifact router destination for the report

The mutation gate (MGR-012) verifies this artifact's existence
before issuing an AUTHORIZED verdict.

---------------------------------------------------------------------

## REQUIREMENT CATEGORY 2 — MUTATION VALIDATION

### Rule VR-010 — Pre-Mutation State Snapshot Required

**Rule ID:** VR-010
**Category:** Mutation Validation
**Severity:** CRITICAL
**EA Authority:** EA-010
**Auto-enforceable:** No (implementation review)

**Requirement:**
Before PHASE-08 applies any mutation to a target artifact, the
tooling must capture and persist a pre-mutation state snapshot
for that artifact. The snapshot must be sufficient to restore
the artifact to its exact pre-mutation state if rollback is
triggered.

Acceptable snapshot mechanisms:
- File content hash + copy stored to rollback staging directory
- Git stash of the artifact's current state with a labeled ref
- In-memory byte buffer persisted to a rollback manifest

Every IG must specify which snapshot mechanism its implementation
uses and where rollback snapshots are stored.

---

### Rule VR-011 — Each Mutation Operation Must Be Individually Logged

**Rule ID:** VR-011
**Category:** Mutation Validation
**Severity:** CRITICAL
**EA Authority:** EA-006
**Auto-enforceable:** Yes (log inspection)

**Requirement:**
Every individual mutation operation (one write, one patch, one
header injection) must produce a discrete log entry before the
next operation begins. Batch mutation operations that produce a
single log entry covering multiple artifact changes violate this
rule.

Each log entry must include:
- Target artifact path (canonical)
- Operation type (`write` / `patch` / `inject` / `delete`)
- Pre-mutation hash of the artifact
- Post-mutation hash of the artifact
- Timestamp
- Phase identifier (`PHASE-08`)
- Success/failure status

---

### Rule VR-012 — Post-Mutation Artifact Hash Must Be Recorded

**Rule ID:** VR-012
**Category:** Mutation Validation
**Severity:** HIGH
**EA Authority:** EA-007
**Auto-enforceable:** Yes

**Requirement:**
Immediately after each mutation operation completes, the tooling
must compute and record the post-mutation SHA-256 hash of the
mutated artifact. This hash is used by PHASE-09 (Post-Mutation
Validation) to verify that the artifact was not further modified
between mutation and validation.

If the hash recorded after mutation does not match the hash
computed at the start of PHASE-09 validation for that artifact,
the discrepancy must be flagged as `ARTIFACT_TAMPERED` and
rollback must be triggered.

---

### Rule VR-013 — Mutation Boundary Enforcement

**Rule ID:** VR-013
**Category:** Mutation Validation
**Severity:** CRITICAL
**EA Authority:** EA-003, EA-004
**Auto-enforceable:** No (architecture review)

**Requirement:**
Mutation operations must only execute within PHASE-08. The tooling
must enforce a mutation-enabled flag that is set exclusively by
the pipeline controller upon receiving a gate `AUTHORIZED` verdict
and cleared immediately when PHASE-08 completes.

Any code path that performs a write operation outside of the
mutation-enabled window must be treated as a critical
implementation defect.

Every IG must specify how its implementation enforces this
boundary, whether by flag, context manager, capability token, or
equivalent mechanism.

---

### Rule VR-014 — Failed Mutation Must Trigger Immediate Halt

**Rule ID:** VR-014
**Category:** Mutation Validation
**Severity:** CRITICAL
**EA Authority:** EA-010
**Auto-enforceable:** Yes (runtime check)

**Requirement:**
If any single mutation operation within PHASE-08 fails (raises an
exception, produces a non-zero exit code, or yields a post-mutation
hash inconsistent with the planned outcome), the pipeline controller
must:

1. Halt all remaining mutation operations immediately.
2. Record the failure in the mutation execution log.
3. Trigger the rollback protocol (EA-010).
4. Transition the pipeline to PHASE-10 for failure reporting.

Under no circumstances may the pipeline attempt to continue
mutation after a failure, skip the failed artifact and proceed,
or suppress the failure to preserve forward progress.

---------------------------------------------------------------------

## REQUIREMENT CATEGORY 3 — SCHEMA COMPLIANCE

### Rule VR-020 — All Produced Artifacts Must Be Schema-Validated

**Rule ID:** VR-020
**Category:** Schema Compliance
**Severity:** CRITICAL
**EA Authority:** EA-007
**Auto-enforceable:** Yes

**Requirement:**
Every artifact produced by the tooling (simulation reports,
mutation logs, validation reports, execution summaries) must
be validated against its declared schema before being written
to its canonical destination. Schema validation must occur
in-process, not as a post-hoc audit step.

Every IG must list all artifacts the implementation produces
and specify the schema that each artifact is validated against.

---

### Rule VR-021 — Schema Version Must Be Pinned

**Rule ID:** VR-021
**Category:** Schema Compliance
**Severity:** HIGH
**EA Authority:** EA-007, EA-008
**Auto-enforceable:** Yes

**Requirement:**
Tooling must not perform dynamic schema discovery at runtime.
Schema versions must be pinned in the implementation's
configuration at build time. The pinned schema version must
match the schema version referenced in the EP and DS artifacts
for the envelope the tooling serves.

An IG must specify every schema version pin and the config key
or constant where the pin is declared.

---

### Rule VR-022 — Schema Validation Failures Are Non-Suppressible

**Rule ID:** VR-022
**Category:** Schema Compliance
**Severity:** CRITICAL
**EA Authority:** EA-007
**Auto-enforceable:** No (code review)

**Requirement:**
Schema validation failures must never be caught and suppressed.
A schema validation exception must propagate to the pipeline
controller, which must treat it as a CRITICAL failure and trigger
the appropriate halt or rollback procedure.

Tooling must not implement try-except patterns that silently
discard schema validation errors and allow execution to continue.
Every IG must confirm this constraint in its error handling
specification.

---

### Rule VR-023 — Input Artifact Schema Validation at Phase Entry

**Rule ID:** VR-023
**Category:** Schema Compliance
**Severity:** HIGH
**EA Authority:** EA-007
**Auto-enforceable:** Yes

**Requirement:**
When a phase reads an artifact produced by a prior phase as input,
the reading phase must validate that artifact against its schema
before consuming its content. Tooling must not assume that an
artifact produced earlier in the same run is schema-valid without
re-validating.

This requirement applies to: simulation outcome records (read by
PHASE-06), mutation plans (read by PHASE-08), and validation reports
(read by PHASE-10).

---------------------------------------------------------------------

## REQUIREMENT CATEGORY 4 — GOVERNANCE ENFORCEMENT

### Rule VR-030 — EA Addenda Must Be Enforced in Code, Not Only Declared

**Rule ID:** VR-030
**Category:** Governance Enforcement
**Severity:** CRITICAL
**EA Authority:** EA-005
**Auto-enforceable:** No (architecture review)

**Requirement:**
Every EA addendum referenced in the DS Section 8 and EP governance
declarations must have a corresponding enforcement point in the
tooling implementation. Declaration of an EA rule in an artifact
without a code-level enforcement mechanism is a governance
compliance gap.

Every IG must include a governance enforcement map of the form:

| EA ID  | Rule Summary                  | Enforcing Module / Function        |
|--------|-------------------------------|------------------------------------|
| EA-001 | Artifact hash integrity        | `artifact_validator.check_hashes()` |
| EA-004 | Simulation before mutation     | `pipeline_controller.phase_gate()` |
| ...    | ...                           | ...                                |

---

### Rule VR-031 — EA-001 Hash Check Must Run at PHASE-01 and at Gate

**Rule ID:** VR-031
**Category:** Governance Enforcement
**Severity:** CRITICAL
**EA Authority:** EA-001
**Auto-enforceable:** Yes

**Requirement:**
The artifact integrity hash check mandated by EA-001 must run
at two points:
1. During PHASE-01 (Environment Initialization) — initial check
2. At the mutation gate, immediately before issuing an AUTHORIZED
   verdict (MGR-021) — re-verification

Both executions must be logged. The gate-time re-verification must
compare hashes recomputed at gate time against manifest values,
not against the PHASE-01 cached result.

---

### Rule VR-032 — EA-005 Governance Consistency Check Must Produce a Result Record

**Rule ID:** VR-032
**Category:** Governance Enforcement
**Severity:** HIGH
**EA Authority:** EA-005
**Auto-enforceable:** Yes

**Requirement:**
When the tooling executes the EA-005 governance consistency check,
the result must be persisted as a named result record (not only
a log entry). The result record must contain:

- Check timestamp
- Artifacts inspected (list)
- Conflicts detected (list, may be empty)
- Overall result: `PASSED` or `FAILED`

The mutation gate reads this result record (MGR-020). If the
record does not exist, MGR-020 fails.

---

### Rule VR-033 — Governance Violations Must Be Unambiguously Classified

**Rule ID:** VR-033
**Category:** Governance Enforcement
**Severity:** HIGH
**EA Authority:** EA-005
**Auto-enforceable:** No (code review)

**Requirement:**
When the tooling detects a governance violation (schema conflict,
unresolved cross-reference, EA rule breach), the violation must
be recorded with:

- Violation type (one of: `SCHEMA_CONFLICT`, `REFERENCE_UNRESOLVED`,
  `EA_RULE_BREACH`, `HASH_MISMATCH`, `SKIP_PROHIBITED`,
  `BOUNDARY_VIOLATION`)
- Violating artifact or module
- EA rule that was breached (if applicable)
- Recommended remediation action

Generic error messages (e.g., `"validation failed"`) without
this structured classification are not acceptable governance
violation records.

---

### Rule VR-034 — Rollback Execution Must Be Logged and Confirmed

**Rule ID:** VR-034
**Category:** Governance Enforcement
**Severity:** CRITICAL
**EA Authority:** EA-010
**Auto-enforceable:** Yes (log inspection)

**Requirement:**
When the rollback protocol is triggered (per EA-010), the tooling
must:
1. Log each rollback operation individually as it executes
2. Compute and log the post-rollback hash of each restored artifact
3. Verify the post-rollback hash matches the pre-mutation snapshot hash
4. Record the overall rollback result: `COMPLETE` or `PARTIAL`

A `PARTIAL` rollback result (where one or more artifacts could not
be fully restored) must be treated as a CRITICAL incident requiring
human intervention. The pipeline must not attempt any further
operations after a PARTIAL rollback.

---------------------------------------------------------------------

## REQUIREMENT SUMMARY TABLE

| Rule ID  | Category               | Severity | Auto-Enforceable |
|----------|------------------------|----------|------------------|
| VR-001   | Simulation Validation  | CRITICAL | No               |
| VR-002   | Simulation Validation  | CRITICAL | Yes              |
| VR-003   | Simulation Validation  | HIGH     | Yes              |
| VR-004   | Simulation Validation  | HIGH     | No               |
| VR-005   | Simulation Validation  | CRITICAL | Yes              |
| VR-010   | Mutation Validation    | CRITICAL | No               |
| VR-011   | Mutation Validation    | CRITICAL | Yes              |
| VR-012   | Mutation Validation    | HIGH     | Yes              |
| VR-013   | Mutation Validation    | CRITICAL | No               |
| VR-014   | Mutation Validation    | CRITICAL | Yes              |
| VR-020   | Schema Compliance      | CRITICAL | Yes              |
| VR-021   | Schema Compliance      | HIGH     | Yes              |
| VR-022   | Schema Compliance      | CRITICAL | No               |
| VR-023   | Schema Compliance      | HIGH     | Yes              |
| VR-030   | Governance Enforcement | CRITICAL | No               |
| VR-031   | Governance Enforcement | CRITICAL | Yes              |
| VR-032   | Governance Enforcement | HIGH     | Yes              |
| VR-033   | Governance Enforcement | HIGH     | No               |
| VR-034   | Governance Enforcement | CRITICAL | Yes              |

**Total rules:** 19
**CRITICAL:** 11 | **HIGH:** 8

---------------------------------------------------------------------

## VERSION HISTORY

| Version | Date       | Author    | Change Summary            |
|---------|------------|-----------|---------------------------|
| 1.0     | 2026-03-12 | Architect | Initial canonical release |
