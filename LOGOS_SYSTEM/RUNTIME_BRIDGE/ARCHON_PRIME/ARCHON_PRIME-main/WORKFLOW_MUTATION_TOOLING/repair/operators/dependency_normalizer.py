# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-013
# module_name:          dependency_normalizer
# subsystem:            mutation_tooling
# module_role:          mutation
# canonical_path:       WORKFLOW_MUTATION_TOOLING/repair/operators/dependency_normalizer.py
# responsibility:       Mutation module: dependency normalizer
# runtime_stage:        repair
# execution_entry:      None
# allowed_targets:      ["WORKFLOW_TARGET_PROCESSING/PROCESSING"]
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
ARCHON PRIME — Dependency Normalizer Operator
Stage 5: Repair System Implementation

Plans and applies corrections to inconsistent, missing, or circular
dependency declarations identified by the analysis subsystem.

SAFETY CONTRACT:
  - plan_repair() is always safe — read-only analysis only.
  - apply_repair() MUST NOT be called while mutation_allowed = false
    or crawl_mode = dry_run. The RepairController enforces this gate.
"""

from typing import Any, Dict


class DependencyNormalizerOperator:
    """
    Detects dependency inconsistencies (missing deps, circular imports,
    cross-package boundary violations) and plans normalization repairs.
    """

    ISSUE_TYPE = "dependency_inconsistency"

    def plan_repair(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse a dependency_inconsistency issue and produce a repair plan.
        Read-only — no file modifications occur here.

        Parameters
        ----------
        issue : dict with keys:
            module, file_path, inconsistency_type,
            offending_import, recommended_action

        Returns
        -------
        Repair plan dict.
        """
        module = issue.get("module", "unknown")
        file_path = issue.get("file_path", "")
        inconsistency_type = issue.get("inconsistency_type", "unknown")
        offending_import = issue.get("offending_import", "")
        recommended_action = issue.get("recommended_action", "review_manually")

        action_map = {
            "circular": "break_circular_import",
            "missing": "add_missing_dependency",
            "cross_package": "redirect_to_facade",
            "unused": "remove_unused_import",
        }
        action = action_map.get(inconsistency_type, "normalize_dependency")

        return {
            "operator": self.__class__.__name__,
            "issue_type": self.ISSUE_TYPE,
            "module": module,
            "file_path": file_path,
            "action": action,
            "inconsistency_type": inconsistency_type,
            "offending_import": offending_import,
            "recommended_action": recommended_action,
            "reversible": True,
            "mutation_required": True,
            "status": "planned",
            "applied": False,
        }

    def apply_repair(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply dependency normalization to the target file.

        THIS METHOD MUST ONLY BE CALLED WHEN mutation_allowed = true.
        """
        if not issue.get("_mutation_authorized", False):
            raise RuntimeError(
                "DependencyNormalizerOperator.apply_repair() called without "
                "mutation_authorized flag."
            )

        file_path = issue.get("file_path", "")
        offending_import = issue.get("offending_import", "")
        action = issue.get("action", "")

        if not file_path or not offending_import:
            return {"status": "failed", "reason": "Insufficient issue details"}

        if action == "remove_unused_import":
            try:
                with open(file_path, "r") as f:
                    lines = f.readlines()

                filtered = [line for line in lines if offending_import not in line]

                with open(file_path, "w") as f:
                    f.writelines(filtered)

                return {
                    "status": "applied",
                    "action": action,
                    "file_path": file_path,
                    "removed": offending_import,
                }

            except OSError as exc:
                return {"status": "failed", "reason": str(exc)}

        # All other dependency normalization actions require manual review
        return {
            "status": "deferred",
            "reason": (
                f"Action '{action}' requires manual review before automated apply"
            ),
            "file_path": file_path,
        }
