# SOP Governance Fix Plan

This plan addresses SOP governance gaps without implementing changes here.

## 1) Establish Deny-by-Default Policy Engine
- Create a Policy_Engine under SOP runtime-ops layer.
- Require explicit allow-list checks for every operation.
- Emit structured denial reasons for audit logging.

## 2) Implement Capability_Registry
- Define canonical capability records and required proofs.
- Bind DRAC capability request schema where applicable.
- Disallow dynamic capability creation.

## 3) Add Proof_Gate_Client
- Create an interface-only client to STARTUP/PXL_Gate.
- Require proof discharge status for any SOP dispatch.
- Fail-closed on missing proof state.

## 4) Add Runtime_Bridge_Client
- Implement a strict bridge interface for executing approved ops.
- Require policy approval + proof approval + capability admission.

## 5) Add Immutable Audit Logging
- Provide append-only audit writer in SOP tools.
- Deny any audit readback into runtime.

## 6) Implement Fail-Closed Mechanisms
- Add SOP fail-closed checks aligned to governance artifacts.
- If governance artifacts are missing or invalid, deny all operations.

## 7) Remove Legacy Bypass Paths
- Deprecate legacy SOP nexus and ops scripts in BUILDING_BLOCKS/INVARIABLES.
- Replace placeholders with SOP-only, ops-side orchestration.

## 8) Update Tests to Match SOP Runtime-ops Paths
- Rewrite SOP tests to match actual SOP module paths.
- Add tests for deny-by-default, proof gating, and audit logging.

## Reference Constraints
- [DOCUMENTS/GOVERNANCE_ENFORCEMENT_INDEX.md](DOCUMENTS/GOVERNANCE_ENFORCEMENT_INDEX.md)
- [DOCUMENTS/FAIL-CLOSED_RUNTIME_CHECKLIST.md](DOCUMENTS/FAIL-CLOSED_RUNTIME_CHECKLIST.md)
- [DOCUMENTS/RUNTIME_DEPENDENCY_AND_GOVERNANCE_MAPPING.md](DOCUMENTS/RUNTIME_DEPENDENCY_AND_GOVERNANCE_MAPPING.md)
