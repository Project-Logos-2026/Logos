SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: EP_Configuration
ARTIFACT_NAME: EP_CONFIG_README
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelopes / EP_CONFIG
STATUS: Active

---------------------------------------------------------------------

# EP_CONFIG — Execution Plan Configuration Layer README

## What This Directory Is

The `EP_CONFIG` directory is the canonical configuration layer for
**Execution Plan (EP) artifacts** within ARCHON_PRIME Execution
Envelopes. It defines the pipeline phase model, execution ordering
rules, and mutation gate conditions that every EP artifact must
comply with.

This directory is part of the Execution Envelope configuration
subsystem located at:

```
AP_SYSTEM_CONFIG/SYSTEM/EXECUTION_ENVELOPES/
```

---------------------------------------------------------------------

## What an Execution Plan (EP) Is

In an ARCHON_PRIME Execution Envelope, four artifact types work
together:

| Artifact Type        | Code | Purpose                                 |
|----------------------|------|-----------------------------------------|
| Design Specification | DS   | Defines problem, scope, and intent      |
| Execution Plan       | EP   | Defines the ordered phases of execution |
| Implementation Guide | IG   | Provides implementation-level detail    |
| Execution Attributes | EA   | Defines runtime governance rules        |

The **EP artifact** is the operational artifact of the bundle.

- It specifies exactly which phases the execution pipeline runs.
- It defines the sequence and dependencies of those phases.
- It must be consistent with the DS's phase overview and with the
  envelope manifest's `execution_phases` array.
- It is compiled only after the DS has been validated and approved.

No execution may begin without a valid, schema-conformant EP artifact
that declares a complete canonical phase sequence.

---------------------------------------------------------------------

## What the EP_CONFIG Layer Governs

The EP_CONFIG layer does not contain EP artifacts. It contains the
**configuration artifacts that define how all EP artifacts must
structure their execution pipeline, enforce ordering, and gate
mutation phases**.

The EP_CONFIG layer answers three questions for every EP:

1. **What phases must exist?** — defined in the Phase Model
2. **In what order must they run?** — defined in the Execution Order Rules
3. **What must be true before mutations are allowed?** — defined in the Mutation Gate Rules

---------------------------------------------------------------------

## Files in This Directory

### EP_CONFIG_PHASE_MODEL.md

**Purpose:** Defines the canonical ten-phase execution pipeline.

Every EP artifact must declare all ten phases in the order
specified here. This file defines each phase's:
- Canonical name and code (PHASE-01 through PHASE-10)
- Category (Setup / Analysis / Simulation / Planning / Mutation /
  Validation / Reporting)
- Purpose statement
- Required inputs
- Required outputs
- Gate conditions
- Prohibited actions
- EA governance mappings

The Phase Model is the authoritative reference for what phases
exist and what each phase must accomplish.

---

### EP_CONFIG_EXECUTION_ORDER_RULES.md

**Purpose:** Defines deterministic ordering requirements, phase
dependency rules, skip prohibitions, and required validation
checkpoints.

This file specifies:
- **Phase dependency rules** (EOR-001 through EOR-003): How each
  phase depends on its predecessor, single-predecessor constraint,
  and completion status persistence.
- **Skip prohibition rules** (EOR-010 through EOR-014): Which
  phases can never be skipped under any circumstances. PHASE-05
  and PHASE-06 (simulation phases) are absolutely non-skippable
  per EA-004.
- **Validation checkpoint rules** (EOR-020 through EOR-023): Four
  mandatory checkpoints that must pass at defined pipeline positions
  before the next phase group may proceed.
- **Structural rules** (EOR-030 through EOR-031): How EP artifacts
  must declare their phase sequence and how that declaration must
  be consistent with the envelope manifest.

---

### EP_CONFIG_MUTATION_GATE_RULES.md

**Purpose:** Defines the complete set of conditions that must be
satisfied before PHASE-08 (Controlled Mutation) is authorized.

The mutation gate is positioned between PHASE-06 (Simulation
Validation) and PHASE-07 (Mutation Planning). It is the primary
safety control point in the execution pipeline.

This file specifies 13 gate rules across three categories:
- **Simulation conditions** (MGR-001 through MGR-004): Simulation
  must be completed, non-empty, and free of critical failures.
- **Validation conditions** (MGR-010 through MGR-013): Simulation
  validation must pass, DS success criteria must be satisfied.
- **Governance conditions** (MGR-020 through MGR-024): EA-005
  governance check, EA-001 hash integrity, EA-002 router active,
  EA-010 rollback armed, EA-003 order locked.

All 13 rules must pass for the gate to issue an `AUTHORIZED`
verdict. Any single failure produces a `BLOCKED` verdict and
routes execution to PHASE-10 for failure reporting.

---

### EP_CONFIG_README.md

**Purpose:** This file. Explains the EP_CONFIG layer and its role
within the Execution Envelope governance system.

---------------------------------------------------------------------

## How EP_CONFIG Fits into the Execution Envelope System

```
EXECUTION_ENVELOPES/
├── DS_CONFIG/          ← Governs DS artifacts (structure + validation)
├── EA_CONFIG/          ← Governs EA addenda (runtime rules)
├── EP_CONFIG/          ← Governs EP artifacts (this directory)
├── IG_CONFIG/          ← Governs IG artifacts
├── EE_SCHEMAS/         ← JSON schemas for all artifact types
└── VALIDATION/         ← Validation infrastructure and reports
```

EP_CONFIG is downstream of DS_CONFIG in the artifact lifecycle:
a DS must be validated before an EP is compiled. EP_CONFIG rules
apply at EP compilation time (structural rules) and at execution
time (ordering and gate rules).

---------------------------------------------------------------------

## EP Artifact Lifecycle and EP_CONFIG Touch Points

```
DS VALIDATED AND APPROVED
         │
         ▼
COMPILE EP ARTIFACT
         │
         ▼
Check phase sequence declared   ← EP_CONFIG_PHASE_MODEL.md
         │                         EP_CONFIG_EXECUTION_ORDER_RULES.md (EOR-030)
         ▼
Check manifest consistency      ← EP_CONFIG_EXECUTION_ORDER_RULES.md (EOR-031)
         │
         ▼
EP STRUCTURAL VALIDATION PASSED
         │
         ▼
BEGIN EXECUTION
         │
         ▼
PHASE-01 → PHASE-04             ← Checkpoint EOR-020, EOR-021 enforced
         │
         ▼
PHASE-05 → PHASE-06             ← Simulation phases (EOR-010 enforces
         │                         skip prohibition)
         ▼
MUTATION GATE EVALUATION        ← EP_CONFIG_MUTATION_GATE_RULES.md
         │                         (13 rules, AUTHORIZED or BLOCKED)
    ┌────┴────┐
    │         │
AUTHORIZED BLOCKED
    │         │
PHASE-07  PHASE-10
to         (Failure
PHASE-09   Report)
    │
    ▼
PHASE-10 (Reporting)            ← Checkpoint EOR-023 enforced
```

---------------------------------------------------------------------

## Key Invariants

The EP_CONFIG layer enforces the following invariants for all
ARCHON_PRIME execution:

| # | Invariant                                                          | Source                     |
|---|-------------------------------------------------------------------|----------------------------|
| 1 | Simulation always precedes mutation                               | EA-004, MGR-001, EOR-010   |
| 2 | Mutation never occurs without a gate AUTHORIZED verdict            | MGR (all)                  |
| 3 | No phase may be skipped                                           | EOR-010 through EOR-014    |
| 4 | Execution order is deterministic and locked                       | EA-003, EOR-001, MGR-024   |
| 5 | Rollback must be armed before any mutation phase begins           | EA-010, MGR-023            |
| 6 | Artifact integrity is re-verified at the mutation gate            | EA-001, MGR-021            |
| 7 | Reporting always executes regardless of prior phase outcomes      | EOR-013, PHASE-10 model    |
| 8 | Phase completion status is always persisted before advancing      | EOR-003                    |

---------------------------------------------------------------------

## Updating This Configuration Layer

Changes to EP_CONFIG artifacts require Architect-level authority.
Any modification must:

1. Not reduce the number of mandatory phases.
2. Not relax mutation gate conditions.
3. Not introduce skip pathways for simulation phases.
4. Increment the `VERSION` field in the affected configuration file.
5. Be recorded in the file's Version History table.

The mutation gate (EP_CONFIG_MUTATION_GATE_RULES.md) is the most
safety-critical artifact in this directory. Changes to gate rule
conditions require explicit dual review before taking effect.

---------------------------------------------------------------------

## Related Artifacts

| Artifact                              | Location                                  |
|---------------------------------------|-------------------------------------------|
| Phase Model                           | EP_CONFIG/EP_CONFIG_PHASE_MODEL.md        |
| Execution Order Rules                 | EP_CONFIG/EP_CONFIG_EXECUTION_ORDER_RULES.md |
| Mutation Gate Rules                   | EP_CONFIG/EP_CONFIG_MUTATION_GATE_RULES.md |
| EA-003 Deterministic Ordering         | EA_CONFIG/EA-003_DETERMINISTIC_EXECUTION_ORDERING.md |
| EA-004 Simulation First Rule          | EA_CONFIG/EA-004_SIMULATION_FIRST_RULE.md |
| EA-010 Failure Rollback Protocol      | EA_CONFIG/EA-010_FAILURE_ROLLBACK_PROTOCOL.md |
| Execution Envelope Manifest Schema    | EE_SCHEMAS/EXECUTION_ENVELOPE_SCHEMA.json |
| DS Configuration Layer                | DS_CONFIG/DS_CONFIG_README.md             |

---------------------------------------------------------------------

## VERSION HISTORY

| Version | Date       | Author    | Change Summary            |
|---------|------------|-----------|---------------------------|
| 1.0     | 2026-03-12 | Architect | Initial canonical release |
