# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-003
# module_name:          config_loader
# subsystem:            mutation_tooling
# module_role:          orchestration
# canonical_path:       WORKFLOW_MUTATION_TOOLING/controllers/config_loader.py
# responsibility:       Orchestration module: config loader
# runtime_stage:        orchestration
# execution_entry:      None
# allowed_targets:      []
# forbidden_targets:    ["SYSTEM", "WORKFLOW_NEXUS"]
# allowed_imports:      []
# forbidden_imports:    []
# spec_reference:       [SPEC-AP-V2.1]
# implementation_phase: PHASE_2
# authoring_authority:  ARCHON_PRIME
# version:              1.0
# status:               canonical
# ============================================================
from WORKFLOW_NEXUS.Governance.workflow_gate import enforce_runtime_gate

enforce_runtime_gate()

# ------------------------------------------------------------
# END ARCHON PRIME MODULE HEADER
# ------------------------------------------------------------

import json
import os


class ConfigLoader:

    def __init__(self, root_path):
        self.root = root_path

    def load_json(self, path):
        with open(os.path.join(self.root, path)) as f:
            return json.load(f)

    def load_crawl_config(self):
        return self.load_json("config/crawl_config.json")

    def load_repair_config(self):
        return self.load_json("config/repair_config.json")

    def load_simulation_config(self):
        return self.load_json("config/simulation_config.json")

    def load_module_registry(self):
        return self.load_json("registry/module_registry.json")

    def load_audit_registry(self):
        return self.load_json("registry/audit_registry.json")

    def load_repair_registry(self):
        return self.load_json("registry/repair_registry.json")

    def load_simulation_registry(self):
        return self.load_json("registry/simulation_registry.json")

    def load_all(self):
        return {
            "crawl_config": self.load_crawl_config(),
            "repair_config": self.load_repair_config(),
            "simulation_config": self.load_simulation_config(),
            "module_registry": self.load_module_registry(),
            "audit_registry": self.load_audit_registry(),
            "repair_registry": self.load_repair_registry(),
            "simulation_registry": self.load_simulation_registry(),
        }
