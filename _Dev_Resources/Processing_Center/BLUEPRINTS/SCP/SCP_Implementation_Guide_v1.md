# LOGOS SCP Protocol — Implementation Guide

**Version**: 1.0.0  
**Status**: AUTHORITATIVE  
**Date**: 2026-03-06  
**Entailed From**: SCP_Design_Specification_v1.md  
**Scope**: GPT-processable implementation obligations for SCP system  
**Purpose**: Remove ambiguity at spec→code translation boundary

---

## 1. Overview

This guide translates the Synthetic Cognition Protocol Design Specification into concrete implementation obligations. SCP provides semantic projection, fractal cognition, and geometric analysis for the LOGOS runtime.

**Core Principle** (§1, §3.2): SCP performs semantic analysis but never modifies EAs. All EA writes flow through Logos Agent sovereignty.

**Critical Dependency** (§7.1, INV-SCP-16): SCP Nexus must be injected into I1 sub-agent wrapper before semantic projection can occur.

---

## 2. Component Inventory

### 2.1 Existing Modules (Already Implemented)

All paths relative to: `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Synthetic_Cognition_Protocol/`

| Module | Path | Status | Spec Reference |
|--------|------|--------|----------------|
| SCP_Nexus.py | SCP_Nexus/ | ✓ Exists | §4.1 |
| banach_data_nodes.py | SCP_Core/BDN_System/core/ | ✓ Exists | §4.2 |
| fractal_orbital_node_generator.py | SCP_Core/BDN_System/core/ | ✓ Exists | §4.2 |
| fractal_mvs.py | SCP_Core/MVS_System/MVS_Core/ | ✓ Exists | §4.3 |
| modal_vector_sync.py | SCP_Core/MVS_System/MVS_Core/fractal_orbital/ | ✓ Exists | §4.3 |

### 2.2 Required New Modules

| Module | Path | Purpose | Spec Reference |
|--------|------|---------|----------------|
| Semantic_Scorer.py | SCP_Core/ | Aggregate scores from geometric metrics | §5.5 |
| Trinity_Detector.py | SCP_Core/ | Detect three-fold structures | §6 |
| Fractal_Analysis_Engine.py | SCP_Core/ | Bounded fractal projection | §4.4, §5.3 |

### 2.3 Integration Touch Points

**Existing modules requiring modification**:
- `Logos_Core/Orchestration/Agent_Wrappers.py`: I1 sub-agent wrapper (SCP Nexus injection, semantic projection calls) (§7.1)
- `SCP_Nexus/SCP_Nexus.py`: Integration with new Semantic_Scorer, Trinity_Detector (§4.1)

---

## 3. Implementation Obligations by Spec Section

### 3.1 BDN System (§4.2, §5.2)

**Obligation**: Implement BDN structure, deterministic positioning, and graph management.

**BDN Structure** (§4.2):
```python
# From banach_data_nodes.py (extend existing)
@dataclass
class BanachDataNode:
    node_id: str
    semantic_content: dict        # Extracted meaning elements
    position: tuple[float, ...]   # Coordinates in semantic space
    dimensionality: int           # Semantic complexity measure
    connections: list[str]        # Connected node IDs (DAG only)
    fractal_depth: int           # Recursion level
    metadata: dict               # Creation time, source EA, etc.
    
    def compute_position(content: dict) -> tuple:
        """
        Deterministic positioning (INV-SCP-02, INV-SCP-24).
        
        Algorithm:
        1. Compute SHA-256 hash of serialized content
        2. Convert hash to n-dimensional coordinates
        3. Normalize to unit hypercube [0,1]^n
        
        Returns: Position tuple (x, y, z, ...)
        """
        content_hash = hashlib.sha256(
            json.dumps(content, sort_keys=True).encode()
        ).hexdigest()
        
        # Convert hex to coordinates (example: 3D space)
        coords = []
        for i in range(0, min(len(content_hash), 48), 16):
            hex_chunk = content_hash[i:i+16]
            coord = int(hex_chunk, 16) / (16**16)  # Normalize to [0,1]
            coords.append(coord)
        
        return tuple(coords)
    
    def add_connection(self, target_node_id: str) -> bool:
        """
        Add connection, enforcing DAG constraint (INV-SCP-03).
        
        Must check for cycles before adding.
        Returns: True if added, False if would create cycle
        """
        # Cycle detection required
        if self._would_create_cycle(target_node_id):
            return False
        
        self.connections.append(target_node_id)
        return True
    
    def _would_create_cycle(self, target_node_id: str) -> bool:
        """
        DFS-based cycle detection.
        Returns: True if adding connection would create cycle
        """
        # Implementation: traverse from target back to self
        ...
```

**BDN Creation Protocol** (§5.2, INV-SCP-08):
```python
# In SCP_Nexus.py
def create_bdn(self, ea_id: str, semantic_content: dict) -> BanachDataNode:
    """
    Create new BDN from EA content (idempotent, §5.2).
    
    Pre-conditions:
    - ea_id must be valid
    - semantic_content must be non-empty dict
    
    Post-conditions:
    - BDN added to Nexus graph
    - Event logged to SOP
    - Deterministic: same content → same BDN structure (INV-SCP-08)
    
    Returns: Created BDN
    """
    # 1. Extract semantic elements
    semantic_elements = self._extract_semantic_elements(semantic_content)
    
    # 2. Compute deterministic position (INV-SCP-02)
    position = BanachDataNode.compute_position(semantic_elements)
    
    # 3. Determine dimensionality (complexity heuristic)
    dimensionality = len(semantic_elements.keys())
    
    # 4. Create BDN
    node_id = f"BDN:{ea_id}:{hash(str(position))}"
    bdn = BanachDataNode(
        node_id=node_id,
        semantic_content=semantic_elements,
        position=position,
        dimensionality=dimensionality,
        connections=[],
        fractal_depth=0,  # Set during fractal analysis
        metadata={
            "created_at": datetime.utcnow().isoformat(),
            "source_ea": ea_id
        }
    )
    
    # 5. Add to graph
    self.bdn_graph[node_id] = bdn
    
    # 6. Log event (§10.1)
    self.operational_logger.log_event(
        "scp_bdn_created",
        {
            "bdn_id": node_id,
            "position": str(position),
            "dimensionality": dimensionality,
            "ea_id": ea_id
        }
    )
    
    return bdn
```

### 3.2 MVS System (§4.3, §5.4)

**Obligation**: Implement modal vector synchronization with drift detection and bounded execution.

**MVS Synchronization Protocol** (§5.4, INV-SCP-04, INV-SCP-10):
```python
# In MVS_System/ (extend existing modal_vector_sync.py)
class ModalVectorSync:
    def __init__(self, drift_threshold: float = 0.3):
        self.drift_threshold = drift_threshold
        self.sync_counter = 0
        self.last_sync_tick = 0
    
    def check_sync_trigger(self, ea_count: int) -> bool:
        """
        Check if synchronization should trigger (INV-SCP-04).
        
        Triggers:
        - Every 10 EAs projected
        - On explicit sync request
        
        Returns: True if sync needed
        """
        return (ea_count % 10 == 0) or (ea_count == 0)  # Session start
    
    def synchronize(self, bdn_graph: dict) -> tuple[bool, float]:
        """
        Synchronize BDN positions via geometric optimization (§5.4).
        
        Algorithm:
        1. Compute semantic proximity matrix
        2. Apply geometric optimization (minimize drift)
        3. Update BDN positions in-place
        4. Measure drift score
        
        Constraints (INV-SCP-10):
        - Must complete within single tick
        - Non-blocking execution
        
        Returns: (success, drift_score)
        Raises: MVSFailureError if drift > threshold after sync
        """
        start_time = time.time()
        
        # 1. Compute proximity matrix
        proximity_matrix = self._compute_proximity_matrix(bdn_graph)
        
        # 2. Optimize positions
        optimized_positions = self._geometric_optimization(
            bdn_graph,
            proximity_matrix
        )
        
        # 3. Update positions
        for node_id, new_position in optimized_positions.items():
            bdn_graph[node_id].position = new_position
        
        # 4. Measure drift
        drift_score = self._measure_drift(bdn_graph, proximity_matrix)
        
        # 5. Check threshold (INV-SCP-05)
        success = (drift_score < self.drift_threshold)
        
        # 6. Log sync duration (should be < 1 tick, ~100ms)
        duration_ms = (time.time() - start_time) * 1000
        
        if not success:
            raise MVSFailureError(
                f"Drift {drift_score} exceeds threshold {self.drift_threshold}"
            )
        
        return (success, drift_score)
    
    def _compute_proximity_matrix(self, bdn_graph: dict) -> dict:
        """
        Compute semantic proximity between all BDN pairs.
        
        Proximity metric: 1 / (1 + euclidean_distance(pos1, pos2))
        """
        matrix = {}
        nodes = list(bdn_graph.values())
        
        for i, node1 in enumerate(nodes):
            for node2 in nodes[i+1:]:
                distance = self._euclidean_distance(
                    node1.position,
                    node2.position
                )
                proximity = 1.0 / (1.0 + distance)
                matrix[(node1.node_id, node2.node_id)] = proximity
        
        return matrix
    
    def _geometric_optimization(
        self,
        bdn_graph: dict,
        proximity_matrix: dict
    ) -> dict:
        """
        Optimize BDN positions to minimize drift.
        
        Simple gradient descent approach:
        - Move nodes closer if high semantic proximity
        - Move nodes apart if low semantic proximity
        """
        optimized = {}
        for node_id, bdn in bdn_graph.items():
            # Compute adjustment vector
            adjustment = self._compute_adjustment(bdn, bdn_graph, proximity_matrix)
            
            # Apply adjustment (small step size for stability)
            new_position = tuple(
                bdn.position[i] + 0.1 * adjustment[i]
                for i in range(len(bdn.position))
            )
            
            optimized[node_id] = new_position
        
        return optimized
    
    def _measure_drift(self, bdn_graph: dict, proximity_matrix: dict) -> float:
        """
        Measure total drift score across graph.
        
        Drift = average inconsistency between position distance and semantic proximity
        """
        total_drift = 0.0
        count = 0
        
        for (id1, id2), proximity in proximity_matrix.items():
            pos1 = bdn_graph[id1].position
            pos2 = bdn_graph[id2].position
            distance = self._euclidean_distance(pos1, pos2)
            
            # Inconsistency: proximity should be inverse of distance
            expected_proximity = 1.0 / (1.0 + distance)
            drift = abs(proximity - expected_proximity)
            
            total_drift += drift
            count += 1
        
        return total_drift / count if count > 0 else 0.0
```

### 3.3 Fractal Analysis Engine (§4.4, §5.3)

**Obligation**: Implement bounded fractal projection with recursion depth limit.

**Fractal Analysis Engine** (§5.3, INV-SCP-06, INV-SCP-09):
```python
# New module: Fractal_Analysis_Engine.py
class FractalAnalysisEngine:
    def __init__(self, max_depth: int = 7):
        self.max_depth = max_depth
    
    def analyze_fractal_structure(
        self,
        bdn: BanachDataNode,
        bdn_graph: dict
    ) -> tuple[int, float]:
        """
        Analyze BDN for recursive self-similar patterns (§5.3).
        
        Algorithm:
        1. Detect recursive structures in semantic content
        2. Compute fractal orbit trajectories
        3. Measure self-similarity score
        4. Respect max depth limit (INV-SCP-06, INV-SCP-09)
        
        Returns: (fractal_depth, self_similarity_score)
        """
        # 1. Initialize recursion
        depth = 0
        self_similarity = 0.0
        current_content = bdn.semantic_content
        
        # 2. Recursive descent
        while depth < self.max_depth:
            # Check for self-similar substructure
            substructure = self._extract_substructure(current_content)
            
            if substructure is None:
                break  # No further recursion
            
            # Measure similarity between current and substructure
            similarity = self._compute_similarity(current_content, substructure)
            
            if similarity < 0.5:  # Threshold for self-similarity
                break
            
            self_similarity = max(self_similarity, similarity)
            current_content = substructure
            depth += 1
        
        # 3. Apply penalty if truncated (§9.3, INV-SCP-32)
        if depth >= self.max_depth:
            # Depth limit reached - truncation
            self_similarity -= 0.1  # Penalty
        
        return (depth, self_similarity)
    
    def _extract_substructure(self, content: dict) -> Optional[dict]:
        """
        Extract nested recursive structure if present.
        
        Examples:
        - Lists within lists
        - Dicts within dicts with similar keys
        - Patterns that repeat at smaller scales
        """
        # Check for nested structures
        for key, value in content.items():
            if isinstance(value, dict) and len(value) > 0:
                return value  # Found recursive dict
            elif isinstance(value, list) and len(value) > 0:
                # Check if list elements have structure
                if all(isinstance(x, dict) for x in value):
                    return value[0]  # First element as substructure
        
        return None
    
    def _compute_similarity(self, content1: dict, content2: dict) -> float:
        """
        Measure structural similarity between two semantic contents.
        
        Metric: Jaccard similarity of key sets + value type similarity
        """
        keys1 = set(content1.keys())
        keys2 = set(content2.keys())
        
        # Jaccard similarity
        intersection = keys1 & keys2
        union = keys1 | keys2
        
        if len(union) == 0:
            return 0.0
        
        key_similarity = len(intersection) / len(union)
        
        # Type similarity for overlapping keys
        type_matches = sum(
            1 for k in intersection
            if type(content1[k]) == type(content2[k])
        )
        type_similarity = type_matches / len(intersection) if intersection else 0.0
        
        return (key_similarity + type_similarity) / 2.0
```

### 3.4 Trinity Detector (§6)

**Obligation**: Implement three-fold structure detection with deterministic algorithm.

**Trinity Detection** (§6.2, INV-SCP-14):
```python
# New module: Trinity_Detector.py
class TrinityDetector:
    def detect_trinity_structures(self, bdn_graph: dict) -> list[tuple]:
        """
        Detect three-fold structures in BDN graph (§6.2).
        
        Algorithm:
        1. Find all triangular subgraphs
        2. Check balanced connectivity
        3. Verify semantic complementarity
        
        Returns: List of trinity structures (tuples of 3 node IDs)
        Guarantee (INV-SCP-14): Deterministic and reproducible
        """
        trinities = []
        nodes = list(bdn_graph.values())
        
        # 1. Find triangular subgraphs
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes[i+1:], i+1):
                for k, node3 in enumerate(nodes[j+1:], j+1):
                    # Check if forms triangle
                    if self._is_triangle(node1, node2, node3):
                        # Check semantic complementarity
                        if self._is_semantically_complementary(node1, node2, node3):
                            trinities.append((
                                node1.node_id,
                                node2.node_id,
                                node3.node_id
                            ))
        
        return trinities
    
    def _is_triangle(
        self,
        node1: BanachDataNode,
        node2: BanachDataNode,
        node3: BanachDataNode
    ) -> bool:
        """
        Check if three nodes form balanced triangle (§6.2).
        
        Balanced connectivity: each vertex connects to other two
        """
        # Check all pairwise connections
        has_1_to_2 = node2.node_id in node1.connections
        has_2_to_3 = node3.node_id in node2.connections
        has_3_to_1 = node1.node_id in node3.connections
        
        return has_1_to_2 and has_2_to_3 and has_3_to_1
    
    def _is_semantically_complementary(
        self,
        node1: BanachDataNode,
        node2: BanachDataNode,
        node3: BanachDataNode
    ) -> bool:
        """
        Check if nodes represent distinct but related concepts (§6.2).
        
        Complementarity criteria:
        - Low overlap in semantic content (distinct)
        - High proximity in semantic space (related)
        """
        # Measure content overlap
        keys1 = set(node1.semantic_content.keys())
        keys2 = set(node2.semantic_content.keys())
        keys3 = set(node3.semantic_content.keys())
        
        overlap_12 = len(keys1 & keys2) / len(keys1 | keys2)
        overlap_23 = len(keys2 & keys3) / len(keys2 | keys3)
        overlap_31 = len(keys3 & keys1) / len(keys3 | keys1)
        
        avg_overlap = (overlap_12 + overlap_23 + overlap_31) / 3.0
        
        # Measure spatial proximity
        dist_12 = self._distance(node1.position, node2.position)
        dist_23 = self._distance(node2.position, node3.position)
        dist_31 = self._distance(node3.position, node1.position)
        
        avg_distance = (dist_12 + dist_23 + dist_31) / 3.0
        
        # Complementarity: low overlap + close proximity
        return (avg_overlap < 0.3) and (avg_distance < 0.5)
    
    def _distance(self, pos1: tuple, pos2: tuple) -> float:
        """Euclidean distance between positions"""
        return math.sqrt(sum((a - b)**2 for a, b in zip(pos1, pos2)))
```

### 3.5 Semantic Scorer (§5.5)

**Obligation**: Implement weighted scoring formula with deterministic output.

**Semantic Scoring** (§5.5, INV-SCP-11, INV-SCP-12):
```python
# New module: Semantic_Scorer.py
class SemanticScorer:
    def compute_semantic_score(
        self,
        bdn: BanachDataNode,
        bdn_graph: dict,
        fractal_depth: int,
        self_similarity: float,
        trinity_count: int,
        mvs_synchronized: bool
    ) -> tuple[float, dict]:
        """
        Compute weighted semantic score (§5.5).
        
        Formula:
        semantic_score = (
            0.3 * connectivity_score +
            0.3 * fractal_coherence_score +
            0.2 * position_stability_score +
            0.2 * trinity_alignment_score
        )
        
        Guarantees:
        - Deterministic (INV-SCP-11)
        - Bounded [0.0, 1.0] (INV-SCP-12)
        
        Returns: (semantic_score, score_breakdown)
        """
        # 1. Connectivity score
        connectivity_score = self._compute_connectivity_score(bdn, bdn_graph)
        
        # 2. Fractal coherence score
        fractal_coherence_score = self._compute_fractal_coherence(
            fractal_depth,
            self_similarity
        )
        
        # 3. Position stability score
        position_stability_score = self._compute_position_stability(
            bdn,
            mvs_synchronized
        )
        
        # 4. Trinity alignment score (capped at 0.2, INV-SCP-15)
        trinity_alignment_score = min(
            0.05 * trinity_count if trinity_count == 1 else 0.10,
            0.2  # Cap
        )
        
        # 5. Weighted sum
        semantic_score = (
            0.3 * connectivity_score +
            0.3 * fractal_coherence_score +
            0.2 * position_stability_score +
            0.2 * trinity_alignment_score
        )
        
        # 6. Ensure bounds (INV-SCP-12)
        semantic_score = max(0.0, min(1.0, semantic_score))
        
        # 7. Breakdown for logging
        breakdown = {
            "connectivity": connectivity_score,
            "fractal_coherence": fractal_coherence_score,
            "position_stability": position_stability_score,
            "trinity_alignment": trinity_alignment_score
        }
        
        return (semantic_score, breakdown)
    
    def _compute_connectivity_score(
        self,
        bdn: BanachDataNode,
        bdn_graph: dict
    ) -> float:
        """
        Score based on number and quality of connections.
        
        Formula: min(1.0, connection_count / 10.0)
        """
        connection_count = len(bdn.connections)
        return min(1.0, connection_count / 10.0)
    
    def _compute_fractal_coherence(
        self,
        fractal_depth: int,
        self_similarity: float
    ) -> float:
        """
        Score based on fractal structure depth and self-similarity.
        
        Formula: (depth / max_depth) * self_similarity
        """
        max_depth = 7  # From INV-SCP-06
        depth_score = fractal_depth / max_depth
        return depth_score * self_similarity
    
    def _compute_position_stability(
        self,
        bdn: BanachDataNode,
        mvs_synchronized: bool
    ) -> float:
        """
        Score based on position stability after MVS sync.
        
        If synchronized: high score (0.9)
        If not synchronized: reduced score (0.5)
        """
        return 0.9 if mvs_synchronized else 0.5
```

### 3.6 Integration Points (§7)

**I1 Sub-Agent Wrapper Modification** (§7.1):
```python
# In Agent_Wrappers.py
class I1AgentWrapper:
    def __init__(
        self,
        scp_nexus: SCPNexus,  # Injected dependency (INV-SCP-16)
        uwm: UWM,
        operational_logger: Logger
    ):
        self.scp_nexus = scp_nexus
        self.uwm = uwm
        self.operational_logger = operational_logger
    
    def _on_tick(self, context: dict) -> dict:
        """
        I1 tick processing with SCP semantic projection (§7.1).
        
        Flow:
        1. Extract EA from context
        2. Query UWM for EA content
        3. Invoke SCP projection
        4. Receive semantic score
        5. Construct evaluation AA proposal
        6. Return proposal in tick_result
        """
        # 1. Extract EA ID
        ea_id = context.get("ea_id")
        if not ea_id:
            return {"error": "No EA ID in context"}
        
        # 2. Query UWM for content (§7.3, INV-SCP-18)
        ea = self.uwm.get_smp(ea_id)
        if not ea:
            return {"error": f"EA {ea_id} not found"}
        
        # 3. Invoke SCP projection (§5.1)
        try:
            semantic_score, score_breakdown, geometric_metrics = \
                self.scp_nexus.project_semantic_content(ea_id, ea.payload)
        except Exception as e:
            self.operational_logger.log_error(
                "i1_scp_projection_failed",
                {"ea_id": ea_id, "error": str(e)}
            )
            return {"error": f"SCP projection failed: {e}"}
        
        # 4. Construct evaluation AA proposal (§5.6)
        aa_proposal = {
            "aa_type": "evaluation",
            "content": {
                "semantic_score": semantic_score,
                "geometric_metrics": geometric_metrics,
                "projection_metadata": {
                    "bdn_count": self.scp_nexus.get_bdn_count(),
                    "mvs_synchronized": self.scp_nexus.is_synchronized(),
                    "analysis_timestamp": datetime.utcnow().isoformat()
                }
            },
            "producer": "i1_scp_pipeline",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # 5. Return proposal (Logos Agent will review and attach)
        return {
            "aa_proposal": aa_proposal,
            "semantic_score": semantic_score,
            "score_breakdown": score_breakdown
        }
```

**SCP Nexus Integration** (§4.1, §5):
```python
# In SCP_Nexus.py (extend existing)
class SCPNexus:
    def __init__(self, operational_logger: Logger, rge_context: Optional[dict] = None):
        self.operational_logger = operational_logger
        self.bdn_graph: dict[str, BanachDataNode] = {}
        self.mvs = ModalVectorSync()
        self.fractal_engine = FractalAnalysisEngine()
        self.trinity_detector = TrinityDetector()
        self.semantic_scorer = SemanticScorer()
        self.ea_count = 0
        self.rge_context = rge_context  # Optional RGE integration
    
    def project_semantic_content(
        self,
        ea_id: str,
        content: dict
    ) -> tuple[float, dict, dict]:
        """
        Main semantic projection orchestration (§5).
        
        Flow:
        1. Validate input (INV-SCP-07)
        2. Create BDN (§5.2)
        3. Perform fractal analysis (§5.3)
        4. Check MVS sync trigger (§5.4)
        5. Detect trinity structures (§6)
        6. Compute semantic score (§5.5)
        7. Log events
        8. Return score + breakdown
        
        Returns: (semantic_score, score_breakdown, geometric_metrics)
        Raises: ProjectionError on failures (INV-SCP-28, INV-SCP-29)
        """
        # 1. Validate (INV-SCP-07)
        if not ea_id or not content:
            raise ProjectionError("Invalid EA ID or empty content")
        
        # 2. Create BDN (§5.2)
        try:
            bdn = self.create_bdn(ea_id, content)
        except Exception as e:
            raise ProjectionError(f"BDN creation failed: {e}")
        
        # 3. Fractal analysis (§5.3)
        fractal_depth, self_similarity = self.fractal_engine.analyze_fractal_structure(
            bdn,
            self.bdn_graph
        )
        bdn.fractal_depth = fractal_depth
        
        # Log fractal analysis (§10.1)
        self.operational_logger.log_event(
            "scp_fractal_analyzed",
            {
                "ea_id": ea_id,
                "fractal_depth": fractal_depth,
                "self_similarity_score": self_similarity
            }
        )
        
        # 4. MVS sync check (§5.4, INV-SCP-04)
        self.ea_count += 1
        mvs_synchronized = True
        
        if self.mvs.check_sync_trigger(self.ea_count):
            try:
                success, drift_score = self.mvs.synchronize(self.bdn_graph)
                mvs_synchronized = success
                
                # Log sync (§10.1)
                self.operational_logger.log_event(
                    "scp_mvs_synchronized",
                    {
                        "bdn_count": len(self.bdn_graph),
                        "drift_score": drift_score,
                        "sync_duration_ms": 0  # Computed in MVS
                    }
                )
            except MVSFailureError as e:
                # Log failure (§10.1)
                self.operational_logger.log_event(
                    "scp_mvs_failure",
                    {
                        "drift_score": e.drift_score,
                        "threshold": self.mvs.drift_threshold,
                        "failure_count": self.mvs.failure_count
                    }
                )
                mvs_synchronized = False
        
        # 5. Trinity detection (§6)
        trinities = self.trinity_detector.detect_trinity_structures(self.bdn_graph)
        trinity_count = len(trinities)
        
        if trinity_count > 0:
            # Log trinity detection (§10.1)
            self.operational_logger.log_event(
                "scp_trinity_detected",
                {
                    "node_ids": str(trinities),
                    "trinity_type": "semantic",
                    "confidence": 1.0  # Deterministic detection
                }
            )
        
        # 6. Compute semantic score (§5.5)
        semantic_score, score_breakdown = self.semantic_scorer.compute_semantic_score(
            bdn,
            self.bdn_graph,
            fractal_depth,
            self_similarity,
            trinity_count,
            mvs_synchronized
        )
        
        # Log score (§10.1)
        self.operational_logger.log_event(
            "scp_semantic_scored",
            {
                "ea_id": ea_id,
                "semantic_score": semantic_score,
                "score_breakdown": score_breakdown
            }
        )
        
        # 7. Compile geometric metrics for AA
        geometric_metrics = {
            "connectivity": len(bdn.connections),
            "fractal_depth": fractal_depth,
            "position_stability": score_breakdown["position_stability"],
            "trinity_alignment": trinity_count > 0
        }
        
        return (semantic_score, score_breakdown, geometric_metrics)
    
    def get_bdn_count(self) -> int:
        """Return current BDN count"""
        return len(self.bdn_graph)
    
    def is_synchronized(self) -> bool:
        """Return MVS synchronization status"""
        return self.mvs.last_sync_successful
    
    def on_session_end(self):
        """Clear BDN graph at session end (INV-SCP-22)"""
        self.bdn_graph.clear()
        self.ea_count = 0
```

---

## 4. Error Handling Implementation

### 4.1 BDN Positioning Failures (§9.1, INV-SCP-30)

```python
class BDNPositioningError(Exception):
    """Raised when BDN positioning fails"""
    pass

# In create_bdn()
try:
    position = BanachDataNode.compute_position(semantic_elements)
except Exception as e:
    # Fallback positioning (§9.1)
    self.operational_logger.log_error(
        "scp_bdn_positioning_failed",
        {"ea_id": ea_id, "error": str(e)}
    )
    
    # Random jitter + retry
    position = self._fallback_position()
    
    if position is None:
        # Both attempts failed - propose governance_annotation
        raise BDNPositioningError(f"BDN positioning failed: {e}")
```

### 4.2 MVS Synchronization Failures (§9.2, INV-SCP-31)

```python
class MVSFailureError(Exception):
    def __init__(self, drift_score: float):
        self.drift_score = drift_score
        super().__init__(f"MVS sync failed: drift {drift_score}")

# In SCP Nexus
mvs_failure_count = 0

try:
    success, drift_score = self.mvs.synchronize(self.bdn_graph)
except MVSFailureError as e:
    mvs_failure_count += 1
    
    # Check persistent failure threshold (INV-SCP-31)
    if mvs_failure_count >= 3:
        self.operational_logger.log_critical(
            "scp_mvs_persistent_failure",
            {
                "failure_count": mvs_failure_count,
                "session_id": self.session_id,
                "alert": "SESSION_TERMINATION_REQUIRED"
            }
        )
        raise SessionCorruptionError("Persistent MVS failures - terminating session")
```

### 4.3 Fractal Recursion Overflow (§9.3, INV-SCP-32)

```python
# In FractalAnalysisEngine.analyze_fractal_structure()
if depth >= self.max_depth:
    # Truncation occurred (§9.3)
    self.operational_logger.log_event(
        "scp_fractal_truncated",
        {
            "ea_id": bdn.metadata["source_ea"],
            "depth_limit": self.max_depth
        }
    )
    
    # Apply penalty (INV-SCP-32)
    self_similarity -= 0.1
    
    # Return truncated result (graceful degradation)
    return (self.max_depth, max(0.0, self_similarity))
```

---

## 5. File-Level Implementation Map

### 5.1 SCP_Nexus.py (Modifications)

**Path**: `Synthetic_Cognition_Protocol/SCP_Nexus/SCP_Nexus.py`  
**Spec Reference**: §4.1, §5  
**Status**: Exists, requires integration

**Required additions**:
```python
class SCPNexus:
    def __init__(self, operational_logger, rge_context=None)
    def project_semantic_content(self, ea_id, content) -> tuple[float, dict, dict]
    def create_bdn(self, ea_id, semantic_content) -> BanachDataNode
    def get_bdn_count() -> int
    def is_synchronized() -> bool
    def on_session_end()
```

### 5.2 Semantic_Scorer.py (New)

**Path**: `Synthetic_Cognition_Protocol/SCP_Core/Semantic_Scorer.py`  
**Spec Reference**: §5.5  
**Status**: New module required

**Required methods**:
```python
class SemanticScorer:
    def compute_semantic_score(...) -> tuple[float, dict]
    def _compute_connectivity_score(...) -> float
    def _compute_fractal_coherence(...) -> float
    def _compute_position_stability(...) -> float
```

### 5.3 Trinity_Detector.py (New)

**Path**: `Synthetic_Cognition_Protocol/SCP_Core/Trinity_Detector.py`  
**Spec Reference**: §6  
**Status**: New module required

**Required methods**:
```python
class TrinityDetector:
    def detect_trinity_structures(bdn_graph) -> list[tuple]
    def _is_triangle(node1, node2, node3) -> bool
    def _is_semantically_complementary(node1, node2, node3) -> bool
```

### 5.4 Fractal_Analysis_Engine.py (New)

**Path**: `Synthetic_Cognition_Protocol/SCP_Core/Fractal_Analysis_Engine.py`  
**Spec Reference**: §4.4, §5.3  
**Status**: New module required

**Required methods**:
```python
class FractalAnalysisEngine:
    def __init__(self, max_depth=7)
    def analyze_fractal_structure(bdn, bdn_graph) -> tuple[int, float]
    def _extract_substructure(content) -> Optional[dict]
    def _compute_similarity(content1, content2) -> float
```

### 5.5 Agent_Wrappers.py (Modifications)

**Path**: `Logos_Core/Orchestration/Agent_Wrappers.py`  
**Spec Reference**: §7.1  
**Status**: Requires integration changes

**Required additions**:
```python
class I1AgentWrapper:
    def __init__(self, scp_nexus, uwm, operational_logger)
    def _on_tick(self, context) -> dict:
        # Add SCP projection call
        # Construct evaluation AA proposal
        # Return proposal in tick_result
```

---

## 6. Testing Strategy

### 6.1 Unit Tests

**BDN positioning determinism** (INV-SCP-02, INV-SCP-24):
- Same content → same position (5 repetitions)
- Different content → different positions
- Hash collision handling

**Trinity detection** (INV-SCP-14):
- 3-node triangle → detected
- 3-node non-triangle → not detected
- Semantic complementarity threshold tests

**Semantic scoring** (INV-SCP-11, INV-SCP-12):
- Same inputs → same score (determinism)
- All scores in [0.0, 1.0] bounds
- Trinity cap at 0.2 enforced

**Fractal depth limiting** (INV-SCP-06):
- Recursion stops at depth 7
- Penalty applied on truncation
- Graceful degradation verified

### 6.2 Integration Tests

**Full projection pipeline**:
1. Create EA with semantic content
2. I1 invokes SCP projection
3. Verify BDN created
4. Verify fractal analysis executed
5. Verify semantic score returned
6. Verify evaluation AA proposed
7. Verify Logos Agent receives proposal

**MVS synchronization**:
1. Create 10 EAs to trigger sync
2. Verify MVS synchronize() called
3. Verify BDN positions updated
4. Verify drift < threshold

**Multi-tick with BDN continuity**:
1. Project EA at tick 1
2. Store BDN state in MTP continuity token
3. Restore BDN state at tick 2
4. Extend projection with new EA
5. Verify semantic coherence maintained

### 6.3 Compliance Tests

**Session isolation** (INV-SCP-21, INV-SCP-22):
1. Create BDN graph in session 1
2. End session 1
3. Verify BDN graph cleared
4. Start session 2
5. Verify session 1 BDNs not accessible

**Determinism** (INV-SCP-23):
1. Project identical EA content 5 times
2. Verify all semantic scores identical

**Fail-closed error handling** (INV-SCP-28, INV-SCP-29):
1. Trigger BDN positioning failure
2. Verify no partial score returned
3. Verify error propagated to I1

---

## 7. Deployment Checklist

**Pre-deployment validation**:
- [ ] 3 new modules implemented (Semantic_Scorer, Trinity_Detector, Fractal_Analysis_Engine)
- [ ] SCP_Nexus integration complete
- [ ] I1 sub-agent wrapper modified with SCP Nexus injection
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All compliance tests pass

**Operational readiness**:
- [ ] SCP Nexus injected into I1 wrapper (INV-SCP-16)
- [ ] MVS synchronization triggers operational
- [ ] Fractal depth limit enforced (7 levels)
- [ ] Trinity detection active
- [ ] Evaluation AA production tested
- [ ] Session cleanup verified (BDN graph cleared)

---

## 8. Ambiguities and Escalation Points

### 8.1 RGE Geometric Context Application

**Ambiguity**: Spec states RGE provides geometric context (§7.5) but doesn't specify exact application mechanism.

**Resolution required**:
- How should RGE radii/angles modify BDN positioning?
- Should RGE context override deterministic positioning or augment it?
- What happens if RGE context conflicts with MVS synchronization?

**Recommendation**: V1 treats RGE context as optional advisory input. If present, applies as perturbation to deterministic position. If absent, proceeds normally.

### 8.2 Semantic Element Extraction

**Ambiguity**: Spec requires extracting "semantic elements" from EA payload (§5.2) but doesn't define extraction algorithm.

**Resolution required**:
- What constitutes a "semantic element"?
- Should extraction be syntax-based (dict keys) or analysis-based (NLP)?
- Should different EA types have different extraction strategies?

**Recommendation**: V1 uses simple structural extraction (dict keys + nested structures). V1.1+ could add NLP-based semantic parsing.

### 8.3 BDN Connection Formation

**Ambiguity**: Spec states BDNs have connections but doesn't specify when/how connections are created.

**Resolution required**:
- Are connections based on semantic proximity?
- Are connections based on EA temporal sequence?
- Should connection formation be automatic or manual?

**Recommendation**: V1 creates connections based on semantic proximity (proximity matrix from MVS). Nodes within threshold distance auto-connect.

---

*End of implementation guide.*
