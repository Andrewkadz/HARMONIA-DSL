"""HARMONIA-DSL v2.0: Time-Stepping Interpreter

This module implements the TimeSteppingInterpreter, which wraps the core
PhiPiEInterpreterFixed to enable discrete time simulation and dynamic behavior.

This is the critical upgrade that transforms HARMONIA-DSL from a static,
algebraic model to a dynamic, calculus-based model capable of simulating
the evolution of harmonic intelligence over time.

Mathematical foundations: /theory/V2_TIME_DYNAMICS_FORMALIZATION.md
"""

from typing import List, Dict, Any, Optional
from collections import deque
from dataclasses import dataclass, field
from phi_pi_e_interpreter import PhiPiEInterpreterFixed, FieldContext, RecursiveState
import copy


@dataclass
class TimeSteppingContext:
    """Extended context for time-stepping simulation.
    
    This maintains a history of state variables over time.
    """
    # Time tracking
    current_time: int = 0
    num_steps: int = 0
    
    # State history (time series of all state variables)
    history_maxlen: int = 1000
    history: Dict[str, deque] = field(default_factory=dict)
    
    # Derivative and integral values (computed by ∂ and ∫ operators)
    derivative_value: float = 0.0
    integral_value: float = 0.0
    
    # Latest state values (captured from interpreter output)
    latest_psi: float = 0.0
    latest_phi: float = 0.0
    latest_epsilon: float = 0.0
    latest_stabilized: float = 0.0
    
    def __post_init__(self):
        """Initialize history deques for all tracked variables."""
        if not self.history:
            self.history = {
                "psi_signal": deque(maxlen=self.history_maxlen),
                "phi_state": deque(maxlen=self.history_maxlen),
                "epsilon_drift": deque(maxlen=self.history_maxlen),
                "stabilized_value": deque(maxlen=self.history_maxlen),
            }
    
    def update_history(self, psi: float, phi: float, epsilon: float, stabilized: float):
        """Record the current state into the history.
        
        Args:
            psi: Current psi_signal value
            phi: Current phi_state value
            epsilon: Current epsilon_drift value
            stabilized: Current stabilized_value
        """
        self.history["psi_signal"].append(psi)
        self.history["phi_state"].append(phi)
        self.history["epsilon_drift"].append(epsilon)
        self.history["stabilized_value"].append(stabilized)
        
        self.latest_psi = psi
        self.latest_phi = phi
        self.latest_epsilon = epsilon
        self.latest_stabilized = stabilized
    
    def get_history(self, variable_name: str) -> List[float]:
        """Get the complete history of a variable as a list.
        
        Args:
            variable_name: Name of the variable (e.g., "psi_signal")
        
        Returns:
            List of historical values, ordered from oldest to newest
        """
        if variable_name not in self.history:
            return []
        return list(self.history[variable_name])
    
    def get_current_value(self, variable_name: str) -> float:
        """Get the current value of a state variable.
        
        Args:
            variable_name: Name of the variable
        
        Returns:
            Current value of the variable
        """
        variable_map = {
            "psi_signal": self.latest_psi,
            "phi_state": self.latest_phi,
            "epsilon_drift": self.latest_epsilon,
            "stabilized_value": self.latest_stabilized,
        }
        
        return variable_map.get(variable_name, 0.0)


class TimeSteppingInterpreter:
    """Interpreter for time-stepping simulation of HARMONIA-DSL programs.
    
    This interpreter wraps the core PhiPiEInterpreterFixed and executes it
    repeatedly over discrete time steps, maintaining a history of all
    state variables.
    
    This enables:
    - Dynamic simulation of system evolution
    - Calculus operators (∂ and ∫)
    - Memory and learning (access to past states)
    - Predictive safety (monitoring rates of change)
    - Formal verification (long-term stability analysis)
    """
    
    def __init__(self, history_maxlen: int = 1000):
        """Initialize the time-stepping interpreter.
        
        Args:
            history_maxlen: Maximum length of state history to maintain
        """
        self.history_maxlen = history_maxlen
    
    def run(self, program: str, num_steps: int, 
            initial_psi: float = 0.0, initial_phi: float = 0.0,
            initial_epsilon: float = 0.0) -> TimeSteppingContext:
        """Execute a HARMONIA-DSL program over multiple time steps.
        
        Args:
            program: The HARMONIA-DSL program to execute
            num_steps: Number of discrete time steps to simulate
            initial_psi: Initial psi_signal value
            initial_phi: Initial phi_state value
            initial_epsilon: Initial epsilon_drift value
        
        Returns:
            TimeSteppingContext containing the final state and complete history
        """
        # Initialize context
        ts_context = TimeSteppingContext(history_maxlen=self.history_maxlen)
        ts_context.num_steps = num_steps
        
        # Track state across time steps
        current_psi = initial_psi
        current_phi = initial_phi
        current_epsilon = initial_epsilon
        current_stabilized = 0.0
        
        # Time-stepping loop
        for t in range(num_steps):
            ts_context.current_time = t
            
            # Create a new interpreter for this time step
            interpreter = PhiPiEInterpreterFixed()
            
            # Execute the program (silently - suppress debug output)
            import sys
            from io import StringIO
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            try:
                result = interpreter.execute(program)
            finally:
                sys.stdout = old_stdout
            
            # Extract state from the interpreter's context
            # The interpreter creates a context internally
            if hasattr(interpreter, 'fields') and 'context' in interpreter.fields:
                context = interpreter.fields['context']
                if hasattr(context, 'state'):
                    current_psi = context.state.psi_signal
                    current_phi = context.state.phi_state
                    current_epsilon = context.state.epsilon_drift
                    current_stabilized = context.state.stabilized_value
            
            # Record the state into history
            ts_context.update_history(current_psi, current_phi, current_epsilon, current_stabilized)
        
        return ts_context
    
    def run_file(self, filename: str, num_steps: int) -> TimeSteppingContext:
        """Execute a HARMONIA-DSL file over multiple time steps.
        
        Args:
            filename: Path to the .hrm file
            num_steps: Number of discrete time steps to simulate
        
        Returns:
            TimeSteppingContext containing the final state and complete history
        """
        with open(filename, 'r', encoding='utf-8') as f:
            program = f.read()
        
        return self.run(program, num_steps)
    
    def compute_derivative(self, ts_context: TimeSteppingContext, 
                          variable_name: str) -> float:
        """Compute the discrete derivative (rate of change) of a variable.
        
        Uses backward difference: ∂S/∂t ≈ S(t) - S(t-1)
        
        Args:
            ts_context: The time-stepping context with history
            variable_name: Name of the variable to differentiate
        
        Returns:
            The derivative (rate of change) at the current time
        """
        history = ts_context.get_history(variable_name)
        
        if len(history) < 2:
            return 0.0  # Not enough history to compute derivative
        
        # Backward difference: current value - previous value
        return history[-1] - history[-2]
    
    def compute_integral(self, ts_context: TimeSteppingContext,
                        variable_name: str, window_size: Optional[int] = None) -> float:
        """Compute the discrete integral (accumulated value) of a variable.
        
        Uses trapezoidal rule for numerical integration.
        
        Args:
            ts_context: The time-stepping context with history
            variable_name: Name of the variable to integrate
            window_size: Number of time steps to integrate over (None = all history)
        
        Returns:
            The integral (accumulated value) over the specified window
        """
        history = ts_context.get_history(variable_name)
        
        if len(history) < 2:
            return 0.0  # Not enough history to compute integral
        
        # Determine the window
        if window_size is None or window_size > len(history):
            window = history
        else:
            window = history[-window_size:]
        
        # Trapezoidal rule: sum of averages of consecutive pairs
        integral = 0.0
        for i in range(len(window) - 1):
            integral += (window[i] + window[i + 1]) / 2.0
        
        return integral


# Convenience function for quick time-stepping execution
def run_time_stepping(program: str, num_steps: int, 
                     history_maxlen: int = 1000) -> TimeSteppingContext:
    """Convenience function to run a program with time-stepping.
    
    Args:
        program: The HARMONIA-DSL program
        num_steps: Number of time steps to simulate
        history_maxlen: Maximum history length
    
    Returns:
        TimeSteppingContext with results
    """
    interpreter = TimeSteppingInterpreter(history_maxlen=history_maxlen)
    return interpreter.run(program, num_steps)
