# SOP Order Of Operations

Entry points:
- SOP_Nexus.StandardNexus.register_participant(participant)
- SOP_Nexus.StandardNexus.ingest(packet)
- SOP_Nexus.StandardNexus.tick(causal_intent=None)
- SOP_Nexus.NexusHandle.emit(payload, causal_intent=None)
- scan_bypass.scan_for_bypasses()
- scan_bypass.scan_for_todos()
- scan_bypass.main()

Step-by-step internal flow (Nexus):
1. Participants register and receive a NexusHandle.
2. Inbound packets are ingested and mesh-validated.
3. Tick routes inbound packets to participants.
4. MRE pre-check gates each participant tick.
5. Participants execute deterministically (sorted by id).
6. MRE post-check completes the tick.
7. Participant projections are mesh-validated and routed.
8. Egress payloads are tagged via provisional proof tagging.

Step-by-step internal flow (scan_bypass):
1. scan_for_bypasses scans repository files for bypass patterns.
2. scan_for_todos scans for security-related TODO markers.
3. main aggregates results and returns a status code.

Exit points:
- NexusHandle.emit (ingress) and Participant.project_state (egress).
- scan_bypass returns exit codes from main.

Explicit non-operations:
- No agent reasoning or goal selection.
- No governance authority mutation.
- No network calls or external system execution.
