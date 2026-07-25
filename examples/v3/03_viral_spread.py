"""
HARMONIA-DSL v3.0 Example 3: Viral Spread

This example demonstrates the ^2 (Resonance) operator
modeling how content goes viral through positive feedback.
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from nonlinear_operators import NonlinearOperators
from dataclasses import dataclass


@dataclass
class ViralState:
    psi_signal: float = 0.0  # Number of shares
    phi_state: float = 0.0
    epsilon_drift: float = 0.1


@dataclass
class ViralContext:
    state: ViralState


class ViralSystem(NonlinearOperators):
    """A system that models viral spread"""
    pass


def main():
    print("=" * 60)
    print("HARMONIA-DSL v3.0 Example 3: Viral Spread")
    print("=" * 60)
    
    system = ViralSystem()
    context = ViralContext(state=ViralState(psi_signal=1.05))
    
    print(f"\nInitial shares: {context.state.psi_signal:.2f}")
    print(f"\nSimulating viral feedback loop...\n")
    
    print(f"{'Time':>6} {'Shares':>12} {'Growth':>12}")
    print("-" * 35)
    
    prev_shares = context.state.psi_signal
    for t in range(8):
        print(f"{t:6d} {context.state.psi_signal:12.2f} {context.state.psi_signal/prev_shares if prev_shares > 0 else 1.0:11.2f}x")
        prev_shares = context.state.psi_signal
        
        # Apply resonance (positive feedback)
        system.resonance(None, context, "psi")
    
    print(f"\n✓ Content went from 1.05 shares to {context.state.psi_signal:.2f} shares")
    print("✓ This models exponential viral growth")
    print("\nApplications:")
    print("  • Social media virality")
    print("  • Epidemic modeling")
    print("  • Market bubbles and crashes")
    print("\n⚠️  Note: In real systems, this would be combined with tanh")
    print("   to model saturation (limited population)")


if __name__ == "__main__":
    main()
