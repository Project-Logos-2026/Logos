# Phase-2 Threat Model (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)

Threat classes and blocking artifacts:
- implicit authority inference → blocked by deny-by-default posture across Phase-2 entries and privation dominance (Phase-2.3), plus Memory Safety (Phase-2.2) and planning inertness (Phase-2.4).
- execution-by-accident → blocked by non-executable SMP substrate (Phase-2.1.1), read-only UWM spec (Phase-2.2), inert planning lifecycle (Phase-2.4), and external untrusted boundary (Phase-2.5).
- external trust leakage → blocked by External Boundary Governance (Phase-2.5) requiring untrusted intake, privation + provenance + memory safety gating.
- memory mutation → blocked by Phase-2.1.1 SMP invariants (no writes), Phase-2.2 read-only UWM, privation dominance (Phase-2.3), and deny-by-default constraints.
- planning → action escalation → blocked by inert plan objects and validation-only pipeline (Phase-2.4), privation-first evaluation, and no scheduling/ticks/activation.

Declarative only; introduces no executable logic or authority.
