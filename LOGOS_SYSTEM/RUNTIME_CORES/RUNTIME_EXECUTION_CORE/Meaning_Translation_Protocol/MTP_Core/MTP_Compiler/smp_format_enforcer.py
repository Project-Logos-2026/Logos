# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: smp_format_enforcer
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Meaning_Translation_Protocol/MTP_Core/MTP_Compiler/smp_format_enforcer.py.
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
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Meaning_Translation_Protocol/MTP_Core/MTP_Compiler/smp_format_enforcer.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
SMP Format Enforcer.

Validates compiled SMP tags, checks mutation, computes hashes, records
audit entries, and routes outputs through approval gates.

Design-only runtime helper. No external side effects unless injected
handlers are provided by the caller.
"""


from dataclasses import dataclass
import hashlib
import json
import time
from typing import Any, Callable, Dict, Optional

from .tool_compiler import CompiledSMP, MTPToolCompiler
from .tool_aggregator import ToolAggregator, ToolOutput


class SMPFormatViolation(Exception):
	pass


@dataclass(frozen=True)
class EnforcementAudit:
	smp_id: str
	timestamp: float
	status: str
	compiled_fingerprint: str
	final_hash: str
	notes: Dict[str, Any]


@dataclass(frozen=True)
class EnforcementResult:
	approved: bool
	audit: EnforcementAudit
	nexus_dispatched: bool
	i2_dispatched: bool
	logos_agent_dispatched: bool


class SMPFormatEnforcer:
	"""
	Validates SMP format, enforces mutation checks, and dispatches
	to downstream gates if approved.
	"""

	REQUIRED_HEADER_FIELDS = {
		"smp_id",
		"source",
		"timestamp",
		"epistemic_status",
		"privation_gate_result",
		"security_flags",
		"language",
		"processing_history",
		"aa_catalog",
		"schema_version",
		"immutability_seal",
	}

	REQUIRED_TAGS = {
		"<SMP>",
		"</SMP>",
		"<HEADER>",
		"</HEADER>",
		"<RAW_INPUT>",
		"</RAW_INPUT>",
		"<NATURAL_LANGUAGE_LAYER>",
		"</NATURAL_LANGUAGE_LAYER>",
		"<SYMBOLIC_MATHEMATICS_LAYER>",
		"</SYMBOLIC_MATHEMATICS_LAYER>",
		"<FORMAL_LOGIC_LAYER>",
		"</FORMAL_LOGIC_LAYER>",
	}

	def __init__(
		self,
		audit_logger: Optional[Callable[[EnforcementAudit], None]] = None,
		nexus_gate_approver: Optional[Callable[[CompiledSMP], bool]] = None,
		i2_privation_gate: Optional[Callable[[CompiledSMP], bool]] = None,
		nexus_sender: Optional[Callable[[CompiledSMP], None]] = None,
		i2_sender: Optional[Callable[[CompiledSMP], None]] = None,
		logos_agent_sender: Optional[Callable[[CompiledSMP], None]] = None,
	) -> None:
		self.audit_logger = audit_logger
		self.nexus_gate_approver = nexus_gate_approver
		self.i2_privation_gate = i2_privation_gate
		self.nexus_sender = nexus_sender
		self.i2_sender = i2_sender
		self.logos_agent_sender = logos_agent_sender

	def enforce(self, compiled: CompiledSMP) -> EnforcementResult:
		self._validate_header(compiled)
		self._validate_tags(compiled.tagged_text)
		self._validate_mutation(compiled)
		self._validate_seal(compiled)

		final_hash = self._hash_compiled(compiled)
		approved = self._approve(compiled)

		audit = EnforcementAudit(
			smp_id=compiled.header.smp_id,
			timestamp=time.time(),
			status="approved" if approved else "rejected",
			compiled_fingerprint=compiled.compiled_fingerprint,
			final_hash=final_hash,
			notes={},
		)

		if self.audit_logger is not None:
			self.audit_logger(audit)

		nexus_dispatched = False
		i2_dispatched = False
		logos_agent_dispatched = False

		if approved:
			nexus_dispatched = self._dispatch(self.nexus_sender, compiled)
			i2_dispatched = self._dispatch(self.i2_sender, compiled)
			logos_agent_dispatched = self._dispatch(self.logos_agent_sender, compiled)

		return EnforcementResult(
			approved=approved,
			audit=audit,
			nexus_dispatched=nexus_dispatched,
			i2_dispatched=i2_dispatched,
			logos_agent_dispatched=logos_agent_dispatched,
		)

	def _validate_header(self, compiled: CompiledSMP) -> None:
		header_fields = compiled.header.__dict__.keys()
		missing = self.REQUIRED_HEADER_FIELDS - set(header_fields)
		if missing:
			raise SMPFormatViolation(f"Missing header fields: {sorted(missing)}")

	def _validate_tags(self, tagged_text: str) -> None:
		missing = [tag for tag in self.REQUIRED_TAGS if tag not in tagged_text]
		if missing:
			raise SMPFormatViolation(f"Missing SMP tags: {missing}")

	def _validate_mutation(self, compiled: CompiledSMP) -> None:
		recomputed = self._hash_payload(compiled)
		if recomputed != compiled.compiled_fingerprint:
			raise SMPFormatViolation("Compiled payload fingerprint mismatch")

	def _validate_seal(self, compiled: CompiledSMP) -> None:
		if not compiled.sealed:
			raise SMPFormatViolation("SMP immutability seal missing")

	def _hash_compiled(self, compiled: CompiledSMP) -> str:
		canonical = _canonical_json(
			{
				"header": compiled.header.__dict__,
				"raw_input": compiled.raw_input,
				"natural_language_layer": compiled.natural_language_layer,
				"symbolic_mathematics_layer": compiled.symbolic_mathematics_layer,
				"formal_logic_layer": compiled.formal_logic_layer,
				"tagged_text": compiled.tagged_text,
				"sealed": compiled.sealed,
				"sealed_at": compiled.sealed_at,
			}
		)
		return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

	def _hash_payload(self, compiled: CompiledSMP) -> str:
		canonical = _canonical_json(
			{
				"header": compiled.header.__dict__,
				"raw_input": compiled.raw_input,
				"natural_language_layer": compiled.natural_language_layer,
				"symbolic_mathematics_layer": compiled.symbolic_mathematics_layer,
				"formal_logic_layer": compiled.formal_logic_layer,
			}
		)
		return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

	def _approve(self, compiled: CompiledSMP) -> bool:
		nexus_ok = True
		if self.nexus_gate_approver is not None:
			nexus_ok = bool(self.nexus_gate_approver(compiled))

		i2_ok = True
		if self.i2_privation_gate is not None:
			i2_ok = bool(self.i2_privation_gate(compiled))

		return nexus_ok and i2_ok

	def _dispatch(self, sender: Optional[Callable[[CompiledSMP], None]], compiled: CompiledSMP) -> bool:
		if sender is None:
			return False
		sender(compiled)
		return True


def compile_and_enforce(
	outputs: list[ToolOutput],
	header_overrides: Optional[Dict[str, Any]] = None,
	aggregator: Optional[ToolAggregator] = None,
	compiler: Optional[MTPToolCompiler] = None,
	enforcer: Optional[SMPFormatEnforcer] = None,
) -> EnforcementResult:
	aggregator = aggregator or ToolAggregator()
	compiler = compiler or MTPToolCompiler()
	enforcer = enforcer or SMPFormatEnforcer()

	aggregated = aggregator.aggregate(outputs)
	compiled = compiler.compile(aggregated, header_overrides=header_overrides)
	return enforcer.enforce(compiled)


def _canonical_json(value: Any) -> str:
	return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)

