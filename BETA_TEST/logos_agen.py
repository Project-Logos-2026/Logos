from typing import Dict, Any
from LOGOS_SYSTEM.System_Stack.Logos_Protocol.Runtime_Operations.External_Interface.i2_ingress import SMP

def logos_reason(smp: SMP) -> Dict[str, Any]:
    """
    Deterministic, non-model reasoning.
    No world knowledge. No inference.
    Pattern + intent classification only.
    """

    text = smp.payload["normalized_text"].lower()

    if any(word in text for word in ["hello", "hi", "hey"]):
        intent = "GREETING"
    elif text.endswith("?"):
        intent = "QUESTION"
    elif any(word in text for word in ["do", "run", "execute"]):
        intent = "ACTION_REQUEST"
    else:
        intent = "STATEMENT"

    return {
        "intent": intent,
        "length": len(text),
        "tokens_estimate": len(text.split()),
    }
