# I1_Agent Order Of Operations

Entry points:
- I1_Nexus.StandardNexus.register_participant(participant)
- I1_Nexus.StandardNexus.ingest(packet)
- I1_Nexus.StandardNexus.tick(causal_intent=None)
- I1_Nexus.NexusHandle.emit(payload, causal_intent=None)
- OmniscienceIntegration.compute_metrics(...)
- OmniscienceIntegration.enrich_packet(...)
- SignPrincipalOperator.anchor(token)
- SignPrincipalOperator.resolve_tokens(tokens)
- SignPrincipalOperator.coherence_check()
- SignPrincipalOperator.apply_to_packet(packet, ...)

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
1. OmniProperty integration computes deterministic coverage metrics.
2. Sign Principal operator resolves tokens and emits trace metadata.
3. Enriched packets return without semantic mutation.

Step-by-step internal flow (protocol_operations):
- UNSPECIFIED (module-level flow not inspected here).

Exit points:
- NexusHandle.emit (ingress) and Participant.project_state (egress).
- Enrichment functions return modified packet copies.

Explicit non-operations:
- No autonomous inference or belief formation.
- No governance authority mutation.
- No external IO or tool execution.
