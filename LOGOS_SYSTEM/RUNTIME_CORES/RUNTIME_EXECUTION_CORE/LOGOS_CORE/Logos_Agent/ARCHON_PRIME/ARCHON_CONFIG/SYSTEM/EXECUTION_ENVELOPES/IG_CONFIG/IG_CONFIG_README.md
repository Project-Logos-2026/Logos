SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: IG_Configuration
ARTIFACT_NAME: IG_CONFIG_README
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelopes / IG_CONFIG
STATUS: Active

---------------------------------------------------------------------

# IG_CONFIG — Implementation Guide Configuration Layer README

## What This Directory Is

The `IG_CONFIG` directory is the canonical configuration layer for
**Implementation Guide (IG) artifacts** within ARCHON_PRIME
Execution Envelopes. It defines the implementation requirements,
tooling architecture expectations, and validation obligations that
every IG artifact must specify for its associated tooling.

This directory is part of the Execution Envelope configuration
subsystem located at:

```
AP_SYSTEM_CONFIG/SYSTEM/EXECUTION_ENVELOPES/
```

---------------------------------------------------------------------

## What an Implementation Guide (IG) Is

An ARCHON_PRIME Execution Envelope consists of four artifact types:

| Artifact Type        | Code | Purpose                                    |
|----------------------|------|--------------------------------------------|
| Design Specification | DS   | Defines the problem, scope, and intent     |
| Execution Plan       | EP   | Defines the ordered phases of execution    |
| Implementation Guide | IG   | Specifies how tooling implements the plan  |
| Execution Attributes | EA   | Defines runtime governance rules           |

The **IG artifact** is the implementation contract of the bundle.

- It specifies which modules, classes, and functions implement
  each execution phase.
- It defines how the tooling loads configuration, handles errors,
  routes artifacts, and enforces governance rules at the code level.
- It maps each EA addendum to the specific enforcement point in
  the implementation.
- It is the authoritative reference for reviewers verifying that
  the tooling faithfully implements the EP.

An IG does not describe what the pipeline should accomplish (that
is the DS and EP's role). It describes how the implementation
accomplishes it.

---------------------------------------------------------------------

## What the IG_CONFIG Layer Governs

The IG_CONFIG layer does not contain IG artifacts. It contains the
**configuration artifacts that define what every IG must address**,
how tooling must be architecturally organized, and what validation
behaviors the implementation must exhibit.

The IG_CONFIG layer answers three questions for every IG author:

1. **What must the implementation accomplish?** — Implementation Requirements
2. **How must the tooling be built?** — Tooling Requirements
3. **What must the tooling verify?** — Validation Requirements

---------------------------------------------------------------------

## Files in This Directory

### IG_CONFIG_IMPLEMENTATION_REQUIREMENTS.md

**Purpose:** Defines functional requirements that every IG must
specify for its tooling implementation.

This file covers four requirement categories:
- **Module Categories** (IR-001 through IR-006): The canonical
  module categories every implementation must declare (controller,
  simulation, mutation, validation, artifact router, reporting),
  plus module registration and separation rules.
- **Execution Environment Compatibility** (IR-010 through IR-013):
  Python version constraints, dependency declaration, environment
  isolation, and cross-platform path handling.
- **Logging Requirements** (IR-020 through IR-024): Mandatory
  logging at phase boundaries, per-operation mutation logging,
  structured log format, log rotation and retention.
- **Artifact Routing Requirements** (IR-030 through IR-033):
  Artifact router mandatory use, canonical destination enforcement,
  forbidden in-place writes, and routing manifest requirements.

---

### IG_CONFIG_TOOLING_REQUIREMENTS.md

**Purpose:** Defines code-level architectural and behavioral
requirements that every IG must specify for its tooling.

This file covers four requirement categories:
- **Module Architecture** (TR-001 through TR-005): Pipeline
  controller pattern, phase class interface contract, no global
  mutable state, dependency injection for phase dependencies, and
  module import discipline.
- **Configuration Loading** (TR-010 through TR-014): Configuration
  loaded from canonical sources, no hardcoded paths or values,
  configuration schema validation at load time, immutable config
  at runtime, environment variable override rules.
- **Error Handling** (TR-020 through TR-025): Classified exception
  hierarchy, no bare except clauses, fatal vs recoverable
  classification, error propagation to pipeline controller, error
  context preservation, and prohibition on silent failure.
- **Deterministic Execution Support** (TR-030 through TR-034):
  No random or time-dependent execution paths, fixed iteration
  order, idempotent phase design, no side effects outside declared
  output targets, and reproducible artifact output.

---

### IG_CONFIG_VALIDATION_REQUIREMENTS.md

**Purpose:** Defines the validation behaviors that every IG must
specify its tooling to implement.

This file covers four requirement categories:
- **Simulation Validation** (VR-001 through VR-005): Simulation
  layer independence from mutation executor, 100% coverage of
  in-scope targets, severity classification rules for outcomes,
  immutability of simulation results, and simulation validation
  report as a mandatory first-class artifact.
- **Mutation Validation** (VR-010 through VR-014): Pre-mutation
  state snapshots, per-operation mutation logging, post-mutation
  hash recording, mutation boundary enforcement, and immediate
  halt on any mutation failure.
- **Schema Compliance** (VR-020 through VR-023): All produced
  artifacts validated against schema before routing, schema
  version pinning, non-suppressible schema validation failures,
  and input artifact re-validation at phase entry.
- **Governance Enforcement** (VR-030 through VR-034): EA addenda
  must be enforced in code with a governance map, EA-001 hash
  check at PHASE-01 and at the mutation gate, EA-005 governance
  check must produce a named result record, governance violations
  must be structurally classified, and EA-010 rollback execution
  must be individually logged and confirmed.

---

### IG_CONFIG_README.md

**Purpose:** This file. Explains the IG_CONFIG layer and its role
within the Execution Envelope governance system.

---------------------------------------------------------------------

## How IG_CONFIG Fits into the Execution Envelope System

```
EXECUTION_ENVELOPES/
├── DS_CONFIG/          ← Governs DS artifacts (structure + validation)
├── EA_CONFIG/          ← Governs EA addenda (runtime governance rules)
├── EP_CONFIG/          ← Governs EP artifacts (phase model + ordering)
├── IG_CONFIG/          ← Governs IG artifacts (this directory)
├── EE_SCHEMAS/         ← JSON schemas for all artifact types
└── VALIDATION/         ← Validation infrastructure and reports
```

IG_CONFIG sits downstream of EP_CONFIG in the artifact lifecycle.
An EP must be compiled and structure-validated before an IG is
authored. The IG translates the EP's phase sequence into concrete
module-level implementation specifications.

```
DS (validated) → EP (compiled) → IG (authored)
                                     ↓
                              IG_CONFIG rules applied
                                     ↓
                              Tooling implemented
                                     ↓
                              Execution begins
```

---------------------------------------------------------------------

## IG Artifact Lifecycle and IG_CONFIG Touch Points

```
EP COMPILED AND STRUCTURE-VALIDATED
             │
             ▼
AUTHOR IG ARTIFACT
             │
             ▼
Check implementation requirements  ← IG_CONFIG_IMPLEMENTATION_REQUIREMENTS.md
             │                        (module categories, env compat,
             │                         logging, artifact routing)
             ▼
Check tooling requirements         ← IG_CONFIG_TOOLING_REQUIREMENTS.md
             │                        (architecture, config loading,
             │                         error handling, determinism)
             ▼
Check validation requirements      ← IG_CONFIG_VALIDATION_REQUIREMENTS.md
             │                        (simulation, mutation, schema,
             │                         governance enforcement)
             ▼
IG REVIEW PASSED → STATUS: approved
             │
             ▼
TOOLING IMPLEMENTED per IG
             │
             ▼
ENVELOPE EXECUTES
```

---------------------------------------------------------------------

## Mandatory IG Content Checklist

Every IG artifact must address the following topics to be
considered complete by IG_CONFIG standards:

| # | Required IG Content Item                              | Source Rule |
|---|-------------------------------------------------------|-------------|
| 1 | Module category declaration (all 6 canonical types)   | IR-001      |
| 2 | Python version and dependency declaration              | IR-010, IR-011 |
| 3 | Log format specification                              | IR-023      |
| 4 | Artifact routing table (all produced artifacts)       | IR-033      |
| 5 | Pipeline controller module identified                 | TR-001      |
| 6 | Phase class interface specification                   | TR-002      |
| 7 | Configuration source and schema reference             | TR-010, TR-011 |
| 8 | Exception hierarchy specification                     | TR-020      |
| 9 | EA governance enforcement map                         | VR-030      |
| 10 | Simulation layer independence confirmation            | VR-001      |
| 11 | Pre-mutation snapshot mechanism specification         | VR-010      |
| 12 | Schema version pin table (all artifacts)              | VR-021      |
| 13 | Rollback mechanism specification                      | VR-034      |

An IG that does not address all 13 items must be returned for
revision before it is approved.

---------------------------------------------------------------------

## Key Constraints Summary

| Constraint                                             | Source          |
|--------------------------------------------------------|-----------------|
| Simulation layer must be isolated from mutation        | VR-001, TR-001  |
| No global mutable state in tooling                     | TR-003          |
| No hardcoded paths or schema versions                  | TR-011, VR-021  |
| No bare except clauses                                 | TR-021          |
| No silent failure                                      | TR-025, VR-022  |
| No mutation outside PHASE-08 mutation window           | VR-013          |
| No continuation after mutation failure                 | VR-014          |
| Schema validation must occur before artifact routing   | VR-020          |
| Rollback must be logged per operation                  | VR-034          |
| Governance must be enforced in code, not only declared | VR-030          |

---------------------------------------------------------------------

## Updating This Configuration Layer

Changes to IG_CONFIG artifacts require Architect-level authority.
Any modification must:

1. Not weaken validation requirements (VR rules).
2. Not remove mandatory module categories (IR-001).
3. Not relax the mutation boundary constraint (VR-013).
4. Increment the `VERSION` field in the affected configuration file.
5. Be recorded in the file's Version History table.

---------------------------------------------------------------------

## Related Artifacts

| Artifact                              | Location                                           |
|---------------------------------------|----------------------------------------------------|
| Implementation Requirements           | IG_CONFIG/IG_CONFIG_IMPLEMENTATION_REQUIREMENTS.md |
| Tooling Requirements                  | IG_CONFIG/IG_CONFIG_TOOLING_REQUIREMENTS.md        |
| Validation Requirements               | IG_CONFIG/IG_CONFIG_VALIDATION_REQUIREMENTS.md     |
| EP Phase Model                        | EP_CONFIG/EP_CONFIG_PHASE_MODEL.md                 |
| EP Mutation Gate Rules                | EP_CONFIG/EP_CONFIG_MUTATION_GATE_RULES.md         |
| EA-004 Simulation First Rule          | EA_CONFIG/EA-004_SIMULATION_FIRST_RULE.md          |
| EA-010 Failure Rollback Protocol      | EA_CONFIG/EA-010_FAILURE_ROLLBACK_PROTOCOL.md      |
| DS Configuration Layer                | DS_CONFIG/DS_CONFIG_README.md                      |

---------------------------------------------------------------------

## VERSION HISTORY

| Version | Date       | Author    | Change Summary            |
|---------|------------|-----------|---------------------------|
| 1.0     | 2026-03-12 | Architect | Initial canonical release |
