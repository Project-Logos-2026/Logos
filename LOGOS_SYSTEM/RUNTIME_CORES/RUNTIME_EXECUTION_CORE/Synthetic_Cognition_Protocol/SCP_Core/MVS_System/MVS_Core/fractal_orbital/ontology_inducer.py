# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: ontology_inducer
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
  source: System_Stack/Synthetic_Cognition_Protocol/MVS_System/mvs_calculators/ontology_inducer.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from LOGOS_SYSTEM.System_Stack.Synthetic_Cognition_Protocol.logos_validator_hub import validator_gate
from LOGOS_SYSTEM.System_Stack.Synthetic_Cognition_Protocol.async_workers import submit_async
from LOGOS_SYSTEM.System_Stack.Synthetic_Cognition_Protocol.config_loader import Config

class OntologyInducer:
    """
    Infers schema (types, relations, constraints) from raw inputs.
    """
    def __init__(self):
        self.config = Config()
        self.ontology = {}

    @validator_gate
    def induce(self, data: list, async_mode: bool = False):
        """
        Induce ontology from list of samples (dicts).
        async_mode: schedule in background.
        """
        if async_mode:
            submit_async(self._induce_impl, data)
            return True
        return self._induce_impl(data)

    def _induce_impl(self, data: list):
        ontology = {}
        for sample in data:
            for k, v in sample.items():
                ontology.setdefault(k, set()).add(type(v).__name__)
        self.ontology = {k: list(v) for k, v in ontology.items()}
        return self.ontology
