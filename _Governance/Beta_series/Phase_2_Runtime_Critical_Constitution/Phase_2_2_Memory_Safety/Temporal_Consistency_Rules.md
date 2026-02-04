# Phase-2.2 Temporal Consistency Rules (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)

## Temporal Constraints on Reads
- Reads must respect SMP temporal_context fields (observation time, valid_from/valid_until); requests outside declared windows are denied.
- No cross-tick synthesis, forecasting, or inference across temporal boundaries.
- No historical stitching or time-based aggregation of SMPs.

## Prohibitions
- No prediction, extrapolation, or trend analysis derived from SMP temporal_context.
- No carryover of authority or visibility between time windows without explicit governed approval.
- No time-based caching or memoization of read results.

## Fail-Closed Behavior
- Missing temporal_context: deny the read and log (design-only requirement).
- Ambiguous or conflicting temporal windows: deny and log.
- Attempts to perform temporal inference or aggregation: deny and log.

All rules are declarative; no runtime logic or scheduling is introduced.
