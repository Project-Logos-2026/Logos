# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: skill_acquisition
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
  source: System_Stack/Logos_Agents/Logos_Agent/code_generator/skill_acquisition.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from core.logos_validator_hub import validator_gate
from core.async_workers import submit_async
from core.config_loader import Config

class SkillAcquisition:
    """
    Extracts procedures from data logs and creates callable tools.
    """
    def __init__(self):
        self.config = Config()
        self.tools = {}

    @validator_gate
    def acquire(self, logs: list, async_mode: bool = False):
        """
        Acquire new skills from logs.
        async_mode: schedule in background.
        """
        if async_mode:
            submit_async(self._acquire_impl, logs)
            return True
        return self._acquire_impl(logs)

    def _acquire_impl(self, logs: list):
        for entry in logs:
            if isinstance(entry, str) and entry.startswith('action:'):
                parts = entry.split(':', 1)[1].split(',')
                name = parts[0].strip()
                params = [p.strip() for p in parts[1:]]
                self.tools[name] = {'params': params}
        return self.tools
