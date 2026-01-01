"""
HARMONIA-DSL v6.0 Example: Pattern Learning Agent

This example demonstrates how an agent learns to recognize and predict
patterns in its environment, using memory to improve prediction accuracy.

The agent:
1. Observes a cyclical pattern in the environment
2. Builds memory of past observations
3. Learns to predict future states
4. Improves prediction accuracy over time

Author: Manus AI
Date: January 1, 2026
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory_learning import State, MemoryLearningEngine
import math


class PatternLearningAgent:
    """An agent that learns to predict cyclical patterns."""
    
    def __init__(self):
        self.engine = MemoryLearningEngine(
            memory_depth=15,
            decay_rate=0.1,
            learning_rate=0.1,
            projection_steps=3
        )
        self.time = 0.0
        self.prediction_errors = []
    
    def generate_environment_state(self, t: float) -> State:
        """Generate a cyclical environmental pattern."""
        # Sinusoidal pattern with period of 10 steps
        psi = 5.0 + 3.0 * math.sin(2 * math.pi * t / 10.0)
        phi = 5.0 + 2.0 * math.cos(2 * math.pi * t / 10.0)
        epsilon = 0.2 + 0.1 * math.sin(2 * math.pi * t / 5.0)
        
        return State(psi=psi, phi=phi, epsilon=epsilon, timestamp=t)
    
    def predict_next_state(self) -> State:
        """Use memory and learning to predict the next state."""
        result = self.engine.process_state(
            self.generate_environment_state(self.time)
        )
        
        # Use first projection as prediction
        if result['psi_plus'] and len(result['psi_plus']) > 0:
            return result['psi_plus'][0]
        else:
            # Fallback: use current state
            return self.generate_environment_state(self.time)
    
    def evaluate_prediction(self, predicted: State, actual: State) -> float:
        """Calculate prediction error."""
        error = (predicted - actual).magnitude()
        return error
    
    def run_learning_cycle(self, steps: int = 30):
        """Run the pattern learning simulation."""
        print("=" * 70)
        print("HARMONIA-DSL v6.0: Pattern Learning Agent")
        print("=" * 70)
        print()
        print("The agent learns to predict cyclical environmental patterns.\n")
        
        for step in range(steps):
            # Predict next state
            predicted = self.predict_next_state()
            
            # Advance time and observe actual state
            self.time += 1.0
            actual = self.generate_environment_state(self.time)
            
            # Evaluate prediction
            error = self.evaluate_prediction(predicted, actual)
            self.prediction_errors.append(error)
            
            # Get knowledge level
            knowledge = self.engine.knowledge.get_knowledge()
            
            # Print periodic updates
            if step % 5 == 0:
                avg_recent_error = sum(self.prediction_errors[-5:]) / min(5, len(self.prediction_errors))
                print(f"Step {step:2d} | Knowledge K={knowledge:5.2f}")
                print(f"         Actual:    Ψ={actual.psi:5.2f}, Φ={actual.phi:5.2f}, ε={actual.epsilon:.3f}")
                print(f"         Predicted: Ψ={predicted.psi:5.2f}, Φ={predicted.phi:5.2f}, ε={predicted.epsilon:.3f}")
                print(f"         Error: {error:.3f} | Avg Recent Error: {avg_recent_error:.3f}")
                print()
        
        # Analysis
        print("=" * 70)
        print("LEARNING ANALYSIS")
        print("=" * 70)
        
        early_errors = self.prediction_errors[:10]
        late_errors = self.prediction_errors[-10:]
        
        avg_early = sum(early_errors) / len(early_errors)
        avg_late = sum(late_errors) / len(late_errors)
        improvement = (avg_early - avg_late) / avg_early * 100
        
        print(f"Early Prediction Error (steps 0-9):   {avg_early:.3f}")
        print(f"Late Prediction Error (steps 20-29):  {avg_late:.3f}")
        print(f"Improvement: {improvement:.1f}%")
        print(f"Final Knowledge: {self.engine.knowledge.get_knowledge():.2f}")
        print()
        
        if improvement > 20:
            print("✓ SUCCESS: Agent learned the pattern!")
        elif improvement > 0:
            print("⚡ PARTIAL: Agent showed some learning.")
        else:
            print("⚠ WARNING: Agent did not improve predictions.")
        print()


class SkillAcquisitionAgent:
    """An agent that develops skills over time through practice."""
    
    def __init__(self):
        self.engine = MemoryLearningEngine(
            memory_depth=20,
            decay_rate=0.08,
            learning_rate=0.15,
            projection_steps=5
        )
        self.skill_level = 0.0
        self.time = 0.0
    
    def practice_task(self, difficulty: float) -> float:
        """Practice a task and improve based on experience."""
        # Current capability
        capability = self.skill_level + self.engine.knowledge.get_knowledge() * 0.5
        
        # Success depends on capability vs difficulty
        success_rate = min(1.0, capability / difficulty)
        
        # Create state representing practice session
        state = State(
            psi=capability,
            phi=success_rate * 10.0,
            epsilon=max(0.1, 1.0 - success_rate),
            timestamp=self.time
        )
        
        # Process through learning engine
        result = self.engine.process_state(state)
        
        # Skill improves with practice
        self.skill_level += 0.1 * success_rate
        self.time += 1.0
        
        return success_rate
    
    def run_training(self, sessions: int = 40):
        """Run skill acquisition training."""
        print("=" * 70)
        print("HARMONIA-DSL v6.0: Skill Acquisition Through Learning")
        print("=" * 70)
        print()
        print("The agent develops skills through repeated practice.\n")
        
        task_difficulty = 8.0
        
        for session in range(sessions):
            success_rate = self.practice_task(task_difficulty)
            knowledge = self.engine.knowledge.get_knowledge()
            total_capability = self.skill_level + knowledge * 0.5
            
            if session % 8 == 0:
                print(f"Session {session:2d} | Skill={self.skill_level:5.2f}, Knowledge K={knowledge:5.2f}")
                print(f"           Total Capability={total_capability:5.2f}, Success Rate={success_rate*100:5.1f}%")
                print()
        
        # Final assessment
        print("=" * 70)
        print("TRAINING COMPLETE")
        print("=" * 70)
        print(f"Initial Capability: 0.00")
        print(f"Final Skill Level: {self.skill_level:.2f}")
        print(f"Final Knowledge: {self.engine.knowledge.get_knowledge():.2f}")
        print(f"Total Capability: {self.skill_level + self.engine.knowledge.get_knowledge() * 0.5:.2f}")
        print()
        
        final_success = self.practice_task(task_difficulty)
        if final_success > 0.8:
            print(f"✓ MASTERY: Agent achieved {final_success*100:.1f}% success rate!")
        elif final_success > 0.5:
            print(f"⚡ COMPETENT: Agent achieved {final_success*100:.1f}% success rate.")
        else:
            print(f"⚠ NOVICE: Agent at {final_success*100:.1f}% success rate.")
        print()


if __name__ == "__main__":
    # Example 1: Pattern Learning
    pattern_agent = PatternLearningAgent()
    pattern_agent.run_learning_cycle(steps=30)
    
    print("\n" + "=" * 70 + "\n")
    
    # Example 2: Skill Acquisition
    skill_agent = SkillAcquisitionAgent()
    skill_agent.run_training(sessions=40)
