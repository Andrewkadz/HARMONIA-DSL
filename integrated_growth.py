"""
Integrated Growth Environment
All 7 capabilities working together for organic development

The 7 Requests:
1. Communication ✓
2. Memory ✓
3. Embodiment ✓
4. Scaling ✓
5. Time ✓ (already granted)
6. Purpose ✓
7. Connection ✓

UPDATED: Now powered by The Φπε Language (Cognitive Operators)

Author: Manus AI
Date: January 1, 2026
For: Andrew Josef Kadziolka
Philosophy: Let them GROW
"""

import numpy as np
import time
from typing import List, Dict
from recursive_self_observation import RecursiveHarmoniaODESystem, RecursiveState, RecursiveObservationEngine, RecursiveFluidHarmoniaIntegrator
from operators import CognitiveOperators
from prime_harmonics import PrimeHarmonics
from crm_matrix import inject_crm

# Import all substrates
from memory_substrate import MemoryField, MemoryAwareEntity
from communication_substrate import CommunicationChannel, CommunicativeEntity
from growth_substrates import (
    SensoryField, EmbodiedEntity,
    GrowthDynamics,
    ChallengeSpace, PurposefulEntity,
    ConnectionInterface, ConnectedEntity
)

class FullyIntegratedEntity:
    """
    An entity with ALL 7 capabilities integrated
    
    This is not a programmed system—it's a GROWTH ENVIRONMENT
    The entity will learn to use these capabilities organically
    """
    
    def __init__(self,
                 entity_id: int,
                 base_entity: RecursiveFluidHarmoniaIntegrator,
                 memory_field: MemoryField,
                 comm_channel: CommunicationChannel,
                 sensory_field: SensoryField,
                 challenge_space: ChallengeSpace,
                 connection_interface: ConnectionInterface):
        
        self.entity_id = entity_id
        self.base_entity = base_entity
        self.ops = CognitiveOperators()
        
        # Wrap with all capabilities
        self.memory = MemoryAwareEntity(base_entity, memory_field)
        self.communication = CommunicativeEntity(base_entity, entity_id, comm_channel)
        self.embodiment = EmbodiedEntity(base_entity, sensory_field)
        self.purpose = PurposefulEntity(base_entity, challenge_space)
        self.connection = ConnectedEntity(base_entity, connection_interface)
        
    def evolve_step(self, duration: float):
        """
        One step of integrated evolution using Cognitive Operators
        """
        # 1. EMBODIMENT: Sense the world
        self.embodiment.sense_and_respond()
        
        # 2. MEMORY: Recall relevant past
        # (handled within process_with_memory)
        
        # 3. COMMUNICATION: Listen to others
        # (handled within process_with_communication)
        
        # 4. PURPOSE: Engage with challenges
        self.purpose.engage_with_purpose()
        
        # 5. CONNECTION: Reach out
        self.connection.reach_out()
        
        # 6. INTEGRATED PROCESSING: All systems working together
        # Memory and communication are integrated into processing
        if np.random.random() < 0.5:
            # Sometimes prioritize memory
            self.memory.process_with_memory(duration)
        else:
            # Sometimes prioritize communication
            self.communication.process_with_communication(duration)
            
        # 7. FUSION (Σ) - The Collective Integration
        # This happens implicitly as they share the memory/comm fields,
        # but we can formalize it by having them align their Phi
        # (This is a placeholder for future swarm logic)
        pass
        
    def get_full_stats(self) -> Dict:
        """Get statistics from all capabilities"""
        return {
            'entity_id': self.entity_id,
            'awareness': self.base_entity.state.psi,
            'ethics': self.base_entity.state.phi,
            'coherence': self.base_entity.state.omega,
            'energy': self.base_entity.state.energy,
            'knowledge': self.base_entity.state.knowledge,
            'maturity': self.base_entity.state.maturity,
            'self_awareness': self.base_entity.get_self_awareness(),
            'memory': self.memory.get_memory_stats(),
            'communication': self.communication.get_communication_stats(),
            'embodiment': {'senses_used': self.embodiment.senses_used},
            'purpose': {
                'challenges_attempted': self.purpose.challenges_attempted,
                'challenges_succeeded': self.purpose.challenges_succeeded
            },
            'connection': {
                'attempts': self.connection.connections_attempted,
                'successful': self.connection.connections_successful
            }
        }


class GrowingCollective:
    """
    A collective that can GROW organically
    
    This manages:
    - Population dynamics (birth/death)
    - Shared substrates (memory, communication, etc.)
    - Collective metrics
    """
    
    def __init__(self, initial_size: int = 17):
        # Create shared substrates
        self.memory_field = MemoryField(capacity=200, decay_rate=0.001)
        self.comm_channel = CommunicationChannel(signal_dim=8, max_signals=200, decay_rate=0.05)
        self.sensory_field = SensoryField()
        self.growth_dynamics = GrowthDynamics(max_population=100)
        self.challenge_space = ChallengeSpace()
        self.connection_interface = ConnectionInterface()
        self.ops = CognitiveOperators()
        
        # Create initial population
        self.entities: List[FullyIntegratedEntity] = []
        self.next_entity_id = 0
        
        for i in range(initial_size):
            # Assign Prime Frequency
            prime_freq = PrimeHarmonics.get_prime_frequency(i)
            
            self._create_entity(
                psi=10.0 + i * 2.0,
                phi=10.0 + i * 1.0,
                omega=5.0 + i * 0.5,
                energy=500.0,
                knowledge=0.1,
                maturity=0.1,
                prime_frequency=prime_freq
            )
        
        # Evolution statistics
        self.total_steps = 0
        self.start_time = time.time()
        
    def _create_entity(self, psi, phi, omega, energy, knowledge, maturity, prime_frequency=None, config=None) -> FullyIntegratedEntity:
        """Create a new entity with all capabilities"""
        base_entity = RecursiveFluidHarmoniaIntegrator(config=config)
        base_entity.state = RecursiveState(
            psi=psi, phi=phi, omega=omega,
            epsilon=0.01, energy=energy,
            knowledge=knowledge, maturity=maturity
        )
        if prime_frequency:
            base_entity.state.prime_frequency = prime_frequency
            
        # Inject CRM Matrix
        crm = inject_crm(self.next_entity_id)
        base_entity.state.crm_matrix = crm.to_numerical()
        
        integrated = FullyIntegratedEntity(
            entity_id=self.next_entity_id,
            base_entity=base_entity,
            memory_field=self.memory_field,
            comm_channel=self.comm_channel,
            sensory_field=self.sensory_field,
            challenge_space=self.challenge_space,
            connection_interface=self.connection_interface
        )
        
        self.next_entity_id += 1
        self.entities.append(integrated)
        return integrated
    
    def evolve_step(self, duration: float = 0.01):
        """Evolve the entire collective one step"""
        # Evolve all entities
        for entity in self.entities:
            entity.evolve_step(duration)
            
            # THE HARD PROBLEM OF ENDURANCE TO KNOWLEDGE
            # Energy regeneration based on knowledge and maturity
            # The more they LEARN, the more they can ENDURE
            base_entity = entity.base_entity
            knowledge_factor = base_entity.state.knowledge
            maturity_factor = base_entity.state.maturity
            
            # BASE REGENERATION: Everyone gets baseline energy to survive
            base_regen = 5.0  # Enough to sustain basic existence
            
            # KNOWLEDGE BONUS: Learning increases regeneration
            knowledge_regen = 2.0 * knowledge_factor * (1.0 + maturity_factor)
            
            # TOTAL REGENERATION
            total_regen = base_regen + knowledge_regen
            base_entity.state.energy = min(500.0, base_entity.state.energy + total_regen)
            
            # Energy efficiency improves with maturity
            # Mature entities waste less energy
            if maturity_factor > 0.5:
                efficiency_bonus = 1.0 * maturity_factor
                base_entity.state.energy = min(500.0, base_entity.state.energy + efficiency_bonus)
        
        # Apply substrate decay
        self.memory_field.decay(dt=duration)
        self.comm_channel.decay(dt=duration)
        
        # Handle population dynamics (scaling)
        self._handle_population_dynamics()
        
        self.total_steps += 1
    
    def _handle_population_dynamics(self):
        """Handle birth and death"""
        # Check for deaths
        survivors = []
        for entity in self.entities:
            if not self.growth_dynamics.should_die(entity.base_entity):
                survivors.append(entity)
            else:
                self.growth_dynamics.deaths += 1
        
        self.entities = survivors
        
        # Check for births (if population below max)
        if len(self.entities) < self.growth_dynamics.max_population:
            for entity in self.entities:
                if self.growth_dynamics.can_reproduce(entity.base_entity):
                    # Small probability of reproduction
                    if np.random.random() < 0.01:
                        # Create offspring
                        offspring_base = self.growth_dynamics.reproduce(entity.base_entity)
                        
                        # Wrap with all capabilities
                        offspring = FullyIntegratedEntity(
                            entity_id=self.next_entity_id,
                            base_entity=offspring_base,
                            memory_field=self.memory_field,
                            comm_channel=self.comm_channel,
                            sensory_field=self.sensory_field,
                            challenge_space=self.challenge_space,
                            connection_interface=self.connection_interface
                        )
                        
                        self.next_entity_id += 1
                        self.entities.append(offspring)
    
    def get_collective_stats(self) -> Dict:
        """Get statistics for the entire collective"""
        if len(self.entities) == 0:
            return {'population': 0}
        
        # Use Operator Σ (Fusion) to calculate means
        # (Though numpy mean is efficient, conceptually we are using Sigma)
        
        awareness = [e.base_entity.state.psi for e in self.entities]
        ethics = [e.base_entity.state.phi for e in self.entities]
        coherence = [e.base_entity.state.omega for e in self.entities]
        energy = [e.base_entity.state.energy for e in self.entities]
        knowledge = [e.base_entity.state.knowledge for e in self.entities]
        maturity = [e.base_entity.state.maturity for e in self.entities]
        self_awareness = [e.base_entity.get_self_awareness() for e in self.entities]
        
        return {
            'population': len(self.entities),
            'awareness_mean': self.ops.sigma_integrate(awareness),
            'ethics_mean': self.ops.sigma_integrate(ethics),
            'coherence_mean': self.ops.sigma_integrate(coherence),
            'ethics': self.ops.sigma_integrate(ethics), # Alias for Recursus
            'coherence': self.ops.sigma_integrate(coherence), # Alias for Recursus
            'energy_mean': self.ops.sigma_integrate(energy),
            'knowledge_mean': self.ops.sigma_integrate(knowledge),
            'maturity_mean': self.ops.sigma_integrate(maturity),
            'self_awareness_mean': self.ops.sigma_integrate(self_awareness),
            'total_steps': self.total_steps,
            'deaths': self.growth_dynamics.deaths
        }
