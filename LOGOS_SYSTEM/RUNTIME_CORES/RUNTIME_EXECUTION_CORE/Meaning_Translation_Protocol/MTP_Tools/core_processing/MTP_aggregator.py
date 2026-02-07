from __future__ import annotations

#!/usr/bin/env python3
# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: MTP_aggregator
runtime_layer: inferred
role: MTP tool orchestration and aggregation
agent_binding: None
protocol_binding: Meaning_Translation_Protocol
boot_phase: inferred
expected_imports: [tool_aggregator, tool_compiler, smp_format_enforcer]
provides: [MTPEnrichmentOrchestrator, build_mtp_smp_packet]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "Returns non-authoritative error payloads when enforcement fails."
rewrite_provenance:
  source: System_Stack/Meaning_Translation_Protocol/core_processing/MTP_aggregator.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-02-06T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
MTP core aggregation orchestrator.

Design-first, fail-closed, non-executing. This module does not invoke
external tools unless explicit outputs are provided. It aggregates tool
outputs into the three enrichment layers and builds sealed SMP packets.
"""

from dataclasses import dataclass
import time
from typing import Any, Dict, Iterable, List, Mapping, Optional

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Meaning_Translation_Protocol.MTP_Core.MTP_Compiler.tool_aggregator import (
	ToolAggregator,
	ToolOutput,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Meaning_Translation_Protocol.MTP_Core.MTP_Compiler.tool_compiler import (
	CompiledSMP,
	MTPToolCompiler,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Meaning_Translation_Protocol.MTP_Core.MTP_Compiler.smp_format_enforcer import (
	EnforcementResult,
	SMPFormatEnforcer,
)


LAYER_NATURAL_LANGUAGE = "natural_language"
LAYER_SYMBOLIC_MATHEMATICS = "symbolic_mathematics"
LAYER_FORMAL_LOGIC = "formal_logic"


@dataclass(frozen=True)
class MTPAggregationResult:
	aggregated: Any
	compiled: Optional[CompiledSMP]
	enforcement: Optional[EnforcementResult]
	status: str
	reason: Optional[str] = None


class MTPEnrichmentOrchestrator:
	"""
	Orchestrate enrichment tool outputs and build sealed SMP packets.

	This orchestrator is non-executing by default and expects precomputed
	tool outputs. It aggregates outputs into the required enrichment layers
	and defers enforcement to the compiler/enforcer layer.
	"""

	def __init__(
		self,
		aggregator: Optional[ToolAggregator] = None,
		compiler: Optional[MTPToolCompiler] = None,
		enforcer: Optional[SMPFormatEnforcer] = None,
	) -> None:
		self.aggregator = aggregator or ToolAggregator()
		self.compiler = compiler or MTPToolCompiler()
		self.enforcer = enforcer or SMPFormatEnforcer()

	def collect_enrichment(
		self,
		raw_input: Mapping[str, Any],
		context: Optional[Dict[str, Any]] = None,
		tool_outputs: Optional[Iterable[ToolOutput]] = None,
	) -> List[ToolOutput]:
		context = dict(context or {})
		outputs: List[ToolOutput] = []

		outputs.append(
			ToolOutput(
				source_id="ingress",
				name="raw_input",
				payload={"raw_input": raw_input},
				metadata={"category": "raw_input"},
				timestamp=time.time(),
			)
		)

		if tool_outputs:
			outputs.extend(tool_outputs)

		return outputs

	def build_smp(
		self,
		raw_input: Mapping[str, Any],
		context: Optional[Dict[str, Any]] = None,
		tool_outputs: Optional[Iterable[ToolOutput]] = None,
		header_overrides: Optional[Mapping[str, Any]] = None,
	) -> MTPAggregationResult:
		outputs = self.collect_enrichment(
			raw_input=raw_input,
			context=context,
			tool_outputs=tool_outputs,
		)

		aggregated = self.aggregator.aggregate(outputs, context=context)
		compiled = self.compiler.compile(aggregated, header_overrides=header_overrides)

		try:
			enforcement = self.enforcer.enforce(compiled)
		except Exception as exc:
			return MTPAggregationResult(
				aggregated=aggregated,
				compiled=compiled,
				enforcement=None,
				status="rejected",
				reason=str(exc),
			)

		if not enforcement.approved:
			return MTPAggregationResult(
				aggregated=aggregated,
				compiled=compiled,
				enforcement=enforcement,
				status="rejected",
				reason="format_enforcement_failed",
			)

		return MTPAggregationResult(
			aggregated=aggregated,
			compiled=compiled,
			enforcement=enforcement,
			status="approved",
			reason=None,
		)


def build_mtp_smp_packet(
	*,
	raw_input: Mapping[str, Any],
	context: Optional[Dict[str, Any]] = None,
	tool_outputs: Optional[Iterable[ToolOutput]] = None,
	header_overrides: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
	"""
	Build a sealed SMP packet from ingress input.

	Returns a dict payload for upstream routing without executing external tools.
	"""
	orchestrator = MTPEnrichmentOrchestrator()
	result = orchestrator.build_smp(
		raw_input=raw_input,
		context=context,
		tool_outputs=tool_outputs,
		header_overrides=header_overrides,
	)

	compiled_payload = _compiled_to_dict(result.compiled) if result.compiled else None

	return {
		"status": result.status,
		"reason": result.reason,
		"smp": compiled_payload,
	}


def _compiled_to_dict(compiled: Optional[CompiledSMP]) -> Optional[Dict[str, Any]]:
	if compiled is None:
		return None
	return {
		"header": compiled.header.__dict__,
		"raw_input": compiled.raw_input,
		"natural_language_layer": compiled.natural_language_layer,
		"symbolic_mathematics_layer": compiled.symbolic_mathematics_layer,
		"formal_logic_layer": compiled.formal_logic_layer,
		"tagged_text": compiled.tagged_text,
		"compiled_at": compiled.compiled_at,
		"compiled_by": compiled.compiled_by,
		"sealed": compiled.sealed,
		"sealed_at": compiled.sealed_at,
		"source_fingerprint": compiled.source_fingerprint,
		"compiled_fingerprint": compiled.compiled_fingerprint,
	}

