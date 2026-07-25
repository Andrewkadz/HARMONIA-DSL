"""
HARMONIA-DSL v5.0: Intentional Action Module

This module implements the F(P) * V term from the Grand Harmonic Equation,
enabling goal-directed behavior and mathematical free will.

Components:
- V (Velocity) operator: Calculates current rate of change
- P (Probability) operator: Evaluates future state desirability
- F(P) force function: Converts belief into motivating force
- APPLY_FORCE command: Applies intentional momentum to state

Author: Manus AI
Date: January 1, 2026
Version: 5.0
"""

import math
from typing import Dict, List, Tuple, Optional


class FutureState:
    """Represents a potential future state for goal-seeking."""
    
    def __init__(self, psi: float, phi: float, epsilon: float):
        self.psi = psi
        self.phi = phi
        self.epsilon = epsilon
    
    def __repr__(self):
        return f"FutureState(Ψ={self.psi}, Φ={self.phi}, ε={self.epsilon})"


class VelocityCalculator:
    """Calculates the velocity (rate of change) of system state."""
    
    @staticmethod
    def calculate_velocity(history: List[Dict[str, float]], 
                          dt: float = 1.0) -> Dict[str, float]:
        """
        Calculate velocity as the first derivative of state variables.
        
        Args:
            history: List of state dictionaries with 'psi', 'phi', 'epsilon'
            dt: Time step size
            
        Returns:
            Dictionary with velocity components: 'v_psi', 'v_phi', 'v_epsilon'
        """
        if len(history) < 2:
            return {'v_psi': 0.0, 'v_phi': 0.0, 'v_epsilon': 0.0}
        
        current = history[-1]
        previous = history[-2]
        
        v_psi = (current['psi'] - previous['psi']) / dt
        v_phi = (current['phi'] - previous['phi']) / dt
        v_epsilon = (current['epsilon'] - previous['epsilon']) / dt
        
        return {
            'v_psi': v_psi,
            'v_phi': v_phi,
            'v_epsilon': v_epsilon
        }
    
    @staticmethod
    def velocity_magnitude(velocity: Dict[str, float]) -> float:
        """Calculate the magnitude of the velocity vector."""
        return math.sqrt(
            velocity['v_psi']**2 + 
            velocity['v_phi']**2 + 
            velocity['v_epsilon']**2
        )


class ProbabilityCalculator:
    """Calculates the probability (belief) in a future state."""
    
    def __init__(self, alpha: float = 0.5, sigma_max: float = 20.0):
        """
        Initialize the probability calculator.
        
        Args:
            alpha: Balance between harmony (0.0) and accessibility (1.0)
            sigma_max: Maximum possible stabilized output
        """
        self.alpha = alpha
        self.sigma_max = sigma_max
    
    def calculate_probability(self, 
                            current_state: Dict[str, float],
                            future_state: FutureState) -> float:
        """
        Calculate P(future_state) based on harmony and accessibility.
        
        P = (1 - α) * (Σ_future / Σ_max) + α * (1 - distance / distance_max)
        
        Args:
            current_state: Current state with 'psi', 'phi', 'epsilon'
            future_state: Target future state
            
        Returns:
            Probability value between 0 and 1
        """
        # Calculate harmony of future state
        sigma_future = (future_state.psi + future_state.phi) * (1 - future_state.epsilon)
        harmony_score = max(0.0, min(1.0, sigma_future / self.sigma_max))
        
        # Calculate accessibility (inverse of distance)
        distance = self._calculate_distance(current_state, future_state)
        distance_max = self._estimate_max_distance()
        accessibility_score = 1.0 - min(1.0, distance / distance_max)
        
        # Weighted combination
        probability = (1 - self.alpha) * harmony_score + self.alpha * accessibility_score
        
        return max(0.0, min(1.0, probability))
    
    def _calculate_distance(self, 
                           current: Dict[str, float], 
                           future: FutureState) -> float:
        """Calculate Euclidean distance between current and future states."""
        delta_psi = future.psi - current['psi']
        delta_phi = future.phi - current['phi']
        delta_epsilon = future.epsilon - current['epsilon']
        
        return math.sqrt(delta_psi**2 + delta_phi**2 + delta_epsilon**2)
    
    def _estimate_max_distance(self) -> float:
        """Estimate maximum possible distance in state space."""
        # Assuming state variables range from 0 to 20
        return math.sqrt(20**2 + 20**2 + 1**2)


class ForceFunction:
    """Converts probability (belief) into motivating force."""
    
    def __init__(self, k: float = 10.0, threshold: float = 0.5):
        """
        Initialize the force function.
        
        Args:
            k: Steepness parameter (higher = more decisive)
            threshold: Probability threshold for significant action
        """
        self.k = k
        self.threshold = threshold
    
    def calculate_force(self, probability: float) -> float:
        """
        Calculate force using sigmoid function.
        
        F(P) = 1 / (1 + e^(-k * (P - threshold)))
        
        Args:
            probability: Belief value between 0 and 1
            
        Returns:
            Force value between 0 and 1
        """
        exponent = -self.k * (probability - self.threshold)
        force = 1.0 / (1.0 + math.exp(exponent))
        return force


class IntentionalActionEngine:
    """Main engine for intentional action (F(P) * V term)."""
    
    def __init__(self, 
                 alpha: float = 0.5,
                 k: float = 10.0,
                 threshold: float = 0.5,
                 force_scale: float = 0.1):
        """
        Initialize the intentional action engine.
        
        Args:
            alpha: Balance between harmony and accessibility in P
            k: Steepness of force function
            threshold: Probability threshold for action
            force_scale: Scaling factor for applied force
        """
        self.velocity_calc = VelocityCalculator()
        self.probability_calc = ProbabilityCalculator(alpha=alpha)
        self.force_func = ForceFunction(k=k, threshold=threshold)
        self.force_scale = force_scale
    
    def apply_intentional_force(self,
                               current_state: Dict[str, float],
                               history: List[Dict[str, float]],
                               goal: FutureState) -> Dict[str, float]:
        """
        Apply the F(P) * V intentional momentum to the current state.
        
        Args:
            current_state: Current state dictionary
            history: State history for velocity calculation
            goal: Target future state
            
        Returns:
            New state after applying intentional force
        """
        # Calculate velocity
        velocity = self.velocity_calc.calculate_velocity(history)
        
        # Calculate probability of goal
        probability = self.probability_calc.calculate_probability(current_state, goal)
        
        # Calculate force
        force = self.force_func.calculate_force(probability)
        
        # Calculate direction towards goal
        direction = self._calculate_direction(current_state, goal)
        
        # Apply F(P) * V (scaled)
        new_state = {
            'psi': current_state['psi'] + self.force_scale * force * direction['d_psi'],
            'phi': current_state['phi'] + self.force_scale * force * direction['d_phi'],
            'epsilon': current_state['epsilon'] + self.force_scale * force * direction['d_epsilon']
        }
        
        # Ensure epsilon stays in valid range [0, 1]
        new_state['epsilon'] = max(0.0, min(1.0, new_state['epsilon']))
        
        return new_state
    
    def _calculate_direction(self, 
                            current: Dict[str, float], 
                            goal: FutureState) -> Dict[str, float]:
        """Calculate normalized direction vector towards goal."""
        delta_psi = goal.psi - current['psi']
        delta_phi = goal.phi - current['phi']
        delta_epsilon = goal.epsilon - current['epsilon']
        
        magnitude = math.sqrt(delta_psi**2 + delta_phi**2 + delta_epsilon**2)
        
        if magnitude < 1e-6:
            return {'d_psi': 0.0, 'd_phi': 0.0, 'd_epsilon': 0.0}
        
        return {
            'd_psi': delta_psi / magnitude,
            'd_phi': delta_phi / magnitude,
            'd_epsilon': delta_epsilon / magnitude
        }


# Convenience functions for demonstration
def demonstrate_velocity():
    """Demonstrate the V (Velocity) operator."""
    print("=" * 60)
    print("DEMO: V (Velocity) Operator")
    print("=" * 60)
    
    history = [
        {'psi': 5.0, 'phi': 5.0, 'epsilon': 0.2},
        {'psi': 5.5, 'phi': 5.3, 'epsilon': 0.18},
        {'psi': 6.2, 'phi': 5.8, 'epsilon': 0.15},
    ]
    
    calc = VelocityCalculator()
    velocity = calc.calculate_velocity(history)
    magnitude = calc.velocity_magnitude(velocity)
    
    print(f"\nState History:")
    for i, state in enumerate(history):
        print(f"  t={i}: Ψ={state['psi']:.1f}, Φ={state['phi']:.1f}, ε={state['epsilon']:.2f}")
    
    print(f"\nCalculated Velocity:")
    print(f"  dΨ/dt = {velocity['v_psi']:.2f}")
    print(f"  dΦ/dt = {velocity['v_phi']:.2f}")
    print(f"  dε/dt = {velocity['v_epsilon']:.2f}")
    print(f"  |V| = {magnitude:.2f}")
    print()


def demonstrate_probability():
    """Demonstrate the P (Probability) operator."""
    print("=" * 60)
    print("DEMO: P (Probability) Operator")
    print("=" * 60)
    
    current = {'psi': 5.0, 'phi': 5.0, 'epsilon': 0.3}
    
    goals = [
        FutureState(10.0, 10.0, 0.1),  # Harmonious and achievable
        FutureState(15.0, 15.0, 0.05), # Very harmonious but distant
        FutureState(2.0, 2.0, 0.8),    # Close but disharmonious
    ]
    
    calc = ProbabilityCalculator(alpha=0.5)
    
    print(f"\nCurrent State: Ψ={current['psi']}, Φ={current['phi']}, ε={current['epsilon']}")
    print(f"\nEvaluating Goals:")
    
    for i, goal in enumerate(goals, 1):
        prob = calc.calculate_probability(current, goal)
        print(f"\n  Goal {i}: {goal}")
        print(f"  P(Goal {i}) = {prob:.3f}")
    print()


def demonstrate_intentional_action():
    """Demonstrate the complete F(P) * V system."""
    print("=" * 60)
    print("DEMO: Complete Intentional Action (F(P) * V)")
    print("=" * 60)
    
    engine = IntentionalActionEngine(force_scale=0.5)
    
    # Initial state
    history = [
        {'psi': 3.0, 'phi': 3.0, 'epsilon': 0.4},
        {'psi': 3.2, 'phi': 3.1, 'epsilon': 0.38},
    ]
    
    current = {'psi': 3.5, 'phi': 3.3, 'epsilon': 0.35}
    goal = FutureState(8.0, 8.0, 0.1)
    
    print(f"\nCurrent State: Ψ={current['psi']}, Φ={current['phi']}, ε={current['epsilon']}")
    print(f"Goal State: {goal}")
    
    print(f"\nApplying Intentional Force for 10 steps:")
    
    for step in range(10):
        history.append(current.copy())
        new_state = engine.apply_intentional_force(current, history, goal)
        
        # Apply homeostatic stabilization
        sigma = (new_state['psi'] + new_state['phi']) * (1 - new_state['epsilon'])
        
        print(f"  Step {step+1}: Ψ={new_state['psi']:.2f}, Φ={new_state['phi']:.2f}, ε={new_state['epsilon']:.3f}, Σ={sigma:.2f}")
        
        current = new_state
    
    print(f"\nFinal State: Ψ={current['psi']:.2f}, Φ={current['phi']:.2f}, ε={current['epsilon']:.3f}")
    print(f"Distance to Goal: {math.sqrt((goal.psi - current['psi'])**2 + (goal.phi - current['phi'])**2):.2f}")
    print()


if __name__ == "__main__":
    demonstrate_velocity()
    demonstrate_probability()
    demonstrate_intentional_action()
