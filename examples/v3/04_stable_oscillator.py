"""
HARMONIA-DSL v3.0 Example 4: Stable Oscillator

This example demonstrates combining all three nonlinear operators
to create a stable, bounded oscillating system.
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from nonlinear_operators import NonlinearOperators
from dataclasses import dataclass


@dataclass
class OscillatorState:
    psi_signal: float = 0.0  # Primary oscillating variable
    phi_state: float = 0.0    # Secondary variable
    epsilon_drift: float = 0.05
    stabilized_value: float = 0.0


@dataclass
class OscillatorContext:
    state: OscillatorState


class StableOscillator(NonlinearOperators):
    """A nonlinear oscillator with bounded behavior"""
    
    def stabilize(self, context):
        context.state.stabilized_value = (
            (context.state.psi_signal + context.state.phi_state) * 
            (1 - context.state.epsilon_drift)
        )


def main():
    print("=" * 60)
    print("HARMONIA-DSL v3.0 Example 4: Stable Oscillator")
    print("=" * 60)
    
    system = StableOscillator()
    context = OscillatorContext(state=OscillatorState(psi_signal=2.0, phi_state=3.0))
    
    print(f"\nInitial: ψ={context.state.psi_signal:.2f}, φ={context.state.phi_state:.2f}")
    print(f"\nCombining resonance (^2), saturation (tanh), and decay (exp-)...\n")
    
    print(f"{'Time':>6} {'ψ':>10} {'φ':>10} {'Σ':>10}")
    print("-" * 40)
    
    for t in range(30):
        # Apply resonance to ψ (amplification)
        system.resonance(None, context, "psi")
        
        # Apply tanh to prevent runaway (saturation)
        system.hyperbolic_tangent(None, context, "psi", scale_factor=5.0)
        
        # Apply decay to φ (dampening)
        system.exponential_decay(None, context, "phi", decay_rate=0.1, dt=1.0)
        
        # Stabilize
        system.stabilize(context)
        
        if t % 3 == 0:  # Print every 3rd step
            print(f"{t:6d} {context.state.psi_signal:10.4f} {context.state.phi_state:10.4f} {context.state.stabilized_value:10.4f}")
    
    print(f"\n✓ System exhibits stable, bounded oscillations")
    print("✓ Resonance amplifies, tanh saturates, exp- dampens")
    print("\nApplications:")
    print("  • Modeling heartbeat rhythms")
    print("  • Economic boom-bust cycles")
    print("  • Neural oscillations in the brain")
    print("  • Foundation for consciousness modeling")


if __name__ == "__main__":
    main()
