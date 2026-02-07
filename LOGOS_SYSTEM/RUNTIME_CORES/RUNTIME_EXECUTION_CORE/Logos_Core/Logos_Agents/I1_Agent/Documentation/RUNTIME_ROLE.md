# I1_Agent Runtime Role

I1_Agent provides deterministic integration utilities for SCP/epistemic handling and a Standard Nexus for safe routing. The core modules add traceability and coverage metadata without modifying semantic content.

Supported invariants:
- Deterministic metadata enrichment
- Mesh enforcement and MRE gating at the Nexus
- Fail-closed behavior on invalid packets

Removal impact analysis:
- I1 routing and SCP integration metadata would be unavailable.
- Downstream SCP operations would lose determinism and trace signals.

Prohibited extensions:
- No autonomous inference or belief formation
- No authority escalation or SOP mutation
- No external IO or tool execution
