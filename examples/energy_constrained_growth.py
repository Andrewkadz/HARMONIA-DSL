"""
Example 3: Energy-Constrained Growth

Demonstrates how the energy-growth coupling creates realistic saturation
in maturity development based on available resources.

Author: Manus AI
Date: January 1, 2026
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from cross_layer_coupling import CoupledFluidHarmoniaIntegrator


def main():
    print("=" * 70)
    print("HARMONIA-DSL v10.0 Example: Energy-Constrained Growth")
    print("=" * 70)
    print()
    print("This demonstrates how growth saturates based on energy availability.")
    print("The tanh function creates realistic bounded growth.")
    print()
    
    # Scenario 1: High energy (rapid growth)
    print("=" * 70)
    print("Scenario 1: High Energy Environment")
    print("=" * 70)
    
    agent_high_energy = CoupledFluidHarmoniaIntegrator(dt=0.01)
    agent_high_energy.state.energy = 120.0  # High energy
    agent_high_energy.state.knowledge = 2.0  # Some knowledge
    
    print(f"\nInitial State:")
    print(f"  Energy: {agent_high_energy.state.energy:.2f} (HIGH)")
    print(f"  Knowledge (K): {agent_high_energy.state.knowledge:.2f}")
    print(f"  Maturity (Γ): {agent_high_energy.state.maturity:.3f}")
    
    result_high = agent_high_energy.process(
        inputs={'velocity': 1.5},
        duration=8.0
    )
    
    print(f"\nAfter 8 seconds:")
    print(f"  Energy: {agent_high_energy.state.energy:.2f}")
    print(f"  Maturity (Γ): {agent_high_energy.state.maturity:.3f}")
    print(f"  Growth Rate: RAPID (high energy enables fast development)")
    
    # Scenario 2: Low energy (slow growth)
    print("\n" + "=" * 70)
    print("Scenario 2: Low Energy Environment")
    print("=" * 70)
    
    agent_low_energy = CoupledFluidHarmoniaIntegrator(dt=0.01)
    agent_low_energy.state.energy = 50.0  # Low energy
    agent_low_energy.state.knowledge = 2.0  # Same knowledge
    
    print(f"\nInitial State:")
    print(f"  Energy: {agent_low_energy.state.energy:.2f} (LOW)")
    print(f"  Knowledge (K): {agent_low_energy.state.knowledge:.2f}")
    print(f"  Maturity (Γ): {agent_low_energy.state.maturity:.3f}")
    
    result_low = agent_low_energy.process(
        inputs={'velocity': 1.5},
        duration=8.0
    )
    
    print(f"\nAfter 8 seconds:")
    print(f"  Energy: {agent_low_energy.state.energy:.2f}")
    print(f"  Maturity (Γ): {agent_low_energy.state.maturity:.3f}")
    print(f"  Growth Rate: SLOW (low energy constrains development)")
    
    # Scenario 3: Maturity saturation
    print("\n" + "=" * 70)
    print("Scenario 3: Maturity Saturation (tanh effect)")
    print("=" * 70)
    
    agent_mature = CoupledFluidHarmoniaIntegrator(dt=0.01)
    agent_mature.state.maturity = 0.8  # Already mature
    agent_mature.state.energy = 120.0  # High energy
    agent_mature.state.knowledge = 5.0  # High knowledge
    
    print(f"\nInitial State:")
    print(f"  Maturity (Γ): {agent_mature.state.maturity:.3f} (ALREADY HIGH)")
    print(f"  Energy: {agent_mature.state.energy:.2f}")
    print(f"  Knowledge (K): {agent_mature.state.knowledge:.2f}")
    
    result_mature = agent_mature.process(
        inputs={'velocity': 1.5},
        duration=8.0
    )
    
    print(f"\nAfter 8 seconds:")
    print(f"  Maturity (Γ): {agent_mature.state.maturity:.3f}")
    print(f"  Growth: SATURATED (tanh prevents unbounded growth)")
    
    # Comparison
    print("\n" + "=" * 70)
    print("Comparison: Energy-Growth Coupling Effect")
    print("=" * 70)
    
    print(f"\nHigh Energy Environment:")
    print(f"  Final Maturity: {agent_high_energy.state.maturity:.3f}")
    print(f"  Growth: Rapid development enabled")
    
    print(f"\nLow Energy Environment:")
    print(f"  Final Maturity: {agent_low_energy.state.maturity:.3f}")
    print(f"  Growth: Constrained by resources")
    
    print(f"\nAlready Mature Agent:")
    print(f"  Final Maturity: {agent_mature.state.maturity:.3f}")
    print(f"  Growth: Saturated (approaching 1.0 asymptotically)")
    
    print("\n" + "=" * 70)
    print("Key Insights")
    print("=" * 70)
    print("1. Growth is BOUNDED by available energy")
    print("2. tanh creates SATURATION as maturity approaches 1.0")
    print("3. Prevents unrealistic unbounded growth")
    print("4. Creates realistic resource-constrained development")
    print("5. Implements [Cξ * (Eψ/R)] * tanh(ΓΛ√Ξ)")
    print()
    print("✓ Energy and growth are now coupled for realism!")


if __name__ == "__main__":
    main()
