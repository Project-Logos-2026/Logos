"""
Radial_Genesis_Engine - Composite_Aggregator Registration Diff
This is NOT a replacement for Composite_Aggregator.py.
This is a diff showing the exact registration sequence to add
triune + recursion coupling scoring modules.

Apply to the initialization site where CompositeAggregator is
constructed and modules are registered.

Composite_Aggregator.py itself requires NO modifications.
Genesis_Selector requires NO modifications.
Hysteresis_Governor requires NO modifications.
Mode_Controller requires NO modifications.
Override channel requires NO modifications.
Runtime_Spine requires NO modifications.

Registration order per spec:
    1. StabilityMetric          (geometric, Phase 6)
    2. TriuneFitScore           (triadic fit)
    3. CommutationBalanceScore   (MESH residuals)
    4. DivergenceMetric          (stability telemetry)
    5. RecursionCouplingCoherenceScore (recursion layer coupling)

CompositeAggregator evaluates in sorted-by-name order regardless of
registration order. Registration order affects only the construction
sequence, not evaluation determinism.

Post-registration evaluation order (sorted by name):
    1. commutation_balance
    2. divergence_metric
    3. recursion_coupling_coherence
    4. stability_metric
    5. triune_fit_score

No execution authority. No identity mutation. No spine mutation.
"""

# === DIFF START — Add to RGE initialization / bootstrap ===

# --- Existing (unchanged) ---
# from ...Evaluation.Stability_Metric import StabilityMetric
# from ...Evaluation.Composite_Aggregator import CompositeAggregator

# --- New imports ---
# from ...Evaluation.Triune_Fit_Score import TriuneFitScore
# from ...Evaluation.Commutation_Balance_Score import CommutationBalanceScore
# from ...Evaluation.Divergence_Metric import DivergenceMetric
# from ...Evaluation.Recursion_Coupling_Coherence_Score import RecursionCouplingCoherenceScore

# --- Existing construction (unchanged) ---
# aggregator = CompositeAggregator()
# aggregator.register(StabilityMetric())

# --- New registrations (append after existing) ---
# aggregator.register(TriuneFitScore(capability_table=loaded_table))
# aggregator.register(CommutationBalanceScore(gamma=1.0))
# aggregator.register(DivergenceMetric(mu=1.0))
# aggregator.register(RecursionCouplingCoherenceScore(enable_instrumentation=False))

# --- Per-tick telemetry injection (in evaluation loop) ---
# fit_score.inject_from_telemetry(snapshot)
# comm_score.inject_from_telemetry(snapshot)
# div_metric.inject_from_telemetry(snapshot)
# rccs.inject_from_telemetry(snapshot)

# === DIFF END ===
