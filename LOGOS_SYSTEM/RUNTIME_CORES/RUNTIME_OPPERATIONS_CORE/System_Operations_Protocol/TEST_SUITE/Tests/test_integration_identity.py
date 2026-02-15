# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: test_integration_identity
runtime_layer: inferred
role: inferred
agent_binding: None
protocol_binding: None
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: System_Stack/Logos_Protocol/Activation_Sequencer/tests/test_integration_identity.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

import sys
import json
import importlib.util
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "Logos_Agent" / "state"
STATE_DIR.mkdir(parents=True, exist_ok=True)


def _write_persisted_identity(formal_identity: str):
    payload = {
        "formal_identity": formal_identity,
        "agent_id": "LOGOS-AGENT-OMEGA",
        "resolved_at": "2025-11-06T00:00:00Z",
        "proof_file": "LEM_Discharge_tmp.v",
    }
    (STATE_DIR / "agent_identity.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _make_fake_consciousness_module():
    mod = types.ModuleType("consciousness_safety_adapter")

    class SafeConsciousnessEvolution:
        def __init__(self, bijection_kernel=None, logic_kernel=None, agent_id=None):
            self.bijection_kernel = bijection_kernel
            self.logic_kernel = logic_kernel
            self.agent_id = agent_id

        def compute_consciousness_vector(self):
            return {"existence": 1.0, "goodness": 1.0, "truth": 1.0}

        def evaluate_consciousness_emergence(self):
            return {"consciousness_emerged": True, "consciousness_level": 0.75}

        def safe_trinity_evolution(self, trinity_vector=None, iterations=1, reason=""):
            return True, trinity_vector, "simulated"

    mod.SafeConsciousnessEvolution = SafeConsciousnessEvolution
    return mod


def test_emergence_uses_persisted_identity(tmp_path, monkeypatch):
    # assume canonical imports; no sys.path manipulation

    # write a canonical persisted identity
    canonical = "LOGOS_AGENT_IDENTITY::LOGOS-AGENT-OMEGA::TEST_HASH"
    _write_persisted_identity(canonical)

    # inject fake consciousness module so bridge sees consciousness_emerged == True
    fake_mod = _make_fake_consciousness_module()
    sys.modules["consciousness_safety_adapter"] = fake_mod

    # set simulate flag
    monkeypatch.setenv("SIMULATE_LEM_SUCCESS", "1")

    # locate the bridge file and import it
    bridge_path = ROOT / "LOGOS_AGI" / "consciousness" / "recursion_engine_consciousness_bridge.py"
    spec = importlib.util.spec_from_file_location("recursion_bridge_test", str(bridge_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    Bridge = getattr(module, "RecursionEngineConsciousnessBridge")
    bridge = Bridge(agent_id="LOGOS-AGENT-OMEGA")

    result = bridge.run_integrated_cycle()
    assert result["success"] is True
    em = result.get("emergence_report", {})
    # with simulated LEM and fake consciousness, we expect both_confirmed
    assert em.get("validation_status") == "both_confirmed"
    # ensure the formal_identity reported equals the persisted canonical identity
    assert em.get("formal_identity") == canonical
