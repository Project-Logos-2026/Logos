# Phase-2.5 External Interface Governance (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)

## Boundary Definition
- External tools, models, APIs, CLIs, libraries, and services are outside the trust boundary.
- All external systems are untrusted by default; no implicit authority is granted.

## Prohibitions
- No direct execution of external outputs.
- No external writes to memory or SMPs.
- No planning influence, scheduling, or activation from external systems.
- No bypass of privation, provenance, or memory safety.

This is declarative only and adds no executable logic.
