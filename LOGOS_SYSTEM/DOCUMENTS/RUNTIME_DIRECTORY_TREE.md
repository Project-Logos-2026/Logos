# RUNTIME_DIRECTORY_TREE.md

## LOGOS System — Runtime Directory Tree (Authoritative)

This document enumerates the **authoritative runtime directory structure** for the
LOGOS System as defined in the current `main` branch.

Only directories and modules that are **required or reachable during runtime or
descriptive simulation** are included.

The following are intentionally excluded:
- ARCHIVE (historical / frozen snapshots)
- DEV_RESOURCES (rewrite tooling, migration helpers)
- Top-level COQ (research / legacy; runtime gates live under STARTUP)

---

## Runtime Root

```text
LOGOS_SYSTEM/
├── SYSTEM/
│   └── System_Stack/
│       │
│       ├── Logos_Agents/
│       │   ├── I1_Agent/                         # SCP-bound (Sign Principle)
│       │   │   ├── identity/
│       │   │   ├── intake/
│       │   │   └── validation/
│       │   │
│       │   ├── I2_Agent/                         # MTP-bound (Bridge Principle)
│       │   │   ├── interpretation/
│       │   │   ├── translation/
│       │   │   └── mediation/
│       │   │
│       │   ├── I3_Agent/                         # ARP-bound (Mind Principle)
│       │   │   ├── reasoning/
│       │   │   ├── evaluation/
│       │   │   └── coherence_checks/
│       │   │
│       │   └── Logos_Agent/                      # SOP-bound (System Authority)
│       │       ├── activation/
│       │       ├── orchestration/
│       │       ├── mutation_gates/
│       │       ├── IEL_Generation/
│       │       ├── Module_Authoring/
│       │       └── System_Mutation_Gates/
│       │
│       ├── Logos_Protocol/
│       │   ├── Activation_Sequencing/
│       │   ├── Runtime_Orchestration/
│       │   ├── Safety_Gates/
│       │   └── Unified_Working_Memory/
│       │       ├── SMP/
│       │       ├── State/
│       │       └── Read_Write_Policies/
│       │
│       ├── Meaning_Translation_Protocol/
│       │   ├── Interpretation_Core/
│       │   ├── Semantic_Normalization/
│       │   ├── SMP_Packetization/
│       │   └── Interface_Layer/
│       │
│       ├── Synthetic_Cognition_Protocol/
│       │   ├── SCP_Nexus/
│       │   │   ├── sign_resolution/
│       │   │   └── constraint_binding/
│       │   │
│       │   ├── MVS_System/
│       │   │   ├── modal_axes/
│       │   │   ├── vector_projection/
│       │   │   └── triangulation/
│       │   │
│       │   └── BDN_System/
│       │       ├── belief_nodes/
│       │       ├── dependency_graphs/
│       │       └── stabilization/
│       │
│       ├── System_Operations_Protocol/
│       │   ├── SOP_Nexus/
│       │   ├── Governance_Enforcement/
│       │   ├── Deployment_Control/
│       │   ├── Telemetry/
│       │   └── Fail_Closed_Mechanisms/
│       │
│       └── PXL/
│           ├── axioms/
│           ├── operators/
│           ├── modal_structure/
│           └── proof_interfaces/
│
├── STARTUP/
│   └── PXL_Gate/                                # Runtime proof + activation gate
│       ├── Protopraxis/
│       │   ├── primitives/
│       │   └── grounding/
│       │
│       ├── coq/
│       │   └── src/
│       │       ├── baseline/
│       │       ├── modal/
│       │       ├── triune/
│       │       └── tests/
│       │
│       └── state/
│           ├── lock_files/
│           ├── activation_state/
│           └── proof_status/
│
├── Governance/
│   ├── Phase_Definitions/
│   ├── Lifecycle_Boundaries/
│   ├── Autonomy_Policies/
│   ├── Denial_Invariants/
│   └── Design_Only_Declarations/
│
└── SYSTEM_AUDIT_LOGS/
    ├── autonomy/
    ├── state/
    ├── activation/
    └── test_logs/
