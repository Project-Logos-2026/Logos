# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: MTP_Output_Renderer
runtime_layer: language_egress
role: AF-LANG-003 Output Renderer
responsibility: Renders finalized semantic structures into human-readable
    natural language (L1), arithmetic shadow expressions (L2), and PXL
    formal references (L3) per the Output Synchronization Model.
    Uses deterministic template selection. No probabilistic paraphrasing.
    Variant selection from curated substitution tables only.
    Does not alter meaning. Does not reorder with meaning impact.
    Does not influence runtime decisions.
agent_binding: None
protocol_binding: Meaning_Translation_Protocol
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: [hashlib, time, dataclasses, typing, enum]
provides: [OutputRenderer, RenderedOutput, L1Surface, L2Shadow, L3Reference, RenderConfig]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: Returns raw content concatenation on template failure.
    Never fabricates content not present in linearization plan.
    Halts on L1/L2 divergence if L2 is populated.
rewrite_provenance:
  source: new_module
  rewrite_phase: MTP_Egress_Enhancement
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: MTP
  metrics: render_count, template_hits, template_misses, l2_sync_checks
---------------------
"""

import hashlib
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum


# =============================================================================
# Tone and Verbosity
# =============================================================================

class ToneLevel(Enum):
    FORMAL = "formal"
    NEUTRAL = "neutral"
    ACCESSIBLE = "accessible"


class VerbosityLevel(Enum):
    MINIMAL = "minimal"
    STANDARD = "standard"
    DETAILED = "detailed"


class RenderStatus(Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FALLBACK = "fallback"
    FAILED = "failed"


# =============================================================================
# Output Layer Structures (L1 / L2 / L3)
# =============================================================================

@dataclass
class L1Surface:
    sentences: List[str] = field(default_factory=list)
    paragraph: str = ""
    template_hits: int = 0
    template_misses: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sentences": self.sentences,
            "paragraph": self.paragraph,
            "template_hits": self.template_hits,
            "template_misses": self.template_misses,
        }


@dataclass
class L2Shadow:
    expressions: List[str] = field(default_factory=list)
    populated: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "expressions": self.expressions,
            "populated": self.populated,
        }


@dataclass
class L3Reference:
    pxl_refs: List[str] = field(default_factory=list)
    proof_hashes: List[str] = field(default_factory=list)
    populated: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pxl_refs": self.pxl_refs,
            "proof_hashes": self.proof_hashes,
            "populated": self.populated,
        }


@dataclass
class RenderConfig:
    tone: ToneLevel = ToneLevel.NEUTRAL
    verbosity: VerbosityLevel = VerbosityLevel.STANDARD
    include_l2: bool = False
    include_l3: bool = False


@dataclass
class RenderedOutput:
    render_id: str
    source_plan_id: str
    config: RenderConfig = field(default_factory=RenderConfig)
    l1: L1Surface = field(default_factory=L1Surface)
    l2: L2Shadow = field(default_factory=L2Shadow)
    l3: L3Reference = field(default_factory=L3Reference)
    status: RenderStatus = RenderStatus.FAILED
    content_hash: str = ""
    render_timestamp: float = 0.0
    render_time_ms: float = 0.0
    sync_valid: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "render_id": self.render_id,
            "source_plan_id": self.source_plan_id,
            "l1": self.l1.to_dict(),
            "l2": self.l2.to_dict(),
            "l3": self.l3.to_dict(),
            "status": self.status.value,
            "content_hash": self.content_hash,
            "render_timestamp": self.render_timestamp,
            "render_time_ms": round(self.render_time_ms, 2),
            "sync_valid": self.sync_valid,
        }


# =============================================================================
# Sentence Templates (SP → sentence frame per tone)
# =============================================================================

_TEMPLATES: Dict[str, Dict[str, str]] = {
    "SP-01": {
        "formal": "{content}.",
        "neutral": "{content}.",
        "accessible": "{content}.",
    },
    "SP-02": {
        "formal": "A distinction is drawn: {content}.",
        "neutral": "Specifically, {content}.",
        "accessible": "To be clear, {content}.",
    },
    "SP-03": {
        "formal": "It is not the case that {content}.",
        "neutral": "This does not hold: {content}.",
        "accessible": "That is not the case — {content}.",
    },
    "SP-04": {
        "formal": "Subject to the constraint: {content}.",
        "neutral": "With the constraint that {content}.",
        "accessible": "Keep in mind: {content}.",
    },
    "SP-05": {
        "formal": "This depends on the following: {content}.",
        "neutral": "This requires: {content}.",
        "accessible": "First, {content}.",
    },
    "SP-06": {
        "formal": "Evaluation yields: {content}.",
        "neutral": "Assessment: {content}.",
        "accessible": "Looking at this: {content}.",
    },
    "SP-07": {
        "formal": "There is uncertainty regarding: {content}.",
        "neutral": "It remains uncertain whether {content}.",
        "accessible": "It is not yet clear whether {content}.",
    },
    "SP-08": {
        "formal": "The following is unknown: {content}.",
        "neutral": "This is currently unknown: {content}.",
        "accessible": "We do not yet know: {content}.",
    },
    "SP-09": {
        "formal": "The following commitment is registered: {content}.",
        "neutral": "Committed: {content}.",
        "accessible": "We are committed to: {content}.",
    },
    "SP-10": {
        "formal": "The following relation holds: {content}.",
        "neutral": "Related: {content}.",
        "accessible": "Connected to this: {content}.",
    },
    "SP-11": {
        "formal": "Within the scope of: {content}.",
        "neutral": "In the context of {content}:",
        "accessible": "Regarding {content}:",
    },
    "SP-12": {
        "formal": "Grounded in: {content}.",
        "neutral": "Based on: {content}.",
        "accessible": "This comes from: {content}.",
    },
}

_VERBOSITY_CONNECTORS: Dict[str, Dict[str, str]] = {
    "minimal": {
        "conjunction": " ",
        "transition": " ",
        "separator": " ",
    },
    "standard": {
        "conjunction": " Furthermore, ",
        "transition": " Additionally, ",
        "separator": " ",
    },
    "detailed": {
        "conjunction": " Furthermore, it should be noted that ",
        "transition": " In addition to the above, ",
        "separator": "\n\n",
    },
}


# =============================================================================
# Output Renderer (AF-LANG-003)
# =============================================================================

class OutputRenderer:

    def render(
        self,
        plan: Any,
        config: Optional[RenderConfig] = None,
        stability_report: Optional[Any] = None,
    ) -> RenderedOutput:
        start = time.monotonic()

        if config is None:
            config = RenderConfig()

        output = RenderedOutput(
            render_id=f"RO-{plan.plan_id}",
            source_plan_id=plan.plan_id,
            config=config,
            render_timestamp=time.time(),
        )

        try:
            l1 = self._render_l1(plan, config, stability_report)
            output.l1 = l1

            if config.include_l2:
                l2 = self._render_l2(plan)
                output.l2 = l2

            if config.include_l3:
                l3 = self._render_l3(plan)
                output.l3 = l3

            if output.l2.populated:
                output.sync_valid = self._check_l1_l2_sync(output.l1, output.l2)
                if not output.sync_valid:
                    output.status = RenderStatus.FAILED
                    output.render_time_ms = (time.monotonic() - start) * 1000.0
                    return output

            if l1.template_misses > 0 and l1.template_hits > 0:
                output.status = RenderStatus.PARTIAL
            elif l1.template_misses > 0:
                output.status = RenderStatus.FALLBACK
            else:
                output.status = RenderStatus.SUCCESS

        except Exception:
            output.status = RenderStatus.FALLBACK
            output.l1 = self._fallback_render(plan)

        output.content_hash = hashlib.sha256(
            output.l1.paragraph.encode("utf-8")
        ).hexdigest()

        output.render_time_ms = (time.monotonic() - start) * 1000.0
        return output

    def _render_l1(
        self,
        plan: Any,
        config: RenderConfig,
        stability_report: Optional[Any],
    ) -> L1Surface:
        surface = L1Surface()
        tone_key = config.tone.value
        connectors = _VERBOSITY_CONNECTORS.get(
            config.verbosity.value,
            _VERBOSITY_CONNECTORS["standard"],
        )

        for unit in plan.units:
            sp_code = unit.primitive_code
            templates = _TEMPLATES.get(sp_code)

            if templates is None:
                surface.sentences.append(unit.content)
                surface.template_misses += 1
                continue

            template = templates.get(tone_key, templates.get("neutral", "{content}."))
            sentence = template.format(content=unit.content)
            surface.sentences.append(sentence)
            surface.template_hits += 1

        separator = connectors.get("separator", " ")
        surface.paragraph = separator.join(surface.sentences)

        return surface

    def _render_l2(self, plan: Any) -> L2Shadow:
        shadow = L2Shadow()
        expressions: List[str] = []

        for unit in plan.units:
            if unit.confidence is not None:
                expressions.append(
                    f"{unit.primitive_code}({unit.source_node_id}) = {unit.confidence}"
                )

        if expressions:
            shadow.expressions = expressions
            shadow.populated = True

        return shadow

    def _render_l3(self, plan: Any) -> L3Reference:
        ref = L3Reference()
        pxl_refs: List[str] = []

        for unit in plan.units:
            if unit.modality and "pxl" in str(unit.modality).lower():
                pxl_refs.append(f"{unit.primitive_code}:{unit.source_node_id}")

        if pxl_refs:
            ref.pxl_refs = pxl_refs
            ref.populated = True

        return ref

    def _check_l1_l2_sync(self, l1: L1Surface, l2: L2Shadow) -> bool:
        if not l2.populated:
            return True

        l1_node_count = len(l1.sentences)
        l2_expr_count = len(l2.expressions)

        if l2_expr_count > l1_node_count:
            return False

        return True

    def _fallback_render(self, plan: Any) -> L1Surface:
        surface = L1Surface()
        for unit in plan.units:
            surface.sentences.append(unit.content)
            surface.template_misses += 1

        surface.paragraph = " ".join(surface.sentences)
        return surface
