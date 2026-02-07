# Cognitive_State_Protocol Runtime Role

CSP provides operations-layer state routing and memory substrate utilities. The Nexus enforces deterministic tick orchestration, mesh validation, MRE gating, and provisional proof tagging on egress. The Core includes memory and unified working memory utilities, including snapshot helpers and structural stubs.

Supported invariants:
- Deterministic tick ordering and mesh enforcement
- MRE pre/post gating
- Fail-closed behavior on invalid packets

Removal impact analysis:
- Nexus removal disables CSP routing and state exchange for registered participants.
- Memory/UWM removal breaks snapshot utilities and memory substrate availability.

Prohibited extensions:
- No agent reasoning or autonomous goal selection
- No governance authority escalation or SOP mutation
- No external IO beyond explicit snapshot utilities
