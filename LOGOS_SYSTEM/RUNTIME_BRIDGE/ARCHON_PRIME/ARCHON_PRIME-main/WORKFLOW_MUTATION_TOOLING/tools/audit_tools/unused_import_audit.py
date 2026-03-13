# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-048
# module_name:          unused_import_audit
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/unused_import_audit.py
# responsibility:       Inspection module: unused import audit
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


def run(target):

    issues = []

    for p in Path(target).rglob("*.py"):

        try:
            tree = ast.parse(open(p).read())

            imports = []
            names = set()

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):
                    for n in node.names:
                        imports.append(n.name)

                if isinstance(node, ast.Name):
                    names.add(node.id)

            for imp in imports:
                if imp.split(".")[0] not in names:

                    issues.append(
                        {
                            "id": generate_id(str(p) + imp),
                            "file": str(p),
                            "import": imp,
                            "issue": "unused_import",
                        }
                    )

        except Exception:
            pass

    write_log("unused_import_audit", target, "unused_import", issues)
