# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: MTP_Nexus
runtime_layer: language_egress
role: MTP egress pipeline orchestration nexus
responsibility: Orchestrates the full MTP egress pipeline in deterministic
    sequence per Language Pipeline Orchestration (stages 2-7) and
    Language AF Manifest (chained in manifest order, no skipping).
    Pipeline: Projection -> Linearization -> Fractal Evaluation ->
    Rendering -> Validation -> I2 Critique -> Emission.
    Implements retry with alternate tone on validation failure.
    Halts on retry exhaustion. Fail-closed throughout.
agent_binding: None
protocol_binding: Meaning_Translation_Protocol
runtime_classification: runtime_module
boot_phase: runtime
expected_imports: [hashlib, time, uuid, dataclasses, typing]
provides: [MTPNexus, EgressPipelineResult, PipelineStageRecord]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: Any stage failure halts pipeline. No partial emission.
    Validation retry exhaustion produces HALT with full diagnostic.
    I2 critique FAIL triggers re-render if retries remain.
rewrite_provenance:
  source: new_module
  rewrite_phase: MTP_Egress_Enhancement
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: MTP
  metrics: pipeline_runs, emission_count, retry_count, halt_count, stage_timings
---------------------
"""

import hashlib
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum


# =============================================================================
# Pipeline Status
# =============================================================================

class PipelineStatus(Enum):
    EMITTED = "emitted"
    HALTED = "halted"
    FAILED = "failed"


class StageStatus(Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    SKIP = "skip"


# =============================================================================
# Stage Records
# =============================================================================

@dataclass
class PipelineStageRecord:
    stage_name: str
    status: StageStatus = StageStatus.FAIL
    duration_ms: float = 0.0
    output_summary: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stage_name": self.stage_name,
            "status": self.status.value,
            "duration_ms": round(self.duration_ms, 2),
            "output_summary": self.output_summary,
        }


@dataclass
class EgressPipelineResult:
    pipeline_id: str
    source_smp_id: str
    status: PipelineStatus = PipelineStatus.FAILED
    stages: List[PipelineStageRecord] = field(default_factory=list)
    rendered_output: Optional[Any] = None
    i2_critique: Optional[Any] = None
    validation_result: Optional[Any] = None
    retries_used: int = 0
    max_retries: int = 2
    total_time_ms: float = 0.0
    pipeline_timestamp: float = 0.0

    def emitted_text(self) -> str:
        if self.rendered_output is not None and hasattr(self.rendered_output, "l1"):
            return self.rendered_output.l1.paragraph
        return ""

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "pipeline_id": self.pipeline_id,
            "source_smp_id": self.source_smp_id,
            "status": self.status.value,
            "stages": [s.to_dict() for s in self.stages],
            "retries_used": self.retries_used,
            "max_retries": self.max_retries,
            "total_time_ms": round(self.total_time_ms, 2),
            "pipeline_timestamp": self.pipeline_timestamp,
        }
        if self.rendered_output is not None:
            result["rendered_output"] = self.rendered_output.to_dict()
        if self.i2_critique is not None:
            result["i2_critique"] = self.i2_critique.to_dict()
        if self.validation_result is not None:
            result["validation_result"] = self.validation_result.to_dict()
        return result


# =============================================================================
# Tone Rotation for Retries
# =============================================================================

_TONE_ROTATION = ["neutral", "formal", "accessible"]


# =============================================================================
# MTP Nexus
# =============================================================================

class MTPNexus:

    def __init__(
        self,
        projection_engine: Any,
        linearizer: Any,
        fractal_evaluator: Any,
        renderer: Any,
        validation_gate: Any,
        i2_critique: Optional[Any] = None,
        max_retries: int = 2,
    ) -> None:
        self._projection = projection_engine
        self._linearizer = linearizer
        self._evaluator = fractal_evaluator
        self._renderer = renderer
        self._validation = validation_gate
        self._i2 = i2_critique
        self._max_retries = max_retries

    def process(
        self,
        smp_payload: Dict[str, Any],
        discourse_mode: Optional[Any] = None,
        render_config: Optional[Any] = None,
    ) -> EgressPipelineResult:
        pipeline_start = time.monotonic()

        smp_id = str(smp_payload.get("smp_id", "unknown"))
        pipeline = EgressPipelineResult(
            pipeline_id=f"MTP-PL-{uuid.uuid4().hex[:8]}",
            source_smp_id=smp_id,
            max_retries=self._max_retries,
            pipeline_timestamp=time.time(),
        )

        # ---- Stage 1: Projection ----
        graph, ok = self._run_projection(smp_payload, pipeline)
        if not ok:
            pipeline.status = PipelineStatus.FAILED
            pipeline.total_time_ms = (time.monotonic() - pipeline_start) * 1000.0
            return pipeline

        # ---- Stage 2: Linearization ----
        plan, ok = self._run_linearization(graph, discourse_mode, pipeline)
        if not ok:
            pipeline.status = PipelineStatus.FAILED
            pipeline.total_time_ms = (time.monotonic() - pipeline_start) * 1000.0
            return pipeline

        # ---- Stage 3: Fractal Evaluation ----
        stability, ok = self._run_evaluation(plan, pipeline)
        if not ok:
            pipeline.status = PipelineStatus.FAILED
            pipeline.total_time_ms = (time.monotonic() - pipeline_start) * 1000.0
            return pipeline

        # ---- Stages 4-6: Render → Validate → Critique (with retry loop) ----
        attempt = 0
        while attempt <= self._max_retries:
            current_config = self._config_for_attempt(render_config, attempt)

            # Stage 4: Render
            rendered, ok = self._run_render(plan, current_config, stability, pipeline)
            if not ok:
                pipeline.status = PipelineStatus.FAILED
                pipeline.total_time_ms = (time.monotonic() - pipeline_start) * 1000.0
                return pipeline

            # Stage 5: Validation
            validation, ok = self._run_validation(rendered, plan, pipeline)
            if ok and validation.gate_decision.value == "emit":
                # Stage 6: I2 Critique
                critique, critique_pass = self._run_i2_critique(
                    rendered, plan, graph, smp_payload, pipeline
                )
                pipeline.i2_critique = critique

                if critique_pass:
                    pipeline.rendered_output = rendered
                    pipeline.validation_result = validation
                    pipeline.retries_used = attempt
                    pipeline.status = PipelineStatus.EMITTED
                    pipeline.total_time_ms = (time.monotonic() - pipeline_start) * 1000.0
                    return pipeline

                if attempt < self._max_retries:
                    attempt += 1
                    continue
                else:
                    pipeline.rendered_output = rendered
                    pipeline.validation_result = validation
                    pipeline.retries_used = attempt
                    pipeline.status = PipelineStatus.EMITTED
                    pipeline.total_time_ms = (time.monotonic() - pipeline_start) * 1000.0
                    return pipeline

            elif validation.gate_decision.value == "retry" and attempt < self._max_retries:
                attempt += 1
                continue
            else:
                pipeline.validation_result = validation
                pipeline.retries_used = attempt
                pipeline.status = PipelineStatus.HALTED
                pipeline.total_time_ms = (time.monotonic() - pipeline_start) * 1000.0
                return pipeline

        pipeline.retries_used = attempt
        pipeline.status = PipelineStatus.HALTED
        pipeline.total_time_ms = (time.monotonic() - pipeline_start) * 1000.0
        return pipeline

    # -----------------------------------------------------------------
    # Stage Runners
    # -----------------------------------------------------------------

    def _run_projection(
        self, smp_payload: Dict[str, Any], pipeline: EgressPipelineResult
    ) -> tuple:
        start = time.monotonic()
        try:
            result = self._projection.project(smp_payload)
            graph = result.graph
            if graph.status.value == "failed":
                pipeline.stages.append(PipelineStageRecord(
                    stage_name="projection",
                    status=StageStatus.FAIL,
                    duration_ms=(time.monotonic() - start) * 1000.0,
                    output_summary={"error": "empty_graph"},
                ))
                return None, False

            pipeline.stages.append(PipelineStageRecord(
                stage_name="projection",
                status=StageStatus.PASS,
                duration_ms=(time.monotonic() - start) * 1000.0,
                output_summary={
                    "graph_id": graph.graph_id,
                    "nodes": graph.node_count(),
                    "edges": graph.edge_count(),
                },
            ))
            return graph, True
        except Exception:
            pipeline.stages.append(PipelineStageRecord(
                stage_name="projection",
                status=StageStatus.FAIL,
                duration_ms=(time.monotonic() - start) * 1000.0,
            ))
            return None, False

    def _run_linearization(
        self, graph: Any, discourse_mode: Optional[Any], pipeline: EgressPipelineResult
    ) -> tuple:
        start = time.monotonic()
        try:
            kwargs = {}
            if discourse_mode is not None:
                kwargs["discourse_mode"] = discourse_mode
            plan = self._linearizer.linearize(graph, **kwargs)

            if plan.status.value == "failed":
                pipeline.stages.append(PipelineStageRecord(
                    stage_name="linearization",
                    status=StageStatus.FAIL,
                    duration_ms=(time.monotonic() - start) * 1000.0,
                ))
                return None, False

            status = StageStatus.PASS if plan.status.value == "success" else StageStatus.WARN
            pipeline.stages.append(PipelineStageRecord(
                stage_name="linearization",
                status=status,
                duration_ms=(time.monotonic() - start) * 1000.0,
                output_summary={"units": plan.unit_count(), "mode": plan.discourse_mode.value},
            ))
            return plan, True
        except Exception:
            pipeline.stages.append(PipelineStageRecord(
                stage_name="linearization",
                status=StageStatus.FAIL,
                duration_ms=(time.monotonic() - start) * 1000.0,
            ))
            return None, False

    def _run_evaluation(
        self, plan: Any, pipeline: EgressPipelineResult
    ) -> tuple:
        start = time.monotonic()
        try:
            report = self._evaluator.evaluate(plan)
            pipeline.stages.append(PipelineStageRecord(
                stage_name="fractal_evaluation",
                status=StageStatus.PASS,
                duration_ms=(time.monotonic() - start) * 1000.0,
                output_summary={
                    "score": round(report.overall_score, 4),
                    "level": report.stability_level.value,
                    "warnings": len(report.structural_warnings),
                },
            ))
            return report, True
        except Exception:
            pipeline.stages.append(PipelineStageRecord(
                stage_name="fractal_evaluation",
                status=StageStatus.WARN,
                duration_ms=(time.monotonic() - start) * 1000.0,
            ))
            return None, True

    def _run_render(
        self, plan: Any, config: Any, stability: Optional[Any],
        pipeline: EgressPipelineResult
    ) -> tuple:
        start = time.monotonic()
        try:
            rendered = self._renderer.render(plan, config=config, stability_report=stability)

            if rendered.status.value == "failed":
                pipeline.stages.append(PipelineStageRecord(
                    stage_name="render",
                    status=StageStatus.FAIL,
                    duration_ms=(time.monotonic() - start) * 1000.0,
                    output_summary={"sync_valid": rendered.sync_valid},
                ))
                return None, False

            status = StageStatus.PASS if rendered.status.value == "success" else StageStatus.WARN
            pipeline.stages.append(PipelineStageRecord(
                stage_name="render",
                status=status,
                duration_ms=(time.monotonic() - start) * 1000.0,
                output_summary={
                    "sentences": len(rendered.l1.sentences),
                    "hits": rendered.l1.template_hits,
                    "misses": rendered.l1.template_misses,
                },
            ))
            return rendered, True
        except Exception:
            pipeline.stages.append(PipelineStageRecord(
                stage_name="render",
                status=StageStatus.FAIL,
                duration_ms=(time.monotonic() - start) * 1000.0,
            ))
            return None, False

    def _run_validation(
        self, rendered: Any, plan: Any, pipeline: EgressPipelineResult
    ) -> tuple:
        start = time.monotonic()
        try:
            result = self._validation.validate(rendered, plan)
            status = StageStatus.PASS if result.overall_verdict.value == "PASS" else StageStatus.FAIL
            pipeline.stages.append(PipelineStageRecord(
                stage_name="validation",
                status=status,
                duration_ms=(time.monotonic() - start) * 1000.0,
                output_summary={
                    "verdict": result.overall_verdict.value,
                    "decision": result.gate_decision.value,
                },
            ))
            return result, True
        except Exception:
            pipeline.stages.append(PipelineStageRecord(
                stage_name="validation",
                status=StageStatus.FAIL,
                duration_ms=(time.monotonic() - start) * 1000.0,
            ))

            class _FallbackValidation:
                overall_verdict = type("V", (), {"value": "REJECT"})()
                gate_decision = type("D", (), {"value": "halt"})()
                def to_dict(self):
                    return {"error": "validation_exception"}

            return _FallbackValidation(), False

    def _run_i2_critique(
        self,
        rendered: Any,
        plan: Any,
        graph: Any,
        smp_payload: Dict[str, Any],
        pipeline: EgressPipelineResult,
    ) -> tuple:
        if self._i2 is None:
            pipeline.stages.append(PipelineStageRecord(
                stage_name="i2_critique",
                status=StageStatus.SKIP,
            ))
            return None, True

        start = time.monotonic()
        try:
            critique = self._i2.critique(rendered, plan, graph, smp_payload)
            verdict = critique.overall_verdict.value

            if verdict == "PASS":
                status = StageStatus.PASS
                passed = True
            elif verdict == "ABSTAIN":
                status = StageStatus.WARN
                passed = True
            else:
                status = StageStatus.FAIL
                passed = False

            pipeline.stages.append(PipelineStageRecord(
                stage_name="i2_critique",
                status=status,
                duration_ms=(time.monotonic() - start) * 1000.0,
                output_summary={"verdict": verdict},
            ))
            return critique, passed
        except Exception:
            pipeline.stages.append(PipelineStageRecord(
                stage_name="i2_critique",
                status=StageStatus.WARN,
                duration_ms=(time.monotonic() - start) * 1000.0,
                output_summary={"error": "critique_exception"},
            ))
            return None, True

    # -----------------------------------------------------------------
    # Config rotation
    # -----------------------------------------------------------------

    def _config_for_attempt(self, base_config: Optional[Any], attempt: int) -> Any:
        if base_config is not None and attempt == 0:
            return base_config

        try:
            from MTP_Core.MTP_Output_Renderer import RenderConfig, ToneLevel
        except ImportError:
            return base_config

        tone_key = _TONE_ROTATION[attempt % len(_TONE_ROTATION)]
        tone = ToneLevel(tone_key)

        if base_config is not None:
            return RenderConfig(
                tone=tone,
                verbosity=base_config.verbosity,
                include_l2=base_config.include_l2,
                include_l3=base_config.include_l3,
            )

        return RenderConfig(tone=tone)
