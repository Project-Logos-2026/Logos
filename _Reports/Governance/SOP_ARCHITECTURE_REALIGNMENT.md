# SOP Architecture Realignment

This document realigns SOP to its intended operations-only role based on authoritative repo documentation. No code changes are made here.

## Intended SOP Role (Authoritative)
Sources:
- [DOCUMENTS/RUNTIME_DIRECTORY_TREE.md](DOCUMENTS/RUNTIME_DIRECTORY_TREE.md)
- [DOCUMENTS/GOVERNANCE_ENFORCEMENT_INDEX.md](DOCUMENTS/GOVERNANCE_ENFORCEMENT_INDEX.md)
- [DOCUMENTS/RUNTIME_DEPENDENCY_AND_GOVERNANCE_MAPPING.md](DOCUMENTS/RUNTIME_DEPENDENCY_AND_GOVERNANCE_MAPPING.md)
- [DOCUMENTS/RUNTIME_IMPORT_AND_AUTHORITY_GRAPH.md](DOCUMENTS/RUNTIME_IMPORT_AND_AUTHORITY_GRAPH.md)
- [DOCUMENTS/RUNTIME_GOVERNANCE_ALIGNMENT.md](DOCUMENTS/RUNTIME_GOVERNANCE_ALIGNMENT.md)

SOP must be:
- Operations authority and governance enforcement
- Proof-gated for any dispatch
- Observability-only (no semantic reasoning)
- Deny-by-default and fail-closed
- Interfaced to CSP and MTP only via bridge-level interfaces

## Current State Observations
- SOP runtime-ops layer exists only as [LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/System_Operations_Protocol/SOP_Nexus/SOP_Nexus.py](LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/System_Operations_Protocol/SOP_Nexus/SOP_Nexus.py), which is an execution-side Nexus core and not SOP-specific operations authority.
- SOP governance enforcement directories referenced in documentation do not exist under the SOP runtime-ops layer.
- Legacy SOP implementations exist in BUILDING_BLOCKS and include self-improvement and broad orchestration behaviors that violate SOP boundaries.

## Realignment Targets
SOP should depend on, and only on, the following interfaces:
- Runtime Bridge (execution dispatch)
- PXL Gate (proof discharge and activation status)
- CSP (state hydration interface only)
- MTP (translation interface only)

SOP should explicitly avoid:
- Any reasoning or semantic interpretation
- Any direct execution-side Nexus implementation
- Any direct protocol startup orchestration
- Any direct mutation beyond SOP authority scope

## Realignment Actions (Planning Only)
- Replace execution-side Nexus core usage with an operations-side SOP Nexus façade that only orchestrates SOP components.
- Introduce SOP-bound governance enforcement and fail-closed mechanisms per documentation.
- Define explicit SOP interfaces to CSP/MTP without importing CSP/MTP internals.
- Isolate or delete legacy SOP code paths that include self-improvement or broad execution control.

## Dependencies to Enforce
- SOP activation is gated by STARTUP/PXL_Gate proof status.
- SOP governance enforcement is the sole loader of governance artifacts (no direct agent import).
- SOP writes to audit logs are append-only and do not allow readback into runtime.
