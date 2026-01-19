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
module_name: client
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
  source: System_Stack/Logos_Agents/I2_Agent/protocol_operations/llm_io/client.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""


from typing import Any, Dict, List, Optional

from .config import load_config
from .types import ChatMessage, ChatRequest, ChatResponse
from .providers_openai import OpenAIProvider
from .providers_llama import LlamaProvider

class LLMClient:
    """
    Unified I/O wrapper for LLM backends.
    - backend chosen by env LLM_BACKEND
    - provider created lazily
    """

    def __init__(self):
        self.cfg = load_config()
        self._provider = None

    def _get_provider(self):
        if self._provider is not None:
            return self._provider

        if self.cfg.backend == "openai":
            self._provider = OpenAIProvider(
                api_key=self.cfg.openai_api_key or "",
                base_url=self.cfg.openai_base_url,
                default_model=self.cfg.openai_model,
            )
            return self._provider

        if self.cfg.backend == "llama":
            self._provider = LlamaProvider(
                endpoint=self.cfg.llama_endpoint,
                default_model=self.cfg.llama_model,
                default_temperature=self.cfg.llama_temperature,
            )
            return self._provider

        raise RuntimeError(f"Unsupported backend: {self.cfg.backend}")

    def chat(
        self,
        *,
        messages: List[Dict[str, str]] | List[ChatMessage],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> ChatResponse:
        norm: List[ChatMessage] = []
        for m in messages:
            if isinstance(m, ChatMessage):
                norm.append(m)
            else:
                norm.append(ChatMessage(role=m["role"], content=m["content"]))

        req = ChatRequest(
            messages=norm,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            extra=extra or {},
        )
        provider = self._get_provider()
        return provider.chat(req)
