# SOP Core Component Map

This map defines required SOP components, their responsibilities, interfaces, and candidate files. No code changes are made here.

## Ops_Kernel
- Responsibility: Central operations authority, lifecycle control, and dispatch coordination.
- Inputs: Proof gate status, policy decisions, capability registry results, runtime bridge requests.
- Outputs: Approved operations dispatch requests; audit events.
- Forbidden: Reasoning, semantic interpretation, direct protocol control.
- Reuse/Refactor: [BUILDING_BLOCKS/SOP_BUILDING_BLOCKS/SOP_BLUEPRINT_DRAFT.md](BUILDING_BLOCKS/SOP_BUILDING_BLOCKS/SOP_BLUEPRINT_DRAFT.md) as design spec only.
- Delete: None (component missing; create new).

## Capability_Registry
- Responsibility: Canonical list of allowed operations and their prerequisites.
- Inputs: Governance artifacts, SOP policy definitions.
- Outputs: Capability admission decisions and capability metadata.
- Forbidden: Dynamic generation of capabilities; agent-driven escalation.
- Reuse/Refactor: [BUILDING_BLOCKS/DRAC_BUILDING_BLOCKS/DRAC_PROTOCOL_V1/SOP_DRAC_CAPABILITY_REQUEST_CONTRACT.md](BUILDING_BLOCKS/DRAC_BUILDING_BLOCKS/DRAC_PROTOCOL_V1/SOP_DRAC_CAPABILITY_REQUEST_CONTRACT.md) for DRAC request schema.
- Delete: None (component missing; create new).

## Policy_Engine
- Responsibility: Deny-by-default policy evaluation and authorization checks.
- Inputs: Governance artifacts, request metadata, capability registry.
- Outputs: Allow/deny decision and reasons; audit trail records.
- Forbidden: Reasoning about semantics, direct execution.
- Reuse/Refactor: None; create SOP policy module.
- Delete: None.

## Proof_Gate_Client
- Responsibility: Interface to STARTUP/PXL_Gate to verify proof status before dispatch.
- Inputs: Proof status requests, required proof artifacts.
- Outputs: Pass/fail with proof metadata.
- Forbidden: Running proofs directly inside SOP runtime-ops.
- Reuse/Refactor: Use documentation references for contract only; no code exists.
- Delete: None.

## Runtime_Bridge_Client
- Responsibility: Execute approved operations via the runtime bridge; enforce request contracts.
- Inputs: Approved ops requests, capability tokens.
- Outputs: Dispatch results, error states, audit events.
- Forbidden: Direct execution-side nexus access.
- Reuse/Refactor: None; define SOP bridge interface only.
- Delete: None.

## SOP_Nexus (Operations-Side Only)
- Responsibility: Register SOP components, sequence SOP startup, expose health state.
- Inputs: SOP component registrations, health signals.
- Outputs: SOP status and readiness signals.
- Forbidden: Policy decisions, proof evaluation, or semantic operations.
- Reuse/Refactor: [BUILDING_BLOCKS/SOP_BUILDING_BLOCKS/SOP_Nexus/sop_nexus_orchestrator.py](BUILDING_BLOCKS/SOP_BUILDING_BLOCKS/SOP_Nexus/sop_nexus_orchestrator.py) for naming only; requires full rewrite.
- Delete: [BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_nexus.py](BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_nexus.py) once replaced.

## Supporting SOP Utilities (Non-Authoritative)
- Audit log writer (append-only)
- Telemetry emitters
- Schema validators

Candidate legacy sources (to rewrite, not reuse):
- [BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_operations.py](BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_operations.py)
- [BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_nexus.py](BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_nexus.py)
