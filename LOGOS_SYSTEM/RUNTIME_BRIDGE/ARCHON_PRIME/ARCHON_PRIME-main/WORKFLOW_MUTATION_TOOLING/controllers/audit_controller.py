# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-002
# module_name:          audit_controller
# subsystem:            mutation_tooling
# module_role:          orchestration
# canonical_path:       WORKFLOW_MUTATION_TOOLING/controllers/audit_controller.py
# responsibility:       Orchestration module: audit controller
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

import datetime
import importlib.util
import json
import sys
from pathlib import Path

# Ensure the tools/audit_tools directory is importable
_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT / "tools" / "audit_tools"))

# Stage-0 config loader
sys.path.insert(0, str(_REPO_ROOT / "controllers"))
from config_loader import ConfigLoader  # noqa: E402


class AuditController:
    """
    Wires the Stage-0 configuration system to the audit module registry.
    Supports dry-run mode, dynamic module loading, and artifact routing.
    """

    AUDIT_OUTPUT_DIR = _REPO_ROOT / "AP_SYSTEM_AUDIT"
    REGISTRY_PATH = _REPO_ROOT / "registry" / "audit_registry.json"

    def __init__(self, root_path=None):
        self.root = Path(root_path) if root_path else _REPO_ROOT
        self.cfg_loader = ConfigLoader(str(self.root))
        self.crawl_cfg = self.cfg_loader.load_crawl_config()
        self.sim_cfg = self.cfg_loader.load_simulation_config()
        self.dry_run = self.crawl_cfg.get("crawl_mode") == "dry_run"
        self.registry = self.load_registry()
        self.AUDIT_OUTPUT_DIR.mkdir(exist_ok=True)

    # ── Registry ──────────────────────────────────────────────────────────────

    def load_registry(self):
        with open(self.REGISTRY_PATH) as f:
            return json.load(f)

    # ── Dynamic module loading ─────────────────────────────────────────────────

    def import_module(self, entry):
        """
        Attempt to import an audit module by its file_path.
        Returns (module_object, error_string_or_None).
        """
        file_path = self.root / entry["file_path"]
        spec = importlib.util.spec_from_file_location(entry["stem"], file_path)
        if spec is None:
            return None, f"Cannot create spec for {file_path}"
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            return mod, None
        except Exception as exc:
            return None, str(exc)

    # ── Import validation ─────────────────────────────────────────────────────

    def validate_imports(self):
        """
        Attempt to import every registered audit module.
        Returns (ok_list, error_list).
        """
        ok, errors = [], []
        for entry in self.registry["audits"]:
            mod, err = self.import_module(entry)
            if err:
                errors.append(
                    {
                        "module": entry["module"],
                        "file": entry["file_path"],
                        "error": err,
                    }
                )
            else:
                ok.append(entry["module"])
        return ok, errors

    # ── Audit execution ───────────────────────────────────────────────────────

    def run_audit(self, entry, target):
        """
        Execute a single audit module's entry function against target directory.
        Respects dry_run: logs intent without executing when True.
        """
        if self.dry_run:
            return {
                "module": entry["module"],
                "status": "skipped_dry_run",
                "target": target,
            }

        if entry.get("role") in ("utility", "runner"):
            return {"module": entry["module"], "status": "skipped_non_executable_role"}

        mod, err = self.import_module(entry)
        if err:
            return {"module": entry["module"], "status": "import_error", "error": err}

        fn_name = entry.get("entry_function", "run")
        fn = getattr(mod, fn_name, None)
        if fn is None:
            return {
                "module": entry["module"],
                "status": "entry_function_not_found",
                "fn": fn_name,
            }

        try:
            fn(target)
            return {"module": entry["module"], "status": "ok", "target": target}
        except Exception as exc:
            return {
                "module": entry["module"],
                "status": "runtime_error",
                "error": str(exc),
            }

    def run_all_audits(self, target):
        """
        Execute all audit modules (role == 'audit') against target directory.
        Returns list of result dicts.
        """
        results = []
        for entry in self.registry["audits"]:
            if entry.get("role") == "audit":
                results.append(self.run_audit(entry, target))
        return results

    # ── Reporting ─────────────────────────────────────────────────────────────

    def write_import_errors(self, errors):
        out = self.AUDIT_OUTPUT_DIR / "AUDIT_IMPORT_ERRORS.json"
        with open(out, "w") as f:
            json.dump(
                {
                    "generated": datetime.datetime.utcnow().isoformat() + "Z",
                    "total_errors": len(errors),
                    "errors": errors,
                },
                f,
                indent=2,
            )
        return str(out)

    def write_stage1_report(self, imported_ok, import_errors, validation_status):
        audit_entries = [e for e in self.registry["audits"] if e["role"] == "audit"]
        runner_entries = [e for e in self.registry["audits"] if e["role"] == "runner"]
        utility_entries = [e for e in self.registry["audits"] if e["role"] == "utility"]

        report = {
            "stage": "Audit System Wiring",
            "generated": datetime.datetime.utcnow().isoformat() + "Z",
            "dry_run_mode": self.dry_run,
            "audit_modules_detected": len(self.registry["audits"]),
            "audit_modules_registered": len(self.registry["audits"]),
            "audit_modules_imported": len(imported_ok),
            "audit_modules_failed_import": len(import_errors),
            "audit_count_by_role": {
                "audit": len(audit_entries),
                "runner": len(runner_entries),
                "utility": len(utility_entries),
            },
            "audit_registry_path": str(self.REGISTRY_PATH.relative_to(self.root)),
            "controller_created": "controllers/audit_controller.py",
            "artifact_output_dir": str(self.AUDIT_OUTPUT_DIR),
            "imported_modules": imported_ok,
            "import_errors": import_errors,
            "validation_status": validation_status,
        }

        out = self.AUDIT_OUTPUT_DIR / "AP_STAGE1_AUDIT_SYSTEM_REPORT.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2)
        return str(out)


if __name__ == "__main__":
    controller = AuditController()
    ok, errors = controller.validate_imports()

    if errors:
        controller.write_import_errors(errors)

    status = "PASS" if not errors else "PARTIAL"
    report_path = controller.write_stage1_report(ok, errors, status)

    print(f"Audit modules detected:  {len(controller.registry['audits'])}")
    print(f"Successfully imported:   {len(ok)}")
    print(f"Import errors:           {len(errors)}")
    print(f"Dry-run mode:            {controller.dry_run}")
    print(f"Validation status:       {status}")
    print(f"Report written:          {report_path}")
