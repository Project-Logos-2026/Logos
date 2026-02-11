"""
Minimal deterministic verification for RGE override and mode gating.
References: GENESIS_SELECTOR_STATE_MACHINE.md, MODE_CONTROLLER_INTERFACE_SPEC.md
"""

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Controller.RGE_Override_Channel import (
    RGEOverrideChannel,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Controller.Genesis_Selector import (
    GenesisSelector,
)
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Core.Topology_State import (
    AGENTS,
    AXES,
    TopologyState,
)


class _ModeGateStub:
    def __init__(self, allowed: bool) -> None:
        self.allowed = allowed

    def is_activation_allowed(self) -> bool:
        return self.allowed


def _default_assignments() -> dict[str, str]:
    return dict(zip(AGENTS, AXES))


def test_override_yields_immediately() -> None:
    override = RGEOverrideChannel()
    selector = GenesisSelector(override_channel=override)

    override.register_override()

    assert selector.select_best() is None


def test_hard_override_clears_retained_state() -> None:
    override = RGEOverrideChannel()
    selector = GenesisSelector(override_channel=override)
    selector._retained_state["marker"] = "active"
    selector._infeasible_config_ids.add("config-1")

    override.register_hard_override()

    assert selector.select_best() is None
    assert selector._retained_state == {}
    assert selector._infeasible_config_ids == set()


def test_mode_gating_blocks_activation() -> None:
    selector = GenesisSelector(mode_controller=_ModeGateStub(allowed=False))

    assert selector.select_best() is None


def test_static_configuration_no_rotation(monkeypatch) -> None:
    config = TopologyState(rotation_index=0, agent_assignments=_default_assignments())

    monkeypatch.setattr(
        TopologyState,
        "enumerate_all_configurations",
        staticmethod(lambda: [config]),
    )

    selector = GenesisSelector()
    selector.select_best()

    assert config.rotation_index == 0


def test_override_lift_requires_mode_activation() -> None:
    override = RGEOverrideChannel()
    mode_controller = _ModeGateStub(allowed=False)
    selector = GenesisSelector(
        mode_controller=mode_controller,
        override_channel=override,
    )

    override.register_override()
    assert selector.select_best() is None

    override.clear_override()
    assert selector.select_best() is None

    mode_controller.allowed = True
    assert selector.select_best() is not None
