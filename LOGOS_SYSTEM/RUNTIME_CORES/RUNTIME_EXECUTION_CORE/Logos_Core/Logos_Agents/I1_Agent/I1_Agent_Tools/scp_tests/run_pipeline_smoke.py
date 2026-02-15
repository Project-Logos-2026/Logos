from __future__ import annotations
'\nLOGOS_MODULE_METADATA\n---------------------\nmodule_name: run_pipeline_smoke\nruntime_layer: inferred\nrole: inferred\nagent_binding: None\nprotocol_binding: None\nboot_phase: inferred\nexpected_imports: []\nprovides: []\ndepends_on_runtime_state: False\nfailure_mode:\n  type: unknown\n  notes: ""\nrewrite_provenance:\n  source: System_Stack/Logos_Agents/I1_Agent/protocol_operations/scp_tests/run_pipeline_smoke.py\n  rewrite_phase: Phase_B\n  rewrite_timestamp: 2026-01-18T23:03:31.726474\nobservability:\n  log_channel: None\n  metrics: disabled\n---------------------\n'
import json
import sys
from typing import Any, Dict
from .sample_smp import make_sample_smp
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I1_Agent.protocol_operations.scp_integrations.pipeline_runner import run_scp_pipeline

def main() -> int:
    smp = make_sample_smp()
    result = run_scp_pipeline(smp=smp, payload_ref={'opaque': True, 'input_hash': smp['input_reference']['input_hash']})
    out = result.to_dict() if hasattr(result, 'to_dict') else result
    print(json.dumps(out, indent=2, ensure_ascii=False, sort_keys=False))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())