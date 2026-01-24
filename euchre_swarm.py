#!/usr/bin/env python3
"""
6D Euchre Swarm Simulation
Multi-agent cognitive dynamics in 6D phase space
Author: Andrew Kadziolka
Date: January 24, 2026
"""

import numpy as np
from euchre_operators import EuchreState, Vector6D, EuchreOperators
from typing import List, Dict, Tuple, Optional
import random
import math

class CognitiveAgent:
    """
    Individual agent in 6D Euchre swarm
    Each agent is an autonomous cognitive entity
    """
    
    def __init__(self, agent_id: int, initial_state: EuchreState):
        self.id = agent_id
        self.state = initial_state
        self.history: List[EuchreState] = [initial_state.copy()]
        self.transmissions_sent = 0
        self.transmissions_received = 0
        self.load_transferred = 0.0
        self.fuel_received = 0.0
        self.strategy = self._determine_initial_strategy()
        
        # Personality traits (affect behavior)
        self.cooperation_tendency = random.uniform(0.3, 0.9)
        self.exploration_rate = random.uniform(0.1, 0.5)
        self.transmission_threshold = random.uniform(3.0, 7.0)
    
    def _determine_initial_strategy(self) -> str:
        """Determine agent's initial strategy based on starting position"""
        if self.state.systemic < -5:
            return "load_seeker"  # High load, needs transmission
        elif self.state.informational > 7:
            return "transmitter"  # High info, can help others
        elif self.state.fuel_level > 8:
            return "explorer"  # High fuel, can expand dimensions
        else:
            return "balanced"
    
    def perceive_environment(self, neighbors: List['CognitiveAgent']) -> Vector6D:
        """
        Generate perception vector based on nearby agents
        """
        if not neighbors:
            # Self-perception only
            return Vector6D(
                x=0,
                y=random.uniform(0, 2),
                z=0,
                w=self.state.systemic,
                u=0,
                v=self.state.ontological
            )
        
        # Average neighbor positions
        avg_strategic = np.mean([n.state.strategic for n in neighbors])
        avg_systemic = np.mean([n.state.systemic for n in neighbors])
        avg_info = np.mean([n.state.informational for n in neighbors])
        
        return Vector6D(
            x=0,
            y=random.uniform(0, 2),
            z=(avg_strategic - self.state.strategic) * 0.1,
            w=(avg_systemic - self.state.systemic) * 0.1,
            u=(avg_info - self.state.informational) * 0.1,
            v=self.state.ontological * 0.1
        )
    
    def decide_transmission(self, neighbors: List['CognitiveAgent']) -> Tuple[Optional['CognitiveAgent'], Vector6D]:
        """
        Decide whether to transmit and to whom
        Returns (target_agent, transmission_vector)
        """
        # Don't transmit if fuel too low
        if self.state.fuel_level < 2.0:
            return None, Vector6D()
        
        # Don't transmit if load not high enough
        if abs(self.state.systemic) < self.transmission_threshold:
            return None, Vector6D()
        
        # Find agent with lowest load (most able to receive)
        if neighbors:
            # Cooperative agents prefer helping high-load neighbors
            if random.random() < self.cooperation_tendency:
                target = max(neighbors, key=lambda n: abs(n.state.systemic))
            else:
                # Selfish agents prefer low-load neighbors (easier transmission)
                target = min(neighbors, key=lambda n: abs(n.state.systemic))
            
            # Calculate transmission vector
            load_to_transfer = abs(self.state.systemic) * 0.3  # Transfer 30% of load
            info_to_share = self.state.informational * 0.2  # Share 20% of info
            
            transmission_vec = Vector6D(
                x=0,
                y=0,
                z=self.state.strategic * 0.5,
                w=0,
                u=info_to_share,
                v=0
            )
            
            return target, transmission_vec
        
        return None, Vector6D()
    
    def generate_load_vector(self) -> Vector6D:
        """Generate load vector based on current state"""
        # Load increases with distance from equilibrium
        load_magnitude = abs(self.state.systemic) + (10 - self.state.fuel_level) * 0.5
        
        return Vector6D(
            x=0,
            y=0,
            z=0,
            w=-load_magnitude,
            u=0,
            v=0
        )
    
    def generate_growth_vector(self) -> Vector6D:
        """Generate growth vector based on strategy"""
        if self.strategy == "explorer":
            growth_magnitude = self.state.fuel_level * 0.5
        elif self.strategy == "transmitter":
            growth_magnitude = self.state.informational * 0.3
        else:
            growth_magnitude = 2.0
        
        return Vector6D(
            x=0,
            y=0,
            z=0,
            w=0,
            u=growth_magnitude,
            v=0
        )
    
    def update_strategy(self):
        """Adapt strategy based on current state"""
        if self.state.fuel_level < 3.0:
            self.strategy = "load_seeker"
        elif self.state.informational > 7.0 and self.state.fuel_level > 5.0:
            self.strategy = "transmitter"
        elif self.state.fuel_level > 8.0:
            self.strategy = "explorer"
        else:
            self.strategy = "balanced"


class EuchreSwarm:
    """
    Multi-agent swarm simulation in 6D Euchre phase space
    """
    
    def __init__(self, num_agents: int = 20, interaction_radius: float = 5.0):
        self.num_agents = num_agents
        self.interaction_radius = interaction_radius
        self.agents: List[CognitiveAgent] = []
        self.operators = EuchreOperators()
        self.time = 0.0
        self.dt = 1.0
        
        # Swarm statistics
        self.total_transmissions = 0
        self.total_expansions = 0
        self.collective_fuel = 0.0
        self.collective_load = 0.0
        
    def initialize_agents(self, distribution: str = "random"):
        """
        Initialize agents with different distributions
        
        distribution options:
        - "random": Random positions in phase space
        - "clustered": Agents start near each other
        - "diverse": Agents span the full range of each dimension
        - "crisis": All agents start with high load
        """
        self.agents = []
        
        for i in range(self.num_agents):
            if distribution == "random":
                state = EuchreState(
                    spatial=0.0,
                    temporal=0.0,
                    strategic=random.uniform(0, 10),
                    systemic=random.uniform(-10, 10),
                    informational=random.uniform(0, 10),
                    ontological=random.uniform(0, 10),
                    fuel_level=random.uniform(5, 10)
                )
            elif distribution == "clustered":
                center = (5.0, 0.0, 5.0, 5.0)
                state = EuchreState(
                    spatial=0.0,
                    temporal=0.0,
                    strategic=center[0] + random.gauss(0, 1),
                    systemic=center[1] + random.gauss(0, 1),
                    informational=center[2] + random.gauss(0, 1),
                    ontological=center[3] + random.gauss(0, 1),
                    fuel_level=random.uniform(7, 10)
                )
            elif distribution == "diverse":
                state = EuchreState(
                    spatial=0.0,
                    temporal=0.0,
                    strategic=i * 10.0 / self.num_agents,
                    systemic=-10 + i * 20.0 / self.num_agents,
                    informational=i * 10.0 / self.num_agents,
                    ontological=i * 10.0 / self.num_agents,
                    fuel_level=5 + i * 5.0 / self.num_agents
                )
            elif distribution == "crisis":
                state = EuchreState(
                    spatial=0.0,
                    temporal=0.0,
                    strategic=random.uniform(0, 5),
                    systemic=random.uniform(-10, -5),  # High load
                    informational=random.uniform(0, 3),  # Low info
                    ontological=random.uniform(5, 10),
                    fuel_level=random.uniform(3, 7)  # Medium fuel
                )
            
            agent = CognitiveAgent(i, state)
            self.agents.append(agent)
    
    def find_neighbors(self, agent: CognitiveAgent) -> List[CognitiveAgent]:
        """Find agents within interaction radius"""
        neighbors = []
        agent_pos = agent.state.to_vector()
        
        for other in self.agents:
            if other.id == agent.id:
                continue
            
            other_pos = other.state.to_vector()
            distance = np.linalg.norm(agent_pos - other_pos)
            
            if distance < self.interaction_radius:
                neighbors.append(other)
        
        return neighbors
    
    def process_transmissions(self) -> List[Tuple[CognitiveAgent, CognitiveAgent, Vector6D]]:
        """
        Process all agent transmission decisions
        Returns list of (sender, receiver, transmission_vector)
        """
        transmissions = []
        
        for agent in self.agents:
            neighbors = self.find_neighbors(agent)
            target, trans_vec = agent.decide_transmission(neighbors)
            
            if target and trans_vec.magnitude() > 0:
                transmissions.append((agent, target, trans_vec))
                agent.transmissions_sent += 1
                target.transmissions_received += 1
                self.total_transmissions += 1
        
        return transmissions
    
    def step(self):
        """Execute one time step of swarm simulation"""
        # Process transmissions
        transmissions = self.process_transmissions()
        
        # Update each agent
        for agent in self.agents:
            neighbors = self.find_neighbors(agent)
            
            # Generate operator vectors
            perception_vec = agent.perceive_environment(neighbors)
            load_vec = agent.generate_load_vector()
            growth_vec = agent.generate_growth_vector()
            
            # Check if agent is receiving transmission
            transmission_vec = Vector6D()
            for sender, receiver, trans_vec in transmissions:
                if receiver.id == agent.id:
                    transmission_vec = Vector6D(
                        x=transmission_vec.x + trans_vec.x,
                        y=transmission_vec.y + trans_vec.y,
                        z=transmission_vec.z + trans_vec.z,
                        w=transmission_vec.w + trans_vec.w,
                        u=transmission_vec.u + trans_vec.u,
                        v=transmission_vec.v + trans_vec.v
                    )
                    # Receiver gets fuel boost from transmission
                    agent.state.fuel_level = min(10, agent.state.fuel_level + 0.5)
                    agent.fuel_received += 0.5
            
            # If agent is sending transmission, use that vector
            for sender, receiver, trans_vec in transmissions:
                if sender.id == agent.id:
                    transmission_vec = trans_vec
                    # Sender loses some load
                    load_magnitude = abs(agent.state.systemic) * 0.3
                    agent.load_transferred += load_magnitude
            
            # Evolve agent state
            new_state = self.operators.evolution_operator(
                agent.state,
                perception_vec,
                transmission_vec,
                load_vec,
                growth_vec,
                self.dt
            )
            
            # Check for dimensional expansion
            if new_state.fuel_level > self.operators.fuel_threshold:
                expanded_state, expansion = self.operators.dimensional_expansion(
                    new_state, 'informational', self.dt
                )
                if expansion > 0:
                    self.total_expansions += 1
                new_state = expanded_state
            
            # Update agent
            agent.state = new_state
            agent.history.append(new_state.copy())
            agent.update_strategy()
        
        # Update time
        self.time += self.dt
        
        # Update swarm statistics
        self.collective_fuel = sum(a.state.fuel_level for a in self.agents)
        self.collective_load = sum(abs(a.state.systemic) for a in self.agents)
    
    def run(self, duration: float = 24.0):
        """Run swarm simulation for specified duration"""
        num_steps = int(duration / self.dt)
        
        print(f"Starting swarm simulation: {self.num_agents} agents, {duration} hours")
        print(f"Interaction radius: {self.interaction_radius}")
        print()
        
        for step in range(num_steps):
            self.step()
            
            if step % 6 == 0:  # Report every 6 hours
                self.print_status()
        
        print()
        print("=" * 80)
        print("SIMULATION COMPLETE")
        print("=" * 80)
        self.print_final_statistics()
    
    def print_status(self):
        """Print current swarm status"""
        avg_strategic = np.mean([a.state.strategic for a in self.agents])
        avg_systemic = np.mean([a.state.systemic for a in self.agents])
        avg_info = np.mean([a.state.informational for a in self.agents])
        avg_fuel = np.mean([a.state.fuel_level for a in self.agents])
        
        print(f"t = {self.time:5.1f}h | "
              f"Agents: {self.num_agents} | "
              f"Transmissions: {self.total_transmissions:3d} | "
              f"Expansions: {self.total_expansions:3d}")
        print(f"         | "
              f"Avg Strategic: {avg_strategic:5.2f} | "
              f"Avg Systemic: {avg_systemic:6.2f} | "
              f"Avg Info: {avg_info:5.2f} | "
              f"Avg Fuel: {avg_fuel:5.2f}")
        print()
    
    def print_final_statistics(self):
        """Print final swarm statistics"""
        print()
        print("COLLECTIVE STATISTICS:")
        print("-" * 80)
        print(f"Total Transmissions: {self.total_transmissions}")
        print(f"Total Dimensional Expansions: {self.total_expansions}")
        print(f"Transmissions per Agent: {self.total_transmissions / self.num_agents:.2f}")
        print(f"Expansions per Agent: {self.total_expansions / self.num_agents:.2f}")
        print()
        
        print("STRATEGY DISTRIBUTION:")
        strategy_counts = {}
        for agent in self.agents:
            strategy_counts[agent.strategy] = strategy_counts.get(agent.strategy, 0) + 1
        for strategy, count in sorted(strategy_counts.items()):
            print(f"  {strategy:15s}: {count:3d} agents ({count/self.num_agents*100:5.1f}%)")
        print()
        
        print("DIMENSIONAL AVERAGES (Initial → Final):")
        initial_avg = {
            'strategic': np.mean([a.history[0].strategic for a in self.agents]),
            'systemic': np.mean([a.history[0].systemic for a in self.agents]),
            'informational': np.mean([a.history[0].informational for a in self.agents]),
            'ontological': np.mean([a.history[0].ontological for a in self.agents]),
            'fuel': np.mean([a.history[0].fuel_level for a in self.agents])
        }
        final_avg = {
            'strategic': np.mean([a.state.strategic for a in self.agents]),
            'systemic': np.mean([a.state.systemic for a in self.agents]),
            'informational': np.mean([a.state.informational for a in self.agents]),
            'ontological': np.mean([a.state.ontological for a in self.agents]),
            'fuel': np.mean([a.state.fuel_level for a in self.agents])
        }
        
        for dim in ['strategic', 'systemic', 'informational', 'ontological', 'fuel']:
            delta = final_avg[dim] - initial_avg[dim]
            print(f"  {dim:15s}: {initial_avg[dim]:6.2f} → {final_avg[dim]:6.2f} (Δ = {delta:+6.2f})")
        print()
        
        print("TOP 5 TRANSMITTERS:")
        top_transmitters = sorted(self.agents, key=lambda a: a.transmissions_sent, reverse=True)[:5]
        for i, agent in enumerate(top_transmitters, 1):
            print(f"  {i}. Agent {agent.id:3d}: {agent.transmissions_sent:3d} transmissions, "
                  f"strategy={agent.strategy}, info={agent.state.informational:.1f}")
        print()
        
        print("TOP 5 EXPANDERS:")
        # Count expansions by looking at info dimension jumps
        expansion_counts = []
        for agent in self.agents:
            expansions = 0
            for i in range(1, len(agent.history)):
                if agent.history[i].informational > agent.history[i-1].informational + 0.5:
                    expansions += 1
            expansion_counts.append((agent, expansions))
        
        top_expanders = sorted(expansion_counts, key=lambda x: x[1], reverse=True)[:5]
        for i, (agent, expansions) in enumerate(top_expanders, 1):
            print(f"  {i}. Agent {agent.id:3d}: {expansions:3d} expansions, "
                  f"strategy={agent.strategy}, fuel={agent.state.fuel_level:.1f}")
        print()
        
        print("EMERGENT PATTERNS:")
        # Detect cooperation vs competition
        cooperation_score = np.mean([a.cooperation_tendency for a in self.agents])
        print(f"  Cooperation Score: {cooperation_score:.2f}")
        
        # Detect clustering
        positions = np.array([a.state.to_vector() for a in self.agents])
        centroid = np.mean(positions, axis=0)
        avg_distance_to_centroid = np.mean([np.linalg.norm(pos - centroid) for pos in positions])
        print(f"  Clustering (avg distance to centroid): {avg_distance_to_centroid:.2f}")
        
        # Detect load distribution efficiency
        initial_load_variance = np.var([abs(a.history[0].systemic) for a in self.agents])
        final_load_variance = np.var([abs(a.state.systemic) for a in self.agents])
        print(f"  Load Distribution: variance {initial_load_variance:.2f} → {final_load_variance:.2f}")
        
        if final_load_variance < initial_load_variance:
            print(f"  → Load EQUALIZED (more efficient distribution)")
        else:
            print(f"  → Load CONCENTRATED (less efficient distribution)")


def demo_swarm_crisis():
    """
    Demo: Crisis scenario - all agents start with high load
    Watch emergence of cooperation through transmission
    """
    print("=" * 80)
    print("6D EUCHRE SWARM SIMULATION: CRISIS SCENARIO")
    print("=" * 80)
    print()
    print("Scenario: All agents start with high cognitive load")
    print("Question: Will they discover cooperation through transmission?")
    print()
    
    swarm = EuchreSwarm(num_agents=30, interaction_radius=6.0)
    swarm.initialize_agents(distribution="crisis")
    swarm.run(duration=24.0)


def demo_swarm_diverse():
    """
    Demo: Diverse agents - spanning full range of dimensions
    Watch emergence of specialization and roles
    """
    print("=" * 80)
    print("6D EUCHRE SWARM SIMULATION: DIVERSE AGENTS")
    print("=" * 80)
    print()
    print("Scenario: Agents span full range of cognitive dimensions")
    print("Question: Will specialized roles emerge?")
    print()
    
    swarm = EuchreSwarm(num_agents=25, interaction_radius=7.0)
    swarm.initialize_agents(distribution="diverse")
    swarm.run(duration=24.0)


if __name__ == "__main__":
    # Run crisis scenario
    demo_swarm_crisis()
    
    print("\n\n")
    
    # Run diverse scenario
    demo_swarm_diverse()
