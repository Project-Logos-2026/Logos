from __future__ import annotations
'\nLOGOS_MODULE_METADATA\n---------------------\nmodule_name: cycle_runner\nruntime_layer: inferred\nrole: inferred\nagent_binding: None\nprotocol_binding: None\nboot_phase: inferred\nexpected_imports: []\nprovides: []\ndepends_on_runtime_state: False\nfailure_mode:\n  type: unknown\n  notes: ""\nrewrite_provenance:\n  source: System_Stack/Logos_Agents/I1_Agent/protocol_operations/scp_cycle/cycle_runner.py\n  rewrite_phase: Phase_B\n  rewrite_timestamp: 2026-01-18T23:03:31.726474\nobservability:\n  log_channel: None\n  metrics: disabled\n---------------------\n'
from typing import Any, Dict
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I1_Agent.protocol_operations.scp_runtime.smp_intake import load_smp
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I1_Agent.protocol_operations.scp_runtime.work_order import build_work_order
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I1_Agent.protocol_operations.scp_runtime.result_packet import emit_result_packet
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I1_Agent.protocol_operations.scp_transform.iterative_loop import run_iterative_stabilization
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I1_Agent.protocol_operations.scp_cycle.policy import decide_policy

def run_scp_cycle(*, smp: Dict[str, Any], payload: Any=None) -> Any:
    """
    One SCP cycle:
      - Validate SMP
      - Build work order
      - Optionally run bounded stabilization loop
      - Emit append-only SCPResultPacket
    'payload' is optional; if omitted SCP operates on metadata only.
    """
    env = load_smp(smp=smp)
    wo = build_work_order(envelope=env)
    pol = decide_policy(smp=env.raw)
    if not pol.run_loop:
        return emit_result_packet(smp_id=env.smp_id, status='ok', summary=f'SCP cycle skipped loop: {pol.reason}', score_vector=env.triadic_scores, findings={'work_order': {'priority': wo.priority, 'objectives': wo.objectives, 'selected_domains': wo.selected_domains, 'constraints': wo.constraints}}, recommended_next={'route_to': 'LOGOS'}, reference_obj=env.input_hash)
    outcome = run_iterative_stabilization(payload=payload if payload is not None else {'smp_id': env.smp_id, 'input_hash': env.input_hash}, context={'work_order': wo.__dict__, 'smp_id': env.smp_id})
    step_summary = [{'name': s.name, 'applied': s.applied, 'notes': s.notes} for s in outcome.steps]
    return emit_result_packet(smp_id=env.smp_id, status=outcome.status, summary=f'SCP loop ran: {outcome.summary} ({pol.reason})', score_vector=outcome.score_vector or env.triadic_scores, findings={'work_order': {'priority': wo.priority, 'objectives': wo.objectives, 'selected_domains': wo.selected_domains, 'constraints': wo.constraints}, 'transform_steps': step_summary}, recommended_next={'route_to': 'LOGOS'}, reference_obj=env.input_hash)