"""
HARMONIA-DSL v6.0 Example: Adaptive Safety Agent

This example demonstrates how an agent learns from experience to avoid
dangerous states (high epsilon) and gravitates toward safe, harmonious states.

The agent:
1. Explores different states
2. Learns which states lead to danger (high ε)
3. Uses memory to avoid repeating mistakes
4. Projects future states to prevent danger proactively

Author: Manus AI
Date: January 1, 2026
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory_learning import State, MemoryLearningEngine
import random
import math


class AdaptiveSafetyAgent:
    """An agent that learns to maintain safety through experience."""
    
    def __init__(self):
        self.engine = MemoryLearningEngine(
            memory_depth=10,
            decay_rate=0.15,
            learning_rate=0.08,
            projection_steps=5
        )
        self.current_state = State(psi=5.0, phi=5.0, epsilon=0.3, timestamp=0.0)
        self.time = 0.0
        self.danger_threshold = 0.6  # ε above this is dangerous
    
    def evaluate_safety(self, state: State) -> float:
        """Evaluate how safe a state is (0=safe, 1=dangerous)."""
        return min(state.epsilon / self.danger_threshold, 1.0)
    
    def choose_action(self) -> str:
        """Choose an action based on current knowledge and projections."""
        # Process current state
        result = self.engine.process_state(self.current_state)
        
        # Check future projections
        if result['psi_plus']:
            future_dangers = [self.evaluate_safety(s) for s in result['psi_plus']]
            avg_future_danger = sum(future_dangers) / len(future_dangers)
        else:
            avg_future_danger = 0.0
        
        current_danger = self.evaluate_safety(self.current_state)
        
        # Decision logic
        if current_danger > 0.7:
            return "EMERGENCY_STABILIZE"
        elif avg_future_danger > 0.5:
            return "PREEMPTIVE_ADJUST"
        elif self.current_state.epsilon < 0.2:
            return "EXPLORE"  # Safe to explore
        else:
            return "MAINTAIN"
    
    def execute_action(self, action: str):
        """Execute the chosen action and update state."""
        if action == "EMERGENCY_STABILIZE":
            # Rapid stabilization
            self.current_state.psi += 2.0
            self.current_state.phi += 2.0
            self.current_state.epsilon = max(0.1, self.current_state.epsilon - 0.3)
        
        elif action == "PREEMPTIVE_ADJUST":
            # Gentle correction before danger
            self.current_state.psi += 1.0
            self.current_state.phi += 1.0
            self.current_state.epsilon = max(0.1, self.current_state.epsilon - 0.1)
        
        elif action == "EXPLORE":
            # Try new things (might increase epsilon)
            self.current_state.psi += random.uniform(-0.5, 1.5)
            self.current_state.phi += random.uniform(-0.5, 1.5)
            self.current_state.epsilon += random.uniform(-0.05, 0.15)
        
        else:  # MAINTAIN
            # Small random drift
            self.current_state.psi += random.uniform(-0.3, 0.3)
            self.current_state.phi += random.uniform(-0.3, 0.3)
            self.current_state.epsilon += random.uniform(-0.05, 0.05)
        
        # Ensure bounds
        self.current_state.psi = max(0.0, self.current_state.psi)
        self.current_state.phi = max(0.0, self.current_state.phi)
        self.current_state.epsilon = max(0.0, min(1.0, self.current_state.epsilon))
        
        # Update time
        self.time += 1.0
        self.current_state.timestamp = self.time
    
    def get_output(self) -> float:
        """Calculate stabilized output Σ = (Ψ + Φ) * (1 - ε)."""
        return (self.current_state.psi + self.current_state.phi) * (1 - self.current_state.epsilon)
    
    def run_simulation(self, steps: int = 50):
        """Run the adaptive safety simulation."""
        print("=" * 70)
        print("HARMONIA-DSL v6.0: Adaptive Safety Agent")
        print("=" * 70)
        print()
        print("The agent learns to avoid danger and maintain harmony.\n")
        
        danger_count = 0
        safe_count = 0
        
        for step in range(steps):
            # Choose and execute action
            action = self.choose_action()
            self.execute_action(action)
            
            # Evaluate
            danger = self.evaluate_safety(self.current_state)
            output = self.get_output()
            knowledge = self.engine.knowledge.get_knowledge()
            
            if danger > 0.7:
                danger_count += 1
                status = "⚠️  DANGER"
            elif danger > 0.4:
                status = "⚡ CAUTION"
            else:
                safe_count += 1
                status = "✓ SAFE"
            
            # Print periodic updates
            if step % 10 == 0 or danger > 0.7:
                print(f"Step {step:2d} | {status} | Action: {action:20s}")
                print(f"         State: Ψ={self.current_state.psi:5.2f}, Φ={self.current_state.phi:5.2f}, ε={self.current_state.epsilon:.3f}")
                print(f"         Knowledge K={knowledge:.2f}, Output Σ={output:.2f}")
                print()
        
        # Summary
        print("=" * 70)
        print("SIMULATION COMPLETE")
        print("=" * 70)
        print(f"Total Steps: {steps}")
        print(f"Safe States: {safe_count} ({safe_count/steps*100:.1f}%)")
        print(f"Dangerous States: {danger_count} ({danger_count/steps*100:.1f}%)")
        print(f"Final Knowledge: {self.engine.knowledge.get_knowledge():.2f}")
        print(f"Final Output: {self.get_output():.2f}")
        print()
        
        if danger_count < steps * 0.2:
            print("✓ SUCCESS: Agent learned to maintain safety!")
        else:
            print("⚠ WARNING: Agent struggled with safety.")
        print()


if __name__ == "__main__":
    random.seed(42)  # Reproducible results
    agent = AdaptiveSafetyAgent()
    agent.run_simulation(steps=50)
