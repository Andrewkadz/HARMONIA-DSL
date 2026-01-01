"""
Example 2: Action-Ethics Trade-off

Demonstrates how the accumulation-intention coupling creates a realistic
trade-off between action and ethical consideration.

Author: Manus AI
Date: January 1, 2026
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from cross_layer_coupling import CoupledFluidHarmoniaIntegrator


def main():
    print("=" * 70)
    print("HARMONIA-DSL v10.0 Example: Action-Ethics Trade-off")
    print("=" * 70)
    print()
    print("This demonstrates the realistic 'thinking vs. doing' dynamics.")
    print("High-velocity action suppresses ethical consideration.")
    print()
    
    # Scenario 1: Reflective mode (low velocity, high ethical consideration)
    print("=" * 70)
    print("Scenario 1: Reflective Mode (Low Velocity)")
    print("=" * 70)
    
    agent_reflective = CoupledFluidHarmoniaIntegrator(dt=0.01)
    
    print(f"\nInitial State:")
    print(f"  Velocity: 0.2 (LOW - reflective)")
    print(f"  Intention: 0.3 (LOW - contemplative)")
    print(f"  Ethics (Φ): {agent_reflective.state.phi:.2f}")
    
    result_reflective = agent_reflective.process(
        inputs={'velocity': 0.2, 'intention': 0.3},
        duration=5.0
    )
    
    print(f"\nAfter 5 seconds:")
    print(f"  Ethics (Φ): {agent_reflective.state.phi:.2f}")
    print(f"  Accumulated ΔΦ: {agent_reflective.state.delta_phi_accum:.3f}")
    print(f"  Harmonic Response (R): {result_reflective['R']:.2f}")
    print(f"  Mode: ETHICAL ACCUMULATION (thinking deeply)")
    
    # Scenario 2: Action mode (high velocity, suppressed ethical consideration)
    print("\n" + "=" * 70)
    print("Scenario 2: Action Mode (High Velocity)")
    print("=" * 70)
    
    agent_action = CoupledFluidHarmoniaIntegrator(dt=0.01)
    
    print(f"\nInitial State:")
    print(f"  Velocity: 3.0 (HIGH - active)")
    print(f"  Intention: 0.9 (HIGH - purposeful)")
    print(f"  Ethics (Φ): {agent_action.state.phi:.2f}")
    
    result_action = agent_action.process(
        inputs={'velocity': 3.0, 'intention': 0.9},
        duration=5.0
    )
    
    print(f"\nAfter 5 seconds:")
    print(f"  Ethics (Φ): {agent_action.state.phi:.2f}")
    print(f"  Accumulated ΔΦ: {agent_action.state.delta_phi_accum:.3f}")
    print(f"  Harmonic Response (R): {result_action['R']:.2f}")
    print(f"  Mode: ACTION EXECUTION (doing, not overthinking)")
    
    # Scenario 3: Balanced mode
    print("\n" + "=" * 70)
    print("Scenario 3: Balanced Mode (Moderate Velocity)")
    print("=" * 70)
    
    agent_balanced = CoupledFluidHarmoniaIntegrator(dt=0.01)
    
    print(f"\nInitial State:")
    print(f"  Velocity: 1.0 (MODERATE)")
    print(f"  Intention: 0.5 (MODERATE)")
    print(f"  Ethics (Φ): {agent_balanced.state.phi:.2f}")
    
    result_balanced = agent_balanced.process(
        inputs={'velocity': 1.0, 'intention': 0.5},
        duration=5.0
    )
    
    print(f"\nAfter 5 seconds:")
    print(f"  Ethics (Φ): {agent_balanced.state.phi:.2f}")
    print(f"  Accumulated ΔΦ: {agent_balanced.state.delta_phi_accum:.3f}")
    print(f"  Harmonic Response (R): {result_balanced['R']:.2f}")
    print(f"  Mode: BALANCED (thinking and doing)")
    
    # Comparison
    print("\n" + "=" * 70)
    print("Comparison: Accumulation-Intention Coupling Effect")
    print("=" * 70)
    
    print(f"\nReflective Mode (Low Activity):")
    print(f"  Ethical Accumulation: {agent_reflective.state.delta_phi_accum:.3f}")
    print(f"  Behavior: Deep ethical consideration")
    
    print(f"\nAction Mode (High Activity):")
    print(f"  Ethical Accumulation: {agent_action.state.delta_phi_accum:.3f}")
    print(f"  Behavior: Execution without overthinking")
    
    print(f"\nBalanced Mode:")
    print(f"  Ethical Accumulation: {agent_balanced.state.delta_phi_accum:.3f}")
    print(f"  Behavior: Thoughtful action")
    
    print("\n" + "=" * 70)
    print("Key Insights")
    print("=" * 70)
    print("1. High activity SUPPRESSES ethical accumulation")
    print("2. Low activity ENABLES deep ethical consideration")
    print("3. This prevents 'analysis paralysis' during action")
    print("4. Creates realistic 'thinking vs. doing' dynamics")
    print("5. The coupling implements Σ(ΔΦ * Ω) / (Θn * F(P) + V)")
    print()
    print("✓ Action and ethics are now dynamically balanced!")


if __name__ == "__main__":
    main()
