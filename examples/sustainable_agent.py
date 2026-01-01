"""
HARMONIA-DSL v7.0 Example: Sustainable Agent

This example demonstrates an agent that learns to operate efficiently
within energy constraints. The agent must complete tasks while managing
a finite energy budget, learning which actions are most efficient.

Key Concepts:
- Energy as a limiting resource
- Efficiency optimization over time
- Sustainable operation strategies

Author: Manus AI
Date: January 1, 2026
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from energy_thermodynamics import EnergyConstrainedEngine
import random


class SustainableAgent:
    """An agent that learns to operate sustainably within energy limits."""
    
    def __init__(self, capacity: float = 100.0, recharge_rate: float = 3.0):
        self.engine = EnergyConstrainedEngine(
            capacity=capacity,
            recharge_rate=recharge_rate
        )
        self.tasks_completed = 0
        self.tasks_failed = 0
        self.time = 0.0
        
    def evaluate_task(self, task_difficulty: float) -> dict:
        """
        Evaluate and attempt a task.
        
        Args:
            task_difficulty: How difficult the task is (affects energy cost)
            
        Returns:
            Dictionary with task result
        """
        # Calculate required parameters
        action_magnitude = task_difficulty
        drift = max(0.1, 1.0 - self.engine.energy_pool.get_state().get_level())
        
        # Base output calculation
        psi = 10.0
        phi = 8.0
        sigma_base = (psi + phi) * (1 - drift)
        
        # Process the action
        result = self.engine.process_action(
            action_magnitude=action_magnitude,
            drift=drift,
            sigma_base=sigma_base,
            psi=psi
        )
        
        # Determine success based on output
        success = result['output'] > task_difficulty * 2.0
        
        if success:
            self.tasks_completed += 1
        else:
            self.tasks_failed += 1
        
        self.time += 1.0
        
        return {
            'success': success,
            'output': result['output'],
            'energy_used': result['energy_cost'],
            'energy_remaining': result['energy_remaining'],
            'efficiency': result['efficiency']
        }
    
    def choose_task(self, available_tasks: list) -> float:
        """
        Choose a task based on current energy level.
        
        Strategy: Choose easier tasks when energy is low.
        """
        energy_level = self.engine.energy_pool.get_state().get_level()
        
        if energy_level > 0.7:
            # High energy: can tackle difficult tasks
            return max(available_tasks)
        elif energy_level > 0.3:
            # Medium energy: moderate tasks
            return sorted(available_tasks)[len(available_tasks)//2]
        else:
            # Low energy: easy tasks only
            return min(available_tasks)
    
    def run_simulation(self, steps: int = 50):
        """Run the sustainable agent simulation."""
        print("=" * 70)
        print("HARMONIA-DSL v7.0: Sustainable Agent")
        print("=" * 70)
        print()
        print("The agent learns to operate efficiently within energy constraints.\n")
        
        available_tasks = [2.0, 4.0, 6.0, 8.0, 10.0]
        
        for step in range(steps):
            # Choose task based on energy level
            task_difficulty = self.choose_task(available_tasks)
            
            # Attempt task
            result = self.evaluate_task(task_difficulty)
            
            # Print periodic updates
            if step % 10 == 0:
                energy_state = self.engine.get_energy_state()
                safety = self.engine.check_safety()
                
                print(f"Step {step}:")
                print(f"  Task Difficulty: {task_difficulty:.1f}")
                print(f"  Success: {'✓' if result['success'] else '✗'}")
                print(f"  Energy: {result['energy_remaining']:.1f}/{self.engine.energy_pool.capacity:.1f} ({energy_state.get_level()*100:.0f}%)")
                print(f"  Efficiency η: {result['efficiency']:.3f}")
                print(f"  Entropy S: {energy_state.entropy:.3f}")
                
                if safety['safe']:
                    print(f"  Status: ✓ Safe")
                elif safety['energy_critical']:
                    print(f"  Status: ⚠️  Energy Critical")
                else:
                    print(f"  Status: ⚡ Caution")
                print()
        
        # Summary
        print("=" * 70)
        print("SIMULATION COMPLETE")
        print("=" * 70)
        print(f"Total Steps: {steps}")
        print(f"Tasks Completed: {self.tasks_completed}")
        print(f"Tasks Failed: {self.tasks_failed}")
        print(f"Success Rate: {self.tasks_completed/(self.tasks_completed+self.tasks_failed)*100:.1f}%")
        print(f"Final Energy: {self.engine.energy_pool.current_energy:.1f}/{self.engine.energy_pool.capacity:.1f}")
        print(f"Overall Efficiency: {self.engine.efficiency_tracker.get_efficiency():.3f}")
        print()
        
        if self.tasks_completed > self.tasks_failed * 2:
            print("✓ SUCCESS: Agent operated sustainably!")
        else:
            print("⚠ WARNING: Agent struggled with energy management.")
        print()


class AdaptiveEfficiencyAgent:
    """Agent that actively learns to improve efficiency."""
    
    def __init__(self):
        self.engine = EnergyConstrainedEngine(capacity=100.0, recharge_rate=2.0)
        self.strategy_performance = {
            'aggressive': [],
            'moderate': [],
            'conservative': []
        }
        
    def execute_strategy(self, strategy: str) -> float:
        """Execute a strategy and return efficiency."""
        if strategy == 'aggressive':
            action_mag = 10.0
            drift = 0.4
        elif strategy == 'moderate':
            action_mag = 5.0
            drift = 0.2
        else:  # conservative
            action_mag = 2.0
            drift = 0.1
        
        result = self.engine.process_action(
            action_magnitude=action_mag,
            drift=drift,
            sigma_base=20.0,
            psi=10.0
        )
        
        return result['efficiency']
    
    def run_learning_simulation(self, trials: int = 30):
        """Run adaptive learning simulation."""
        print("=" * 70)
        print("HARMONIA-DSL v7.0: Adaptive Efficiency Learning")
        print("=" * 70)
        print()
        print("Agent learns which strategy is most efficient.\n")
        
        strategies = ['aggressive', 'moderate', 'conservative']
        
        for trial in range(trials):
            # Try each strategy
            strategy = strategies[trial % 3]
            efficiency = self.execute_strategy(strategy)
            self.strategy_performance[strategy].append(efficiency)
            
            if trial % 10 == 0 and trial > 0:
                # Analyze performance
                avg_perf = {
                    s: sum(self.strategy_performance[s]) / len(self.strategy_performance[s])
                    for s in strategies if self.strategy_performance[s]
                }
                
                best_strategy = max(avg_perf, key=avg_perf.get)
                
                print(f"Trial {trial}:")
                print(f"  Aggressive: η = {avg_perf.get('aggressive', 0):.3f}")
                print(f"  Moderate: η = {avg_perf.get('moderate', 0):.3f}")
                print(f"  Conservative: η = {avg_perf.get('conservative', 0):.3f}")
                print(f"  Best Strategy: {best_strategy.upper()}")
                print()
        
        # Final analysis
        print("=" * 70)
        print("LEARNING COMPLETE")
        print("=" * 70)
        
        final_avg = {
            s: sum(self.strategy_performance[s]) / len(self.strategy_performance[s])
            for s in strategies
        }
        
        best = max(final_avg, key=final_avg.get)
        worst = min(final_avg, key=final_avg.get)
        
        print(f"Best Strategy: {best.upper()} (η = {final_avg[best]:.3f})")
        print(f"Worst Strategy: {worst.upper()} (η = {final_avg[worst]:.3f})")
        print(f"Improvement: {(final_avg[best] - final_avg[worst]) / final_avg[worst] * 100:.1f}%")
        print()
        print("✓ Agent successfully learned optimal efficiency strategy!")
        print()


if __name__ == "__main__":
    random.seed(42)
    
    # Example 1: Sustainable Agent
    agent = SustainableAgent(capacity=100.0, recharge_rate=3.0)
    agent.run_simulation(steps=50)
    
    print("\n" + "=" * 70 + "\n")
    
    # Example 2: Adaptive Efficiency Learning
    adaptive_agent = AdaptiveEfficiencyAgent()
    adaptive_agent.run_learning_simulation(trials=30)
