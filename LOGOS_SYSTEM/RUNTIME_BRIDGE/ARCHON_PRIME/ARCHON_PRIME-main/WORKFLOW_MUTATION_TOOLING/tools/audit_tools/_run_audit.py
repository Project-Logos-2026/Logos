#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-022
# module_name:          _run_audit
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/_run_audit.py
# responsibility:       Inspection module:  run audit
# runtime_stage:        audit
# execution_entry:      main
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
ARCHON_PRIME Mechanical Completeness Audit
PROMPT_013_R1

All output written to /workspaces/ARCHON_PRIME/AP_SYSTEM_AUDIT/Complettion_Audit/
"""

import ast
import datetime
import json
import os
import re
from pathlib import Path

REPO_ROOT = Path("/workspaces/ARCHON_PRIME")
OUTPUT_DIR = REPO_ROOT / "AP_SYSTEM_AUDIT" / "Complettion_Audit"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

step_failures = []


def write_json(path, data):
    path = Path(path)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    # Validate parseable
    json.loads(text)
    path.write_text(text, encoding="utf-8")
    print(f"  [WROTE] {path.name}")


def record_failure(step, message, exc=None):
    record = {"step": step, "message": message}
    if exc:
        record["exception"] = str(exc)
    step_failures.append(record)
    print(f"  [FAIL] {step}: {message}")


def flush_failures():
    write_json(OUTPUT_DIR / "step_failures.json", step_failures)


# ─────────────────────────────────────────────
# STEP 1 — Parse MODULE_INVENTORY.md
# ─────────────────────────────────────────────
def step1_parse_module_inventory():
    print("\n=== STEP 1: Parse MODULE_INVENTORY.md ===")
    source = REPO_ROOT / "tools" / "MODULE_INVENTORY.md"
    if not source.exists():
        record_failure("Step1", f"MODULE_INVENTORY.md not found at {source}")
        return []

    text = source.read_text(encoding="utf-8")
    lines = text.splitlines()

    modules = []
    current_subsystem = None
    i = 0

    # Subsystem pattern: ## SUBSYSTEM N — NAME
    subsystem_re = re.compile(r"^##\s+SUBSYSTEM\s+(\d+)\s+[—\-]+\s+(.+)", re.IGNORECASE)
    # Module header: ### MXX — `filename`  (or ### MXX — filename)
    module_header_re = re.compile(
        r"^###\s+(M\d+)\s+[—\-]+\s+[`\"]?([^\`\"]+)[`\"]?", re.IGNORECASE
    )

    subsystem_name_map = {
        "0": "S0_FOUNDATION",
        "1": "S1_AUDIT_REGENERATION",
        "2": "S2_REPO_ANALYSIS",
        "3": "S3_SIMULATION",
        "4": "S4_CRAWL_PLANNING",
        "5": "S5_MUTATION_OPERATORS",
        "6": "S6_CRAWL_EXECUTION",
        "7": "S7_ERROR_REPAIR",
        "8": "S8_QUARANTINE",
        "9": "S9_ARTIFACT_REPORTING",
        "10": "S10_ORCHESTRATION",
    }

    while i < len(lines):
        line = lines[i]

        # Check for subsystem header
        m = subsystem_re.match(line)
        if m:
            snum = m.group(1)
            current_subsystem = subsystem_name_map.get(snum, f"S{snum}_UNKNOWN")
            i += 1
            continue

        # Check for module header
        m = module_header_re.match(line)
        if m:
            module_id = m.group(1)
            module_name = m.group(2).strip()

            # Parse table rows that follow
            fields = {}
            j = i + 1
            while j < len(lines) and j < i + 20:
                tline = lines[j].strip()
                if tline.startswith("|") and "|" in tline[1:]:
                    parts = [p.strip() for p in tline.split("|")]
                    parts = [p for p in parts if p]
                    if len(parts) >= 2:
                        key = parts[0].replace("**", "").strip()
                        val = parts[1].replace("**", "").strip()
                        # Clean backticks and markdown from value
                        val = val.replace("`", "").strip()
                        fields[key] = val
                elif tline.startswith("#"):
                    break
                j += 1

            path_val = fields.get("Path", "").strip()
            # NOTE: The Path field in MODULE_INVENTORY.md contains the FULL file path
            # (including the filename), NOT just a directory path.
            # e.g. Path = "ARCHON_PRIME/tools/normalization_tools/schema_registry.py"
            # So expected_full_path = path_val as-is.
            # expected_path = parent directory only.
            expected_full_path = path_val
            # Derive parent directory from the full path
            if "/" in path_val:
                expected_path = path_val.rsplit("/", 1)[0] + "/"
            else:
                expected_path = path_val

            blocking_class = fields.get("Class", "UNKNOWN")
            phase = fields.get("Phase", "UNKNOWN")

            if current_subsystem is None:
                current_subsystem = "S_UNKNOWN"

            modules.append(
                {
                    "module_id": module_id,
                    "module_name": module_name,
                    "expected_path": expected_path,
                    "expected_full_path": expected_full_path,
                    "subsystem": current_subsystem,
                    "blocking_class": blocking_class,
                    "phase": phase,
                    "required": True,
                }
            )

        i += 1

    print(f"  Parsed {len(modules)} modules from MODULE_INVENTORY.md")
    if len(modules) < 35:
        record_failure(
            "Step1",
            f"Parsing warning: only {len(modules)} modules parsed (expected ~39). Possible parser error.",
        )

    write_json(OUTPUT_DIR / "spec_module_inventory.json", modules)
    return modules


# ─────────────────────────────────────────────
# STEP 2 — Repo File Inventory
# ─────────────────────────────────────────────
def step2_repo_file_inventory():
    print("\n=== STEP 2: Scan Repo File Inventory ===")
    EXCLUDE_DIRS = {".git", "__pycache__", ".egg-info"}
    EXCLUDE_FILENAMES = {"__init__.py"}

    files = []
    now = datetime.datetime.utcnow().isoformat() + "Z"

    for root, dirs, filenames in os.walk(REPO_ROOT):
        # Prune excluded directories
        dirs[:] = [
            d for d in dirs if d not in EXCLUDE_DIRS and not d.endswith(".egg-info")
        ]
        # Also skip __pycache__ anywhere
        dirs[:] = [d for d in dirs if "__pycache__" not in d]

        for fname in filenames:
            if fname in EXCLUDE_FILENAMES:
                continue
            fpath = Path(root) / fname
            try:
                rel = fpath.relative_to(REPO_ROOT)
            except ValueError:
                continue

            rel_str = str(rel).replace("\\", "/")
            ext = fpath.suffix
            try:
                size = fpath.stat().st_size
            except Exception:
                size = 0

            line_count = None
            if ext in (".py", ".md"):
                try:
                    content = fpath.read_text(encoding="utf-8", errors="replace")
                    line_count = content.count("\n") + 1
                except Exception:
                    line_count = None

            files.append(
                {
                    "relative_path": rel_str,
                    "absolute_path": str(fpath),
                    "filename": fname,
                    "extension": ext,
                    "size_bytes": size,
                    "line_count": line_count,
                }
            )

    total_py = sum(1 for f in files if f["extension"] == ".py")

    inventory = {
        "generated_at": now,
        "repo_root": str(REPO_ROOT) + "/",
        "total_files": len(files),
        "total_python_files": total_py,
        "files": files,
    }

    write_json(OUTPUT_DIR / "repo_file_inventory.json", inventory)
    print(f"  Found {len(files)} files ({total_py} Python)")
    return inventory


# ─────────────────────────────────────────────
# STEP 3 — Config File Presence
# ─────────────────────────────────────────────
def step3_config_file_presence():
    print("\n=== STEP 3: Config File Presence ===")
    configs = [
        {
            "config_file": "configs/crawl_configs/crawl_config.json",
            "blocker_impact": "controller_main.py cannot initialize without this file",
        },
        {
            "config_file": "configs/crawl_configs/routing_table.json",
            "blocker_impact": "artifact_router.py cannot route outputs without this file",
        },
        {
            "config_file": "AP_SYSTEM_CONFIG/logos_targets.yaml",
            "blocker_impact": "target_selector cannot identify crawl targets",
        },
        {
            "config_file": "AP_SYSTEM_CONFIG/ap_config.yaml",
            "blocker_impact": "pipeline_orchestrator cannot validate mutation_allowed flag",
        },
        {
            "config_file": "tools/normalization_tools/header_schema.json",
            "blocker_impact": "header_injector.py cannot operate without this file",
        },
        {
            "config_file": "configs/repair_registry/repair_registry.json",
            "blocker_impact": "repair_router.py cannot classify failures without this file",
        },
    ]

    results = []
    for cfg in configs:
        fpath = REPO_ROOT / cfg["config_file"]
        exists = fpath.exists() and fpath.is_file()
        if exists:
            size = fpath.stat().st_size
            is_empty = size == 0
        else:
            size = None
            is_empty = None

        results.append(
            {
                "config_file": cfg["config_file"],
                "exists": exists,
                "size_bytes": size,
                "is_empty": is_empty,
                "blocker_impact": cfg["blocker_impact"],
            }
        )
        status = "PRESENT" if exists else "MISSING"
        print(f"  {cfg['config_file']}: {status}")

    write_json(OUTPUT_DIR / "config_file_presence.json", results)
    return results


# ─────────────────────────────────────────────
# STEP 4 — Module Presence Verification
# ─────────────────────────────────────────────
def step4_module_presence(spec_modules, file_inventory):
    print("\n=== STEP 4: Module Presence Verification ===")
    # Build lookup structures from repo file inventory
    # filename -> list of relative_paths
    filename_to_paths = {}
    # relative_path set for exact match
    rel_paths = set()

    for f in file_inventory["files"]:
        rel_paths.add(f["relative_path"])
        fn = f["filename"]
        if fn not in filename_to_paths:
            filename_to_paths[fn] = []
        filename_to_paths[fn].append(f["relative_path"])

    def normalize_path(p):
        """Normalize expected_full_path to match relative repo paths."""
        # Strip leading ARCHON_PRIME/ prefix since repo root IS ARCHON_PRIME
        p = p.replace("\\", "/")
        if p.startswith("ARCHON_PRIME/"):
            p = p[len("ARCHON_PRIME/") :]
        return p

    matrix = []
    counts = {"PRESENT_CORRECT": 0, "PRESENT_MISPLACED": 0, "MISSING": 0}

    for mod in spec_modules:
        module_id = mod["module_id"]
        module_name = mod["module_name"]
        expected_full_path = mod["expected_full_path"]

        norm_expected = normalize_path(expected_full_path)

        # First: exact path match
        if norm_expected in rel_paths:
            status = "PRESENT_CORRECT"
            actual_path = norm_expected
        else:
            # Second: filename match anywhere
            matches = filename_to_paths.get(module_name, [])
            # Filter out __init__.py just in case
            matches = [m for m in matches if Path(m).name != "__init__.py"]
            if matches:
                status = "PRESENT_MISPLACED"
                actual_path = matches[0]  # use first found
            else:
                status = "MISSING"
                actual_path = None

        counts[status] += 1
        matrix.append(
            {
                "module_id": module_id,
                "module_name": module_name,
                "expected_full_path": expected_full_path,
                "status": status,
                "actual_path": actual_path,
            }
        )
        print(f"  {module_id} ({module_name}): {status}")

    print(f"\n  Summary: {counts}")
    write_json(OUTPUT_DIR / "module_presence_matrix.json", matrix)
    return matrix


# ─────────────────────────────────────────────
# STEP 5 — Implementation Depth Analysis
# ─────────────────────────────────────────────
def step5_implementation_depth(spec_modules, presence_matrix):
    print("\n=== STEP 5: Implementation Depth Analysis ===")

    # Build map: module_id -> presence record
    presence_by_id = {p["module_id"]: p for p in presence_matrix}

    depth_results = []

    for mod in spec_modules:
        mid = mod["module_id"]
        mname = mod["module_name"]
        pres = presence_by_id.get(mid)

        if not pres or pres["status"] == "MISSING":
            continue

        actual_path = pres["actual_path"]
        if not actual_path:
            continue

        fpath = REPO_ROOT / actual_path

        try:
            content = fpath.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            record_failure("Step5", f"Cannot read {actual_path}", e)
            continue

        lines = content.splitlines()
        line_count = len(lines)

        # Parse AST
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            record_failure("Step5", f"Syntax error in {actual_path}: {e}")
            # Still record what we can
            depth_results.append(
                {
                    "module_id": mid,
                    "module_name": mname,
                    "actual_path": actual_path,
                    "line_count": line_count,
                    "function_count": 0,
                    "class_count": 0,
                    "has_only_pass": False,
                    "has_only_print": False,
                    "has_docstring_only": False,
                    "has_no_output": True,
                    "classification": "SKELETON",
                    "parse_error": str(e),
                }
            )
            continue

        # Count functions and classes
        function_count = sum(
            1
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
        class_count = sum(
            1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        )

        # Analyze function bodies
        all_funcs = [
            node
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]

        def body_is_only_pass(func):
            body = func.body
            # Skip docstring at start
            effective_body = body
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
            ):
                effective_body = body[1:]
            if not effective_body:
                return True
            return all(
                isinstance(stmt, (ast.Pass,))
                or (
                    isinstance(stmt, ast.Expr)
                    and isinstance(stmt.value, ast.Constant)
                    and stmt.value.value is ...
                )
                for stmt in effective_body
            )

        def body_is_only_print(func):
            body = func.body
            effective_body = body
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
            ):
                effective_body = body[1:]
            if not effective_body:
                return False
            has_print = False
            has_other = False
            for stmt in effective_body:
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                    call = stmt.value
                    if isinstance(call.func, ast.Name) and call.func.id == "print":
                        has_print = True
                        continue
                if isinstance(stmt, (ast.Pass,)):
                    continue
                if isinstance(stmt, ast.Return) and stmt.value is None:
                    continue
                has_other = True
            return has_print and not has_other

        def body_is_docstring_only(func):
            body = func.body
            if not body:
                return True
            # docstring is first expr with a constant
            start = 0
            if isinstance(body[0], ast.Expr) and isinstance(
                body[0].value, ast.Constant
            ):
                start = 1
            else:
                return False  # no docstring = not docstring-only
            rest = body[start:]
            if not rest:
                return True
            # rest must be only pass or return None
            return all(
                isinstance(s, ast.Pass)
                or (isinstance(s, ast.Return) and s.value is None)
                for s in rest
            )

        has_only_pass = False
        has_only_print = False
        has_docstring_only = False

        if all_funcs:
            has_only_pass = all(body_is_only_pass(f) for f in all_funcs)
            has_only_print = all(body_is_only_print(f) for f in all_funcs)
            has_docstring_only = all(body_is_docstring_only(f) for f in all_funcs)

        # has_no_output: no open(), json.dump(), write(), logging calls
        output_calls = {"open", "write", "dump", "dumps", "logging"}
        has_output = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                fname = None
                if isinstance(node.func, ast.Name):
                    fname = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    fname = node.func.attr
                if fname in output_calls:
                    has_output = True
                    break
        has_no_output = not has_output

        # Classification (first match wins)
        if line_count < 30 and function_count <= 1 and class_count == 0:
            classification = "SKELETON"
        elif function_count >= 1 and (
            has_only_pass or has_only_print or has_docstring_only
        ):
            classification = "NO_OP"
        elif has_no_output is not False:  # has_no_output == True => no output
            if has_no_output:
                classification = "PARTIAL"
            else:
                classification = "FUNCTIONAL"
        else:
            classification = "FUNCTIONAL"

        # Re-check: FUNCTIONAL requires has logic AND produces output
        # PARTIAL: has logic but has_no_output == True
        # Final pass:
        if classification not in ("SKELETON", "NO_OP"):
            if has_no_output:
                classification = "PARTIAL"
            else:
                classification = "FUNCTIONAL"

        depth_results.append(
            {
                "module_id": mid,
                "module_name": mname,
                "actual_path": actual_path,
                "line_count": line_count,
                "function_count": function_count,
                "class_count": class_count,
                "has_only_pass": has_only_pass,
                "has_only_print": has_only_print,
                "has_docstring_only": has_docstring_only,
                "has_no_output": has_no_output,
                "classification": classification,
            }
        )

        print(
            f"  {mid} ({mname}): {classification} (lines={line_count}, funcs={function_count}, classes={class_count})"
        )

    write_json(OUTPUT_DIR / "module_implementation_depth.json", depth_results)
    return depth_results


# ─────────────────────────────────────────────
# STEP 6 — Subsystem Completion Metrics
# ─────────────────────────────────────────────
def step6_subsystem_metrics(spec_modules, presence_matrix, depth_results):
    print("\n=== STEP 6: Subsystem Completion Metrics ===")

    presence_by_id = {p["module_id"]: p for p in presence_matrix}
    depth_by_id = {d["module_id"]: d for d in depth_results}

    # Group by subsystem
    subsystems = {}
    for mod in spec_modules:
        ss = mod["subsystem"]
        if ss not in subsystems:
            subsystems[ss] = []
        subsystems[ss].append(mod)

    metrics = []
    for ss, mods in sorted(subsystems.items()):
        required = len(mods)
        present = 0
        correct = 0
        misplaced = 0
        missing = 0
        functional = 0
        partial = 0
        noop = 0
        skeleton = 0
        blocking_missing = 0

        for mod in mods:
            mid = mod["module_id"]
            pres = presence_by_id.get(mid, {})
            status = pres.get("status", "MISSING")
            depth = depth_by_id.get(mid, {})
            cls = depth.get("classification", None)

            if status == "PRESENT_CORRECT":
                present += 1
                correct += 1
            elif status == "PRESENT_MISPLACED":
                present += 1
                misplaced += 1
            else:
                missing += 1
                if mod["blocking_class"] == "BLOCKING":
                    blocking_missing += 1

            if cls == "FUNCTIONAL":
                functional += 1
            elif cls == "PARTIAL":
                partial += 1
            elif cls == "NO_OP":
                noop += 1
            elif cls == "SKELETON":
                skeleton += 1

        completion_pct = (
            round((functional / required) * 100, 1) if required > 0 else 0.0
        )

        metrics.append(
            {
                "subsystem": ss,
                "required_modules": required,
                "present_modules": present,
                "correct_path_modules": correct,
                "misplaced_modules": misplaced,
                "missing_modules": missing,
                "functional_modules": functional,
                "partial_modules": partial,
                "noop_modules": noop,
                "skeleton_modules": skeleton,
                "blocking_modules_missing": blocking_missing,
                "completion_percent": completion_pct,
            }
        )

        print(
            f"  {ss}: required={required}, present={present}, functional={functional}, missing={missing}, completion={completion_pct}%"
        )

    write_json(OUTPUT_DIR / "subsystem_completion_metrics.json", metrics)
    return metrics


# ─────────────────────────────────────────────
# STEP 7 — Pipeline Stage Readiness
# ─────────────────────────────────────────────
def step7_pipeline_stage_readiness(presence_matrix, depth_results):
    print("\n=== STEP 7: Pipeline Stage Readiness ===")

    depth_by_name = {d["module_name"]: d for d in depth_results}
    presence_by_name = {}
    for p in presence_matrix:
        name = p["module_name"]
        if name not in presence_by_name:
            presence_by_name[name] = p

    STAGES = [
        {
            "stage_id": "Stage_0",
            "stage_name": "Foundation: Schemas + Config Layer",
            "required_modules": [
                "schema_registry.py",
                "routing_table_loader.py",
                "repair_registry_loader.py",
            ],
        },
        {
            "stage_id": "Stage_1",
            "stage_name": "Pre-Crawl Audit Regeneration Scripts",
            "required_modules": [
                "repo_directory_scanner.py",
                "python_file_collector.py",
                "import_extractor.py",
                "symbol_import_extractor.py",
                "header_schema_scanner.py",
                "governance_contract_scanner.py",
                "runtime_phase_scanner.py",
            ],
        },
        {
            "stage_id": "Stage_2",
            "stage_name": "Repo Analysis Tools",
            "required_modules": [
                "module_index_builder.py",
                "dependency_graph_builder.py",
                "circular_dependency_detector.py",
                "runtime_phase_mapper.py",
                "runtime_boot_sequencer.py",
                "canonical_import_registry_builder.py",
            ],
        },
        {
            "stage_id": "Stage_3",
            "stage_name": "Mutation Operators (Isolated)",
            "required_modules": ["header_injector.py", "import_rewriter.py"],
        },
        {
            "stage_id": "Stage_4",
            "stage_name": "Validation Pipeline + Syntax Tools",
            "required_modules": [
                "syntax_validator.py",
                "governance_validator.py",
                "phase_validator.py",
            ],
        },
        {
            "stage_id": "Stage_5",
            "stage_name": "Simulation Layer",
            "required_modules": [
                "repo_simulator.py",
                "runtime_simulator.py",
                "import_simulator.py",
                "crawl_planner.py",
                "execution_graph_builder.py",
            ],
        },
        {
            "stage_id": "Stage_6",
            "stage_name": "Crawl Executor + Processing Pipeline",
            "required_modules": [
                "module_processor.py",
                "crawl_executor.py",
                "crawl_monitor.py",
            ],
        },
        {
            "stage_id": "Stage_7",
            "stage_name": "Error Classification + Repair + Quarantine",
            "required_modules": [
                "error_classifier.py",
                "repair_router.py",
                "repair_executor.py",
                "quarantine_manager.py",
            ],
        },
        {
            "stage_id": "Stage_8",
            "stage_name": "Artifact Routing + Reporting + Commit",
            "required_modules": [
                "artifact_router.py",
                "report_generator.py",
                "commit_finalizer.py",
            ],
        },
        {
            "stage_id": "Stage_9",
            "stage_name": "Orchestration + Controller",
            "required_modules": ["task_router.py", "controller_main.py"],
        },
    ]

    readiness_list = []
    for stage in STAGES:
        required = stage["required_modules"]
        present_list = []
        missing_list = []
        all_functional = True

        for mname in required:
            pres = presence_by_name.get(mname)
            if pres and pres["status"] in ("PRESENT_CORRECT", "PRESENT_MISPLACED"):
                present_list.append(mname)
                depth = depth_by_name.get(mname)
                if not depth or depth.get("classification") != "FUNCTIONAL":
                    all_functional = False
            else:
                missing_list.append(mname)
                all_functional = False

        validation_gate = all_functional and len(missing_list) == 0

        # Determine readiness_status
        if validation_gate:
            readiness_status = "READY"
        elif len(missing_list) == 0 and len(present_list) > 0:
            readiness_status = "PARTIAL"
        elif len(missing_list) >= len(required) // 2:
            readiness_status = "NOT_IMPLEMENTED"
        else:
            readiness_status = "PARTIAL"

        entry = {
            "stage_id": stage["stage_id"],
            "stage_name": stage["stage_name"],
            "required_modules": required,
            "modules_present": present_list,
            "modules_missing": missing_list,
            "validation_gate_passable": validation_gate,
            "readiness_status": readiness_status,
        }
        readiness_list.append(entry)
        print(f"  {stage['stage_id']} ({stage['stage_name']}): {readiness_status}")

    write_json(OUTPUT_DIR / "pipeline_stage_readiness.json", readiness_list)
    return readiness_list


# ─────────────────────────────────────────────
# STEP 8 — Prior Audit Claim Verification
# ─────────────────────────────────────────────
def step8_prior_audit_verification(presence_matrix, depth_results, config_presence):
    print("\n=== STEP 8: Prior Audit Claim Verification ===")

    gaps_path = REPO_ROOT / "AP_SYSTEM_AUDIT" / "AP_AUDIT_GAPS.json"
    if not gaps_path.exists():
        record_failure("Step8", f"AP_AUDIT_GAPS.json not found at {gaps_path}")
        write_json(
            OUTPUT_DIR / "prior_audit_verification.json",
            {"error": "AP_AUDIT_GAPS.json not found"},
        )
        return {}

    gaps_data = json.loads(gaps_path.read_text(encoding="utf-8"))

    prior_score = gaps_data.get("logos_readiness_score", "N/A")
    prior_grade = gaps_data.get("readiness_grade", "N/A")

    gaps = gaps_data.get("gaps", {})
    missing_modules = gaps.get("missing_modules", [])
    partial_modules = gaps.get("partial_modules", [])
    logos_blockers = gaps.get("logos_readiness_blockers", [])

    # Build lookups
    presence_by_name = {}
    for p in presence_matrix:
        key = p["module_name"]
        if key not in presence_by_name:
            presence_by_name[key] = p

    # Also build path-based lookup for misplaced checks
    _presence_by_relpath = {
        p["actual_path"]: p for p in presence_matrix if p["actual_path"]
    }
    depth_by_path = {}
    for d in depth_results:
        depth_by_path[d["actual_path"]] = d

    # Verify missing_module claims
    missing_claims = []
    for claim in missing_modules:
        location = claim.get("location", "")
        expected = claim.get("expected", "")

        # Try to find a module matching this location/claim
        # location is like "crawler/pipeline/" — find any module with status
        matched = None
        matched_status = None
        for p in presence_matrix:
            efp = p["expected_full_path"]
            norm = efp.replace("ARCHON_PRIME/", "").replace("\\", "/")
            if location.rstrip("/") in norm:
                matched = p
                matched_status = p["status"]
                break

        if matched is None:
            # Search filename-based
            verified = "CONFIRMED"
            evidence = (
                f"No module found matching location '{location}' — claim CONFIRMED"
            )
        elif matched_status == "MISSING":
            verified = "CONFIRMED"
            evidence = f"{matched['module_name']} status=MISSING at {matched['expected_full_path']}"
        elif matched_status == "PRESENT_CORRECT":
            verified = "REFUTED"
            evidence = (
                f"{matched['module_name']} PRESENT_CORRECT at {matched['actual_path']}"
            )
        else:
            verified = "PARTIAL — file exists but misplaced"
            evidence = f"{matched['module_name']} PRESENT_MISPLACED at {matched['actual_path']}"

        missing_claims.append(
            {
                "claim_location": location,
                "claim_expected": expected,
                "verified_status": verified,
                "evidence": evidence,
            }
        )

    # Verify partial_module claims
    partial_claims = []
    for claim in partial_modules:
        module_path = claim.get("module", "")
        issue = claim.get("issue", "")

        # Extract basename
        mname = Path(module_path).name

        depth = None
        # Try by path
        for d in depth_results:
            if d["actual_path"] and (
                module_path in d["actual_path"] or d["actual_path"] in module_path
            ):
                depth = d
                break
        if not depth:
            for d in depth_results:
                if d["module_name"] == mname:
                    depth = d
                    break

        if depth is None:
            # Module may be MISSING
            pres = None
            for p in presence_matrix:
                if p["module_name"] == mname:
                    pres = p
                    break
            if pres and pres["status"] == "MISSING":
                verified = "CONFIRMED"
                evidence = f"{mname}: MISSING from repo — cannot be partial if absent"
            else:
                verified = "CONFIRMED"
                evidence = f"{mname}: not found in depth analysis — SKELETON or MISSING"
        else:
            cls = depth["classification"]
            if cls in ("SKELETON", "NO_OP"):
                verified = "CONFIRMED"
                evidence = f"line_count: {depth['line_count']}, classification: {cls}, has_only_print: {depth['has_only_print']}"
            elif cls == "FUNCTIONAL":
                verified = "REFUTED"
                evidence = f"classification: FUNCTIONAL, line_count: {depth['line_count']}, has_no_output: {depth['has_no_output']}"
            else:
                verified = "PARTIAL — exists but incomplete"
                evidence = f"classification: {cls}, line_count: {depth['line_count']}"

        partial_claims.append(
            {
                "claim_module": module_path,
                "claim_issue": issue,
                "verified_status": verified,
                "evidence": evidence,
            }
        )

    # Verify logos_readiness_blockers
    blocker_claims = []
    config_by_key = {}
    for c in config_presence:
        config_by_key[c["config_file"]] = c

    for blocker in logos_blockers:
        b_lower = blocker.lower()

        if "logos_targets.yaml" in b_lower or "target configuration" in b_lower:
            cfg = config_by_key.get("AP_SYSTEM_CONFIG/logos_targets.yaml", {})
            if not cfg.get("exists", False):
                verified = "CONFIRMED"
                evidence = (
                    "logos_targets.yaml: exists=false in config_file_presence.json"
                )
            else:
                verified = "REFUTED"
                evidence = "logos_targets.yaml found"
        elif "ap_config.yaml" in b_lower:
            cfg = config_by_key.get("AP_SYSTEM_CONFIG/ap_config.yaml", {})
            if not cfg.get("exists", False):
                verified = "CONFIRMED"
                evidence = "ap_config.yaml: exists=false in config_file_presence.json"
            else:
                verified = "REFUTED"
                evidence = "ap_config.yaml found"
        elif "end-to-end pipeline" in b_lower or "pipeline runner" in b_lower:
            # Check controller_main.py
            ctrl = None
            for p in presence_matrix:
                if p["module_name"] == "controller_main.py":
                    ctrl = p
                    break
            if ctrl and ctrl["status"] in ("PRESENT_CORRECT", "PRESENT_MISPLACED"):
                depth = None
                for d in depth_results:
                    if d["module_name"] == "controller_main.py":
                        depth = d
                        break
                if depth and depth["classification"] == "FUNCTIONAL":
                    verified = "REFUTED"
                    evidence = "controller_main.py FUNCTIONAL"
                else:
                    cls = depth["classification"] if depth else "MISSING"
                    verified = "CONFIRMED"
                    evidence = (
                        f"controller_main.py classification: {cls} — not end-to-end"
                    )
            else:
                verified = "CONFIRMED"
                evidence = "controller_main.py MISSING from repo"
        elif "repair" in b_lower:
            # Check repair modules
            repair_present = [
                p
                for p in presence_matrix
                if "repair" in p["module_name"] and p["status"] != "MISSING"
            ]
            if not repair_present:
                verified = "CONFIRMED"
                evidence = "No repair modules present in repo"
            else:
                functional_repair = [
                    d
                    for d in depth_results
                    if "repair" in d["module_name"]
                    and d["classification"] == "FUNCTIONAL"
                ]
                if not functional_repair:
                    verified = "CONFIRMED"
                    evidence = f"Repair modules present but none FUNCTIONAL: {[p['module_name'] for p in repair_present]}"
                else:
                    verified = "REFUTED"
                    evidence = f"Functional repair modules: {[d['module_name'] for d in functional_repair]}"
        elif "simulation" in b_lower:
            sim_present = [
                p
                for p in presence_matrix
                if "simulator" in p["module_name"] and p["status"] != "MISSING"
            ]
            functional_sim = [
                d
                for d in depth_results
                if "simulator" in d["module_name"]
                and d["classification"] == "FUNCTIONAL"
            ]
            if not functional_sim:
                verified = "CONFIRMED"
                evidence = f"Simulation modules status: present={[p['module_name'] for p in sim_present]}, none FUNCTIONAL"
            else:
                verified = "REFUTED"
                evidence = f"Functional simulators: {[d['module_name'] for d in functional_sim]}"
        elif "crawler" in b_lower and "configurable" in b_lower:
            crawl_exec = None
            for p in presence_matrix:
                if p["module_name"] in ("crawl_executor.py", "crawl_engine.py"):
                    crawl_exec = p
                    break
            if crawl_exec and crawl_exec["status"] != "MISSING":
                depth = next(
                    (
                        d
                        for d in depth_results
                        if d["module_name"] == crawl_exec["module_name"]
                    ),
                    None,
                )
                cls = depth["classification"] if depth else "SKELETON"
                if cls == "FUNCTIONAL":
                    verified = "REFUTED"
                    evidence = f"{crawl_exec['module_name']}: FUNCTIONAL"
                else:
                    verified = "CONFIRMED"
                    evidence = f"{crawl_exec['module_name']}: classification={cls}"
            else:
                verified = "CONFIRMED"
                evidence = "crawl_executor.py MISSING"
        else:
            verified = "UNVERIFIABLE"
            evidence = f"Claim '{blocker}' — no direct mapping to audit artifact"

        blocker_claims.append(
            {
                "blocker": blocker,
                "verified_status": verified,
                "evidence": evidence,
            }
        )

    result = {
        "prior_audit_score": prior_score,
        "prior_audit_grade": prior_grade,
        "missing_module_claims": missing_claims,
        "partial_module_claims": partial_claims,
        "readiness_blocker_claims": blocker_claims,
    }

    write_json(OUTPUT_DIR / "prior_audit_verification.json", result)
    return result


# ─────────────────────────────────────────────
# STEP 9 — Global Completion Score
# ─────────────────────────────────────────────
def step9_completion_score(subsystem_metrics, config_presence):
    print("\n=== STEP 9: Global Completion Score ===")

    now = datetime.datetime.utcnow().isoformat() + "Z"

    total_required = sum(m["required_modules"] for m in subsystem_metrics)
    total_present = sum(m["present_modules"] for m in subsystem_metrics)
    total_functional = sum(m["functional_modules"] for m in subsystem_metrics)
    total_skeleton_noop = sum(
        m["skeleton_modules"] + m["noop_modules"] for m in subsystem_metrics
    )
    total_missing = sum(m["missing_modules"] for m in subsystem_metrics)
    blocking_gaps = sum(m["blocking_modules_missing"] for m in subsystem_metrics)
    config_files_missing = sum(1 for c in config_presence if not c["exists"])

    completion_score = (
        round((total_functional / total_required) * 100, 1)
        if total_required > 0
        else 0.0
    )

    # Grade
    if completion_score >= 90:
        grade = "A"
    elif completion_score >= 75:
        grade = "B"
    elif completion_score >= 60:
        grade = "C"
    elif completion_score >= 40:
        grade = "D"
    else:
        grade = "F"

    prior_score = 38.0
    delta = round(completion_score - prior_score, 1)

    score = {
        "generated_at": now,
        "total_required_modules": total_required,
        "total_present_modules": total_present,
        "total_functional_modules": total_functional,
        "total_skeleton_or_noop": total_skeleton_noop,
        "total_missing_modules": total_missing,
        "blocking_gaps": blocking_gaps,
        "config_files_missing": config_files_missing,
        "completion_score": completion_score,
        "completion_grade": grade,
        "prior_audit_score": prior_score,
        "delta_from_prior_audit": delta,
    }

    write_json(OUTPUT_DIR / "repo_completion_score.json", score)
    print(f"\n  Completion Score: {completion_score}% (Grade: {grade})")
    print(f"  Prior Audit: {prior_score}%, Delta: {delta:+.1f}%")
    print(
        f"  Total Required: {total_required}, Present: {total_present}, Functional: {total_functional}, Missing: {total_missing}"
    )
    return score


# ─────────────────────────────────────────────
# STEP 10 — Final Mechanical Audit Report
# ─────────────────────────────────────────────
def step10_final_report(
    config_presence,
    presence_matrix,
    depth_results,
    subsystem_metrics,
    stage_readiness,
    prior_verification,
    completion_score,
):
    print("\n=== STEP 10: Final Mechanical Audit Report ===")

    now = datetime.datetime.utcnow().isoformat() + "Z"

    lines = []
    lines.append("# ARCHON_PRIME — Mechanical Completeness Audit Report")
    lines.append(f"Generated: {now}")
    lines.append("Audit Version: PROMPT_013_R1")
    lines.append("")

    # ── Section 1: Config File Presence ──
    lines.append("## 1. Config File Presence")
    lines.append("")
    lines.append("| config_file | exists | size_bytes | blocker_impact |")
    lines.append("|-------------|--------|------------|----------------|")
    for c in config_presence:
        lines.append(
            f"| {c['config_file']} | {c['exists']} | {c['size_bytes']} | {c['blocker_impact']} |"
        )
    lines.append("")

    # ── Section 2: Module Presence Summary ──
    lines.append("## 2. Module Presence Summary")
    lines.append("")
    correct = sum(1 for p in presence_matrix if p["status"] == "PRESENT_CORRECT")
    misplaced = sum(1 for p in presence_matrix if p["status"] == "PRESENT_MISPLACED")
    missing_count = sum(1 for p in presence_matrix if p["status"] == "MISSING")
    lines.append(f"- **PRESENT_CORRECT**: {correct}")
    lines.append(f"- **PRESENT_MISPLACED**: {misplaced}")
    lines.append(f"- **MISSING**: {missing_count}")
    lines.append("")

    # Build blocking class lookup from spec
    spec_path = OUTPUT_DIR / "spec_module_inventory.json"
    spec_data = json.loads(spec_path.read_text()) if spec_path.exists() else []
    blocking_by_id = {
        m["module_id"]: m.get("blocking_class", "UNKNOWN") for m in spec_data
    }

    missing_mods = [p for p in presence_matrix if p["status"] == "MISSING"]
    if missing_mods:
        lines.append("### Missing Modules")
        lines.append("")
        lines.append(
            "| module_id | module_name | expected_full_path | blocking_class |"
        )
        lines.append("|-----------|-------------|-------------------|----------------|")
        for m in missing_mods:
            bc = blocking_by_id.get(m["module_id"], "UNKNOWN")
            lines.append(
                f"| {m['module_id']} | {m['module_name']} | {m['expected_full_path']} | {bc} |"
            )
    lines.append("")

    # ── Section 3: Misplaced Modules ──
    lines.append("## 3. Misplaced Modules")
    lines.append("")
    misplaced_mods = [p for p in presence_matrix if p["status"] == "PRESENT_MISPLACED"]
    if misplaced_mods:
        lines.append("| module_id | module_name | expected_path | actual_path |")
        lines.append("|-----------|-------------|--------------|------------|")
        spec_by_id = {m["module_id"]: m for m in spec_data}
        for m in misplaced_mods:
            spec = spec_by_id.get(m["module_id"], {})
            exp = spec.get("expected_path", m["expected_full_path"])
            lines.append(
                f"| {m['module_id']} | {m['module_name']} | {exp} | {m['actual_path']} |"
            )
    else:
        lines.append("_No misplaced modules detected._")
    lines.append("")

    # ── Section 4: Skeleton and No-Op Modules ──
    lines.append("## 4. Skeleton and No-Op Modules")
    lines.append("")
    degraded = [
        d for d in depth_results if d["classification"] in ("SKELETON", "NO_OP")
    ]
    if degraded:
        lines.append("| module_id | module_name | line_count | classification |")
        lines.append("|-----------|-------------|------------|----------------|")
        for d in degraded:
            lines.append(
                f"| {d['module_id']} | {d['module_name']} | {d['line_count']} | {d['classification']} |"
            )
    else:
        lines.append("_No skeleton or no-op modules detected._")
    lines.append("")

    # ── Section 5: Subsystem Completion Table ──
    lines.append("## 5. Subsystem Completion Table")
    lines.append("")
    lines.append(
        "| subsystem | required | present | functional | missing | blocking_missing | completion_pct |"
    )
    lines.append(
        "|-----------|----------|---------|------------|---------|-----------------|----------------|"
    )
    for m in subsystem_metrics:
        lines.append(
            f"| {m['subsystem']} | {m['required_modules']} | {m['present_modules']} | "
            f"{m['functional_modules']} | {m['missing_modules']} | "
            f"{m['blocking_modules_missing']} | {m['completion_percent']}% |"
        )
    lines.append("")

    # ── Section 6: Pipeline Stage Readiness ──
    lines.append("## 6. Pipeline Stage Readiness Table")
    lines.append("")
    lines.append(
        "| stage | stage_name | readiness_status | validation_gate_passable | missing_modules |"
    )
    lines.append(
        "|-------|------------|-----------------|------------------------|----------------|"
    )
    for s in stage_readiness:
        missing_str = ", ".join(s["modules_missing"]) if s["modules_missing"] else "—"
        lines.append(
            f"| {s['stage_id']} | {s['stage_name']} | {s['readiness_status']} | "
            f"{s['validation_gate_passable']} | {missing_str} |"
        )
    lines.append("")

    # ── Section 7: Prior Audit Claim Verification ──
    lines.append("## 7. Prior Audit Claim Verification")
    lines.append("")
    lines.append("| claim_type | claim | verified_status | evidence |")
    lines.append("|------------|-------|----------------|----------|")

    for c in prior_verification.get("missing_module_claims", []):
        claim_text = f"{c['claim_location']} — {c['claim_expected']}"
        lines.append(
            f"| missing_module | {claim_text} | {c['verified_status']} | {c['evidence']} |"
        )

    for c in prior_verification.get("partial_module_claims", []):
        lines.append(
            f"| partial_module | {c['claim_module']}: {c['claim_issue'][:60]} | {c['verified_status']} | {c['evidence']} |"
        )

    for c in prior_verification.get("readiness_blocker_claims", []):
        lines.append(
            f"| readiness_blocker | {c['blocker']} | {c['verified_status']} | {c['evidence']} |"
        )

    lines.append("")

    # ── Section 8: Global Completion Score ──
    lines.append("## 8. Global Completion Score")
    lines.append("")
    cs = completion_score
    lines.append(
        f"- **completion_score**: {cs['completion_score']}% (Grade: {cs['completion_grade']})"
    )
    lines.append(f"- **prior_audit_score**: {cs['prior_audit_score']}%")
    lines.append(f"- **delta**: {cs['delta_from_prior_audit']:+.1f}%")
    lines.append(f"- **total_required_modules**: {cs['total_required_modules']}")
    lines.append(f"- **total_present_modules**: {cs['total_present_modules']}")
    lines.append(f"- **total_functional_modules**: {cs['total_functional_modules']}")
    lines.append(f"- **total_missing_modules**: {cs['total_missing_modules']}")
    lines.append(f"- **blocking_gaps**: {cs['blocking_gaps']}")
    lines.append(f"- **config_files_missing**: {cs['config_files_missing']}")
    lines.append("")

    delta = cs["delta_from_prior_audit"]
    score = cs["completion_score"]
    prior = cs["prior_audit_score"]

    if abs(delta) <= 5:
        verdict = "CONFIRMED"
        verdict_detail = (
            f"Completion score {score}% is within ±5% of prior audit claim {prior}%."
        )
    elif score > prior + 5:
        verdict = "REFUTED"
        verdict_detail = (
            f"Completion score {score}% materially exceeds prior audit claim {prior}%."
        )
    else:
        verdict = "PARTIALLY_CONFIRMED"
        verdict_detail = (
            f"Completion score {score}% differs from prior audit claim {prior}%."
        )

    lines.append(f"**Verdict vs Prior Audit**: {verdict}")
    lines.append(f"_{verdict_detail}_")
    lines.append("")

    report_path = OUTPUT_DIR / "ap_repo_mechanical_audit_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print("  [WROTE] ap_repo_mechanical_audit_report.md")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print(f"\n{'='*60}")
    print("ARCHON_PRIME Mechanical Completeness Audit")
    print(f"{'='*60}")
    print(f"Output: {OUTPUT_DIR}")

    try:
        spec_modules = step1_parse_module_inventory()
    except Exception as e:
        record_failure("Step1", "Fatal error", e)
        spec_modules = []

    try:
        file_inventory = step2_repo_file_inventory()
    except Exception as e:
        record_failure("Step2", "Fatal error", e)
        file_inventory = {"files": []}

    try:
        config_presence = step3_config_file_presence()
    except Exception as e:
        record_failure("Step3", "Fatal error", e)
        config_presence = []

    try:
        presence_matrix = step4_module_presence(spec_modules, file_inventory)
    except Exception as e:
        record_failure("Step4", "Fatal error", e)
        presence_matrix = []

    try:
        depth_results = step5_implementation_depth(spec_modules, presence_matrix)
    except Exception as e:
        record_failure("Step5", "Fatal error", e)
        depth_results = []

    try:
        subsystem_metrics = step6_subsystem_metrics(
            spec_modules, presence_matrix, depth_results
        )
    except Exception as e:
        record_failure("Step6", "Fatal error", e)
        subsystem_metrics = []

    try:
        stage_readiness = step7_pipeline_stage_readiness(presence_matrix, depth_results)
    except Exception as e:
        record_failure("Step7", "Fatal error", e)
        stage_readiness = []

    try:
        prior_verification = step8_prior_audit_verification(
            presence_matrix, depth_results, config_presence
        )
    except Exception as e:
        record_failure("Step8", "Fatal error", e)
        prior_verification = {}

    try:
        score = step9_completion_score(subsystem_metrics, config_presence)
    except Exception as e:
        record_failure("Step9", "Fatal error", e)
        score = {
            "completion_score": 0,
            "completion_grade": "F",
            "prior_audit_score": 38.0,
            "delta_from_prior_audit": -38.0,
        }

    try:
        step10_final_report(
            config_presence,
            presence_matrix,
            depth_results,
            subsystem_metrics,
            stage_readiness,
            prior_verification,
            score,
        )
    except Exception as e:
        record_failure("Step10", "Fatal error", e)

    flush_failures()

    print(f"\n{'='*60}")
    print("VALIDATION CHECKLIST")
    print(f"{'='*60}")
    required_files = [
        "spec_module_inventory.json",
        "repo_file_inventory.json",
        "config_file_presence.json",
        "module_presence_matrix.json",
        "module_implementation_depth.json",
        "subsystem_completion_metrics.json",
        "pipeline_stage_readiness.json",
        "prior_audit_verification.json",
        "repo_completion_score.json",
        "ap_repo_mechanical_audit_report.md",
        "step_failures.json",
    ]
    all_present = True
    for fname in required_files:
        fpath = OUTPUT_DIR / fname
        exists = fpath.exists() and fpath.stat().st_size > 0
        status = "✓" if exists else "✗"
        if not exists:
            all_present = False
        print(f"  [{status}] {fname}")

    print("")
    if step_failures:
        print(f"EXIT STATUS: PARTIAL ({len(step_failures)} step failure(s) recorded)")
    elif all_present:
        print("EXIT STATUS: SUCCESS — all 11 artifacts produced, no step failures")
    else:
        print("EXIT STATUS: FAILURE — missing artifacts")


if __name__ == "__main__":
    main()
