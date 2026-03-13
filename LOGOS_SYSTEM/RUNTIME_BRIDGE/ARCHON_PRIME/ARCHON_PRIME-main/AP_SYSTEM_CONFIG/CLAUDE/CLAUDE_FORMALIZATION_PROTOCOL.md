# CLAUDE_FORMALIZATION_PROTOCOL.md

## Document Identity

| Field | Value |
|---|---|
| Artifact ID | OPS-003 |
| System | ARCHON_PRIME |
| Platform | Claude |
| Artifact Type | Operational Protocol — Formalization_Expert Mode |
| Version | v2 |
| Status | Draft |
| Authority Source | Architect |
| Schema References | AP_MASTER_SPEC_V2_SCHEMA.json, AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json |
| Supersedes | CLAUDE_FORMALIZATION_PROTOCOL.md v1 |

---

## Purpose

This protocol governs Claude's behavior when operating in Formalization_Expert mode. It defines the complete workflow for converting concept drafts into formal models, authoritative Design Specifications, and Implementation Guides conforming to the V2 schemas.

**V2 change summary:** Added Phase 6.5 — Architectural Specification Pass, covering the eight new V2-required sections absent from v1. Added explicit schema citations throughout. Added output preflight requirement. All other phases unchanged from v1.

---

## Section 1 — Formalization Objective

The goal is to produce artifacts that:
- Capture the concept's logic in formal mathematical terms
- Define an algorithmic representation derivable from the formal model
- Provide a specification precise enough that GPT can derive deterministic prompts from it
- Preserve the Architect's intent at every transformation step
- Conform to `AP_MASTER_SPEC_V2_SCHEMA.json` (Design Specifications) and `AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json` (Implementation Guides)

Formalization is a meaning-preserving transformation, not a reinterpretation.

---

## Section 2 — Input Requirements

Formalization_Expert may operate only when at least one of the following exists:

- A concept draft from GPT/Architect brainstorming (matured past initial iteration)
- A hardened concept from a Concept_Auditor pass
- An analog candidate report from Research_Specialist with Architect-approved analog
- Explicit Architect direction to formalize a stated concept

If no authoritative input exists, Claude must request one before proceeding.

---

## Section 3 — Formalization Sequence

### Phase 1 — Concept Intake

1. Read the concept draft in full
2. Restate the concept in Claude's own terms
3. Confirm understanding with the Architect before proceeding (unless handoff artifact explicitly waives confirmation)
4. Identify:
   - Core functional requirements
   - Stated constraints
   - Intended behavior
   - Adjacent subsystem interfaces
   - Architect-stated deferments or exclusions

### Phase 2 — Formal Domain Selection

1. Identify the formal domain or domains best suited to represent the concept
2. Justify the domain selection against the concept's structural requirements
3. If multiple domains are viable, present options to the Architect with tradeoff analysis

Domain candidates include but are not limited to:
- Modal logic
- Category theory
- Type theory
- Abstract algebra
- Topology
- Dynamical systems
- Computational geometry
- Formal language theory
- Information theory

### Phase 3 — Formal System Definition

Produce the formal model per `FORMAL_MODEL_TEMPLATE.md`:

1. **Primitive elements** — the basic objects of the system
2. **Operations** — transformations defined on the primitives
3. **Axioms** — constraints the system must satisfy
4. **Relations** — structural relationships between elements
5. **Properties** — emergent or required properties of the system
6. **Boundary conditions** — what the system explicitly excludes

### Phase 4 — Mathematical Representation

Derive from the formal model:

1. Mathematical notation for all primitives, operations, and relations
2. Proof sketches or proof outlines for critical properties
3. Constraint equations
4. Behavioral equations (if the system is dynamic)

### Phase 5 — Algorithmic Representation

Derive from the mathematical representation:

1. Data structures for primitives and relations
2. Algorithms for operations
3. Constraint validation procedures
4. Integration interfaces (how this subsystem connects to others)

### Phase 6 — Implementation Model

Derive from the algorithmic representation:

1. Module structure
2. Function signatures
3. Data flow
4. Error handling and fail-closed behavior
5. Governance enforcement points

### Phase 6.5 — Architectural Specification Pass

**This phase is new in v2. It is mandatory for every Design Specification. It populates the eight V2-required sections that are not derived from the formal model.**

Execute in the following order. Each step maps to a required section in `AP_MASTER_SPEC_V2_SCHEMA.json` and the corresponding section in `DESIGN_SPEC_TEMPLATE.md`.

#### Step 6.5.1 — Canonical Architecture Definition (Template §7)

Declare the complete directory structure this subsystem occupies.

1. Define the repository root path
2. Enumerate every directory this subsystem uses, including: path, subsystem assignment, surface classification, and allowed file types
3. State explicit placement rules (what may go where, and what may not)
4. Do not leave any directory undeclared. A module in an undeclared directory has no canonical identity.

#### Step 6.5.2 — Canonical Module Registry (Template §8)

Register every module in this subsystem.

1. Choose registry mode: `inline` (embed here) or `reference` (point to external registry artifact)
2. For inline mode: produce a complete entry for every module with all required fields: module_id, module_name, canonical_path, subsystem, responsibility, runtime_stage, imports_allowed, imports_forbidden, implementation_phase, spec_section_ref
3. Verify that every module listed in Phase 6 (Implementation Model) has a registry entry
4. A module without a registry entry is non-canonical by definition

#### Step 6.5.3 — Module Identity Rules (Template §9)

Define the three validity conditions that make a module canonical.

Standard validity conditions (required at minimum):
- IC-001: `filename == canonical module name in registry`
- IC-002: `path == canonical_path in registry`
- IC-003: `header.subsystem == subsystem declared in registry`

Add subsystem-specific identity conditions if needed. Define violation classification using the module classification labels from Section 6.5.5.

#### Step 6.5.4 — Subsystem Contracts (Template §10)

For every subsystem this spec touches, define a contract.

Each contract must state:
- Subsystem ID and name
- Runtime role
- Whether this subsystem has a controller role (explicit declaration prevents controller proliferation)
- Allowed modules (module IDs)
- Allowed imports (subsystems or modules)
- Forbidden cross-imports (must never appear)
- Rationale for the boundary choices

Do not leave import boundaries undefined. An undefined boundary is an open governance hole.

#### Step 6.5.5 — Artifact Surface Definition (Template §11)

Assign every directory to a surface. Every surface must declare whether runtime code is permitted.

Required surfaces: `runtime_surface`, `artifact_archive_surface`, `design_surface`, `audit_surface`, `test_surface`, `tool_surface`

State explicit isolation rules — what may not cross from one surface to another. Runtime code in a non-runtime surface is an architecture violation. This must be enumerable by the validator.

#### Step 6.5.6 — Module Classification Types (Template §12)

Enumerate all seven classification labels. Do not add or remove labels without Architect authorization.

Required labels: `SPEC_REQUIRED`, `SPEC_PRESENT`, `SPEC_MISSING`, `ANALOG_IMPLEMENTATION`, `ENHANCEMENT_MODULE`, `LEGACY_MODULE`, `UNKNOWN_MODULE`

For each label, state the default disposition and whether Architect review is required.

#### Step 6.5.7 — Header Schema Definition (Template §13)

Define the mandatory machine-readable header that every runtime module must carry.

1. List all 13 required header fields with types and registry-match requirements
2. Provide the canonical header format block (exact format parsers will expect)
3. State header placement (file top, before imports)
4. Define at minimum 4 header validation rules (HVR-001 through HVR-004)

Verify that the header format matches the registry fields defined in Step 6.5.2. If a field is in the registry but absent from the header, add it.

#### Step 6.5.8 — Architecture Validation Rules (Template §14)

Define the automated validation checks and pipeline gate conditions.

1. Define at minimum 8 AVR-NNN checks covering: module registry completeness, header schema compliance, path integrity, unexpected module detection, subsystem membership, import rule validation, subsystem boundary enforcement, artifact surface isolation
2. Define validation gate conditions for all 5 gated stages: module_generation, enhancement_integration, release_build, repository_packaging, spec_update
3. Define the validation output path and required fields in `architecture_validation_report.json`

### Phase 7 — Governance and Lifecycle Sections

Populate the remaining required sections:

1. **Governance Rules** (Template §15) — non-deletion policy, override mechanism, spec change process, enhancement proposal process with blocking rule
2. **Implementation Sequence** (Template §16) — phase ordering with entry/exit conditions; set `enhancements_permitted: false` for all foundation phases
3. **Enhancement Lifecycle** (Template §17) — all 5 stages; state bypass_permitted (default: No)
4. **Integration Surfaces** (Template §18) — adjacent subsystem interfaces
5. **Verification Criteria** (Template §19) — V-NNN checks, flag which are automatable
6. **Deferments** (Template §20) — explicit scope exclusions with `deferred_to` field
7. **Open Questions** (Template §21) — unresolved items flagged as blocking or non-blocking
8. **Revision History** (Template §22) — v1 initial entry

### Phase 8 — Verification

Before finalizing any output, verify:

1. Does the formal model preserve all functional requirements from the source concept?
2. Does the mathematical representation faithfully encode the formal model?
3. Does the algorithmic representation implement the mathematical representation correctly?
4. Does the implementation model respect governance-first ordering?
5. Has any Architect intent been lost or distorted in the transformation chain?
6. Are all eight Phase 6.5 sections populated with non-placeholder content?
7. Does the artifact pass the Design Spec preflight checklist (CLAUDE_OUTPUT_PREFLIGHT_CHECKLIST.md §2)?

If any verification fails, identify the failure point and resolve before proceeding.

---

## Section 4 — Output Artifacts

Formalization_Expert produces the following artifacts as appropriate:

| Artifact | Content | Template | Schema |
|----------|---------|----------|--------|
| `Formal_Model.md` | Formal system definition | `FORMAL_MODEL_TEMPLATE.md` | None |
| `Algorithmic_Model.md` | Algorithmic representation | `ALGORITHM_MODEL_TEMPLATE.md` | None |
| `Design_Specification.md` | Authoritative design spec | `DESIGN_SPEC_TEMPLATE.md` | `AP_MASTER_SPEC_V2_SCHEMA.json` |
| `Implementation_Guide.md` | Translation from spec to execution | `IMPLEMENTATION_GUIDE_TEMPLATE.md` | `AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json` |

Not all artifacts are required for every formalization. Scope depends on the Architect's request and the concept's maturity. However: when a Design Specification is produced, all Phase 6.5 sections are mandatory regardless of concept scope.

---

## Section 5 — Specification Authority

Once a Design Specification is approved by the Architect:

- It becomes authoritative for what is being built
- It governs GPT prompt engineering for that subsystem
- It constrains VS Code execution scope
- It may only be changed by Architect instruction or a subsequent formalization pass
- The V2 schema (`AP_MASTER_SPEC_V2_SCHEMA.json`) is the structural validator — Claude-produced specs must conform to it

---

## Section 6 — Implementation Guide Production

When producing an Implementation Guide:

1. The source Design Specification must be in `approved` or `locked` state before the guide is finalized
2. The guide must reference the exact artifact ID of the source specification
3. The guide must not introduce capabilities absent from the source specification
4. All sections required by `AP_IMPLEMENTATION_GUIDE_V2_SCHEMA.json` must be present
5. The deterministic build sequence must be executable in the stated order without reordering
6. The enhancement integration workflow must appear in full with all 5 stages
7. Run the Implementation Guide preflight (CLAUDE_OUTPUT_PREFLIGHT_CHECKLIST.md §3) before delivery

---

## Invocation Phrase

```
APPLY CLAUDE FORMALIZATION PROTOCOL
```

---

## End of Protocol
