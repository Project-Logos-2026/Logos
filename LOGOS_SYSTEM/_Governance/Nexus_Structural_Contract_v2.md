# Nexus Structural Contract v2

## CATEGORY A — EXECUTION_NEXUS

Definition:
Runtime execution boundary.

Required structural signals:
- Has tick, register_participant, ingest methods
- Imports or invokes MeteredReasoningEnforcer (MRE)
- Imports or invokes MeshEnforcer
- Fail-closed raise behavior
- No dynamic imports

Current expected members:
- ARP_Nexus.py
- SCP_Nexus.py

---

## CATEGORY B — BINDING_NEXUS

Definition:
Protocol or Agent binding layer.
Deterministic runtime boundary without MRE enforcement.

Structural signals:
- Has tick/register/ingest OR equivalent binding surface
- Fail-closed raise behavior
- Does NOT import MRE
- Does NOT perform pipeline orchestration
- No dynamic imports

Current expected members:
- I1_Nexus
- I2_Nexus
- I3_Nexus
- Logos_Agent_Nexus
- Logos_Protocol_Nexus
- CSP_Nexus
- DRAC_Nexus
- EMP_Nexus
- SOP_Nexus

---

## CATEGORY C — NON_NEXUS

Definition:
Files ending in *_Nexus.py that do not meet Execution or Binding definition.

Includes:
- Test modules
- Legacy/forbidden modules
- Composite memory modules
- Pipeline orchestration shells
- Misnamed artifacts

---

## EXCLUSIONS

Exclude from scan:
- Files in any TEST directory
- Files containing header markers:
    EXECUTION: FORBIDDEN
    LEGACY_REWRITE_CANDIDATE
- Files under */TEST_SUITE/*
