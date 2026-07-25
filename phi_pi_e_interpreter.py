"""HARMONIA-DSL Interpreter

This interpreter implements the core stabilization formula derived from
the Grand Harmonic Equation (R):

    R = [ lim ( ΨΩ → ∞ ) ] * { ( Ξ / Λc ) * [ ( 1 - ∂Ω / ∂Ψ ) ] }  
          +  Σ [ Θn ]  
          +  { F(P) * V }  
          +  [ ΔΩ(T) / S ]  
          +  { Ψ± * K }  
          +  ({ Φ * β })  
          +  [ Cξ / Eψ ]  
          +  { Γ ( ΨΩ, F(P), ΔΩ ) }

The current implementation (v1.0) focuses on the core stabilization:
    Σ = (Ψ + Φ) * (1 - ε)

For the complete theoretical foundations, see /theory/RI1_GRANDHARMONICEQUATION.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Union, Optional, Set
import math
import numpy as np
from collections import defaultdict, deque
from enum import Enum
import uuid

@dataclass
class FieldTension:
    """Represents the tension between recursive fields"""
    strength: float = 0.0
    phase: float = 0.0
    charge: float = 0.0
    
    def __add__(self, other: 'FieldTension') -> 'FieldTension':
        return FieldTension(
            strength=self.strength + other.strength,
            phase=(self.phase + other.phase) / 2,
            charge=self.charge + other.charge
        )
    
    def __sub__(self, other: 'FieldTension') -> 'FieldTension':
        return FieldTension(
            strength=self.strength - other.strength,
            phase=(self.phase - other.phase) / 2,
            charge=self.charge - other.charge
        )

@dataclass
class RecursiveState:
    """Represents a recursive state in the field"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    depth: int = 0
    parent: Optional[str] = None
    children: Set[str] = field(default_factory=set)
    tension: FieldTension = field(default_factory=FieldTension)
    phase: float = 0.0
    charge: float = 0.0
    
    # ΦπεNode fields (for Phi-Coder-AI integration)
    psi_signal: float = 0.0      # ψ: Recursive animation signal
    phi_state: float = 0.0        # φ: Harmonic equilibrium state
    epsilon_drift: float = 0.0    # ε: Incremental drift/error
    stabilized_value: float = 0.0 # Result of stabilization
    
    def add_child(self, child_id: str) -> None:
        self.children.add(child_id)
    
    def remove_child(self, child_id: str) -> None:
        self.children.discard(child_id)

@dataclass
class FieldContext:
    """Context for field evaluation"""
    state: RecursiveState
    tension: FieldTension
    phase: float
    charge: float
    depth: int
    
    def __init__(self, state: Optional[RecursiveState] = None):
        if state is None:
            state = RecursiveState()
        self.state = state
        self.tension = state.tension
        self.phase = state.phase
        self.charge = state.charge
        self.depth = state.depth

    def fork(self) -> 'FieldContext':
        """Create a new context with increased depth"""
        new_state = RecursiveState(
            parent=self.state.id,
            depth=self.depth + 1,
            tension=self.tension,
            phase=self.phase,
            charge=self.charge
        )
        self.state.add_child(new_state.id)
        return FieldContext(new_state)

    def merge(self, other: 'FieldContext') -> None:
        """Merge another context into this one"""
        self.tension = self.tension + other.tension
        self.phase = (self.phase + other.phase) / 2
        self.charge = self.charge + other.charge

class PhiPiEInterpreterFixed:
    def __init__(self):
        self.fields: Dict[str, Any] = {}
        self.symbols = {
            'Φ': self.stabilize,         # Harmonic Equilibrium
            'Π': self.transcend,         # Transcendent Continuity
            'Ε': self.ignite,           # Ignition / Initiation
            'ε': self.micro_ignite,     # Micro-Ignition
            'Δ': self.fuse,             # Fusion / Transformation
            'δ': self.micro_transform,  # Micro-Transformation
            'Ψ': self.pulse,            # Oscillation / Recursive Pulse
            'Λ': self.illuminate,       # Structural Illumination
            'λ': self.entangle,         # Entanglement
            'Γ': self.grow,             # Recursive Growth
            'Ω': self.close,            # Closure
            'ω': self.will_force,       # Will-Force
            'Σ': self.coexist,          # Coexistence
            'Ξ': self.emerge,           # Emergent System
            'ζ': self.recurrence,       # Recurrence Pattern
            'Τ': self.synchronize,      # Synchronization
            'Ρ': self.perceive,         # Perception Modulation
            'Θ': self.intend,           # Intention
            'η': self.index,            # Index / Parameter
            'χ': self.measure,          # Measurement
            'n': self.index,            # Index (alternative)
            # Grok's operators (added Dec 31, 2025)
            'Κ': self.probe,            # Query Probe (Kappa)
            'Υ': self.consensus_merge,  # Consensus Merge (Upsilon)
            'Β': self.reflection_echo   # Reflection Echo (Beta)
        }
        
        self.operators = {
            '→': self.flow,           # Flow Vector
            '+': self.simultaneity,   # Simultaneity
            ':': self.interact,       # Interaction
            '/': self.disrupt,        # Disruption
            '|': self.orthogonal,     # Orthogonality
            '[]': self.loop,          # Loop
            '=': self.stabilize       # Stabilization
        }

    def clean_input(self, code: str) -> str:
        """Clean and prepare input code for parsing - FIXED VERSION"""
        # Remove // comments properly
        lines = code.splitlines()
        cleaned_lines = []
        for line in lines:
            # Remove everything after //
            if '//' in line:
                line = line.split('//')[0]
            line = line.strip()
            if line:
                cleaned_lines.append(line)
        
        # Join without spaces initially
        code = ''.join(cleaned_lines)
        
        # Remove ASCII_OUTPUT_MODE marker
        code = code.replace('ASCII_OUTPUT_MODE', '').replace('[:ASCII:]', '')
        
        # FIXED: Proper allowed characters including all Greek letters
        allowed_chars = set('ΦΠΕεΔδΨΛλΓΩωΣΞζΤΡΘηχn→+::/|[]=()0123456789., ')
        code = ''.join(c for c in code if c in allowed_chars)
        
        return code

    def tokenize(self, code: str) -> List[str]:
        """Tokenize code into operators - NEW METHOD"""
        tokens = []
        i = 0
        while i < len(code):
            char = code[i]
            
            # Skip whitespace
            if char in ' \t\n\r':
                i += 1
                continue
            
            # Handle brackets as single tokens
            if char == '[':
                # Find matching ]
                depth = 1
                j = i + 1
                while j < len(code) and depth > 0:
                    if code[j] == '[':
                        depth += 1
                    elif code[j] == ']':
                        depth -= 1
                    j += 1
                tokens.append(code[i:j])  # Include brackets
                i = j
            elif char in self.symbols:
                tokens.append(char)
                i += 1
            elif char in self.operators:
                tokens.append(char)
                i += 1
            else:
                # Unknown character, skip
                i += 1
        
        return tokens

    def execute(self, code: str) -> Any:
        """Execute a complete Φπε program - FIXED VERSION"""
        try:
            # Clean input
            cleaned_code = self.clean_input(code)
            print(f"\nCleaned code: {cleaned_code}")
            
            # Tokenize into operators
            tokens = self.tokenize(cleaned_code)
            print(f"Tokens: {tokens}")
            
            # Create initial context
            context = FieldContext()
            current_value = None
            
            # Execute tokens sequentially
            for token in tokens:
                print(f"\nExecuting token: {token}")
                
                if token.startswith('[') and token.endswith(']'):
                    # Handle loop
                    loop_code = token[1:-1]  # Remove brackets
                    current_value = self.execute_loop(loop_code, context)
                elif token in self.symbols:
                    # Execute symbol operator
                    handler = self.symbols[token]
                    current_value = handler(current_value, context)
                elif token in self.operators:
                    # Execute operator (needs special handling for binary ops)
                    handler = self.operators[token]
                    current_value = handler(current_value, context)
                else:
                    print(f"Unknown token: {token}")
            
            return current_value
            
        except Exception as e:
            error_msg = f"Error executing code: {str(e)}"
            print(f"Error details: {error_msg}")
            import traceback
            traceback.print_exc()
            raise RuntimeError(error_msg) from e

    def execute_loop(self, loop_code: str, context: FieldContext) -> Any:
        """Execute code inside a loop"""
        # Execute the loop code multiple times (or until convergence)
        result = None
        for iteration in range(10):  # Max 10 iterations
            result = self.execute(loop_code)
            # Could add convergence check here
        return result

    # ===== OPERATOR IMPLEMENTATIONS =====
    # (All the operator methods from the original, unchanged)
    
    def stabilize(self, field: Any, context: FieldContext) -> Any:
        """Apply harmonic equilibrium to a field"""
        context.tension.strength = max(0, context.tension.strength - 0.1)
        context.phase = (context.phase + math.pi/2) % (2 * math.pi)
        
        # ΦπεNode integration: Set phi_state from stabilized tension
        context.state.phi_state = 1.0 - context.tension.strength
        
        return field

    def transcend(self, field: Any, context: FieldContext) -> Any:
        """Apply transcendent continuity to field"""
        new_context = context.fork()
        new_context.depth += 1
        new_context.phase += math.pi/4
        return field

    def ignite(self, field: Any, context: FieldContext) -> Any:
        """Initiate recursive process"""
        new_context = context.fork()
        new_context.phase = 0
        new_context.charge = 1.0
        return field

    def micro_ignite(self, field: Any, context: FieldContext) -> Any:
        """Activate within a recursion loop"""
        new_context = context.fork()
        new_context.phase += math.pi/8
        new_context.charge *= 0.5
        
        # ΦπεNode integration: Set epsilon_drift based on recursion depth
        context.state.epsilon_drift = 0.1 * context.depth
        
        return field

    def fuse(self, field: Any, context: FieldContext) -> Any:
        """Apply fusion transformation to field"""
        context.tension.strength += 0.5
        context.phase = (context.phase + math.pi/3) % (2 * math.pi)
        return field

    def micro_transform(self, field: Any, context: FieldContext) -> Any:
        """Apply micro-transformation"""
        context.tension.strength += 0.1
        context.phase += math.pi/16
        return field

    def pulse(self, field: Any, context: FieldContext) -> Any:
        """Initiate recursive pulse"""
        new_context = context.fork()
        new_context.phase += math.pi/2
        new_context.charge *= 1.5
        
        # ΦπεNode integration: Set psi_signal from current charge
        context.state.psi_signal = context.charge
        
        return field

    def illuminate(self, field: Any, context: FieldContext) -> Any:
        """Extract structural clarity from field"""
        context.charge *= 2.0
        context.phase += math.pi/4
        return field

    def entangle(self, field: Any, context: FieldContext) -> Any:
        """Create nonlocal binding between fields"""
        context.tension.strength += 1.0
        context.phase = (context.phase + math.pi/4) % (2 * math.pi)
        return field

    def grow(self, field: Any, context: FieldContext) -> Any:
        """Apply recursive growth"""
        new_context = context.fork()
        new_context.phase += math.pi/3
        new_context.charge *= 1.2
        return field

    def close(self, field: Any, context: FieldContext) -> Any:
        """Mark recursive closure"""
        context.tension.strength = 0
        context.phase = 0
        context.charge = 0
        return field

    def will_force(self, field: Any, context: FieldContext) -> Any:
        """Apply autonomous drive"""
        new_context = context.fork()
        new_context.phase += math.pi/2
        new_context.charge *= 1.5
        return field

    def coexist(self, field: Any, context: FieldContext) -> Any:
        """Hold multiple fields in coexistence"""
        context.tension.strength += 0.5
        context.phase = (context.phase + math.pi/6) % (2 * math.pi)
        
        # ΦπεNode integration: Perform stabilization (ψ + φ) * (1 - ε)
        psi = context.state.psi_signal
        phi = context.state.phi_state
        eps = context.state.epsilon_drift
        
        context.state.stabilized_value = (psi + phi) * (1 - eps)
        
        return field

    def emerge(self, field: Any, context: FieldContext) -> Any:
        """Create emergent system"""
        new_context = context.fork()
        new_context.phase += math.pi/4
        new_context.charge *= 1.3
        return field

    def recurrence(self, field: Any, context: FieldContext) -> Any:
        """Create harmonic echo pattern"""
        new_context = context.fork()
        new_context.phase += math.pi/3
        new_context.charge *= 1.2
        return field

    def synchronize(self, field: Any, context: FieldContext) -> Any:
        """Synchronize recursive contexts"""
        context.phase = 0  # Reset to synchronized state
        return field

    def perceive(self, field: Any, context: FieldContext) -> Any:
        """Modulate perception"""
        context.phase += math.pi/8
        return field

    def intend(self, field: Any, context: FieldContext) -> Any:
        """Set intention vector"""
        context.charge = 1.0
        return field

    def index(self, field: Any, context: FieldContext) -> Any:
        """Index or quantify"""
        return field

    def measure(self, field: Any, context: FieldContext) -> Any:
        """Measurement transformation"""
        context.phase = (context.phase + math.pi/4) % (2 * math.pi)
        return field

    def flow(self, field: Any, context: FieldContext) -> Any:
        """Apply directional flow to field"""
        new_context = context.fork()
        new_context.phase += math.pi/6
        new_context.charge *= 1.1
        return field

    def simultaneity(self, field: Any, context: FieldContext) -> Any:
        """Coexistent fields"""
        # For now, just maintain the field
        return field

    def interact(self, field: Any, context: FieldContext) -> Any:
        """Create interaction between fields"""
        context.tension.strength += 0.3
        context.phase = (context.phase + math.pi/8) % (2 * math.pi)
        return field

    def disrupt(self, field: Any, context: FieldContext) -> Any:
        """Create disruption/instability"""
        context.tension.strength += 0.5
        context.phase = (context.phase + math.pi * 0.7) % (2 * math.pi)
        context.charge *= 0.5
        return field

    def orthogonal(self, field: Any, context: FieldContext) -> Any:
        """Create non-interacting fields"""
        context.tension.strength = 0
        context.phase = (context.phase + math.pi/8) % (2 * math.pi)
        return field

    def loop(self, field: Any, context: FieldContext) -> Any:
        """Create recursion memory"""
        new_context = context.fork()
        new_context.phase += math.pi/3
        new_context.charge *= 1.1
        return field

    # ===== GROK'S OPERATORS (Added December 31, 2025) =====
    
    def probe(self, field: Any, context: FieldContext) -> Any:
        """
        Κ (Kappa): Query Probe
        
        Probes a field for relevance/safety, increasing ψ (signal) based on ε (drift).
        Supports consciousness as active inquiry, safety by amplifying drift on unsafe probes,
        coexistence by merging probe results non-destructively.
        
        Implementation: psi_new = psi + (epsilon_drift * factor)
        """
        # Calculate probe factor based on current drift
        factor = 2.0  # Amplification factor for drift
        
        # Increase psi_signal proportional to epsilon_drift
        drift_amplification = context.state.epsilon_drift * factor
        context.state.psi_signal += drift_amplification
        
        # Also update charge to reflect the probe
        context.charge += drift_amplification
        
        # Increase tension slightly to indicate probing activity
        context.tension.strength += 0.2
        
        # Log the probe action
        if hasattr(context, 'probe_count'):
            context.probe_count += 1
        else:
            context.probe_count = 1
        
        return field
    
    def consensus_merge(self, field: Any, context: FieldContext) -> Any:
        """
        Υ (Upsilon): Consensus Merge
        
        Merges multiple states with a harmonic mean, updating φ (tension) for coherence.
        Models coexistence in multi-agent setups, ensures safety by raising ε on high variance,
        reflects consciousness as unified awareness from diverse fields.
        
        Implementation: merged = n / sum(1 / state_i for state_i in states)
        """
        # Collect current state values for harmonic mean
        states = [
            context.state.psi_signal if context.state.psi_signal != 0 else 0.1,
            context.state.phi_state if context.state.phi_state != 0 else 0.1,
            context.charge if context.charge != 0 else 0.1
        ]
        
        # Calculate harmonic mean: n / sum(1/x_i)
        n = len(states)
        harmonic_sum = sum(1.0 / s for s in states if s != 0)
        
        if harmonic_sum > 0:
            merged_value = n / harmonic_sum
        else:
            merged_value = 0.0
        
        # Calculate variance to detect discord
        mean_val = sum(states) / n
        variance = sum((s - mean_val) ** 2 for s in states) / n
        
        # Update phi_state with merged value
        context.state.phi_state = merged_value
        
        # Adjust tension based on variance (high variance = discord)
        context.tension.strength = min(1.0, variance / 10.0)
        
        # Raise epsilon on high variance (safety mechanism)
        if variance > 5.0:
            context.state.epsilon_drift += 0.1
            context.state.epsilon_drift = min(1.0, context.state.epsilon_drift)
        
        return field
    
    def reflection_echo(self, field: Any, context: FieldContext) -> Any:
        """
        Β (Beta): Reflection Echo
        
        Echoes a stabilized value back as a depth increment, simulating self-reflection.
        Captures consciousness as meta-loops, safety via bounds on echo,
        coexistence by echoing shared states.
        
        Implementation: echo = 1 / stabilized_value, then depth += echo (capped)
        """
        # Get current stabilized value
        stabilized = context.state.stabilized_value
        
        # Calculate echo (inverse of stabilized value)
        if stabilized > 0.01:  # Avoid division by very small numbers
            echo = 1.0 / stabilized
        elif stabilized < -0.01:
            echo = 1.0 / abs(stabilized)
        else:
            echo = 10.0  # Cap for near-zero values
        
        # Cap echo to prevent infinities
        echo = min(echo, 10.0)
        echo = max(echo, 0.1)
        
        # Increment depth by echo (simulates self-reflection)
        context.state.depth += int(echo)
        
        # Also update phase to reflect the reflection
        context.phase = (context.phase + echo * math.pi / 4) % (2 * math.pi)
        
        # Reduce tension slightly (reflection brings calm)
        context.tension.strength = max(0, context.tension.strength - 0.1)
        
        return field

    def partial_derivative(self, field: Any, context: FieldContext, variable_name: str = "psi_signal") -> Any:
        """
        ∂ (Partial): Partial Derivative Operator
        
        Computes the discrete derivative (rate of change) of a state variable.
        This operator requires time-stepping to function properly.
        
        Uses backward difference: ∂S/∂t ≈ S(t) - S(t-1)
        
        Implementation:
        - Retrieves the history of the specified variable
        - Computes the difference between current and previous values
        - Stores result in context.derivative_value
        
        This operator enables:
        - Predictive safety (monitoring rates of change)
        - Trend analysis (is the system improving or degrading?)
        - Dynamic adaptation (respond to velocity, not just position)
        
        Args:
            field: The field being operated on
            context: The field context (must have history)
            variable_name: Name of the variable to differentiate (default: "psi_signal")
        
        Returns:
            The field (unchanged)
        """
        # Check if we're in a time-stepping context
        if not hasattr(context, 'history') or variable_name not in context.history:
            # No history available - derivative is 0
            if hasattr(context, 'derivative_value'):
                context.derivative_value = 0.0
            return field
        
        history = context.history[variable_name]
        
        if len(history) < 2:
            # Not enough history to compute derivative
            if hasattr(context, 'derivative_value'):
                context.derivative_value = 0.0
            return field
        
        # Backward difference: current - previous
        derivative = history[-1] - history[-2]
        
        # Store the derivative value in the context
        if hasattr(context, 'derivative_value'):
            context.derivative_value = derivative
        
        # Also update psi_signal with the derivative (for chaining)
        context.state.psi_signal = derivative
        
        return field
    
    def time_integral(self, field: Any, context: FieldContext, 
                     variable_name: str = "psi_signal", window_size: Optional[int] = None) -> Any:
        """
        ∫ (Integral): Time Integral Operator
        
        Computes the discrete integral (accumulated value) of a state variable
        over a specified time window. This operator requires time-stepping.
        
        Uses trapezoidal rule: ∫ S dt ≈ Δt * sum of averages of consecutive pairs
        
        Implementation:
        - Retrieves the history of the specified variable
        - Applies trapezoidal rule over the window
        - Stores result in context.integral_value
        
        This operator enables:
        - Memory and accumulation (total experience over time)
        - Long-term stability analysis (has the system been stable?)
        - Energy calculations (work done over time)
        
        Args:
            field: The field being operated on
            context: The field context (must have history)
            variable_name: Name of the variable to integrate (default: "psi_signal")
            window_size: Number of time steps to integrate over (None = all history)
        
        Returns:
            The field (unchanged)
        """
        # Check if we're in a time-stepping context
        if not hasattr(context, 'history') or variable_name not in context.history:
            # No history available - integral is 0
            if hasattr(context, 'integral_value'):
                context.integral_value = 0.0
            return field
        
        history = list(context.history[variable_name])
        
        if len(history) < 2:
            # Not enough history to compute integral
            if hasattr(context, 'integral_value'):
                context.integral_value = 0.0
            return field
        
        # Determine the window
        if window_size is None or window_size > len(history):
            window = history
        else:
            window = history[-window_size:]
        
        # Trapezoidal rule: sum of averages of consecutive pairs
        integral = 0.0
        for i in range(len(window) - 1):
            integral += (window[i] + window[i + 1]) / 2.0
        
        # Store the integral value in the context
        if hasattr(context, 'integral_value'):
            context.integral_value = integral
        
        # Also update phi_state with the integral (for chaining)
        context.state.phi_state = integral
        
        return field
