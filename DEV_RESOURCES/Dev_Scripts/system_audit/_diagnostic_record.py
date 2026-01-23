"""
Shared diagnostic record utilities for End-to-End schema compliance.
Fail-closed: missing positions must be computed or explicitly set to -1.
"""
from typing import Dict, Optional

def diag(
    *,
    error_type: str,
    line: int,
    char_start: int,
    char_end: int,
    details: Optional[str] = None,
    severity: Optional[str] = "medium",
    source: Optional[str] = None,
) -> Dict:
    if line < 1:
        raise ValueError("line must be >= 1")
    if char_start < 0 or char_end < char_start:
        raise ValueError("invalid char range")
    return {
        "error_type": error_type,
        "line": line,
        "char_start": char_start,
        "char_end": char_end,
        "severity": severity or "medium",
        "details": details or "",
        "_source": source or "",
    }
