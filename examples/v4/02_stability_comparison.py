"""
HARMONIA-DSL v4.0 Example 2: Comparing Stable vs Unstable Systems

This example demonstrates the difference between systems with and without
proper stabilization mechanisms.
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from convergence_analysis import analyze_system_convergence
from nonlinear_operators import NonlinearOperators
from dataclasses import dataclass


@dataclass
class SystemState:
    psi_signal: float = 0.0
    phi_state: float = 0.0
    epsilon_drift: float = 0.0
    stabilized_value: float = 0.0


@dataclass
class SystemContext:
    state: SystemState


class System(NonlinearOperators):
    def stabilize(self, context):
        context.state.stabilized_value = (
            (context.state.psi_signal + context.state.phi_state) * 
            (1 - context.state.epsilon_drift)
        )


def analyze_stable_system():
    """Analyze a system with proper stabilization"""
    print("=" * 70)
    print("SYSTEM A: With Stabilization (tanh saturation)")
    print("=" * 70)
    print()
    
    system = System()
    context = SystemContext(state=SystemState(psi_signal=3.0, phi_state=2.0))
    
    def update(ctx):
        # Resonance with saturation
        system.resonance(None, ctx, "psi")
        system.hyperbolic_tangent(None, ctx, "psi", scale_factor=10.0)
        system.stabilize(ctx)
    
    print("Dynamics: Resonance + Saturation")
    print(f"Initial: ψ={context.state.psi_signal:.2f}")
    print("\nAnalyzing...")
    
    analyzer = analyze_system_convergence(context, update, max_iterations=200, tolerance=0.001)
    
    print(f"\n✓ Stable: {analyzer.is_stable()}")
    print(f"✓ Attractor: {analyzer.get_attractor_type()}")
    print(f"✓ Iterations: {analyzer.result.iterations}")
    
    if analyzer.result.attractor_state:
        print(f"✓ Final ψ: {analyzer.result.attractor_state.psi_signal:.4f}")
    
    print("\n→ The saturation prevents unbounded growth.")
    print()


def analyze_unstable_system():
    """Analyze a system without stabilization"""
    print("=" * 70)
    print("SYSTEM B: Without Stabilization (pure resonance)")
    print("=" * 70)
    print()
    
    system = System()
    context = SystemContext(state=SystemState(psi_signal=1.5, phi_state=1.5))
    
    def update(ctx):
        # Pure resonance without saturation
        system.resonance(None, ctx, "psi")
        system.stabilize(ctx)
    
    print("Dynamics: Pure Resonance (no saturation)")
    print(f"Initial: ψ={context.state.psi_signal:.2f}")
    print("\nAnalyzing...")
    
    analyzer = analyze_system_convergence(context, update, max_iterations=50, tolerance=0.001)
    
    print(f"\n✓ Stable: {analyzer.is_stable()}")
    print(f"✓ Attractor: {analyzer.get_attractor_type()}")
    print(f"✓ Iterations: {analyzer.result.iterations}")
    
    print("\n→ Without saturation, the system diverges (unsafe!).")
    print()


def main():
    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  HARMONIA-DSL v4.0: Stability Comparison".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    analyze_stable_system()
    analyze_unstable_system()
    
    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print()
    print("Convergence analysis reveals the critical importance of")
    print("stabilization mechanisms like saturation (tanh).")
    print()
    print("Without them, even simple systems can become unsafe.")
    print()


if __name__ == "__main__":
    main()
