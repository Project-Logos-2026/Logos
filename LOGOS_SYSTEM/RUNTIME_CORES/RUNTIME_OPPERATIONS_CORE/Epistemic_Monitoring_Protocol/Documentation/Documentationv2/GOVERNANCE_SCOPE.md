# EMP Governance Scope

Applicable governance layers:
- LOGOS
- UNSPECIFIED

Permissions:
- Apply bounded epistemic tagging
- Register participants and route packets via Nexus
- Enforce mesh constraints and MRE gating

Prohibitions:
- No agent reasoning or inference
- No authority expansion or capability grants
- No SOP mutation or external execution

Enforcement points:
- PreProcessGate and PostProcessGate
- MeshEnforcer
- MREGovernor

Non-authority declaration:
- This protocol does not confer or expand authority.

Coq verification clarification:
- Coq subprocess invocation for proof compilation is classified as mechanical
  bounded epistemic tagging, not reasoning or inference.
- Coq subprocess is a verification tool, not an execution environment.
- No Coq-compiled artifacts (.vo) are executed at runtime.
- All Coq verification results are emitted as non-authoritative ProtocolAAs.
