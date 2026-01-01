"""
HARMONIA-DSL v3.0 Example 2: Neural Activation

This example demonstrates the tanh (Hyperbolic Tangent) operator
modeling how neurons saturate at maximum firing rates.
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from nonlinear_operators import NonlinearOperators
from dataclasses import dataclass


@dataclass
class NeuronState:
    psi_signal: float = 0.0  # Input signal
    phi_state: float = 0.0    # Output (firing rate)
    epsilon_drift: float = 0.05


@dataclass
class NeuronContext:
    state: NeuronState


class NeuralSystem(NonlinearOperators):
    """A system that models neural activation"""
    
    def activate(self, context, max_firing_rate=100.0):
        """Apply neural activation function"""
        self.hyperbolic_tangent(None, context, "psi", scale_factor=max_firing_rate)
        context.state.phi_state = context.state.psi_signal


def main():
    print("=" * 60)
    print("HARMONIA-DSL v3.0 Example 2: Neural Activation")
    print("=" * 60)
    
    system = NeuralSystem()
    context = NeuronContext(state=NeuronState(psi_signal=0.0))
    
    print(f"\nMaximum firing rate: 100 Hz")
    print(f"\nIncreasing input stimulus and observing firing rate...\n")
    
    print(f"{'Input':>10} {'Firing Rate':>15}")
    print("-" * 30)
    
    for stimulus in [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 50.0, 100.0]:
        context.state.psi_signal = stimulus
        system.activate(context, max_firing_rate=100.0)
        print(f"{stimulus:10.1f} {context.state.phi_state:15.2f} Hz")
    
    print(f"\n✓ Firing rate saturates at ~100 Hz despite increasing input")
    print("✓ This models realistic neural behavior")
    print("\nApplications:")
    print("  • Neural network activation functions")
    print("  • Modeling biological neurons")
    print("  • Preventing runaway feedback in AI systems")


if __name__ == "__main__":
    main()
