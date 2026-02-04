# Phase-2 Failure Modes (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)

Known failure/misuse scenarios and resolutions (fail-closed, deny + audit):
- Missing provenance on read or intake → deny and log (Phase-2.2, Phase-2.5).
- Privation metadata missing or conflicting → deny and log (Phase-2.3).
- Role not authorized or unspecified → deny and log (Phase-2.2).
- Schema mismatch for SMPs, plans, or external intake → deny and log (Phase-2.1.1, Phase-2.4, Phase-2.5).
- Attempted execution/activation/scheduling/ticks → deny and log (all phases, deny-by-default constraints).
- Planning escalation or chaining → deny and log (Phase-2.4 lifecycle bounds).
- External output without trust minimization → deny and log (Phase-2.5 wrappers and intake spec).
- Ambiguity or absence of explicit allowance → deny and log (global posture).

Declarative only; no runtime code or authorization objects are added.
