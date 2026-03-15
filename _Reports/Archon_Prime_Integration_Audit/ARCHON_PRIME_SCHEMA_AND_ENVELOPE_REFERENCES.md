# ARCHON PRIME SCHEMA AND ENVELOPE REFERENCES
**Generated:** 2026-03-13  
**Target:** `LOGOS_SYSTEM/RUNTIME_BRIDGE/ARCHON_PRIME/ARCHON_PRIME-main`  
**Method:** Static inspection of all .json schema files and execution envelope documents  

---

## 1. Schema Inventory

### 1.1 System-Level Schemas (AP_SYSTEM_CONFIG/SYSTEM/SCHEMAS/)

| File | Path | Purpose |
|------|------|---------|
| `AP_MODULE_HEADER_SCHEMA.json` | `SYSTEM/SCHEMAS/` | Canonical AP module header definition |
| `HEADER_POLICY_REGISTRY.json` | `SYSTEM/SCHEMAS/` | Registry of header policies per module type |
| `AP_MODULE_HEADER_TEMPLATE.py` | `SYSTEM/SCHEMAS/` | Python template for inserting AP headers |

#### AP_MODULE_HEADER_SCHEMA.json (v1.0)

```json
{
  "schema_name": "ARCHON_PRIME_MODULE_HEADER",
  "version": "1.0",
  "authority": "ARCHON_PRIME",
  "header_boundary_start": "# ARCHON PRIME MODULE HEADER",
  "header_boundary_end": "# END ARCHON PRIME MODULE HEADER",
  "guard_activation": "from SYSTEM.workflow_guard import enforce_runtime_guard",
  "fields": [
    "module_id", "module_name", "subsystem", "module_role", "canonical_path",
    "responsibility", "runtime_stage", "execution_entry", "allowed_targets",
    "forbidden_targets", "allowed_imports", "forbidden_imports",
    "spec_reference", "implementation_phase", "authoring_authority", "version", "status"
  ]
}
```

**Note:** The schema references `from SYSTEM.workflow_guard import enforce_runtime_guard` — but actual deployed code uses `from WORKFLOW_NEXUS.Governance.workflow_gate import enforce_runtime_gate`. The schema is slightly out of sync with the deployed implementation (different module path and function name).

### 1.2 Config-Level Schemas (AP_SYSTEM_CONFIG/SYSTEM/CONFIG/)

| File | Purpose |
|------|---------|
| `AP_PIPELINE_AUDIT_LOG_SCHEMA.json` | Defines the JSON structure for pipeline audit log entries |

### 1.3 Execution Envelope Schemas (AP_SYSTEM_CONFIG/SYSTEM/EXECUTION_ENVELOPES/EE_CONFIG/EE_SCHEMAS/)

| File | Purpose |
|------|---------|
| `EXECUTION_ENVELOPE_SCHEMA.json` | JSON schema for execution envelope documents |
| `DESIGN_SPEC_SCHEMA.json` | JSON schema for design specification documents (DS) |
| `IMPLEMENTATION_GUIDE_SCHEMA.json` | JSON schema for implementation guide documents (IG) |
| `EXECUTION_APPEND.json` | Supplemental execution rules appended to the EE schema |

### 1.4 Workflow Mutation Tooling Schemas (WORKFLOW_MUTATION_TOOLING/schemas/)

| File | Purpose |
|------|---------|
| `CrawlMutationRecord.schema.json` | Schema for crawl mutation log records |
| `PhaseGate.schema.json` | Schema for phase gate validation records |
| `QuarantineRecord.schema.json` | Schema for quarantine records |
| `ValidationManifest.schema.json` | Schema for pipeline validation manifests |

### 1.5 Agent-Facing Schemas (AP_SYSTEM_CONFIG/CLAUDE/ and AP_SYSTEM_CONFIG/GPT/)

| File | Agent | Purpose |
|------|-------|---------|
| `AP_DESIGN_SPEC_SCHEMA.json` | Claude | Design spec structure schema |
| `AP_IMPLEMENTATION_GUIDE_SCHEMA.json` | Claude | Implementation guide schema |
| `ARTIFACT_SCHEMA.json` | Claude | Artifact metadata schema |
| `CONCEPT_ARTIFACT_SCHEMA.json` | Claude | Concept artifact schema |
| `ANALOG_DISCOVERY_SCHEMA.json` | Claude | Analog discovery schema |
| `TOOL_ENFORCEMENT_SCHEMA.json` | Claude | Tool enforcement / allowed tool list |
| `AP_PROMPT_SCHEMA_V1.json` | GPT | Prompt schema version 1 |
| `PROMPT_EXECUTION_FEEDBACK_SCHEMA.json` | GPT | Prompt execution feedback |
| `PROMPT_REGISTRY.json` | GPT | Registry of all compiled prompts |
| `AP_SPEC_COMPILER_MANIFEST.json` | GPT | Spec compiler manifest |

---

## 2. Execution Envelope System

AP's execution envelope system is a governance layer for describing *how* work should be executed. Envelopes come in four types:

| Envelope Type | Config Prefix | Description |
|--------------|---------------|-------------|
| Design Specification (DS) | `DS_CONFIG/` | How design spec artifacts are structured |
| Execution Artifact (EA) | `EA_CONFIG/` | Artifact routing and integrity rules |
| Execution Envelope (EE) | `EE_CONFIG/` | The core workflow execution container |
| Execution Protocol (EP) | `EP_CONFIG/` | Phase model and mutation gate rules |
| Implementation Guide (IG) | `IG_CONFIG/` | How implementation guides are structured |

### Active Envelopes (WORKFLOW_EXECUTION_ENVELOPES/ACTIVE_ENVELOPES/)

| Envelope | Files | Purpose |
|----------|-------|---------|
| `AP_V2_Tooling` | DS, EA, EP, IG + MANIFEST | Envelope for the AP V2 tooling build |
| `AP_V3_NEXUS` | DS, EA, EP, IG + EE_MANIFEST | Envelope for the AP V3 NEXUS system |

### Envelope Attributes (EA_CONFIG/EA-001 through EA-010)

| Attribute | Specification |
|-----------|--------------|
| EA-001 | ENVELOPE_TARGET_INTEGRITY — target files must match declared scope |
| EA-002 | ARTIFACT_ROUTER_ENFORCEMENT — all artifacts must route through the router |
| EA-003 | DETERMINISTIC_EXECUTION_ORDERING — stage sequence must be deterministic |
| EA-004 | SIMULATION_FIRST_RULE — all mutations must be simulated before applying |
| EA-005 | GOVERNANCE_CONSISTENCY_CHECK — artifacts must be governance-consistent |
| EA-006 | EXECUTION_LOGGING_REQUIREMENTS — all execution must be logged |
| EA-007 | ARTIFACT_METADATA_SCHEMA_ENFORCEMENT — all artifacts must carry valid metadata |
| EA-008 | ENVELOPE_MANIFEST_CONTRACT — envelopes must have a valid manifest |
| EA-009 | PROMPT_COMPILER_INTEGRATION — prompts must be compiler-validated |
| EA-010 | FAILURE_ROLLBACK_PROTOCOL — failures must trigger rollback |

---

## 3. Schema Dependency Map

```
Execution Pipeline
    ↓ governed by
AP_PIPELINE_AUDIT_LOG_SCHEMA.json    [logs]
AP_MODULE_HEADER_SCHEMA.json          [module headers]
HEADER_POLICY_REGISTRY.json           [header policy enforcement]
    ↓ structured by
EXECUTION_ENVELOPE_SCHEMA.json        [EE artifacts]
DESIGN_SPEC_SCHEMA.json               [DS artifacts]
IMPLEMENTATION_GUIDE_SCHEMA.json      [IG artifacts]
    ↓ validated by
PhaseGate.schema.json                 [phase gate records]
ValidationManifest.schema.json        [validation output]
CrawlMutationRecord.schema.json       [crawl mutation log]
QuarantineRecord.schema.json          [quarantine events]
    ↓ agent interface
AP_PROMPT_SCHEMA_V1.json             [GPT prompt format]
ARTIFACT_SCHEMA.json                  [Claude artifact format]
```

---

## 4. Schema vs. LOGOS Governance Schema Comparison

| AP Schema | LOGOS Equivalent | Gap |
|-----------|-----------------|-----|
| `AP_MODULE_HEADER_SCHEMA.json` | No explicit LOGOS schema file (LOGOS uses docstring convention) | INCOMPATIBLE |
| `EXECUTION_ENVELOPE_SCHEMA.json` | No LOGOS EE equivalent | NO EQUIVALENT |
| `DESIGN_SPEC_SCHEMA.json` | LOGOS uses `.md` spec documents | FORMAT GAP |
| `AP_PIPELINE_AUDIT_LOG_SCHEMA.json` | LOGOS audit logs use custom JSON | SCHEMA GAP |
| `PhaseGate.schema.json` | LOGOS uses Coq proof gates (PXL gate) | CONCEPTUALLY DIFFERENT |
| `ValidationManifest.schema.json` | No LOGOS equivalent | NO EQUIVALENT |
| `PROMPT_REGISTRY.json` | No LOGOS equivalent | NO EQUIVALENT (AP-unique) |
| `TOOL_ENFORCEMENT_SCHEMA.json` | LOGOS governance artifacts + `destructive_tools_index.json` | PARTIAL OVERLAP |

---

## 5. Execution Envelope References in Python Code

Python modules reference the envelope system indirectly through:
- Config files: `configs/audit_configs/PRE_CRAWL_CHECKLIST.md`
- Schema files: loaded by `normalization_tools/schema_registry.py`
- Header injection: `tools/audit_tools/header_schema_audit.py` validates against `AP_MODULE_HEADER_SCHEMA.json`

The `tools_internal/v21_header_injection.py` module explicitly works with the header schema to inject compliant headers into Python modules.

---

## 6. Key Schema Findings

| Finding | Severity |
|---------|----------|
| AP's header schema (`AP_MODULE_HEADER_SCHEMA.json`) references a different governance guard path than what's deployed (`SYSTEM.workflow_guard` vs. `WORKFLOW_NEXUS.Governance.workflow_gate`) | HIGH — schema is out of sync with implementation |
| AP's execution envelope system (EE/DS/IG/EA/EP) has no LOGOS equivalent — it's a standalone workflow governance layer | HIGH — no LOGOS normalization target exists |
| AP's phase gate concept (PhaseGate.schema.json) is structurally different from LOGOS's Coq proof gate | HIGH — different governance paradigm |
| AP has 6 JSON schemas in `WORKFLOW_MUTATION_TOOLING/schemas/` loaded at runtime by the pipeline — these are functional schemas, not just design docs | MEDIUM — must be preserved in any normalization |
| PROMPT_REGISTRY.json contains AP-specific compiled prompt records — no LOGOS equivalent surface | MEDIUM — AP-unique, would remain local |

---

*Report produced by: LOGOS Archon Prime Integration Audit — 2026-03-13*
