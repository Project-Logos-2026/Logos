"""Stasis holding area for preloaded libraries."""

from __future__ import annotations

from typing import Any, Dict, Optional


class StasisHoldingArea:
    """Keeps external handles ready for deployment without executing them."""

    def __init__(self) -> None:
        self._handles: Dict[str, Any] = {}

    def hold(self, name: str, handle: Any) -> None:
        self._handles[name] = handle

    def get(self, name: str) -> Optional[Any]:
        return self._handles.get(name)

    def route(self, name: str) -> Dict[str, Any]:
        handle = self._handles.get(name)
        if handle is None:
            return {"ok": False, "reason": "not_held", "name": name}
        return {"ok": True, "name": name, "handle": handle}
