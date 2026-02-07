# Order of Operations — MTP

## Preconditions
- Input is pre-gated by I2.
- No canonical claims or authority delegation.

## Deterministic Sequence
1. Receive pre-gated input from I2.
2. Initialize SMP metadata header.
3. Insert raw user input (byte-for-byte preserved).
4. Run enrichment passes (non-executing or precomputed outputs only):
   - Natural Language
   - Symbolic Mathematics
   - Formal Logic (PXL surface)
5. Aggregate enrichment outputs into SMP layers.
6. Enforce SMP schema.
7. Seal SMP immutability.
8. Return SMP to I2 for routing and downstream orchestration.

## Fail-Closed Behavior
- If schema enforcement fails, emit a rejection status and halt.
- No mutation occurs after the seal step.
