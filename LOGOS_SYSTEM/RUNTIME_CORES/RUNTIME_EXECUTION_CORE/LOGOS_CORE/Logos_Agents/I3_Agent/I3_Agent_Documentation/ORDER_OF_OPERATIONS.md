# I3_Agent Order Of Operations

Entry points:
- I3_Nexus.StandardNexus.register_participant(participant)
- I3_Nexus.StandardNexus.ingest(packet)
- I3_Nexus.StandardNexus.tick(causal_intent=None)
- I3_Nexus.NexusHandle.emit(payload, causal_intent=None)
- MindPrincipalOperator.build_plan_skeleton(...)
- MindPrincipalOperator.apply_to_packet(packet, ...)
- OmnipresenceIntegration.compute_metrics(...)
- OmnipresenceIntegration.enrich_packet(...)

Step-by-step internal flow (Nexus):
1. Participants register and receive a NexusHandle.
2. Inbound packets are ingested and mesh-validated.
3. Tick routes inbound packets to participants.
4. MRE pre-check gates each participant tick.
5. Participants execute deterministically (sorted by id).
6. MRE post-check completes the tick.
7. Participant projections are mesh-validated and routed.
8. Egress payloads are tagged via provisional proof tagging.

Step-by-step internal flow (Core integrations):
1. Mind Principal operator builds deterministic plan skeletons.
2. OmniProperty integration computes context-span metrics.
3. Enriched packets return without semantic mutation.

Step-by-step internal flow (protocol_operations):
- UNSPECIFIED (module-level flow not inspected here).

Exit points:
- NexusHandle.emit (ingress) and Participant.project_state (egress).
- Enrichment functions return modified packet copies.

Explicit non-operations:
- No autonomous inference or goal selection.
- No governance authority mutation.
- No external IO or tool execution.
