# SOP Lifecycle Boundary — Design-Only Declaration

Status: DESIGN_ONLY
Authority: NONE
Execution: FORBIDDEN

## Purpose

This document designates the **future canonical lifecycle boundary** for the
System Operations Protocol (SOP).

It introduces:
- no execution,
- no logic,
- no wiring,
- no authority.

## Observation

As of this revision, SOP has **no authoritative lifecycle coordinator**.
All existing SOP modules operate as utilities, subsystems, or façades.

## Designated Boundary (Future)

The canonical SOP lifecycle boundary SHALL be defined at:

SYSTEM/System_Stack/System_Operations_Protocol/infrastructure/agent_system/

Rationale:
- This subtree is the first point where SOP participates in system-level coordination.
- It is the earliest location where SOP can meaningfully be said to "enter runtime."
- No lifecycle logic is currently present here.

## Telemetry Note

When lifecycle logic is later introduced, the following calls MAY be placed
at this boundary:

- sop_init()
- sop_active_limited()
- sop_halt()
- sop_inert()

No such calls are permitted prior to explicit authorization.

## Governance

This document is declarative only.
It does not grant permission to implement or wire lifecycle logic.
