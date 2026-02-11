# DRAC Order Of Operations

Entry points:
- DRACCore.start_phase(phase_id)
- DRACCore.complete_phase(notes=None)
- DRACCore.status()
- DRAC_Nexus.StandardNexus.register_participant(participant)
- DRAC_Nexus.StandardNexus.ingest(packet)
- DRAC_Nexus.StandardNexus.tick(causal_intent=None)
- DRAC_Nexus.NexusHandle.emit(payload, causal_intent=None)

Step-by-step internal flow (Core):
1. start_phase creates a DRACPhaseState and marks it active.
2. complete_phase finalizes the active phase and records completion.
3. status reports active phase and completion counts.

Step-by-step internal flow (Nexus):
1. Participants register and receive a NexusHandle.
2. Inbound packets are ingested and mesh-validated.
3. Tick routes inbound packets to participants.
4. MRE pre-check gates each participant tick.
5. Participants execute deterministically (sorted by id).
6. MRE post-check completes the tick.
7. Participant projections are mesh-validated and routed.
8. Egress payloads are tagged via provisional proof tagging.

Exit points:
- DRACCore.status for safe introspection.
- NexusHandle.emit (ingress) and Participant.project_state (egress).

Explicit non-operations:
- No inference or epistemic evaluation.
- No governance authority mutation.
- No autonomous external IO or network calls.
