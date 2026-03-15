# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-016
# module_name:          header_injection_operator
# subsystem:            mutation_tooling
# module_role:          mutation
# canonical_path:       WORKFLOW_MUTATION_TOOLING/repair/operators/header_injection_operator.py
# responsibility:       Mutation module: header injection operator
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
ARCHON PRIME — Header Injection Operator
Stage 5: Repair System Implementation

Plans and applies canonical header block injection into Python modules
that are missing required governance/metadata headers.

SAFETY CONTRACT:
  - plan_repair() is always safe — read-only analysis only.
  - apply_repair() MUST NOT be called while mutation_allowed = false
    or crawl_mode = dry_run. The RepairController enforces this gate.
"""

from typing import Any, Dict

CANONICAL_HEADER_TEMPLATE = '''\
"""
Module: {module_name}
Purpose: {purpose}
Status: PENDING_REVIEW
"""
'''


class HeaderInjectionOperator:
    """
    Detects Python modules missing governance header blocks
    and plans/applies canonical header injection.
    """

    ISSUE_TYPE = "header_violation"

    def plan_repair(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse a header_violation issue and produce a repair plan record.
        Read-only — no file modifications occur here.

        Parameters
        ----------
        issue : dict with keys: module, file_path, violation_type, expected_header

        Returns
        -------
        Repair plan dict.
        """
        module = issue.get("module", "unknown")
        file_path = issue.get("file_path", "")
        violation_type = issue.get("violation_type", "missing_header")
        expected_header = issue.get(
            "expected_header",
            CANONICAL_HEADER_TEMPLATE.format(
                module_name=module, purpose="auto-detected"
            ),
        )

        return {
            "operator": self.__class__.__name__,
            "issue_type": self.ISSUE_TYPE,
            "module": module,
            "file_path": file_path,
            "action": "inject_header",
            "violation_type": violation_type,
            "header_to_inject": expected_header,
            "inject_position": "top_of_file",
            "reversible": True,
            "mutation_required": True,
            "status": "planned",
            "applied": False,
        }

    def apply_repair(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inject canonical header into the target file.

        THIS METHOD MUST ONLY BE CALLED WHEN mutation_allowed = true.
        """
        if not issue.get("_mutation_authorized", False):
            raise RuntimeError(
                "HeaderInjectionOperator.apply_repair() called without "
                "mutation_authorized flag."
            )

        file_path = issue.get("file_path", "")
        header = issue.get(
            "expected_header",
            CANONICAL_HEADER_TEMPLATE.format(
                module_name=issue.get("module", "unknown"),
                purpose="auto-detected",
            ),
        )

        if not file_path:
            return {"status": "failed", "reason": "No file_path provided"}

        try:
            with open(file_path, "r") as f:
                existing = f.read()

            # Do not double-inject
            if existing.lstrip().startswith('"""'):
                return {"status": "skipped", "reason": "Header already present"}

            with open(file_path, "w") as f:
                f.write(header + "\n" + existing)

            return {"status": "applied", "file_path": file_path}

        except OSError as exc:
            return {"status": "failed", "reason": str(exc)}
