# Agent_Safety_Shims Order Of Operations

Entry points:
- Agent.tick(environment=None)
- Agent.halt()
- CapabilityRouter.load_artifact(artifact)
- CapabilityRouter.request(action)
- validate_authz_memory_bounded(artifact)
- enable_bounded_memory_writes()
- disable_bounded_memory_writes()
- router_allows_memory_write(artifact)
- MemorySubstrate.write(entry, artifact=None)
- MemorySubstrate.read_all()
- TickEngine.run(identity, proof, activation_attn, sd_attn, audit_logger)

Step-by-step internal flow:
1. Agent is instantiated with no permissions by default.
2. CapabilityRouter loads artifacts and evaluates requests (deny-all default).
3. MemorySubstrate validates authorization artifacts and enforces bounds.
4. TickEngine invokes LogosProtocolNexus activation and introspective ticks.

Exit points:
- Agent.tick returns status payload.
- MemorySubstrate returns boolean acceptance and logs.
- TickEngine returns collected logs.

Explicit non-operations:
- No autonomous capability grants.
- No external IO beyond controlled logging and nexus calls.
- No agent reasoning or goal selection.
