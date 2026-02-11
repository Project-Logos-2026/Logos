# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: EMP_Proof_Index
runtime_layer: operations
role: Runtime module
responsibility: Maintains session-scoped index of verified proofs, dependency
    graphs, axiom footprints, and theorem signatures. Provides search by name,
    axiom usage, or structural pattern. Supports gap detection and coverage
    reporting. Rebuilt on each session via DRAC reconstruction. No persistent state.
agent_binding: None
protocol_binding: Epistemic_Monitoring_Protocol
runtime_classification: runtime_module
boot_phase: E3
expected_imports:
  - typing
  - dataclasses
  - collections
  - pathlib
  - re
provides:
  - ProofEntry
  - DependencyGraph
  - UnprovenReference
  - CoverageReport
  - EMP_Proof_Index
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: Index operations are read-only after population. Missing files or
    parse errors produce empty results, never partial or fabricated data.
rewrite_provenance:
  source: EMP_NATIVE_COQ_PROOF_ENGINE_BLUEPRINT_AND_ROADMAP.md
  rewrite_phase: Phase_E3
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: EMP
  metrics: disabled
---------------------
"""

from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
from pathlib import Path
import re


# =============================================================================
# Data Structures
# =============================================================================

@dataclass
class ProofEntry:
    theorem_name: str
    file_path: str
    proven: bool
    admitted: bool
    axiom_footprint: List[str]
    proof_steps: int
    imports: List[str]
    classification: str = "UNINDEXED"

    @property
    def is_sound(self) -> bool:
        return self.proven and not self.admitted


@dataclass
class DependencyGraph:
    root: str
    edges: Dict[str, List[str]] = field(default_factory=dict)
    nodes: Set[str] = field(default_factory=set)

    def depth(self) -> int:
        if not self.edges:
            return 0
        visited = set()
        return self._dfs_depth(self.root, visited)

    def _dfs_depth(self, node: str, visited: Set[str]) -> int:
        if node in visited or node not in self.edges:
            return 0
        visited.add(node)
        children = self.edges.get(node, [])
        if not children:
            return 1
        return 1 + max(self._dfs_depth(c, visited) for c in children)

    def all_dependencies(self) -> Set[str]:
        result = set()
        self._collect(self.root, result)
        return result - {self.root}

    def _collect(self, node: str, acc: Set[str]) -> None:
        if node in acc:
            return
        acc.add(node)
        for child in self.edges.get(node, []):
            self._collect(child, acc)


@dataclass
class UnprovenReference:
    name: str
    declaration_type: str
    file_path: str
    referenced_by: List[str] = field(default_factory=list)


@dataclass
class CoverageReport:
    total_theorems: int
    proven_count: int
    admitted_count: int
    unproven_count: int
    total_axioms: int
    pxl_kernel_axioms_used: int
    non_kernel_axioms: List[str]
    files_indexed: int
    coverage_percentage: float
    gaps: List[UnprovenReference] = field(default_factory=list)


# =============================================================================
# Coq Source Parsers
# =============================================================================

_THEOREM_DECL = re.compile(
    r"\b(Theorem|Lemma|Corollary|Proposition|Definition|Fixpoint)\s+(\w+)"
)
_AXIOM_DECL = re.compile(r"\b(Axiom|Parameter|Hypothesis)\s+(\w+)")
_REQUIRE_IMPORT = re.compile(r"(?:From\s+\w+\s+)?Require\s+(?:Import|Export)\s+([\w\s.]+)\.")
_ADMITTED = re.compile(r"\bAdmitted\.")
_QED = re.compile(r"\b(?:Qed|Defined)\.")
_PROOF_START = re.compile(r"\bProof\.")


def _parse_v_file(path: Path) -> Dict[str, Any]:
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {"theorems": [], "axioms": [], "imports": [], "source": ""}

    theorems = _THEOREM_DECL.findall(source)
    axioms = _AXIOM_DECL.findall(source)

    raw_imports = _REQUIRE_IMPORT.findall(source)
    imports = []
    for imp in raw_imports:
        for module_name in imp.split():
            module_name = module_name.strip().rstrip(".")
            if module_name:
                imports.append(module_name)

    proof_blocks = []
    lines = source.split("\n")
    current_theorem = None
    has_admitted = False

    for line in lines:
        th_match = _THEOREM_DECL.search(line)
        if th_match:
            current_theorem = th_match.group(2)
            has_admitted = False

        if _ADMITTED.search(line) and current_theorem:
            proof_blocks.append((current_theorem, True))
            current_theorem = None

        if _QED.search(line) and current_theorem:
            proof_blocks.append((current_theorem, False))
            current_theorem = None

    theorem_status = {}
    for name, admitted in proof_blocks:
        theorem_status[name] = admitted

    return {
        "theorems": theorems,
        "axioms": axioms,
        "imports": imports,
        "theorem_status": theorem_status,
        "source": source,
    }


# =============================================================================
# EMP Proof Index
# =============================================================================

class EMP_Proof_Index:
    """
    Session-scoped proof index.

    Maintains an index of all verified proofs, their dependency graphs,
    axiom footprints, and theorem signatures. Rebuilt on each session.

    NO REASONING. NO MUTATION. READ-ONLY INDEX AFTER POPULATION.
    """

    def __init__(self):
        self._entries: Dict[str, ProofEntry] = {}
        self._file_entries: Dict[str, List[str]] = defaultdict(list)
        self._axiom_index: Dict[str, List[str]] = defaultdict(list)
        self._import_graph: Dict[str, List[str]] = defaultdict(list)
        self._axiom_declarations: Dict[str, str] = {}
        self._files_indexed: Set[str] = set()

    # -------------------------------------------------------------------------
    # Indexing
    # -------------------------------------------------------------------------

    def index_file(self, file_path: str, verification_result=None) -> int:
        path = Path(file_path)
        parsed = _parse_v_file(path)

        if not parsed["theorems"] and not parsed["axioms"]:
            self._files_indexed.add(file_path)
            return 0

        count = 0
        classification = "UNVERIFIED"
        if verification_result is not None:
            if getattr(verification_result, "verified", False):
                classification = "VERIFIED"

        for decl_type, name in parsed["theorems"]:
            admitted = parsed["theorem_status"].get(name, False)
            proven = name in parsed["theorem_status"] and not admitted

            entry = ProofEntry(
                theorem_name=name,
                file_path=file_path,
                proven=proven,
                admitted=admitted,
                axiom_footprint=[ax_name for _, ax_name in parsed["axioms"]],
                proof_steps=0,
                imports=parsed["imports"],
                classification=classification,
            )
            self._entries[name] = entry
            self._file_entries[file_path].append(name)

            for _, ax_name in parsed["axioms"]:
                self._axiom_index[ax_name].append(name)

            count += 1

        for decl_type, ax_name in parsed["axioms"]:
            self._axiom_declarations[ax_name] = file_path

        self._import_graph[file_path] = parsed["imports"]
        self._files_indexed.add(file_path)

        return count

    def index_directory(self, directory: str) -> int:
        root = Path(directory)
        if not root.is_dir():
            return 0

        total = 0
        for v_file in sorted(root.rglob("*.v")):
            total += self.index_file(str(v_file))
        return total

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(self, query: str) -> List[ProofEntry]:
        query_lower = query.lower()
        results = []
        for name, entry in self._entries.items():
            if query_lower in name.lower():
                results.append(entry)
        return results

    def search_by_axiom(self, axiom_name: str) -> List[ProofEntry]:
        theorem_names = self._axiom_index.get(axiom_name, [])
        return [self._entries[n] for n in theorem_names if n in self._entries]

    def get_entry(self, theorem_name: str) -> Optional[ProofEntry]:
        return self._entries.get(theorem_name)

    # -------------------------------------------------------------------------
    # Dependency Graphs
    # -------------------------------------------------------------------------

    def get_dependency_graph(self, theorem_name: str) -> Optional[DependencyGraph]:
        entry = self._entries.get(theorem_name)
        if entry is None:
            return None

        graph = DependencyGraph(root=theorem_name)
        graph.nodes.add(theorem_name)

        file_imports = self._import_graph.get(entry.file_path, [])
        for imp in file_imports:
            graph.edges.setdefault(theorem_name, []).append(imp)
            graph.nodes.add(imp)

        return graph

    # -------------------------------------------------------------------------
    # Axiom Footprint
    # -------------------------------------------------------------------------

    def get_axiom_footprint(self, theorem_name: str) -> List[str]:
        entry = self._entries.get(theorem_name)
        if entry is None:
            return []
        return list(entry.axiom_footprint)

    # -------------------------------------------------------------------------
    # Gap Detection
    # -------------------------------------------------------------------------

    def find_gaps(self) -> List[UnprovenReference]:
        gaps = []
        for ax_name, file_path in self._axiom_declarations.items():
            if ax_name not in self._entries or not self._entries[ax_name].proven:
                referencing = self._axiom_index.get(ax_name, [])
                gaps.append(
                    UnprovenReference(
                        name=ax_name,
                        declaration_type="Axiom/Parameter",
                        file_path=file_path,
                        referenced_by=referencing,
                    )
                )
        return gaps

    # -------------------------------------------------------------------------
    # Coverage Report
    # -------------------------------------------------------------------------

    def coverage_report(self, pxl_kernel_axioms: Optional[set] = None) -> CoverageReport:
        total = len(self._entries)
        proven = sum(1 for e in self._entries.values() if e.proven and not e.admitted)
        admitted = sum(1 for e in self._entries.values() if e.admitted)
        unproven = total - proven - admitted

        all_axioms = set(self._axiom_declarations.keys())
        kernel = pxl_kernel_axioms or set()
        kernel_used = all_axioms & kernel
        non_kernel = sorted(all_axioms - kernel)

        coverage = (proven / total * 100.0) if total > 0 else 0.0

        return CoverageReport(
            total_theorems=total,
            proven_count=proven,
            admitted_count=admitted,
            unproven_count=unproven,
            total_axioms=len(all_axioms),
            pxl_kernel_axioms_used=len(kernel_used),
            non_kernel_axioms=non_kernel,
            files_indexed=len(self._files_indexed),
            coverage_percentage=round(coverage, 2),
            gaps=self.find_gaps(),
        )

    # -------------------------------------------------------------------------
    # Introspection (Safe)
    # -------------------------------------------------------------------------

    def status(self) -> Dict[str, Any]:
        return {
            "entries_count": len(self._entries),
            "files_indexed": len(self._files_indexed),
            "axioms_tracked": len(self._axiom_declarations),
            "proven_theorems": sum(
                1 for e in self._entries.values() if e.is_sound
            ),
        }
