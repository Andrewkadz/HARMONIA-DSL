"""Test suite for HARMONIA-DSL v2.0 Time & Dynamics

This test suite validates the TimeSteppingInterpreter and the new
calculus operators (∂ and ∫).
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

import pytest
from time_stepping_interpreter import (
    TimeSteppingInterpreter,
    TimeSteppingContext,
    run_time_stepping
)
from phi_pi_e_interpreter import FieldContext, RecursiveState


class TestTimeSteppingBasics:
    """Test basic time-stepping functionality"""
    
    def test_single_step_execution(self):
        """Test that a program executes for a single time step"""
        program = "Φ 5 3 0.1"  # Simple stabilization
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=1)
        
        assert result.current_time == 0
        assert result.num_steps == 1
        assert len(result.history["psi_signal"]) == 1
    
    def test_multiple_steps_execution(self):
        """Test that a program executes for multiple time steps"""
        program = "Φ 5 3 0.1"
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=10)
        
        assert result.num_steps == 10
        assert len(result.history["psi_signal"]) == 10
        assert len(result.history["phi_state"]) == 10
        assert len(result.history["epsilon_drift"]) == 10
    
    def test_history_recording(self):
        """Test that state history is recorded correctly"""
        program = "Φ 5 3 0.1"
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=5)
        
        # Check that history contains values
        psi_history = result.get_history("psi_signal")
        assert len(psi_history) == 5
        
        # All values should be the same (static program)
        assert all(v == psi_history[0] for v in psi_history)
    
    def test_history_maxlen(self):
        """Test that history respects maximum length"""
        program = "Φ 5 3 0.1"
        
        interpreter = TimeSteppingInterpreter(history_maxlen=10)
        result = interpreter.run(program, num_steps=20)
        
        # History should be capped at maxlen
        assert len(result.history["psi_signal"]) == 10


class TestDerivativeOperator:
    """Test the partial derivative operator (∂)"""
    
    def test_derivative_with_constant_signal(self):
        """Test derivative of a constant signal (should be 0)"""
        program = """
        Φ 5 3 0.1
        ∂ psi_signal
        """
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=5)
        
        # Derivative of constant should be 0
        derivative = interpreter.compute_derivative(result, "psi_signal")
        assert derivative == 0.0
    
    def test_derivative_with_increasing_signal(self):
        """Test derivative of an increasing signal"""
        # Create a program that increases psi_signal each step
        program = """
        Φ 5 3 0.1
        Ψ 1
        """  # Ψ adds to psi_signal
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=5)
        
        # Derivative should be positive
        derivative = interpreter.compute_derivative(result, "psi_signal")
        assert derivative > 0
    
    def test_derivative_insufficient_history(self):
        """Test derivative with insufficient history"""
        program = "Φ 5 3 0.1"
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=1)
        
        # Should return 0 when history < 2
        derivative = interpreter.compute_derivative(result, "psi_signal")
        assert derivative == 0.0


class TestIntegralOperator:
    """Test the time integral operator (∫)"""
    
    def test_integral_of_constant(self):
        """Test integral of a constant value"""
        program = "Φ 5 3 0.1"  # psi_signal = 5
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=10)
        
        # Integral of constant c over n steps ≈ c * n (with trapezoidal rule)
        integral = interpreter.compute_integral(result, "psi_signal")
        
        # Should be approximately 5 * 10 = 50
        assert 45 < integral < 55  # Allow some numerical error
    
    def test_integral_with_window(self):
        """Test integral with a specified window size"""
        program = "Φ 5 3 0.1"
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=20)
        
        # Integrate over last 5 steps only
        integral = interpreter.compute_integral(result, "psi_signal", window_size=5)
        
        # Should be approximately 5 * 5 = 25
        assert 20 < integral < 30
    
    def test_integral_insufficient_history(self):
        """Test integral with insufficient history"""
        program = "Φ 5 3 0.1"
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=1)
        
        # Should return 0 when history < 2
        integral = interpreter.compute_integral(result, "psi_signal")
        assert integral == 0.0


class TestDynamicPrograms:
    """Test programs that demonstrate dynamic behavior"""
    
    def test_oscillating_system(self):
        """Test a system that oscillates over time"""
        # Program that alternates between two states
        program = """
        Φ 5 3 0.1
        Ψ 1
        Λ -1
        """
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=20)
        
        # Check that values change over time
        psi_history = result.get_history("psi_signal")
        assert len(set(psi_history)) > 1  # Not all the same
    
    def test_accumulation_over_time(self):
        """Test a system that accumulates value over time"""
        program = """
        Φ 1 1 0.0
        Ψ 0.1
        """  # Add 0.1 to psi_signal each step
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=10)
        
        # psi_signal should increase over time
        psi_history = result.get_history("psi_signal")
        assert psi_history[-1] > psi_history[0]
    
    def test_stabilization_over_time(self):
        """Test that a system stabilizes over time"""
        program = """
        Φ 10 5 0.5
        Σ
        """  # High initial drift, should stabilize
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=20)
        
        # Stabilized value should be computed
        stabilized_history = result.get_history("stabilized_value")
        assert len(stabilized_history) == 20
        assert all(v >= 0 for v in stabilized_history)


class TestPredictiveSafety:
    """Test predictive safety using derivatives"""
    
    def test_detect_increasing_drift(self):
        """Test detection of increasing drift (trending towards danger)"""
        program = """
        Φ 5 3 0.1
        ε 0.05
        """  # Increase drift each step
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=10)
        
        # Derivative of epsilon_drift should be positive
        drift_derivative = interpreter.compute_derivative(result, "epsilon_drift")
        assert drift_derivative > 0  # System is trending towards danger
    
    def test_detect_stabilizing_system(self):
        """Test detection of a stabilizing system"""
        program = """
        Φ 5 3 0.5
        Σ
        """  # Start with high drift, stabilize
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=10)
        
        # Check that stabilized_value is computed
        stabilized_history = result.get_history("stabilized_value")
        assert len(stabilized_history) == 10


class TestMemoryAndLearning:
    """Test memory and learning capabilities enabled by history"""
    
    def test_access_past_states(self):
        """Test that we can access past states"""
        program = "Φ 5 3 0.1"
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=10)
        
        # We should be able to access any past state
        for i in range(10):
            history = result.get_history("psi_signal")
            assert len(history) == 10
    
    def test_compare_current_to_past(self):
        """Test comparing current state to past states"""
        program = """
        Φ 5 3 0.1
        Ψ 0.5
        """
        
        interpreter = TimeSteppingInterpreter()
        result = interpreter.run(program, num_steps=10)
        
        history = result.get_history("psi_signal")
        current = history[-1]
        past = history[0]
        
        # Current should differ from past
        assert current != past


class TestConvenienceFunctions:
    """Test convenience functions"""
    
    def test_run_time_stepping_function(self):
        """Test the convenience function"""
        program = "Φ 5 3 0.1"
        
        result = run_time_stepping(program, num_steps=5)
        
        assert result.num_steps == 5
        assert len(result.history["psi_signal"]) == 5


# Run all tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
