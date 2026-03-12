import ast
import sys
import json
from pathlib import Path
from typing import Set, Dict, List, Tuple

# Config
ROOTS = [
    Path("STARTUP/START_LOGOS.py"),
    Path("STARTUP/LOGOS_SYSTEM.py"),
]
EXCLUDE_PATTERNS = [
    "TEST", "TEST_SUITE", "demo", "smoke", "__pycache__"
]
REPORT_DIR = Path("_Reports/Phase6_Runtime_CallGraph")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Globals
reachable_modules: Set[str] = set()
adjacency_map: Dict[str, List[str]] = {}
dynamic_import_sites: List[Tuple[str, int]] = []
sys_path_sites: List[Tuple[str, int]] = []
eval_exec_sites: List[Tuple[str, int]] = []
excluded_modules: List[Tuple[str, str]] = []

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
    # Only support absolute imports under LOGOS_SYSTEM
    if mod.startswith("LOGOS_SYSTEM."):
        rel = mod.replace(".", "/") + ".py"
        p = Path(rel)
        if p.exists():
            return p
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
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if (getattr(node.func.value, 'id', None) == 'importlib'):
                    dynamic_import_sites.append((str(path), node.lineno))
            elif isinstance(node.func, ast.Name):
                if node.func.id in ("eval", "exec"):
                    eval_exec_sites.append((str(path), node.lineno))
        elif isinstance(node, ast.Assign):
            # sys.path mutation
            for t in ast.walk(node):
                if isinstance(t, ast.Attribute):
                    if t.attr == "path" and getattr(t.value, 'id', None) == "sys":
                        sys_path_sites.append((str(path), node.lineno))
    return sorted(imports)

def traverse(path: Path, visited: Set[str]):
    if is_excluded(path):
        excluded_modules.append((str(path), "excluded by pattern"))
        return
    modname = module_name_from_path(path)
    if modname in visited:
        return
    visited.add(modname)
    reachable_modules.add(modname)
    imports = scan_file(path)
    adjacency_map[modname] = imports
    for imp in imports:
        imp_path = resolve_import(path, imp)
        if imp_path and imp_path.exists():
            traverse(imp_path, visited)
        else:
            # Not found or not under LOGOS_SYSTEM, skip
            continue

def main():
    visited = set()
    for root in ROOTS:
        if not root.exists():
            print(f"Root not found: {root}", file=sys.stderr)
            sys.exit(1)
        traverse(root, visited)
    # Write artifacts
    with open(REPORT_DIR/"PHASE6_RUNTIME_REACHABLE_MODULES.json", "w", encoding="utf-8") as f:
        json.dump(sorted(reachable_modules), f, indent=2)
    with open(REPORT_DIR/"PHASE6_RUNTIME_ADJACENCY_MAP.json", "w", encoding="utf-8") as f:
        json.dump({k: sorted(v) for k, v in sorted(adjacency_map.items())}, f, indent=2)
    with open(REPORT_DIR/"PHASE6_RUNTIME_DYNAMIC_IMPORT_SITES.json", "w", encoding="utf-8") as f:
        json.dump(sorted(dynamic_import_sites), f, indent=2)
    with open(REPORT_DIR/"PHASE6_RUNTIME_SYS_PATH_SITES.json", "w", encoding="utf-8") as f:
        json.dump(sorted(sys_path_sites), f, indent=2)
    with open(REPORT_DIR/"PHASE6_RUNTIME_EVAL_EXEC_SITES.json", "w", encoding="utf-8") as f:
        json.dump(sorted(eval_exec_sites), f, indent=2)
    with open(REPORT_DIR/"PHASE6_RUNTIME_EXCLUDED_MODULES.json", "w", encoding="utf-8") as f:
        json.dump(sorted(excluded_modules), f, indent=2)

if __name__ == "__main__":
    main()
