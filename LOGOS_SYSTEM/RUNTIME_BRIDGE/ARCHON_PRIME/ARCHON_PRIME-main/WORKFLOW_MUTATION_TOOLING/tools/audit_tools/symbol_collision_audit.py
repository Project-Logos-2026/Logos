# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-046
# module_name:          symbol_collision_audit
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/symbol_collision_audit.py
# responsibility:       Inspection module: symbol collision audit
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

    symbols = {}
    issues = []

    for p in Path(target).rglob("*.py"):

        try:
            tree = ast.parse(open(p).read())

            for node in ast.walk(tree):

                if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):

                    name = node.name

                    if name in symbols:

                        issues.append(
                            {
                                "id": generate_id(name + str(p)),
                                "symbol": name,
                                "file_a": symbols[name],
                                "file_b": str(p),
                                "issue": "symbol_collision",
                            }
                        )

                    else:
                        symbols[name] = str(p)

        except Exception:
            pass

    write_log("symbol_collision_audit", target, "symbol_collision", issues)
