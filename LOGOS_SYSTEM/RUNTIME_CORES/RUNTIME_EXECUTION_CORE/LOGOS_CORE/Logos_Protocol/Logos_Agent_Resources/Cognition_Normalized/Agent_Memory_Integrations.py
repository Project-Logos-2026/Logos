# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: Agent_Memory_Integrations
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/Logos_Agent_Resources/Cognition_Normalized/Agent_Memory_Integrations.py.
agent_binding: None
protocol_binding: Logos_Protocol
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/Logos_Agent_Resources/Cognition_Normalized/Agent_Memory_Integrations.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

# ==================== AGENT REPLAY ADAPTER ====================

class AgentReplayAdapter:
    """
    Adapter that gives agents access to the replay infrastructure
    Handles state persistence, event logging, and memory access
    """
    
    def __init__(self, 
                 agent_id: str,
                 agent_type: str,
                 replay_infra: CompleteReplayInfrastructure,
                 session_id: str = None):
        
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.infra = replay_infra
        
        # Get or create session
        if session_id:
            self.session_id = session_id
        else:
            # Create new session for this agent
            self.session_id = self.infra.start_session(
                f"agent_{agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                description=f"Session for agent {agent_id}"
            )
        
        # Agent-specific state management
        self.agent_state = self._load_agent_state()
        self.memory_context = {}
        
        # Event templates for common agent actions
        self.event_templates = self._create_event_templates()
        
        # Performance metrics
        self.metrics = {
            'events_logged': 0,
            'state_saves': 0,
            'memory_accesses': 0,
            'replay_calls': 0
        }
        
        # Log agent creation
        self.log_event(
            ReplayEventType.AGENT_CREATED,
            payload={
                'agent_id': self.agent_id,
                'agent_type': self.agent_type,
                'initial_state': self.agent_state,
                'adapter_version': '1.0.0'
            },
            source_component='agent_adapter',
            criticality=3
        )
    
    async def execute_with_replay(self,
                                 action_name: str,
                                 action_func: callable,
                                 *args,
                                 save_state: bool = True,
                                 **kwargs) -> Tuple[Any, ReplayEvent]:
        """
        Execute an agent action with automatic replay logging
        Returns (result, event)
        """
        
        # Create pre-action event
        pre_event = self.log_event(
            ReplayEventType.AGENT_ACTION,
            payload={
                'action': action_name,
                'stage': 'pre_execution',
                'agent_id': self.agent_id,
                'agent_state_before': self.agent_state,
                'args': self._serialize_for_replay(args),
                'kwargs': self._serialize_for_replay(kwargs),
                'timestamp': datetime.now(timezone.utc).isoformat()
            },
            source_component=f'agent:{self.agent_id}',
            criticality=2
        )
        
        try:
            # Execute the action
            result = await action_func(*args, **kwargs) if asyncio.iscoroutinefunction(action_func) \
                     else action_func(*args, **kwargs)
            
            # Log successful execution
            post_event = self.log_event(
                ReplayEventType.AGENT_ACTION,
                payload={
                    'action': action_name,
                    'stage': 'post_execution',
                    'agent_id': self.agent_id,
                    'agent_state_after': self.agent_state,
                    'result': self._serialize_for_replay(result),
                    'execution_time_ms': 0,  # Would track actual time
                    'success': True,
                    'parent_event_ids': [pre_event.event_id]
                },
                source_component=f'agent:{self.agent_id}',
                criticality=2
            )
            
            # Save state if requested
            if save_state:
                self.save_agent_state()
            
            return result, post_event
            
        except Exception as e:
            # Log failure
            error_event = self.log_event(
                ReplayEventType.AGENT_ACTION,
                payload={
                    'action': action_name,
                    'stage': 'error',
                    'agent_id': self.agent_id,
                    'error': str(e),
                    'error_type': type(e).__name__,
                    'parent_event_ids': [pre_event.event_id],
                    'success': False
                },
                source_component=f'agent:{self.agent_id}',
                criticality=4  # Higher criticality for errors
            )
            
            raise
    
    def log_hypothesis(self,
                      hypothesis: str,
                      confidence: float,
                      evidence: List[Dict],
                      context: Dict = None) -> ReplayEvent:
        """
        Log an agent hypothesis for replay
        """
        
        return self.log_event(
            ReplayEventType.AGENT_HYPOTHESIS,
            payload={
                'agent_id': self.agent_id,
                'hypothesis': hypothesis,
                'confidence': confidence,
                'evidence': evidence,
                'context': context or {},
                'reasoning_chain': self._capture_reasoning_chain()
            },
            source_component=f'agent:{self.agent_id}',
            criticality=3
        )
    
    def log_learning(self,
                    learned_concept: str,
                    old_belief: Any,
                    new_belief: Any,
                    trigger_event_id: str = None) -> ReplayEvent:
        """
        Log agent learning for replay
        """
        
        parent_events = []
        if trigger_event_id:
            parent_events = [trigger_event_id]
        
        return self.log_event(
            ReplayEventType.AGENT_LEARNED,
            payload={
                'agent_id': self.agent_id,
                'learned_concept': learned_concept,
                'old_belief': old_belief,
                'new_belief': new_belief,
                'learning_method': 'inference',  # Would be parameterized
                'confidence_change': abs(new_belief.get('confidence', 0) - old_belief.get('confidence', 0))
            },
            parent_event_ids=parent_events,
            source_component=f'agent:{self.agent_id}',
            criticality=4  # Learning events are important for replay
        )
    
    def save_agent_state(self, force_checkpoint: bool = False):
        """
        Save agent state to persistent storage
        """
        
        # Update internal state
        self.agent_state['last_saved'] = datetime.now(timezone.utc).isoformat()
        self.agent_state['event_count'] = self.metrics['events_logged']
        
        # Save to agent-specific storage
        state_path = self._get_agent_state_path()
        state_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(state_path, 'wb') as f:
            pickle.dump({
                'agent_state': self.agent_state,
                'memory_context': self.memory_context,
                'metrics': self.metrics,
                'session_id': self.session_id,
                'saved_at': datetime.now(timezone.utc).isoformat()
            }, f)
        
        self.metrics['state_saves'] += 1
        
        # Optionally create checkpoint
        if force_checkpoint or self.metrics['events_logged'] % 100 == 0:
            self.create_agent_checkpoint()
    
    def create_agent_checkpoint(self):
        """
        Create a full checkpoint of agent state
        """
        
        checkpoint_state = {
            'agent': self.agent_state,
            'memory': self.memory_context,
            'metrics': self.metrics,
            'session_info': {
                'session_id': self.session_id,
                'events_logged': self.metrics['events_logged'],
                'agent_id': self.agent_id
            }
        }
        
        logger = self.infra.get_logger(self.session_id)
        if logger:
            logger.create_checkpoint(
                checkpoint_state,
                description=f"Agent {self.agent_id} checkpoint"
            )
    
    def load_from_checkpoint(self, checkpoint_id: str = None):
        """
        Load agent state from checkpoint
        """
        
        if checkpoint_id:
            # Load specific checkpoint
            checkpoint_path = self.infra.base_path / self.session_id / "checkpoints" / f"{checkpoint_id}.cpt"
            if checkpoint_path.exists():
                return self._load_checkpoint(checkpoint_path)
        else:
            # Load latest checkpoint
            checkpoints_dir = self.infra.base_path / self.session_id / "checkpoints"
            if checkpoints_dir.exists():
                checkpoint_files = list(checkpoints_dir.glob("*.cpt"))
                if checkpoint_files:
                    latest = max(checkpoint_files, key=lambda p: p.stat().st_mtime)
                    return self._load_checkpoint(latest)
        
        return None
    
    def replay_agent_session(self,
                            target_sequence: int = None,
                            callback: callable = None) -> Dict:
        """
        Replay this agent's session
        """
        
        self.metrics['replay_calls'] += 1
        
        return self.infra.replay_and_analyze(
            self.session_id,
            start_sequence=0,
            end_sequence=target_sequence,
            granularity=ReplayGranularity.OPERATIONAL,
            callback=callback
        )
    
    def get_agent_timeline(self) -> List[Dict]:
        """
        Get timeline of agent events
        """
        
        session_path = self.infra.base_path / self.session_id
        events = self._load_all_events(session_path)
        
        agent_events = []
        for event in events:
            if (event.source_component == f'agent:{self.agent_id}' or 
                (event.payload and event.payload.get('agent_id') == self.agent_id)):
                
                agent_events.append({
                    'sequence': event.sequence_number,
                    'timestamp': event.timestamp.isoformat(),
                    'type': event.event_type.name,
                    'payload_summary': self._summarize_payload(event.payload)
                })
        
        return agent_events
    
    # ==================== HELPER METHODS ====================
    
    def _load_agent_state(self) -> Dict:
        """Load agent state from persistent storage"""
        
        state_path = self._get_agent_state_path()
        if state_path.exists():
            try:
                with open(state_path, 'rb') as f:
                    saved_data = pickle.load(f)
                    return saved_data.get('agent_state', {})
            except:
                pass
        
        # Default initial state
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'state_version': 1,
            'capabilities': [],
            'beliefs': {},
            'goals': [],
            'knowledge_base': {}
        }
    
    def _get_agent_state_path(self) -> Path:
        """Get path for agent state storage"""
        return self.infra.base_path / "agent_states" / f"{self.agent_id}.state"
    
    def _create_event_templates(self) -> Dict:
        """Create templates for common agent events"""
        return {
            'action_start': {
                'template': {
                    'agent_id': self.agent_id,
                    'stage': 'start',
                    'timestamp': None
                }
            },
            'action_complete': {
                'template': {
                    'agent_id': self.agent_id,
                    'stage': 'complete',
                    'success': True,
                    'execution_time_ms': None
                }
            },
            'memory_access': {
                'template': {
                    'agent_id': self.agent_id,
                    'operation': None,  # 'read', 'write', 'query'
                    'memory_key': None,
                    'result_count': None
                }
            }
        }
    
    def _serialize_for_replay(self, obj: Any) -> Any:
        """Serialize object for replay logging"""
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, (list, tuple)):
            return [self._serialize_for_replay(item) for item in obj]
        elif isinstance(obj, dict):
            return {str(k): self._serialize_for_replay(v) for k, v in obj.items()}
        else:
            # Try to serialize, fall back to string representation
            try:
                return pickle.dumps(obj).hex()
            except:
                return str(obj)
    
    def _capture_reasoning_chain(self) -> List[Dict]:
        """Capture current reasoning chain (simplified)"""
        # In full implementation, this would capture the agent's
        # current reasoning trace
        return [
            {
                'step': 'current_context',
                'data': self.memory_context
            }
        ]
    
    def _summarize_payload(self, payload: Dict) -> Dict:
        """Create summary of payload for timeline"""
        return {
            'keys': list(payload.keys()),
            'action': payload.get('action', 'unknown'),
            'agent_involved': payload.get('agent_id') == self.agent_id
        }
    
    def log_event(self, event_type: ReplayEventType, **kwargs) -> ReplayEvent:
        """Log event through infrastructure"""
        event = asyncio.run(
            self.infra.log_event(self.session_id, event_type, **kwargs)
        )
        self.metrics['events_logged'] += 1
        return event
		
		
		# ==================== AGENT MEMORY INTEGRATION ====================

class AgentMemoryBridge:
    """
    Bridges agent memory system with replay infrastructure
    Provides unified memory access with automatic logging
    """
    
    def __init__(self,
                 agent_adapter: AgentReplayAdapter,
                 memory_system: Any,  # Your existing memory system
                 enable_persistence: bool = True):
        
        self.adapter = agent_adapter
        self.memory = memory_system
        self.enable_persistence = enable_persistence
        
        # Memory access patterns for optimization
        self.access_patterns = defaultdict(int)
        self.cache = {}
        
        # Load persistent memory if available
        if enable_persistence:
            self._load_persistent_memory()
    
    async def store(self,
                   key: str,
                   value: Any,
                   metadata: Dict = None,
                   log_event: bool = True) -> str:
        """
        Store a memory with automatic replay logging
        """
        
        # Generate memory ID
        memory_id = f"mem_{self.adapter.agent_id}_{key}_{hashlib.sha256(str(value).encode()).hexdigest()[:8]}"
        
        # Store in memory system
        await self.memory.store(memory_id, value, metadata)
        
        # Log memory creation
        if log_event:
            self.adapter.log_event(
                ReplayEventType.MEMORY_CREATED,
                payload={
                    'agent_id': self.adapter.agent_id,
                    'memory_id': memory_id,
                    'key': key,
                    'value_type': type(value).__name__,
                    'value_size': len(str(value)),
                    'metadata': metadata or {},
                    'storage_backend': self.memory.__class__.__name__
                },
                source_component=f'agent_memory:{self.adapter.agent_id}',
                criticality=2
            )
        
        # Update access pattern
        self.access_patterns[key] += 1
        
        # Auto-persist if enabled
        if self.enable_persistence and self.access_patterns[key] % 10 == 0:
            self._persist_memory(key, memory_id, value)
        
        return memory_id
    
    async def retrieve(self,
                      key: str,
                      query: Any = None,
                      limit: int = 10,
                      log_event: bool = True) -> List[Any]:
        """
        Retrieve memories with automatic logging
        """
        
        # Check cache first
        cache_key = f"{key}_{str(query)}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Retrieve from memory system
        results = await self.memory.retrieve(key, query, limit)
        
        # Log memory access
        if log_event:
            self.adapter.log_event(
                ReplayEventType.MEMORY_ACCESSED,
                payload={
                    'agent_id': self.adapter.agent_id,
                    'operation': 'retrieve',
                    'key': key,
                    'query': query,
                    'result_count': len(results),
                    'cache_hit': False
                },
                source_component=f'agent_memory:{self.adapter.agent_id}',
                criticality=1
            )
        
        # Update cache
        self.cache[cache_key] = results
        
        # Update access pattern
        self.access_patterns[key] += 1
        
        return results
    
    async def associate(self,
                       source_id: str,
                       target_id: str,
                       relation_type: str,
                       strength: float = 1.0):
        """
        Create association between memories
        """
        
        # Create association in memory system
        await self.memory.associate(source_id, target_id, relation_type, strength)
        
        # Log association
        self.adapter.log_event(
            ReplayEventType.MEMORY_CONSOLIDATED,
            payload={
                'agent_id': self.adapter.agent_id,
                'operation': 'associate',
                'source_id': source_id,
                'target_id': target_id,
                'relation_type': relation_type,
                'strength': strength
            },
            source_component=f'agent_memory:{self.adapter.agent_id}',
            criticality=2
        )
    
    def get_memory_context(self) -> Dict:
        """
        Get current memory context for agent
        """
        
        return {
            'access_patterns': dict(self.access_patterns),
            'cache_size': len(self.cache),
            'memory_stats': self._get_memory_stats(),
            'recent_accesses': sorted(
                self.access_patterns.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }
    
    def save_memory_state(self):
        """
        Save complete memory state
        """
        
        if not self.enable_persistence:
            return
        
        # Get all memories
        all_memories = self._export_memories()
        
        # Save to persistent storage
        memory_state_path = self.adapter._get_agent_state_path().with_suffix('.memory')
        memory_state_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(memory_state_path, 'wb') as f:
            pickle.dump({
                'memories': all_memories,
                'associations': self._export_associations(),
                'access_patterns': dict(self.access_patterns),
                'saved_at': datetime.now(timezone.utc).isoformat(),
                'agent_id': self.adapter.agent_id
            }, f)
    
    def load_memory_state(self, checkpoint_id: str = None):
        """
        Load memory state from checkpoint
        """
        
        if checkpoint_id:
            # Load specific memory checkpoint
            checkpoint_path = self.adapter.infra.base_path / "memory_checkpoints" / f"{checkpoint_id}.mem"
            if checkpoint_path.exists():
                return self._load_memory_checkpoint(checkpoint_path)
        else:
            # Load latest memory state
            memory_state_path = self.adapter._get_agent_state_path().with_suffix('.memory')
            if memory_state_path.exists():
                with open(memory_state_path, 'rb') as f:
                    return pickle.load(f)
        
        return None
    
    # ==================== PERSISTENCE METHODS ====================
    
    def _load_persistent_memory(self):
        """Load persistent memory on startup"""
        
        memory_state = self.load_memory_state()
        if memory_state:
            print(f"Loaded {len(memory_state.get('memories', []))} memories for agent {self.adapter.agent_id}")
            
            # Restore memories
            for memory_data in memory_state.get('memories', []):
                asyncio.create_task(
                    self.store(
                        memory_data['key'],
                        memory_data['value'],
                        memory_data['metadata'],
                        log_event=False  # Don't log during restoration
                    )
                )
            
            # Restore access patterns
            self.access_patterns.update(memory_state.get('access_patterns', {}))
    
    def _persist_memory(self, key: str, memory_id: str, value: Any):
        """Persist memory to long-term storage"""
        
        persistence_path = self.adapter.infra.base_path / "persistent_memory" / self.adapter.agent_id
        persistence_path.mkdir(parents=True, exist_ok=True)
        
        # Store with metadata
        memory_file = persistence_path / f"{memory_id}.mem"
        with open(memory_file, 'wb') as f:
            pickle.dump({
                'key': key,
                'value': value,
                'memory_id': memory_id,
                'persisted_at': datetime.now(timezone.utc).isoformat(),
                'agent_id': self.adapter.agent_id
            }, f)
    
    def _export_memories(self) -> List[Dict]:
        """Export all memories for persistence"""
        # Implementation depends on your memory system
        # This would extract all memories in serializable format
        return []
    
    def _export_associations(self) -> List[Dict]:
        """Export all associations for persistence"""
        # Implementation depends on your memory system
        return []
    
    def _get_memory_stats(self) -> Dict:
        """Get memory system statistics"""
        return {
            'total_memories': len(self.access_patterns),
            'total_accesses': sum(self.access_patterns.values()),
            'cache_hit_rate': 0,  # Would calculate
            'persistence_enabled': self.enable_persistence
        }
		
		
		# ==================== AGENT BOOTSTRAP SYSTEM ====================

class AgentBootstrapSystem:
    """
    Handles agent initialization, state restoration, and warm-up
    """
    
    def __init__(self, replay_infra: CompleteReplayInfrastructure):
        self.infra = replay_infra
        self.agent_registry = {}
        self.bootstrapped_agents = {}
        
        # Bootstrap configurations
        self.bootstrap_config = {
            'restore_state': True,
            'load_memory': True,
            'warmup_events': 10,
            'create_initial_checkpoint': True,
            'validate_restoration': True
        }
    
    async def bootstrap_agent(self,
                            agent_class: Any,
                            agent_id: str,
                            agent_config: Dict,
                            restore_from: str = None) -> AgentReplayAdapter:
        """
        Bootstrap an agent with state restoration
        """
        
        print(f"Bootstrapping agent: {agent_id}")
        
        # Step 1: Create or restore session
        session_id = await self._prepare_agent_session(agent_id, restore_from)
        
        # Step 2: Create agent adapter
        adapter = AgentReplayAdapter(
            agent_id=agent_id,
            agent_type=agent_class.__name__,
            replay_infra=self.infra,
            session_id=session_id
        )
        
        # Step 3: Restore agent state if requested
        if self.bootstrap_config['restore_state']:
            await self._restore_agent_state(adapter, restore_from)
        
        # Step 4: Initialize the actual agent
        agent = agent_class(
            agent_id=agent_id,
            config=agent_config,
            replay_adapter=adapter
        )
        
        # Step 5: Initialize memory system
        if self.bootstrap_config['load_memory']:
            await self._initialize_agent_memory(agent, adapter)
        
        # Step 6: Warm-up if needed
        if self.bootstrap_config['warmup_events'] > 0:
            await self._warmup_agent(agent, adapter)
        
        # Step 7: Create initial checkpoint
        if self.bootstrap_config['create_initial_checkpoint']:
            adapter.create_agent_checkpoint()
        
        # Step 8: Validate restoration
        if self.bootstrap_config['validate_restoration']:
            await self._validate_restoration(adapter)
        
        # Register agent
        self.bootstrapped_agents[agent_id] = {
            'agent': agent,
            'adapter': adapter,
            'bootstrapped_at': datetime.now(timezone.utc).isoformat(),
            'session_id': session_id
        }
        
        print(f"Agent {agent_id} bootstrapped successfully")
        print(f"  Session: {session_id}")
        print(f"  State restored: {self.bootstrap_config['restore_state']}")
        print(f"  Memory loaded: {self.bootstrap_config['load_memory']}")
        
        return adapter
    
    async def shutdown_agent(self, agent_id: str, save_state: bool = True):
        """
        Properly shutdown an agent with state preservation
        """
        
        if agent_id not in self.bootstrapped_agents:
            return
        
        agent_info = self.bootstrapped_agents[agent_id]
        adapter = agent_info['adapter']
        
        print(f"Shutting down agent: {agent_id}")
        
        # Step 1: Final checkpoint
        if save_state:
            adapter.create_agent_checkpoint()
            adapter.save_agent_state()
        
        # Step 2: Save memory state
        if hasattr(agent_info['agent'], 'memory_bridge'):
            agent_info['agent'].memory_bridge.save_memory_state()
        
        # Step 3: End session
        final_state = {
            'agent_id': agent_id,
            'final_metrics': adapter.metrics,
            'shutdown_time': datetime.now(timezone.utc).isoformat()
        }
        
        self.infra.end_session(agent_info['session_id'], final_state)
        
        # Step 4: Unregister
        del self.bootstrapped_agents[agent_id]
        
        print(f"Agent {agent_id} shutdown complete")
    
    async def migrate_agent(self,
                          agent_id: str,
                          new_agent_class: Any,
                          preserve_state: bool = True) -> AgentReplayAdapter:
        """
        Migrate agent to new class while preserving state
        """
        
        if agent_id not in self.bootstrapped_agents:
            raise ValueError(f"Agent {agent_id} not found")
        
        agent_info = self.bootstrapped_agents[agent_id]
        
        print(f"Migrating agent {agent_id} to {new_agent_class.__name__}")
        
        # Step 1: Capture current state
        current_state = agent_info['adapter'].agent_state
        current_memory = agent_info['agent'].memory_bridge.get_memory_context() \
                        if hasattr(agent_info['agent'], 'memory_bridge') else {}
        
        # Step 2: Shutdown old agent
        await self.shutdown_agent(agent_id, save_state=True)
        
        # Step 3: Bootstrap new agent with preserved state
        new_adapter = await self.bootstrap_agent(
            new_agent_class,
            agent_id,
            agent_config={'migrated_from': agent_info['agent'].__class__.__name__},
            restore_from=agent_info['session_id']
        )
        
        # Step 4: Restore state if preserved
        if preserve_state:
            new_adapter.agent_state.update(current_state)
            if hasattr(new_adapter, 'memory_context'):
                new_adapter.memory_context.update(current_memory)
            
            new_adapter.save_agent_state()
        
        print(f"Agent {agent_id} migration complete")
        
        return new_adapter
    
    # ==================== BOOTSTRAP METHODS ====================
    
    async def _prepare_agent_session(self, agent_id: str, restore_from: str) -> str:
        """Prepare session for agent"""
        
        if restore_from:
            # Check if session exists
            session_path = self.infra.base_path / restore_from
            if session_path.exists():
                print(f"  Restoring from session: {restore_from}")
                return restore_from
        
        # Create new session
        return self.infra.start_session(
            f"{agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            description=f"Session for agent {agent_id}"
        )
    
    async def _restore_agent_state(self, adapter: AgentReplayAdapter, restore_from: str):
        """Restore agent state from persistence"""
        
        try:
            # Try to load from checkpoint
            checkpoint_state = adapter.load_from_checkpoint()
            if checkpoint_state:
                adapter.agent_state.update(checkpoint_state.get('agent', {}))
                adapter.memory_context.update(checkpoint_state.get('memory', {}))
                print(f"  Restored state from checkpoint")
                return
            
            # Try to load from persistent state
            state_path = adapter._get_agent_state_path()
            if state_path.exists():
                with open(state_path, 'rb') as f:
                    saved_state = pickle.load(f)
                    adapter.agent_state.update(saved_state.get('agent_state', {}))
                    adapter.memory_context.update(saved_state.get('memory_context', {}))
                print(f"  Restored state from persistence")
                
        except Exception as e:
            print(f"  State restoration failed: {e}")
    
    async def _initialize_agent_memory(self, agent, adapter):
        """Initialize agent memory system"""
        
        if hasattr(agent, 'initialize_memory'):
            # Check if memory bridge is already attached
            if not hasattr(agent, 'memory_bridge'):
                # Create memory bridge
                memory_system = agent.initialize_memory()
                agent.memory_bridge = AgentMemoryBridge(
                    adapter,
                    memory_system,
                    enable_persistence=True
                )
            
            # Load persistent memory
            agent.memory_bridge._load_persistent_memory()
            print(f"  Memory system initialized")
    
    async def _warmup_agent(self, agent, adapter):
        """Warm up agent with synthetic events"""
        
        print(f"  Warming up agent with {self.bootstrap_config['warmup_events']} events")
        
        warmup_events = [
            (ReplayEventType.AGENT_ACTION, {'action': 'bootstrap_warmup', 'stage': 'start'}),
            (ReplayEventType.MEMORY_CREATED, {'key': 'bootstrap_memory', 'value': 'warmup_data'}),
            (ReplayEventType.AGENT_HYPOTHESIS, {'hypothesis': 'System is bootstrapped', 'confidence': 0.9}),
        ]
        
        for event_type, payload in warmup_events[:self.bootstrap_config['warmup_events']]:
            adapter.log_event(event_type, payload=payload, source_component='bootstrap', criticality=1)
    
    async def _validate_restoration(self, adapter: AgentReplayAdapter):
        """Validate that restoration was successful"""
        
        # Quick replay of recent events
        try:
            replay_report = adapter.replay_agent_session(target_sequence=5)
            
            if replay_report['replay']['success_rate'] > 0.9:
                print(f"  Restoration validated: success rate {replay_report['replay']['success_rate']:.1%}")
            else:
                print(f"  Restoration validation warning: low success rate")
                
        except Exception as e:
            print(f"  Restoration validation failed: {e}")
    
    def get_bootstrap_report(self) -> Dict:
        """Get bootstrap system report"""
        
        return {
            'total_agents': len(self.bootstrapped_agents),
            'agents': {
                agent_id: {
                    'session': info['session_id'],
                    'bootstrapped_at': info['bootstrapped_at'],
                    'agent_type': info['agent'].__class__.__name__,
                    'adapter_metrics': info['adapter'].metrics
                }
                for agent_id, info in self.bootstrapped_agents.items()
            },
            'config': self.bootstrap_config,
            'infrastructure_stats': self.infra.get_statistics()
        }
		
		# ==================== EXAMPLE AGENT IMPLEMENTATION ====================

class ReplayEnabledAgent:
    """
    Example agent with replay infrastructure integration
    """
    
    def __init__(self,
                 agent_id: str,
                 config: Dict,
                 replay_adapter: AgentReplayAdapter = None):
        
        self.agent_id = agent_id
        self.config = config
        
        # Replay integration
        self.replay_adapter = replay_adapter
        self.memory_bridge = None
        
        # Agent state
        self.beliefs = {}
        self.goals = []
        self.capabilities = []
        
        # Initialize from config
        self._initialize_from_config()
        
        # Log initialization if adapter is provided
        if self.replay_adapter:
            self.replay_adapter.agent_state.update({
                'beliefs': self.beliefs,
                'goals': self.goals,
                'capabilities': self.capabilities
            })
    
    def initialize_memory(self):
        """Initialize memory system"""
        # Return your existing memory system instance
        from your_memory_system import MemorySystem
        return MemorySystem()
    
    async def process_input(self, input_data: Dict) -> Dict:
        """
        Process input with replay logging
        """
        
        if not self.replay_adapter:
            # Fallback to normal processing
            return await self._process_without_replay(input_data)
        
        # Process with replay logging
        result, event = await self.replay_adapter.execute_with_replay(
            action_name='process_input',
            action_func=self._process_input_internal,
            input_data=input_data,
            save_state=True
        )
        
        # Update agent state
        self._update_state_from_result(result)
        
        return result
    
    async def learn_from_experience(self, experience: Dict) -> Dict:
        """
        Learn from experience with replay logging
        """
        
        if not self.replay_adapter:
            return await self._learn_without_replay(experience)
        
        # Capture old belief for comparison
        old_belief = self.beliefs.get(experience.get('concept'))
        
        # Execute learning
        result, event = await self.replay_adapter.execute_with_replay(
            action_name='learn_from_experience',
            action_func=self._learn_internal,
            experience=experience,
            save_state=True
        )
        
        # Log learning event
        if old_belief != self.beliefs.get(experience.get('concept')):
            self.replay_adapter.log_learning(
                learned_concept=experience.get('concept', 'unknown'),
                old_belief={'value': old_belief} if old_belief else {},
                new_belief={'value': self.beliefs.get(experience.get('concept'))},
                trigger_event_id=event.event_id
            )
        
        return result
    
    async def reason_about(self, topic: str, context: Dict = None) -> Dict:
        """
        Perform reasoning with replay logging
        """
        
        if not self.replay_adapter:
            return await self._reason_without_replay(topic, context)
        
        # Use memory if available
        if self.memory_bridge:
            memories = await self.memory_bridge.retrieve(
                key=topic,
                query=context,
                limit=5
            )
            context = {**context, 'related_memories': memories} if context else {'related_memories': memories}
        
        # Log hypothesis generation
        hypothesis_event = self.replay_adapter.log_hypothesis(
            hypothesis=f"Reasoning about {topic}",
            confidence=0.7,
            evidence=context or {},
            context={'topic': topic}
        )
        
        # Execute reasoning
        result, action_event = await self.replay_adapter.execute_with_replay(
            action_name='reason_about',
            action_func=self._reason_internal,
            topic=topic,
            context=context,
            save_state=False  # Don't save state for every reasoning step
        )
        
        return result
    
    # ==================== INTERNAL METHODS ====================
    
    async def _process_input_internal(self, input_data: Dict) -> Dict:
        """Internal processing implementation"""
        # Your agent's actual processing logic
        return {'processed': True, 'input': input_data}
    
    async def _learn_internal(self, experience: Dict) -> Dict:
        """Internal learning implementation"""
        concept = experience.get('concept')
        value = experience.get('value')
        
        if concept:
            self.beliefs[concept] = value
        
        return {'learned': True, 'concept': concept, 'value': value}
    
    async def _reason_internal(self, topic: str, context: Dict) -> Dict:
        """Internal reasoning implementation"""
        # Your agent's reasoning logic
        return {
            'topic': topic,
            'conclusions': [],
            'confidence': 0.8,
            'reasoning_steps': 3
        }
    
    def _update_state_from_result(self, result: Dict):
        """Update agent state from processing result"""
        # Update beliefs, goals, etc. based on result
        pass
    
    def _initialize_from_config(self):
        """
        Initialize agent state from configuration.
        """
        pass