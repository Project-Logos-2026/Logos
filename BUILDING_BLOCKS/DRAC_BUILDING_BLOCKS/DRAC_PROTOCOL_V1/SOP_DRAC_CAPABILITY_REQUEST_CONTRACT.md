SOP_DRAC_CAPABILITY_REQUEST_CONTRACT
===================================

Purpose
-------
Defines the sole lawful interface by which SOP may request
real-time capability mediation from DRAC.

Request Object
--------------
{
  "session_id": "hash",
  "consumer_id": "protocol_or_agent_id",
  "priority": "P1 | P2",
  "required_AF_families": [],
  "required_CE_families": [],
  "constraints": {}
}

Rules
-----
- DRAC receives no semantic payloads
- Requests describe capability gaps only
- DRAC may return references or proposals
- No direct deployment without Logos approval

Failure Semantics
-----------------
- Unmet requests return NULL capability
- Execution stack must degrade gracefully