import ast
import sys
import json
from pathlib import Path
from typing import Set, Dict, List, Tuple

ROOTS = [
    Path("STARTUP/START_LOGOS.py"),
    Path("STARTUP/LOGOS_SYSTEM.py"),
]
INCLUDE_ROOT = Path("LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE")
EXCLUDE_PATTERNS = [
    "RUNTIME_OPPERATIONS_CORE", "DRAC", "Radial_Genesis_Engine", "TEST", "test_", "Tests", "cli", "dev", "harness"
]
REPORT_DIR = Path("_Reports/Phase6_Runtime_CallGraph")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

reachable_modules: Set[str] = set()
call_graph: Dict[str, List[str]] = {}
load_order: List[str] = []
boundaries: List[Dict] = []
hygiene_violations: List[Dict] = []

visited: Set[str] = set()
load_stack: List[str] = []

# Utility

def is_excluded(path: Path) -> bool:
    p = str(path)
    for pat in EXCLUDE_PATTERNS:
        if pat in p:
            return True
    return False

def module_name_from_path(path: Path) -> str:
    rel = path.with_suffix("").as_posix()
    return rel

def resolve_import(base: Path, mod: str) -> Path:
    if mod.startswith("LOGOS_SYSTEM."):
        rel = mod.replace(".", "/") + ".py"
        p = Path(rel)
        if p.exists():
            return p
    elif mod == "STARTUP.LOGOS_SYSTEM":
        return Path("STARTUP/LOGOS_SYSTEM.py")
    elif mod == "STARTUP.START_LOGOS":
        return Path("STARTUP/START_LOGOS.py")
    return None

def scan_file(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        tree = ast.parse(src, filename=str(path))
    except Exception as e:
        print(f"Parse error: {path}: {e}", file=sys.stderr)
        sys.exit(1)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.add(n.name)
                if is_excluded(Path(n.name.replace('.', '/') + '.py')):
                    boundaries.append({"from": str(path), "to": n.name, "type": "excluded_import"})
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
                if is_excluded(Path(node.module.replace('.', '/') + '.py')):
                    boundaries.append({"from": str(path), "to": node.module, "type": "excluded_import"})
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if (getattr(node.func.value, 'id', None) == 'importlib'):
                    hygiene_violations.append({"file": str(path), "line": node.lineno, "type": "importlib_usage"})
            elif isinstance(node.func, ast.Name):
                if node.func.id in ("eval", "exec"):
                    hygiene_violations.append({"file": str(path), "line": node.lineno, "type": node.func.id})
        elif isinstance(node, ast.Assign):
            for t in ast.walk(node):
                if isinstance(t, ast.Attribute):
                    if t.attr == "path" and getattr(t.value, 'id', None) == "sys":
                        hygiene_violations.append({"file": str(path), "line": node.lineno, "type": "sys_path_mutation"})
    return sorted(imports)

def traverse(path: Path, visited: Set[str], stack: List[str]):
    if is_excluded(path):
        return
    modname = module_name_from_path(path)
    if modname in visited:
        return
    visited.add(modname)
    reachable_modules.add(modname)
    stack.append(modname)
    imports = scan_file(path)
    call_graph[modname] = []
    for imp in imports:
        imp_path = resolve_import(path, imp)
        if imp_path and imp_path.exists() and not is_excluded(imp_path):
            call_graph[modname].append(module_name_from_path(imp_path))
            traverse(imp_path, visited, stack)
        elif imp_path and is_excluded(imp_path):
            boundaries.append({"from": modname, "to": imp, "type": "excluded_import"})
    stack.pop()
    if modname not in load_order:
        load_order.append(modname)

def main():
    for root in ROOTS:
        if not root.exists():
            print(f"Root not found: {root}", file=sys.stderr)
            sys.exit(1)
        traverse(root, visited, load_stack)
    # Write artifacts
    with open(REPORT_DIR/"PHASE6C_EXECUTION_REACHABLE_MODULES.json", "w", encoding="utf-8") as f:
        json.dump(sorted(reachable_modules), f, indent=2)
    with open(REPORT_DIR/"PHASE6C_EXECUTION_CALL_GRAPH.json", "w", encoding="utf-8") as f:
        json.dump({k: sorted(v) for k, v in sorted(call_graph.items())}, f, indent=2)
    with open(REPORT_DIR/"PHASE6C_EXECUTION_MODULE_LOAD_ORDER.json", "w", encoding="utf-8") as f:
        json.dump(load_order, f, indent=2)
    with open(REPORT_DIR/"PHASE6C_EXECUTION_BOUNDARIES.json", "w", encoding="utf-8") as f:
        json.dump(boundaries, f, indent=2)
    with open(REPORT_DIR/"PHASE6C_EXECUTION_HYGIENE_REPORT.json", "w", encoding="utf-8") as f:
        json.dump(hygiene_violations, f, indent=2)
    # Fail closed on hygiene violation
    if hygiene_violations:
        print("Hygiene violation detected.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
