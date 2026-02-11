# Epistemic Monitoring Protocol (EMP) — Native Coq Proof Engine

## Overview

EMP is a P2 (priority-two) protocol in the LOGOS runtime responsible for
epistemic classification of artifacts through mechanical proof verification.
This build transforms EMP from a 14-line stub classifier into a native Coq
proof engine with search, template derivation, abstraction, and MSPC coherence
witness capabilities.

EMP remains a non-reasoning, non-assertive protocol. All verification is
mechanical. All outputs are non-authoritative ProtocolAAs. Logos Agent alone
evaluates them for promotion decisions.

## Directory Structure

```
Epistemic_Monitoring_Protocol/
├── EMP_Core/
│   ├── __init__.py                  Package initializer
│   ├── EMP_Coq_Bridge.py           Coq subprocess management (Phase E1)
│   ├── EMP_Meta_Reasoner.py        Six-tier Coq-backed classifier (Phase E2)
│   ├── EMP_Proof_Index.py          Session-scoped proof index and search (Phase E3)
│   ├── EMP_Template_Engine.py      Proof template extraction (Phase E5)
│   └── EMP_Abstraction_Engine.py   Structural pattern operations (Phase E6)
├── EMP_Nexus/
│   ├── __init__.py                  Package initializer
│   ├── EMP_Nexus.py                 Enhanced Standard Nexus (Phase E4)
│   ├── Library_Manifest.py          Allowed library registry (preserved)
│   └── EMP_MSPC_Witness.py          MSPC coherence integration (Phase E7)
├── EMP_Documentation/
│   ├── EMP_TO_SOP_CONTRACT_SCHEMA.md  SOP contract (preserved)
│   └── EMP_PROOF_RESULT_SCHEMA.md     Proof result AA schema (Phase E2)
└── Documentation/
    ├── GOVERNANCE_SCOPE.md           Governance scope (preserved + Coq clarification)
    ├── MANIFEST.md                   File inventory (updated)
    ├── METADATA.json                 Protocol metadata (updated)
    ├── ORDER_OF_OPERATIONS.md        Operational flows (updated)
    ├── RUNTIME_ROLE.md               Runtime role (updated)
    ├── STACK_POSITION.md             Dependency map (updated)
    └── README.md                     This file
```

## Classification Tiers

EMP assigns six monotonic classification states:

| Tier | Label | Confidence Uplift | Condition |
|------|-------|-------------------|-----------|
| 0 | UNVERIFIED | 0.00 | No proof content or no Coq bridge |
| 1 | PROVISIONAL | 0.02 | Coq compilation fails |
| 2 | PARTIAL | 0.05 | Compiles but contains Admitted proofs |
| 3 | VERIFIED_AXIOMATIC | 0.10 | Zero admits, axioms exceed PXL kernel |
| 4 | VERIFIED_PXL | 0.15 | Zero admits, all axioms in PXL kernel |
| 5 | CANONICAL_CANDIDATE | 0.20 | VERIFIED_PXL + MSPC coherence PASS |

No artifact may skip classification levels. Budget exhaustion halts at current
state. All errors fail closed to UNVERIFIED.

## Module Summary

### EMP_Coq_Bridge (Phase E1)
Manages Coq subprocess lifecycle. Submits .v content for compilation, parses
structured output, enforces compilation timeouts, maintains loadpath
configuration matching PXL_Gate _CoqProject semantics.

### EMP_Meta_Reasoner (Phase E2)
Replacement for original 14-line stub. Delegates to EMP_Coq_Bridge for
verification, assigns six-tier classification, produces structured EMP_PROOF_RESULT
AAs. Preserves original budget enforcement interface.

### EMP_Proof_Index (Phase E3)
Session-scoped index of all verified proofs. Supports search by name or axiom,
dependency graph traversal, axiom footprint analysis, gap detection, and
coverage reporting. Rebuilt on each session.

### EMP_Nexus (Phase E4)
Enhanced Standard Nexus. PostProcessGate upgraded with Coq-backed proof tagging
when Meta Reasoner is available. Backward-compatible keyword fast-path preserved
for non-proof payloads.

### EMP_Template_Engine (Phase E5)
Extracts reusable proof templates from verified proofs. Produces parameterized
skeletons, validates instantiations via re-verification. All templates are
non-authoritative per Phase-3.1, bound to source via cryptographic hash.

### EMP_Abstraction_Engine (Phase E6)
Mechanical abstraction operations: generalization, lemma suggestion, cross-module
pattern mining, complexity analysis. All candidates tagged UNVERIFIED until
re-verified via EMP_Coq_Bridge.

### EMP_MSPC_Witness (Phase E7)
Integration point for MSPC coherence witness under Octafolium architecture.
Routes four-modality expressibility checks via Logos Agent. Gates
CANONICAL_CANDIDATE classification.

## Dependencies

- PXL_Gate Coq baseline: STARTUP/PXL_Gate/coq/ (60 .v files, _CoqProject)
- Coq environment: coqc on system PATH or jsCoq WebAssembly
- MSPC Protocol: LOGOS_SYSTEM/Runtime_Protocols/MSPC/ (Phase E7 only)
- Logos Agent: routing relay for MSPC communication

## Governance

All capabilities fall within existing EMP governance scope. No new authority.
No new permissions. Coq verification is classified as mechanical bounded
epistemic tagging. All outputs are non-authoritative ProtocolAAs. EMP-to-SOP
contract remains advisory-only, one-way, MRE enforced.

## Deployment Gate

Deployment requires:
1. Coq environment path resolution (coqc available on target system)
2. MSPC Protocol operational readiness (Phase E7 gating)
3. PXL kernel axiom set formal declaration
4. Logos Agent approval of MSPC routing path

Until these conditions are met, METADATA.json shows ready_for_deployment: false.

## Build Provenance

Design authority: EMP_NATIVE_COQ_PROOF_ENGINE_BLUEPRINT_AND_ROADMAP.md
Build phases: E1 through E8
Estimated effort: 18-26 days (minimum viable: E1+E2+E4 in 6-10 days)
