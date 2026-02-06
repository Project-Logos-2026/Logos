# SOP Rename and Move Map

This is a proposed rename/move plan. No changes are made here.

## Documentation and Contracts
| Source | Target | Notes |
| --- | --- | --- |
| [BUILDING_BLOCKS/SOP_BUILDING_BLOCKS/SOP_BLUEPRINT_DRAFT.md](BUILDING_BLOCKS/SOP_BUILDING_BLOCKS/SOP_BLUEPRINT_DRAFT.md) | LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/System_Operations_Protocol/Documentation/SOP_Blueprint_Draft.md | Preserve design-only status and update paths. |
| [BUILDING_BLOCKS/DRAC_BUILDING_BLOCKS/DRAC_PROTOCOL_V1/SOP_DRAC_CAPABILITY_REQUEST_CONTRACT.md](BUILDING_BLOCKS/DRAC_BUILDING_BLOCKS/DRAC_PROTOCOL_V1/SOP_DRAC_CAPABILITY_REQUEST_CONTRACT.md) | LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/System_Operations_Protocol/Governance_Enforcement/Contracts/SOP_Drac_Capability_Request_Contract.md | Move contract into SOP governance scope. |

## SOP Nexus Orchestrator
| Source | Target | Notes |
| --- | --- | --- |
| [BUILDING_BLOCKS/SOP_BUILDING_BLOCKS/SOP_Nexus/sop_nexus_orchestrator.py](BUILDING_BLOCKS/SOP_BUILDING_BLOCKS/SOP_Nexus/sop_nexus_orchestrator.py) | LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/System_Operations_Protocol/SOP_Nexus/Sop_Nexus_Orchestrator.py | Replace stub with ops-only orchestrator. |

## Legacy SOP Artifacts
| Source | Target | Notes |
| --- | --- | --- |
| [BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_nexus.py](BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_nexus.py) | _Dev_Resources/Archive/Legacy_SOP/sop_nexus.py | Archive after SOP replacement is implemented. |
| [BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_operations.py](BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_operations.py) | _Dev_Resources/Archive/Legacy_SOP/sop_operations.py | Archive after SOP replacement is implemented. |
| [BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_nexus_orchestrator.py](BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_nexus_orchestrator.py) | _Dev_Resources/Archive/Legacy_SOP/sop_nexus_orchestrator.py | Archive after SOP replacement is implemented. |

## SOP Runtime-ops Nexus
| Source | Target | Notes |
| --- | --- | --- |
| [LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/System_Operations_Protocol/SOP_Nexus/SOP_Nexus.py](LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/System_Operations_Protocol/SOP_Nexus/SOP_Nexus.py) | LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/System_Operations_Protocol/SOP_Nexus/Sop_Nexus_Core.py | Split ops-only nexus core from façade if needed; keep execution-side logic out. |
