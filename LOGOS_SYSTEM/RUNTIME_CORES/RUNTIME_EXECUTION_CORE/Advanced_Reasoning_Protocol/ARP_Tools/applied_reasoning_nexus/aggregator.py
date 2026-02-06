from __future__ import annotations

from typing import Any, Dict


def aggregate_results(*results: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {"status": "ok", "results": []}
    for res in results:
        if not isinstance(res, dict):
            continue
        merged["results"].append(res)
    merged["count"] = len(merged["results"])
    return merged
