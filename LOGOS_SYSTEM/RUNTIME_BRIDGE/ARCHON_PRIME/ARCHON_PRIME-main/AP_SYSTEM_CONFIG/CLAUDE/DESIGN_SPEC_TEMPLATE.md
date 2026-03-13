# DESIGN_SPEC_TEMPLATE.md

## Document Identity

* **System:** ARCHON_PRIME
* **Platform:** Claude
* **Artifact Type:** Template — Design Specification
* **Version:** v2
* **Status:** Draft
* **Schema Reference:** AP_MASTER_SPEC_V2_SCHEMA.json
* **Supersedes:** DESIGN_SPEC_TEMPLATE.md v1
* **Intent:** Provide the standardized structure for all design specifications produced by Claude. Updated to reflect V2 schema requirements: canonical architecture definition, module registry, subsystem contracts, artifact surface separation, header schema definition, module classification, architecture validation rules, enhancement lifecycle, and implementation sequencing.

---

## Usage

When Claude produces a `Design_Specification.md` for any subsystem, it must follow this template structure exactly. Sections may be omitted only if they are genuinely inapplicable to the subsystem being specified. Any omission requires an explicit note stating why the section does not apply.

All section IDs, field names, and pattern constraints must conform to AP_MASTER_SPEC_V2_SCHEMA.json. The validator module will enforce structural compliance.

Sections marked **[REQUIRED]** must be present in every spec. Sections marked **[CONDITIONAL]** apply only when the indicated condition is met. Sections marked **[RECOMMENDED]** should be present but may be deferred with justification.

---

## Template

```markdown
# Design Specification: [Subsystem Name]

## Specification Identity
**[REQUIRED]**

* **Artifact ID:** SPEC-[NNNN]
* **Subsystem:** [canonical subsystem name]
* **Version:** v[N]
* **Status:** [Draft / Under Review / Approved / Locked]
* **Source Concept:** [CON-NNNN — Concept Artifact reference]
* **Schema:** AP_MASTER_SPEC_V2_SCHEMA.json
* **Author:** Claude / Formalization_Expert
* **Date:** [YYYY-MM-DD]
* **Approved By:** [Architect — leave blank until approved; required before status transitions to Approved or Locked]
* **Authority Source:** [ARCHON_PRIME_ARCHITECT]

---

## Lineage
**[CONDITIONAL — required when this spec supersedes a prior version or derives from an analog]**

* **Concept Origin:** [CON-NNNN]
* **Analog Origin:** [ANL-NNNN or null]
* **Prior Version:** [SPEC-NNNN vN or null]
* **Supersedes:** [SPEC-NNNN — artifact ID of the spec this version replaces, if applicable]

---

## 1. Purpose
**[REQUIRED]**

What this subsystem exists to do. One to three paragraphs. Scope statement only — functional requirements are captured in Section 2.

---

## 2. Functional Requirements
**[REQUIRED — minimum 1 entry]**

What the subsystem must do. Each requirement must be specific, testable, and traceable to the source concept.

| ID | Requirement | Source | Testable |
|----|-------------|--------|----------|
| FR-001 | [description] | [CON-NNNN or section ref] | [Yes / No] |
| FR-002 | [description] | [CON-NNNN or section ref] | [Yes / No] |

---

## 3. Constraints
**[REQUIRED — minimum 1 entry]**

What the subsystem must not do or what limits it must respect.

| ID | Constraint | Rationale | Enforcement Mechanism |
|----|-----------|-----------|----------------------|
| C-001 | [description] | [why] | [how enforced at runtime or validation] |
| C-002 | [description] | [why] | [how enforced] |

---

## 4. Formal Model
**[REQUIRED]**

### 4.1 Primitives

The basic objects of the system.

| Symbol | Name | Description | Type |
|--------|------|-------------|------|
| [symbol] | [name] | [what it represents] | [set / element / function / etc.] |

### 4.2 Operations

Transformations defined on the primitives.

| Symbol | Name | Signature | Description |
|--------|------|-----------|-------------|
| [symbol] | [name] | [input → output] | [what it does] |

### 4.3 Axioms

Constraints the system must satisfy.

| ID | Axiom | Formal Statement | Informal Meaning |
|----|-------|-----------------|------------------|
| AX-001 | [name] | [formal notation] | [plain language] |

### 4.4 Relations

Structural relationships between elements.

| Symbol | Name | Type | Description |
|--------|------|------|-------------|
| [symbol] | [name] | [equivalence / order / etc.] | [what it captures] |

### 4.5 Properties

Required or emergent properties.

| ID | Property | Formal Statement | Status |
|----|----------|-----------------|--------|
| P-001 | [name] | [formal notation] | [proved / conjectured / required] |

---

## 5. Mathematical Representation
**[RECOMMENDED]**

Formal notation for the system's elements, operations, and constraints. Proof sketches for critical properties.

---

## 6. Algorithmic Representation
**[RECOMMENDED]**

### 6.1 Data Structures

### 6.2 Algorithms

### 6.3 Constraint Validation

### 6.4 Error Handling

---

## 7. Canonical Architecture Definition
**[REQUIRED]**

Explicit definition of the directory structure this subsystem occupies. Every directory must be declared. No module may be placed in an undeclared directory.

### 7.1 Repository Root

```
[canonical repository root path]
```

### 7.2 Directory Tree

| Path | Subsystem | Surface | Allowed File Types | Description |
|------|-----------|---------|-------------------|-------------|
| [path/relative/to/root] | [subsystem name] | [runtime_surface / artifact_archive_surface / design_surface / audit_surface / test_surface / tool_surface] | [.py, .json, etc.] | [purpose] |

### 7.3 Placement Rules

| ID | Rule | Rationale |
|----|------|-----------|
| PR-001 | [explicit placement rule] | [why] |
| PR-002 | [explicit placement rule] | [why] |

---

## 8. Canonical Module Registry
**[REQUIRED]**

Identity record for every module in this subsystem. A module not listed here is by definition non-canonical and will be flagged by the architecture validator.

**Registry Mode:** [inline / reference]
*(If reference: Registry Artifact Ref: [artifact ID of external registry])*

| Module ID | Module Name | Canonical Path | Subsystem | Responsibility | Runtime Stage | Imports Allowed | Imports Forbidden | Phase |
|-----------|-------------|----------------|-----------|----------------|---------------|-----------------|-------------------|-------|
| M[N] | [filename without ext] | [full path from root] | [subsystem] | [one-sentence description] | [analysis / processing / etc.] | [subsystems or modules] | [subsystems or modules] | [PHASE_N] |

---

## 9. Module Identity Rules
**[REQUIRED]**

A module is canonically valid only when all three conditions are simultaneously satisfied.

### 9.1 Validity Conditions

| ID | Condition | Enforcement Point |
|----|-----------|------------------|
| IC-001 | filename == canonical module name in registry | header_validation |
| IC-002 | path == canonical_path in registry | path_validation |
| IC-003 | header.subsystem == subsystem declared in registry | header_validation |

### 9.2 Violation Classification

| Category | Description | Severity |
|----------|-------------|----------|
| [violation type] | [what it means] | [blocking / major / minor] |

---

## 10. Subsystem Contracts
**[REQUIRED — one entry per subsystem this spec governs or interacts with]**

Boundary definitions controlling what each subsystem may contain and import.

### [Subsystem Name]

* **Subsystem ID:** [identifier]
* **Runtime Role:** [what this subsystem does in the pipeline]
* **Controller Role:** [Yes / No — explicit declaration prevents controller proliferation]
* **Allowed Modules:** [module IDs]
* **Allowed Imports:** [subsystems or modules]
* **Forbidden Cross-Imports:** [subsystems that must never be imported]
* **Rationale:** [why these boundaries are defined this way]

---

## 11. Artifact Surface Definition
**[REQUIRED]**

Declares which directories belong to which surface. Runtime code may only exist in `runtime_surface` directories. This rule has no exceptions.

| Surface | Directories | Runtime Code Permitted |
|---------|-------------|----------------------|
| runtime_surface | [paths] | Yes |
| artifact_archive_surface | [paths] | No |
| design_surface | [paths] | No |
| audit_surface | [paths] | No |
| test_surface | [paths] | No |
| tool_surface | [paths] | No |

### Surface Isolation Rules

| ID | Rule | Source Surface | Target Surface |
|----|------|---------------|---------------|
| [ID] | [what is prohibited] | [surface] | [surface] |

---

## 12. Module Classification Types
**[REQUIRED]**

First-class classification system. All classification types must be declared before implementation begins. Classification is assigned at architecture validation, not post-hoc.

| Classification | Label | Description | Default Disposition | Architect Review Required |
|---------------|-------|-------------|--------------------|-----------------------------|
| [ID] | SPEC_REQUIRED | Defined in spec, not yet built | — | No |
| [ID] | SPEC_PRESENT | Defined in spec and verified present | retain | No |
| [ID] | SPEC_MISSING | Defined in spec, absent from repo | escalate | Yes |
| [ID] | ANALOG_IMPLEMENTATION | Present, performs spec function, not spec-generated | adopt / wrap / replace | Yes |
| [ID] | ENHANCEMENT_MODULE | Present, extends spec functionality, not in spec | flag_for_review | Yes |
| [ID] | LEGACY_MODULE | Present, predates current spec | replace / archive | Yes |
| [ID] | UNKNOWN_MODULE | Present, no matching spec entry | escalate | Yes |

---

## 13. Header Schema Definition
**[REQUIRED]**

Defines the mandatory machine-readable header block every runtime module must contain. Headers must match canonical registry values. Modules without valid headers fail architecture validation.

### 13.1 Required Header Fields

| Field Name | Type | Must Match Registry | Description |
|------------|------|--------------------|-----------------------|
| module_id | string | Yes | Canonical module ID (M[N]) |
| module_name | string | Yes | Canonical filename without extension |
| subsystem | string | Yes | Subsystem this module belongs to |
| canonical_path | string | Yes | Full canonical path from repository root |
| responsibility | string | No | Single-sentence functional description |
| runtime_stage | enum | No | [initialization / analysis / processing / validation / repair / audit / reporting / utility] |
| allowed_imports | string_list | No | Subsystems or modules permitted to import |
| forbidden_imports | string_list | No | Subsystems or modules prohibited from importing |
| spec_reference | string | No | Section of this spec defining this module's behavior |
| implementation_phase | string | No | Build phase (e.g., PHASE_1) |
| authoring_authority | string | No | ARCHON_PRIME |
| version | string | No | Module version |
| status | enum | No | [canonical / draft / deprecated] |

### 13.2 Header Format

```
# ARCHON PRIME MODULE HEADER
module_id: [M-ID]
module_name: [filename]
subsystem: [subsystem]
canonical_path: [path/from/root/filename.py]
responsibility: [one sentence]
runtime_stage: [stage]
allowed_imports:
  - [subsystem or module]
forbidden_imports:
  - [subsystem or module]
spec_reference: [SPEC-NNNN.section.N]
implementation_phase: [PHASE_N]
authoring_authority: ARCHON_PRIME
version: [N.N]
status: [canonical / draft / deprecated]
```

### 13.3 Header Placement

Headers must appear at the top of the file, before any imports or executable code.

### 13.4 Header Validation Rules

| ID | Rule | Violation Label |
|----|------|----------------|
| HVR-001 | Header block must be present in every runtime module | header_schema_violations |
| HVR-002 | All required fields must be populated | header_schema_violations |
| HVR-003 | Fields marked Must Match Registry must equal registry values exactly | header_schema_violations |
| HVR-004 | status must be a declared enum value | header_schema_violations |

---

## 14. Architecture Validation Rules
**[REQUIRED]**

Defines the mandatory compliance checks the architecture validator must run. All blocking checks must pass before any gated pipeline stage proceeds.

### 14.1 Validation Checks

| ID | Check Name | Description | Blocking | Report Field |
|----|-----------|-------------|----------|-------------|
| AVR-001 | module_registry_completeness | Every registry module exists at its canonical path | Yes | missing_spec_modules |
| AVR-002 | header_schema_compliance | Every runtime module has a valid header matching registry values | Yes | header_schema_violations |
| AVR-003 | path_integrity | Every runtime module is located at its canonical path | Yes | misplaced_modules |
| AVR-004 | unexpected_module_detection | Any module in runtime surface not in registry is flagged | Yes | unexpected_modules |
| AVR-005 | subsystem_membership_validation | header.subsystem matches registry for every module | Yes | subsystem_mismatch |
| AVR-006 | import_rule_validation | imports ∈ allowed_imports AND imports ∉ forbidden_imports | Yes | import_rule_violations |
| AVR-007 | subsystem_boundary_enforcement | No forbidden cross-subsystem imports exist | Yes | subsystem_boundary_violations |
| AVR-008 | artifact_surface_isolation | Runtime modules exist only in runtime_surface directories | Yes | artifact_surface_violations |

### 14.2 Validation Gate Conditions

| Gate ID | Stage | Condition |
|---------|-------|-----------|
| VG-001 | module_generation | architecture_valid == true |
| VG-002 | enhancement_integration | architecture_valid == true |
| VG-003 | release_build | architecture_valid == true |
| VG-004 | repository_packaging | architecture_valid == true |
| VG-005 | spec_update | architecture_valid == true |

### 14.3 Validation Output

The validator produces: `[audit_surface_path]/architecture_validation_report.json`

Required fields: `validation_timestamp`, `summary`, `missing_spec_modules`, `unexpected_modules`, `misplaced_modules`, `header_schema_violations`, `import_rule_violations`, `subsystem_boundary_violations`, `artifact_surface_violations`, `architecture_valid`

---

## 15. Governance Rules
**[REQUIRED]**

### 15.1 Non-Deletion Policy

[State the rule. Example: "No canonical module may be deleted from the repository without explicit Architect authorization. Removal requires a spec update identifying the module as deprecated and specifying what replaces it."]

**Exceptions:** [List permitted exceptions, or state "None."]

### 15.2 Architect Override Mechanism

**Trigger:** [When override is invoked]
**Process:** [How it is executed and recorded]

### 15.3 Spec Change Process

Ordered steps required to modify this specification:

1. [step]
2. [step]
3. [step]

### 15.4 Enhancement Proposal Process

Ordered steps required before an enhancement may be implemented:

1. [step]
2. [step]
3. [step]

**Blocking Rule:** Enhancements must modify the design spec and implementation guide before any code is committed. This rule has no exceptions without explicit Architect authorization.

---

## 16. Implementation Sequence
**[REQUIRED]**

Defines the mandatory build order. Enhancements may not be integrated before the phase in which they are authorized.

| Phase ID | Phase Name | Modules | Entry Condition | Exit Condition | Enhancements Permitted |
|----------|-----------|---------|----------------|----------------|----------------------|
| PHASE_1 | [name] | [module IDs] | [what must be true] | [what must be true] | No |
| PHASE_2 | [name] | [module IDs] | [what must be true] | [what must be true] | No |
| PHASE_N | [name] | [module IDs] | [what must be true] | [what must be true] | [Yes / No] |

**Out-of-order disposition:** Halt pipeline. Escalate to Architect.

---

## 17. Enhancement Lifecycle
**[REQUIRED]**

No enhancement may be implemented before completing all prior stages. Stage sequence is non-negotiable.

| Stage ID | Stage Name | Required Output | Authority |
|----------|-----------|----------------|-----------|
| EL-001 | proposal | Enhancement proposal document | Architect review |
| EL-002 | review | Review decision (approve / reject / revise) | Architect |
| EL-003 | approval | Explicit approval record | Architect |
| EL-004 | spec_update | Updated Design Specification | Claude / Formalization_Expert |
| EL-005 | implementation | Implementation in repo | GPT / VS Code |

**Pre-implementation gate conditions:**
1. Design specification updated and approved
2. Implementation guide updated and approved
3. Architecture validation passes on updated spec

**Bypass permitted:** No. *(If yes: conditions and authority must be stated explicitly.)*

---

## 18. Integration Surfaces
**[RECOMMENDED]**

How this subsystem connects to adjacent subsystems.

| Adjacent Subsystem | Interface Type | Data Flow |
|-------------------|---------------|-----------|
| [name] | [type] | [direction and content] |

---

## 19. Verification Criteria
**[REQUIRED — minimum 1 entry]**

How to verify that an implementation correctly realizes this specification.

| ID | Criterion | Method | Automated |
|----|-----------|--------|-----------|
| V-001 | [what to verify] | [how to verify] | [Yes / No] |

---

## 20. Deferments
**[RECOMMENDED]**

What is explicitly out of scope for this specification. Deferments are binding — deferred items must not be re-prioritized without Architect authorization.

| Item | Rationale | Deferred To |
|------|-----------|-------------|
| [what is deferred] | [why] | [phase, spec version, or artifact] |

---

## 21. Open Questions
**[RECOMMENDED]**

Unresolved items requiring Architect decision. Blocking questions must be resolved before spec may transition to Approved.

| ID | Question | Blocking | Resolution |
|----|----------|----------|------------|
| [ID] | [question] | [Yes / No] | [blank until resolved] |

---

## 22. Revision History
**[REQUIRED]**

Append-only. Do not modify prior entries.

| Version | Date | Change | Author |
|---------|------|--------|--------|
| v1 | [YYYY-MM-DD] | Initial specification | Claude / Formalization_Expert |

```

---

## Section Inventory

For reference, the sections added in v2 relative to v1:

| Section | v1 | v2 | Notes |
|---------|----|----|-------|
| Specification Identity | ✓ | ✓ | Expanded: artifact ID pattern, schema ref, authority source |
| Lineage | — | ✓ | New |
| Purpose | ✓ | ✓ | Unchanged |
| Functional Requirements | ✓ | ✓ | Added testable flag |
| Constraints | ✓ | ✓ | Added enforcement mechanism column |
| Formal Model | ✓ | ✓ | Unchanged |
| Mathematical Representation | ✓ | ✓ | Unchanged |
| Algorithmic Representation | ✓ | ✓ | Unchanged |
| Canonical Architecture Definition | — | ✓ | New — §7 |
| Canonical Module Registry | — | ✓ | New — §8 |
| Module Identity Rules | — | ✓ | New — §9 |
| Subsystem Contracts | — | ✓ | New — §10 |
| Artifact Surface Definition | — | ✓ | New — §11 |
| Module Classification Types | — | ✓ | New — §12 |
| Header Schema Definition | — | ✓ | New — §13 |
| Architecture Validation Rules | — | ✓ | New — §14 |
| Governance Rules | — | ✓ | New — §15 |
| Implementation Sequence | — | ✓ | New — §16 |
| Enhancement Lifecycle | — | ✓ | New — §17 |
| Integration Surfaces | ✓ | ✓ | Renumbered §18 |
| Verification Criteria | ✓ | ✓ | Added automated flag, renumbered §19 |
| Deferments | ✓ | ✓ | Added deferred_to field, renumbered §20 |
| Open Questions | ✓ | ✓ | Added blocking flag, renumbered §21 |
| Revision History | ✓ | ✓ | Renumbered §22 |

---

## End of Template
