"""Archon Prime safety audit script — read-only, generates 3 JSON reports."""
import ast, importlib.util, json, pathlib, sys
from datetime import datetime, timezone

TOOL_BASE  = pathlib.Path("/workspaces/Logos/LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/LOGOS_CORE/Logos_Agent/ARCHON_PRIME/WORKFLOW_TARGET_AUDITS")
INDEX_FILE = TOOL_BASE / "archon_tool_index.json"
OUT_ROOT   = pathlib.Path("/workspaces/Logos/_Dev_Resources/Reports/ARCHON_DIAGNOSTICS")
REPO_ROOT  = pathlib.Path("/workspaces/Logos")

OUT_ROOT.mkdir(parents=True, exist_ok=True)

ARCHON_PATTERNS = [
    "diagnostic","report","analysis","cluster","packet","graph","symbol",
    "architecture","triage","module","ast","dependency","runtime","security",
    "integration","fragment","coverage","cohesion","complexity","coupling",
    "entrypoint","inventory","license","circulation","detection","mapping","mapper",
]

# ── Load index ────────────────────────────────────────────────────────────────
with open(INDEX_FILE) as f:
    idx = json.load(f)
pipeline = idx["archon_pipeline"]

# ── Integrity check ───────────────────────────────────────────────────────────
def check_tool(key, entry):
    result = {
        "stage_key":        key,
        "stage":            entry["stage"],
        "tool":             entry["tool"],
        "path":             entry["path"],
        "execution_entry":  entry.get("execution_entry"),
        "path_exists":      False,
        "import_ok":        False,
        "import_error":     None,
        "entrypoint_ok":    False,
        "entrypoint_error": None,
        "output_routing_ok":False,
        "status":           "FAIL",
        "issues":           [],
    }
    abs_path = TOOL_BASE / entry["path"]

    if not abs_path.exists():
        result["issues"].append(f"File missing: {abs_path}")
        return result
    result["path_exists"] = True

    src = abs_path.read_text(errors="replace")

    if "ARCHON_OUTPUT_ROOT" in src:
        result["output_routing_ok"] = True
    else:
        result["issues"].append("ARCHON_OUTPUT_ROOT not referenced in source")

    entry_fn = entry.get("execution_entry")
    if entry_fn is None:
        result["entrypoint_ok"] = True
    else:
        try:
            tree = ast.parse(src, filename=str(abs_path))
            top_defs = {n.name for n in ast.walk(tree)
                        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
            if entry_fn in top_defs:
                result["entrypoint_ok"] = True
            else:
                result["issues"].append(f"Entry function '{entry_fn}' not found at top-level")
                result["entrypoint_error"] = f"function '{entry_fn}' absent"
        except SyntaxError as e:
            result["issues"].append(f"AST parse error: {e}")
            result["entrypoint_error"] = str(e)

    try:
        spec = importlib.util.spec_from_file_location(f"archon_{key}", abs_path)
        if spec and spec.loader:
            result["import_ok"] = True
        else:
            result["issues"].append("importlib could not create valid spec")
            result["import_error"] = "invalid spec"
    except Exception as e:
        result["issues"].append(f"Import spec error: {e}")
        result["import_error"] = str(e)

    if (result["path_exists"] and result["import_ok"]
            and result["entrypoint_ok"] and result["output_routing_ok"]):
        result["status"] = "PASS"
    else:
        result["status"] = "FAIL"
    return result

tool_results  = [check_tool(k, v) for k, v in pipeline.items()]
total_tools   = len(tool_results)
pass_count    = sum(1 for r in tool_results if r["status"] == "PASS")
fail_count    = sum(1 for r in tool_results if r["status"] == "FAIL")
import_errors = [r for r in tool_results if r["import_error"]]
missing_files = [r for r in tool_results if not r["path_exists"]]
missing_entry = [r for r in tool_results if not r["entrypoint_ok"]]
missing_route = [r for r in tool_results if not r["output_routing_ok"]]

integrity_report = {
    "report_type":    "archon_tool_integrity_report",
    "generated_at":   datetime.now(timezone.utc).isoformat(),
    "index_file":     str(INDEX_FILE),
    "schema_version": idx.get("schema_version"),
    "summary": {
        "total_tools":            total_tools,
        "pass":                   pass_count,
        "fail":                   fail_count,
        "missing_files":          len(missing_files),
        "import_errors":          len(import_errors),
        "missing_entrypoints":    len(missing_entry),
        "missing_output_routing": len(missing_route),
        "overall_status":         "PASS" if fail_count == 0 else "DEGRADED",
    },
    "tools": tool_results,
}
with open(OUT_ROOT / "archon_tool_integrity_report.json", "w") as f:
    json.dump(integrity_report, f, indent=2)
print("OK archon_tool_integrity_report.json")

# ── Root .txt scan ────────────────────────────────────────────────────────────
def ts(epoch):
    return datetime.fromtimestamp(epoch, tz=timezone.utc).isoformat()

txt_files = []
for p in sorted(REPO_ROOT.iterdir()):
    if p.is_file() and p.suffix.lower() == ".txt":
        s = p.stat()
        txt_files.append({
            "filename":           p.name,
            "absolute_path":      str(p.resolve()),
            "file_size_bytes":    s.st_size,
            "created_timestamp":  ts(s.st_ctime),
            "modified_timestamp": ts(s.st_mtime),
        })

txt_inventory = {
    "report_type":     "root_txt_file_inventory",
    "generated_at":    datetime.now(timezone.utc).isoformat(),
    "scan_directory":  str(REPO_ROOT.resolve()),
    "total_txt_files": len(txt_files),
    "files":           txt_files,
}
with open(OUT_ROOT / "root_txt_file_inventory.json", "w") as f:
    json.dump(txt_inventory, f, indent=2)
print(f"OK root_txt_file_inventory.json  ({len(txt_files)} files)")

# ── Archon candidate classification ────────────────────────────────────────────
candidates, non_candidates = [], []
for entry in txt_files:
    matched = [pat for pat in ARCHON_PATTERNS if pat in entry["filename"].lower()]
    rec = {**entry, "matched_patterns": matched, "likely_archon_artifact": bool(matched)}
    (candidates if rec["likely_archon_artifact"] else non_candidates).append(rec)

archon_candidates = {
    "report_type":           "archon_root_txt_candidates",
    "generated_at":          datetime.now(timezone.utc).isoformat(),
    "scan_directory":        str(REPO_ROOT.resolve()),
    "classification_patterns": ARCHON_PATTERNS,
    "summary": {
        "total_txt_files":        len(txt_files),
        "likely_archon_artifacts": len(candidates),
        "non_archon_txt_files":   len(non_candidates),
    },
    "likely_archon_artifacts": candidates,
    "non_archon_txt_files":    non_candidates,
}
with open(OUT_ROOT / "archon_root_txt_candidates.json", "w") as f:
    json.dump(archon_candidates, f, indent=2)
print(f"OK archon_root_txt_candidates.json  ({len(candidates)} candidates)")

# ── Summary ───────────────────────────────────────────────────────────────────
print()
print("=" * 60)
print("  ARCHON PRIME - SAFETY AUDIT SUMMARY")
print("=" * 60)
print(f"  Total tools checked          : {total_tools}")
print(f"  PASS                         : {pass_count}")
print(f"  FAIL                         : {fail_count}")
print(f"  Missing files                : {len(missing_files)}")
print(f"  Import spec errors           : {len(import_errors)}")
print(f"  Missing entrypoints          : {len(missing_entry)}")
print(f"  Missing ARCHON_OUTPUT_ROOT   : {len(missing_route)}")
print(f"  Root .txt files found        : {len(txt_files)}")
print(f"  Likely Archon artifacts      : {len(candidates)}")
print("=" * 60)
if missing_route:
    print("\n  Tools missing ARCHON_OUTPUT_ROOT:")
    for r in missing_route:
        print(f"    * {r['tool']}  ({r['path']})")
if missing_files:
    print("\n  Missing tool files:")
    for r in missing_files:
        print(f"    * {r['path']}")
if missing_entry:
    print("\n  Missing entrypoints:")
    for r in missing_entry:
        print(f"    * {r['tool']}  entry='{r['execution_entry']}'  ({r['entrypoint_error']})")
if candidates:
    print("\n  Likely Archon .txt artifacts at repo root:")
    for c in candidates:
        print(f"    * {c['filename']}  {c['file_size_bytes']} bytes  patterns={c['matched_patterns']}")
print()
print(f"  Reports -> {OUT_ROOT}")
