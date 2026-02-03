# Phase-3.1 Derived Policy Compiler Charter (Design-Only)

Status: DESIGN_ONLY — NON-EXECUTABLE — NON-AUTHORIZING
Authority: DENY (default)

## Purpose & Scope
Phase-3.1 governs whether and how existing governance artifacts may be translated into machine-checkable forms. It introduces zero authority, zero execution, and no runtime enablement. It is strictly about derivation governance, not execution or consumption.

## Normative Authority Hierarchy
- Markdown governance artifacts are the sole source of truth (normative, authoritative).
- Any derived artifact is a non-authoritative mirror and subordinate to the Markdown originals.

## Permitted Derivations (Design-Only)
- Deterministic, read-only intermediate representations (IR) of Markdown governance.
- Structural constraint representations that mirror, but do not extend, Markdown intent.
- Validators whose only outputs are {COMPLIANT | NON-COMPLIANT}; no side effects.

## Forbidden Capabilities
- No execution hooks or runtime triggers.
- No authorization objects or grants.
- No mutation, learning, planning, scheduling, continuation, or persistence.
- No runtime consumption of governance artifacts; derived forms are not to be used by runtime systems.

## Derivation Rules
- Derivation must be deterministic and reproducible from Markdown sources.
- Derived artifacts must be generated, not hand-authored.
- Every derived artifact must bind to its Markdown source via cryptographic hash.
- Proof-of-equivalence between Markdown and derived form is required; absence is denial.

## Failure Semantics
- Any mismatch, ambiguity, missing hash binding, or absent proof-of-equivalence → DENY + AUDIT (design-only requirement).
- No reconciliation, override, or discretionary exceptions.

## Phase Boundary Statement
- Phase-3.1 does not unlock execution, agency, or autonomy.
- Phase-3.1 exists solely to prevent misinterpretation and governance drift when creating non-authoritative derivatives.

## Designation
This document is DESIGN_ONLY, NON-EXECUTABLE, NON-AUTHORIZING, and preserves deny-by-default. No machine-readable or runtime-facing artifacts are introduced by this phase.
