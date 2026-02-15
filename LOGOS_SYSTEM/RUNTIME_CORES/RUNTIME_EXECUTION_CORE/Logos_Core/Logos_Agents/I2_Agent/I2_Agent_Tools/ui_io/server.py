"""
LOGOS_MODULE_METADATA
---------------------
module_name: server
runtime_layer: inferred
role: inferred
agent_binding: None
protocol_binding: None
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: System_Stack/Logos_Agents/I2_Agent/protocol_operations/ui_io/server.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I2_Agent.protocol_operations.ui_io.adapter import handle_inbound
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

class InboundPacket(BaseModel):
    payload: str

@app.post('/ingest')
async def ingest(packet: InboundPacket):
    response = handle_inbound(inbound=packet.payload, default_route='LOGOS')
    return {'route': response.route, 'priority': response.priority, 'reason': response.reason, 'payload': response.payload}