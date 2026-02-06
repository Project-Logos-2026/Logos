"""External library importer stub (deny-by-default)."""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional


class ExternalLibraryImporter:
    """Records external libraries and exposes them only when explicitly allowed."""

    def __init__(self) -> None:
        self._registry: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, loader: Optional[Callable[[], Any]] = None) -> None:
        """Register a library with an optional loader."""

        self._registry[name] = {"loader": loader, "handle": None}

    def load(self, name: str) -> Dict[str, Any]:
        """Load a registered library if a loader was provided."""

        entry = self._registry.get(name)
        if not entry:
            return {"ok": False, "reason": "not_registered", "name": name}
        loader = entry.get("loader")
        if loader is None:
            return {"ok": False, "reason": "no_loader", "name": name}
        try:
            entry["handle"] = loader()
            return {"ok": True, "name": name}
        except Exception as exc:  # pragma: no cover - defensive stub
            return {"ok": False, "reason": str(exc), "name": name}

    def get_handle(self, name: str) -> Optional[Any]:
        """Return a loaded handle if available."""

        entry = self._registry.get(name)
        if not entry:
            return None
        return entry.get("handle")
