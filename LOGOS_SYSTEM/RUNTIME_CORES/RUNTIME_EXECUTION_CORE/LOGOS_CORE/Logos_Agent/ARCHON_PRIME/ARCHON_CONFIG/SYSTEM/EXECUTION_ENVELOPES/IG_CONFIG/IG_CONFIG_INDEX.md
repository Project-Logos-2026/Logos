SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: IG_Configuration
ARTIFACT_NAME: IG_CONFIG_INDEX
VERSION: 1.0
DATE: 2026-03-12
AUTHORITY: Architect
SUBSYSTEM: Execution_Envelopes / IG_CONFIG
STATUS: Active

---------------------------------------------------------------------

# IG_CONFIG — Configuration Artifact Index

## Purpose

This index provides a complete reference for all artifacts in the
IG_CONFIG layer, all rules defined across those artifacts, and
cross-reference maps between rule categories and EA addenda.

---------------------------------------------------------------------

## ARTIFACT REGISTRY

| Artifact                                  | Purpose                                               | Rules Defined |
|-------------------------------------------|-------------------------------------------------------|---------------|
| IG_CONFIG_IMPLEMENTATION_REQUIREMENTS.md  | Module categories, env compat, logging, routing       | IR-001–033    |
| IG_CONFIG_TOOLING_REQUIREMENTS.md         | Architecture, config loading, error handling, determinism | TR-001–034 |
| IG_CONFIG_VALIDATION_REQUIREMENTS.md      | Simulation, mutation, schema, governance validation   | VR-001–034    |
| IG_CONFIG_README.md                       | Layer overview, mandatory content checklist           | (reference)   |
| IG_CONFIG_INDEX.md                        | This file — complete index                            | (index)       |

---------------------------------------------------------------------

## SECTION 1 — IMPLEMENTATION REQUIREMENTS (IR)

Defined in: `IG_CONFIG_IMPLEMENTATION_REQUIREMENTS.md`

### Category 1 — Module Categories

| Rule ID | Rule Title                              | Severity | EA Authority |
|---------|-----------------------------------------|----------|--------------|
| IR-001  | Required Module Category Declaration    | CRITICAL | EA-007       |
| IR-002  | Module Category to Phase Alignment      | HIGH     | EA-003       |
| IR-003  | Prohibited Module Coupling              | HIGH     | EA-004       |

**Canonical module categories (IR-001):**
```
controller | simulation | mutation | validation | artifact_router | reporting
```

### Category 2 — Execution Environment Compatibility

| Rule ID | Rule Title                              | Severity | EA Authority |
|---------|-----------------------------------------|----------|--------------|
| IR-010  | Canonical Environment Declaration       | HIGH     | EA-007       |
| IR-011  | Environment Verification Module Required | HIGH    | EA-005       |
| IR-012  | Configuration Loading from Canonical Config Path | MEDIUM | EA-008  |
| IR-013  | Isolation of Simulation from Live Execution Context | CRITICAL | EA-004 |

### Category 3 — Logging Requirements

| Rule ID | Rule Title                              | Severity | EA Authority |
|---------|-----------------------------------------|----------|--------------|
| IR-020  | Structured Log Format Required          | HIGH     | EA-006       |
| IR-021  | Log Output Path Compliance              | HIGH     | EA-006       |
| IR-022  | Log Entry Immutability                  | HIGH     | EA-006       |
| IR-023  | Rollback Events Must Be Logged          | CRITICAL | EA-010       |

### Category 4 — Artifact Routing Requirements

| Rule ID | Rule Title                              | Severity | EA Authority |
|---------|-----------------------------------------|----------|--------------|
| IR-030  | All Writes Must Pass Through Artifact Router | CRITICAL | EA-002  |
| IR-031  | Canonical Output Path Declaration       | HIGH     | EA-002       |
| IR-032  | Write Path Validation Before Execution  | HIGH     | EA-002       |
| IR-033  | Artifact Identity Recorded at Write Time | HIGH    | EA-007       |

---------------------------------------------------------------------

## SECTION 2 — TOOLING REQUIREMENTS (TR)

Defined in: `IG_CONFIG_TOOLING_REQUIREMENTS.md`

### Category 1 — Module Architecture

| Rule ID | Rule Title                              | Severity | EA Authority |
|---------|-----------------------------------------|----------|--------------|
| TR-001  | Pipeline Controller Pattern Required    | CRITICAL | EA-003       |
| TR-002  | Phase Module Interface Contract         | HIGH     | EA-003       |
| TR-003  | Execution Context Object Required       | HIGH     | EA-003       |
| TR-004  | No Global State Permitted               | HIGH     | EA-003       |
| TR-005  | Single Responsibility per Module        | MEDIUM   | EA-005       |

### Category 2 — Configuration Loading

| Rule ID | Rule Title                              | Severity | EA Authority |
|---------|-----------------------------------------|----------|--------------|
| TR-010  | Configuration Loaded at Initialization Only | HIGH | EA-008     |
| TR-011  | Configuration Schema Validation at Load Time | HIGH | EA-007    |
| TR-012  | Configuration Values Must Be Typed      | MEDIUM   | EA-007       |
| TR-013  | No Configuration Mutation After Load    | HIGH     | EA-003       |

### Category 3 — Error Handling

| Rule ID | Rule Title                              | Severity | EA Authority |
|---------|-----------------------------------------|----------|--------------|
| TR-020  | Structured Error Type Required          | HIGH     | EA-005       |
| TR-021  | CRITICAL Errors Halt the Pipeline       | CRITICAL | EA-010       |
| TR-022  | HIGH Errors Are Evaluated Before Gate Advancement | HIGH | EA-005 |
| TR-023  | Errors Must Not Be Silently Swallowed   | CRITICAL | EA-006       |
| TR-024  | Recoverable Errors Permit Continuation with Record | MEDIUM | EA-006 |

### Category 4 — Deterministic Execution Support

| Rule ID | Rule Title                              | Severity | EA Authority |
|---------|-----------------------------------------|----------|--------------|
| TR-030  | Deterministic Input Ordering Required   | CRITICAL | EA-003       |
| TR-031  | No Timestamp-Dependent Control Flow     | HIGH     | EA-003       |
| TR-032  | Idempotent Phase Design Required        | HIGH     | EA-003       |
| TR-033  | Simulation and Live Execution Must Produce Identical Plans | CRITICAL | EA-004 |
| TR-034  | Prompt Compiler Compatibility Required  | MEDIUM   | EA-009       |

---------------------------------------------------------------------

## SECTION 3 — VALIDATION REQUIREMENTS (VR)

Defined in: `IG_CONFIG_VALIDATION_REQUIREMENTS.md`

### Category 1 — Simulation Validation

| Rule ID | Rule Title                                        | Severity | Auto-Enforceable |
|---------|---------------------------------------------------|----------|------------------|
| VR-001  | Simulation Layer Must Be Independently Verifiable | CRITICAL | No               |
| VR-002  | Simulation Must Cover All In-Scope Targets        | CRITICAL | Yes              |
| VR-003  | Simulation Outcome Severity Classification        | HIGH     | Yes              |
| VR-004  | Simulation Results Must Not Be Mutably Cached     | HIGH     | No               |
| VR-005  | Simulation Validation Report Is a Mandatory Artifact | CRITICAL | Yes            |

### Category 2 — Mutation Validation

| Rule ID | Rule Title                                        | Severity | Auto-Enforceable |
|---------|---------------------------------------------------|----------|------------------|
| VR-010  | Pre-Mutation State Snapshot Required              | CRITICAL | No               |
| VR-011  | Each Mutation Operation Must Be Individually Logged | CRITICAL | Yes            |
| VR-012  | Post-Mutation Artifact Hash Must Be Recorded      | HIGH     | Yes              |
| VR-013  | Mutation Boundary Enforcement                     | CRITICAL | No               |
| VR-014  | Failed Mutation Must Trigger Immediate Halt       | CRITICAL | Yes              |

### Category 3 — Schema Compliance

| Rule ID | Rule Title                                        | Severity | Auto-Enforceable |
|---------|---------------------------------------------------|----------|------------------|
| VR-020  | All Produced Artifacts Must Be Schema-Validated   | CRITICAL | Yes              |
| VR-021  | Schema Version Must Be Pinned                     | HIGH     | Yes              |
| VR-022  | Schema Validation Failures Are Non-Suppressible   | CRITICAL | No               |
| VR-023  | Input Artifact Schema Validation at Phase Entry   | HIGH     | Yes              |

### Category 4 — Governance Enforcement

| Rule ID | Rule Title                                        | Severity | Auto-Enforceable |
|---------|---------------------------------------------------|----------|------------------|
| VR-030  | EA Addenda Must Be Enforced in Code               | CRITICAL | No               |
| VR-031  | EA-001 Hash Check at PHASE-01 and at Gate         | CRITICAL | Yes              |
| VR-032  | EA-005 Governance Check Must Produce Result Record | HIGH    | Yes              |
| VR-033  | Governance Violations Must Be Unambiguously Classified | HIGH | No            |
| VR-034  | Rollback Execution Must Be Logged and Confirmed   | CRITICAL | Yes              |

---------------------------------------------------------------------

## SECTION 4 — RULE SEVERITY SUMMARY

### IR Rules

| Severity | Count | Rule IDs                                 |
|----------|-------|------------------------------------------|
| CRITICAL | 4     | IR-001, IR-013, IR-023, IR-030           |
| HIGH     | 9     | IR-002, IR-003, IR-010, IR-011, IR-020, IR-021, IR-022, IR-031, IR-032, IR-033 |
| MEDIUM   | 1     | IR-012                                   |

### TR Rules

| Severity | Count | Rule IDs                                 |
|----------|-------|------------------------------------------|
| CRITICAL | 4     | TR-001, TR-021, TR-023, TR-030, TR-033   |
| HIGH     | 10    | TR-002, TR-003, TR-004, TR-010, TR-011, TR-013, TR-020, TR-022, TR-031, TR-032 |
| MEDIUM   | 3     | TR-005, TR-012, TR-024, TR-034           |

### VR Rules

| Severity | Count | Rule IDs                                                 |
|----------|-------|----------------------------------------------------------|
| CRITICAL | 11    | VR-001, VR-002, VR-005, VR-010, VR-011, VR-013, VR-014, VR-020, VR-022, VR-030, VR-031, VR-034 |
| HIGH     | 8     | VR-003, VR-004, VR-012, VR-021, VR-023, VR-032, VR-033  |

---------------------------------------------------------------------

## SECTION 5 — EA AUTHORITY MAP

| EA ID  | IR Rules                    | TR Rules               | VR Rules                       |
|--------|-----------------------------|------------------------|--------------------------------|
| EA-001 | —                           | —                      | VR-031                         |
| EA-002 | IR-030, IR-031, IR-032      | —                      | —                              |
| EA-003 | IR-002                      | TR-001, TR-002, TR-003, TR-004, TR-013, TR-030, TR-031, TR-032 | — |
| EA-004 | IR-013                      | TR-033                 | VR-001, VR-002, VR-013         |
| EA-005 | IR-011                      | TR-005, TR-020, TR-022 | VR-030, VR-032, VR-033         |
| EA-006 | IR-020, IR-021, IR-022      | TR-023, TR-024         | VR-011                         |
| EA-007 | IR-001, IR-010, IR-033      | TR-011, TR-012         | VR-020, VR-021, VR-022, VR-023 |
| EA-008 | IR-012                      | TR-010                 | —                              |
| EA-009 | —                           | TR-034                 | —                              |
| EA-010 | IR-023                      | TR-021                 | VR-010, VR-014, VR-034         |

---------------------------------------------------------------------

## SECTION 6 — MANDATORY IG CONTENT CHECKLIST

An IG artifact must address all 13 items below to pass IG_CONFIG review:

| # | Required Content Item                              | Governing Rule |
|---|----------------------------------------------------|----------------|
| 1 | Module category declaration (all 6 canonical types)| IR-001         |
| 2 | Python version and dependency declaration           | IR-010, IR-011 |
| 3 | Log format specification                           | IR-020         |
| 4 | Artifact routing table (all produced artifacts)    | IR-033         |
| 5 | Pipeline controller module identified              | TR-001         |
| 6 | Phase class interface specification                | TR-002         |
| 7 | Configuration source and schema reference          | TR-010, TR-011 |
| 8 | Exception hierarchy specification                  | TR-020         |
| 9 | EA governance enforcement map                      | VR-030         |
| 10 | Simulation layer independence confirmation         | VR-001         |
| 11 | Pre-mutation snapshot mechanism specification      | VR-010         |
| 12 | Schema version pin table (all artifacts)           | VR-021         |
| 13 | Rollback mechanism specification                   | VR-034         |

---------------------------------------------------------------------

## VERSION HISTORY

| Version | Date       | Author    | Change Summary            |
|---------|------------|-----------|---------------------------|
| 1.0     | 2026-03-12 | Architect | Initial canonical release |
