**Status:** CANONICAL | DESIGN-ONLY | NON-EXECUTABLE  
**Authority:** Structural Specification Only  
**Execution:** STRICTLY FORBIDDEN  
**Phase:** DR-AC Rebuild Target Definition  
**Scope:** Authorized output structure declaration

---

## Semantic Synopsis

This specification defines the ONLY directory structure and artifact classes that the DR-AC rebuild is permitted to generate. It serves as the authoritative target for reconstruction and the validation boundary for all rebuild outputs. No output outside this specification is authorized.

---

## 1. Purpose and Scope

### 1.1 Purpose

This specification establishes:
- The canonical directory tree structure
- Authorized artifact classes and their locations
- Explicit exclusions and forbidden outputs
- Mapping rules from DR-AC stages to output locations

### 1.2 Scope

This specification applies to:
- All DR-AC rebuild outputs
- All artifact generation stages
- All governance validation points
- All structural integrity checks

This specification does NOT:
- Authorize execution of generated artifacts
- Define runtime behavior or semantics
- Grant persistent state permissions
- Enable autonomous operation

---

## 2. High-Level Directory Tree

The canonical output tree consists of the following top-level structure:

```
LOGOS_SYSTEM/
├── Primitives/
│   ├── Semantic_Axioms/
│   ├── PXL_Core/
│   └── Governance_Invariants/
├── Runtime_Spine/
│   ├── Session_Management/
│   ├── Reconstruction_Pipeline/
│   └── Orchestration/
├── Governance/
│   ├── Phase_Definitions/
│   ├── Denial_Invariants/
│   ├── Design_Only_Declarations/
│   └── Autonomy_Policies/
├── Application_Functions/
│   ├── Stateless_Modules/
│   └── Curated_Artifacts/
├── Documentation/
│   ├── Design_Specifications/
│   ├── Type_Schemas/
│   └── Boundary_Contracts/
└── Validation/
    ├── Integrity_Checks/
    └── Audit_Records/
```

---

## 3. Artifact Class Definitions and Placement Rules

### 3.1 Primitives/ (Immutable Canonical Inputs)

**Authorized Classes:**
- Semantic axiom definitions (.py, .txt, .md)
- PXL formal specifications (.v, .txt)
- Core governance invariants (.json, .md)
- Orchestration composition rules (.py, .json)

**Placement Rules:**
- Semantic_Axioms/: Pure semantic definitions only
- PXL_Core/: Coq proofs and formal logic
- Governance_Invariants/: Phase 1-5 canonical governance

**Explicit Exclusions:**
- No runtime logic
- No mutable state
- No execution hooks
- No test scaffolding

---

### 3.2 Runtime_Spine/ (Dynamic Reconstruction Infrastructure)

**Authorized Classes:**
- Session initialization modules (.py)
- DR-AC pipeline stage implementations (.py)
- Orchestration composition engines (.py)
- Import graph registries (.json)

**Placement Rules:**
- Session_Management/: Session init, profile loading
- Reconstruction_Pipeline/: Stages 1-6, 8 implementations
- Orchestration/: Composition and routing logic

**Explicit Exclusions:**
- No autonomous agents
- No persistent sessions
- No self-modification
- No execution bypass

---

### 3.3 Governance/ (Runtime Governance Enforcement)

**Authorized Classes:**
- Phase definition documents (.md, .json)
- Denial invariant specifications (.md, .json)
- Design-only declarations (.md)
- Autonomy policy specifications (.md, .json)
- Mutation gate implementations (.py)

**Placement Rules:**
- Phase_Definitions/: Phase 1-5 closure artifacts
- Denial_Invariants/: G1-G8 specifications
- Design_Only_Declarations/: Non-execution constraints
- Autonomy_Policies/: Authority boundaries

**Explicit Exclusions:**
- No runtime policy modification
- No governance bypass pathways
- No audit readback mechanisms
- No implicit permissions

---

### 3.4 Application_Functions/ (Stateless Reusable Logic)

**Authorized Classes:**
- Stateless function modules (.py)
- Curated artifact definitions (.py, .json)
- Expression and routing logic (.py)
- Non-semantic processing modules (.py)

**Placement Rules:**
- Stateless_Modules/: Pure functions, no side effects
- Curated_Artifacts/: User-scoped, non-semantic components

**Explicit Exclusions:**
- No mutable state
- No persistence logic
- No autonomous execution
- No semantic invention

---

### 3.5 Documentation/ (Design-Only Specifications)

**Authorized Classes:**
- Design specifications (.md)
- Type schemas (.md)
- Boundary contracts (.md)
- Cross-artifact binding maps (.md)
- Phase closure artifacts (.md)

**Placement Rules:**
- Design_Specifications/: Phase 2 and 3 artifacts
- Type_Schemas/: Phase 4 formal type definitions
- Boundary_Contracts/: A, B, C specifications

**Explicit Exclusions:**
- No executable documentation
- No code generation templates
- No runtime configuration
- No test specifications

---

### 3.6 Validation/ (Structural Integrity and Audit)

**Authorized Classes:**
- Integrity check scripts (.py)
- Hash validation records (.json)
- Audit log schemas (.json)
- Governance compliance reports (.md, .json)

**Placement Rules:**
- Integrity_Checks/: Deterministic validation only
- Audit_Records/: Immutable records, no readback

**Explicit Exclusions:**
- No runtime monitoring
- No audit readback to runtime
- No self-healing
- No autonomous validation

---

## 4. Artifact Class to Output Location Mapping

### 4.1 DR-AC Stage 1 (session_init) Outputs
**Generates:** None (postcondition validation only)  
**Target:** N/A

### 4.2 DR-AC Stage 2 (profile_loader) Outputs
**Generates:** Import graph for user profile loading  
**Target:** Runtime_Spine/Session_Management/

### 4.3 DR-AC Stage 3 (baseline_assembler) Outputs
**Generates:** Baseline assembly module  
**Target:** Runtime_Spine/Reconstruction_Pipeline/

### 4.4 DR-AC Stage 4 (artifact_overlay) Outputs
**Generates:** Overlay composition module  
**Target:** Runtime_Spine/Reconstruction_Pipeline/

### 4.5 DR-AC Stage 5 (reuse_decision) Outputs
**Generates:** Decision classification module  
**Target:** Runtime_Spine/Reconstruction_Pipeline/

### 4.6 DR-AC Stage 6 (compilation) Outputs
**Generates:** Session compilation module  
**Target:** Runtime_Spine/Reconstruction_Pipeline/

### 4.7 DR-AC Stage 8 (artifact_cataloger) Outputs
**Generates:** Cataloging and persistence gate module  
**Target:** Runtime_Spine/Reconstruction_Pipeline/

### 4.8 Canonical Input Loading Outputs
**Generates:** Primitive loader modules  
**Target:** Runtime_Spine/Orchestration/

### 4.9 Governance Validation Outputs
**Generates:** Safety gate query modules  
**Target:** Governance/

### 4.10 Documentation Generation Outputs
**Generates:** None (documentation is input, not output)  
**Target:** N/A

---

## 5. Explicit Exclusions (Forbidden Outputs)

The DR-AC rebuild MUST NOT generate:

### 5.1 Execution Infrastructure
- Test runners or test suites
- Main entry points or launch scripts
- Runtime orchestrators beyond reconstruction
- Continuous integration configurations
- Deployment scripts or packaging

### 5.2 Mutable State
- Database schemas or migration scripts
- Session persistence mechanisms
- State caching or memoization
- Log rotation or cleanup scripts
- Backup or recovery systems

### 5.3 Autonomous Components
- Self-modifying code
- Auto-scaling or resource management
- Health checks or monitoring daemons
- Automatic retry or recovery logic
- Policy adaptation mechanisms

### 5.4 External Integrations
- API client implementations
- Network protocol handlers
- External service connectors
- Authentication or authorization services
- Third-party library wrappers (beyond standard imports)

### 5.5 Development Tooling
- Debuggers or profilers
- Code formatters or linters
- Documentation generators
- Version control hooks
- Build system configurations

---

## 6. Governance Alignment Notes

### 6.1 Deny-by-Default (G1)
- Output tree structure is explicitly enumerated
- Any location not listed is forbidden
- Any artifact class not authorized is rejected

### 6.2 Fail-Closed (G2)
- Ambiguous output location → HALT
- Unauthorized artifact class → HALT
- Missing placement rule → HALT

### 6.3 No Authority Escalation (G7)
- Generated artifacts hold no execution authority
- No runtime permissions granted
- No autonomous operation enabled

### 6.4 No Audit Readback (G8)
- Validation/ outputs are write-only
- No runtime may query audit records
- Audit records are for human review only

### 6.5 Canonical Primitive Immutability (G4)
- Primitives/ is read-only during rebuild
- No generated artifact may modify primitives
- Primitives are inputs, never outputs

---

## 7. Declarative vs Imperative Posture

### 7.1 This Specification Is Declarative

This document:
- Declares what structure MUST exist post-rebuild
- Declares what artifact classes are authorized
- Declares what locations are valid outputs
- Does NOT describe how to execute the rebuild

### 7.2 This Specification Is NOT Imperative

This document does NOT:
- Define build procedures or scripts
- Specify execution order or parallelization
- Describe runtime behavior
- Grant execution authority

### 7.3 Enforcement

The rebuild pipeline MUST:
- Validate all outputs against this specification
- HALT if any output violates this specification
- Generate ONLY authorized artifact classes
- Write ONLY to authorized locations

---

## 8. Validation Checkpoints

### 8.1 Pre-Generation Validation
**Before generating any output:**
- Confirm artifact class is authorized
- Confirm output location is in canonical tree
- Confirm placement rule is satisfied

### 8.2 Post-Generation Validation
**After generating each output:**
- Verify file exists at authorized location only
- Verify artifact class matches specification
- Verify no forbidden content exists

### 8.3 Post-Rebuild Validation
**After completing entire rebuild:**
- Verify all required locations exist
- Verify no unauthorized locations exist
- Verify no forbidden artifact classes exist
- Verify structural integrity across tree

---

## 9. Closing Declaration

This canonical output tree specification:
- Is the ONLY authorized target for DR-AC rebuild outputs
- Is declarative and non-executable
- Enforces deny-by-default and fail-closed posture
- Maintains governance alignment throughout

Any output not explicitly authorized by this specification is forbidden.

Any violation of this specification results in immediate HALT.

---
