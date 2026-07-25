"""
HARMONIA-DSL v6.0: Memory & Learning
Implements the { Ψ± * K } term from the Grand Harmonic Equation

This module provides:
- Ψ- (Psi-minus): Memory recall with exponential decay
- Ψ+ (Psi-plus): Future projection based on learned patterns
- K (Kappa): Knowledge accumulation over time

Author: Manus AI
Date: January 1, 2026
"""

import math
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class State:
    """Represents a system state at a point in time."""
    psi: float
    phi: float
    epsilon: float
    timestamp: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        return {'psi': self.psi, 'phi': self.phi, 'epsilon': self.epsilon}
    
    def __sub__(self, other: 'State') -> 'State':
        """Calculate the difference between two states."""
        return State(
            psi=self.psi - other.psi,
            phi=self.phi - other.phi,
            epsilon=self.epsilon - other.epsilon,
            timestamp=self.timestamp
        )
    
    def __add__(self, other: 'State') -> 'State':
        """Add two states."""
        return State(
            psi=self.psi + other.psi,
            phi=self.phi + other.phi,
            epsilon=self.epsilon + other.epsilon,
            timestamp=self.timestamp
        )
    
    def __mul__(self, scalar: float) -> 'State':
        """Multiply state by a scalar."""
        return State(
            psi=self.psi * scalar,
            phi=self.phi * scalar,
            epsilon=self.epsilon * scalar,
            timestamp=self.timestamp
        )
    
    def magnitude(self) -> float:
        """Calculate the magnitude of the state vector."""
        return math.sqrt(self.psi**2 + self.phi**2 + self.epsilon**2)


class MemoryBuffer:
    """
    Ψ- (Psi-minus): Memory Recall
    
    Stores historical states and provides weighted recall with exponential decay.
    """
    
    def __init__(self, max_depth: int = 50):
        self.max_depth = max_depth
        self.history: List[State] = []
    
    def add(self, state: State):
        """Add a new state to memory."""
        self.history.append(state)
        if len(self.history) > self.max_depth:
            self.history.pop(0)  # Remove oldest
    
    def recall(self, depth: int = 10, decay_rate: float = 0.1) -> Optional[State]:
        """
        Recall past states with exponential decay weighting.
        
        Formula: Ψ-(t) = Σ [w(i) * state(t-i)] for i in [1, depth]
        Where w(i) = exp(-λ * i)
        
        Args:
            depth: How many states back to recall
            decay_rate: Decay constant λ
        
        Returns:
            Weighted average of past states
        """
        if not self.history:
            return None
        
        actual_depth = min(depth, len(self.history))
        
        # Calculate weights
        weights = [math.exp(-decay_rate * i) for i in range(1, actual_depth + 1)]
        total_weight = sum(weights)
        
        # Weighted sum
        recalled = State(psi=0.0, phi=0.0, epsilon=0.0)
        for i, weight in enumerate(weights):
            if i < len(self.history):
                state = self.history[-(i+1)]  # Go backwards
                recalled = recalled + (state * (weight / total_weight))
        
        return recalled
    
    def get_velocity(self) -> Optional[State]:
        """Calculate current velocity from recent history."""
        if len(self.history) < 2:
            return None
        
        current = self.history[-1]
        previous = self.history[-2]
        dt = current.timestamp - previous.timestamp
        
        if dt == 0:
            dt = 1.0  # Assume unit time
        
        velocity = (current - previous) * (1.0 / dt)
        return velocity


class KnowledgeAccumulator:
    """
    K (Kappa): Knowledge Accumulation
    
    Tracks accumulated knowledge over time based on prediction errors.
    """
    
    def __init__(self, learning_rate: float = 0.01, max_knowledge: float = 100.0):
        self.learning_rate = learning_rate
        self.max_knowledge = max_knowledge
        self.knowledge = 0.0
    
    def update(self, current_state: State, recalled_memory: Optional[State]) -> float:
        """
        Update knowledge based on prediction error.
        
        Formula: K(t) = K(t-1) + α * |state(t) - Ψ-(t)|
        
        Args:
            current_state: The actual current state
            recalled_memory: The recalled/predicted state
        
        Returns:
            Updated knowledge value
        """
        if recalled_memory is None:
            # No memory yet, small initial learning
            self.knowledge = min(self.knowledge + self.learning_rate, self.max_knowledge)
            return self.knowledge
        
        # Calculate prediction error
        error = (current_state - recalled_memory).magnitude()
        
        # Update knowledge
        self.knowledge = min(
            self.knowledge + self.learning_rate * error,
            self.max_knowledge
        )
        
        return self.knowledge
    
    def get_knowledge(self) -> float:
        """Get current knowledge value."""
        return self.knowledge
    
    def reset(self):
        """Reset knowledge to zero."""
        self.knowledge = 0.0


class FutureProjector:
    """
    Ψ+ (Psi-plus): Future Projection
    
    Projects future states based on current dynamics and learned patterns.
    """
    
    def __init__(self):
        self.learned_acceleration = State(psi=0.0, phi=0.0, epsilon=0.0)
    
    def learn_acceleration(self, history: List[State]):
        """Learn average acceleration from historical data."""
        if len(history) < 3:
            return
        
        accelerations = []
        for i in range(2, len(history)):
            dt = 1.0  # Assume unit time
            v1 = (history[i-1] - history[i-2]) * (1.0 / dt)
            v2 = (history[i] - history[i-1]) * (1.0 / dt)
            accel = (v2 - v1) * (1.0 / dt)
            accelerations.append(accel)
        
        if accelerations:
            # Average acceleration
            avg_accel = State(psi=0.0, phi=0.0, epsilon=0.0)
            for accel in accelerations:
                avg_accel = avg_accel + accel
            self.learned_acceleration = avg_accel * (1.0 / len(accelerations))
    
    def project(self, current_state: State, velocity: Optional[State], 
                knowledge: float, steps: int = 5) -> List[State]:
        """
        Project future states.
        
        Formula: Ψ+(t+Δt) = state(t) + V(t) * Δt + K * learned_acceleration * Δt²/2
        
        Args:
            current_state: Current state
            velocity: Current velocity
            knowledge: Knowledge factor K
            steps: Number of steps to project
        
        Returns:
            List of projected future states
        """
        if velocity is None:
            velocity = State(psi=0.0, phi=0.0, epsilon=0.0)
        
        projections = []
        state = current_state
        vel = velocity
        
        for step in range(1, steps + 1):
            dt = 1.0  # Unit time step
            
            # Project: state + velocity*dt + 0.5*acceleration*dt²
            accel_term = self.learned_acceleration * (knowledge * 0.5 * dt * dt)
            vel_term = vel * dt
            next_state = state + vel_term + accel_term
            
            projections.append(next_state)
            
            # Update for next iteration
            state = next_state
            vel = vel + (self.learned_acceleration * (knowledge * dt))
        
        return projections


class MemoryLearningEngine:
    """
    Complete Memory & Learning System
    
    Integrates Ψ-, Ψ+, and K into the full { Ψ± * K } term.
    """
    
    def __init__(self, memory_depth: int = 10, decay_rate: float = 0.1,
                 learning_rate: float = 0.01, projection_steps: int = 5):
        self.memory = MemoryBuffer(max_depth=50)
        self.knowledge = KnowledgeAccumulator(learning_rate=learning_rate)
        self.projector = FutureProjector()
        
        self.memory_depth = memory_depth
        self.decay_rate = decay_rate
        self.projection_steps = projection_steps
        
        self.current_psi_minus = None
        self.current_psi_plus = []
    
    def process_state(self, state: State) -> Dict[str, any]:
        """
        Process a new state through the memory-learning system.
        
        Returns:
            Dictionary with Ψ-, Ψ+, K, and the full term
        """
        # Add to memory
        self.memory.add(state)
        
        # Ψ-: Recall past
        self.current_psi_minus = self.memory.recall(
            depth=self.memory_depth,
            decay_rate=self.decay_rate
        )
        
        # K: Update knowledge
        k_value = self.knowledge.update(state, self.current_psi_minus)
        
        # Learn acceleration patterns
        self.projector.learn_acceleration(self.memory.history)
        
        # Ψ+: Project future
        velocity = self.memory.get_velocity()
        self.current_psi_plus = self.projector.project(
            state, velocity, k_value, self.projection_steps
        )
        
        return {
            'psi_minus': self.current_psi_minus,
            'psi_plus': self.current_psi_plus,
            'knowledge': k_value,
            'memory_learning_term': self.get_memory_learning_term()
        }
    
    def get_memory_learning_term(self) -> float:
        """
        Calculate the full { Ψ± * K } term.
        
        Formula: (Ψ- + Ψ+) * K
        
        Returns:
            The memory-learning contribution to system output
        """
        if self.current_psi_minus is None:
            return 0.0
        
        k = self.knowledge.get_knowledge()
        
        # Average Ψ- and Ψ+ contributions
        psi_minus_mag = self.current_psi_minus.magnitude()
        
        if self.current_psi_plus:
            psi_plus_avg = sum(s.magnitude() for s in self.current_psi_plus) / len(self.current_psi_plus)
        else:
            psi_plus_avg = 0.0
        
        # Combined term
        term = (psi_minus_mag + psi_plus_avg) * k
        return term
    
    def apply_to_system(self, sigma_base: float, influence: float = 0.1) -> float:
        """
        Apply memory-learning to base system output.
        
        Formula: Σ_new = Σ_base + α_ML * Memory_Learning_Term
        
        Args:
            sigma_base: Base stabilized output
            influence: Memory-learning influence factor α_ML
        
        Returns:
            Enhanced output with memory-learning
        """
        ml_term = self.get_memory_learning_term()
        return sigma_base + influence * ml_term


# Demo function
if __name__ == "__main__":
    print("=== HARMONIA-DSL v6.0: Memory & Learning Demo ===\n")
    
    engine = MemoryLearningEngine(memory_depth=5, learning_rate=0.05)
    
    print("DEMO: Learning from a pattern of increasing harmony\n")
    
    # Simulate a learning scenario
    for t in range(20):
        # State gradually improves (learning)
        state = State(
            psi=5.0 + t * 0.5,
            phi=5.0 + t * 0.5,
            epsilon=0.5 - t * 0.02,
            timestamp=float(t)
        )
        
        result = engine.process_state(state)
        
        sigma_base = (state.psi + state.phi) * (1 - state.epsilon)
        sigma_enhanced = engine.apply_to_system(sigma_base, influence=0.1)
        
        if t % 5 == 0:
            print(f"Step {t}:")
            print(f"  State: Ψ={state.psi:.1f}, Φ={state.phi:.1f}, ε={state.epsilon:.3f}")
            print(f"  Knowledge K: {result['knowledge']:.2f}")
            print(f"  Σ_base: {sigma_base:.2f}")
            print(f"  Σ_enhanced: {sigma_enhanced:.2f}")
            print(f"  Improvement: {((sigma_enhanced - sigma_base) / sigma_base * 100):.1f}%")
            print()
    
    print("✓ Knowledge accumulated successfully!")
    print("✓ System learned to improve its output over time!")
