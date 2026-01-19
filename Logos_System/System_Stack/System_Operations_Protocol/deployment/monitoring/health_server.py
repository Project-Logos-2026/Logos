# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: health_server
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
  source: System_Stack/System_Operations_Protocol/deployment/monitoring/health_server.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from datetime import datetime

import requests
from fastapi import FastAPI

app = FastAPI(title="LOGOS Health Monitor")


@app.get("/")
async def health_dashboard():
    services = {
        "LOGOS API": "http://localhost:8090/health",
        "Demo Interface": "http://localhost:8080/health",
    }

    status = {}
    for name, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            status[name] = {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": response.elapsed.total_seconds() * 1000,
                "last_check": datetime.now().isoformat(),
            }
        except Exception as e:
            status[name] = {
                "status": "unreachable",
                "error": str(e),
                "last_check": datetime.now().isoformat(),
            }

    overall_health = all(s["status"] == "healthy" for s in status.values())

    return {
        "overall_health": "healthy" if overall_health else "degraded",
        "services": status,
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8099)
