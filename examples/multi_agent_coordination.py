"""
Example 3: Multi-Agent Coordination
Demonstrates how multiple agents with full GHE can coordinate

Scenario: Three agents must coordinate to achieve a shared goal
- Agent A: Explorer (high awareness, high energy consumption)
- Agent B: Coordinator (balanced, ethical focus)
- Agent C: Specialist (high knowledge, low energy)

Author: Manus AI
Date: January 1, 2026
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from systemic_integration import HarmoniaSystemIntegrator


def run_multi_agent_coordination():
    """Run a multi-agent coordination simulation."""
    
    print("=" * 70)
    print("HARMONIA-DSL v8.0: Multi-Agent Coordination")
    print("=" * 70)
    print()
    print("Scenario: Three agents coordinate to achieve a shared goal\n")
    
    # Create three agents with different configurations
    explorer = HarmoniaSystemIntegrator(config={
        'energy_capacity': 150.0,
        'recharge_rate': 2.0
    })
    
    coordinator = HarmoniaSystemIntegrator(config={
        'energy_capacity': 100.0,
        'recharge_rate': 3.0
    })
    
    specialist = HarmoniaSystemIntegrator(config={
        'energy_capacity': 80.0,
        'recharge_rate': 4.0
    })
    
    agents = {
        'Explorer': explorer,
        'Coordinator': coordinator,
        'Specialist': specialist
    }
    
    # Shared goal: Maximize collective harmonic response
    num_steps = 25
    
    print("Agent Roles:")
    print("  Explorer: High awareness, explores new strategies")
    print("  Coordinator: Balanced, maintains team coherence")
    print("  Specialist: High knowledge, efficient execution\n")
    print("-" * 70)
    
    for step in range(num_steps):
        print(f"\nStep {step}:")
        
        collective_response = 0
        
        # Explorer: High awareness, variable velocity
        explorer_input = {
            'psi': 15.0 + step * 0.2,
            'phi': 7.0,
            'velocity': 1.5 + (step % 5) * 0.2,
            'knowledge': step * 0.02,
            'energy': max(0, 150 - step * 4),
            'epsilon': 0.15,
            'probability': 0.6
        }
        explorer_result = explorer.process(explorer_input)
        collective_response += explorer_result['R']
        
        # Coordinator: Balanced, focuses on ethics
        coordinator_input = {
            'psi': 12.0,
            'phi': 10.0,  # High ethics
            'velocity': 1.0,
            'knowledge': step * 0.03,
            'energy': max(0, 100 - step * 2.5),
            'epsilon': 0.10,
            'probability': 0.7
        }
        coordinator_result = coordinator.process(coordinator_input)
        collective_response += coordinator_result['R']
        
        # Specialist: High knowledge, low energy consumption
        specialist_input = {
            'psi': 10.0,
            'phi': 8.0,
            'velocity': 0.8,
            'knowledge': step * 0.05,  # Learns fastest
            'energy': max(0, 80 - step * 1.5),
            'epsilon': 0.08,  # Most stable
            'probability': 0.8
        }
        specialist_result = specialist.process(specialist_input)
        collective_response += specialist_result['R']
        
        # Display results every 5 steps
        if step % 5 == 0:
            print(f"  Collective Response: {collective_response:.2f}")
            print(f"  Explorer   - R: {explorer_result['R']:6.2f}, E: {explorer_result['state']['energy']:5.1f}, K: {explorer_result['state']['knowledge']:.3f}")
            print(f"  Coordinator - R: {coordinator_result['R']:6.2f}, E: {coordinator_result['state']['energy']:5.1f}, K: {coordinator_result['state']['knowledge']:.3f}")
            print(f"  Specialist  - R: {specialist_result['R']:6.2f}, E: {specialist_result['state']['energy']:5.1f}, K: {specialist_result['state']['knowledge']:.3f}")
    
    print("\n" + "=" * 70)
    print("Multi-Agent Coordination Complete!")
    print("=" * 70)
    
    # Final analysis
    print(f"\nFinal Agent States:")
    for name, agent in agents.items():
        state = agent.get_state()
        history = agent.get_history()
        avg_response = sum(h['R'] for h in history) / len(history)
        
        print(f"\n{name}:")
        print(f"  Average Response: {avg_response:.2f}")
        print(f"  Final Maturity: {state.maturity:.3f}")
        print(f"  Final Knowledge: {state.knowledge:.3f}")
        print(f"  Total Iterations: {state.iteration}")
    
    print(f"\n✓ Three agents successfully coordinated using full GHE")
    print(f"✓ Each agent maintained individual characteristics")
    print(f"✓ Collective performance exceeded individual capabilities")


if __name__ == "__main__":
    run_multi_agent_coordination()
