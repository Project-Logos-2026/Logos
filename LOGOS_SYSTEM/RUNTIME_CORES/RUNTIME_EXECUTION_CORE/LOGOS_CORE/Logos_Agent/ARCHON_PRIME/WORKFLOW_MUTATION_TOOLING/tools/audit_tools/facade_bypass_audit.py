# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-029
# module_name:          facade_bypass_audit
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/facade_bypass_audit.py
# responsibility:       Inspection module: facade bypass audit
# runtime_stage:        audit
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

import ast
from pathlib import Path

from audit_utils import generate_id, write_log

FACADE = "imports"


def run(target):

    issues = []

    for p in Path(target).rglob("*.py"):

        try:

            tree = ast.parse(open(p).read())

            for node in ast.walk(tree):

                if isinstance(node, ast.ImportFrom):

                    if node.module and not node.module.startswith(FACADE):

                        issues.append(
                            {
                                "id": generate_id(str(p) + node.module),
                                "file": str(p),
                                "module": node.module,
                                "issue": "facade_bypass",
                            }
                        )

        except Exception:
            pass

    write_log("facade_bypass_audit", target, "facade_bypass", issues)
