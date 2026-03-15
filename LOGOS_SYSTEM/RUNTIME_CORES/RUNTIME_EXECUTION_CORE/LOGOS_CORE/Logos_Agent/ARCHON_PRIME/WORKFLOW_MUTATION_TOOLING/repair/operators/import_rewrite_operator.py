# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-017
# module_name:          import_rewrite_operator
# subsystem:            mutation_tooling
# module_role:          mutation
# canonical_path:       WORKFLOW_MUTATION_TOOLING/repair/operators/import_rewrite_operator.py
# responsibility:       Mutation module: import rewrite operator
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
ARCHON PRIME — Import Rewrite Operator
Stage 5: Repair System Implementation

Plans and applies corrections to broken or malformed import statements.

SAFETY CONTRACT:
  - plan_repair() is always safe — read-only analysis only.
  - apply_repair() MUST NOT be called while mutation_allowed = false
    or crawl_mode = dry_run. The RepairController enforces this gate.
"""

from typing import Any, Dict


class ImportRewriteOperator:
    """
    Detects broken, ambiguous, or non-canonical import statements
    and produces correction plans. Applies rewrites only when
    explicitly permitted by the crawl configuration.
    """

    ISSUE_TYPE = "import_error"

    def plan_repair(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse an import_error issue and produce a repair plan record.
        Read-only — no file modifications occur here.

        Parameters
        ----------
        issue : dict with keys: module, file_path, broken_import, suggested_import

        Returns
        -------
        Repair plan dict describing the correction to be applied.
        """
        module = issue.get("module", "unknown")
        file_path = issue.get("file_path", "")
        broken = issue.get("broken_import", "")
        suggested = issue.get("suggested_import", "")

        plan = {
            "operator": self.__class__.__name__,
            "issue_type": self.ISSUE_TYPE,
            "module": module,
            "file_path": file_path,
            "action": "rewrite_import",
            "from": broken,
            "to": suggested,
            "reversible": True,
            "mutation_required": True,
            "status": "planned",
            "applied": False,
        }
        return plan

    def apply_repair(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply the planned import rewrite to the target file.

        THIS METHOD MUST ONLY BE CALLED WHEN mutation_allowed = true.
        The RepairController is responsible for enforcing this gate.
        Raises RuntimeError if called without explicit mutation authorization.
        """
        if not issue.get("_mutation_authorized", False):
            raise RuntimeError(
                "ImportRewriteOperator.apply_repair() called without "
                "mutation_authorized flag. RepairController must set this "
                "only when crawl_config mutation_allowed = true."
            )

        file_path = issue.get("file_path", "")
        broken = issue.get("broken_import", "")
        suggested = issue.get("suggested_import", "")

        if not file_path or not broken or not suggested:
            return {"status": "failed", "reason": "Insufficient issue details"}

        try:
            with open(file_path, "r") as f:
                source = f.read()

            if broken not in source:
                return {"status": "skipped", "reason": "Pattern not found in source"}

            rewritten = source.replace(broken, suggested)

            with open(file_path, "w") as f:
                f.write(rewritten)

            return {
                "status": "applied",
                "file_path": file_path,
                "replaced": broken,
                "with": suggested,
            }

        except OSError as exc:
            return {"status": "failed", "reason": str(exc)}
