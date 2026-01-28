# Recursion Governance Contract (RGC)

This contract defines the ONLY permitted conditions under which
recursive self-evaluation or multi-tick execution may occur.

It has two inseparable faces:

1. Formal Proof Index (Coq / PXL Gate)
2. Runtime Enforcement (Python / Governance)

These faces are cross-hash-locked.
If either changes, recursion MUST be denied.

This contract does NOT grant autonomy.
It defines the final recursion boundary.

Timestamp: 2026-01-25T05:59:17.023867+00:00