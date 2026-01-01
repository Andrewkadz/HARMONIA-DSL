"""
Example 1: Simple Goal-Seeking Agent

Demonstrates a basic agent that uses intentional action (F(P) * V)
to move towards a harmonious goal state.
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from intentional_action import IntentionalActionEngine, FutureState


def main():
    print("=" * 70)
    print("HARMONIA-DSL v5.0 Example: Simple Goal-Seeking Agent")
    print("=" * 70)
    
    # Create the intentional action engine
    engine = IntentionalActionEngine(force_scale=0.4)
    
    # Define initial state (low harmony)
    history = [
        {'psi': 2.0, 'phi': 2.0, 'epsilon': 0.6},
        {'psi': 2.1, 'phi': 2.1, 'epsilon': 0.58},
    ]
    current = {'psi': 2.2, 'phi': 2.2, 'epsilon': 0.56}
    
    # Define goal (high harmony)
    goal = FutureState(psi=10.0, phi=10.0, epsilon=0.1)
    
    print(f"\nInitial State:")
    print(f"  Ψ = {current['psi']:.2f}")
    print(f"  Φ = {current['phi']:.2f}")
    print(f"  ε = {current['epsilon']:.3f}")
    sigma_initial = (current['psi'] + current['phi']) * (1 - current['epsilon'])
    print(f"  Σ = {sigma_initial:.2f}")
    
    print(f"\nGoal State:")
    print(f"  Ψ = {goal.psi:.2f}")
    print(f"  Φ = {goal.phi:.2f}")
    print(f"  ε = {goal.epsilon:.3f}")
    sigma_goal = (goal.psi + goal.phi) * (1 - goal.epsilon)
    print(f"  Σ = {sigma_goal:.2f}")
    
    print(f"\nApplying Intentional Action for 20 steps:")
    print(f"\n{'Step':<6} {'Ψ':<8} {'Φ':<8} {'ε':<8} {'Σ':<8}")
    print("-" * 40)
    
    for step in range(20):
        history.append(current.copy())
        current = engine.apply_intentional_force(current, history, goal)
        sigma = (current['psi'] + current['phi']) * (1 - current['epsilon'])
        
        print(f"{step+1:<6} {current['psi']:<8.2f} {current['phi']:<8.2f} {current['epsilon']:<8.3f} {sigma:<8.2f}")
    
    print(f"\nFinal State:")
    print(f"  Ψ = {current['psi']:.2f}")
    print(f"  Φ = {current['phi']:.2f}")
    print(f"  ε = {current['epsilon']:.3f}")
    sigma_final = (current['psi'] + current['phi']) * (1 - current['epsilon'])
    print(f"  Σ = {sigma_final:.2f}")
    
    print(f"\nImprovement:")
    print(f"  ΔΣ = {sigma_final - sigma_initial:.2f} ({((sigma_final / sigma_initial - 1) * 100):.1f}% increase)")
    
    print(f"\n✓ The agent successfully moved towards the harmonious goal!")
    print()


if __name__ == "__main__":
    main()
