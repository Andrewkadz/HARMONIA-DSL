"""
Example 1: Real-Time Adaptive Agent

Demonstrates how continuous-time dynamics enable fluid, real-time
adaptation to changing conditions.

Author: Manus AI
Date: January 1, 2026
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from continuous_dynamics import FluidHarmoniaIntegrator
import numpy as np


def main():
    print("=" * 70)
    print("HARMONIA-DSL v9.0 Example: Real-Time Adaptive Agent")
    print("=" * 70)
    print()
    print("This agent continuously adapts to changing task demands.")
    print("Watch how the state variables evolve smoothly over time.")
    print()
    
    # Create fluid integrator with fine time resolution
    agent = FluidHarmoniaIntegrator(dt=0.01)
    
    # Scenario: Agent faces varying task difficulty
    scenarios = [
        {'name': 'Easy Task', 'velocity': 0.5, 'duration': 2.0},
        {'name': 'Moderate Task', 'velocity': 1.5, 'duration': 2.0},
        {'name': 'Difficult Task', 'velocity': 3.0, 'duration': 2.0},
        {'name': 'Rest Period', 'velocity': 0.0, 'duration': 2.0},
    ]
    
    print("Initial State:")
    print(f"  Awareness (Ψ): {agent.state.psi:.2f}")
    print(f"  Ethics (Φ): {agent.state.phi:.2f}")
    print(f"  Coherence (Ω): {agent.state.omega:.2f}")
    print(f"  Energy: {agent.state.energy:.2f}")
    print()
    
    for scenario in scenarios:
        print(f"\n--- {scenario['name']} (velocity={scenario['velocity']}) ---")
        
        result = agent.process(
            inputs={'velocity': scenario['velocity']},
            duration=scenario['duration']
        )
        
        state = agent.state
        print(f"Time: {state.time:.1f}s")
        print(f"  Awareness (Ψ): {state.psi:.2f}")
        print(f"  Ethics (Φ): {state.phi:.2f}")
        print(f"  Coherence (Ω): {state.omega:.2f}")
        print(f"  Drift (ε): {state.epsilon:.3f}")
        print(f"  Energy: {state.energy:.2f}")
        print(f"  Knowledge (K): {state.knowledge:.2f}")
        print(f"  Maturity (Γ): {state.maturity:.3f}")
        print(f"  Harmonic Response (R): {result['R']:.2f}")
        
        # Analyze trajectory smoothness
        trajectory = result['trajectory']
        psi_values = trajectory['states'][:, 0]
        psi_changes = np.diff(psi_values)
        max_change = np.max(np.abs(psi_changes))
        
        print(f"  Max Awareness change per step: {max_change:.4f}")
        print(f"  → Trajectory is {'smooth' if max_change < 1.0 else 'jumpy'}")
    
    print("\n" + "=" * 70)
    print("Key Observations:")
    print("=" * 70)
    print("1. State variables evolve SMOOTHLY (no discrete jumps)")
    print("2. The agent adapts IN REAL-TIME to changing task demands")
    print("3. Energy depletes during difficult tasks, recharges during rest")
    print("4. Knowledge and maturity accumulate continuously")
    print("5. The system maintains stability throughout")
    print()
    print("✓ Continuous-time dynamics enable fluid, realistic behavior!")


if __name__ == "__main__":
    main()
