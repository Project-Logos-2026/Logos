SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: Runtime_Contract
ARTIFACT_NAME: ARTIFACT_ROUTER_CONTRACT
VERSION: 1.0
DATE: 2026-03-11
AUTHORITY: Architect
SUBSYSTEM: Execution_Context

---------------------------------------------------------------------

PURPOSE

Defines the contract governing all artifact write operations during
AP_V2 tooling execution.

---------------------------------------------------------------------

CONTRACT RULES

1. All artifact writes must be mediated by the artifact router.
2. Direct filesystem writes are prohibited.
3. Write path must satisfy:

   write_path ∈ artifact_router.allowed_paths

4. Any write not mediated by artifact router must halt execution.

---------------------------------------------------------------------

ALLOWED WRITE SURFACES

AP_SYSTEM_CONFIG/SYSTEM/REPORTS/
AP_SYSTEM_CONFIG/SYSTEM/EXECUTION_ENVELOPES/
AP_SYSTEM_CONFIG/SYSTEM/VALIDATION/
AP_SYSTEM_CONFIG/SYSTEM/EXECUTION_CONTEXT/

---------------------------------------------------------------------

PROHIBITED WRITE SURFACES

AP_SYSTEM_CONFIG/CLAUDE/
AP_SYSTEM_CONFIG/GPT/
AP_SYSTEM_CONFIG/VS_CODE/
Any path outside AP_SYSTEM_ROOT

---------------------------------------------------------------------

ENFORCEMENT

The artifact router must:

• log every write operation
• reject writes to prohibited surfaces
• record artifact identity before and after each write
• emit a routing event for each write in the execution log
