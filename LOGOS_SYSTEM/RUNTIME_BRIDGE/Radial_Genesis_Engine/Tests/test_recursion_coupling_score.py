"""
Deterministic scoring test for RecursionCouplingCoherenceScore.

Validates:
    - Identical deltas produce score 0
    - Zero strain produces score 0
    - Extreme divergence produces score < 1
    - Instrumented vs non-instrumented produce identical scores
    - Contribution sum equals total coupling penalty
    - All floats in report are finite
    - Pair ordering is deterministic

No execution authority. No identity mutation. No spine mutation.
"""

import math
import unittest

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Core.Telemetry_Snapshot import (
    RecursionLayerTelemetry,
    CANONICAL_RECURSION_LAYERS,
    _all_unordered_pairs,
    _generate_pair_key,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Evaluation.Recursion_Coupling_Coherence_Score import (
    RecursionCouplingCoherenceScore,
)


def _build_telemetry(
    deltas=None,
    residuals=None,
    stability=None,
    dim=3,
    layers=None,
):
    """Helper to build RecursionLayerTelemetry with defaults."""
    layers = layers or CANONICAL_RECURSION_LAYERS
    pairs = _all_unordered_pairs(layers)
    if deltas is None:
        deltas = {l: tuple([0.0] * dim) for l in layers}
    if residuals is None:
        residuals = {l: 0.5 for l in layers}
    if stability is None:
        stability = {l: 0.5 for l in layers}
    return RecursionLayerTelemetry(
        recursion_layers=layers,
        layer_shared_delta=deltas,
        layer_residual=residuals,
        layer_stability=stability,
        layer_throughput={l: 1.0 for l in layers},
        coupling_weights={p: 1.0 / len(pairs) for p in pairs},
    )


def _make_scorer(enable_instr=False):
    return RecursionCouplingCoherenceScore(
        module_weight=1.0,
        enable_instrumentation=enable_instr,
    )


def _dummy_snapshot():
    return {
        "config_id": "test",
        "rotation_index": 0,
        "agent_assignments": {"axis_0": "SCP", "axis_1": "MTP", "axis_2": "ARP", "axis_3": "LOGOS"},
        "assignment_string": "ARP-LOGOS-MTP-SCP",
    }


class TestIdenticalDeltasProduceZero(unittest.TestCase):
    def test_identical_deltas(self):
        rt = _build_telemetry(
            deltas={l: (0.5, 0.5, 0.5) for l in CANONICAL_RECURSION_LAYERS},
        )
        scorer = _make_scorer()
        scorer.inject_recursion_telemetry(rt)
        score = scorer.compute_score(_dummy_snapshot())
        self.assertAlmostEqual(score, 0.0, places=10)


class TestZeroStrainProducesZero(unittest.TestCase):
    def test_zero_strain(self):
        rt = _build_telemetry(
            deltas={l: (0.5 if i % 2 == 0 else -0.5, 0.0, 0.0)
                    for i, l in enumerate(CANONICAL_RECURSION_LAYERS)},
            residuals={l: 0.0 for l in CANONICAL_RECURSION_LAYERS},
            stability={l: 0.0 for l in CANONICAL_RECURSION_LAYERS},
        )
        scorer = _make_scorer()
        scorer.inject_recursion_telemetry(rt)
        score = scorer.compute_score(_dummy_snapshot())
        self.assertEqual(score, 0.0)


class TestExtremeDivergenceBelowOne(unittest.TestCase):
    def test_extreme_divergence(self):
        layers = CANONICAL_RECURSION_LAYERS
        deltas = {}
        for i, l in enumerate(layers):
            deltas[l] = (1.0, 1.0, 1.0) if i == 0 else (-1.0, -1.0, -1.0)
        rt = _build_telemetry(
            deltas=deltas,
            residuals={l: 1000.0 for l in layers},
            stability={l: 1000.0 for l in layers},
        )
        scorer = _make_scorer()
        scorer.inject_recursion_telemetry(rt)
        score = scorer.compute_score(_dummy_snapshot())
        self.assertGreater(score, 0.0)
        self.assertLess(score, 1.0)


class TestInstrumentedVsNonInstrumentedIdentical(unittest.TestCase):
    def test_score_identity(self):
        deltas = {}
        for i, l in enumerate(CANONICAL_RECURSION_LAYERS):
            deltas[l] = tuple(
                math.sin(i * 1.5 + d * 0.7) * 0.8 for d in range(4)
            )
        rt = _build_telemetry(deltas=deltas, dim=4)

        scorer_off = _make_scorer(enable_instr=False)
        scorer_off.inject_recursion_telemetry(rt)
        score_off = scorer_off.compute_score(_dummy_snapshot())

        scorer_on = _make_scorer(enable_instr=True)
        scorer_on.inject_recursion_telemetry(rt)
        score_on = scorer_on.compute_score(_dummy_snapshot())

        self.assertEqual(score_off, score_on)


class TestContributionSumEqualsTotal(unittest.TestCase):
    def test_contribution_sum(self):
        deltas = {}
        for i, l in enumerate(CANONICAL_RECURSION_LAYERS):
            deltas[l] = tuple(
                math.sin(i * 1.5 + d * 0.7) * 0.8 for d in range(4)
            )
        rt = _build_telemetry(deltas=deltas, dim=4)
        scorer = _make_scorer(enable_instr=True)
        scorer.inject_recursion_telemetry(rt)
        score = scorer.compute_score(_dummy_snapshot())
        report = scorer.get_last_instrumentation_report()
        self.assertIsNotNone(report)
        contrib_sum = sum(p["contribution"] for p in report["pairs"])
        self.assertAlmostEqual(contrib_sum, report["total_coupling_penalty"], places=14)
        self.assertAlmostEqual(contrib_sum, score, places=14)


class TestAllFloatsFinite(unittest.TestCase):
    def test_finite_values(self):
        deltas = {}
        for i, l in enumerate(CANONICAL_RECURSION_LAYERS):
            deltas[l] = tuple(
                math.sin(i * 1.5 + d * 0.7) * 0.8 for d in range(4)
            )
        rt = _build_telemetry(deltas=deltas, dim=4)
        scorer = _make_scorer(enable_instr=True)
        scorer.inject_recursion_telemetry(rt)
        scorer.compute_score(_dummy_snapshot())
        report = scorer.get_last_instrumentation_report()
        self.assertIsNotNone(report)
        for pair_detail in report["pairs"]:
            for key in ["residual_raw", "residual_normalized", "g_i", "g_j", "weight", "contribution"]:
                self.assertTrue(math.isfinite(pair_detail[key]), f"{key} not finite")
        for layer, val in report["strain_gates"].items():
            self.assertTrue(math.isfinite(val), f"strain_gate[{layer}] not finite")
        self.assertTrue(math.isfinite(report["total_coupling_penalty"]))


class TestDeterministicPairOrdering(unittest.TestCase):
    def test_pair_order(self):
        deltas = {}
        for i, l in enumerate(CANONICAL_RECURSION_LAYERS):
            deltas[l] = tuple(
                math.sin(i * 1.5 + d * 0.7) * 0.8 for d in range(4)
            )
        rt = _build_telemetry(deltas=deltas, dim=4)
        scorer = _make_scorer(enable_instr=True)
        scorer.inject_recursion_telemetry(rt)
        scorer.compute_score(_dummy_snapshot())
        report = scorer.get_last_instrumentation_report()
        self.assertIsNotNone(report)
        pair_keys = [p["pair"] for p in report["pairs"]]
        layers = CANONICAL_RECURSION_LAYERS
        expected = []
        for i in range(len(layers)):
            for j in range(i + 1, len(layers)):
                expected.append(_generate_pair_key(layers[i], layers[j]))
        self.assertEqual(pair_keys, expected)


class TestNoTelemetryReturnsZero(unittest.TestCase):
    def test_no_telemetry(self):
        scorer = _make_scorer()
        score = scorer.compute_score(_dummy_snapshot())
        self.assertEqual(score, 0.0)


class TestInstrumentationDisabledReturnsNone(unittest.TestCase):
    def test_disabled_report(self):
        scorer = _make_scorer(enable_instr=False)
        report = scorer.get_last_instrumentation_report()
        self.assertIsNone(report)


class TestReportSchemaShape(unittest.TestCase):
    def test_schema(self):
        rt = _build_telemetry()
        scorer = _make_scorer(enable_instr=True)
        scorer.inject_recursion_telemetry(rt)
        scorer.compute_score(_dummy_snapshot())
        report = scorer.get_last_instrumentation_report()
        self.assertIsNotNone(report)
        required_keys = {"delta_dimensionality", "pair_count", "layers", "strain_gates", "pairs", "total_coupling_penalty"}
        self.assertEqual(set(report.keys()), required_keys)
        pair_keys = {"pair", "residual_raw", "residual_normalized", "g_i", "g_j", "weight", "contribution"}
        for pd in report["pairs"]:
            self.assertEqual(set(pd.keys()), pair_keys)


if __name__ == "__main__":
    unittest.main()
