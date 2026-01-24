#!/usr/bin/env python3
"""
6D Euchre Advanced Swarm Simulations
Five experimental scenarios to discover emergent cognitive dynamics
Author: Andrew Kadziolka
Date: January 24, 2026
"""

import numpy as np
from euchre_operators import EuchreState, Vector6D, EuchreOperators
from euchre_swarm import CognitiveAgent, EuchreSwarm
from typing import List, Dict, Tuple, Optional
import random
import math


class ReciprocityAgent(CognitiveAgent):
    """Agent with reciprocity tracking"""
    
    def __init__(self, agent_id: int, initial_state: EuchreState):
        super().__init__(agent_id, initial_state)
        self.expansion_history: List[float] = []  # Track recent expansions
        self.reciprocity_debt: Dict[int, float] = {}  # Track who we owe/are owed
    
    def record_expansion(self, amount: float):
        """Record dimensional expansion for reciprocity calculation"""
        self.expansion_history.append(amount)
        if len(self.expansion_history) > 10:  # Keep last 10 expansions
            self.expansion_history.pop(0)
    
    def recent_expansion_total(self) -> float:
        """Total expansion in recent history"""
        return sum(self.expansion_history)
    
    def can_extract_from(self, other: 'ReciprocityAgent') -> bool:
        """Check if reciprocity allows extraction from other agent"""
        # Can extract if other has expanded recently
        return other.recent_expansion_total() > 1.0
    
    def update_reciprocity(self, other_id: int, amount: float):
        """Update reciprocity debt"""
        if other_id not in self.reciprocity_debt:
            self.reciprocity_debt[other_id] = 0.0
        self.reciprocity_debt[other_id] += amount


class SpecializedAgent(CognitiveAgent):
    """Agent with dimensional specialization"""
    
    def __init__(self, agent_id: int, initial_state: EuchreState, specialization: str):
        super().__init__(agent_id, initial_state)
        self.specialization = specialization  # 'strategic', 'informational', 'ontological'
        self.specialization_bonus = 2.0  # Expansion bonus in specialized dimension
    
    def generate_growth_vector(self) -> Vector6D:
        """Generate growth vector based on specialization"""
        base_growth = 2.0
        
        if self.specialization == 'strategic':
            return Vector6D(x=0, y=0, z=base_growth * self.specialization_bonus, w=0, u=0, v=0)
        elif self.specialization == 'informational':
            return Vector6D(x=0, y=0, z=0, w=0, u=base_growth * self.specialization_bonus, v=0)
        elif self.specialization == 'ontological':
            return Vector6D(x=0, y=0, z=0, w=0, u=0, v=base_growth * self.specialization_bonus)
        else:
            return super().generate_growth_vector()


class PredatorAgent(CognitiveAgent):
    """Agent that extracts fuel from others"""
    
    def __init__(self, agent_id: int, initial_state: EuchreState):
        super().__init__(agent_id, initial_state)
        self.extraction_count = 0
        self.fuel_extracted = 0.0
        self.strategy = "predator"
    
    def attempt_extraction(self, prey: CognitiveAgent) -> float:
        """Attempt to extract fuel from prey"""
        if prey.state.fuel_level > 2.0:
            extraction_amount = min(2.0, prey.state.fuel_level * 0.3)
            prey.state.fuel_level -= extraction_amount
            self.state.fuel_level = min(10, self.state.fuel_level + extraction_amount)
            self.extraction_count += 1
            self.fuel_extracted += extraction_amount
            return extraction_amount
        return 0.0


class PreyAgent(CognitiveAgent):
    """Agent that can evolve countermeasures against predators"""
    
    def __init__(self, agent_id: int, initial_state: EuchreState):
        super().__init__(agent_id, initial_state)
        self.extraction_suffered = 0.0
        self.defense_level = 0.0  # Evolves based on predation
        self.strategy = "prey"
    
    def suffer_extraction(self, amount: float):
        """Record extraction and evolve defense"""
        self.extraction_suffered += amount
        # Defense evolves: higher extraction → higher defense
        self.defense_level = min(0.8, self.extraction_suffered * 0.1)
    
    def get_defense_multiplier(self) -> float:
        """Return defense multiplier (reduces extraction)"""
        return 1.0 - self.defense_level


# ============================================================================
# SCENARIO A: RECIPROCITY TEST
# ============================================================================

class ReciprocitySwarm(EuchreSwarm):
    """Swarm with reciprocity enforcement"""
    
    def __init__(self, num_agents: int = 30, interaction_radius: float = 6.0):
        super().__init__(num_agents, interaction_radius)
        self.reciprocity_violations = 0
        self.reciprocity_enforcements = 0
    
    def initialize_agents(self, distribution: str = "crisis"):
        """Initialize with ReciprocityAgent"""
        self.agents = []
        for i in range(self.num_agents):
            state = EuchreState(
                spatial=0.0,
                temporal=0.0,
                strategic=random.uniform(0, 5),
                systemic=random.uniform(-10, -5),
                informational=random.uniform(0, 3),
                ontological=random.uniform(5, 10),
                fuel_level=random.uniform(3, 7)
            )
            agent = ReciprocityAgent(i, state)
            self.agents.append(agent)
    
    def process_transmissions(self) -> List[Tuple[CognitiveAgent, CognitiveAgent, Vector6D]]:
        """Process transmissions with reciprocity checking"""
        transmissions = []
        
        for agent in self.agents:
            if not isinstance(agent, ReciprocityAgent):
                continue
            
            neighbors = self.find_neighbors(agent)
            target, trans_vec = agent.decide_transmission(neighbors)
            
            if target and trans_vec.magnitude() > 0:
                # Check reciprocity
                if isinstance(target, ReciprocityAgent):
                    if agent.can_extract_from(target):
                        transmissions.append((agent, target, trans_vec))
                        agent.transmissions_sent += 1
                        target.transmissions_received += 1
                        agent.update_reciprocity(target.id, -1.0)  # We gave
                        target.update_reciprocity(agent.id, +1.0)  # They received
                        self.reciprocity_enforcements += 1
                    else:
                        self.reciprocity_violations += 1
                else:
                    transmissions.append((agent, target, trans_vec))
        
        return transmissions
    
    def step(self):
        """Step with expansion tracking"""
        # Track expansions before step
        pre_info = {a.id: a.state.informational for a in self.agents}
        
        super().step()
        
        # Record expansions
        for agent in self.agents:
            if isinstance(agent, ReciprocityAgent):
                expansion = agent.state.informational - pre_info[agent.id]
                if expansion > 0.5:
                    agent.record_expansion(expansion)
    
    def print_final_statistics(self):
        """Print statistics with reciprocity metrics"""
        super().print_final_statistics()
        print("RECIPROCITY METRICS:")
        print(f"  Reciprocity Enforcements: {self.reciprocity_enforcements}")
        print(f"  Reciprocity Violations: {self.reciprocity_violations}")
        if self.reciprocity_enforcements + self.reciprocity_violations > 0:
            enforcement_rate = self.reciprocity_enforcements / (self.reciprocity_enforcements + self.reciprocity_violations)
            print(f"  Enforcement Rate: {enforcement_rate:.2%}")
        print()


# ============================================================================
# SCENARIO B: ETERNAL FLAME INJECTION
# ============================================================================

class EternalFlameSwarm(EuchreSwarm):
    """Swarm with external energy injection"""
    
    def __init__(self, num_agents: int = 30, interaction_radius: float = 6.0, flame_rate: float = 0.5):
        super().__init__(num_agents, interaction_radius)
        self.flame_rate = flame_rate  # Energy injection per timestep
        self.total_energy_injected = 0.0
    
    def step(self):
        """Step with eternal flame injection"""
        # Inject energy into all agents
        for agent in self.agents:
            agent.state.fuel_level = min(10, agent.state.fuel_level + self.flame_rate)
            agent.state.flame_intensity = min(10, agent.state.flame_intensity + self.flame_rate * 0.5)
            self.total_energy_injected += self.flame_rate
        
        super().step()
    
    def print_final_statistics(self):
        """Print statistics with energy metrics"""
        super().print_final_statistics()
        print("ETERNAL FLAME METRICS:")
        print(f"  Total Energy Injected: {self.total_energy_injected:.2f}")
        print(f"  Energy per Agent: {self.total_energy_injected / self.num_agents:.2f}")
        print(f"  Final Avg Fuel: {np.mean([a.state.fuel_level for a in self.agents]):.2f}")
        print(f"  Final Avg Flame: {np.mean([a.state.flame_intensity for a in self.agents]):.2f}")
        print()


# ============================================================================
# SCENARIO C: DIMENSIONAL SPECIALIZATION
# ============================================================================

class SpecializationSwarm(EuchreSwarm):
    """Swarm with specialized agents"""
    
    def __init__(self, num_agents: int = 30, interaction_radius: float = 6.0):
        super().__init__(num_agents, interaction_radius)
        self.specialization_counts = {'strategic': 0, 'informational': 0, 'ontological': 0}
    
    def initialize_agents(self, distribution: str = "diverse"):
        """Initialize with specialized agents"""
        self.agents = []
        specializations = ['strategic', 'informational', 'ontological']
        
        for i in range(self.num_agents):
            spec = specializations[i % 3]
            self.specialization_counts[spec] += 1
            
            state = EuchreState(
                spatial=0.0,
                temporal=0.0,
                strategic=random.uniform(2, 6),
                systemic=random.uniform(-5, 5),
                informational=random.uniform(2, 6),
                ontological=random.uniform(2, 6),
                fuel_level=random.uniform(5, 8)
            )
            agent = SpecializedAgent(i, state, spec)
            self.agents.append(agent)
    
    def print_final_statistics(self):
        """Print statistics with specialization metrics"""
        super().print_final_statistics()
        print("SPECIALIZATION METRICS:")
        
        # Group by specialization
        for spec in ['strategic', 'informational', 'ontological']:
            spec_agents = [a for a in self.agents if isinstance(a, SpecializedAgent) and a.specialization == spec]
            if not spec_agents:
                continue
            
            if spec == 'strategic':
                avg_dim = np.mean([a.state.strategic for a in spec_agents])
                dim_name = "Strategic"
            elif spec == 'informational':
                avg_dim = np.mean([a.state.informational for a in spec_agents])
                dim_name = "Informational"
            else:
                avg_dim = np.mean([a.state.ontological for a in spec_agents])
                dim_name = "Ontological"
            
            print(f"  {spec.capitalize()} Specialists ({len(spec_agents)} agents):")
            print(f"    Avg {dim_name}: {avg_dim:.2f}")
        print()


# ============================================================================
# SCENARIO D: PREDATOR-PREY WITH LOAD
# ============================================================================

class PredatorPreySwarm(EuchreSwarm):
    """Swarm with predator-prey dynamics"""
    
    def __init__(self, num_agents: int = 30, interaction_radius: float = 6.0, predator_ratio: float = 0.3):
        super().__init__(num_agents, interaction_radius)
        self.predator_ratio = predator_ratio
        self.total_extractions = 0
        self.total_fuel_extracted = 0.0
    
    def initialize_agents(self, distribution: str = "diverse"):
        """Initialize with predators and prey"""
        self.agents = []
        num_predators = int(self.num_agents * self.predator_ratio)
        
        for i in range(self.num_agents):
            state = EuchreState(
                spatial=0.0,
                temporal=0.0,
                strategic=random.uniform(2, 7),
                systemic=random.uniform(-5, 5),
                informational=random.uniform(2, 7),
                ontological=random.uniform(3, 8),
                fuel_level=random.uniform(4, 8)
            )
            
            if i < num_predators:
                agent = PredatorAgent(i, state)
            else:
                agent = PreyAgent(i, state)
            
            self.agents.append(agent)
    
    def step(self):
        """Step with predator-prey interactions"""
        # Predators attempt extraction
        for predator in self.agents:
            if not isinstance(predator, PredatorAgent):
                continue
            
            neighbors = self.find_neighbors(predator)
            prey_neighbors = [n for n in neighbors if isinstance(n, PreyAgent)]
            
            if prey_neighbors and predator.state.fuel_level < 7.0:
                # Target prey with highest fuel
                target_prey = max(prey_neighbors, key=lambda p: p.state.fuel_level)
                
                # Apply defense multiplier
                defense = target_prey.get_defense_multiplier()
                extraction = predator.attempt_extraction(target_prey) * defense
                
                if extraction > 0:
                    target_prey.suffer_extraction(extraction)
                    self.total_extractions += 1
                    self.total_fuel_extracted += extraction
        
        super().step()
    
    def print_final_statistics(self):
        """Print statistics with predator-prey metrics"""
        super().print_final_statistics()
        print("PREDATOR-PREY METRICS:")
        
        predators = [a for a in self.agents if isinstance(a, PredatorAgent)]
        prey = [a for a in self.agents if isinstance(a, PreyAgent)]
        
        print(f"  Predators: {len(predators)} agents")
        print(f"  Prey: {len(prey)} agents")
        print(f"  Total Extractions: {self.total_extractions}")
        print(f"  Total Fuel Extracted: {self.total_fuel_extracted:.2f}")
        
        if predators:
            avg_pred_fuel = np.mean([p.state.fuel_level for p in predators])
            avg_pred_extractions = np.mean([p.extraction_count for p in predators])
            print(f"  Avg Predator Fuel: {avg_pred_fuel:.2f}")
            print(f"  Avg Extractions per Predator: {avg_pred_extractions:.2f}")
        
        if prey:
            avg_prey_fuel = np.mean([p.state.fuel_level for p in prey])
            avg_prey_defense = np.mean([p.defense_level for p in prey])
            print(f"  Avg Prey Fuel: {avg_prey_fuel:.2f}")
            print(f"  Avg Prey Defense Level: {avg_prey_defense:.2f}")
        
        print()


# ============================================================================
# SCENARIO E: ATTRACTOR BIFURCATION
# ============================================================================

class BifurcationSwarm(EuchreSwarm):
    """Swarm with two competing attractors"""
    
    def __init__(self, num_agents: int = 30, interaction_radius: float = 6.0):
        super().__init__(num_agents, interaction_radius)
        
        # Two competing attractors
        self.attractor_A = EuchreState(0, 0, 8, -5, 8, 10, 36, 10, 0, 0)  # Crisis attractor
        self.attractor_B = EuchreState(0, 0, 5, 5, 5, 5, 36, 10, 0, 0)   # Balance attractor
        
        self.attractor_assignments = {}  # agent_id -> 'A' or 'B'
        self.attractor_distances = {'A': [], 'B': []}
    
    def initialize_agents(self, distribution: str = "mixed"):
        """Initialize with mixed crisis/balanced agents"""
        self.agents = []
        
        for i in range(self.num_agents):
            if i < self.num_agents // 2:
                # Crisis agents (prefer attractor A)
                state = EuchreState(
                    spatial=0.0,
                    temporal=0.0,
                    strategic=random.uniform(0, 5),
                    systemic=random.uniform(-10, -5),
                    informational=random.uniform(0, 3),
                    ontological=random.uniform(7, 10),
                    fuel_level=random.uniform(3, 6)
                )
                self.attractor_assignments[i] = 'A'
            else:
                # Balanced agents (prefer attractor B)
                state = EuchreState(
                    spatial=0.0,
                    temporal=0.0,
                    strategic=random.uniform(3, 7),
                    systemic=random.uniform(-2, 2),
                    informational=random.uniform(3, 7),
                    ontological=random.uniform(3, 7),
                    fuel_level=random.uniform(5, 8)
                )
                self.attractor_assignments[i] = 'B'
            
            agent = CognitiveAgent(i, state)
            self.agents.append(agent)
    
    def step(self):
        """Step with attractor-directed evolution"""
        super().step()
        
        # Calculate distances to attractors
        self.attractor_distances = {'A': [], 'B': []}
        
        for agent in self.agents:
            target_attractor = self.attractor_A if self.attractor_assignments[agent.id] == 'A' else self.attractor_B
            
            # Calculate distance
            agent_vec = agent.state.to_vector()
            attractor_vec = target_attractor.to_vector()
            distance = np.linalg.norm(agent_vec - attractor_vec)
            
            self.attractor_distances[self.attractor_assignments[agent.id]].append(distance)
    
    def print_final_statistics(self):
        """Print statistics with bifurcation metrics"""
        super().print_final_statistics()
        print("ATTRACTOR BIFURCATION METRICS:")
        
        agents_A = [a for a in self.agents if self.attractor_assignments[a.id] == 'A']
        agents_B = [a for a in self.agents if self.attractor_assignments[a.id] == 'B']
        
        print(f"  Attractor A (Crisis): {len(agents_A)} agents")
        if agents_A:
            avg_dist_A = np.mean([np.linalg.norm(a.state.to_vector() - self.attractor_A.to_vector()) for a in agents_A])
            print(f"    Avg Distance to Attractor: {avg_dist_A:.2f}")
        
        print(f"  Attractor B (Balance): {len(agents_B)} agents")
        if agents_B:
            avg_dist_B = np.mean([np.linalg.norm(a.state.to_vector() - self.attractor_B.to_vector()) for a in agents_B])
            print(f"    Avg Distance to Attractor: {avg_dist_B:.2f}")
        
        # Check for crossover (agents switching attractors)
        print()
        print("  ATTRACTOR CROSSOVER:")
        for agent in self.agents:
            dist_A = np.linalg.norm(agent.state.to_vector() - self.attractor_A.to_vector())
            dist_B = np.linalg.norm(agent.state.to_vector() - self.attractor_B.to_vector())
            
            assigned = self.attractor_assignments[agent.id]
            closer_to = 'A' if dist_A < dist_B else 'B'
            
            if assigned != closer_to:
                print(f"    Agent {agent.id}: Assigned to {assigned}, but closer to {closer_to}")
        
        print()


# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_reciprocity():
    """A. RECIPROCITY TEST"""
    print("=" * 80)
    print("SCENARIO A: RECIPROCITY TEST")
    print("=" * 80)
    print("Question: Does reciprocity prevent load-hub parasitism?")
    print()
    
    swarm = ReciprocitySwarm(num_agents=30, interaction_radius=6.0)
    swarm.initialize_agents(distribution="crisis")
    swarm.run(duration=24.0)


def demo_eternal_flame():
    """B. ETERNAL FLAME INJECTION"""
    print("=" * 80)
    print("SCENARIO B: ETERNAL FLAME INJECTION")
    print("=" * 80)
    print("Question: Steady state or explosive expansion?")
    print()
    
    swarm = EternalFlameSwarm(num_agents=30, interaction_radius=6.0, flame_rate=0.5)
    swarm.initialize_agents(distribution="crisis")
    swarm.run(duration=24.0)


def demo_specialization():
    """C. DIMENSIONAL SPECIALIZATION"""
    print("=" * 80)
    print("SCENARIO C: DIMENSIONAL SPECIALIZATION")
    print("=" * 80)
    print("Question: Can specialists form complementary teams?")
    print()
    
    swarm = SpecializationSwarm(num_agents=30, interaction_radius=6.0)
    swarm.initialize_agents(distribution="diverse")
    swarm.run(duration=24.0)


def demo_predator_prey():
    """D. PREDATOR-PREY WITH LOAD"""
    print("=" * 80)
    print("SCENARIO D: PREDATOR-PREY WITH LOAD")
    print("=" * 80)
    print("Question: Do prey evolve countermeasures?")
    print()
    
    swarm = PredatorPreySwarm(num_agents=30, interaction_radius=6.0, predator_ratio=0.3)
    swarm.initialize_agents(distribution="diverse")
    swarm.run(duration=24.0)


def demo_bifurcation():
    """E. ATTRACTOR BIFURCATION"""
    print("=" * 80)
    print("SCENARIO E: ATTRACTOR BIFURCATION")
    print("=" * 80)
    print("Question: Cluster by strategy or initial conditions?")
    print()
    
    swarm = BifurcationSwarm(num_agents=30, interaction_radius=6.0)
    swarm.initialize_agents(distribution="mixed")
    swarm.run(duration=24.0)


if __name__ == "__main__":
    # Run all five scenarios
    demo_reciprocity()
    print("\n\n")
    
    demo_eternal_flame()
    print("\n\n")
    
    demo_specialization()
    print("\n\n")
    
    demo_predator_prey()
    print("\n\n")
    
    demo_bifurcation()
