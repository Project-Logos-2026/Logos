# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from __future__ import annotations
# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: providers_openai
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
  source: System_Stack/Logos_Agents/I2_Agent/protocol_operations/llm_io/providers_openai.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""


import json
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional

from .types import ChatMessage, ChatRequest, ChatResponse

class OpenAIProvider:
    """
    OpenAI-compatible Chat Completions over HTTP.
    No external dependencies.
    """

    def __init__(self, *, api_key: str, base_url: str, default_model: str):
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required for openai backend.")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.default_model = default_model

    def chat(self, req: ChatRequest) -> ChatResponse:
        model = req.model or self.default_model
        url = f"{self.base_url}/v1/chat/completions"

        payload: Dict[str, Any] = {
            "model": model,
            "messages": [m.to_dict() for m in req.messages],
            "temperature": req.temperature,
        }
        if req.max_tokens is not None:
            payload["max_tokens"] = req.max_tokens
        payload.update(req.extra or {})

        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        request = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=60) as resp:
                raw = resp.read().decode("utf-8")
                out = json.loads(raw)
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode("utf-8")
            except Exception:
                pass
            raise RuntimeError(f"OpenAIProvider HTTPError {e.code}: {body}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"OpenAIProvider URLError: {e}") from e

        try:
            text = out["choices"][0]["message"]["content"]
        except Exception:
            text = ""

        return ChatResponse(
            text=text or "",
            raw=out,
            provider="openai",
            model=model,
        )
