# Phase-2.5 External Deprecation Map (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)

## Legacy / Related External References
- Automation/orchestrator packets referencing external tools, provenance pins, or adapters (e.g., Start_Agent packets, Logos_AGI pin verification helpers) — informational only; not trusted, not executable.
- _Dev_Resources/Dev_Invariables/semantic_capability_map_v0.json entries involving external or UWM/ARP interactions — informational; non-authoritative.
- Any legacy adapter stubs or grouping metadata mentioning external interfaces — informational only.

## Canonical Posture
- External systems are untrusted; intake-only with privation + provenance + memory safety gating.
- No direct execution, no memory writes, no planning influence.

Declarative only; no runtime logic introduced.
