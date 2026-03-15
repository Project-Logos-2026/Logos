"""
Epistemic_Expansion_Engine
Orchestrates the full semantic ingestion and epistemic analysis pipeline.

Pipeline:
    SemanticExtractor
        down  nuggets
    SemanticClusterMapper
        down  clusters
    LogicalCompressionEngine
        down  compressed artifacts
    PrincipleDiscoveryEngine
        down  principles
    EpistemicTopologyEngine
        down  epistemic graph
    (returned to Cognitive Compiler / Nexus)

The ApplicationFunctionGraphConstructor provides a parallel pathway for
source-code inputs, appending function-graph nodes into the epistemic graph
before it is returned to the caller.
"""

from Semantic_Extractor import SemanticExtractor
from Semantic_Cluster_Mapper import SemanticClusterMapper
from Logical_Compression_Engine import LogicalCompressionEngine
from Principle_Discovery_Engine import PrincipleDiscoveryEngine
from Epistemic_Topology_Engine import EpistemicTopologyEngine
from Application_Function_Graph_Constructor import ApplicationFunctionGraphConstructor


class EpistemicExpansionEngine:
    """
    Wires all six analysis engines into a single deterministic pipeline.

    Usage
    -----
    engine = EpistemicExpansionEngine()

    # Text document ingestion
    result = engine.run(text_block="...", source_path="path/to/doc.md")

    # With optional source-code topology appended
    result = engine.run(
        text_block="...",
        source_path="path/to/module.py",
        source_code=open("path/to/module.py").read(),
    )
    """

    def __init__(self):
        self.extractor = SemanticExtractor()
        self.cluster_mapper = SemanticClusterMapper()
        self.compressor = LogicalCompressionEngine()
        self.principle_engine = PrincipleDiscoveryEngine()
        self.topology_engine = EpistemicTopologyEngine()
        self.af_graph = ApplicationFunctionGraphConstructor()

    def run(
        self,
        text_block: str,
        source_path: str,
        source_code: str = "",
    ) -> dict:
        """
        Execute the full epistemic expansion pipeline.

        Parameters
        ----------
        text_block  : natural-language text to ingest
        source_path : originating file path (used for nugget provenance)
        source_code : optional Python source; when provided, function-graph
                      nodes are merged into the epistemic graph

        Returns
        -------
        dict with keys:
            nuggets           - raw semantic nuggets
            clusters          - cluster topology
            compressed        - compressed logical artifacts
            principles        - discovered invariant principles
            epistemic_graph   - final graph {nodes, edges}
            function_graph    - DRAC function graph (empty list if no source_code)
        """
        # Stage 1 - semantic extraction
        nuggets = self.extractor.extract(text_block, source_path)

        # Stage 2 - cluster mapping
        clusters = self.cluster_mapper.cluster(nuggets)

        # Stage 3 - logical compression
        compressed = self.compressor.compress(nuggets)

        # Stage 4 - principle discovery
        principles = self.principle_engine.discover(compressed)

        # Stage 5 - epistemic topology (compressed + principles)
        all_artifacts = compressed + principles
        epistemic_graph = self.topology_engine.build_graph(all_artifacts)

        # Stage 6 (parallel) - application function graph from source code
        function_graph = []
        if source_code:
            try:
                function_graph = self.af_graph.build(source_code)
                # Append function nodes into the epistemic graph
                for fn in function_graph:
                    epistemic_graph["nodes"].append(fn["name"])
                    for dep in fn["dependencies"]:
                        epistemic_graph["edges"].append((fn["name"], dep))
            except SyntaxError:
                pass  # source_code not parseable - skip without raising

        return {
            "nuggets": nuggets,
            "clusters": clusters,
            "compressed": compressed,
            "principles": principles,
            "epistemic_graph": epistemic_graph,
            "function_graph": function_graph,
        }
