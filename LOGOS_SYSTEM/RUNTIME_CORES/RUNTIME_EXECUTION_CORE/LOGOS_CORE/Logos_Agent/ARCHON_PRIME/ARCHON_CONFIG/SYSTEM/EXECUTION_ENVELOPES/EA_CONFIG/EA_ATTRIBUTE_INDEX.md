SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: EP_Configuration
ARTIFACT_NAME: EA_ATTRIBUTE_INDEX
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelopes / EA_CONFIG
STATUS: Active

---------------------------------------------------------------------

# EA_CONFIG — Execution Attribute Index

## Purpose

This index provides a quick-reference registry for all ten canonical
Execution Attribute (EA) addenda that govern ARCHON_PRIME Execution
Envelopes. Each entry identifies the EA's title, governing domain,
enforcement scope, and primary verification criterion.

For full rule text, refer to the individual EA artifact files.

---------------------------------------------------------------------

## EA ADDENDA REGISTRY

| EA ID  | Title                              | Domain             | Severity     |
|--------|------------------------------------|--------------------|--------------|
| EA-001 | Envelope Target Integrity          | Artifact Identity  | CRITICAL     |
| EA-002 | Artifact Router Enforcement        | Artifact Routing   | CRITICAL     |
| EA-003 | Deterministic Execution Ordering   | Execution Control  | CRITICAL     |
| EA-004 | Simulation First Rule              | Safety             | CRITICAL     |
| EA-005 | Governance Consistency Check       | Governance         | CRITICAL     |
| EA-006 | Execution Logging Requirements     | Observability      | HIGH         |
| EA-007 | Artifact Metadata Schema Enforcement | Schema Compliance | HIGH        |
| EA-008 | Envelope Manifest Contract         | Manifest Integrity | HIGH         |
| EA-009 | Prompt Compiler Integration        | Tooling            | MEDIUM       |
| EA-010 | Failure Rollback Protocol          | Safety / Recovery  | CRITICAL     |

---------------------------------------------------------------------

## EA-001 — Envelope Target Integrity

**File:** `EA-001_ENVELOPE_TARGET_INTEGRITY.md`
**Domain:** Artifact Identity
**Severity:** CRITICAL

**Rule Summary:**
Execution envelopes must explicitly declare the artifact identities
(filenames and SHA-256 hashes) of the DS, IG, and EP artifacts they
target. Any mismatch between manifest artifact hashes and runtime
artifact hashes must halt execution immediately.

**Enforcement Scope:**
- PHASE-01 (Environment Initialization) — initial hash check
- Mutation Gate — re-verification before AUTHORIZED verdict (MGR-021)

**Primary Verification Criterion:** EA-V-001
- Method: Envelope manifest hash comparison against runtime artifacts
- Pass Condition: All DS, IG, and EP artifact hashes match manifest

**Cross-Referenced By:** DSV-010, DSV-011, MGR-021, VR-031, EOR-020

---------------------------------------------------------------------

## EA-002 — Artifact Router Enforcement

**File:** `EA-002_ARTIFACT_ROUTER_ENFORCEMENT.md`
**Domain:** Artifact Routing
**Severity:** CRITICAL

**Rule Summary:**
All artifacts produced during execution must be routed through the
canonical artifact router. Direct file writes to non-canonical
paths are prohibited. The artifact router must be validated as
active before mutation phases begin.

**Enforcement Scope:**
- All phases that produce output artifacts (PHASE-02 through PHASE-10)
- Mutation gate check (MGR-022)

**Primary Verification Criterion:** EA-V-002
- Method: Artifact router audit of output destinations
- Pass Condition: All produced artifacts written to canonical paths

**Cross-Referenced By:** IR-030, IR-031, IR-032, MGR-022, EOR-007

---------------------------------------------------------------------

## EA-003 — Deterministic Execution Ordering

**File:** `EA-003_DETERMINISTIC_EXECUTION_ORDERING.md`
**Domain:** Execution Control
**Severity:** CRITICAL

**Rule Summary:**
Execution plans must define a strict deterministic phase order.
The seven canonical phases must appear in the specified sequence.
Reordering or omission of phases is prohibited.

**Canonical Phase Order (EA-003 definition):**
```
Phase_1: Environment_Verification
Phase_2: Artifact_Discovery
Phase_3: Static_Analysis
Phase_4: Simulation_Pass
Phase_5: Controlled_Mutation
Phase_6: Validation
Phase_7: Reporting
```

**Note:** The EP_CONFIG phase model expands this to ten phases for
implementation precision. EA-003 defines the invariant ordering
principle; EP_CONFIG_PHASE_MODEL.md provides the canonical
ten-phase expansion.

**Primary Verification Criterion:** EA-V-003
- Method: Execution plan structural validation
- Pass Condition: All phases present and ordered as specified

**Cross-Referenced By:** EOR-001, EOR-002, EOR-010, EOR-030, MGR-024, TR-030

---------------------------------------------------------------------

## EA-004 — Simulation First Rule

**File:** `EA-004_SIMULATION_FIRST_RULE.md`
**Domain:** Safety
**Severity:** CRITICAL

**Rule Summary:**
Execution envelopes must perform a complete simulation pass before
any mutation operations execute. The required order is:

```
simulate() → validate() → mutate()
```

Mutation is prohibited until simulation validation succeeds.
This rule is non-bypassable — no configuration flag or runtime
argument may skip or disable simulation.

**Enforcement Scope:**
- PHASE-05 (Simulation Pass) — mandatory phase
- PHASE-06 (Simulation Validation) — mandatory gate
- Mutation gate (MGR-001 through MGR-004)

**Primary Verification Criterion:** EA-V-004
- Method: Execution log inspection
- Pass Condition: Simulation phase executed and validated prior to mutation

**Cross-Referenced By:** EOR-010, MGR-001, MGR-002, MGR-003, MGR-004,
  DSV-041, VR-001, VR-002, VR-013

---------------------------------------------------------------------

## EA-005 — Governance Consistency Check

**File:** `EA-005_GOVERNANCE_CONSISTENCY_CHECK.md`
**Domain:** Governance
**Severity:** CRITICAL

**Rule Summary:**
Before execution begins, the system must verify governance artifact
consistency across: (1) Execution Envelope artifacts, (2) Workflow
configuration artifacts, (3) Governance protocol artifacts. Checks
include metadata header validation, schema compatibility, and
cross-reference resolution. Execution must halt if any governance
conflict is detected.

**Enforcement Scope:**
- PHASE-01 (Environment Initialization)
- PHASE-06 (Simulation Validation)
- Mutation gate (MGR-020)

**Primary Verification Criterion:** EA-V-005
- Method: Metadata scanner and schema validator
- Pass Condition: No schema conflicts or unresolved references

**Cross-Referenced By:** DSV-040, MGR-020, VR-030, VR-032, VR-033, EOR-020

---------------------------------------------------------------------

## EA-006 — Execution Logging Requirements

**File:** `EA-006_EXECUTION_LOGGING_REQUIREMENTS.md`
**Domain:** Observability
**Severity:** HIGH

**Rule Summary:**
All execution phases must produce structured log entries. Logging
is mandatory at phase entry, phase exit, each mutation operation,
each validation check, and each governance event. Log entries must
be immutable once written. Log artifacts are first-class outputs
routed through the artifact router.

**Enforcement Scope:**
- All ten canonical phases
- Per-operation logging in PHASE-08

**Primary Verification Criterion:** EA-V-006
- Method: Log artifact completeness audit
- Pass Condition: All phases and operations have corresponding log entries

**Cross-Referenced By:** IR-020, IR-021, IR-022, IR-023, VR-011, EOR-003,
  MGR-004, MGR-012

---------------------------------------------------------------------

## EA-007 — Artifact Metadata Schema Enforcement

**File:** `EA-007_ARTIFACT_METADATA_SCHEMA_ENFORCEMENT.md`
**Domain:** Schema Compliance
**Severity:** HIGH

**Rule Summary:**
All artifacts produced by execution envelope tooling must conform
to their declared schema before being written to their canonical
destination. Schema validation must occur in-process. Schema
versions must be pinned. Schema validation failures must propagate
as CRITICAL errors — they must not be caught and suppressed.

**Enforcement Scope:**
- All phases that produce output artifacts
- Input artifact validation at phase entry

**Primary Verification Criterion:** EA-V-007
- Method: Schema validation at artifact write time
- Pass Condition: All produced artifacts pass schema validation

**Cross-Referenced By:** DSV-020, DSV-021, VR-020, VR-021, VR-022, VR-023,
  EOR-020, MGR-007

---------------------------------------------------------------------

## EA-008 — Envelope Manifest Contract

**File:** `EA-008_ENVELOPE_MANIFEST_CONTRACT.md`
**Domain:** Manifest Integrity
**Severity:** HIGH

**Rule Summary:**
Every execution envelope must have a valid `ENVELOPE_MANIFEST.json`
conforming to the manifest schema. The manifest is the authoritative
source of artifact bundle identity, execution phase declarations,
and EA addenda references. Any EP or DS artifact that conflicts
with the manifest must be resolved before execution.

**Enforcement Scope:**
- PHASE-01 (Environment Initialization)
- PHASE-10 (Reporting)

**Primary Verification Criterion:** EA-V-008
- Method: Manifest schema validation and artifact bundle reconciliation
- Pass Condition: Manifest valid and all declared artifacts present

**Cross-Referenced By:** DSV-012, DSV-013, EOR-031, VR-021

---------------------------------------------------------------------

## EA-009 — Prompt Compiler Integration

**File:** `EA-009_PROMPT_COMPILER_INTEGRATION.md`
**Domain:** Tooling
**Severity:** MEDIUM

**Rule Summary:**
Execution envelope tooling must declare compatibility with the
ARCHON_PRIME prompt compiler. Prompts used by the tooling must be
compiled through the prompt compiler rather than constructed
inline at runtime. Compiled prompts are treated as versioned
artifacts subject to manifest tracking.

**Enforcement Scope:**
- Implementation modules that generate or consume prompts

**Primary Verification Criterion:** EA-V-009
- Method: Prompt compilation audit
- Pass Condition: All runtime prompts sourced from compiled prompt artifacts

**Cross-Referenced By:** TR-034

---------------------------------------------------------------------

## EA-010 — Failure Rollback Protocol

**File:** `EA-010_FAILURE_ROLLBACK_PROTOCOL.md`
**Domain:** Safety / Recovery
**Severity:** CRITICAL

**Rule Summary:**
Execution envelopes must define a rollback protocol for mutation
failure. On failure: (1) halt execution immediately, (2) restore
pre-mutation artifact state, (3) record rollback event in execution
logs, (4) generate failure report. Rollback is triggered by:
validation failure, artifact integrity mismatch, or governance
rule violation.

**Enforcement Scope:**
- PHASE-08 (Controlled Mutation) — rollback must be armed before start
- Mutation gate (MGR-023) — confirms rollback mechanism is armed

**Primary Verification Criterion:** EA-V-010
- Method: Failure simulation test
- Pass Condition: Repository state restored successfully after failure

**Cross-Referenced By:** DSV-042, MGR-023, VR-010, VR-014, VR-034, EOR-022

---------------------------------------------------------------------

## CROSS-REFERENCE MATRIX — EA to Rule Systems

| EA ID  | DSV Rules              | EOR Rules           | MGR Rules          | IR/TR/VR Rules                    |
|--------|------------------------|---------------------|--------------------|-----------------------------------|
| EA-001 | DSV-010, DSV-011       | EOR-020             | MGR-021            | VR-031                            |
| EA-002 | —                      | —                   | MGR-022            | IR-030, IR-031, IR-032            |
| EA-003 | —                      | EOR-001, EOR-010,   | MGR-024            | TR-030, TR-033                    |
|        |                        | EOR-030, EOR-031    |                    |                                   |
| EA-004 | DSV-041                | EOR-010, EOR-021    | MGR-001–004        | VR-001, VR-002, VR-013            |
| EA-005 | DSV-040                | EOR-020             | MGR-020            | VR-030, VR-032, VR-033            |
| EA-006 | —                      | EOR-003             | MGR-004, MGR-012   | IR-020–023, VR-011                |
| EA-007 | DSV-020–023            | EOR-020             | —                  | VR-020–023                        |
| EA-008 | DSV-012, DSV-013       | EOR-031             | —                  | VR-021                            |
| EA-009 | —                      | —                   | —                  | TR-034                            |
| EA-010 | DSV-042                | EOR-022             | MGR-023            | VR-010, VR-014, VR-034            |

---------------------------------------------------------------------

## VERSION HISTORY

| Version | Date       | Author    | Change Summary            |
|---------|------------|-----------|---------------------------|
| 1.0     | 2026-03-12 | Architect | Initial canonical release |
