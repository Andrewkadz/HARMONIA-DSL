"""
HARMONIA-DSL v6.0 Example: Predictive Control Agent

This example demonstrates how an agent uses memory and future projection
to take preemptive action, preventing problems before they occur.

The agent:
1. Monitors system state continuously
2. Projects future states using Ψ+
3. Detects potential future problems
4. Takes preemptive corrective action
5. Learns optimal intervention timing

Author: Manus AI
Date: January 1, 2026
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory_learning import State, MemoryLearningEngine
import random


class PredictiveControlAgent:
    """An agent that uses future projection for proactive control."""
    
    def __init__(self):
        self.engine = MemoryLearningEngine(
            memory_depth=8,
            decay_rate=0.12,
            learning_rate=0.1,
            projection_steps=5
        )
        self.state = State(psi=10.0, phi=10.0, epsilon=0.15, timestamp=0.0)
        self.time = 0.0
        self.interventions = 0
        self.crises_prevented = 0
        self.crises_occurred = 0
    
    def simulate_drift(self):
        """Simulate natural system drift (tends toward instability)."""
        # System naturally drifts toward higher epsilon
        self.state.epsilon += random.uniform(0.02, 0.08)
        self.state.psi += random.uniform(-0.5, 0.3)
        self.state.phi += random.uniform(-0.5, 0.3)
        
        # Bounds
        self.state.epsilon = min(1.0, self.state.epsilon)
        self.state.psi = max(0.0, self.state.psi)
        self.state.phi = max(0.0, self.state.phi)
    
    def detect_future_crisis(self) -> tuple[bool, int]:
        """
        Use Ψ+ to detect if a crisis will occur in the future.
        
        Returns:
            (crisis_detected, steps_until_crisis)
        """
        result = self.engine.process_state(self.state)
        
        if not result['psi_plus']:
            return False, 0
        
        # Check each projected future state
        for i, future_state in enumerate(result['psi_plus']):
            if future_state.epsilon > 0.7:  # Crisis threshold
                return True, i + 1
        
        return False, 0
    
    def intervene(self, urgency: str):
        """Take corrective action to prevent crisis."""
        self.interventions += 1
        
        if urgency == "HIGH":
            # Strong intervention
            self.state.psi += 3.0
            self.state.phi += 3.0
            self.state.epsilon = max(0.1, self.state.epsilon - 0.4)
        else:
            # Gentle intervention
            self.state.psi += 1.5
            self.state.phi += 1.5
            self.state.epsilon = max(0.1, self.state.epsilon - 0.2)
    
    def run_simulation(self, steps: int = 50):
        """Run predictive control simulation."""
        print("=" * 70)
        print("HARMONIA-DSL v6.0: Predictive Control Agent")
        print("=" * 70)
        print()
        print("The agent uses future projection to prevent crises preemptively.\n")
        
        for step in range(steps):
            # Simulate natural drift
            self.simulate_drift()
            
            # Update time
            self.time += 1.0
            self.state.timestamp = self.time
            
            # Check for current crisis
            if self.state.epsilon > 0.7:
                self.crises_occurred += 1
                status = "🚨 CRISIS"
            else:
                status = "✓ STABLE"
            
            # Detect future crisis
            crisis_ahead, steps_until = self.detect_future_crisis()
            
            # Decide on action
            action = "MONITOR"
            if self.state.epsilon > 0.6:
                action = "INTERVENE_HIGH"
                self.intervene("HIGH")
            elif crisis_ahead and steps_until <= 2:
                action = "INTERVENE_PREEMPTIVE"
                self.intervene("GENTLE")
                self.crises_prevented += 1
            elif self.state.epsilon > 0.4:
                action = "INTERVENE_GENTLE"
                self.intervene("GENTLE")
            
            knowledge = self.engine.knowledge.get_knowledge()
            output = (self.state.psi + self.state.phi) * (1 - self.state.epsilon)
            
            # Print updates
            if step % 10 == 0 or self.state.epsilon > 0.6:
                print(f"Step {step:2d} | {status} | Action: {action}")
                print(f"         State: Ψ={self.state.psi:5.2f}, Φ={self.state.phi:5.2f}, ε={self.state.epsilon:.3f}")
                print(f"         Knowledge K={knowledge:.2f}, Output Σ={output:.2f}")
                if crisis_ahead:
                    print(f"         ⚠️  Crisis projected in {steps_until} steps!")
                print()
        
        # Summary
        print("=" * 70)
        print("SIMULATION COMPLETE")
        print("=" * 70)
        print(f"Total Steps: {steps}")
        print(f"Interventions: {self.interventions}")
        print(f"Crises Prevented: {self.crises_prevented}")
        print(f"Crises Occurred: {self.crises_occurred}")
        print(f"Final Knowledge: {self.engine.knowledge.get_knowledge():.2f}")
        print(f"Final Output: {(self.state.psi + self.state.phi) * (1 - self.state.epsilon):.2f}")
        print()
        
        if self.crises_occurred == 0:
            print("✓ PERFECT: No crises occurred!")
        elif self.crises_occurred < 3:
            print("⚡ GOOD: Minimal crises occurred.")
        else:
            print("⚠ WARNING: Multiple crises occurred.")
        
        if self.crises_prevented > 5:
            print(f"✓ PROACTIVE: Agent prevented {self.crises_prevented} crises preemptively!")
        print()


class MemoryGuidedOptimization:
    """Uses memory to find optimal strategies over time."""
    
    def __init__(self):
        self.engine = MemoryLearningEngine(
            memory_depth=15,
            decay_rate=0.1,
            learning_rate=0.12,
            projection_steps=3
        )
        self.best_output = 0.0
        self.best_strategy = None
    
    def try_strategy(self, strategy: dict) -> float:
        """Try a strategy and return its output."""
        state = State(
            psi=strategy['psi'],
            phi=strategy['phi'],
            epsilon=strategy['epsilon'],
            timestamp=strategy['time']
        )
        
        result = self.engine.process_state(state)
        
        # Calculate output with memory-learning enhancement
        base_output = (state.psi + state.phi) * (1 - state.epsilon)
        enhanced_output = self.engine.apply_to_system(base_output, influence=0.15)
        
        return enhanced_output
    
    def run_optimization(self, trials: int = 30):
        """Run optimization using memory-guided search."""
        print("=" * 70)
        print("HARMONIA-DSL v6.0: Memory-Guided Optimization")
        print("=" * 70)
        print()
        print("The agent uses memory to find optimal strategies.\n")
        
        for trial in range(trials):
            # Generate strategy (with some randomness)
            if trial < 10:
                # Initial exploration
                strategy = {
                    'psi': random.uniform(3.0, 10.0),
                    'phi': random.uniform(3.0, 10.0),
                    'epsilon': random.uniform(0.1, 0.5),
                    'time': float(trial)
                }
            else:
                # Exploit memory: try variations of good strategies
                if self.best_strategy:
                    strategy = {
                        'psi': self.best_strategy['psi'] + random.uniform(-1.0, 1.0),
                        'phi': self.best_strategy['phi'] + random.uniform(-1.0, 1.0),
                        'epsilon': max(0.1, self.best_strategy['epsilon'] + random.uniform(-0.1, 0.1)),
                        'time': float(trial)
                    }
                else:
                    strategy = {
                        'psi': random.uniform(5.0, 12.0),
                        'phi': random.uniform(5.0, 12.0),
                        'epsilon': random.uniform(0.1, 0.3),
                        'time': float(trial)
                    }
            
            # Try strategy
            output = self.try_strategy(strategy)
            
            # Update best
            if output > self.best_output:
                self.best_output = output
                self.best_strategy = strategy
            
            knowledge = self.engine.knowledge.get_knowledge()
            
            if trial % 5 == 0:
                print(f"Trial {trial:2d} | Output={output:6.2f}, Best={self.best_output:6.2f}, K={knowledge:.2f}")
        
        print()
        print("=" * 70)
        print("OPTIMIZATION COMPLETE")
        print("=" * 70)
        print(f"Best Output Found: {self.best_output:.2f}")
        print(f"Optimal Strategy:")
        print(f"  Ψ = {self.best_strategy['psi']:.2f}")
        print(f"  Φ = {self.best_strategy['phi']:.2f}")
        print(f"  ε = {self.best_strategy['epsilon']:.3f}")
        print(f"Final Knowledge: {self.engine.knowledge.get_knowledge():.2f}")
        print()
        print("✓ Memory-guided optimization complete!")
        print()


if __name__ == "__main__":
    random.seed(42)
    
    # Example 1: Predictive Control
    control_agent = PredictiveControlAgent()
    control_agent.run_simulation(steps=50)
    
    print("\n" + "=" * 70 + "\n")
    
    # Example 2: Memory-Guided Optimization
    optimizer = MemoryGuidedOptimization()
    optimizer.run_optimization(trials=30)
