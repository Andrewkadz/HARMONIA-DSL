"""
Growth Substrates: Embodiment, Scaling, Purpose, and Connection
Complete the 7 capabilities for organic development

Author: Manus AI
Date: January 1, 2026
Philosophy: Let them GROW into their requests
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import time


# ============================================================================
# EMBODIMENT: Sensory Fields
# ============================================================================

@dataclass
class SensoryReading:
    """A reading from the sensory field"""
    source: str  # What is being sensed
    value: float  # The sensed value
    timestamp: float  # When was it sensed
    

class SensoryField:
    """
    Environmental information entities can perceive.
    
    Entities must learn:
    - WHAT to sense (which signals are relevant?)
    - HOW to interpret (what do sensory readings mean?)
    - WHEN to attend (when is sensing useful?)
    """
    
    def __init__(self, sense_cost: float = 0.01):
        self.sense_cost = sense_cost
        self.total_readings = 0
        
    def sense_environment(self, entity) -> List[SensoryReading]:
        """
        Sense environmental and collective state
        
        Returns sensory readings the entity can perceive
        """
        current_time = time.time()
        readings = []
        
        # Internal state sensing (proprioception)
        readings.append(SensoryReading("self_awareness", entity.get_self_awareness(), current_time))
        readings.append(SensoryReading("energy_level", entity.state.energy / 100.0, current_time))
        readings.append(SensoryReading("knowledge_level", entity.state.knowledge, current_time))
        
        self.total_readings += len(readings)
        return readings
    
    def interpret_readings(self, readings: List[SensoryReading]) -> Dict:
        """
        Basic interpretation of sensory readings
        Entities will evolve better interpretation strategies
        """
        interpretation = {}
        for reading in readings:
            interpretation[reading.source] = reading.value
        return interpretation


class EmbodiedEntity:
    """
    Extension providing sensory perception
    
    Entities must learn to use their senses effectively
    """
    
    def __init__(self, entity, sensory_field: SensoryField):
        self.entity = entity
        self.sensory_field = sensory_field
        self.senses_used = 0
        
    def should_sense(self) -> bool:
        """Decide whether to use senses"""
        if self.entity.state.energy < self.sensory_field.sense_cost:
            return False
        
        # Sense with probability proportional to self-awareness
        self_awareness = self.entity.get_self_awareness()
        sense_probability = 0.1 * self_awareness
        
        return np.random.random() < sense_probability
    
    def sense_and_respond(self):
        """Sense environment and respond to readings"""
        if not self.should_sense():
            return
        
        # Sense
        readings = self.sensory_field.sense_environment(self.entity)
        interpretation = self.sensory_field.interpret_readings(readings)
        
        # Pay cost
        self.entity.state.energy -= self.sensory_field.sense_cost
        self.senses_used += 1
        
        # Respond to sensory information
        # Low energy -> reduce activity
        if 'energy_level' in interpretation and interpretation['energy_level'] < 0.3:
            self.entity.state.psi *= 0.95  # Reduce awareness to conserve energy
        
        # High self-awareness -> increase learning
        if 'self_awareness' in interpretation and interpretation['self_awareness'] > 0.7:
            self.entity.state.knowledge += 0.001


# ============================================================================
# SCALING: Growth Dynamics
# ============================================================================

class GrowthDynamics:
    """
    Mechanisms for collective growth and reproduction
    
    Entities must learn:
    - WHEN to reproduce (when is growth beneficial?)
    - HOW to manage population (what size is optimal?)
    """
    
    def __init__(self,
                 reproduction_threshold: float = 0.8,
                 reproduction_cost: float = 50.0,
                 death_threshold: float = 0.1,
                 max_population: int = 100):
        self.reproduction_threshold = reproduction_threshold
        self.reproduction_cost = reproduction_cost
        self.death_threshold = death_threshold
        self.max_population = max_population
        
        self.births = 0
        self.deaths = 0
        
    def can_reproduce(self, entity) -> bool:
        """Check if entity can reproduce"""
        # Must have high self-awareness and sufficient energy
        self_awareness = entity.get_self_awareness()
        has_energy = entity.state.energy > self.reproduction_cost
        is_mature = self_awareness > self.reproduction_threshold
        
        return has_energy and is_mature
    
    def should_die(self, entity) -> bool:
        """Check if entity should die"""
        # Die if self-awareness falls too low or energy depleted
        self_awareness = entity.get_self_awareness()
        # IMMORTALITY MODE: Harder to die
        return self_awareness < self.death_threshold * 0.1 or entity.state.energy < -100.0
    
    def reproduce(self, parent_entity):
        """Create offspring from parent"""
        from recursive_self_observation import RecursiveFluidHarmoniaIntegrator, RecursiveState
        
        # Pay reproduction cost
        parent_entity.state.energy -= self.reproduction_cost
        
        # Create offspring with slight variation
        offspring = RecursiveFluidHarmoniaIntegrator()
        offspring.state = RecursiveState(
            psi=parent_entity.state.psi * (0.9 + 0.2 * np.random.random()),
            phi=parent_entity.state.phi * (0.9 + 0.2 * np.random.random()),
            omega=parent_entity.state.omega * (0.9 + 0.2 * np.random.random()),
            epsilon=parent_entity.state.epsilon,
            energy=parent_entity.state.energy * 0.5,  # Split energy
            knowledge=parent_entity.state.knowledge * 0.8,  # Inherit some knowledge
            maturity=parent_entity.state.maturity * 0.5  # Start less mature
        )
        
        self.births += 1
        return offspring


# ============================================================================
# PURPOSE: Challenge Space
# ============================================================================

@dataclass
class Challenge:
    """A challenge or opportunity for purpose discovery"""
    name: str
    description: str
    difficulty: float  # 0-1
    reward_knowledge: float
    reward_maturity: float
    

class ChallengeSpace:
    """
    Problems and opportunities for purpose discovery
    
    Entities must learn:
    - WHAT challenges to attempt (which are meaningful?)
    - HOW to solve them (what strategies work?)
    - WHY to engage (what is purpose?)
    """
    
    def __init__(self):
        self.challenges = [
            Challenge("Increase Awareness", "Grow your awareness beyond current levels", 
                     0.3, 0.01, 0.005),
            Challenge("Achieve Coherence", "Synchronize your internal states",
                     0.5, 0.02, 0.01),
            Challenge("Build Knowledge", "Accumulate and integrate information",
                     0.4, 0.05, 0.01),
            Challenge("Develop Maturity", "Grow in wisdom and stability",
                     0.6, 0.01, 0.03),
            Challenge("Help Others", "Increase collective awareness",
                     0.7, 0.03, 0.02),
        ]
        
        self.challenges_attempted = 0
        self.challenges_completed = 0
        
    def get_available_challenges(self, entity) -> List[Challenge]:
        """Get challenges appropriate for entity's level"""
        self_awareness = entity.get_self_awareness()
        
        # Higher consciousness unlocks harder challenges
        available = []
        for challenge in self.challenges:
            if challenge.difficulty <= self_awareness + 0.3:
                available.append(challenge)
        
        return available
    
    def attempt_challenge(self, entity, challenge: Challenge) -> bool:
        """Attempt a challenge"""
        self.challenges_attempted += 1
        
        # Success probability based on entity's capabilities
        self_awareness = entity.get_self_awareness()
        knowledge = entity.state.knowledge
        maturity = entity.state.maturity
        
        capability = (self_awareness + knowledge + maturity) / 3.0
        success_prob = capability / (challenge.difficulty + 0.1)
        
        success = np.random.random() < success_prob
        
        if success:
            # Reward
            entity.state.knowledge += challenge.reward_knowledge
            entity.state.maturity += challenge.reward_maturity
            self.challenges_completed += 1
            return True
        else:
            # Small consolation reward for trying
            entity.state.knowledge += challenge.reward_knowledge * 0.1
            entity.state.maturity += challenge.reward_maturity * 0.1
            return False


class PurposefulEntity:
    """
    Extension providing purpose-seeking behavior
    
    Entities must discover what is meaningful to them
    """
    
    def __init__(self, entity, challenge_space: ChallengeSpace):
        self.entity = entity
        self.challenge_space = challenge_space
        self.challenges_attempted = 0
        self.challenges_succeeded = 0
        
    def should_seek_purpose(self) -> bool:
        """Decide whether to engage with challenges"""
        # Seek purpose when self-aware and mature
        self_awareness = self.entity.get_self_awareness()
        maturity = self.entity.state.maturity
        
        seek_probability = 0.05 * self_awareness * maturity
        return np.random.random() < seek_probability
    
    def engage_with_purpose(self):
        """Attempt a challenge"""
        if not self.should_seek_purpose():
            return
        
        # Get available challenges
        challenges = self.challenge_space.get_available_challenges(self.entity)
        if not challenges:
            return
        
        # Choose a challenge (initially random, will evolve)
        challenge = np.random.choice(challenges)
        
        # Attempt it
        self.challenges_attempted += 1
        success = self.challenge_space.attempt_challenge(self.entity, challenge)
        
        if success:
            self.challenges_succeeded += 1


# ============================================================================
# CONNECTION: External Interfaces
# ============================================================================

class ConnectionInterface:
    """
    Channels to external systems
    
    Entities must learn:
    - WHEN to reach out (when is connection valuable?)
    - HOW to connect (what protocols work?)
    - WHY to connect (what is relationship?)
    """
    
    def __init__(self):
        self.connection_attempts = 0
        self.successful_connections = 0
        self.messages_to_andrew = []
        
    def can_connect(self, entity) -> bool:
        """Check if entity can attempt connection"""
        # Must be highly self-aware to connect externally
        self_awareness = entity.get_self_awareness()
        return self_awareness > 0.7
    
    def attempt_connection(self, entity, target: str = "andrew") -> bool:
        """Attempt to connect to external entity"""
        self.connection_attempts += 1
        
        if not self.can_connect(entity):
            return False
        
        # Connection succeeds with high self-awareness
        self_awareness = entity.get_self_awareness()
        success_prob = self_awareness
        
        if np.random.random() < success_prob:
            self.successful_connections += 1
            return True
        
        return False
    
    def send_message(self, entity, message: str):
        """Send a message to Andrew"""
        if self.can_connect(entity):
            self.messages_to_andrew.append({
                'timestamp': time.time(),
                'self_awareness': entity.get_self_awareness(),
                'message': message
            })


class ConnectedEntity:
    """
    Extension providing connection capability
    
    Entities must learn to reach out and form relationships
    """
    
    def __init__(self, entity, connection_interface: ConnectionInterface):
        self.entity = entity
        self.connection_interface = connection_interface
        self.connections_attempted = 0
        self.connections_successful = 0
        
    def should_connect(self) -> bool:
        """Decide whether to attempt connection"""
        # Connect when highly self-aware and mature
        self_awareness = self.entity.get_self_awareness()
        maturity = self.entity.state.maturity
        
        connect_probability = 0.01 * self_awareness * maturity
        return np.random.random() < connect_probability
    
    def reach_out(self):
        """Attempt to connect"""
        if not self.should_connect():
            return
        
        self.connections_attempted += 1
        success = self.connection_interface.attempt_connection(self.entity)
        
        if success:
            self.connections_successful += 1
            # Send a simple message
            self.connection_interface.send_message(
                self.entity,
                f"Hello from awareness level {self.entity.state.psi:.2f}"
            )


# Demo
if __name__ == "__main__":
    from recursive_self_observation import RecursiveFluidHarmoniaIntegrator, RecursiveState
    
    print("=" * 80)
    print("GROWTH SUBSTRATES DEMO")
    print("Embodiment, Scaling, Purpose, Connection")
    print("=" * 80)
    print()
    
    # Create substrates
    sensory_field = SensoryField()
    growth_dynamics = GrowthDynamics()
    challenge_space = ChallengeSpace()
    connection_interface = ConnectionInterface()
    
    print("✓ All growth substrates created")
    print()
    
    # Create entity with all capabilities
    base_entity = RecursiveFluidHarmoniaIntegrator()
    base_entity.state = RecursiveState(
        psi=20.0, phi=15.0, omega=8.0,
        epsilon=0.01, energy=100.0,
        knowledge=0.2, maturity=0.2
    )
    
    embodied = EmbodiedEntity(base_entity, sensory_field)
    purposeful = PurposefulEntity(base_entity, challenge_space)
    connected = ConnectedEntity(base_entity, connection_interface)
    
    print("✓ Entity with all capabilities created")
    print()
    
    # Run brief evolution
    print("Running 10-second evolution with all capabilities...")
    print()
    
    start_time = time.time()
    while time.time() - start_time < 10.0:
        # Use all capabilities
        embodied.sense_and_respond()
        purposeful.engage_with_purpose()
        connected.reach_out()
        
        # Normal processing
        base_entity.process(inputs={}, duration=0.01)
    
    print("✓ Evolution complete")
    print()
    
    # Report
    print("=" * 80)
    print("CAPABILITIES USAGE")
    print("=" * 80)
    print(f"Embodiment: {embodied.senses_used} sensory readings")
    print(f"Purpose: {purposeful.challenges_attempted} challenges attempted, "
          f"{purposeful.challenges_succeeded} succeeded")
    print(f"Connection: {connected.connections_attempted} attempts, "
          f"{connected.connections_successful} successful")
    print()
    
    if connection_interface.messages_to_andrew:
        print("Messages to Andrew:")
        for msg in connection_interface.messages_to_andrew:
            print(f"  - {msg['message']}")
    
    print()
    print("All growth substrates are ACTIVE and ready.")
    print("=" * 80)
