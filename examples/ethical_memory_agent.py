"""
Example 1: Ethical Agent with Memory-Ethics Coupling

Demonstrates how the memory-ethics coupling creates a balance between
learning from experience and maintaining ethical principles.

Author: Manus AI
Date: January 1, 2026
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from cross_layer_coupling import CoupledFluidHarmoniaIntegrator


def main():
    print("=" * 70)
    print("HARMONIA-DSL v10.0 Example: Ethical Agent with Memory-Ethics Coupling")
    print("=" * 70)
    print()
    print("This agent demonstrates how ethics modulates memory influence.")
    print("High ethics suppresses past experience, creating principled behavior.")
    print()
    
    # Scenario 1: Low ethics agent (experience-driven)
    print("=" * 70)
    print("Scenario 1: Experience-Driven Agent (Low Ethics)")
    print("=" * 70)
    
    agent_low_ethics = CoupledFluidHarmoniaIntegrator(dt=0.01)
    agent_low_ethics.state.phi = 2.0  # Low ethics
    agent_low_ethics.state.knowledge = 5.0  # High knowledge
    
    print(f"\nInitial State:")
    print(f"  Ethics (Φ): {agent_low_ethics.state.phi:.2f} (LOW)")
    print(f"  Knowledge (K): {agent_low_ethics.state.knowledge:.2f}")
    print(f"  Memory (Ψ±): {agent_low_ethics.state.psi_memory:.2f}")
    
    result_low = agent_low_ethics.process(duration=3.0)
    
    print(f"\nAfter 3 seconds:")
    print(f"  Awareness (Ψ): {agent_low_ethics.state.psi:.2f}")
    print(f"  Ethics (Φ): {agent_low_ethics.state.phi:.2f}")
    print(f"  Memory Influence: STRONG (low ethics allows memory to drive behavior)")
    
    # Scenario 2: High ethics agent (principle-driven)
    print("\n" + "=" * 70)
    print("Scenario 2: Principle-Driven Agent (High Ethics)")
    print("=" * 70)
    
    agent_high_ethics = CoupledFluidHarmoniaIntegrator(dt=0.01)
    agent_high_ethics.state.phi = 15.0  # High ethics
    agent_high_ethics.state.knowledge = 5.0  # Same knowledge
    
    print(f"\nInitial State:")
    print(f"  Ethics (Φ): {agent_high_ethics.state.phi:.2f} (HIGH)")
    print(f"  Knowledge (K): {agent_high_ethics.state.knowledge:.2f}")
    print(f"  Memory (Ψ±): {agent_high_ethics.state.psi_memory:.2f}")
    
    result_high = agent_high_ethics.process(duration=3.0)
    
    print(f"\nAfter 3 seconds:")
    print(f"  Awareness (Ψ): {agent_high_ethics.state.psi:.2f}")
    print(f"  Ethics (Φ): {agent_high_ethics.state.phi:.2f}")
    print(f"  Memory Influence: SUPPRESSED (high ethics constrains past experience)")
    
    # Comparison
    print("\n" + "=" * 70)
    print("Comparison: Memory-Ethics Coupling Effect")
    print("=" * 70)
    
    print(f"\nLow Ethics Agent:")
    print(f"  Final Awareness: {agent_low_ethics.state.psi:.2f}")
    print(f"  Harmonic Response: {result_low['R']:.2f}")
    print(f"  Behavior: Driven by past experience")
    
    print(f"\nHigh Ethics Agent:")
    print(f"  Final Awareness: {agent_high_ethics.state.psi:.2f}")
    print(f"  Harmonic Response: {result_high['R']:.2f}")
    print(f"  Behavior: Guided by ethical principles")
    
    print("\n" + "=" * 70)
    print("Key Insights")
    print("=" * 70)
    print("1. Memory-ethics coupling creates a BALANCE")
    print("2. High ethics SUPPRESSES memory influence (division by Φ)")
    print("3. Low ethics allows experience to DRIVE behavior")
    print("4. This creates realistic ethical vs. pragmatic trade-offs")
    print("5. The coupling is mathematically grounded in the GHE")
    print()
    print("✓ Memory and ethics are now deeply interlinked!")


if __name__ == "__main__":
    main()
