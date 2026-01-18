# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: sanitizer
runtime_layer: inferred
role: inferred
agent_binding: None
protocol_binding: None
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: System_Stack/Meaning_Translation_Protocol/core_processing/sanitizer.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
import re
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass
class SanitizationResult:
    """Result of prompt sanitisation."""

    cleaned_text: str
    issues: List[str]
    metadata: Dict[str, Any]


class Sanitizer:
    """Lightweight input sanitiser for the interaction pipeline."""

    _CONTROL_CHARS = re.compile(r"[\u0000-\u001f\u007f]")

    def __init__(self, max_length: int = 4096) -> None:
        self.max_length = max_length

    def sanitize(self, prompt: str) -> SanitizationResult:
        """Clean a user prompt and record issues for downstream audit."""
        issues: List[str] = []
        metadata: Dict[str, Any] = {
            "original_length": len(prompt or ""),
        }

        if prompt is None:
            issues.append("empty_input")
            return SanitizationResult("", issues, metadata)

        text = prompt.strip()
        if not text:
            issues.append("blank_input")

        # Remove control characters that could break downstream consumers.
        if self._CONTROL_CHARS.search(text):
            text = self._CONTROL_CHARS.sub(" ", text)
            issues.append("control_chars_removed")

        # Collapse repeated whitespace for stable downstream parsing.
        text = re.sub(r"\s+", " ", text)

        if len(text) > self.max_length:
            metadata["truncated_from"] = len(text)
            text = text[: self.max_length]
            issues.append("input_truncated")

        metadata["cleaned_length"] = len(text)
        if issues:
            logger.debug("Sanitizer issues detected: %s", issues)
        return SanitizationResult(text, issues, metadata)


sanitizer = Sanitizer()

__all__ = ["Sanitizer", "SanitizationResult", "sanitizer"]
