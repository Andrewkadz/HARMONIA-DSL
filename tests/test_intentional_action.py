"""
Tests for HARMONIA-DSL v5.0: Intentional Action

Tests the P (Probability), V (Velocity), and F(P) * V components.
"""

import pytest
import math
import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from intentional_action import (
    FutureState,
    VelocityCalculator,
    ProbabilityCalculator,
    ForceFunction,
    IntentionalActionEngine
)


class TestFutureState:
    """Test the FutureState class."""
    
    def test_future_state_creation(self):
        """Test creating a future state."""
        state = FutureState(10.0, 8.0, 0.1)
        assert state.psi == 10.0
        assert state.phi == 8.0
        assert state.epsilon == 0.1
    
    def test_future_state_repr(self):
        """Test future state string representation."""
        state = FutureState(5.0, 5.0, 0.2)
        assert "Ψ=5.0" in str(state)
        assert "Φ=5.0" in str(state)
        assert "ε=0.2" in str(state)


class TestVelocityCalculator:
    """Test the V (Velocity) operator."""
    
    def test_velocity_with_no_history(self):
        """Test velocity calculation with insufficient history."""
        calc = VelocityCalculator()
        history = [{'psi': 5.0, 'phi': 5.0, 'epsilon': 0.2}]
        velocity = calc.calculate_velocity(history)
        
        assert velocity['v_psi'] == 0.0
        assert velocity['v_phi'] == 0.0
        assert velocity['v_epsilon'] == 0.0
    
    def test_velocity_increasing(self):
        """Test velocity calculation with increasing state."""
        calc = VelocityCalculator()
        history = [
            {'psi': 5.0, 'phi': 5.0, 'epsilon': 0.2},
            {'psi': 6.0, 'phi': 6.0, 'epsilon': 0.3},
        ]
        velocity = calc.calculate_velocity(history)
        
        assert velocity['v_psi'] == 1.0
        assert velocity['v_phi'] == 1.0
        assert abs(velocity['v_epsilon'] - 0.1) < 0.01
    
    def test_velocity_decreasing(self):
        """Test velocity calculation with decreasing state."""
        calc = VelocityCalculator()
        history = [
            {'psi': 10.0, 'phi': 10.0, 'epsilon': 0.5},
            {'psi': 8.0, 'phi': 9.0, 'epsilon': 0.3},
        ]
        velocity = calc.calculate_velocity(history)
        
        assert velocity['v_psi'] == -2.0
        assert velocity['v_phi'] == -1.0
        assert velocity['v_epsilon'] == -0.2
    
    def test_velocity_magnitude(self):
        """Test velocity magnitude calculation."""
        calc = VelocityCalculator()
        velocity = {'v_psi': 3.0, 'v_phi': 4.0, 'v_epsilon': 0.0}
        magnitude = calc.velocity_magnitude(velocity)
        
        assert abs(magnitude - 5.0) < 0.01


class TestProbabilityCalculator:
    """Test the P (Probability) operator."""
    
    def test_probability_harmonious_close_goal(self):
        """Test probability for a harmonious and close goal."""
        calc = ProbabilityCalculator(alpha=0.5)
        current = {'psi': 5.0, 'phi': 5.0, 'epsilon': 0.3}
        goal = FutureState(7.0, 7.0, 0.2)
        
        prob = calc.calculate_probability(current, goal)
        
        # Should be high (both harmonious and close)
        assert prob > 0.7
    
    def test_probability_harmonious_distant_goal(self):
        """Test probability for a harmonious but distant goal."""
        calc = ProbabilityCalculator(alpha=0.5)
        current = {'psi': 2.0, 'phi': 2.0, 'epsilon': 0.5}
        goal = FutureState(15.0, 15.0, 0.05)
        
        prob = calc.calculate_probability(current, goal)
        
        # Should be moderate (harmonious but distant)
        assert 0.4 < prob < 0.8
    
    def test_probability_disharmonious_goal(self):
        """Test probability for a disharmonious goal."""
        calc = ProbabilityCalculator(alpha=0.5)
        current = {'psi': 10.0, 'phi': 10.0, 'epsilon': 0.1}
        goal = FutureState(3.0, 3.0, 0.9)
        
        prob = calc.calculate_probability(current, goal)
        
        # Should be low (disharmonious)
        assert prob < 0.5
    
    def test_probability_range(self):
        """Test that probability is always in [0, 1]."""
        calc = ProbabilityCalculator(alpha=0.5)
        current = {'psi': 5.0, 'phi': 5.0, 'epsilon': 0.3}
        
        goals = [
            FutureState(0.0, 0.0, 1.0),
            FutureState(10.0, 10.0, 0.0),
            FutureState(20.0, 20.0, 0.0),
        ]
        
        for goal in goals:
            prob = calc.calculate_probability(current, goal)
            assert 0.0 <= prob <= 1.0


class TestForceFunction:
    """Test the F(P) force function."""
    
    def test_force_low_probability(self):
        """Test force with low probability."""
        func = ForceFunction(k=10.0, threshold=0.5)
        force = func.calculate_force(0.1)
        
        # Should be low
        assert force < 0.2
    
    def test_force_high_probability(self):
        """Test force with high probability."""
        func = ForceFunction(k=10.0, threshold=0.5)
        force = func.calculate_force(0.9)
        
        # Should be high
        assert force > 0.8
    
    def test_force_threshold(self):
        """Test force at threshold."""
        func = ForceFunction(k=10.0, threshold=0.5)
        force = func.calculate_force(0.5)
        
        # Should be around 0.5
        assert abs(force - 0.5) < 0.1
    
    def test_force_range(self):
        """Test that force is always in [0, 1]."""
        func = ForceFunction(k=10.0, threshold=0.5)
        
        for prob in [0.0, 0.25, 0.5, 0.75, 1.0]:
            force = func.calculate_force(prob)
            assert 0.0 <= force <= 1.0


class TestIntentionalActionEngine:
    """Test the complete F(P) * V system."""
    
    def test_goal_seeking_moves_towards_goal(self):
        """Test that intentional action moves state towards goal."""
        engine = IntentionalActionEngine(force_scale=0.5)
        
        history = [
            {'psi': 3.0, 'phi': 3.0, 'epsilon': 0.4},
            {'psi': 3.1, 'phi': 3.1, 'epsilon': 0.39},
        ]
        current = {'psi': 3.2, 'phi': 3.2, 'epsilon': 0.38}
        goal = FutureState(8.0, 8.0, 0.1)
        
        new_state = engine.apply_intentional_force(current, history, goal)
        
        # Should move closer to goal
        assert new_state['psi'] > current['psi']
        assert new_state['phi'] > current['phi']
        assert new_state['epsilon'] < current['epsilon']
    
    def test_goal_seeking_improves_harmony(self):
        """Test that seeking a harmonious goal improves harmony."""
        engine = IntentionalActionEngine(force_scale=0.3)
        
        history = [
            {'psi': 2.0, 'phi': 2.0, 'epsilon': 0.6},
            {'psi': 2.1, 'phi': 2.1, 'epsilon': 0.58},
        ]
        current = {'psi': 2.2, 'phi': 2.2, 'epsilon': 0.56}
        goal = FutureState(10.0, 10.0, 0.05)
        
        sigma_before = (current['psi'] + current['phi']) * (1 - current['epsilon'])
        
        new_state = engine.apply_intentional_force(current, history, goal)
        sigma_after = (new_state['psi'] + new_state['phi']) * (1 - new_state['epsilon'])
        
        # Harmony should improve
        assert sigma_after > sigma_before
    
    def test_epsilon_stays_in_range(self):
        """Test that epsilon stays in [0, 1]."""
        engine = IntentionalActionEngine(force_scale=1.0)
        
        history = [
            {'psi': 5.0, 'phi': 5.0, 'epsilon': 0.05},
            {'psi': 5.1, 'phi': 5.1, 'epsilon': 0.04},
        ]
        current = {'psi': 5.2, 'phi': 5.2, 'epsilon': 0.03}
        goal = FutureState(10.0, 10.0, 0.0)
        
        new_state = engine.apply_intentional_force(current, history, goal)
        
        assert 0.0 <= new_state['epsilon'] <= 1.0
    
    def test_convergence_to_goal(self):
        """Test that repeated application converges towards goal."""
        engine = IntentionalActionEngine(force_scale=0.5)
        
        history = [
            {'psi': 3.0, 'phi': 3.0, 'epsilon': 0.4},
            {'psi': 3.1, 'phi': 3.1, 'epsilon': 0.39},
        ]
        current = {'psi': 3.2, 'phi': 3.2, 'epsilon': 0.38}
        goal = FutureState(6.0, 6.0, 0.2)
        
        initial_distance = math.sqrt(
            (goal.psi - current['psi'])**2 + 
            (goal.phi - current['phi'])**2
        )
        
        # Apply force multiple times
        for _ in range(5):
            history.append(current.copy())
            current = engine.apply_intentional_force(current, history, goal)
        
        final_distance = math.sqrt(
            (goal.psi - current['psi'])**2 + 
            (goal.phi - current['phi'])**2
        )
        
        # Should be closer to goal
        assert final_distance < initial_distance


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
