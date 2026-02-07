# Cognitive_State_Protocol Order Of Operations

Entry points:
- CSP_Nexus.StandardNexus.register_participant(participant)
- CSP_Nexus.StandardNexus.ingest(packet)
- CSP_Nexus.StandardNexus.tick(causal_intent=None)
- CSP_Nexus.NexusHandle.emit(payload, causal_intent=None)
- World_Modeling.WorldModel.__init__(...)
- World_Modeling.world_model.atomic_write_json(path, payload)

Step-by-step internal flow (Nexus):
1. Participants register and receive a NexusHandle.
2. Inbound packets are ingested and mesh-validated.
3. Tick routes inbound packets to participants.
4. MRE pre-check gates each participant tick.
5. Participants execute deterministically (sorted by id).
6. MRE post-check completes the tick.
7. Participant projections are mesh-validated and routed.
8. Egress payloads are tagged via provisional proof tagging.

Step-by-step internal flow (Memory/UWM):
- UNSPECIFIED (no single entry function defined in inspected sections).

Exit points:
- NexusHandle.emit (ingress to Nexus).
- Participant.project_state (egress projection).
- world_model atomic snapshot writes (file output utilities).

Explicit non-operations:
- No agent reasoning or goal selection.
- No governance authority mutation.
- No autonomous external IO or network calls.
- No tool execution beyond explicit snapshot utilities.
