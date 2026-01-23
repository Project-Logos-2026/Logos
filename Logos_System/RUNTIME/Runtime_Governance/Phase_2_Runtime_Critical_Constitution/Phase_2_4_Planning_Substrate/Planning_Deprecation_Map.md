# Phase-2.4 Planning Deprecation Map (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)

## Legacy / Related Artifacts
- Logos_System/Planning_Runtime/Plan_Objects (plan_schema.py, plan_serialization.py, plan_validation.py) — non-executable design/validation modules from Phase-P; informational; superseded for canonical schema by this phase’s Plan_Object_Spec.
- _Dev_Resources/Dev_Scripts/smoke_tests/test_logos_runtime_smoke.py — legacy minimal SMP/plan pathway; informational only; not authoritative.
- _Dev_Resources/Dev_Invariables/runtime_spine_contract_v1.json — historical runtime spine with planning references; informational; superseded.
- _Dev_Resources/SYSTEM_STACK_AUTOMATED_GROUPING.json — grouping metadata listing planning/ARP references; non-authoritative.
- Any ARP references in automation/orchestrator packets — legacy, informational only; not executable.

## Canonical Path Forward
- Use Phase-2.4 plan schema and validation pipeline for any planning data representations.
- Plans remain inert, non-executable, and denied by default.

Declarative only; no runtime changes are introduced.
