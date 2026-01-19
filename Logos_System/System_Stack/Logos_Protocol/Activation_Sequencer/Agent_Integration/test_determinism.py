# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: test_determinism
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
  source: System_Stack/Logos_Protocol/Activation_Sequencer/Agent_Integration/test_determinism.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

def test_router_determinism():
    import hashlib
    import pathlib
    import subprocess

    p = pathlib.Path("config/ontological_properties.json").read_bytes()
    h1 = hashlib.sha256(p).hexdigest()
    subprocess.run(["python", "tools/audit_and_emit.py", "--write"], check=True)
    h2 = hashlib.sha256(
        pathlib.Path("config/ontological_properties.json").read_bytes()
    ).hexdigest()
    assert h1 == h2
