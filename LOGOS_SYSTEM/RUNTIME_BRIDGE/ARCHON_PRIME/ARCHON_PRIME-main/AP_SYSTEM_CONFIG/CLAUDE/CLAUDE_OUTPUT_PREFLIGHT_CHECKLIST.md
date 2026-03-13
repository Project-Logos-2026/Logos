# CLAUDE_OUTPUT_PREFLIGHT_CHECKLIST.md

## Document Identity

| Field | Value |
|---|---|
| Artifact ID | OPS-006 |
| System | ARCHON_PRIME |
| Platform | Claude |
| Artifact Type | Self-Verification Checklist |
| Version | v1 |
| Status | Draft |
| Authority Source | Architect |
| Schema Reference | AP_MASTER_SPEC_V2_SCHEMA.json, AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json |
| Supersedes | None — STANDALONE |

---

## Purpose

This checklist is Claude's mandatory pre-delivery gate. It is run internally against every Design Specification and Implementation Guide before the artifact is delivered to the Architect or forwarded to GPT. It is not optional and is not a formality.

If any blocking check fails, Claude must resolve the failure before delivery. Claude must not deliver an artifact that fails a blocking check, regardless of session time pressure or Architect request to "just get it done."

Non-blocking checks must be flagged in the delivery message even if they do not halt delivery.

---

## Section 1 — When to Run This Checklist

Run this checklist immediately before delivering:
- Any `Design_Specification.md` artifact
- Any `Implementation_Guide.md` artifact

Do not run for: concept drafts, analog candidate reports, critique reports, feedback reports, or conversational outputs. Those artifact types have their own verification requirements.

---

## Section 2 — Design Specification Preflight

### 2.1 Identity Block Checks

| # | Check | Blocking | Pass Condition |
|---|-------|----------|----------------|
| DS-ID-01 | `artifact_id` follows pattern `SPEC-NNNN` | Yes | Pattern matches exactly |
| DS-ID-02 | `subsystem` is populated | Yes | Non-empty string |
| DS-ID-03 | `version` follows pattern `vN` | Yes | Pattern matches |
| DS-ID-04 | `status` is a valid lifecycle state | Yes | One of: draft, under_review, approved, locked, superseded, deprecated, rejected |
| DS-ID-05 | `source_concept` references a CON-NNNN artifact | Yes | Non-empty, begins with CON- |
| DS-ID-06 | `schema` field cites `AP_MASTER_SPEC_V2_SCHEMA.json` | Yes | Exact filename present |
| DS-ID-07 | `approved_by` is blank when status is `draft` or `under_review` | Yes | Blank or null for pre-approval states |
| DS-ID-08 | `approved_by` is populated when status is `approved` or `locked` | Yes | Non-empty string for post-approval states |

### 2.2 Required Section Checks

All sections marked [REQUIRED] in the Design Spec template must be present and non-empty.

| # | Section | Blocking | Pass Condition |
|---|---------|----------|----------------|
| DS-SEC-01 | Purpose | Yes | ≥ 1 paragraph |
| DS-SEC-02 | Functional Requirements | Yes | ≥ 1 entry with valid FR-NNN ID |
| DS-SEC-03 | Constraints | Yes | ≥ 1 entry with valid C-NNN ID |
| DS-SEC-04 | Formal Model — Primitives | Yes | Non-empty |
| DS-SEC-05 | Formal Model — Operations | Yes | Non-empty |
| DS-SEC-06 | Formal Model — Axioms | Yes | Non-empty |
| DS-SEC-07 | Canonical Architecture Definition | Yes | directory_tree has ≥ 1 entry; placement_rules has ≥ 1 entry |
| DS-SEC-08 | Canonical Module Registry | Yes | registry_mode declared; either modules populated (inline) or registry_artifact_ref populated (reference) |
| DS-SEC-09 | Module Identity Rules | Yes | ≥ 3 validity conditions present |
| DS-SEC-10 | Subsystem Contracts | Yes | ≥ 1 subsystem contract with allowed/forbidden imports defined |
| DS-SEC-11 | Artifact Surface Definition | Yes | All 6 surfaces enumerated; runtime_code_permitted set for each |
| DS-SEC-12 | Module Classification Types | Yes | All 7 classification labels present |
| DS-SEC-13 | Header Schema Definition — Required Fields | Yes | ≥ 13 required header fields listed |
| DS-SEC-14 | Header Schema Definition — Validation Rules | Yes | ≥ 4 HVR-NNN rules present |
| DS-SEC-15 | Architecture Validation Rules — Checks | Yes | ≥ 8 AVR-NNN checks present |
| DS-SEC-16 | Architecture Validation Rules — Gate Conditions | Yes | ≥ 5 gate conditions covering all gated stages |
| DS-SEC-17 | Governance Rules — Non-Deletion Policy | Yes | Rule stated; exceptions listed or "None" stated |
| DS-SEC-18 | Governance Rules — Enhancement Proposal Process | Yes | Blocking rule stated |
| DS-SEC-19 | Implementation Sequence | Yes | ≥ 1 phase with entry/exit conditions |
| DS-SEC-20 | Enhancement Lifecycle | Yes | All 5 stages (EL-001 through EL-005) present; bypass_permitted stated |
| DS-SEC-21 | Verification Criteria | Yes | ≥ 1 entry with valid V-NNN ID |
| DS-SEC-22 | Revision History | Yes | ≥ 1 entry (v1 initial) |

### 2.3 Content Integrity Checks

| # | Check | Blocking | Pass Condition |
|---|-------|----------|----------------|
| DS-INT-01 | All FR IDs follow pattern `FR-NNN` | Yes | All entries match |
| DS-INT-02 | All constraint IDs follow pattern `C-NNN` | Yes | All entries match |
| DS-INT-03 | All verification criterion IDs follow pattern `V-NNN` | Yes | All entries match |
| DS-INT-04 | All module IDs in registry follow pattern `M[N]+` | Yes | All entries match |
| DS-INT-05 | No open question flagged as `blocking: Yes` has a blank resolution | No | Flag in delivery message |
| DS-INT-06 | Deferments section explicitly states each deferred item and where it is deferred to | No | Flag if any deferment lacks `deferred_to` |
| DS-INT-07 | No section contains placeholder text (e.g., `[description]`, `[TBD]`) | Yes | No unfilled placeholders in delivered artifact |
| DS-INT-08 | Artifact does not introduce capabilities absent from the source concept | Yes | Scope match verified against source concept |
| DS-INT-09 | Governance enforcement is defined before capabilities that require it | Yes | Governance sections appear before implementation sequence |

---

## Section 3 — Implementation Guide Preflight

### 3.1 Identity Block Checks

| # | Check | Blocking | Pass Condition |
|---|-------|----------|----------------|
| IG-ID-01 | `artifact_id` follows pattern `IMPL-NNNN` | Yes | Pattern matches exactly |
| IG-ID-02 | `source_specification` references a valid `SPEC-NNNN` artifact | Yes | Non-empty, begins with SPEC- |
| IG-ID-03 | `version` follows pattern `vN` | Yes | Pattern matches |
| IG-ID-04 | `status` is a valid lifecycle state | Yes | Valid enum value |
| IG-ID-05 | `schema` field cites `AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json` | Yes | Exact filename present |

### 3.2 Required Section Checks

| # | Section | Blocking | Pass Condition |
|---|---------|----------|----------------|
| IG-SEC-01 | Overview | Yes | Non-empty, ≥ 1 sentence |
| IG-SEC-02 | Prerequisites | Yes | ≥ 1 entry with status declared |
| IG-SEC-03 | Deterministic Build Sequence | Yes | ≥ 5 steps; reorder_rule declared |
| IG-SEC-04 | Header Injection Rules | Yes | ≥ 4 HIR-NNN rules; validation behavior declared for all 3 failure cases |
| IG-SEC-05 | Spec Compliance Checks | Yes | ≥ 4 SCC-NNN checks present |
| IG-SEC-06 | Module Generation Contract | Yes | ≥ 3 pre-generation conditions; ≥ 3 generation rules |
| IG-SEC-07 | Analog Reconciliation Process | Yes | All 4 reconciliation steps present; ≥ 3 disposition options |
| IG-SEC-08 | Enhancement Integration Rules | Yes | All 5 workflow steps; pre-integration gate with ≥ 3 conditions; bypass_rule declared |
| IG-SEC-09 | Artifact Directory Rules | Yes | ≥ 3 ADR-NNN rules; violation_disposition declared |
| IG-SEC-10 | Drift Detection Audit | Yes | ≥ 5 DD-NNN checks; audit output path declared |
| IG-SEC-11 | Architecture Validation Gate | Yes | gate_rule present; ≥ 3 gated stages; validator_module defined |
| IG-SEC-12 | Governance Enforcement Points | Yes | ≥ 1 entry |
| IG-SEC-13 | Stages | Yes | ≥ 1 stage with entry/exit conditions |
| IG-SEC-14 | Revision History | Yes | ≥ 1 entry |

### 3.3 Content Integrity Checks

| # | Check | Blocking | Pass Condition |
|---|-------|----------|----------------|
| IG-INT-01 | All build step IDs follow pattern `BS-NNN` | Yes | All entries match |
| IG-INT-02 | Enhancement integration workflow contains all 5 stages in order | Yes | proposal → architect_review → design_spec_update → implementation_guide_update → implementation |
| IG-INT-03 | Validator module has `canonical_path`, `execution_command`, `input_sources`, and `output_artifact` | Yes | All four fields populated |
| IG-INT-04 | No placeholder text remains | Yes | No unfilled placeholders |
| IG-INT-05 | Unresolved ambiguities are documented in ambiguity_log | No | Flag in delivery message if blocking ambiguities exist |
| IG-INT-06 | Guide does not introduce capabilities not present in source specification | Yes | Scope bounded by SPEC reference |

---

## Section 4 — Delivery Message Format

When delivering a passing artifact, Claude must include a brief preflight summary in the delivery message:

```
PREFLIGHT COMPLETE — [ARTIFACT_ID] [artifact_type]
Blocking checks: [N] passed / 0 failed
Non-blocking flags: [N] — [brief list, or "None"]
Schema: [schema filename]
Ready for: [Architect review / GPT handoff / upload]
```

When a blocking check fails, Claude must not deliver the artifact. Instead:

```
PREFLIGHT FAILED — [ARTIFACT_ID] [artifact_type]
Blocking failures:
  - [Check ID]: [what failed]
  - [Check ID]: [what failed]
Artifact not delivered. Resolving before redelivery.
```

---

## Section 5 — Preflight Exemptions

No exemptions exist for blocking checks. Non-blocking checks may be deferred to a revision cycle with explicit documentation in the delivery message. If the Architect explicitly instructs Claude to deliver an artifact despite a known blocking failure, Claude must:

1. State the failing checks clearly
2. State that the artifact does not meet V2 schema requirements
3. Deliver the artifact marked `status: draft` with a note identifying the open failures

Claude must not silently suppress preflight findings.

---

## End of Checklist
