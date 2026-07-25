"""
Example 3: Continuous Learning Agent

Demonstrates how knowledge and maturity accumulate continuously
over time, creating a truly adaptive learning system.

Author: Manus AI
Date: January 1, 2026
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from continuous_dynamics import FluidHarmoniaIntegrator


def main():
    print("=" * 70)
    print("HARMONIA-DSL v9.0 Example: Continuous Learning Agent")
    print("=" * 70)
    print()
    print("This agent learns continuously from experience.")
    print("Watch how knowledge and maturity evolve over time.")
    print()
    
    # Create agent
    agent = FluidHarmoniaIntegrator(dt=0.01)
    
    # Learning scenarios
    scenarios = [
        {
            'name': 'Novice Phase',
            'description': 'Initial learning with moderate effort',
            'velocity': 1.0,
            'duration': 3.0
        },
        {
            'name': 'Practice Phase',
            'description': 'Intensive practice and skill development',
            'velocity': 2.0,
            'duration': 3.0
        },
        {
            'name': 'Mastery Phase',
            'description': 'Refinement and deep understanding',
            'velocity': 1.5,
            'duration': 3.0
        },
        {
            'name': 'Teaching Phase',
            'description': 'Sharing knowledge with others',
            'velocity': 0.5,
            'duration': 3.0
        }
    ]
    
    print("Initial State:")
    print(f"  Knowledge (K): {agent.state.knowledge:.3f}")
    print(f"  Maturity (Γ): {agent.state.maturity:.3f}")
    print(f"  Awareness (Ψ): {agent.state.psi:.2f}")
    print()
    
    for scenario in scenarios:
        print(f"\n{'='*70}")
        print(f"{scenario['name']}: {scenario['description']}")
        print('='*70)
        
        result = agent.process(
            inputs={'velocity': scenario['velocity']},
            duration=scenario['duration']
        )
        
        state = agent.state
        
        print(f"\nTime: {state.time:.1f}s")
        print(f"  Knowledge (K): {state.knowledge:.3f}")
        print(f"  Maturity (Γ): {state.maturity:.3f}")
        print(f"  Awareness (Ψ): {state.psi:.2f}")
        print(f"  Ethics (Φ): {state.phi:.2f}")
        print(f"  Coherence (Ω): {state.omega:.2f}")
        print(f"  Energy: {state.energy:.2f}")
        
        # Calculate learning rate
        trajectory = result['trajectory']
        knowledge_values = trajectory['states'][:, 5]
        learning_rate = (knowledge_values[-1] - knowledge_values[0]) / scenario['duration']
        
        print(f"\n  Learning rate: {learning_rate:.3f} units/second")
        
        # Analyze maturity growth
        maturity_values = trajectory['states'][:, 6]
        if maturity_values[-1] >= 0.99:
            print(f"  Status: MASTERY ACHIEVED (Γ ≈ 1.0)")
        elif maturity_values[-1] >= 0.75:
            print(f"  Status: ADVANCED (Γ ≈ {maturity_values[-1]:.2f})")
        elif maturity_values[-1] >= 0.50:
            print(f"  Status: INTERMEDIATE (Γ ≈ {maturity_values[-1]:.2f})")
        else:
            print(f"  Status: BEGINNER (Γ ≈ {maturity_values[-1]:.2f})")
    
    print("\n" + "=" * 70)
    print("Learning Journey Summary")
    print("=" * 70)
    
    history = agent.get_history()
    
    print(f"\nTotal time: {agent.state.time:.1f}s")
    print(f"Initial knowledge: 0.000")
    print(f"Final knowledge: {agent.state.knowledge:.3f}")
    print(f"Knowledge gain: {agent.state.knowledge:.3f} units")
    print()
    print(f"Initial maturity: 0.000")
    print(f"Final maturity: {agent.state.maturity:.3f}")
    print(f"Maturity gain: {agent.state.maturity:.3f}")
    print()
    print("Key Insights:")
    print("1. Knowledge accumulates CONTINUOUSLY (no discrete steps)")
    print("2. Maturity follows a LOGISTIC GROWTH curve (bounded by 1.0)")
    print("3. Learning rate depends on awareness and coherence")
    print("4. The agent becomes more capable over time")
    print("5. Mastery is achieved through sustained practice")
    print()
    print("✓ Continuous-time enables realistic learning dynamics!")


if __name__ == "__main__":
    main()
