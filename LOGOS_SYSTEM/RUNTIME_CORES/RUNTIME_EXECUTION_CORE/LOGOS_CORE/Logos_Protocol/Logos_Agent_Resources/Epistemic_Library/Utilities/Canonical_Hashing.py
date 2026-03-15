import json
import hashlib
from typing import Any

# Canonicalize JSON: recursively sort keys, normalize whitespace, newlines, and encode as UTF-8

def canonicalize_json(obj: Any) -> bytes:
    def _sort(obj):
        if isinstance(obj, dict):
            return {k: _sort(obj[k]) for k in sorted(obj)}
        elif isinstance(obj, list):
            return [_sort(x) for x in obj]
        else:
            return obj
    sorted_obj = _sort(obj)
    # Deterministic serializer: no insignificant whitespace, newlines normalized
    canon = json.dumps(sorted_obj, separators=(",", ":"), ensure_ascii=False)
    canon = canon.replace('\r\n', '\n').replace('\r', '\n')
    return canon.encode('utf-8')

def compute_sha256(obj: Any) -> str:
    canon_bytes = canonicalize_json(obj)
    return hashlib.sha256(canon_bytes).hexdigest()
