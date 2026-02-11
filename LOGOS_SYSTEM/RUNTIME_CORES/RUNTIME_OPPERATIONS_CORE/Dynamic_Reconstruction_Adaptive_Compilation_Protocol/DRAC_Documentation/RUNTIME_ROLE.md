# DRAC Runtime Role

DRAC provides deterministic phase orchestration for reconstruction/assembly and a Standard Nexus for safe routing. The core is explicitly non-epistemic and does not mutate runtime authority. The Nexus enforces mesh validation, MRE gating, and deterministic routing.

Supported invariants:
- Deterministic phase transitions
- Fail-closed behavior on invalid phase transitions
- Deterministic tick ordering with mesh enforcement

Removal impact analysis:
- Phase orchestration and visibility are lost for DRAC-dependent workflows.
- Nexus removal disables DRAC participant routing and state exchange.

Prohibited extensions:
- No inference, proof evaluation, or belief formation
- No authority escalation or SOP mutation
- No external IO beyond explicit orchestration outputs
