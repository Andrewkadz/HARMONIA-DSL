"""
HARMONIA-DSL v3.0: Nonlinear Operators

This module implements the three nonlinear operators for v3.0:
- exp- (Exponential Decay)
- tanh (Hyperbolic Tangent)  
- ^2 (Resonance)

These operators enable modeling of complex, nonlinear dynamics including
feedback loops, saturation effects, and emergent behavior.
"""

import math
from typing import Any


class NonlinearOperators:
    """Mixin class providing nonlinear operators for v3.0"""
    
    def exponential_decay(self, field: Any, context: Any, 
                         variable_name: str, decay_rate: float, dt: float = 1.0) -> Any:
        """
        exp- (Exponential Decay): Nonlinear Dampening Operator
        
        Applies exponential decay to a state variable, modeling natural dampening,
        forgetting, and return to baseline.
        
        Formula: variable_new = variable_old * e^(-decay_rate * dt)
        
        This operator is essential for modeling:
        - Memory decay and forgetting
        - Natural dampening of oscillations
        - Return to equilibrium states
        - Cooling and thermal dissipation
        
        Args:
            field: The field being operated on
            context: The field context
            variable_name: Name of the variable to decay ("psi", "phi", or "epsilon")
            decay_rate: Rate of decay (positive float)
            dt: Time step (default: 1.0)
        
        Returns:
            The field (unchanged)
        """
        # Get the current value of the variable
        if variable_name == "psi":
            current_value = context.state.psi_signal
        elif variable_name == "phi":
            current_value = context.state.phi_state
        elif variable_name == "epsilon":
            current_value = context.state.epsilon_drift
        else:
            raise ValueError(f"Unknown variable: {variable_name}")
        
        # Apply exponential decay
        new_value = current_value * math.exp(-decay_rate * dt)
        
        # Update the variable
        if variable_name == "psi":
            context.state.psi_signal = new_value
        elif variable_name == "phi":
            context.state.phi_state = new_value
        elif variable_name == "epsilon":
            context.state.epsilon_drift = new_value
        
        return field
    
    def hyperbolic_tangent(self, field: Any, context: Any, 
                          variable_name: str, scale_factor: float = 1.0) -> Any:
        """
        tanh (Hyperbolic Tangent): Saturation Operator
        
        Applies the hyperbolic tangent function to a state variable, modeling
        saturation, diminishing returns, and soft thresholds.
        
        Formula: variable_new = scale_factor * tanh(variable_old)
        
        The tanh function naturally maps any input to a value between -1 and 1,
        creating a soft saturation effect. This operator is essential for:
        - Preventing runaway positive feedback loops
        - Modeling neural activation functions
        - Creating soft boundaries and limits
        - Modeling diminishing returns
        
        Args:
            field: The field being operated on
            context: The field context
            variable_name: Name of the variable to saturate ("psi", "phi", or "epsilon")
            scale_factor: Scaling factor for the output (default: 1.0)
        
        Returns:
            The field (unchanged)
        """
        # Get the current value of the variable
        if variable_name == "psi":
            current_value = context.state.psi_signal
        elif variable_name == "phi":
            current_value = context.state.phi_state
        elif variable_name == "epsilon":
            current_value = context.state.epsilon_drift
        else:
            raise ValueError(f"Unknown variable: {variable_name}")
        
        # Apply hyperbolic tangent
        new_value = scale_factor * math.tanh(current_value)
        
        # Update the variable
        if variable_name == "psi":
            context.state.psi_signal = new_value
        elif variable_name == "phi":
            context.state.phi_state = new_value
        elif variable_name == "epsilon":
            context.state.epsilon_drift = new_value
        
        return field
    
    def resonance(self, field: Any, context: Any, variable_name: str) -> Any:
        """
        ^2 (Resonance): Amplification Operator
        
        Squares a state variable, modeling amplified interactions, feedback loops,
        and explosive growth.
        
        Formula: variable_new = variable_old ^ 2
        
        This is the simplest but most powerful nonlinear operator. It creates
        positive feedback loops where the output is proportional to the square
        of the input. This operator is essential for:
        - Modeling viral spread and exponential growth
        - Creating feedback loops and resonance effects
        - Amplifying small signals
        - Modeling complex, emergent behavior
        
        WARNING: This operator can lead to explosive growth. It should typically
        be combined with the tanh operator to prevent runaway behavior.
        
        Args:
            field: The field being operated on
            context: The field context
            variable_name: Name of the variable to square ("psi", "phi", or "epsilon")
        
        Returns:
            The field (unchanged)
        """
        # Get the current value of the variable
        if variable_name == "psi":
            current_value = context.state.psi_signal
        elif variable_name == "phi":
            current_value = context.state.phi_state
        elif variable_name == "epsilon":
            current_value = context.state.epsilon_drift
        else:
            raise ValueError(f"Unknown variable: {variable_name}")
        
        # Apply resonance (squaring)
        # Preserve the sign by using sign(x) * x^2
        sign = 1 if current_value >= 0 else -1
        new_value = sign * (current_value ** 2)
        
        # Update the variable
        if variable_name == "psi":
            context.state.psi_signal = new_value
        elif variable_name == "phi":
            context.state.phi_state = new_value
        elif variable_name == "epsilon":
            context.state.epsilon_drift = new_value
        
        return field
