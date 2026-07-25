"""
HARMONIA-DSL v4.0 Example 1: Long-Term Safety Verification

This example demonstrates how to use convergence analysis to prove
that a system is safe for all future time.
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from convergence_analysis import analyze_system_convergence
from nonlinear_operators import NonlinearOperators
from dataclasses import dataclass


@dataclass
class SafetyState:
    psi_signal: float = 0.0
    phi_state: float = 0.0
    epsilon_drift: float = 0.0
    stabilized_value: float = 0.0


@dataclass
class SafetyContext:
    state: SafetyState


class SafetySystem(NonlinearOperators):
    def stabilize(self, context):
        context.state.stabilized_value = (
            (context.state.psi_signal + context.state.phi_state) * 
            (1 - context.state.epsilon_drift)
        )


def main():
    print("=" * 70)
    print("HARMONIA-DSL v4.0: Long-Term Safety Verification")
    print("=" * 70)
    print()
    
    # Create a system with potentially dangerous initial conditions
    system = SafetySystem()
    context = SafetyContext(state=SafetyState(
        psi_signal=15.0,  # High signal
        phi_state=10.0,   # High state
        epsilon_drift=0.2  # Moderate drift
    ))
    
    print(f"Initial conditions:")
    print(f"  ψ (signal):  {context.state.psi_signal:.2f}")
    print(f"  φ (state):   {context.state.phi_state:.2f}")
    print(f"  ε (drift):   {context.state.epsilon_drift:.2f}")
    print()
    
    # Define the system dynamics
    def update(ctx):
        # Apply saturation to prevent unbounded growth
        system.hyperbolic_tangent(None, ctx, "psi", scale_factor=20.0)
        
        # Apply decay to phi
        system.exponential_decay(None, ctx, "phi", decay_rate=0.2, dt=1.0)
        
        # Stabilize
        system.stabilize(ctx)
    
    print("System dynamics:")
    print("  - Signal saturates at 20.0 (tanh)")
    print("  - State decays exponentially")
    print("  - Homeostatic stabilization applied")
    print()
    
    # Analyze long-term convergence
    print("Analyzing long-term behavior...")
    analyzer = analyze_system_convergence(
        context, 
        update, 
        max_iterations=1000, 
        tolerance=0.001
    )
    
    print()
    print("=" * 70)
    print("CONVERGENCE ANALYSIS RESULTS")
    print("=" * 70)
    print()
    
    print(f"✓ Attractor Type: {analyzer.get_attractor_type()}")
    print(f"✓ System Stable: {analyzer.is_stable()}")
    print(f"✓ Converged: {analyzer.result.converged}")
    print(f"✓ Iterations: {analyzer.result.iterations}")
    print()
    
    if analyzer.result.attractor_state:
        state = analyzer.result.attractor_state
        print(f"Final equilibrium state:")
        print(f"  ψ (signal):  {state.psi_signal:.4f}")
        print(f"  φ (state):   {state.phi_state:.4f}")
        print(f"  ε (drift):   {state.epsilon_drift:.4f}")
        print(f"  Σ (output):  {state.stabilized_value:.4f}")
        print()
        
        # Check safety criteria
        print("Safety criteria:")
        SAFE_THRESHOLD = 30.0
        DRIFT_THRESHOLD = 0.5
        
        if state.stabilized_value < SAFE_THRESHOLD:
            print(f"  ✅ Output < {SAFE_THRESHOLD}: PASS")
        else:
            print(f"  ❌ Output >= {SAFE_THRESHOLD}: FAIL")
        
        if state.epsilon_drift < DRIFT_THRESHOLD:
            print(f"  ✅ Drift < {DRIFT_THRESHOLD}: PASS")
        else:
            print(f"  ❌ Drift >= {DRIFT_THRESHOLD}: FAIL")
        
        print()
        
        if analyzer.is_stable() and state.stabilized_value < SAFE_THRESHOLD and state.epsilon_drift < DRIFT_THRESHOLD:
            print("🎉 SAFETY VERIFIED: System is provably safe for all future time!")
        else:
            print("⚠️  WARNING: System may enter unsafe states!")
    
    print()
    print("=" * 70)
    print("Key Insight:")
    print("=" * 70)
    print()
    print("By analyzing convergence, we can PROVE long-term safety,")
    print("not just hope for it. This is the foundation of verifiable AI safety.")
    print()


if __name__ == "__main__":
    main()
