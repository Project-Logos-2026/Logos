# EMP Order Of Operations

Entry points:
- EMP_Meta_Reasoner.analyze(artifact)
- EMP_Nexus.PreProcessGate.apply(packet)
- EMP_Nexus.PostProcessGate.apply(packet)
- EMP_Nexus.StandardNexus.register_participant(participant)
- EMP_Nexus.StandardNexus.ingest(packet)
- EMP_Nexus.StandardNexus.tick(causal_intent=None)
- EMP_Nexus.NexusHandle.emit(payload, causal_intent=None)

Step-by-step internal flow (Meta Reasoner):
1. analyze uses a bounded reasoning budget.
2. artifact proof_state decides epistemic_state assignment.
3. reasoning_steps_used is recorded.

Step-by-step internal flow (Nexus):
1. PreProcessGate validates structural admissibility.
2. Inbound packets are ingested and mesh-validated.
3. Tick routes inbound packets to participants.
4. MRE pre-check gates each participant tick.
5. Participants execute deterministically (sorted by id).
6. MRE post-check completes the tick.
7. PostProcessGate applies provisional proof tagging.
8. Participant projections are routed downstream.

Exit points:
- PostProcessGate tagging and egress packet routing.
- NexusHandle.emit (ingress) and Participant.project_state (egress).

Explicit non-operations:
- No agent reasoning or goal selection.
- No governance authority mutation.
- No autonomous external IO or network calls.
