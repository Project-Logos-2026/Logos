"""
Telemetry validation test for RecursionLayerTelemetry.

Validates:
    - Key mismatch rejected
    - Dimensional mismatch rejected
    - Non-finite values rejected
    - Coupling weights not summing to 1 rejected
    - Negative weights rejected
    - Values outside [-1, 1] rejected for shared deltas
    - Negative layer magnitudes rejected
    - Fewer than 2 layers rejected
    - Zero-dimensional vectors rejected

Fail-fast behavior enforced at construction time.

No execution authority. No identity mutation. No spine mutation.
"""

import math
import unittest

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Core.Telemetry_Snapshot import (
    RecursionLayerTelemetry,
    CANONICAL_RECURSION_LAYERS,
    _all_unordered_pairs,
)


_LAYERS = CANONICAL_RECURSION_LAYERS
_PAIRS = _all_unordered_pairs(_LAYERS)
_DIM = 3


def _valid_kwargs():
    """Return a valid construction kwargs dict."""
    return {
        "recursion_layers": _LAYERS,
        "layer_shared_delta": {l: tuple([0.0] * _DIM) for l in _LAYERS},
        "layer_residual": {l: 0.5 for l in _LAYERS},
        "layer_stability": {l: 0.5 for l in _LAYERS},
        "layer_throughput": {l: 1.0 for l in _LAYERS},
        "coupling_weights": {p: 1.0 / len(_PAIRS) for p in _PAIRS},
    }


class TestValidConstruction(unittest.TestCase):
    def test_valid(self):
        rt = RecursionLayerTelemetry(**_valid_kwargs())
        self.assertEqual(rt.delta_dimensionality, _DIM)
        self.assertEqual(rt.pair_count, len(_PAIRS))


class TestKeyMismatchRejected(unittest.TestCase):
    def test_missing_delta_key(self):
        kwargs = _valid_kwargs()
        del kwargs["layer_shared_delta"][_LAYERS[0]]
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)

    def test_extra_delta_key(self):
        kwargs = _valid_kwargs()
        kwargs["layer_shared_delta"]["FAKE_LAYER"] = tuple([0.0] * _DIM)
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)

    def test_missing_residual_key(self):
        kwargs = _valid_kwargs()
        del kwargs["layer_residual"][_LAYERS[0]]
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)

    def test_missing_stability_key(self):
        kwargs = _valid_kwargs()
        del kwargs["layer_stability"][_LAYERS[0]]
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)

    def test_missing_throughput_key(self):
        kwargs = _valid_kwargs()
        del kwargs["layer_throughput"][_LAYERS[0]]
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)

    def test_missing_coupling_pair(self):
        kwargs = _valid_kwargs()
        first_pair = _PAIRS[0]
        del kwargs["coupling_weights"][first_pair]
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)

    def test_extra_coupling_pair(self):
        kwargs = _valid_kwargs()
        kwargs["coupling_weights"]["FAKE_A|FAKE_B"] = 0.0
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)


class TestDimensionalMismatchRejected(unittest.TestCase):
    def test_inconsistent_dim(self):
        kwargs = _valid_kwargs()
        first = _LAYERS[0]
        kwargs["layer_shared_delta"][first] = tuple([0.0] * (_DIM + 1))
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)

    def test_zero_dim(self):
        kwargs = _valid_kwargs()
        for l in _LAYERS:
            kwargs["layer_shared_delta"][l] = ()
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)


class TestNonFiniteValuesRejected(unittest.TestCase):
    def test_nan_in_delta(self):
        kwargs = _valid_kwargs()
        kwargs["layer_shared_delta"][_LAYERS[0]] = (float("nan"), 0.0, 0.0)
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)

    def test_inf_in_delta(self):
        kwargs = _valid_kwargs()
        kwargs["layer_shared_delta"][_LAYERS[0]] = (float("inf"), 0.0, 0.0)
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)

    def test_nan_residual(self):
        kwargs = _valid_kwargs()
        kwargs["layer_residual"][_LAYERS[0]] = float("nan")
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)

    def test_inf_stability(self):
        kwargs = _valid_kwargs()
        kwargs["layer_stability"][_LAYERS[0]] = float("inf")
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)

    def test_nan_coupling_weight(self):
        kwargs = _valid_kwargs()
        kwargs["coupling_weights"][_PAIRS[0]] = float("nan")
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)


class TestCouplingWeightSumRejected(unittest.TestCase):
    def test_sum_not_one(self):
        kwargs = _valid_kwargs()
        for p in _PAIRS:
            kwargs["coupling_weights"][p] = 0.5
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)


class TestNegativeWeightsRejected(unittest.TestCase):
    def test_negative_coupling_weight(self):
        kwargs = _valid_kwargs()
        kwargs["coupling_weights"][_PAIRS[0]] = -0.1
        remaining = _PAIRS[1:]
        redistribute = (1.0 + 0.1) / len(remaining)
        for p in remaining:
            kwargs["coupling_weights"][p] = redistribute
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)


class TestDeltaOutOfBoundsRejected(unittest.TestCase):
    def test_above_one(self):
        kwargs = _valid_kwargs()
        kwargs["layer_shared_delta"][_LAYERS[0]] = (1.5, 0.0, 0.0)
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)

    def test_below_neg_one(self):
        kwargs = _valid_kwargs()
        kwargs["layer_shared_delta"][_LAYERS[0]] = (-1.5, 0.0, 0.0)
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)


class TestNegativeLayerMagnitudesRejected(unittest.TestCase):
    def test_negative_residual(self):
        kwargs = _valid_kwargs()
        kwargs["layer_residual"][_LAYERS[0]] = -0.1
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)

    def test_negative_stability(self):
        kwargs = _valid_kwargs()
        kwargs["layer_stability"][_LAYERS[0]] = -0.1
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)

    def test_negative_throughput(self):
        kwargs = _valid_kwargs()
        kwargs["layer_throughput"][_LAYERS[0]] = -0.1
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)


class TestFewerThanTwoLayersRejected(unittest.TestCase):
    def test_single_layer(self):
        single = (_LAYERS[0],)
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(
                recursion_layers=single,
                layer_shared_delta={single[0]: (0.0, 0.0, 0.0)},
                layer_residual={single[0]: 0.5},
                layer_stability={single[0]: 0.5},
                layer_throughput={single[0]: 1.0},
                coupling_weights={},
            )


class TestNotTupleRejected(unittest.TestCase):
    def test_list_instead_of_tuple(self):
        kwargs = _valid_kwargs()
        kwargs["layer_shared_delta"][_LAYERS[0]] = [0.0, 0.0, 0.0]
        with self.assertRaises(ValueError):
            RecursionLayerTelemetry(**kwargs)


if __name__ == "__main__":
    unittest.main()
