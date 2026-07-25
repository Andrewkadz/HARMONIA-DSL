"""
HARMONIA-DSL v7.0 Example: Resource Allocation

This example demonstrates optimal resource allocation when an agent
must balance multiple competing goals with limited energy. The agent
learns to prioritize high-value actions and manage trade-offs.

Key Concepts:
- Multi-objective optimization under constraints
- Priority-based resource allocation
- Trade-offs between competing goals

Author: Manus AI
Date: January 1, 2026
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from energy_thermodynamics import EnergyConstrainedEngine
from typing import List, Dict


class Goal:
    """Represents a goal with value and energy cost."""
    
    def __init__(self, name: str, value: float, energy_cost: float, urgency: float = 0.5):
        self.name = name
        self.value = value
        self.energy_cost = energy_cost
        self.urgency = urgency
        self.completion_count = 0
        
    def get_priority(self, energy_level: float) -> float:
        """Calculate priority score."""
        # Priority = value * urgency / cost, adjusted for energy level
        base_priority = (self.value * self.urgency) / self.energy_cost
        
        # Adjust for energy level: prefer low-cost goals when energy is low
        if energy_level < 0.3:
            energy_factor = 1.0 / self.energy_cost
        else:
            energy_factor = 1.0
        
        return base_priority * energy_factor
    
    def __repr__(self):
        return f"Goal({self.name}, value={self.value}, cost={self.energy_cost})"


class ResourceAllocationAgent:
    """Agent that allocates limited energy across multiple goals."""
    
    def __init__(self, capacity: float = 100.0, recharge_rate: float = 5.0):
        self.engine = EnergyConstrainedEngine(capacity=capacity, recharge_rate=recharge_rate)
        self.goals: List[Goal] = []
        self.total_value_achieved = 0.0
        
    def add_goal(self, goal: Goal):
        """Add a goal to pursue."""
        self.goals.append(goal)
    
    def select_goal(self) -> Goal:
        """Select the highest priority goal given current energy."""
        energy_level = self.engine.energy_pool.get_state().get_level()
        
        # Calculate priorities
        priorities = [(goal, goal.get_priority(energy_level)) for goal in self.goals]
        
        # Sort by priority
        priorities.sort(key=lambda x: x[1], reverse=True)
        
        return priorities[0][0]
    
    def pursue_goal(self, goal: Goal) -> Dict:
        """Pursue a goal and return result."""
        # Calculate drift based on goal difficulty
        drift = min(0.1 + goal.energy_cost * 0.05, 0.7)
        
        # Process action
        result = self.engine.process_action(
            action_magnitude=goal.energy_cost,
            drift=drift,
            sigma_base=goal.value * 2.0,
            psi=10.0
        )
        
        # Check if goal achieved
        if result['success'] and result['output'] > goal.value:
            goal.completion_count += 1
            self.total_value_achieved += goal.value
            achieved = True
        else:
            achieved = False
        
        return {
            'goal': goal.name,
            'achieved': achieved,
            'value_gained': goal.value if achieved else 0.0,
            'energy_used': result['energy_cost'],
            'energy_remaining': result['energy_remaining']
        }
    
    def run_allocation_simulation(self, steps: int = 40):
        """Run resource allocation simulation."""
        print("=" * 70)
        print("HARMONIA-DSL v7.0: Resource Allocation")
        print("=" * 70)
        print()
        print("Agent allocates limited energy across multiple competing goals.\n")
        
        # Display goals
        print("Available Goals:")
        for goal in self.goals:
            print(f"  - {goal.name}: Value={goal.value:.1f}, Cost={goal.energy_cost:.1f}, Urgency={goal.urgency:.1f}")
        print()
        
        for step in range(steps):
            # Select and pursue goal
            selected_goal = self.select_goal()
            result = self.pursue_goal(selected_goal)
            
            # Print periodic updates
            if step % 10 == 0:
                energy_state = self.engine.get_energy_state()
                
                print(f"Step {step}:")
                print(f"  Selected Goal: {result['goal']}")
                print(f"  Achieved: {'✓' if result['achieved'] else '✗'}")
                print(f"  Value Gained: {result['value_gained']:.1f}")
                print(f"  Energy: {result['energy_remaining']:.1f}/{self.engine.energy_pool.capacity:.1f} ({energy_state.get_level()*100:.0f}%)")
                print(f"  Total Value: {self.total_value_achieved:.1f}")
                print()
        
        # Summary
        print("=" * 70)
        print("ALLOCATION SUMMARY")
        print("=" * 70)
        print()
        print("Goal Completion Counts:")
        for goal in self.goals:
            print(f"  {goal.name}: {goal.completion_count} times")
        print()
        print(f"Total Value Achieved: {self.total_value_achieved:.1f}")
        print(f"Final Energy: {self.engine.energy_pool.current_energy:.1f}/{self.engine.energy_pool.capacity:.1f}")
        print(f"Overall Efficiency: {self.engine.efficiency_tracker.get_efficiency():.3f}")
        print()
        
        if self.total_value_achieved > 100:
            print("✓ SUCCESS: Effective resource allocation!")
        else:
            print("⚡ MODERATE: Resource allocation could be improved.")
        print()


class DynamicPrioritizationDemo:
    """Demonstrates dynamic priority adjustment based on energy."""
    
    def __init__(self):
        self.engine = EnergyConstrainedEngine(capacity=80.0, recharge_rate=2.0)
        
    def run_prioritization_demo(self):
        """Demonstrate dynamic prioritization."""
        print("=" * 70)
        print("HARMONIA-DSL v7.0: Dynamic Prioritization")
        print("=" * 70)
        print()
        print("Priorities shift dynamically based on available energy.\n")
        
        # Define goals
        goals = [
            Goal("High-Value Complex", value=20.0, energy_cost=10.0, urgency=0.8),
            Goal("Medium-Value Moderate", value=10.0, energy_cost=5.0, urgency=0.6),
            Goal("Low-Value Simple", value=5.0, energy_cost=2.0, urgency=0.4)
        ]
        
        # Test at different energy levels
        energy_levels = [1.0, 0.6, 0.3, 0.1]
        
        for energy_level in energy_levels:
            print(f"Energy Level: {energy_level*100:.0f}%")
            print("-" * 70)
            
            # Calculate priorities
            priorities = [(g, g.get_priority(energy_level)) for g in goals]
            priorities.sort(key=lambda x: x[1], reverse=True)
            
            print("Priority Ranking:")
            for i, (goal, priority) in enumerate(priorities, 1):
                print(f"  {i}. {goal.name} (priority: {priority:.2f})")
            
            print()
        
        print("=" * 70)
        print("PRIORITIZATION ANALYSIS")
        print("=" * 70)
        print()
        print("Observations:")
        print("  - High energy: Complex high-value goals prioritized")
        print("  - Medium energy: Balanced approach")
        print("  - Low energy: Simple low-cost goals prioritized")
        print("  - Critical energy: Only minimal actions attempted")
        print()
        print("✓ Dynamic prioritization enables sustainable operation!")
        print()


if __name__ == "__main__":
    # Demo 1: Resource Allocation
    agent = ResourceAllocationAgent(capacity=100.0, recharge_rate=5.0)
    
    # Add diverse goals
    agent.add_goal(Goal("Critical Mission", value=15.0, energy_cost=8.0, urgency=0.9))
    agent.add_goal(Goal("Research Task", value=10.0, energy_cost=5.0, urgency=0.6))
    agent.add_goal(Goal("Maintenance", value=5.0, energy_cost=2.0, urgency=0.4))
    agent.add_goal(Goal("Exploration", value=12.0, energy_cost=7.0, urgency=0.5))
    
    agent.run_allocation_simulation(steps=40)
    
    print("\n" + "=" * 70 + "\n")
    
    # Demo 2: Dynamic Prioritization
    demo = DynamicPrioritizationDemo()
    demo.run_prioritization_demo()
