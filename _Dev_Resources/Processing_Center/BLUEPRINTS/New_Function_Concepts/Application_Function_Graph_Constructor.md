SYSTEM_SPEC — Application_Function_Graph_Constructor
CANONICAL_TARGET: DRAC
ROLE: Executable application-function topology mapper
STATUS: Proposed

OBJECTIVE
Build a DRAC-side subsystem that maps the codebase into an application-function graph usable for:
1. execution topology discovery
2. dependency tracing
3. AF family clustering
4. execution envelope grounding
5. optimization analysis

PRIMARY INPUTS
- Python AST
- function definitions
- class methods
- imports
- call relationships
- AF registry entries
- semantic tags when available

AF ENTRY MODEL
Minimum:
- af_id
- semantic_tag
- category
- function_name

Recommended:
- qualified_name
- file_path
- line_start
- line_end
- dependencies
- signature
- docstring

GRAPH MODEL
Nodes:
- AFs
- module entrypoints
- protocol endpoints
- agent-call surfaces

Edges:
- function_call
- import_dependency
- message_route
- runtime_binding
- protocol_handoff

GRAPH OUTPUTS
- af_dependency_graph.json
- af_call_graph.json
- af_execution_paths.json
- af_family_clusters.json
- graph_summary_report.json

PIPELINE
1. load AF indexes by category
2. build qualified_name → af_id map
3. parse source with AST
4. resolve call relationships
5. create directed edges
6. identify strongly connected regions
7. identify execution families
8. output graph artifacts

CATEGORY INDEX STRATEGY
Use distributed indexes:
- reasoning_engine_index.json
- semantic_processing_index.json
- math_operator_index.json
- agent_control_index.json
- utility_support_index.json
- safety_guard_index.json
- unclassified_index.json

MASTER INDEX
Stores:
- registry pointers
- family summaries
- scoring
- protocol/core affinity
- execution importance
SYSTEM_SPEC — Application_Function_Graph_Constructor
CANONICAL_TARGET: DRAC
ROLE: Executable application-function topology mapper
STATUS: Proposed

OBJECTIVE
Build a DRAC-side subsystem that maps the codebase into an application-function graph usable for:
1. execution topology discovery
2. dependency tracing
3. AF family clustering
4. execution envelope grounding
5. optimization analysis

PRIMARY INPUTS
- Python AST
- function definitions
- class methods
- imports
- call relationships
- AF registry entries
- semantic tags when available

AF ENTRY MODEL
Minimum:
- af_id
- semantic_tag
- category
- function_name

Recommended:
- qualified_name
- file_path
- line_start
- line_end
- dependencies
- signature
- docstring

GRAPH MODEL
Nodes:
- AFs
- module entrypoints
- protocol endpoints
- agent-call surfaces

Edges:
- function_call
- import_dependency
- message_route
- runtime_binding
- protocol_handoff

GRAPH OUTPUTS
- af_dependency_graph.json
- af_call_graph.json
- af_execution_paths.json
- af_family_clusters.json
- graph_summary_report.json

PIPELINE
1. load AF indexes by category
2. build qualified_name → af_id map
3. parse source with AST
4. resolve call relationships
5. create directed edges
6. identify strongly connected regions
7. identify execution families
8. output graph artifacts

CATEGORY INDEX STRATEGY
Use distributed indexes:
- reasoning_engine_index.json
- semantic_processing_index.json
- math_operator_index.json
- agent_control_index.json
- utility_support_index.json
- safety_guard_index.json
- unclassified_index.json

MASTER INDEX
Stores:
- registry pointers
- family summaries
- scoring
- protocol/core affinity
- execution importance

SCORING
Keep scoring in the master index, per your decision.
Suggested fields:
- efficiency
- efficacy
- effectiveness
- stability
- centrality
- protocol_affinity
- core_affinity

WHY DRAC
DRAC is the right location because this tool is about executable reconstruction, dependency topology, and adaptive compilation planning rather than semantic compilation or proof formation.
SCORING
Keep scoring in the master index, per your decision.
Suggested fields:
- efficiency
- efficacy
- effectiveness
- stability
- centrality
- protocol_affinity
- core_affinity

WHY DRAC
DRAC is the right location because this tool is about executable reconstruction, dependency topology, and adaptive compilation planning rather than semantic compilation or proof formation.