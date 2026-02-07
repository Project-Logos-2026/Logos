# EMP Runtime Role

EMP provides bounded epistemic tagging via the meta-reasoner and a Standard Nexus with explicit pre/post gates. It assigns provisional or canonical-candidate epistemic_state based on proof_state without autonomous reasoning. The Nexus enforces mesh validation and deterministic routing.

Supported invariants:
- Reasoning budget enforcement
- Deterministic tick ordering and mesh enforcement
- Fail-closed on invalid packets

Removal impact analysis:
- Epistemic tagging and EMP routing would be unavailable to downstream systems.

Prohibited extensions:
- No autonomous inference or goal selection
- No authority escalation or SOP mutation
- No external IO beyond explicit gating utilities
