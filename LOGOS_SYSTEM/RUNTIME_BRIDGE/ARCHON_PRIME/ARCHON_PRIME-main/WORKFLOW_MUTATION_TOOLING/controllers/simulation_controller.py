# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-007
# module_name:          simulation_controller
# subsystem:            mutation_tooling
# module_role:          orchestration
# canonical_path:       WORKFLOW_MUTATION_TOOLING/controllers/simulation_controller.py
# responsibility:       Orchestration module: simulation controller
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
ARCHON PRIME — Simulation Controller
Stage 3: Simulation System Activation

Responsibilities:
  - Load simulation registry
  - Dynamically import simulator modules
  - Execute simulation modules (read-only)
  - Consume analysis artifacts from AP_SYSTEM_AUDIT/
  - Route simulation outputs to AP_SYSTEM_AUDIT/
  - Respect dry_run mode from crawl_config
"""

import importlib
import json
import os
import sys
import traceback

from controllers.config_loader import ConfigLoader

ARTIFACT_OUTPUT_DIR = "AP_SYSTEM_AUDIT"
IMPORT_ERROR_ARTIFACT = "AP_SYSTEM_AUDIT/SIMULATION_IMPORT_ERRORS.json"

# Analysis artifacts produced by Stage-2 that simulations consume
ANALYSIS_ARTIFACT_INPUTS = {
    "dependency_graph": "AP_SYSTEM_AUDIT/dependency_graph.json",
    "module_topology": "AP_SYSTEM_AUDIT/module_topology.json",
    "structure_map": "AP_SYSTEM_AUDIT/structure_map.json",
    "governance_map": "AP_SYSTEM_AUDIT/governance_map.json",
    "namespace_conflicts": "AP_SYSTEM_AUDIT/namespace_conflicts.json",
}


class SimulationController:

    def __init__(self, root_path: str):
        self.root = root_path
        self.config_loader = ConfigLoader(root_path)
        self.registry = []
        self.simulation_config = {}
        self.crawl_config = {}
        self.import_errors = []
        self.analysis_artifacts = {}

    # ------------------------------------------------------------------
    # Registry and configuration loading
    # ------------------------------------------------------------------

    def load_registry(self) -> list:
        """Load simulation entries from simulation_registry.json."""
        sim_registry = self.config_loader.load_simulation_registry()
        self.registry = sim_registry.get("simulations", [])
        return self.registry

    def load_configs(self) -> dict:
        """Load simulation and crawl configs. Respects dry_run mode."""
        self.simulation_config = self.config_loader.load_simulation_config()
        self.crawl_config = self.config_loader.load_crawl_config()
        return {
            "simulation_config": self.simulation_config,
            "crawl_config": self.crawl_config,
        }

    @property
    def dry_run(self) -> bool:
        return self.crawl_config.get("crawl_mode") == "dry_run"

    # ------------------------------------------------------------------
    # Analysis artifact ingestion (Stage-2 outputs → Stage-3 inputs)
    # ------------------------------------------------------------------

    def load_analysis_artifacts(self) -> dict:
        """
        Read structural artifacts produced by Stage-2 AnalysisController.
        Missing artifacts are noted but do not block execution.
        """
        self.analysis_artifacts = {}
        for key, rel_path in ANALYSIS_ARTIFACT_INPUTS.items():
            full_path = os.path.join(self.root, rel_path)
            if os.path.exists(full_path):
                try:
                    with open(full_path) as f:
                        self.analysis_artifacts[key] = json.load(f)
                except Exception:
                    self.analysis_artifacts[key] = None
            else:
                self.analysis_artifacts[key] = None
        return self.analysis_artifacts

    # ------------------------------------------------------------------
    # Module import validation
    # ------------------------------------------------------------------

    def _ensure_root_on_path(self):
        """Add repo root to sys.path so simulation packages are importable."""
        if self.root not in sys.path:
            sys.path.insert(0, self.root)

    def validate_imports(self) -> list:
        """
        Attempt to import every registered simulation module.
        Failures are collected and written to SIMULATION_IMPORT_ERRORS.json.
        Does not raise on failure.
        """
        self._ensure_root_on_path()
        self.import_errors = []

        for entry in self.registry:
            module_path = entry.get("module", "")
            try:
                importlib.import_module(module_path)
            except Exception:
                self.import_errors.append(
                    {
                        "module": module_path,
                        "name": entry.get("name"),
                        "error": traceback.format_exc().strip(),
                    }
                )

        error_artifact_path = os.path.join(self.root, IMPORT_ERROR_ARTIFACT)
        os.makedirs(os.path.dirname(error_artifact_path), exist_ok=True)
        with open(error_artifact_path, "w") as f:
            json.dump(
                {
                    "stage": "Simulation System Activation",
                    "import_errors": self.import_errors,
                    "total_errors": len(self.import_errors),
                },
                f,
                indent=2,
            )

        return self.import_errors

    # ------------------------------------------------------------------
    # Simulation execution
    # ------------------------------------------------------------------

    def _is_enabled(self, entry: dict) -> bool:
        """Check simulation_config flag for this simulator."""
        flag = entry.get("config_flag")
        if flag is None:
            return True  # No flag means always enabled
        return bool(self.simulation_config.get(flag, True))

    def run_simulation(self, sim_entry: dict) -> dict:
        """
        Dynamically import and execute a single simulator.
        Returns a result record with status and artifact path.
        Execution is skipped if dry_run is active or config flag is off.
        """
        self._ensure_root_on_path()
        name = sim_entry.get("name", "unknown")
        module_path = sim_entry.get("module", "")
        entry_function = sim_entry.get("entry_function", "auto_detect")
        artifact_output = sim_entry.get("artifact_output", "")

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

        if not self._is_enabled(sim_entry):
            result["status"] = "skipped_disabled"
            return result

        try:
            mod = importlib.import_module(module_path)

            if entry_function == "auto_detect":
                for candidate in ("simulate", "run", "main"):
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

            # Pass root path so simulators can locate analysis artifacts
            try:
                func(self.root)
            except TypeError:
                func()

            self._ensure_artifact_routed(artifact_output)
            result["status"] = "success"

        except Exception:
            result["status"] = "failed"
            result["error"] = traceback.format_exc().strip()

        return result

    def _ensure_artifact_routed(self, artifact_output: str):
        """Ensure artifact output directory exists under AP_SYSTEM_AUDIT/."""
        if not artifact_output:
            return
        full_path = os.path.join(self.root, artifact_output)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

    def run_all_simulations(self, target_repo: str = None) -> list:
        """
        Execute all registered simulators in sequence.
        Returns list of result records.
        """
        if target_repo is None:
            target_repo = self.root

        self.load_configs()
        self.load_registry()
        self.load_analysis_artifacts()
        self.validate_imports()

        results = []
        for sim_entry in self.registry:
            result = self.run_simulation(sim_entry)
            results.append(result)

        return results

    # ------------------------------------------------------------------
    # Status / topology accessor
    # ------------------------------------------------------------------

    def get_simulation_outputs(self) -> dict:
        """
        Return available simulation artifacts as a dict.
        Downstream systems may consume these predictions.
        """
        artifact_dir = os.path.join(self.root, ARTIFACT_OUTPUT_DIR)
        outputs = {}

        artifact_keys = {
            "dependency_simulation_report.json": "dependency_simulation",
            "import_simulation_report.json": "import_simulation",
            "namespace_simulation_report.json": "namespace_simulation",
            "runtime_boot_simulation.json": "runtime_boot_simulation",
            "repo_simulation_report.json": "repo_simulation",
        }

        for filename, key in artifact_keys.items():
            path = os.path.join(artifact_dir, filename)
            if os.path.exists(path):
                try:
                    with open(path) as f:
                        outputs[key] = json.load(f)
                except Exception:
                    outputs[key] = None
            else:
                outputs[key] = None

        return outputs


# ---------------------------------------------------------------------------
# CLI entry point (read-only / dry_run safe)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else "/workspaces/ARCHON_PRIME"
    controller = SimulationController(root)
    results = controller.run_all_simulations()
    print(json.dumps(results, indent=2))
