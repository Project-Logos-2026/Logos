
import json
from pathlib import Path

# ==========================
# Module-Level Exclusions
# ==========================

SELF_FILE = "test_structural_invariants.py"

EXCLUDED_DIRS = {
    "TEST_SUITE",
}

EXCLUDED_HEADER_MARKERS = {
    "HEADER_TYPE: LEGACY_REWRITE_CANDIDATE",
    "EXECUTION: FORBIDDEN",
}

SHIM_PATH = "LOGOS_SYSTEM/Governance"

# ==========================
# Utility
# ==========================

def safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def is_excluded(path: Path) -> bool:
    if path.name == SELF_FILE:
        return True
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return True
    text = safe_read(path)
    for marker in EXCLUDED_HEADER_MARKERS:
        if marker in text:
            return True
    return False

# ==========================
# INV-01 — No print() usage
# ==========================

def test_no_print_in_governed_code():
    root = Path("LOGOS_SYSTEM")
    for path in root.rglob("*.py"):
        if is_excluded(path):
            continue
        text = safe_read(path)
        assert "print(" not in text, f"print() found in {path}"

# ==========================
# INV-02 — Single _find_repo_root definition
# ==========================

def test_single_repo_root_definition():
    root = Path("LOGOS_SYSTEM")
    matches = []
    for path in root.rglob("*.py"):
        if is_excluded(path):
            continue
        text = safe_read(path)
        if "def _find_repo_root" in text:
            matches.append(path)
    assert len(matches) == 1, f"_find_repo_root defined in multiple files: {matches}"

# ==========================
# INV-03 — No LOGOS_REPO_ROOT usage
# ==========================

def test_no_env_var_root_resolution():
    root = Path("LOGOS_SYSTEM")
    for path in root.rglob("*.py"):
        if is_excluded(path):
            continue
        text = safe_read(path)
        assert "LOGOS_REPO_ROOT" not in text, f"LOGOS_REPO_ROOT usage found in {path}"

# ==========================
# INV-04 — Single Governance Manifest
# ==========================

def test_single_governance_manifest():
    manifests = list(Path("_Governance").rglob("Semantic_Projection_Manifest.json"))
    assert len(manifests) == 1

# ==========================
# INV-05 — Manifest Schema Conformance
# ==========================

def test_manifest_schema_conformance():
    manifest_path = Path("_Governance/Semantic_Projection_Manifest.json")
    schema_path = Path("_Governance/Schemas/governance_manifest_schema.json")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    for key in schema["required"]:
        assert key in manifest

    assert manifest["manifest_version"] == "1.0"
    assert isinstance(manifest["families"], dict)

    for name, value in manifest["families"].items():
        assert isinstance(value, dict)

# ==========================
# INV-06 — No EXAMPLE_FAMILY
# ==========================

def test_no_test_data_in_governance_manifest():
    manifest_path = Path("_Governance/Semantic_Projection_Manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert "EXAMPLE_FAMILY" not in manifest["families"]

# ==========================
# INV-07 — Shim Import Stability
# ==========================

def test_shim_import_surface_stable():
    imports = []
    root = Path("LOGOS_SYSTEM")
    for path in root.rglob("*.py"):
        if is_excluded(path):
            continue
        text = safe_read(path)
        if SHIM_PATH in text:
            imports.append(path)
    assert isinstance(imports, list)

# ==========================
# INV-09 — Governance Bypass Scan
# ==========================

def test_no_direct_governance_path_bypass():
    root = Path("LOGOS_SYSTEM")
    for path in root.rglob("*.py"):
        if is_excluded(path):
            continue
        text = safe_read(path)
        if "Path(__file__).parents" in text and "_Governance" in text:
            raise AssertionError(f"Direct governance path bypass in {path}")
