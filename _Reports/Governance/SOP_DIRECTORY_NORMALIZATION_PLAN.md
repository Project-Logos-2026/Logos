# SOP Directory Normalization Plan

This plan proposes a canonical SOP layout aligned to repository governance documents. No changes are made here.

## Target Canonical Layout (Title_Case_With_Underscores)
Location:
- LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/System_Operations_Protocol/

Proposed structure:
- System_Operations_Protocol/
  - Ops_Kernel/
  - Capability_Registry/
  - Policy_Engine/
  - Proof_Gate_Client/
  - Runtime_Bridge_Client/
  - SOP_Nexus/
  - Governance_Enforcement/
  - Fail_Closed_Mechanisms/
  - Telemetry/
  - Documentation/
  - Tools/

## Current vs Target Alignment
- Current SOP runtime-ops layer only has SOP_Nexus.
- Documentation expects Governance_Enforcement, Deployment_Control, Telemetry, Fail_Closed_Mechanisms, which are missing.
- BUILDING_BLOCKS contain SOP blueprint and legacy SOP logic; these should be relocated into SOP Documentation or archived.

## Naming Rules
- Directories and files should be Title_Case_With_Underscores.
- SOP operations-side nexus should avoid execution-core naming or placement.

## Documentation Placement
- SOP blueprint and SOP-DRAC contract should live under SOP Documentation or Governance Contracts.
- Existing SOP documentation references in DOCUMENTS should remain, but may need updates to reflect actual SOP runtime-ops path.

## Constraints
- Do not touch CSP or MTP internals.
- Do not modify execution-side Nexus implementations.
- SOP must only reference CSP/MTP via interface-level contracts.
