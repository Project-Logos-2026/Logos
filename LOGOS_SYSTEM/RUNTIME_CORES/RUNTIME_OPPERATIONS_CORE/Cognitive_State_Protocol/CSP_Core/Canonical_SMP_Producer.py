import hashlib
import time
from typing import List
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Cognitive_State_Protocol.CSP_Core.Unified_Working_Memory.SMP_Schema import SMP, AppendArtifact, SMPHeader, SMPProvenance

class CanonicalSMPProducer:
    def produce(self, source_smp: SMP, aas: List[AppendArtifact]) -> SMP:
        aa_hashes = ''.join([aa.aa_hash for aa in aas])
        new_id = "C-SMP:" + hashlib.sha256((source_smp.header.smp_id + aa_hashes).encode()).hexdigest()
        new_chain = list(source_smp.provenance.chain_of_custody) + ["canonical_producer"]
        new_provenance = SMPProvenance(
            source=source_smp.provenance.source,
            acquisition_path=source_smp.provenance.acquisition_path,
            content_hash=hashlib.sha256((str(source_smp.payload) + aa_hashes).encode()).hexdigest(),
            chain_of_custody=new_chain
        )
        new_header = SMPHeader(
            smp_id=new_id,
            smp_type=source_smp.header.smp_type,
            classification_state="canonical",
            created_at=time.time(),
            created_by="logos_agent",
            session_id=source_smp.header.session_id
        )
        new_smp = SMP(
            header=new_header,
            provenance=new_provenance,
            confidence=source_smp.confidence,
            privation=source_smp.privation,
            payload=source_smp.payload,
            append_artifacts=source_smp.append_artifacts
        )
        return new_smp
