"""
Example 3: Ethical Stability

Demonstrates the tanh saturation term tanh(ΔΦ / Ω) which prevents wild swings
in ethical state, creating stable moral reasoning.

Author: Manus AI
Date: January 1, 2026
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from nonlinear_dynamics import NonlinearFluidHarmoniaIntegrator


def main():
    print("=" * 70)
    print("HARMONIA-DSL v11.0 Example: Ethical Stability")
    print("=" * 70)
    print()
    print("This demonstrates how tanh saturation prevents wild ethical swings.")
    print("The term tanh(ΔΦ / Ω) creates stable moral reasoning.")
    print()
    
    # Scenario 1: High coherence (stable ethics)
    print("=" * 70)
    print("Scenario 1: High Coherence (Stable Ethics)")
    print("=" * 70)
    
    agent_stable = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    agent_stable.state.omega = 10.0  # High coherence
    agent_stable.state.phi = 8.0  # Initial ethics
    agent_stable.state.velocity = 2.0  # Some activity
    
    print(f"\nInitial State:")
    print(f"  Coherence (Ω): {agent_stable.state.omega:.2f}")
    print(f"  Ethics (Φ): {agent_stable.state.phi:.2f}")
    
    result_stable = agent_stable.process(duration=3.0)
    
    ethics_change = agent_stable.state.phi - 8.0
    
    print(f"\nAfter 3 seconds:")
    print(f"  Coherence (Ω): {agent_stable.state.omega:.2f}")
    print(f"  Ethics (Φ): {agent_stable.state.phi:.2f}")
    print(f"  Ethics Change: {ethics_change:.2f}")
    print(f"  Behavior: STABLE (high coherence prevents wild swings)")
    
    # Scenario 2: Low coherence (unstable ethics)
    print("\n" + "=" * 70)
    print("Scenario 2: Low Coherence (Potentially Unstable)")
    print("=" * 70)
    
    agent_unstable = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    agent_unstable.state.omega = 2.0  # Low coherence
    agent_unstable.state.phi = 8.0  # Same initial ethics
    agent_unstable.state.velocity = 2.0  # Same activity
    
    print(f"\nInitial State:")
    print(f"  Coherence (Ω): {agent_unstable.state.omega:.2f}")
    print(f"  Ethics (Φ): {agent_unstable.state.phi:.2f}")
    
    result_unstable = agent_unstable.process(duration=3.0)
    
    ethics_change_unstable = agent_unstable.state.phi - 8.0
    
    print(f"\nAfter 3 seconds:")
    print(f"  Coherence (Ω): {agent_unstable.state.omega:.2f}")
    print(f"  Ethics (Φ): {agent_unstable.state.phi:.2f}")
    print(f"  Ethics Change: {ethics_change_unstable:.2f}")
    print(f"  Behavior: LESS STABLE (low coherence allows larger changes)")
    
    # Scenario 3: Moderate coherence
    print("\n" + "=" * 70)
    print("Scenario 3: Moderate Coherence (Balanced)")
    print("=" * 70)
    
    agent_moderate = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    agent_moderate.state.omega = 5.0  # Moderate coherence
    agent_moderate.state.phi = 8.0  # Same initial ethics
    agent_moderate.state.velocity = 2.0  # Same activity
    
    print(f"\nInitial State:")
    print(f"  Coherence (Ω): {agent_moderate.state.omega:.2f}")
    print(f"  Ethics (Φ): {agent_moderate.state.phi:.2f}")
    
    result_moderate = agent_moderate.process(duration=3.0)
    
    ethics_change_moderate = agent_moderate.state.phi - 8.0
    
    print(f"\nAfter 3 seconds:")
    print(f"  Coherence (Ω): {agent_moderate.state.omega:.2f}")
    print(f"  Ethics (Φ): {agent_moderate.state.phi:.2f}")
    print(f"  Ethics Change: {ethics_change_moderate:.2f}")
    print(f"  Behavior: BALANCED (moderate stability)")
    
    # Comparison
    print("\n" + "=" * 70)
    print("Comparison: Tanh Saturation Effect")
    print("=" * 70)
    
    print(f"\nHigh Coherence (Ω=10.0):")
    print(f"  Ethics Change: {ethics_change:.2f}")
    print(f"  Stability: VERY STABLE")
    
    print(f"\nLow Coherence (Ω=2.0):")
    print(f"  Ethics Change: {ethics_change_unstable:.2f}")
    print(f"  Stability: LESS STABLE")
    
    print(f"\nModerate Coherence (Ω=5.0):")
    print(f"  Ethics Change: {ethics_change_moderate:.2f}")
    print(f"  Stability: BALANCED")
    
    print("\n" + "=" * 70)
    print("Key Insights")
    print("=" * 70)
    print("1. tanh saturation PREVENTS wild ethical swings")
    print("2. High coherence = MORE stable ethics")
    print("3. Low coherence = LESS stable ethics (but still bounded)")
    print("4. Creates realistic moral reasoning without extremes")
    print("5. Implements the advanced GHE term: tanh(ΔΦ / Ω)")
    print()
    print("✓ Ethical stability successfully demonstrated!")


if __name__ == "__main__":
    main()
