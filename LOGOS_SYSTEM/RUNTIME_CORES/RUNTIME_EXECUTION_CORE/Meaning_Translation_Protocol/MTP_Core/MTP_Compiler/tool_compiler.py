# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: tool_compiler
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Meaning_Translation_Protocol/MTP_Core/MTP_Compiler/tool_compiler.py.
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
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Meaning_Translation_Protocol/MTP_Core/MTP_Compiler/tool_compiler.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
MTP Tool Compiler.

Consumes aggregated tool output, compiles it into SMP-tagged structures
with a metadata-formatted header, and emits a deterministic compile packet.

Design-only runtime helper. No external side effects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import time
from typing import Any, Dict, List, Mapping, Optional

from .tool_aggregator import AggregatedPacket, ToolAggregator, ToolOutput


@dataclass(frozen=True)
class SMPHeader:
	smp_id: str
	source: str
	timestamp: float
	epistemic_status: str
	proof_coverage: Optional[str]
	dependency_shape: Optional[str]
	semantic_projection: List[str]
	privation_gate_result: str
	security_flags: List[str]
	language: str
	processing_history: List[str]
	aa_catalog: List[str]
	schema_version: str
	immutability_seal: str


@dataclass(frozen=True)
class CompiledSMP:
	header: SMPHeader
	raw_input: Dict[str, Any]
	natural_language_layer: Dict[str, Any]
	symbolic_mathematics_layer: Dict[str, Any]
	formal_logic_layer: Dict[str, Any]
	tagged_text: str
	compiled_at: float
	compiled_by: str
	sealed: bool
	sealed_at: float
	source_fingerprint: str
	compiled_fingerprint: str


class MTPToolCompiler:
	"""
	Compile aggregated tool outputs into SMP structures and tags.
	"""

	def __init__(self, compiler_id: str = "MTP_TOOL_COMPILER") -> None:
		self.compiler_id = compiler_id

	def compile(
		self,
		aggregated: AggregatedPacket,
		header_overrides: Optional[Mapping[str, Any]] = None,
	) -> CompiledSMP:
		header_overrides = dict(header_overrides or {})
		header = self._build_header(aggregated, header_overrides)

		raw_input, natural_language, symbolic_math, formal_logic = self._build_layers(aggregated)

		tagged_text = self._render_tags(
			header,
			raw_input,
			natural_language,
			symbolic_math,
			formal_logic,
		)

		compiled_at = time.time()
		compiled_fingerprint = self._fingerprint_compiled(
			header,
			raw_input,
			natural_language,
			symbolic_math,
			formal_logic,
		)

		self._validate_schema(
			header=header,
			raw_input=raw_input,
			natural_language=natural_language,
			symbolic_math=symbolic_math,
			formal_logic=formal_logic,
		)

		return CompiledSMP(
			header=header,
			raw_input=raw_input,
			natural_language_layer=natural_language,
			symbolic_mathematics_layer=symbolic_math,
			formal_logic_layer=formal_logic,
			tagged_text=tagged_text,
			compiled_at=compiled_at,
			compiled_by=self.compiler_id,
			sealed=True,
			sealed_at=compiled_at,
			source_fingerprint=aggregated.content_fingerprint,
			compiled_fingerprint=compiled_fingerprint,
		)

	def _validate_schema(
		self,
		header: SMPHeader,
		raw_input: Dict[str, Any],
		natural_language: Dict[str, Any],
		symbolic_math: Dict[str, Any],
		formal_logic: Dict[str, Any],
	) -> None:
		missing = []
		if not isinstance(header, SMPHeader):
			missing.append("header")
		if "items" not in raw_input:
			missing.append("raw_input.items")
		if "items" not in natural_language:
			missing.append("natural_language_layer.items")
		if "items" not in symbolic_math:
			missing.append("symbolic_mathematics_layer.items")
		if "items" not in formal_logic:
			missing.append("formal_logic_layer.items")
		if missing:
			raise ValueError(f"SMP schema validation failed: {missing}")

	def _build_header(self, aggregated: AggregatedPacket, overrides: Mapping[str, Any]) -> SMPHeader:
		timestamp = float(overrides.get("timestamp", time.time()))
		smp_id = str(overrides.get("smp_id", f"SMP:{int(timestamp * 1000)}"))
		source = str(overrides.get("source", "MTP"))
		epistemic_status = _normalize_epistemic_status(overrides.get("epistemic_status", "PROVISIONAL"))
		proof_coverage = _normalize_optional_enum(
			overrides.get("proof_coverage"),
			ALLOWED_PROOF_COVERAGE,
			"proof_coverage",
		)
		dependency_shape = _normalize_optional_enum(
			overrides.get("dependency_shape"),
			ALLOWED_DEPENDENCY_SHAPE,
			"dependency_shape",
		)
		semantic_projection = _normalize_semantic_projection(overrides.get("semantic_projection", []))
		privation_gate_result = str(overrides.get("privation_gate_result", "unknown"))
		security_flags = list(overrides.get("security_flags", []))
		language = str(overrides.get("language", "und"))
		processing_history = list(overrides.get("processing_history", []))
		aa_catalog = list(overrides.get("aa_catalog", []))
		schema_version = str(overrides.get("schema_version", "MTP-SMP-0.1"))
		immutability_seal = str(
			overrides.get("immutability_seal", f"seal:{aggregated.content_fingerprint}")
		)

		processing_history.append("aggregated")
		processing_history.append("compiled")

		return SMPHeader(
			smp_id=smp_id,
			source=source,
			timestamp=timestamp,
			epistemic_status=epistemic_status,
			proof_coverage=proof_coverage,
			dependency_shape=dependency_shape,
			semantic_projection=semantic_projection,
			privation_gate_result=privation_gate_result,
			security_flags=security_flags,
			language=language,
			processing_history=processing_history,
			aa_catalog=aa_catalog,
			schema_version=schema_version,
			immutability_seal=immutability_seal,
		)

	def _build_layers(
		self,
		aggregated: AggregatedPacket,
	) -> tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
		raw_input: Dict[str, Any] = {"items": []}
		natural_language: Dict[str, Any] = {"items": []}
		symbolic_math: Dict[str, Any] = {"items": []}
		formal_logic: Dict[str, Any] = {"items": []}

		ordered_outputs = aggregated.ordered_outputs()
		for output in ordered_outputs:
			category = _classify_for_layer(output)
			entry = {
				"source_id": output.source_id,
				"name": output.name,
				"payload": output.payload,
				"metadata": output.metadata,
				"timestamp": output.timestamp,
			}

			if category == "raw_input":
				raw_input["items"].append(entry)
			elif category == "natural_language":
				natural_language["items"].append(entry)
			elif category == "symbolic_mathematics":
				symbolic_math["items"].append(entry)
			elif category == "formal_logic":
				formal_logic["items"].append(entry)
			else:
				natural_language["items"].append(entry)

		return raw_input, natural_language, symbolic_math, formal_logic

	def _render_tags(
		self,
		header: SMPHeader,
		raw_input: Dict[str, Any],
		natural_language: Dict[str, Any],
		symbolic_math: Dict[str, Any],
		formal_logic: Dict[str, Any],
	) -> str:
		header_lines = _format_header(header)
		return "\n".join(
			[
				"<SMP>",
				"<HEADER>",
				*header_lines,
				"</HEADER>",
				"<RAW_INPUT>",
				_canonical_json(raw_input),
				"</RAW_INPUT>",
				"<NATURAL_LANGUAGE_LAYER>",
				_canonical_json(natural_language),
				"</NATURAL_LANGUAGE_LAYER>",
				"<SYMBOLIC_MATHEMATICS_LAYER>",
				_canonical_json(symbolic_math),
				"</SYMBOLIC_MATHEMATICS_LAYER>",
				"<FORMAL_LOGIC_LAYER>",
				_canonical_json(formal_logic),
				"</FORMAL_LOGIC_LAYER>",
				"</SMP>",
			]
		)

	def _fingerprint_compiled(
		self,
		header: SMPHeader,
		raw_input: Dict[str, Any],
		natural_language: Dict[str, Any],
		symbolic_math: Dict[str, Any],
		formal_logic: Dict[str, Any],
	) -> str:
		payload = {
			"header": header.__dict__,
			"raw_input": raw_input,
			"natural_language_layer": natural_language,
			"symbolic_mathematics_layer": symbolic_math,
			"formal_logic_layer": formal_logic,
		}
		canonical = _canonical_json(payload)
		return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def compile_tool_outputs(
	outputs: List[ToolOutput],
	header_overrides: Optional[Mapping[str, Any]] = None,
	aggregator: Optional[ToolAggregator] = None,
) -> CompiledSMP:
	aggregator = aggregator or ToolAggregator()
	aggregated = aggregator.aggregate(outputs)
	compiler = MTPToolCompiler()
	return compiler.compile(aggregated, header_overrides=header_overrides)


def _classify_for_layer(output: ToolOutput) -> str:
	metadata = {str(k).lower(): v for k, v in output.metadata.items()}
	explicit = metadata.get("category") or metadata.get("layer")
	if explicit:
		return str(explicit).lower()

	name = output.name.lower()
	payload_keys = {str(k).lower() for k in output.payload.keys()}

	if "raw_input" in payload_keys or "user_input" in payload_keys or "raw" in name:
		return "raw_input"
	if {"natural_language", "nl", "tokens", "parse"} & payload_keys or "language" in name:
		return "natural_language"
	if {"symbolic", "lambda", "math", "calculus"} & payload_keys or "symbolic" in name:
		return "symbolic_mathematics"
	if {"formal_logic", "pxl", "wff", "axiom"} & payload_keys or "logic" in name:
		return "formal_logic"
	return "unknown"


def _format_header(header: SMPHeader) -> List[str]:
	return [
		f"SMP_ID: {header.smp_id}",
		f"Source: {header.source}",
		f"Timestamp: {header.timestamp}",
		f"Epistemic_Status: {header.epistemic_status}",
		f"Proof_Coverage: {header.proof_coverage or '<none>'}",
		f"Dependency_Shape: {header.dependency_shape or '<none>'}",
		f"Semantic_Projection: {', '.join(header.semantic_projection) or '<none>'}",
		f"Privation_Gate_Result: {header.privation_gate_result}",
		f"Security_Flags: {', '.join(header.security_flags)}",
		f"Language: {header.language}",
		f"Processing_History: {', '.join(header.processing_history)}",
		f"AA_Catalog: {', '.join(header.aa_catalog)}",
		f"Schema_Version: {header.schema_version}",
		f"Immutability_Seal: {header.immutability_seal}",
	]


ALLOWED_EPISTEMIC_STATUS = {"REJECTED", "PROVISIONAL", "CONDITIONAL", "CANONICAL"}
ALLOWED_PROOF_COVERAGE = {"UNPROVEN", "PARTIALLY_PROVEN", "FULLY_PROVEN", "PROVEN_FALSE"}
ALLOWED_DEPENDENCY_SHAPE = {
	"LINGUISTIC_DEPENDENT",
	"INFERENTIAL_DEPENDENT",
	"EVIDENCE_DEPENDENT",
	"AXIOMATIC_DEPENDENT",
}


def _normalize_epistemic_status(value: Any) -> str:
	if not isinstance(value, str) or not value.strip():
		raise ValueError("epistemic_status is required")
	status = value.strip().upper()
	if status not in ALLOWED_EPISTEMIC_STATUS:
		raise ValueError(f"epistemic_status must be one of: {sorted(ALLOWED_EPISTEMIC_STATUS)}")
	return status


def _normalize_optional_enum(value: Any, allowed: set[str], label: str) -> Optional[str]:
	if value is None:
		return None
	if not isinstance(value, str) or not value.strip():
		raise ValueError(f"{label} must be a non-empty string")
	normalized = value.strip().upper()
	if normalized not in allowed:
		raise ValueError(f"{label} must be one of: {sorted(allowed)}")
	return normalized


def _normalize_semantic_projection(value: Any) -> List[str]:
	if value is None:
		return []
	if not isinstance(value, list):
		raise ValueError("semantic_projection must be a list")
	projections = [str(item).strip().upper() for item in value if str(item).strip()]
	if not projections:
		return []
	registered = _load_semantic_projection_families()
	unregistered = [item for item in projections if item not in registered]
	if unregistered:
		raise ValueError(f"semantic_projection unregistered: {sorted(set(unregistered))}")
	return projections


def _load_semantic_projection_families() -> set[str]:
	root = _find_repo_root()
	manifest_path = root / "_Governance" / "Semantic_Projection_Manifest.json"
	if not manifest_path.is_file():
		raise ValueError("Semantic_Projection_Manifest.json missing")
	with manifest_path.open("r", encoding="utf-8") as handle:
		payload = json.load(handle)
	families = payload.get("families") if isinstance(payload, dict) else None
	if not isinstance(families, dict):
		raise ValueError("Semantic_Projection_Manifest.json invalid")
	return {str(key).upper() for key in families.keys()}


def _find_repo_root() -> Path:
	current = Path(__file__).resolve()
	for parent in [current] + list(current.parents):
		if (parent / "_Governance").is_dir():
			return parent
	raise ValueError("Repository root with _Governance not found")


def _canonical_json(value: Any) -> str:
	return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)

