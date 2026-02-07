# Meaning and Translation Protocol (MTP) — Manifest

## Scope
MTP is the authoritative SMP entry-point for non-canonical meaning within the
execution core. It constructs SMPs during the allowed mutation window and
provides enrichment surfaces only.

## Authority Boundaries
- Authorized to build and seal SMPs during the construction window only.
- Not authorized to promote SMPs or mutate SMPs after sealing.
- Not authorized to persist canonical memory or issue Append Artifacts (AA).

## Core Responsibilities
- Receive pre-gated raw input from I2.
- Construct SMP metadata header and preserve raw input.
- Perform tri-modal enrichment:
  - Natural Language
  - Symbolic Mathematics
  - Formal Logic (PXL surface)
- Aggregate enrichment outputs into SMP layers.
- Enforce SMP schema and seal immutability.
- Return SMP to I2 for routing and downstream preparation.

## Governance Constraints
- Fail-closed if schema enforcement fails.
- No proof, validation, or admissibility checks.
- No runtime execution claims beyond enrichment.

## Explicit Non-Responsibilities
- No proof validation or formal admissibility.
- No canonical promotion or truth assertion.
- No AA creation or persistence decisions.
- No mutation after immutability seal.
