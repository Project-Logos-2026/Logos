# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-006
# module_name:          repair_controller
# subsystem:            mutation_tooling
# module_role:          orchestration
# canonical_path:       WORKFLOW_MUTATION_TOOLING/controllers/repair_controller.py
# responsibility:       Orchestration module: repair controller
# runtime_stage:        orchestration
# execution_entry:      run
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
ARCHON PRIME — Repair Controller
Stage 5: Repair System Implementation

Responsibilities:
  - Load repair registry from registry/repair_registry.json
  - Dynamically import repair operator classes
  - Consume upstream audit artifacts from AP_SYSTEM_AUDIT/
  - Map detected issues to appropriate repair operators
  - Generate deterministic repair plans (always safe, read-only)
  - Apply repairs ONLY when mutation_allowed = true AND crawl_mode != dry_run
  - Route repair plan artifact to AP_SYSTEM_AUDIT/repair_plan.json
  - Write import errors to AP_SYSTEM_AUDIT/REPAIR_IMPORT_ERRORS.json
"""

import importlib
import json
import os
import sys
import traceback
from typing import Any, Dict, List, Optional

from controllers.config_loader import ConfigLoader

ARTIFACT_OUTPUT_DIR = "AP_SYSTEM_AUDIT"
IMPORT_ERROR_ARTIFACT = "AP_SYSTEM_AUDIT/REPAIR_IMPORT_ERRORS.json"
REPAIR_PLAN_ARTIFACT = "AP_SYSTEM_AUDIT/repair_plan.json"

# Upstream artifacts produced by Stages 2–4 that drive repair candidate detection
UPSTREAM_ARTIFACTS = {
    "import_integrity": "AP_SYSTEM_AUDIT/import_integrity.json",
    "namespace_conflicts": "AP_SYSTEM_AUDIT/namespace_conflicts.json",
    "dependency_graph": "AP_SYSTEM_AUDIT/dependency_graph.json",
    "circular_dependency_report": "AP_SYSTEM_AUDIT/circular_dependency_report.json",
    "crawler_orphan_report": "AP_SYSTEM_AUDIT/crawler_orphan_report.json",
}

# Map audit issue types to operator module + class names
ISSUE_TYPE_OPERATOR_MAP = {
    "import_error": (
        "repair.operators.import_rewrite_operator",
        "ImportRewriteOperator",
    ),
    "header_violation": (
        "repair.operators.header_injection_operator",
        "HeaderInjectionOperator",
    ),
    "dependency_inconsistency": (
        "repair.operators.dependency_normalizer",
        "DependencyNormalizerOperator",
    ),
    "module_misplacement": (
        "repair.operators.module_relocation_operator",
        "ModuleRelocationOperator",
    ),
    "namespace_collision": (
        "repair.operators.namespace_disambiguator",
        "NamespaceDisambiguatorOperator",
    ),
}


class RepairController:
    """
    Orchestrates deterministic repository repair planning and execution.

    MUTATION GATE:
        Repairs are only applied when ALL of the following are true:
          - crawl_config.mutation_allowed = true
          - crawl_config.crawl_mode != "dry_run"
          - repair_config.repair_enabled = true

        In all other states, only plan_repair() is invoked (read-only).
    """

    def __init__(self, root_path: str):
        self.root = root_path
        self.config_loader = ConfigLoader(root_path)
        self.registry: List[Dict[str, Any]] = []
        self.crawl_config: Dict[str, Any] = {}
        self.repair_config: Dict[str, Any] = {}
        self.upstream_artifacts: Dict[str, Any] = {}
        self.import_errors: List[Dict[str, Any]] = []
        self._operator_cache: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def load_registry(self) -> List[Dict[str, Any]]:
        """Load repair operator registry from repair_registry.json."""
        raw = self.config_loader.load_repair_registry()
        self.registry = raw.get("repairs", [])
        return self.registry

    def load_configs(self) -> Dict[str, Any]:
        """Load crawl and repair configs."""
        self.crawl_config = self.config_loader.load_crawl_config()
        self.repair_config = self.config_loader.load_repair_config()
        return {"crawl_config": self.crawl_config, "repair_config": self.repair_config}

    @property
    def dry_run(self) -> bool:
        return self.crawl_config.get("crawl_mode") == "dry_run"

    @property
    def mutation_allowed(self) -> bool:
        return (
            bool(self.crawl_config.get("mutation_allowed", False))
            and not self.dry_run
            and bool(self.repair_config.get("repair_enabled", False))
        )

    # ------------------------------------------------------------------
    # Upstream artifact ingestion
    # ------------------------------------------------------------------

    def load_upstream_artifacts(self) -> Dict[str, Any]:
        """
        Read all upstream audit/analysis artifacts that determine
        repair candidates. Missing artifacts are recorded as None.
        """
        self.upstream_artifacts = {}
        for key, rel_path in UPSTREAM_ARTIFACTS.items():
            full_path = os.path.join(self.root, rel_path)
            if os.path.exists(full_path):
                try:
                    with open(full_path) as f:
                        self.upstream_artifacts[key] = json.load(f)
                except Exception:
                    self.upstream_artifacts[key] = None
            else:
                self.upstream_artifacts[key] = None
        return self.upstream_artifacts

    # ------------------------------------------------------------------
    # Import validation
    # ------------------------------------------------------------------

    def _ensure_root_on_path(self):
        if self.root not in sys.path:
            sys.path.insert(0, self.root)

    def validate_imports(self) -> List[Dict[str, Any]]:
        """
        Attempt to import all registered repair operator modules.
        Failures written to REPAIR_IMPORT_ERRORS.json; execution continues.
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

        error_path = os.path.join(self.root, IMPORT_ERROR_ARTIFACT)
        os.makedirs(os.path.dirname(error_path), exist_ok=True)
        with open(error_path, "w") as f:
            json.dump(
                {
                    "stage": "Repair System Implementation",
                    "import_errors": self.import_errors,
                    "total_errors": len(self.import_errors),
                },
                f,
                indent=2,
            )
        return self.import_errors

    # ------------------------------------------------------------------
    # Operator loading
    # ------------------------------------------------------------------

    def _load_operator(self, module_path: str, class_name: str) -> Optional[Any]:
        """Dynamically import and instantiate a repair operator class."""
        cache_key = f"{module_path}.{class_name}"
        if cache_key in self._operator_cache:
            return self._operator_cache[cache_key]

        self._ensure_root_on_path()
        try:
            mod = importlib.import_module(module_path)
            cls = getattr(mod, class_name)
            instance = cls()
            self._operator_cache[cache_key] = instance
            return instance
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Issue extraction from upstream artifacts
    # ------------------------------------------------------------------

    def _extract_issues(self) -> List[Dict[str, Any]]:
        """
        Extract repair candidate issues from all loaded upstream artifacts.
        Maps artifact data to standardised issue dicts with issue_type.
        """
        issues = []

        # Namespace conflicts → namespace_collision issues
        ns = self.upstream_artifacts.get("namespace_conflicts")
        if isinstance(ns, list):
            for item in ns:
                issues.append({**item, "issue_type": "namespace_collision"})
        elif isinstance(ns, dict):
            for item in ns.get("issues", ns.get("conflicts", [])) or []:
                issues.append({**item, "issue_type": "namespace_collision"})

        # Circular dependency report → dependency_inconsistency issues
        circ = self.upstream_artifacts.get("circular_dependency_report")
        if isinstance(circ, dict):
            for item in circ.get("cycles_detected", []):
                issues.append(
                    {
                        **item,
                        "issue_type": "dependency_inconsistency",
                        "inconsistency_type": "circular",
                        "file_path": item.get("cycle_at", ""),
                        "offending_import": item.get("back_edge", ""),
                    }
                )

        # Crawler orphan report → module_misplacement issues
        orphan_data = self.upstream_artifacts.get("crawler_orphan_report")
        if isinstance(orphan_data, dict):
            for item in orphan_data.get("orphan_modules", []):
                issues.append(
                    {
                        "module": item.get("import_path", item.get("path", "unknown")),
                        "current_path": item.get("absolute_path", item.get("path", "")),
                        "canonical_path": "",  # Requires human review to determine
                        "reason": "orphan_detected_by_crawler",
                        "issue_type": "module_misplacement",
                    }
                )

        # Import integrity → import_error issues
        integrity = self.upstream_artifacts.get("import_integrity")
        if isinstance(integrity, list):
            for item in integrity:
                issues.append({**item, "issue_type": "import_error"})
        elif isinstance(integrity, dict):
            for item in integrity.get("errors", []):
                issues.append({**item, "issue_type": "import_error"})

        return issues

    # ------------------------------------------------------------------
    # Repair planning
    # ------------------------------------------------------------------

    def generate_repair_plan(
        self, audit_results: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Map detected issues to repair operators and produce plan records.
        Always read-only — plan_repair() never mutates files.

        Parameters
        ----------
        audit_results : Optional list of pre-extracted issue dicts.
                        If None, issues are extracted from upstream artifacts.
        """
        if audit_results is None:
            issues = self._extract_issues()
        else:
            issues = audit_results

        planned_repairs = []
        operators_used = set()

        for issue in issues:
            issue_type = issue.get("issue_type", "")
            operator_spec = ISSUE_TYPE_OPERATOR_MAP.get(issue_type)
            if operator_spec is None:
                continue

            module_path, class_name = operator_spec
            operator = self._load_operator(module_path, class_name)
            if operator is None:
                planned_repairs.append(
                    {
                        "issue_type": issue_type,
                        "status": "operator_load_failed",
                        "module": module_path,
                    }
                )
                continue

            try:
                plan_record = operator.plan_repair(issue)
                planned_repairs.append(plan_record)
                operators_used.add(class_name)
            except Exception:
                planned_repairs.append(
                    {
                        "issue_type": issue_type,
                        "status": "plan_failed",
                        "error": traceback.format_exc().strip(),
                    }
                )

        repair_plan = {
            "repairs_planned": len(planned_repairs),
            "operators_used": sorted(operators_used),
            "issues_detected": len(issues),
            "mutation_allowed": self.mutation_allowed,
            "dry_run_active": self.dry_run,
            "planned_repairs": planned_repairs,
        }

        # Write repair plan artifact
        plan_path = os.path.join(self.root, REPAIR_PLAN_ARTIFACT)
        os.makedirs(os.path.dirname(plan_path), exist_ok=True)
        with open(plan_path, "w") as f:
            json.dump(repair_plan, f, indent=2)

        return repair_plan

    # ------------------------------------------------------------------
    # Repair application (mutation-gated)
    # ------------------------------------------------------------------

    def apply_repairs(self, repair_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Apply planned repairs to the repository.

        MUTATION GATE: This method checks mutation_allowed before any
        apply_repair() call. If the gate is closed, it returns immediately
        with a skipped status for all repairs.
        """
        if not self.mutation_allowed:
            return [
                {
                    "status": "skipped_mutation_not_allowed",
                    "dry_run": self.dry_run,
                    "mutation_allowed": self.mutation_allowed,
                    "message": (
                        "Repairs not applied: mutation_allowed=false or "
                        "dry_run active. Set crawl_mode != dry_run, "
                        "mutation_allowed = true, and repair_enabled = true to enable."
                    ),
                }
            ]

        results = []
        planned = repair_plan.get("planned_repairs", [])

        for plan_record in planned:
            issue_type = plan_record.get("issue_type", "")
            operator_spec = ISSUE_TYPE_OPERATOR_MAP.get(issue_type)
            if operator_spec is None:
                continue

            module_path, class_name = operator_spec
            operator = self._load_operator(module_path, class_name)
            if operator is None:
                results.append(
                    {
                        "status": "operator_load_failed",
                        "module": module_path,
                    }
                )
                continue

            # Authorize mutation for this single call
            issue_with_auth = {**plan_record, "_mutation_authorized": True}
            try:
                result = operator.apply_repair(issue_with_auth)
                results.append(result)
            except Exception:
                results.append(
                    {
                        "status": "apply_failed",
                        "error": traceback.format_exc().strip(),
                    }
                )

        return results

    # ------------------------------------------------------------------
    # Full pipeline entry point
    # ------------------------------------------------------------------

    def run(self, target_repo: str = None) -> Dict[str, Any]:
        """
        Full repair controller pipeline:
          1. Load configs and registry
          2. Load upstream artifacts
          3. Validate operator imports
          4. Generate repair plan (always)
          5. Apply repairs only if mutation gate is open
        """
        self.load_configs()
        self.load_registry()
        self.load_upstream_artifacts()
        self.validate_imports()
        repair_plan = self.generate_repair_plan()

        apply_results = []
        if self.mutation_allowed:
            apply_results = self.apply_repairs(repair_plan)

        return {
            "repair_plan": repair_plan,
            "apply_results": apply_results,
            "mutation_allowed": self.mutation_allowed,
            "dry_run": self.dry_run,
        }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else "/workspaces/ARCHON_PRIME"
    controller = RepairController(root)
    results = controller.run()
    plan = results.get("repair_plan", {})
    print(
        json.dumps(
            {k: v for k, v in plan.items() if k != "planned_repairs"},
            indent=2,
        )
    )
