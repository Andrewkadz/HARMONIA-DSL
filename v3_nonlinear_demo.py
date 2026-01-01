"""
HARMONIA-DSL v3.0 Nonlinear Dynamics Demonstration

This script demonstrates the three new nonlinear operators:
- exp- (Exponential Decay)
- tanh (Hyperbolic Tangent)
- ^2 (Resonance)
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from nonlinear_operators import NonlinearOperators
from dataclasses import dataclass


@dataclass
class SimpleState:
    """Simplified state for demonstration"""
    psi_signal: float = 0.0
    phi_state: float = 0.0
    epsilon_drift: float = 0.0
    stabilized_value: float = 0.0


@dataclass
class SimpleContext:
    """Simplified context for demonstration"""
    state: SimpleState


class V3Demo(NonlinearOperators):
    """Demonstration class with nonlinear operators"""
    
    def stabilize(self, context):
        """Apply the core stabilization formula"""
        context.state.stabilized_value = (
            (context.state.psi_signal + context.state.phi_state) * 
            (1 - context.state.epsilon_drift)
        )


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"{title:^60}")
    print("=" * 60)


def demo_exponential_decay():
    """Demonstrate exponential decay operator"""
    print_header("DEMO 1: Exponential Decay (exp-)")
    
    demo = V3Demo()
    context = SimpleContext(state=SimpleState(psi_signal=10.0, phi_state=5.0, epsilon_drift=0.1))
    
    print(f"\nInitial ψ: {context.state.psi_signal:.4f}")
    print(f"Decay rate: 0.3")
    print(f"\nApplying exponential decay over 10 time steps...\n")
    
    for t in range(10):
        demo.exponential_decay(None, context, "psi", decay_rate=0.3, dt=1.0)
        demo.stabilize(context)
        print(f"t={t+1:2d}: ψ={context.state.psi_signal:6.4f}, Σ={context.state.stabilized_value:6.4f}")
    
    print(f"\n✓ ψ decayed from 10.0 to {context.state.psi_signal:.4f}")
    print("✓ This models memory decay, cooling, return to equilibrium")


def demo_hyperbolic_tangent():
    """Demonstrate hyperbolic tangent operator"""
    print_header("DEMO 2: Hyperbolic Tangent (tanh)")
    
    demo = V3Demo()
    context = SimpleContext(state=SimpleState(psi_signal=0.5, phi_state=5.0, epsilon_drift=0.1))
    
    print(f"\nStarting ψ: {context.state.psi_signal:.4f}")
    print(f"Scale factor: 10.0")
    print(f"\nIncreasing ψ and applying tanh saturation...\n")
    
    for t in range(15):
        # Increase ψ linearly
        context.state.psi_signal += 0.5
        
        # Apply tanh to prevent runaway growth
        demo.hyperbolic_tangent(None, context, "psi", scale_factor=10.0)
        demo.stabilize(context)
        
        print(f"t={t+1:2d}: ψ={context.state.psi_signal:6.4f}, Σ={context.state.stabilized_value:6.4f}")
    
    print(f"\n✓ ψ saturated at {context.state.psi_signal:.4f} (max ~10.0)")
    print("✓ This prevents runaway growth, models neural activation")


def demo_resonance():
    """Demonstrate resonance operator"""
    print_header("DEMO 3: Resonance (^2)")
    
    demo = V3Demo()
    context = SimpleContext(state=SimpleState(psi_signal=1.1, phi_state=5.0, epsilon_drift=0.1))
    
    print(f"\nInitial ψ: {context.state.psi_signal:.4f}")
    print(f"\nApplying resonance (squaring) over 5 time steps...\n")
    print("WARNING: This can lead to explosive growth!")
    
    for t in range(5):
        demo.resonance(None, context, "psi")
        demo.stabilize(context)
        print(f"t={t+1:2d}: ψ={context.state.psi_signal:8.4f}, Σ={context.state.stabilized_value:8.4f}")
    
    print(f"\n✓ ψ grew explosively from 1.1 to {context.state.psi_signal:.4f}")
    print("✓ This models viral spread, feedback loops, amplification")


def demo_combined_nonlinearity():
    """Demonstrate combined nonlinear operators"""
    print_header("DEMO 4: Combined Nonlinearity (Oscillator)")
    
    demo = V3Demo()
    context = SimpleContext(state=SimpleState(psi_signal=2.0, phi_state=3.0, epsilon_drift=0.1))
    
    print(f"\nCreating a nonlinear oscillator using resonance + tanh...")
    print(f"Initial: ψ={context.state.psi_signal:.4f}, φ={context.state.phi_state:.4f}\n")
    
    for t in range(20):
        # Apply resonance to ψ (amplification)
        demo.resonance(None, context, "psi")
        
        # Apply tanh to prevent runaway (saturation)
        demo.hyperbolic_tangent(None, context, "psi", scale_factor=5.0)
        
        # Apply decay to φ (dampening)
        demo.exponential_decay(None, context, "phi", decay_rate=0.1, dt=1.0)
        
        # Stabilize
        demo.stabilize(context)
        
        if t % 2 == 0:  # Print every other step
            print(f"t={t+1:2d}: ψ={context.state.psi_signal:6.4f}, φ={context.state.phi_state:6.4f}, Σ={context.state.stabilized_value:6.4f}")
    
    print(f"\n✓ System exhibits complex, nonlinear dynamics")
    print("✓ Resonance amplifies, tanh saturates, exp- dampens")
    print("✓ This is the foundation for modeling consciousness!")


def main():
    """Run all v3.0 demonstrations"""
    print("\n╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "HARMONIA-DSL v3.0 DEMONSTRATION".center(58) + "║")
    print("║" + "Nonlinear Dynamics".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    demo_exponential_decay()
    demo_hyperbolic_tangent()
    demo_resonance()
    demo_combined_nonlinearity()
    
    print("\n" + "=" * 60)
    print("SUMMARY".center(60))
    print("=" * 60)
    print("\n✅ exp- (Exponential Decay): Natural dampening and decay")
    print("✅ tanh (Hyperbolic Tangent): Saturation and soft limits")
    print("✅ ^2 (Resonance): Amplification and feedback loops")
    print("✅ Combined: Complex, emergent, nonlinear behavior")
    print("\nv3.0 enables modeling of:")
    print("  • Neural networks and activation functions")
    print("  • Population dynamics and resource limits")
    print("  • Economic systems and market crashes")
    print("  • Consciousness and complex cognition")
    print("\n" + "=" * 60)
    print("\n🚀 HARMONIA-DSL v3.0: From linear to realistic!")


if __name__ == "__main__":
    main()
