# IMPLEMENTATION_GUIDE_TEMPLATE.md

## Document Identity

| Field | Value |
|---|---|
| System | ARCHON_PRIME |
| Platform | Claude |
| Artifact Type | Template — Implementation Guide |
| Version | v2 |
| Status | Draft |
| Schema Reference | AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json |
| Supersedes | IMPLEMENTATION_GUIDE_TEMPLATE.md v1 (which contained misplaced Design Spec schema content) |

---

## Usage

When Claude produces an `Implementation_Guide.md` for any subsystem, it must follow this template exactly. The Implementation Guide translates an approved Design Specification into actionable, ordered stages that GPT can convert into deterministic VS Code prompts.

**Authority rule:** The Implementation Guide is authoritative on HOW the specification gets built. It must not introduce capabilities, modules, or behaviors absent from the source Design Specification. If a discrepancy is found between the guide and the spec, the spec wins.

**Source specification must be approved:** A finalized Implementation Guide requires that its source Design Specification is in `approved` or `locked` state. A guide written against a `draft` spec must be flagged as provisional.

All sections marked **[REQUIRED]** must be present. Sections marked **[CONDITIONAL]** apply only when the indicated condition is met. Sections marked **[RECOMMENDED]** should be present but may be deferred with justification.

---

## Template

```markdown
# Implementation Guide: [Subsystem Name]

## Guide Identity
**[REQUIRED]**

| Field | Value |
|---|---|
| Artifact ID | IMPL-[NNNN] |
| Subsystem | [canonical subsystem name] |
| Version | v[N] |
| Status | [Draft / Under Review / Approved / Locked] |
| Source Specification | [SPEC-NNNN — must be approved or locked] |
| Schema | AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json |
| Author | Claude / Formalization_Expert |
| Date | [YYYY-MM-DD] |
| Approved By | [Architect — blank until approved] |
| Authority Source | ARCHON_PRIME_ARCHITECT |

---

## Lineage
**[CONDITIONAL — required when this guide supersedes a prior version]**

| Field | Value |
|---|---|
| Design Origin | [SPEC-NNNN] |
| Concept Origin | [CON-NNNN or null] |
| Prior Version | [IMPL-NNNN vN or null] |

---

## 1. Implementation Overview
**[REQUIRED]**

Plain-language statement of what this guide implements and what it produces. Reference the source Design Specification as the source of truth for WHAT is being built. This guide defines HOW it is built.

State explicitly: what modules are created, what directories are established, and what artifacts are produced by a complete implementation of this guide.

---

## 2. Prerequisites
**[REQUIRED — minimum 1 entry]**

All conditions that must be true before implementation may begin. Blocking prerequisites halt the entire implementation if unsatisfied.

| Prerequisite | Status | Blocking | Notes |
|-------------|--------|----------|-------|
| [dependency description] | [satisfied / pending / blocked] | [Yes / No] | [details] |

---

## 3. Deterministic Build Sequence
**[REQUIRED — minimum 5 steps]**

The ordered, deterministic sequence of build operations. Every step is explicit. Steps may not be reordered without Architect authorization.

**Reorder rule:** Prohibited. Steps must execute in stated order. If reordering is required, produce an updated Implementation Guide.

| Step ID | Step Name | Action | Depends On | Produces | Validation Required | Blocking |
|---------|-----------|--------|-----------|----------|--------------------|-|
| BS-001 | [name] | [concrete action] | [step IDs or none] | [artifact or state] | [Yes / No] | [Yes / No] |
| BS-002 | [name] | [concrete action] | [BS-001] | [artifact or state] | [Yes / No] | [Yes / No] |

---

## 4. Header Injection Rules
**[REQUIRED — minimum 4 rules]**

Rules governing the mandatory machine-readable header block in every runtime module.

**Header source:** `canonical_module_registry` — all header field values must match registry values exactly.

| Rule ID | Rule | Enforcement Point |
|---------|------|------------------|
| HIR-001 | Every runtime module must contain a header block before any imports or executable code | module_generation |
| HIR-002 | Header fields must match canonical registry values for fields marked must_match_registry | post_generation_scan |
| HIR-003 | Header must be present in the exact format specified in the source Design Specification §13.2 | validation_gate |
| HIR-004 | Modules without valid headers fail architecture validation and may not be integrated | validation_gate |

**Validation behavior:**

| Condition | Action |
|-----------|--------|
| Missing header | [halt / flag_and_continue] |
| Invalid field | [halt / flag_and_continue] |
| Registry mismatch | [halt / flag_and_continue] |

---

## 5. Spec Compliance Checks
**[REQUIRED — minimum 4 checks]**

Checks run at module generation time and at architecture validation to verify conformance with the source Design Specification.

| Check ID | Check Name | Description | Blocking | Failure Disposition |
|----------|-----------|-------------|----------|---------------------|
| SCC-001 | module_path_match | Module file exists at canonical_path from registry | Yes | halt_pipeline |
| SCC-002 | module_name_match | Filename matches canonical module_name from registry | Yes | halt_pipeline |
| SCC-003 | subsystem_match | header.subsystem matches registry subsystem value | Yes | halt_pipeline |
| SCC-004 | dependency_rules_match | Module imports comply with imports_allowed and imports_forbidden | Yes | halt_pipeline |

---

## 6. Module Generation Contract
**[REQUIRED]**

Rules governing module generation. All pre-generation conditions must be true before any module is created.

### 6.1 Pre-Generation Conditions

All of the following must be true before a module generation is permitted:

1. Module is listed in the canonical module registry of the source Design Specification
2. Source Design Specification status is `approved` or `locked`
3. Architecture validation passes (or this is the first build pass initializing the registry)
4. [Add subsystem-specific conditions]

### 6.2 Generation Rules

| Rule ID | Rule | Rationale |
|---------|------|-----------|
| MGR-001 | Module must match canonical registry entry on all three identity fields | Canonical identity enforcement |
| MGR-002 | Module imports must comply with subsystem contract for its subsystem | Boundary enforcement |
| MGR-003 | Module must receive a valid header block during generation | Header schema compliance |
| [MGR-NNN] | [additional rules] | [rationale] |

### 6.3 Post-Generation Verification

After each module is generated, verify:

1. File exists at canonical_path
2. Header is present and all registry-match fields are correct
3. Imports comply with allowed/forbidden rules
4. Module passes SCC-001 through SCC-004

---

## 7. Analog Reconciliation Process
**[REQUIRED]**

Process for detecting and reconciling modules present in the repository that were not generated from the spec.

**Detection method:** Architecture validation scan — any module in the runtime surface not in the canonical registry is flagged as a candidate for reconciliation.

### 7.1 Reconciliation Steps

| Step ID | Step Name | Action | Architect Decision Required |
|---------|-----------|--------|---------------------------|
| AR-001 | detect | Identify all modules flagged as ANALOG_IMPLEMENTATION or UNKNOWN_MODULE by validator | No |
| AR-002 | compare | Compare flagged module against the spec module it most closely corresponds to | No |
| AR-003 | evaluate_reuse | Assess whether the analog can be adopted, wrapped, or must be replaced | Yes |
| AR-004 | disposition | Apply Architect-authorized disposition | Yes |

### 7.2 Disposition Options

| Disposition | Conditions | Required Actions |
|-------------|-----------|-----------------|
| adopt | Analog passes all spec compliance checks after header injection | Inject header; add to registry; reclassify as SPEC_PRESENT |
| wrap | Analog has correct behavior but wrong interface | Create wrapper module matching spec; retain analog as internal implementation |
| replace | Analog does not satisfy spec requirements | Generate spec-compliant module; archive analog |
| archive | Analog is legitimate non-spec utility | Move to non-runtime surface; remove from runtime scan scope |
| reject | Analog introduces governance violations | Remove immediately; escalate to Architect |

**Unresolved analog rule:** Any analog not reconciled within one implementation cycle is reclassified as UNKNOWN_MODULE and escalated to the Architect. Implementation cannot progress on affected subsystem until reconciliation is complete.

---

## 8. Enhancement Integration Rules
**[REQUIRED]**

No enhancement may be implemented before completing all prior workflow stages. This rule has no exceptions without explicit Architect authorization.

### 8.1 Integration Workflow

All five stages must complete in order. No stage may be skipped.

| Step ID | Stage | Required Output |
|---------|-------|----------------|
| EI-001 | proposal | Enhancement proposal document describing scope, rationale, and affected modules |
| EI-002 | architect_review | Architect review decision (approve / reject / revise) |
| EI-003 | design_spec_update | Updated Design Specification incorporating the enhancement |
| EI-004 | implementation_guide_update | Updated Implementation Guide reflecting changes |
| EI-005 | implementation | Implementation in repository |

### 8.2 Pre-Integration Gate

All of the following must be true before an enhancement module is committed:

1. Design Specification updated and in `approved` or `locked` state
2. Implementation Guide updated and in `approved` or `locked` state
3. Architecture validation passes on updated spec

**Gate enforcement:** Both automated check and manual verification.

### 8.3 Bypass Rule

**Bypassable:** No

Bypass conditions: None by default. Architect may authorize bypass with explicit written instruction stating the conditions and scope.

---

## 9. Artifact Directory Rules
**[REQUIRED — minimum 3 rules]**

Rules enforcing isolation between artifact surfaces.

| Rule ID | Rule | Blocking |
|---------|------|----------|
| ADR-001 | Runtime modules may only exist in directories classified as runtime_surface | Yes |
| ADR-002 | Export artifacts (reports, audit outputs) must not reside in runtime directories | Yes |
| ADR-003 | Design artifacts (.md specs, guides) must reside in design_surface directories | Yes |
| [ADR-NNN] | [additional rules] | [Yes / No] |

**Violation disposition:** [halt_pipeline / quarantine_module / flag_for_review]

---

## 10. Drift Detection Audit
**[REQUIRED — minimum 5 checks]**

Automated checks that detect deviations between repo state and canonical spec. Must run before enhancement integration, release builds, and at all validation gates.

| Check ID | Check Name | Description | Report Field | Blocking |
|----------|-----------|-------------|-------------|---------|
| DD-001 | unexpected_modules | Modules in runtime surface not in canonical registry | unexpected_modules | Yes |
| DD-002 | duplicate_modules | Multiple modules with same module_id | duplicate_modules | Yes |
| DD-003 | non_spec_paths | Modules located outside canonical paths | misplaced_modules | Yes |
| DD-004 | subsystem_violations | Modules with subsystem mismatch vs registry | subsystem_mismatch | Yes |
| DD-005 | missing_spec_modules | Registry modules absent from repository | missing_spec_modules | Yes |
| DD-006 | header_schema_violations | Modules with missing or invalid headers | header_schema_violations | Yes |
| DD-007 | import_rule_violations | Modules violating allowed/forbidden import rules | import_rule_violations | Yes |
| DD-008 | artifact_surface_violations | Runtime code in non-runtime surface directories | artifact_surface_violations | Yes |

**Audit trigger conditions:**

- Before any enhancement integration step
- Before any release build
- At architecture validation gate invocation
- On Architect request

**Audit output:** `[audit_surface_path]/architecture_validation_report.json`

---

## 11. Architecture Validation Gate
**[REQUIRED]**

**Gate rule:** `architecture_valid == true` is required before any gated stage may proceed.

**Gated stages:**

| Stage | Gate Condition |
|-------|---------------|
| module_generation | architecture_valid == true |
| enhancement_integration | architecture_valid == true |
| release_build | architecture_valid == true |
| repository_packaging | architecture_valid == true |
| spec_update | architecture_valid == true |

**Validator module:**

| Field | Value |
|-------|-------|
| Canonical Path | `[path/to/validate_architecture.py]` |
| Execution Command | `python [path/to/validate_architecture.py]` |
| Input Sources | Canonical module registry, header schema definition, subsystem contracts, artifact surface definitions, repository root |
| Output Artifact | `[audit_surface_path]/architecture_validation_report.json` |

**Validation checks executed:**
1. Module registry completeness
2. Header schema compliance
3. Canonical path integrity
4. Unexpected module detection
5. Subsystem membership validation
6. Import rule validation
7. Subsystem boundary enforcement
8. Artifact surface isolation

**On gate failure:** Halt and escalate to Architect. Do not proceed.

---

## 12. Implementation Stages
**[REQUIRED — minimum 1 stage]**

Each stage is independently executable. Stages must execute in stated order. No stage may be skipped or reordered without Architect authorization.

### Stage 1: [Stage Name]

**Stage ID:** [identifier]
**Entry Condition:** [what must be true before this stage begins]
**Exit Condition:** [what must be true before Stage 2 begins]
**Validation Gate Required:** [Yes / No]

#### Modules

| Module ID | Module Name | Canonical Path | Header Required | Implementation Notes |
|-----------|-------------|----------------|----------------|---------------------|
| M[N] | [name] | [path] | Yes | [spec section ref and specific notes] |

#### Implementation Steps

1. [Specific step — explicit enough for GPT to derive a VS Code prompt]
2. [Specific step]
3. [Specific step]

#### Validation

- [How to verify this stage succeeded]

---

### Stage 2: [Stage Name]

[Same structure as Stage 1]

---

### Stage N: [Stage Name]

[Same structure]

---

## 13. Governance Enforcement Points
**[REQUIRED — minimum 1 entry]**

| Enforcement Point | Rule | Action on Violation |
|------------------|------|---------------------|
| [where enforced] | [the rule] | [halt / escalate_to_architect / log_and_continue] |

---

## 14. Ambiguity Log
**[RECOMMENDED]**

Unresolved ambiguities in the source Design Specification that affect implementation. Blocking ambiguities must be resolved before the affected module is implemented.

| Ambiguity ID | Context | Question | Blocking Module | Recommendation | Escalation Required | Resolution |
|-------------|---------|----------|----------------|----------------|--------------------|-|
| A1 | [spec section] | [what is unclear] | [module ID or null] | [Claude recommendation] | [Yes / No] | [blank until resolved] |

---

## 15. Revision History
**[REQUIRED]**

Append-only.

| Version | Date | Change | Author |
|---------|------|--------|--------|
| v1 | [YYYY-MM-DD] | Initial implementation guide | Claude / Formalization_Expert |

```

---

## Section Inventory

For reference, sections present in this v2 template:

| # | Section | v1 | v2 | Notes |
|---|---------|----|----|-------|
| — | Guide Identity | ✓ | ✓ | Added schema citation, source spec status requirement |
| — | Lineage | — | ✓ | New |
| 1 | Implementation Overview | ✓ | ✓ | Expanded |
| 2 | Prerequisites | ✓ | ✓ | Added blocking flag |
| 3 | Deterministic Build Sequence | — | ✓ | New — replaces generic "stages" framing |
| 4 | Header Injection Rules | — | ✓ | New |
| 5 | Spec Compliance Checks | — | ✓ | New |
| 6 | Module Generation Contract | — | ✓ | New |
| 7 | Analog Reconciliation Process | — | ✓ | New |
| 8 | Enhancement Integration Rules | — | ✓ | New |
| 9 | Artifact Directory Rules | — | ✓ | New |
| 10 | Drift Detection Audit | — | ✓ | New |
| 11 | Architecture Validation Gate | — | ✓ | New |
| 12 | Implementation Stages | ✓ | ✓ | Renamed from "Stages"; added module table with header_required flag |
| 13 | Governance Enforcement Points | ✓ | ✓ | Renumbered |
| 14 | Ambiguity Log | ✓ | ✓ | Renumbered; added blocking_module field |
| 15 | Revision History | ✓ | ✓ | Renumbered |

---

## End of Template
