# I3_Agent Runtime Role

I3_Agent provides deterministic planning skeletons and context-span metadata for ARP operations, with a Standard Nexus for safe routing. Core modules shape plan structure without autonomous goal selection.

Supported invariants:
- Deterministic plan skeleton generation
- Mesh enforcement and MRE gating at the Nexus
- Fail-closed behavior on invalid packets

Removal impact analysis:
- I3 routing and ARP integration metadata would be unavailable.
- Downstream ARP planning pipelines would lose deterministic skeletonization.

Prohibited extensions:
- No autonomous inference or goal selection
- No authority escalation or SOP mutation
- No external IO or tool execution
