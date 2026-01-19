# LOGOS Lock-and-Key Mechanism

## Purpose

The LOGOS lock-and-key mechanism enforces **non-bypassable system admission**
prior to runtime activation.

No LOGOS services may start unless the system has:

1. Proven epistemic legitimacy (LEM admission)
2. Proven proof identity and integrity (dual-proof commutation)
3. Produced a cryptographic unlock hash
4. Issued agent identities from that unlock
5. Recorded the activation in an append-only audit log

---

## Authority Separation (Canonical)

### Orchestration (Exclusive Authority)
**Location**


**Responsibilities**
- Preflight identity guard (PXL ↔ runtime mirror)
- LEM admission (PXL proof rebuild / discharge)
- Dual-proof compilation and hash commutation
- Unlock hash derivation
- Agent ID derivation (I1 / I2 / I3)
- Audit log append

**Canonical entrypoint**


---

### Proof Artifacts (Ephemeral Inputs)

**Location**


- Proof logs are write-over
- Attestation is read-only
- Agents never import proof logs

---

### Audit Logs (Authoritative History)

**Location**


- Append-only
- Each entry corresponds to one activation attempt
- Unlock hash doubles as Session ID

---

## Runtime Consumption

`START_LOGOS.py` is a **pure consumer**.

It:
- Requires the attestation to exist
- Validates its contents:
  - `commute == true`
  - valid `unlock_hash`
  - agent IDs `I1`, `I2`, `I3`
- Fails closed on any violation

It **never**:
- runs proofs
- performs LEM discharge
- rewrites audit state

---

## Invariants (Must Never Be Violated)

- PXL Gate and runtime compiler mirror must remain identical
- No proof logic may execute at runtime
- No fallback paths are permitted
- No agent may start without a valid attestation

---

## Summary

LOGOS cannot:
- reason classically without justification
- activate without proof identity
- act without cryptographic authorization

This mechanism is **final and authoritative**.
