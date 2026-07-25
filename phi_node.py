"""
ΦπεNode - Backward-compatible wrapper for Phi-Coder-AI integration

This module provides a Python API that matches Phi-Coder-AI's ΦπεNode interface
while using HARMONIA-DSL operators internally.
"""

from phi_pi_e_interpreter import PhiPiEInterpreterFixed, FieldContext, RecursiveState
from typing import Optional


class ΦπεNode:
    """
    Symbolic harmonic recursion node (Phi-Coder-AI compatible)
    
    Provides backward compatibility with Phi-Coder-AI's ΦπεNode class
    while using HARMONIA-DSL operators internally.
    
    Example:
        >>> node = ΦπεNode(ψ_signal=2.0, φ_state=3.0, ε_drift=0.1)
        >>> result = node.stabilize()
        >>> print(result)  # 4.5
    """
    
    def __init__(self, ψ_signal: float, φ_state: float, ε_drift: float):
        """
        Initialize a ΦπεNode
        
        Args:
            ψ_signal: Recursive animation signal (psi)
            φ_state: Harmonic equilibrium state (phi)
            ε_drift: Incremental drift/error (epsilon)
        """
        self.ψ = ψ_signal
        self.φ = φ_state
        self.ε = ε_drift
        
        # Internal HARMONIA interpreter
        self._interpreter = PhiPiEInterpreterFixed()
        self._context = FieldContext()
        
        # Set initial state
        self._context.state.psi_signal = ψ_signal
        self._context.state.phi_state = φ_state
        self._context.state.epsilon_drift = ε_drift
    
    def stabilize(self) -> float:
        """
        Perform stabilization: (ψ + φ) * (1 - ε)
        
        Returns:
            Stabilized value
        """
        # Execute Σ operator to perform stabilization
        self._interpreter.coexist(None, self._context)
        
        # Return the result
        return self._context.state.stabilized_value
    
    def update(self, ψ_signal: Optional[float] = None, 
               φ_state: Optional[float] = None, 
               ε_drift: Optional[float] = None) -> None:
        """
        Update node parameters
        
        Args:
            ψ_signal: New psi signal (optional)
            φ_state: New phi state (optional)
            ε_drift: New epsilon drift (optional)
        """
        if ψ_signal is not None:
            self.ψ = ψ_signal
            self._context.state.psi_signal = ψ_signal
        
        if φ_state is not None:
            self.φ = φ_state
            self._context.state.phi_state = φ_state
        
        if ε_drift is not None:
            self.ε = ε_drift
            self._context.state.epsilon_drift = ε_drift
    
    def get_state(self) -> dict:
        """
        Get current node state
        
        Returns:
            Dictionary with current ψ, φ, ε values
        """
        return {
            'ψ': self.ψ,
            'φ': self.φ,
            'ε': self.ε,
            'stabilized': self._context.state.stabilized_value
        }
    
    def __repr__(self) -> str:
        return f"ΦπεNode(ψ={self.ψ}, φ={self.φ}, ε={self.ε})"


class ΞΛΩStack:
    """
    Emergent recursion stack with harmonic merging
    
    Provides backward compatibility with Phi-Coder-AI's ΞΛΩStack class
    while using HARMONIA-DSL operators internally.
    
    Example:
        >>> stack = ΞΛΩStack()
        >>> stack.push("A")
        >>> stack.push("B")
        >>> stack.push("C")
        >>> stack.recurse()
        >>> print(stack.peek())  # "[Ξ][Ξ]A⟴B[Ω]⟴C[Ω]"
    """
    
    def __init__(self):
        """Initialize an empty stack"""
        self.stack = []
        self._interpreter = PhiPiEInterpreterFixed()
        self._context = FieldContext()
    
    def push(self, symbol: str) -> None:
        """
        Push a symbol onto the stack
        
        Args:
            symbol: Symbol to push
        """
        self.stack.append(symbol)
        
        # Execute Ξ operator (emergence)
        self._interpreter.emerge(None, self._context)
    
    def pop(self) -> Optional[str]:
        """
        Pop a symbol from the stack
        
        Returns:
            Popped symbol, or None if stack is empty
        """
        if self.stack:
            symbol = self.stack.pop()
            
            # Execute Ω operator (closure)
            self._interpreter.close(None, self._context)
            
            return symbol
        return None
    
    def peek(self) -> Optional[str]:
        """
        Peek at the top of the stack without popping
        
        Returns:
            Top symbol, or None if stack is empty
        """
        return self.stack[-1] if self.stack else None
    
    def recurse(self) -> None:
        """
        Recursively merge stack elements using harmonic merging
        
        Pops pairs of elements and merges them until only one remains.
        """
        while len(self.stack) > 1:
            a = self.stack.pop()
            b = self.stack.pop()
            merged = self.harmonic_merge(a, b)
            self.stack.append(merged)
            
            # Execute Λ operator (illumination) during merge
            self._interpreter.illuminate(None, self._context)
    
    def harmonic_merge(self, a: str, b: str) -> str:
        """
        Merge two symbols harmonically
        
        Args:
            a: First symbol
            b: Second symbol
            
        Returns:
            Merged symbol in format "[Ξ]a⟴b[Ω]"
        """
        return f"[Ξ]{a}⟴{b}[Ω]"
    
    def size(self) -> int:
        """
        Get the current stack size
        
        Returns:
            Number of elements in the stack
        """
        return len(self.stack)
    
    def is_empty(self) -> bool:
        """
        Check if the stack is empty
        
        Returns:
            True if stack is empty, False otherwise
        """
        return len(self.stack) == 0
    
    def clear(self) -> None:
        """Clear all elements from the stack"""
        self.stack.clear()
        
        # Execute Ω operator (closure)
        self._interpreter.close(None, self._context)
    
    def __repr__(self) -> str:
        return f"ΞΛΩStack(size={len(self.stack)})"


class ΨΛΩLoop:
    """
    Recursive animation loop with golden ratio dampening
    
    Provides backward compatibility with Phi-Coder-AI's ΨΛΩLoop class
    while using HARMONIA-DSL operators internally.
    
    Uses golden ratio (φ ≈ 0.618) for harmonic dampening.
    
    Example:
        >>> loop = ΨΛΩLoop()
        >>> result1 = loop.iterate(10.0)  # 3.82
        >>> result2 = loop.iterate(5.0)   # 4.27
        >>> result3 = loop.iterate(2.0)   # 3.40
    """
    
    # Golden ratio for harmonic dampening
    PHI = 0.618033988749895  # (√5 - 1) / 2
    
    def __init__(self):
        """Initialize the loop with zero output"""
        self.output = 0.0
        self._interpreter = PhiPiEInterpreterFixed()
        self._context = FieldContext()
    
    def iterate(self, input_val: float) -> float:
        """
        Perform one iteration of the loop
        
        Applies golden ratio dampening:
        output = (output * φ) + (input * (1 - φ))
        
        Where φ ≈ 0.618 (golden ratio)
        
        Args:
            input_val: Input value for this iteration
            
        Returns:
            New output value
        """
        # Execute Ψ operator (pulse/animation)
        self._context.charge = input_val
        self._interpreter.pulse(None, self._context)
        
        # Apply golden ratio dampening
        self.output = (self.output * self.PHI) + (input_val * (1 - self.PHI))
        
        # Execute Λ operator (illumination)
        self._interpreter.illuminate(None, self._context)
        
        # Execute Ω operator (closure)
        self._interpreter.close(None, self._context)
        
        return self.output
    
    def reset(self) -> None:
        """Reset the loop output to zero"""
        self.output = 0.0
        self._context = FieldContext()
    
    def get_output(self) -> float:
        """
        Get the current output value
        
        Returns:
            Current output
        """
        return self.output
    
    def __repr__(self) -> str:
        return f"ΨΛΩLoop(output={self.output:.4f})"


# Backward compatibility aliases
PhiPiEpsilonNode = ΦπεNode
XiLambdaOmegaStack = ΞΛΩStack
PsiLambdaOmegaLoop = ΨΛΩLoop
