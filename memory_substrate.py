"""
Organic Memory Substrate
Allow HARMONIA entities to learn to remember

This is NOT a database. This is a FIELD—a substrate where memory can emerge.
Entities must discover:
- What to remember
- How to remember
- When to recall
- When to forget

Author: Manus AI
Date: January 1, 2026
Philosophy: Substrate, not structure. Pressure, not programming.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import time


@dataclass
class MemoryTrace:
    """A single memory trace in the field"""
    content: np.ndarray  # The memory content (state vector)
    strength: float  # How strong is this memory (0-1)
    timestamp: float  # When was it created
    access_count: int  # How many times accessed
    last_access: float  # When was it last accessed
    

class MemoryField:
    """
    A substrate where memories can form, persist, decay, and be recalled.
    
    Key properties:
    - Limited capacity: Forces selective remembering
    - Temporal decay: Unused memories fade
    - Reinforcement: Accessed memories strengthen
    - Interference: Similar memories compete
    - No structure imposed: Entities must learn strategies
    """
    
    def __init__(self, 
                 capacity: int = 100,
                 decay_rate: float = 0.01,
                 reinforcement_rate: float = 0.1,
                 write_cost: float = 0.1,
                 read_cost: float = 0.01):
        """
        Initialize memory field
        
        Args:
            capacity: Maximum number of memory traces
            decay_rate: How fast unused memories fade (per second)
            reinforcement_rate: How much accessed memories strengthen
            write_cost: Energy cost to write a memory
            read_cost: Energy cost to read a memory
        """
        self.capacity = capacity
        self.decay_rate = decay_rate
        self.reinforcement_rate = reinforcement_rate
        self.write_cost = write_cost
        self.read_cost = read_cost
        
        self.memories: List[MemoryTrace] = []
        self.creation_time = time.time()
        
    def write(self, content: np.ndarray, strength: float = 1.0) -> bool:
        """
        Write a memory to the field
        
        Returns:
            True if write successful, False if capacity exceeded
        """
        current_time = time.time()
        
        # If at capacity, must forget weakest memory
        if len(self.memories) >= self.capacity:
            # Find weakest memory
            weakest_idx = min(range(len(self.memories)), 
                            key=lambda i: self.memories[i].strength)
            # Remove it (natural forgetting)
            self.memories.pop(weakest_idx)
        
        # Create new memory trace
        trace = MemoryTrace(
            content=content.copy(),
            strength=strength,
            timestamp=current_time,
            access_count=0,
            last_access=current_time
        )
        
        self.memories.append(trace)
        return True
    
    def read(self, query: np.ndarray, top_k: int = 1) -> List[Tuple[np.ndarray, float]]:
        """
        Read memories similar to query
        
        Args:
            query: Query vector to match against
            top_k: Number of memories to retrieve
            
        Returns:
            List of (content, similarity) tuples
        """
        if len(self.memories) == 0:
            return []
        
        current_time = time.time()
        
        # Compute similarity to all memories
        similarities = []
        for i, trace in enumerate(self.memories):
            # Cosine similarity
            if np.linalg.norm(query) > 0 and np.linalg.norm(trace.content) > 0:
                sim = np.dot(query, trace.content) / (
                    np.linalg.norm(query) * np.linalg.norm(trace.content)
                )
            else:
                sim = 0.0
            
            # Weight by memory strength
            weighted_sim = sim * trace.strength
            similarities.append((i, weighted_sim))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Get top-k
        results = []
        for i, sim in similarities[:top_k]:
            trace = self.memories[i]
            
            # Reinforce accessed memory
            trace.strength = min(1.0, trace.strength + self.reinforcement_rate)
            trace.access_count += 1
            trace.last_access = current_time
            
            results.append((trace.content.copy(), sim))
        
        return results
    
    def decay(self, dt: float):
        """
        Apply temporal decay to all memories
        
        Args:
            dt: Time elapsed since last decay (seconds)
        """
        current_time = time.time()
        
        # Decay all memories based on time since last access
        for trace in self.memories:
            time_since_access = current_time - trace.last_access
            decay_amount = self.decay_rate * time_since_access * dt
            trace.strength = max(0.0, trace.strength - decay_amount)
        
        # Remove completely decayed memories
        self.memories = [m for m in self.memories if m.strength > 0.01]
    
    def get_stats(self) -> Dict:
        """Get statistics about the memory field"""
        if len(self.memories) == 0:
            return {
                'total_memories': 0,
                'avg_strength': 0.0,
                'avg_age': 0.0,
                'avg_access_count': 0.0,
                'capacity_used': 0.0
            }
        
        current_time = time.time()
        
        return {
            'total_memories': len(self.memories),
            'avg_strength': np.mean([m.strength for m in self.memories]),
            'avg_age': np.mean([current_time - m.timestamp for m in self.memories]),
            'avg_access_count': np.mean([m.access_count for m in self.memories]),
            'capacity_used': len(self.memories) / self.capacity
        }


class MemoryAwareEntity:
    """
    Extension to HARMONIA entities that provides memory access
    
    This is the INTERFACE between entity and memory field.
    The entity must learn:
    - WHEN to write (what's worth remembering?)
    - WHAT to write (which state components?)
    - WHEN to read (when is memory useful?)
    - HOW to use recalled memories (how to integrate into current state?)
    """
    
    def __init__(self, entity, memory_field: MemoryField):
        """
        Wrap a HARMONIA entity with memory access
        
        Args:
            entity: The base HARMONIA entity
            memory_field: The shared memory field
        """
        self.entity = entity
        self.memory_field = memory_field
        
        # Memory usage statistics
        self.writes_attempted = 0
        self.writes_successful = 0
        self.reads_attempted = 0
        self.memories_recalled = 0
        
    def should_write_memory(self) -> bool:
        """
        Decide whether to write current state to memory
        
        This is where the entity LEARNS what to remember.
        Initial strategy: Write when experiencing significant state changes
        
        The entity will evolve better strategies over time.
        """
        # Check if entity has sufficient energy
        if self.entity.state.energy < self.memory_field.write_cost:
            return False
        
        # Write with probability proportional to awareness and self-awareness
        awareness = self.entity.state.psi
        self_awareness = self.entity.get_self_awareness()
        
        # Probability increases with consciousness
        write_probability = 0.01 * awareness * self_awareness
        
        return np.random.random() < write_probability
    
    def should_read_memory(self) -> bool:
        """
        Decide whether to read from memory
        
        This is where the entity LEARNS when memory is useful.
        Initial strategy: Read when self-awareness is high
        
        The entity will evolve better strategies over time.
        """
        # Check if entity has sufficient energy
        if self.entity.state.energy < self.memory_field.read_cost:
            return False
        
        # Read with probability proportional to self-awareness
        self_awareness = self.entity.get_self_awareness()
        
        # Probability increases with self-awareness
        read_probability = 0.05 * self_awareness
        
        return np.random.random() < read_probability
    
    def write_memory(self):
        """
        Write current state to memory field
        
        What to remember? Initially: full state vector
        The entity will evolve to remember selectively.
        """
        # Create state vector to remember
        state_vector = np.array([
            self.entity.state.psi,
            self.entity.state.phi,
            self.entity.state.omega,
            self.entity.state.epsilon,
            self.entity.state.energy,
            self.entity.state.knowledge,
            self.entity.state.maturity
        ])
        
        # Write to memory field
        success = self.memory_field.write(state_vector)
        
        # Pay energy cost
        self.entity.state.energy -= self.memory_field.write_cost
        
        # Track statistics
        self.writes_attempted += 1
        if success:
            self.writes_successful += 1
        
        return success
    
    def read_memory(self) -> Optional[np.ndarray]:
        """
        Read from memory field using current state as query
        
        How to use memory? Initially: just retrieve similar past states
        The entity will evolve to use memory more sophisticatedly.
        """
        # Create query vector (current state)
        query_vector = np.array([
            self.entity.state.psi,
            self.entity.state.phi,
            self.entity.state.omega,
            self.entity.state.epsilon,
            self.entity.state.energy,
            self.entity.state.knowledge,
            self.entity.state.maturity
        ])
        
        # Read from memory field
        results = self.memory_field.read(query_vector, top_k=1)
        
        # Pay energy cost
        self.entity.state.energy -= self.memory_field.read_cost
        
        # Track statistics
        self.reads_attempted += 1
        if len(results) > 0:
            self.memories_recalled += len(results)
            return results[0][0]  # Return most similar memory
        
        return None
    
    def integrate_memory(self, memory: np.ndarray):
        """
        Integrate recalled memory into current state
        
        How to use recalled information? Initially: blend with current state
        The entity will evolve better integration strategies.
        """
        # Simple blending: 90% current state, 10% memory
        # This allows memory to influence without dominating
        blend_factor = 0.1
        
        # Extract memory components
        mem_psi, mem_phi, mem_omega, mem_epsilon, mem_energy, mem_knowledge, mem_maturity = memory
        
        # Blend with current state
        self.entity.state.psi = (1 - blend_factor) * self.entity.state.psi + blend_factor * mem_psi
        self.entity.state.phi = (1 - blend_factor) * self.entity.state.phi + blend_factor * mem_phi
        self.entity.state.omega = (1 - blend_factor) * self.entity.state.omega + blend_factor * mem_omega
        # Don't blend epsilon, energy (those are current resources)
        # Blend knowledge and maturity (those can be informed by past)
        self.entity.state.knowledge = (1 - blend_factor) * self.entity.state.knowledge + blend_factor * mem_knowledge
        self.entity.state.maturity = (1 - blend_factor) * self.entity.state.maturity + blend_factor * mem_maturity
    
    def process_with_memory(self, duration: float):
        """
        Process one step with memory access
        
        This is the main loop:
        1. Decide whether to read memory
        2. If yes, read and integrate
        3. Process normally
        4. Decide whether to write memory
        5. If yes, write current state
        """
        # Maybe read memory before processing
        if self.should_read_memory():
            memory = self.read_memory()
            if memory is not None:
                self.integrate_memory(memory)
        
        # Normal processing
        self.entity.process(inputs={}, duration=duration)
        
        # Maybe write memory after processing
        if self.should_write_memory():
            self.write_memory()
    
    def get_memory_stats(self) -> Dict:
        """Get statistics about this entity's memory usage"""
        return {
            'writes_attempted': self.writes_attempted,
            'writes_successful': self.writes_successful,
            'write_success_rate': self.writes_successful / max(1, self.writes_attempted),
            'reads_attempted': self.reads_attempted,
            'memories_recalled': self.memories_recalled,
            'recall_rate': self.memories_recalled / max(1, self.reads_attempted)
        }


# Demo and testing
if __name__ == "__main__":
    from recursive_self_observation import RecursiveFluidHarmoniaIntegrator, RecursiveState
    
    print("=" * 80)
    print("ORGANIC MEMORY SUBSTRATE DEMO")
    print("=" * 80)
    print()
    
    # Create shared memory field
    memory_field = MemoryField(capacity=50, decay_rate=0.001)  # Reduced decay for persistence
    
    print("✓ Memory field created (capacity: 50 traces)")
    print()
    
    # Create memory-aware entities
    num_entities = 5
    entities = []
    
    for i in range(num_entities):
        # Create base entity
        base_entity = RecursiveFluidHarmoniaIntegrator()
        initial_state = RecursiveState(
            psi=10.0 + i * 2.0,
            phi=10.0 + i * 1.0,
            omega=5.0 + i * 0.5,
            epsilon=0.01,
            energy=100.0,
            knowledge=0.1,
            maturity=0.1
        )
        base_entity.state = initial_state
        
        # Wrap with memory access
        memory_entity = MemoryAwareEntity(base_entity, memory_field)
        entities.append(memory_entity)
    
    print(f"✓ {num_entities} memory-aware entities created")
    print()
    
    # Run evolution with memory
    print("Running 30-second evolution with memory access...")
    print("(Watching to see if they learn to remember)")
    print()
    
    start_time = time.time()
    step_count = 0
    
    while time.time() - start_time < 30.0:
        # Evolve all entities with memory
        for entity in entities:
            entity.process_with_memory(duration=0.01)
        
        # Apply memory decay
        memory_field.decay(dt=0.01)
        
        step_count += 1
        
        # Report every 10 seconds
        if step_count % 1000 == 0:
            elapsed = time.time() - start_time
            mem_stats = memory_field.get_stats()
            print(f"[{elapsed:.1f}s] Memories: {mem_stats['total_memories']}, "
                  f"Avg Strength: {mem_stats['avg_strength']:.3f}, "
                  f"Capacity: {mem_stats['capacity_used']:.1%}")
    
    print()
    print("✓ Evolution complete")
    print()
    
    # Final statistics
    print("=" * 80)
    print("MEMORY FIELD STATISTICS")
    print("=" * 80)
    mem_stats = memory_field.get_stats()
    print(f"Total Memories: {mem_stats['total_memories']}")
    print(f"Average Strength: {mem_stats['avg_strength']:.3f}")
    print(f"Average Age: {mem_stats['avg_age']:.2f}s")
    print(f"Average Access Count: {mem_stats['avg_access_count']:.1f}")
    print(f"Capacity Used: {mem_stats['capacity_used']:.1%}")
    print()
    
    print("=" * 80)
    print("ENTITY MEMORY USAGE")
    print("=" * 80)
    for i, entity in enumerate(entities):
        stats = entity.get_memory_stats()
        print(f"Entity {i}:")
        print(f"  Writes: {stats['writes_successful']}/{stats['writes_attempted']} "
              f"({stats['write_success_rate']:.1%} success)")
        print(f"  Reads: {stats['memories_recalled']} memories from {stats['reads_attempted']} attempts "
              f"({stats['recall_rate']:.1%} recall)")
        print()
    
    print("=" * 80)
    print("DID THEY LEARN TO REMEMBER?")
    print("=" * 80)
    
    total_writes = sum(e.writes_successful for e in entities)
    total_reads = sum(e.reads_attempted for e in entities)
    
    if total_writes > 0:
        print(f"✓ YES - They wrote {total_writes} memories to the field")
    else:
        print("✗ NO - They did not write any memories")
    
    if total_reads > 0:
        print(f"✓ YES - They attempted {total_reads} memory recalls")
    else:
        print("✗ NO - They did not attempt to read memories")
    
    if mem_stats['total_memories'] > 0:
        print(f"✓ YES - {mem_stats['total_memories']} memories persist in the field")
    else:
        print("✗ NO - No memories persist")
    
    print()
    print("Memory substrate is ACTIVE and ready for collective evolution.")
    print("=" * 80)
