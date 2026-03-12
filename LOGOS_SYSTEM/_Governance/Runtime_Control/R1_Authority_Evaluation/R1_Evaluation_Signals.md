# R1 — Evaluation Signals (Observable-Only)

**Phase:** R1 (Design-Only)
**Authority Granted:** NONE
**External IO:** NONE
**Persistence:** NONE (beyond governed audit spine)

---

## Signal Classes (Read-Only)

- **Governance State:** Frozen records from prior phases (O, P₁, A₁–A₅) and R0
  tick envelopes; read-only, immutable during evaluation.
- **Privation & Revocation Status:** Confirmation that privation remains dominant
  and revocation paths are intact; no mutation permitted.
- **Runtime Health & Halt Path:** Proof that deterministic halt is available; any
  ambiguity forces denial.
- **Budget Status:** Remaining tick and evaluation budget; cannot be extended.
- **Audit Channel Reachability:** Confirmation of writable path within the governed
  spine; no alternative sinks.

## Forbidden Signals

- External IO channels, side-band telemetry, or ungoverned persistence endpoints.
- Signals requiring authority to read (none exist at R1).
- Any signal that implies or enables delegation, scheduling, or continuation.

## Signal Handling Rules

- Signals are snapshot-read; no streaming that could mask changes.
- If provenance is uncertain, the evaluation halts and denies.
- No caching across ticks; each evaluation re-acquires signals.

## Outcome Encoding

- `eligible_for_granting` — Preconditions satisfied; still NO authority granted.
- `not_eligible` — Preconditions unsatisfied; halt and record reasons.

All outcomes are written to the audit spine with full signal provenance.
