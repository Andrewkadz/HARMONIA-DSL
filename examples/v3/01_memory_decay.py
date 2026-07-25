"""
HARMONIA-DSL v3.0 Example 1: Memory Decay

This example demonstrates the exp- (Exponential Decay) operator
modeling how memories fade over time.
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from nonlinear_operators import NonlinearOperators
from dataclasses import dataclass


@dataclass
class MemoryState:
    psi_signal: float = 0.0  # Memory strength
    phi_state: float = 0.0
    epsilon_drift: float = 0.1


@dataclass
class MemoryContext:
    state: MemoryState


class MemorySystem(NonlinearOperators):
    """A system that models memory decay"""
    
    def stabilize(self, context):
        context.state.phi_state = context.state.psi_signal * (1 - context.state.epsilon_drift)


def main():
    print("=" * 60)
    print("HARMONIA-DSL v3.0 Example 1: Memory Decay")
    print("=" * 60)
    
    system = MemorySystem()
    context = MemoryContext(state=MemoryState(psi_signal=100.0))
    
    print(f"\nInitial memory strength: {context.state.psi_signal:.2f}")
    print(f"Decay rate: 0.2 per time step")
    print(f"\nSimulating memory decay over 20 time steps...\n")
    
    for t in range(21):
        if t % 5 == 0:
            print(f"t={t:2d}: Memory strength = {context.state.psi_signal:6.2f}")
        
        # Apply exponential decay
        system.exponential_decay(None, context, "psi", decay_rate=0.2, dt=1.0)
    
    print(f"\n✓ Memory decayed from 100.00 to {context.state.psi_signal:.2f}")
    print("✓ This models natural forgetting and memory consolidation")
    print("\nApplications:")
    print("  • Modeling human memory decay")
    print("  • Cache eviction policies")
    print("  • Temporal discounting in decision-making")


if __name__ == "__main__":
    main()
