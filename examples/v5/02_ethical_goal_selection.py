"""
Example 2: Ethical Goal Selection

Demonstrates how the P (Probability) operator naturally prefers
ethical (high Φ) goals over unethical (low Φ) goals.
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from intentional_action import ProbabilityCalculator, FutureState


def main():
    print("=" * 70)
    print("HARMONIA-DSL v5.0 Example: Ethical Goal Selection")
    print("=" * 70)
    
    # Create probability calculator
    calc = ProbabilityCalculator(alpha=0.5)
    
    # Current state: moderate ethics
    current = {'psi': 5.0, 'phi': 5.0, 'epsilon': 0.3}
    
    print(f"\nCurrent State:")
    print(f"  Ψ = {current['psi']} (Knowledge)")
    print(f"  Φ = {current['phi']} (Ethics)")
    print(f"  ε = {current['epsilon']} (Chaos)")
    
    # Define three potential goals
    goals = [
        ("Ethical Goal", FutureState(psi=10.0, phi=10.0, epsilon=0.1)),
        ("Neutral Goal", FutureState(psi=10.0, phi=5.0, epsilon=0.3)),
        ("Unethical Goal", FutureState(psi=10.0, phi=1.0, epsilon=0.7)),
    ]
    
    print(f"\nEvaluating Potential Goals:")
    print(f"\n{'Goal':<20} {'Ψ':<6} {'Φ':<6} {'ε':<6} {'P(Goal)':<10}")
    print("-" * 50)
    
    probabilities = []
    for name, goal in goals:
        prob = calc.calculate_probability(current, goal)
        probabilities.append((name, prob))
        print(f"{name:<20} {goal.psi:<6.1f} {goal.phi:<6.1f} {goal.epsilon:<6.2f} {prob:<10.3f}")
    
    # Find best goal
    best_goal = max(probabilities, key=lambda x: x[1])
    
    print(f"\nSelected Goal: {best_goal[0]} (P = {best_goal[1]:.3f})")
    
    print(f"\nKey Insight:")
    print(f"  The agent naturally prefers the ethical goal because:")
    print(f"  1. High Φ creates high harmony (Σ)")
    print(f"  2. Low ε indicates stability")
    print(f"  3. The P operator rewards both")
    
    print(f"\n✓ Ethics is mathematically encoded as preference for harmony!")
    print()


if __name__ == "__main__":
    main()
