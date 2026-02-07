# SOP Runtime Role

SOP provides operations-layer routing through the Standard Nexus and includes a local scan utility for proof-gate bypass detection. The Nexus enforces deterministic routing, mesh validation, and MRE gating. The scan utility performs repository scans and reports findings via return codes.

Supported invariants:
- Deterministic tick ordering and mesh enforcement
- Fail-closed behavior on invalid packets
- Scan utility is local-only and does not confer authority

Removal impact analysis:
- SOP Nexus removal disables SOP packet routing.
- scan_bypass removal eliminates proof-gate bypass scanning tooling.

Prohibited extensions:
- No agent reasoning or autonomous goal selection
- No authority escalation or SOP mutation beyond defined utilities
- No external IO beyond local scan output
