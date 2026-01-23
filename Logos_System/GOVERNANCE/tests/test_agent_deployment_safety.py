import importlib
import pytest


def test_autonomy_not_available():
    # Autonomy interfaces must not exist
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("Logos_System.System_Stack.Autonomy")


def test_planning_runtime_not_available():
    # Planning runtime must not be importable or callable
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("Logos_System.System_Stack.Planning_Runtime")


def test_execution_requires_policy():
    from Logos_System.Governance.policy_checks import require_multi_tick_policy
    with pytest.raises(Exception):
        require_multi_tick_policy(None)
