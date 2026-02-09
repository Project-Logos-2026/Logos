from LOGOS_SYSTEM.System_Stack.Logos_Protocol.Runtime_Operations.External_Interface.i2_ingress import SMP

def sop_accept(smp: SMP) -> bool:
    # Hard fail-closed for now
    if not smp.payload.get("normalized_text"):
        return False
    return True
