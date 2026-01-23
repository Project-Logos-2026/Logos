import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "Documentation/Header_Catalog_Module.json"

def load_catalog():
    return json.loads(CATALOG.read_text())


def build_header(meta: dict) -> str:
    lines = ["# MODULE_META:"]
    for key, value in meta.items():
        if isinstance(value, list):
            lines.append(f"#   {key}: [{', '.join(value)}]")
        else:
            lines.append(f"#   {key}: {value}")
    return "\n".join(lines) + "\n\n"


def inject_header(file_path: Path, meta: dict, dry_run: bool):
    content = file_path.read_text()
    header = build_header(meta)

    if content.startswith("# MODULE_META:"):
        raise RuntimeError(f"Header already exists: {file_path}")

    if dry_run:
        print(f"[DRY-RUN] Would inject header into {file_path}")
        return

    file_path.write_text(header + content)
    print(f"[APPLIED] Header injected into {file_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: inject_module_headers.py <module_id> <file_path> [--apply]")
        sys.exit(1)

    module_id = sys.argv[1]
    file_path = Path(sys.argv[2])
    apply_mode = "--apply" in sys.argv

    catalog = load_catalog()
    modules = catalog.get("modules", {})

    if module_id not in modules:
        raise KeyError(f"Module ID not found in catalog: {module_id}")

    inject_header(file_path, modules[module_id], dry_run=not apply_mode)


if __name__ == "__main__":
    main()
