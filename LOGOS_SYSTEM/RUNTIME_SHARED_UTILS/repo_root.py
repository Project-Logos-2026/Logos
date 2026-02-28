from pathlib import Path

def _find_repo_root() -> Path:
    """
    Walk upward from this file's location to find the repo root containing _Governance/Semantic_Projection_Manifest.json.
    Deterministic regardless of cwd. No environment variable override.
    Raises ValueError if not found.
    Returns: Path to repo root.
    """
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        sentinel = parent / "_Governance" / "Semantic_Projection_Manifest.json"
        if sentinel.is_file():
            return parent
    raise ValueError("Repository root with _Governance/Semantic_Projection_Manifest.json not found")
