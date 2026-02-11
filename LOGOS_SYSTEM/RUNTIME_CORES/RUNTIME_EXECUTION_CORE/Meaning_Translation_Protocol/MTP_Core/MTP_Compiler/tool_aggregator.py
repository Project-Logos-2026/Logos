# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: tool_aggregator
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Meaning_Translation_Protocol/MTP_Core/MTP_Compiler/tool_aggregator.py.
agent_binding: None
protocol_binding: Meaning_Translation_Protocol
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Meaning_Translation_Protocol/MTP_Core/MTP_Compiler/tool_aggregator.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Tool Aggregator for MTP Compiler.

Aggregates tool and library outputs, classifies them into SMP layers,
optimizes ordering, and produces a deterministic packet for compilation.

Design-only runtime helper. No external side effects.
"""


from dataclasses import dataclass, field
import hashlib
import json
import time
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


DEFAULT_ORDER = (
	"raw_input",
	"natural_language",
	"symbolic_mathematics",
	"formal_logic",
	"unknown",
)


@dataclass(frozen=True)
class ToolOutput:
	source_id: str
	name: str
	payload: Mapping[str, Any]
	metadata: Mapping[str, Any] = field(default_factory=dict)
	timestamp: float = field(default_factory=lambda: time.time())


@dataclass(frozen=True)
class AggregatedPacket:
	outputs: Tuple[ToolOutput, ...]
	classifications: Dict[str, List[int]]
	ordered_indices: List[int]
	created_at: float
	context: Dict[str, Any]
	content_fingerprint: str

	def ordered_outputs(self) -> List[ToolOutput]:
		return [self.outputs[idx] for idx in self.ordered_indices]


class ToolAggregator:
	"""
	Aggregate tool outputs into a deterministic, classified packet.
	"""

	def __init__(self, order: Optional[Tuple[str, ...]] = None) -> None:
		self.order = order or DEFAULT_ORDER

	def aggregate(
		self,
		outputs: Iterable[ToolOutput],
		context: Optional[Dict[str, Any]] = None,
	) -> AggregatedPacket:
		context = dict(context or {})
		normalized = tuple(self._normalize_outputs(outputs))
		classifications = self._classify_outputs(normalized)
		ordered_indices = self._optimize_order(normalized, classifications)
		fingerprint = self._fingerprint_outputs(normalized, ordered_indices)
		return AggregatedPacket(
			outputs=normalized,
			classifications=classifications,
			ordered_indices=ordered_indices,
			created_at=time.time(),
			context=context,
			content_fingerprint=fingerprint,
		)

	def _normalize_outputs(self, outputs: Iterable[ToolOutput]) -> Iterable[ToolOutput]:
		for output in outputs:
			if isinstance(output, ToolOutput):
				yield output
			elif isinstance(output, dict):
				yield ToolOutput(
					source_id=str(output.get("source_id", "unknown")),
					name=str(output.get("name", "output")),
					payload=output.get("payload", {}),
					metadata=output.get("metadata", {}),
					timestamp=float(output.get("timestamp", time.time())),
				)

	def _classify_outputs(self, outputs: Tuple[ToolOutput, ...]) -> Dict[str, List[int]]:
		classifications: Dict[str, List[int]] = {key: [] for key in self.order}
		classifications.setdefault("unknown", [])
		for idx, output in enumerate(outputs):
			category = self._classify_output(output)
			classifications.setdefault(category, []).append(idx)
		return classifications

	def _classify_output(self, output: ToolOutput) -> str:
		metadata = {str(k).lower(): v for k, v in output.metadata.items()}
		explicit = metadata.get("category") or metadata.get("layer")
		if explicit:
			return str(explicit).lower()

		payload_keys = {str(k).lower() for k in output.payload.keys()}
		name = output.name.lower()

		if "raw_input" in payload_keys or "user_input" in payload_keys or "raw" in name:
			return "raw_input"

		if {"natural_language", "nl", "tokens", "parse"} & payload_keys or "language" in name:
			return "natural_language"

		if {"symbolic", "lambda", "math", "calculus"} & payload_keys or "symbolic" in name:
			return "symbolic_mathematics"

		if {"formal_logic", "pxl", "wff", "axiom"} & payload_keys or "logic" in name:
			return "formal_logic"

		return "unknown"

	def _optimize_order(
		self,
		outputs: Tuple[ToolOutput, ...],
		classifications: Dict[str, List[int]],
	) -> List[int]:
		category_rank = {key: idx for idx, key in enumerate(self.order)}

		def sort_key(idx: int) -> Tuple[int, int, float, str]:
			output = outputs[idx]
			category = self._classify_output(output)
			priority = int(output.metadata.get("priority", 50))
			return (
				category_rank.get(category, len(self.order)),
				priority,
				output.timestamp,
				output.source_id,
			)

		indices = list(range(len(outputs)))
		return sorted(indices, key=sort_key)

	def _fingerprint_outputs(
		self,
		outputs: Tuple[ToolOutput, ...],
		ordered_indices: List[int],
	) -> str:
		serializable = [self._output_to_dict(outputs[idx]) for idx in ordered_indices]
		canonical = _canonical_json(serializable)
		return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

	def _output_to_dict(self, output: ToolOutput) -> Dict[str, Any]:
		return {
			"source_id": output.source_id,
			"name": output.name,
			"payload": output.payload,
			"metadata": output.metadata,
			"timestamp": output.timestamp,
		}


def _canonical_json(value: Any) -> str:
	return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)

