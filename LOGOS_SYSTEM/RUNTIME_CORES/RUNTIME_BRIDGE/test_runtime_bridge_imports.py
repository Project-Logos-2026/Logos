"""Verify that RUNTIME_BRIDGE modules are importable as a package."""

import importlib


def test_dual_bijective_commutation_validator_importable():
    mod = importlib.import_module(
        "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_BRIDGE.dual_bijective_commutation_validator"
    )
    assert hasattr(mod, "DualBijectiveCommutationValidator")


def test_execution_to_operations_exchanger_importable():
    mod = importlib.import_module(
        "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_BRIDGE.execution_to_operations_exchanger"
    )
    assert hasattr(mod, "ExecutionToOperationsExchanger")
    assert hasattr(mod, "PXLGate")
    assert hasattr(mod, "OperationRequest")
    assert hasattr(mod, "OperationResponse")
