from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any
import uuid

@dataclass
class SMP:
    smp_id: str
    source: str
    timestamp: str
    payload: Dict[str, Any]
    status: str = "PROVISIONAL"

def build_smp(raw_text: str) -> SMP:
    return SMP(
        smp_id=str(uuid.uuid4()),
        source="external_http",
        timestamp=datetime.utcnow().isoformat(),
        payload={"text": raw_text}
    )
