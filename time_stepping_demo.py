"""HARMONIA-DSL v2.0: Time-Stepping Demonstration

This is a simplified but functional demonstration of the v2.0 Time & Dynamics
concept. It shows how time-stepping, state history, and calculus operators
work in principle.

For full integration with the core interpreter, additional refactoring would
be needed to persist state between interpreter calls.
"""

from typing import List, Dict
from collections import deque
from dataclasses import dataclass, field
import math


@dataclass
class TimeSteppingState:
    """State that evolves over time"""
    psi_signal: float = 0.0
    phi_state: float = 0.0
    epsilon_drift: float = 0.0
    stabilized_value: float = 0.0
    
    def stabilize(self):
        """Apply the core stabilization formula: Σ = (ψ + φ) * (1 - ε)"""
        self.stabilized_value = (self.psi_signal + self.phi_state) * (1 - self.epsilon_drift)
        return self.stabilized_value


@dataclass
class TimeSteppingContext:
    """Context for time-stepping simulation"""
    current_time: int = 0
    num_steps: int = 0
    history_maxlen: int = 1000
    history: Dict[str, deque] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.history:
            self.history = {
                "psi_signal": deque(maxlen=self.history_maxlen),
                "phi_state": deque(maxlen=self.history_maxlen),
                "epsilon_drift": deque(maxlen=self.history_maxlen),
                "stabilized_value": deque(maxlen=self.history_maxlen),
            }
    
    def record_state(self, state: TimeSteppingState):
        """Record current state into history"""
        self.history["psi_signal"].append(state.psi_signal)
        self.history["phi_state"].append(state.phi_state)
        self.history["epsilon_drift"].append(state.epsilon_drift)
        self.history["stabilized_value"].append(state.stabilized_value)
    
    def get_history(self, variable_name: str) -> List[float]:
        """Get complete history of a variable"""
        return list(self.history.get(variable_name, []))


class TimeSteppingSimulator:
    """Simplified time-stepping simulator for demonstration"""
    
    def __init__(self, history_maxlen: int = 1000):
        self.history_maxlen = history_maxlen
    
    def run_constant(self, psi: float, phi: float, epsilon: float, num_steps: int) -> TimeSteppingContext:
        """Run a simulation with constant values"""
        context = TimeSteppingContext(history_maxlen=self.history_maxlen)
        context.num_steps = num_steps
        state = TimeSteppingState(psi, phi, epsilon)
        
        for t in range(num_steps):
            context.current_time = t
            state.stabilize()
            context.record_state(state)
        
        return context
    
    def run_dynamic(self, initial_psi: float, initial_phi: float, initial_epsilon: float,
                   psi_delta: float, phi_delta: float, epsilon_delta: float,
                   num_steps: int) -> TimeSteppingContext:
        """Run a simulation where values change over time"""
        context = TimeSteppingContext(history_maxlen=self.history_maxlen)
        context.num_steps = num_steps
        state = TimeSteppingState(initial_psi, initial_phi, initial_epsilon)
        
        for t in range(num_steps):
            context.current_time = t
            state.stabilize()
            context.record_state(state)
            
            # Update state for next step
            state.psi_signal += psi_delta
            state.phi_state += phi_delta
            state.epsilon_drift += epsilon_delta
            
            # Keep epsilon in [0, 1]
            state.epsilon_drift = max(0.0, min(1.0, state.epsilon_drift))
        
        return context
    
    def compute_derivative(self, context: TimeSteppingContext, variable_name: str) -> float:
        """Compute derivative using backward difference"""
        history = context.get_history(variable_name)
        if len(history) < 2:
            return 0.0
        return history[-1] - history[-2]
    
    def compute_integral(self, context: TimeSteppingContext, variable_name: str, 
                        window_size: int = None) -> float:
        """Compute integral using trapezoidal rule"""
        history = context.get_history(variable_name)
        if len(history) < 2:
            return 0.0
        
        if window_size is None or window_size > len(history):
            window = history
        else:
            window = history[-window_size:]
        
        integral = 0.0
        for i in range(len(window) - 1):
            integral += (window[i] + window[i + 1]) / 2.0
        
        return integral


# Demonstration functions
def demo_constant_system():
    """Demonstrate a system with constant values"""
    print("=" * 60)
    print("DEMO 1: Constant System")
    print("=" * 60)
    
    sim = TimeSteppingSimulator()
    result = sim.run_constant(psi=5.0, phi=3.0, epsilon=0.1, num_steps=10)
    
    print(f"Ran for {result.num_steps} time steps")
    print(f"ψ history: {result.get_history('psi_signal')[:5]}...")
    print(f"Stabilized values: {result.get_history('stabilized_value')[:5]}...")
    
    derivative = sim.compute_derivative(result, "psi_signal")
    print(f"∂ψ/∂t = {derivative} (should be 0 for constant)")
    
    integral = sim.compute_integral(result, "psi_signal")
    print(f"∫ψ dt = {integral:.2f} (should be ~{5.0 * 10})")
    print()


def demo_increasing_system():
    """Demonstrate a system that increases over time"""
    print("=" * 60)
    print("DEMO 2: Increasing System")
    print("=" * 60)
    
    sim = TimeSteppingSimulator()
    result = sim.run_dynamic(
        initial_psi=1.0, initial_phi=1.0, initial_epsilon=0.0,
        psi_delta=0.5, phi_delta=0.0, epsilon_delta=0.0,
        num_steps=10
    )
    
    psi_history = result.get_history("psi_signal")
    print(f"ψ evolved: {psi_history[0]:.1f} → {psi_history[-1]:.1f}")
    
    derivative = sim.compute_derivative(result, "psi_signal")
    print(f"∂ψ/∂t = {derivative} (should be 0.5)")
    
    integral = sim.compute_integral(result, "psi_signal")
    print(f"∫ψ dt = {integral:.2f}")
    print()


def demo_predictive_safety():
    """Demonstrate predictive safety through drift monitoring"""
    print("=" * 60)
    print("DEMO 3: Predictive Safety")
    print("=" * 60)
    
    sim = TimeSteppingSimulator()
    result = sim.run_dynamic(
        initial_psi=5.0, initial_phi=3.0, initial_epsilon=0.1,
        psi_delta=0.0, phi_delta=0.0, epsilon_delta=0.05,
        num_steps=15
    )
    
    epsilon_history = result.get_history("epsilon_drift")
    print(f"ε evolved: {epsilon_history[0]:.2f} → {epsilon_history[-1]:.2f}")
    
    drift_derivative = sim.compute_derivative(result, "epsilon_drift")
    print(f"∂ε/∂t = {drift_derivative:.3f}")
    
    if drift_derivative > 0.01:
        print("⚠️  WARNING: Drift is increasing! System trending towards danger.")
    else:
        print("✓ System is stable")
    
    stabilized_history = result.get_history("stabilized_value")
    print(f"Σ evolved: {stabilized_history[0]:.2f} → {stabilized_history[-1]:.2f}")
    print("Note: As ε increases, Σ decreases (homeostatic safety)")
    print()


def demo_memory_and_learning():
    """Demonstrate memory through state history"""
    print("=" * 60)
    print("DEMO 4: Memory and Learning")
    print("=" * 60)
    
    sim = TimeSteppingSimulator()
    result = sim.run_dynamic(
        initial_psi=1.0, initial_phi=1.0, initial_epsilon=0.1,
        psi_delta=0.2, phi_delta=0.1, epsilon_delta=-0.01,
        num_steps=20
    )
    
    psi_history = result.get_history("psi_signal")
    print(f"Memory: Can access all {len(psi_history)} past states")
    print(f"Past (t=0): ψ={psi_history[0]:.2f}")
    print(f"Present (t={len(psi_history)-1}): ψ={psi_history[-1]:.2f}")
    print(f"Change: Δψ = {psi_history[-1] - psi_history[0]:.2f}")
    print(f"Learning: System improved by {((psi_history[-1] / psi_history[0]) - 1) * 100:.1f}%")
    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "HARMONIA-DSL v2.0 DEMONSTRATION" + " " * 16 + "║")
    print("║" + " " * 15 + "Time & Dynamics" + " " * 28 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    demo_constant_system()
    demo_increasing_system()
    demo_predictive_safety()
    demo_memory_and_learning()
    
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("✅ Time-stepping: Execute programs over discrete time")
    print("✅ State history: Complete temporal record")
    print("✅ Derivative (∂): Monitor rates of change")
    print("✅ Integral (∫): Calculate accumulated values")
    print("✅ Predictive safety: Detect danger before it happens")
    print("✅ Memory & learning: Access and compare past states")
    print()
    print("This demonstrates the core concepts of v2.0.")
    print("Full integration with the interpreter is the next step.")
    print()
