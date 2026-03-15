"""
Archon Tooling Orchestrator
Single entry point that runs the full ARCHON_TOOLING analysis suite against
a target repository root and returns a unified result map.

Note: DeterministicRefactorEngine is not invoked automatically because it
can modify files on disk when dry_run=False. Import and invoke it directly
when intentional refactoring is required.
"""

from .semantic_repo_graph import SemanticRepoGraph
from .primitive_extractor import PrimitiveExtractor
from .pattern_miner import PatternMiner
from .constraint_validator import ConstraintValidator


class ArchonToolingOrchestrator:

    def __init__(self, repo_root: str):
        self.repo_root = repo_root

    def run_full_analysis(self) -> dict:
        """
        Execute all read-only analysis tools and return aggregated results.

        Returns
        -------
        dict with keys:
            graph        - semantic repo graph (nodes, edges)
            primitives   - list of all function primitives discovered
            patterns     - dict of function_patterns and import_patterns
            violations   - list of architecture constraint violations
        """
        graph = SemanticRepoGraph(self.repo_root).build()
        primitives = PrimitiveExtractor(self.repo_root).extract()
        patterns = PatternMiner(self.repo_root).mine()
        violations = ConstraintValidator(self.repo_root).validate()

        return {
            "graph": graph,
            "primitives": primitives,
            "patterns": patterns,
            "violations": violations,
        }
