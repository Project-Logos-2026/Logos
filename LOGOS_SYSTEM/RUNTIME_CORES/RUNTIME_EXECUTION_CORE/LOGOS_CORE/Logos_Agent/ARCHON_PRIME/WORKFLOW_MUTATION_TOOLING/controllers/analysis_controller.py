# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-001
# module_name:          analysis_controller
# subsystem:            mutation_tooling
# module_role:          orchestration
# canonical_path:       WORKFLOW_MUTATION_TOOLING/controllers/analysis_controller.py
# responsibility:       Orchestration module: analysis controller
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

"""
ARCHON PRIME — Analysis Controller
Stage 2: Analysis Tools Integration

Responsibilities:
  - Load module registry (analysis category only)
  - Dynamically import analysis modules
  - Execute structural analysis tools
  - Route artifact outputs to AP_SYSTEM_AUDIT/
  - Provide repository topology to downstream systems
  - Respect dry_run mode from crawl_config
"""

import importlib
import json
import os
import sys
import traceback

from controllers.config_loader import ConfigLoader

ARTIFACT_OUTPUT_DIR = "AP_SYSTEM_AUDIT"
IMPORT_ERROR_ARTIFACT = "AP_SYSTEM_AUDIT/ANALYSIS_IMPORT_ERRORS.json"


class AnalysisController:

    def __init__(self, root_path: str):
        self.root = root_path
        self.config_loader = ConfigLoader(root_path)
        self.registry = []
        self.crawl_config = {}
        self.simulation_config = {}
        self.import_errors = []

    # ------------------------------------------------------------------
    # Registry and configuration loading
    # ------------------------------------------------------------------

    def load_registry(self):
        """Load analysis modules from module_registry.json."""
        module_registry = self.config_loader.load_module_registry()
        all_modules = module_registry.get("modules", [])
        self.registry = [m for m in all_modules if m.get("category") == "analysis"]
        return self.registry

    def load_configs(self):
        """Load crawl and simulation configs. Respects dry_run mode."""
        self.crawl_config = self.config_loader.load_crawl_config()
        self.simulation_config = self.config_loader.load_simulation_config()
        return {
            "crawl_config": self.crawl_config,
            "simulation_config": self.simulation_config,
        }

    @property
    def dry_run(self) -> bool:
        return self.crawl_config.get("crawl_mode") == "dry_run"

    # ------------------------------------------------------------------
    # Module import validation
    # ------------------------------------------------------------------

    def _ensure_root_on_path(self):
        """Add repo root to sys.path so tool packages are importable."""
        if self.root not in sys.path:
            sys.path.insert(0, self.root)

    def validate_imports(self):
        """
        Attempt to import every registered analysis module.
        Failures are collected and written to ANALYSIS_IMPORT_ERRORS.json.
        Does not raise on failure.
        """
        self._ensure_root_on_path()
        self.import_errors = []

        for entry in self.registry:
            module_path = entry.get("module", "")
            try:
                importlib.import_module(module_path)
            except Exception:
                error_record = {
                    "module": module_path,
                    "name": entry.get("name"),
                    "error": traceback.format_exc().strip(),
                }
                self.import_errors.append(error_record)

        # Write error artifact regardless of count
        error_artifact_path = os.path.join(self.root, IMPORT_ERROR_ARTIFACT)
        os.makedirs(os.path.dirname(error_artifact_path), exist_ok=True)
        with open(error_artifact_path, "w") as f:
            json.dump(
                {
                    "stage": "Analysis Tools Integration",
                    "import_errors": self.import_errors,
                    "total_errors": len(self.import_errors),
                },
                f,
                indent=2,
            )

        return self.import_errors

    # ------------------------------------------------------------------
    # Analysis execution
    # ------------------------------------------------------------------

    def run_analysis_module(self, module_entry: dict) -> dict:
        """
        Dynamically import and execute a single analysis module.
        Returns a result record with status and artifact path.
        Execution is skipped in dry_run mode (import validation still runs).
        """
        self._ensure_root_on_path()
        name = module_entry.get("name", "unknown")
        module_path = module_entry.get("module", "")
        entry_function = module_entry.get("entry_function", "auto_detect")
        artifact_output = module_entry.get("artifact_output", "")

        result = {
            "name": name,
            "module": module_path,
            "artifact_output": artifact_output,
            "status": None,
            "error": None,
        }

        if self.dry_run:
            result["status"] = "skipped_dry_run"
            return result

        try:
            mod = importlib.import_module(module_path)

            # Resolve entry function
            if entry_function == "auto_detect":
                for candidate in ("run", "scan", "build_graph", "scan_repo", "main"):
                    if hasattr(mod, candidate):
                        entry_function = candidate
                        break

            func = getattr(mod, entry_function, None)
            if func is None:
                result["status"] = "failed"
                result["error"] = (
                    f"Entry function '{entry_function}' not found in {module_path}"
                )
                return result

            # Route artifact output to AP_SYSTEM_AUDIT/ if the module
            # accepts a target/output argument; otherwise call with no args.
            try:
                func()
            except TypeError:
                func(self.root)

            self._route_artifact(module_entry)
            result["status"] = "success"

        except Exception:
            result["status"] = "failed"
            result["error"] = traceback.format_exc().strip()

        return result

    def _route_artifact(self, module_entry: dict):
        """
        Ensure artifact output is directed to AP_SYSTEM_AUDIT/.
        If the module wrote to an alternate path, log it.
        """
        artifact_output = module_entry.get("artifact_output", "")
        if not artifact_output:
            return

        full_path = os.path.join(self.root, artifact_output)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        if not os.path.exists(full_path):
            # Artifact not yet written by the module — log as pending
            routing_log = os.path.join(
                self.root, ARTIFACT_OUTPUT_DIR, "ARTIFACT_ROUTING_LOG.json"
            )
            self._append_routing_log(routing_log, module_entry)

    def _append_routing_log(self, log_path: str, module_entry: dict):
        existing = []
        if os.path.exists(log_path):
            with open(log_path) as f:
                existing = json.load(f)
        existing.append(
            {
                "name": module_entry.get("name"),
                "module": module_entry.get("module"),
                "artifact_output": module_entry.get("artifact_output"),
                "status": "artifact_expected_not_found",
            }
        )
        with open(log_path, "w") as f:
            json.dump(existing, f, indent=2)

    # ------------------------------------------------------------------
    # Batch execution
    # ------------------------------------------------------------------

    def run_all_analysis(self, target_repo: str = None) -> list:
        """
        Execute all registered analysis modules in sequence.
        Returns list of result records.
        """
        if target_repo is None:
            target_repo = self.root

        self.load_configs()
        self.load_registry()
        self.validate_imports()

        results = []
        for module_entry in self.registry:
            result = self.run_analysis_module(module_entry)
            results.append(result)

        return results

    # ------------------------------------------------------------------
    # Topology accessor for downstream systems
    # ------------------------------------------------------------------

    def get_topology(self) -> dict:
        """
        Return available structural artifacts as a topology dict.
        Downstream systems (crawler, simulation) consume this.
        """
        artifact_dir = os.path.join(self.root, ARTIFACT_OUTPUT_DIR)
        topology = {}

        artifact_keys = {
            "dependency_graph.json": "dependency_graph",
            "module_topology.json": "module_topology",
            "structure_map.json": "structure_map",
            "namespace_conflicts.json": "namespace_conflicts",
            "circular_dependency_report.json": "circular_dependency_report",
            "governance_map.json": "governance_map",
        }

        for filename, key in artifact_keys.items():
            path = os.path.join(artifact_dir, filename)
            if os.path.exists(path):
                try:
                    with open(path) as f:
                        topology[key] = json.load(f)
                except Exception:
                    topology[key] = None
            else:
                topology[key] = None

        return topology


# ---------------------------------------------------------------------------
# CLI entry point (read-only / dry_run safe)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else "/workspaces/ARCHON_PRIME"
    controller = AnalysisController(root)
    results = controller.run_all_analysis()
    print(json.dumps(results, indent=2))
