# Proof Projection & Attestation Layer (Design-Only)

## Purpose
Specify the design for projecting Coq proofs into ARP outputs
under Runtime_Control enforcement, without executing proofs.

## Flow (Conceptual)
Coq Proof Artifact
  → Proof ID + Hash
  → Attestation Record
  → ARP Application Function
  → Runtime_Control Enforcement
  → Labeled Output (or Downgrade/DENY)

## Components

### 1. Proof Artifacts (Coq)
- Immutable .v files
- Compiled externally
- Identified by (proof_id, hash)

### 2. Attestation Record
Fields:
- proof_id
- artifact_hash
- scope (AF name)
- timestamp
- signer (future TLM binding)

### 3. ARP Consumption Rules
- AFs may accept proof_refs as opaque tokens only
- No AF may interpret proof contents
- Proof presence may only remove downgrades, never grant authority

### 4. Runtime_Control Enforcement
- Validate proof_ref format
- Match AF scope
- On failure → DENY + audit
- On absence → heuristic_only downgrade

## Epistemic Rules
- Proof-backed results may upgrade labels
- Aggregation still enforces weakest-epistemic dominance
- No proof may enable autonomy or execution

## Failure Modes
- Missing proof → downgrade
- Invalid hash → DENY
- Scope mismatch → DENY
- Replay or reuse outside scope → DENY

## Non-Goals
- No proof execution
- No Coq tooling invocation
- No runtime activation

## Status
Design-only specification complete.
Implementation NOT authorized.
