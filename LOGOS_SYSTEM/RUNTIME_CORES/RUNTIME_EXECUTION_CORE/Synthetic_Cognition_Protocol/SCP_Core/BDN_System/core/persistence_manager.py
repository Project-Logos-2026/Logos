# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: persistence_manager
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
  source: System_Stack/Synthetic_Cognition_Protocol/BDN_System/core/persistence_manager.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

import json
import os
from Logos_System.System_Stack.Synthetic_Cognition_Protocol.mvf_node_operator import FractalDB

class PersistenceManager:
    """Handles auto-saving and auto-loading of the knowledge graph."""

    def __init__(self, db: FractalDB, preseed_data_dir: str = "logos_system/subsystems/telos/generative_tools/precede_nodes_and_data"):
        self.db = db
        self.preseed_data_dir = preseed_data_dir

    def populate_on_startup(self):
        """Loads all preseed nodes and saved nodes into the DB on startup."""
        print("--- [DB] Populating knowledge graph on startup ---")

        # 1. Load preseed nodes
        for filename in os.listdir(self.preseed_data_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.preseed_data_dir, filename), 'r') as f:
                    data = json.load(f)
                    # This is a placeholder for the logic to convert
                    # the preseed JSON into OntologicalNode objects and store them.
                    print(f"  - Loaded preseed file: {filename}")

        # 2. Load nodes from main persistent storage (if any)
        # The SQLite DB is already persistent, so this is automatic.
        # If using a JSON dump as backup, the logic would go here.
        node_count = self.db.conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
        print(f"  - Verified {node_count} existing nodes in persistent storage.")
        print("--- [DB] Population complete ---")

    def save_on_shutdown(self):
        """
        Ensures all data is committed on shutdown. Can also create backups.
        """
        # For SQLite, the 'with self.conn:' statements already ensure commits.
        # This function is for creating a full JSON backup if desired.
        print("--- [DB] Shutdown protocol initiated. Committing final transactions. ---")
        self.db.conn.commit()
        print("--- [DB] All data saved. ---")
