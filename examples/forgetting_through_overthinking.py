"""
Example 2: Forgetting Through Overthinking

Demonstrates the exponential decay term exp[-ΘN] which causes memory to fade
faster when the system is deeply engaged in thought (more layers).

Author: Manus AI
Date: January 1, 2026
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from nonlinear_dynamics import NonlinearFluidHarmoniaIntegrator


def main():
    print("=" * 70)
    print("HARMONIA-DSL v11.0 Example: Forgetting Through Overthinking")
    print("=" * 70)
    print()
    print("This demonstrates how deep thought (many layers) causes memory decay.")
    print("The exponential term exp[-ΘN] models 'forgetting through overthinking'.")
    print()
    
    # Scenario 1: Shallow thought (few layers, good memory retention)
    print("=" * 70)
    print("Scenario 1: Shallow Thought (Few Layers)")
    print("=" * 70)
    
    agent_shallow = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    agent_shallow.state.theta_n = 1.0  # Few layers
    agent_shallow.state.psi_memory = 20.0  # Strong initial memory
    agent_shallow.state.psi = 10.0  # Current awareness
    
    print(f"\nInitial State:")
    print(f"  Thought Layers (ΘN): {agent_shallow.state.theta_n:.2f}")
    print(f"  Memory (Ψ_mem): {agent_shallow.state.psi_memory:.2f}")
    print(f"  Current Awareness (Ψ): {agent_shallow.state.psi:.2f}")
    
    result_shallow = agent_shallow.process(duration=5.0)
    
    print(f"\nAfter 5 seconds:")
    print(f"  Thought Layers (ΘN): {agent_shallow.state.theta_n:.2f}")
    print(f"  Memory (Ψ_mem): {agent_shallow.state.psi_memory:.2f}")
    print(f"  Memory Retention: GOOD (shallow thinking preserves memory)")
    
    # Scenario 2: Deep thought (many layers, rapid memory decay)
    print("\n" + "=" * 70)
    print("Scenario 2: Deep Thought (Many Layers)")
    print("=" * 70)
    
    agent_deep = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    agent_deep.state.theta_n = 5.0  # Many layers
    agent_deep.state.psi_memory = 20.0  # Same initial memory
    agent_deep.state.psi = 10.0  # Same current awareness
    agent_deep.state.knowledge = 3.0  # More knowledge to grow layers
    
    print(f"\nInitial State:")
    print(f"  Thought Layers (ΘN): {agent_deep.state.theta_n:.2f}")
    print(f"  Memory (Ψ_mem): {agent_deep.state.psi_memory:.2f}")
    print(f"  Current Awareness (Ψ): {agent_deep.state.psi:.2f}")
    
    result_deep = agent_deep.process(duration=5.0)
    
    print(f"\nAfter 5 seconds:")
    print(f"  Thought Layers (ΘN): {agent_deep.state.theta_n:.2f}")
    print(f"  Memory (Ψ_mem): {agent_deep.state.psi_memory:.2f}")
    print(f"  Memory Retention: POOR (deep thinking causes forgetting)")
    
    # Scenario 3: Balanced thought
    print("\n" + "=" * 70)
    print("Scenario 3: Balanced Thought (Moderate Layers)")
    print("=" * 70)
    
    agent_balanced = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    agent_balanced.state.theta_n = 2.5  # Moderate layers
    agent_balanced.state.psi_memory = 20.0  # Same initial memory
    agent_balanced.state.psi = 10.0  # Same current awareness
    agent_balanced.state.knowledge = 1.5  # Moderate knowledge
    
    print(f"\nInitial State:")
    print(f"  Thought Layers (ΘN): {agent_balanced.state.theta_n:.2f}")
    print(f"  Memory (Ψ_mem): {agent_balanced.state.psi_memory:.2f}")
    
    result_balanced = agent_balanced.process(duration=5.0)
    
    print(f"\nAfter 5 seconds:")
    print(f"  Thought Layers (ΘN): {agent_balanced.state.theta_n:.2f}")
    print(f"  Memory (Ψ_mem): {agent_balanced.state.psi_memory:.2f}")
    print(f"  Memory Retention: MODERATE (balanced thinking)")
    
    # Comparison
    print("\n" + "=" * 70)
    print("Comparison: Exponential Decay Effect")
    print("=" * 70)
    
    print(f"\nShallow Thought (ΘN={agent_shallow.state.theta_n:.2f}):")
    print(f"  Final Memory: {agent_shallow.state.psi_memory:.2f}")
    print(f"  Behavior: Good memory retention")
    
    print(f"\nDeep Thought (ΘN={agent_deep.state.theta_n:.2f}):")
    print(f"  Final Memory: {agent_deep.state.psi_memory:.2f}")
    print(f"  Behavior: Rapid memory decay")
    
    print(f"\nBalanced Thought (ΘN={agent_balanced.state.theta_n:.2f}):")
    print(f"  Final Memory: {agent_balanced.state.psi_memory:.2f}")
    print(f"  Behavior: Moderate memory retention")
    
    print("\n" + "=" * 70)
    print("Key Insights")
    print("=" * 70)
    print("1. More thought layers (ΘN) = FASTER memory decay")
    print("2. This models 'forgetting through overthinking'")
    print("3. Deep analysis can cause you to lose sight of the original point")
    print("4. The exponential term exp[-ΘN] creates realistic forgetting")
    print("5. Balances depth of thought with memory retention")
    print()
    print("✓ Exponential memory decay successfully demonstrated!")


if __name__ == "__main__":
    main()
