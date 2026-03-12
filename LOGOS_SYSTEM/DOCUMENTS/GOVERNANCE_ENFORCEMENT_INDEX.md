# GOVERNANCE_ENFORCEMENT_INDEX.md

## LOGOS Governance → Runtime Enforcement Index

This document maps **specific governance artifacts** to their **exact runtime
enforcement points**.

Governance files are never imported directly by agents.

---

## Phase Definitions

**Governance/**
- `Phase_Definitions/*.json|md`

**Enforced By**
- `Logos_Protocol/Activation_Sequencing/`
- `STARTUP/PXL_Gate/state/activation_state/`

**Effect**
- Blocks activation outside allowed phase
- Prevents runtime escalation

---

## Lifecycle Boundaries

**Governance/**
- `Lifecycle_Boundaries/*.md`

**Enforced By**
- `System_Operations_Protocol/Governance_Enforcement/`
- `SOP_Nexus`

**Effect**
- Prevents illegal state transitions
- Enforces irreversible phase exits

---

## Autonomy Policies

**Governance/**
- `Autonomy_Policies/*.json`

**Enforced By**
- `Logos_Agent/mutation_gates/`
- `System_Operations_Protocol/Fail_Closed_Mechanisms/`

**Effect**
- Denies implicit autonomy
- Forces explicit authorization paths

---

## Denial Invariants

**Governance/**
- `Denial_Invariants/*.md`

**Enforced By**
- `SOP_Nexus`
- `STARTUP/PXL_Gate`

**Effect**
- Default deny
- Immediate halt on violation

---

## Design-Only Declarations

**Governance/**
- `Design_Only_Declarations/*.md|json`

**Enforced By**
- `STARTUP/PXL_Gate`
- `Logos_Protocol`
- `SOP_Nexus`

**Effect**
- Prevents execution of design-only artifacts
- Forces descriptive-only behavior

---

## Enforcement Rule

If a governance file cannot be loaded, parsed, or validated:

> **Runtime must fail closed.**
