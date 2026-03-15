# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-005
# module_name:          pipeline_controller
# subsystem:            mutation_tooling
# module_role:          orchestration
# canonical_path:       WORKFLOW_MUTATION_TOOLING/controllers/pipeline_controller.py
# responsibility:       Orchestration module: pipeline controller
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
ARCHON PRIME — Pipeline Controller
Stage 6: Pipeline Controller Implementation

Orchestrates the full AP workflow pipeline in strict deterministic order:

    audit → analysis → simulation → crawl → repair

Responsibilities:
  - Initialize and sequence all sub-controllers
  - Enforce phase gate validation between every stage
  - Verify required artifacts exist before advancing
  - Enforce mutation safety throughout
  - Write pipeline manifest and failure report artifacts
  - Halt pipeline on any stage failure
"""

import importlib
import json
import os
import sys
import traceback
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from controllers.config_loader import ConfigLoader

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ARTIFACT_DIR = "AP_SYSTEM_AUDIT"
MANIFEST_ARTIFACT = "AP_SYSTEM_AUDIT/pipeline_execution_manifest.json"
FAILURE_REPORT_ARTIFACT = "AP_SYSTEM_AUDIT/pipeline_failure_report.json"
IMPORT_ERROR_ARTIFACT = "AP_SYSTEM_AUDIT/PIPELINE_IMPORT_ERRORS.json"

PHASE_GATE_SCHEMA_PATH = "schemas/PhaseGate.schema.json"
VALIDATION_MANIFEST_SCHEMA_PATH = "schemas/ValidationManifest.schema.json"

# Required artifacts that must exist before each stage is considered complete
STAGE_ARTIFACT_GATES: Dict[str, List[str]] = {
    "audit": [
        "AP_SYSTEM_AUDIT/AP_STAGE1_AUDIT_SYSTEM_REPORT.json",
    ],
    "analysis": [
        "AP_SYSTEM_AUDIT/AP_STAGE2_ANALYSIS_SYSTEM_REPORT.json",
        "AP_SYSTEM_AUDIT/ANALYSIS_IMPORT_ERRORS.json",
    ],
    "simulation": [
        "AP_SYSTEM_AUDIT/AP_STAGE3_SIMULATION_SYSTEM_REPORT.json",
        "AP_SYSTEM_AUDIT/SIMULATION_IMPORT_ERRORS.json",
    ],
    "crawl": [
        "AP_SYSTEM_AUDIT/AP_STAGE4_CRAWLER_SYSTEM_REPORT.json",
        "AP_SYSTEM_AUDIT/crawler_traversal_plan.json",
        "AP_SYSTEM_AUDIT/CRAWLER_IMPORT_ERRORS.json",
    ],
    "repair": [
        "AP_SYSTEM_AUDIT/AP_STAGE5_REPAIR_SYSTEM_REPORT.json",
        "AP_SYSTEM_AUDIT/repair_plan.json",
        "AP_SYSTEM_AUDIT/REPAIR_IMPORT_ERRORS.json",
    ],
}

PIPELINE_STAGE_ORDER = ["audit", "analysis", "simulation", "crawl", "repair"]


# ---------------------------------------------------------------------------
# PipelineController
# ---------------------------------------------------------------------------


class PipelineController:
    """
    Deterministic pipeline orchestrator for Archon Prime.

    Executes sub-controllers in strict order, validates phase gates between
    each stage, and enforces mutation safety throughout.
    """

    def __init__(self, root_path: str):
        self.root = root_path
        self.config_loader = ConfigLoader(root_path)
        self.crawl_config: Dict[str, Any] = {}
        self.simulation_config: Dict[str, Any] = {}
        self.repair_config: Dict[str, Any] = {}
        self.phase_gate_schema: Dict[str, Any] = {}
        self.validation_manifest_schema: Dict[str, Any] = {}
        self.stage_results: Dict[str, Any] = {}
        self.pipeline_halted: bool = False
        self.halt_reason: str = ""

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def _load_configs(self):
        self.crawl_config = self.config_loader.load_crawl_config()
        self.simulation_config = self.config_loader.load_simulation_config()
        self.repair_config = self.config_loader.load_repair_config()
        self._load_schemas()

    def _load_schemas(self):
        """Load PhaseGate and ValidationManifest schemas for gate validation."""
        for attr, rel_path in [
            ("phase_gate_schema", PHASE_GATE_SCHEMA_PATH),
            ("validation_manifest_schema", VALIDATION_MANIFEST_SCHEMA_PATH),
        ]:
            full = os.path.join(self.root, rel_path)
            if os.path.exists(full):
                with open(full) as f:
                    setattr(self, attr, json.load(f))

    @property
    def dry_run(self) -> bool:
        return self.crawl_config.get("crawl_mode") == "dry_run"

    @property
    def mutation_allowed(self) -> bool:
        return (
            bool(self.crawl_config.get("mutation_allowed", False)) and not self.dry_run
        )

    # ------------------------------------------------------------------
    # Manifest helpers
    # ------------------------------------------------------------------

    def _ts(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _write_json(self, rel_path: str, data: Any):
        full = os.path.join(self.root, rel_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            json.dump(data, f, indent=2)

    def _init_manifest(self) -> Dict[str, Any]:
        manifest = {
            "pipeline_stages": PIPELINE_STAGE_ORDER,
            "pipeline_status": "running",
            "mutation_allowed": self.mutation_allowed,
            "dry_run": self.dry_run,
            "started_at": self._ts(),
            "completed_at": None,
            "stages": {
                s: {"status": "pending", "completed_at": None}
                for s in PIPELINE_STAGE_ORDER
            },
            "halted": False,
            "halt_reason": None,
        }
        self._write_json(MANIFEST_ARTIFACT, manifest)
        return manifest

    def _update_manifest(
        self, manifest: Dict[str, Any], stage: str, status: str, detail: str = ""
    ):
        manifest["stages"][stage]["status"] = status
        manifest["stages"][stage]["completed_at"] = self._ts()
        if detail:
            manifest["stages"][stage]["detail"] = detail
        self._write_json(MANIFEST_ARTIFACT, manifest)

    def _finalize_manifest(self, manifest: Dict[str, Any], status: str):
        manifest["pipeline_status"] = status
        manifest["completed_at"] = self._ts()
        manifest["halted"] = self.pipeline_halted
        manifest["halt_reason"] = self.halt_reason if self.pipeline_halted else None
        self._write_json(MANIFEST_ARTIFACT, manifest)

    def _write_failure_report(self, stage: str, error: str, stage_results: Dict):
        self._write_json(
            FAILURE_REPORT_ARTIFACT,
            {
                "pipeline_status": "FAILED",
                "failed_stage": stage,
                "error": error,
                "timestamp": self._ts(),
                "stage_results_at_failure": stage_results,
            },
        )

    # ------------------------------------------------------------------
    # Phase gate validation
    # ------------------------------------------------------------------

    def _validate_phase_gate(self, stage: str) -> Dict[str, Any]:
        """
        Validate that all required artifacts for a completed stage exist.
        Uses STAGE_ARTIFACT_GATES and PhaseGate schema definition.
        Returns {"passed": bool, "missing": list, "stage": str}.
        """
        required = STAGE_ARTIFACT_GATES.get(stage, [])
        missing = []
        for rel_path in required:
            full = os.path.join(self.root, rel_path)
            if not os.path.exists(full):
                missing.append(rel_path)

        # Additional: verify each existing JSON artifact is parseable
        corrupt = []
        for rel_path in required:
            full = os.path.join(self.root, rel_path)
            if os.path.exists(full) and full.endswith(".json"):
                try:
                    with open(full) as f:
                        json.load(f)
                except (json.JSONDecodeError, OSError) as exc:
                    corrupt.append(f"{rel_path}: {exc}")

        passed = len(missing) == 0 and len(corrupt) == 0
        return {
            "stage": stage,
            "passed": passed,
            "required_artifacts": required,
            "missing_artifacts": missing,
            "corrupt_artifacts": corrupt,
            "schema_used": "PhaseGate",
        }

    def _validate_validation_manifest(self) -> Dict[str, Any]:
        """
        Validate overall system readiness using ValidationManifest schema fields.
        Checks whether simulation artifacts confirm system health.
        """
        checks = {
            "imports_normalized": False,
            "dependencies_resolved": False,
            "namespaces_clean": False,
            "governance_enforced": False,
            "runtime_boot_valid": False,
        }

        # imports_normalized: import simulation report exists and completed
        imp_path = os.path.join(
            self.root, "AP_SYSTEM_AUDIT/import_simulation_report.json"
        )
        if os.path.exists(imp_path):
            try:
                data = json.load(open(imp_path))
                checks["imports_normalized"] = data.get("status") == "complete"
            except Exception:
                pass

        # dependencies_resolved: dependency simulation report exists
        dep_path = os.path.join(
            self.root, "AP_SYSTEM_AUDIT/dependency_simulation_report.json"
        )
        if os.path.exists(dep_path):
            try:
                data = json.load(open(dep_path))
                checks["dependencies_resolved"] = data.get("status") == "complete"
            except Exception:
                pass

        # namespaces_clean: namespace simulation report exists
        ns_path = os.path.join(
            self.root, "AP_SYSTEM_AUDIT/namespace_simulation_report.json"
        )
        if os.path.exists(ns_path):
            try:
                data = json.load(open(ns_path))
                checks["namespaces_clean"] = data.get("total_conflicts_found", -1) == 0
            except Exception:
                pass

        # governance_enforced: governance map exists
        gov_path = os.path.join(self.root, "AP_SYSTEM_AUDIT/governance_map.json")
        checks["governance_enforced"] = os.path.exists(gov_path)

        # runtime_boot_valid: runtime boot simulation exists
        rb_path = os.path.join(
            self.root, "AP_SYSTEM_AUDIT/runtime_boot_simulation.json"
        )
        if os.path.exists(rb_path):
            try:
                data = json.load(open(rb_path))
                checks["runtime_boot_valid"] = data.get("status") == "complete"
            except Exception:
                pass

        return {"schema_used": "ValidationManifest", "checks": checks}

    # ------------------------------------------------------------------
    # Stage runners
    # ------------------------------------------------------------------

    def run_audit_stage(self, target_repo: str) -> Dict[str, Any]:
        """Stage 1 — Audit: validate registry, import audit modules."""
        try:
            sys.path.insert(0, self.root)
            from controllers.audit_controller import AuditController

            ctrl = AuditController(root_path=self.root)
            # Run the import validation portion only (read-only)
            errors = ctrl.validate_imports()
            imported = len(ctrl.registry.get("audits", [])) - len(errors)
            return {
                "stage": "audit",
                "status": "success",
                "modules_registered": len(ctrl.registry.get("audits", [])),
                "modules_imported": imported,
                "import_errors": len(errors),
            }
        except Exception:
            return {
                "stage": "audit",
                "status": "failed",
                "error": traceback.format_exc().strip(),
            }

    def run_analysis_stage(self, target_repo: str) -> Dict[str, Any]:
        """Stage 2 — Analysis: load analysis modules and validate imports."""
        try:
            from controllers.analysis_controller import AnalysisController

            ctrl = AnalysisController(self.root)
            ctrl.load_registry()
            ctrl.load_configs()
            errors = ctrl.validate_imports()
            return {
                "stage": "analysis",
                "status": "success",
                "modules_registered": len(ctrl.registry),
                "import_errors": len(errors),
                "dry_run": ctrl.dry_run,
            }
        except Exception:
            return {
                "stage": "analysis",
                "status": "failed",
                "error": traceback.format_exc().strip(),
            }

    def run_simulation_stage(self, target_repo: str) -> Dict[str, Any]:
        """Stage 3 — Simulation: load simulators, validate imports."""
        try:
            from controllers.simulation_controller import SimulationController

            ctrl = SimulationController(self.root)
            ctrl.load_registry()
            ctrl.load_configs()
            ctrl.load_analysis_artifacts()
            errors = ctrl.validate_imports()
            return {
                "stage": "simulation",
                "status": "success",
                "simulators_registered": len(ctrl.registry),
                "import_errors": len(errors),
                "dry_run": ctrl.dry_run,
                "analysis_artifacts_loaded": sum(
                    1 for v in ctrl.analysis_artifacts.values() if v is not None
                ),
            }
        except Exception:
            return {
                "stage": "simulation",
                "status": "failed",
                "error": traceback.format_exc().strip(),
            }

    def run_crawl_stage(self, target_repo: str) -> Dict[str, Any]:
        """Stage 4 — Crawl: load config, targets, validate imports, run crawl."""
        try:
            from controllers.crawler_controller import CrawlerController

            ctrl = CrawlerController(self.root)
            ctrl.load_configs()
            ctrl.load_targets()
            errors = ctrl.validate_imports()
            result = ctrl.run_crawl(target_repo=target_repo)
            summary = result.get("crawl_summary", {})
            return {
                "stage": "crawl",
                "status": "success",
                "import_errors": len(errors),
                "files_scanned": summary.get("files_scanned", 0),
                "modules_discovered": summary.get("modules_discovered", 0),
                "orphans_detected": summary.get("orphans_detected", 0),
                "dry_run": result.get("dry_run"),
            }
        except Exception:
            return {
                "stage": "crawl",
                "status": "failed",
                "error": traceback.format_exc().strip(),
            }

    def run_repair_stage(self, target_repo: str) -> Dict[str, Any]:
        """Stage 5 — Repair: load registry, validate imports, generate plan."""
        try:
            from controllers.repair_controller import RepairController

            ctrl = RepairController(self.root)
            ctrl.load_configs()
            ctrl.load_registry()
            ctrl.load_upstream_artifacts()
            errors = ctrl.validate_imports()
            plan = ctrl.generate_repair_plan()
            return {
                "stage": "repair",
                "status": "success",
                "operators_registered": len(ctrl.registry),
                "import_errors": len(errors),
                "repairs_planned": plan.get("repairs_planned", 0),
                "issues_detected": plan.get("issues_detected", 0),
                "mutation_allowed": ctrl.mutation_allowed,
            }
        except Exception:
            return {
                "stage": "repair",
                "status": "failed",
                "error": traceback.format_exc().strip(),
            }

    # ------------------------------------------------------------------
    # Full pipeline
    # ------------------------------------------------------------------

    def run_pipeline(self, target_repo: str = None) -> Dict[str, Any]:
        """
        Execute the full AP pipeline in strict deterministic order:
            audit → analysis → simulation → crawl → repair

        Phase gates are validated after each stage.
        Pipeline halts immediately on any stage failure or gate failure.
        """
        if target_repo is None:
            target_repo = self.root

        self._load_configs()
        manifest = self._init_manifest()

        stage_runners = {
            "audit": self.run_audit_stage,
            "analysis": self.run_analysis_stage,
            "simulation": self.run_simulation_stage,
            "crawl": self.run_crawl_stage,
            "repair": self.run_repair_stage,
        }

        for stage in PIPELINE_STAGE_ORDER:
            if self.pipeline_halted:
                break

            runner = stage_runners[stage]

            # --- Execute stage ---
            result = runner(target_repo)
            self.stage_results[stage] = result

            if result.get("status") == "failed":
                error_msg = result.get("error", "unknown error")
                self.pipeline_halted = True
                self.halt_reason = f"Stage '{stage}' failed: {error_msg[:200]}"
                self._update_manifest(manifest, stage, "failed", self.halt_reason)
                self._write_failure_report(stage, error_msg, self.stage_results)
                self._finalize_manifest(manifest, "FAILED")
                return self._build_pipeline_result(manifest)

            # --- Phase gate validation ---
            gate_result = self._validate_phase_gate(stage)
            self.stage_results[f"{stage}_gate"] = gate_result

            if not gate_result["passed"]:
                gate_error = (
                    f"Phase gate FAILED for stage '{stage}'. "
                    f"Missing: {gate_result['missing_artifacts']}. "
                    f"Corrupt: {gate_result['corrupt_artifacts']}."
                )
                self.pipeline_halted = True
                self.halt_reason = gate_error
                self._update_manifest(manifest, stage, "gate_failed", gate_error)
                self._write_failure_report(stage, gate_error, self.stage_results)
                self._finalize_manifest(manifest, "FAILED")
                return self._build_pipeline_result(manifest)

            self._update_manifest(manifest, stage, "success")

        # --- Final ValidationManifest check ---
        validation_manifest = self._validate_validation_manifest()
        self._write_json(
            "AP_SYSTEM_AUDIT/pipeline_validation_manifest.json",
            validation_manifest,
        )

        final_status = "COMPLETE" if not self.pipeline_halted else "FAILED"
        self._finalize_manifest(manifest, final_status)

        return self._build_pipeline_result(manifest, validation_manifest)

    def _build_pipeline_result(
        self,
        manifest: Dict[str, Any],
        validation_manifest: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return {
            "pipeline_status": manifest.get("pipeline_status"),
            "halted": self.pipeline_halted,
            "halt_reason": self.halt_reason or None,
            "stage_results": self.stage_results,
            "validation_manifest": validation_manifest,
            "dry_run": self.dry_run,
            "mutation_allowed": self.mutation_allowed,
        }


# ---------------------------------------------------------------------------
# Import validation helper (used by Stage 6 report)
# ---------------------------------------------------------------------------


def validate_pipeline_import(root_path: str) -> List[Dict[str, Any]]:
    """
    Attempt to import PipelineController.
    Writes PIPELINE_IMPORT_ERRORS.json. Returns list of errors.
    """
    errors = []
    try:
        if root_path not in sys.path:
            sys.path.insert(0, root_path)
        importlib.import_module("controllers.pipeline_controller")
    except Exception:
        errors.append(
            {
                "module": "controllers.pipeline_controller",
                "error": traceback.format_exc().strip(),
            }
        )

    error_path = os.path.join(root_path, IMPORT_ERROR_ARTIFACT)
    os.makedirs(os.path.dirname(error_path), exist_ok=True)
    with open(error_path, "w") as f:
        json.dump(
            {
                "stage": "Pipeline Controller Implementation",
                "import_errors": errors,
                "total_errors": len(errors),
            },
            f,
            indent=2,
        )
    return errors


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "/workspaces/ARCHON_PRIME"
    controller = PipelineController(root)
    result = controller.run_pipeline()
    print(
        json.dumps(
            {k: v for k, v in result.items() if k != "stage_results"},
            indent=2,
        )
    )
