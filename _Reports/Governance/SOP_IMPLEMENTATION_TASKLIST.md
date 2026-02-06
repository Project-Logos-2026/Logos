# SOP Implementation Task List

This is an execution-ready task list for a future session. No changes are made here.

## Phase A — Structure and Documentation
1. Create SOP runtime-ops directory structure per SOP_DIRECTORY_NORMALIZATION_PLAN.
2. Add SOP Documentation folder and move SOP blueprint into Documentation.
3. Create SOP Governance_Enforcement/Contracts and move SOP-DRAC contract into it.
4. Add SOP MANIFEST.md and RUNTIME_ROLE.md in Documentation (design-only).

## Phase B — Core Component Definitions
5. Implement Ops_Kernel scaffold with explicit responsibilities and deny-by-default stance.
6. Implement Capability_Registry with static capability schema and proof requirements.
7. Implement Policy_Engine with explicit authorization checks and failure reasons.
8. Implement Proof_Gate_Client interface to STARTUP/PXL_Gate (no proof execution).
9. Implement Runtime_Bridge_Client interface with strict request validation.

## Phase C — SOP Nexus (Operations-Side Only)
10. Replace SOP_Nexus with ops-only orchestration logic (no execution-side nexus core).
11. Add Sop_Nexus_Orchestrator with component registration and readiness checks.
12. Add Health_State_Manager and Service_Registry within SOP_Nexus.

## Phase D — Governance and Safety
13. Add Fail_Closed_Mechanisms module that halts on missing governance artifacts.
14. Add Audit_Log_Writer (append-only) under SOP Tools.
15. Add Telemetry emitters with explicit non-semantic constraints.
16. Add explicit deny-by-default gating for all SOP dispatch paths.

## Phase E — Legacy Cleanup
17. Archive legacy SOP artifacts from BUILDING_BLOCKS/INVARIABLES into _Dev_Resources/Archive/Legacy_SOP.
18. Remove or replace SOP_BUILDING_BLOCKS/SOP_Nexus placeholder after SOP Nexus rewrite.

## Phase F — Tests and Validation
19. Rewrite SOP tests to target actual SOP runtime-ops modules.
20. Add tests for policy denial, proof gating, capability admission, and audit logging.
21. Add tests for fail-closed behavior on missing governance artifacts.

## Phase G — Documentation Updates
22. Update DOCUMENTS/RUNTIME_DIRECTORY_TREE.md to reflect actual SOP runtime-ops path if needed.
23. Update DOCUMENTS/GOVERNANCE_ENFORCEMENT_INDEX.md with SOP enforcement locations once implemented.
24. Update DOCUMENTS/FAIL-CLOSED_RUNTIME_CHECKLIST.md to reference new SOP modules.

## Phase H — Final Audit
25. Verify SOP adheres to ops-only boundary and no CSP/MTP internals are imported.
26. Ensure Title_Case_With_Underscores naming across SOP directories and files.
27. Review for any remaining bypass paths or legacy imports.
