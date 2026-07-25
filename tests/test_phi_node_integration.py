"""
Unit tests for ΦπεNode integration in HARMONIA-DSL

Tests the integration of Phi-Coder-AI's ΦπεNode logic into HARMONIA operators.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phi_pi_e_interpreter import PhiPiEInterpreterFixed, FieldContext, RecursiveState


class TestRecursiveStateExtension:
    """Test that RecursiveState has been extended with ΦπεNode fields"""
    
    def test_state_has_psi_signal(self):
        """Test that RecursiveState has psi_signal field"""
        state = RecursiveState()
        assert hasattr(state, 'psi_signal')
        assert state.psi_signal == 0.0
    
    def test_state_has_phi_state(self):
        """Test that RecursiveState has phi_state field"""
        state = RecursiveState()
        assert hasattr(state, 'phi_state')
        assert state.phi_state == 0.0
    
    def test_state_has_epsilon_drift(self):
        """Test that RecursiveState has epsilon_drift field"""
        state = RecursiveState()
        assert hasattr(state, 'epsilon_drift')
        assert state.epsilon_drift == 0.0
    
    def test_state_has_stabilized_value(self):
        """Test that RecursiveState has stabilized_value field"""
        state = RecursiveState()
        assert hasattr(state, 'stabilized_value')
        assert state.stabilized_value == 0.0
    
    def test_state_fields_are_mutable(self):
        """Test that ΦπεNode fields can be modified"""
        state = RecursiveState()
        state.psi_signal = 2.0
        state.phi_state = 3.0
        state.epsilon_drift = 0.1
        state.stabilized_value = 4.5
        
        assert state.psi_signal == 2.0
        assert state.phi_state == 3.0
        assert state.epsilon_drift == 0.1
        assert state.stabilized_value == 4.5


class TestPsiOperator:
    """Test Ψ (Psi) operator sets psi_signal"""
    
    def test_psi_sets_psi_signal(self):
        """Test that Ψ operator sets psi_signal from charge"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        context.charge = 5.0
        
        # Execute Ψ operator
        interpreter.pulse(None, context)
        
        # Verify psi_signal was set
        assert context.state.psi_signal == 5.0
    
    def test_psi_with_zero_charge(self):
        """Test Ψ operator with zero charge"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        context.charge = 0.0
        
        interpreter.pulse(None, context)
        
        assert context.state.psi_signal == 0.0
    
    def test_psi_with_negative_charge(self):
        """Test Ψ operator with negative charge"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        context.charge = -2.5
        
        interpreter.pulse(None, context)
        
        assert context.state.psi_signal == -2.5


class TestPhiOperator:
    """Test Φ (Phi) operator sets phi_state"""
    
    def test_phi_sets_phi_state(self):
        """Test that Φ operator sets phi_state from tension"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        context.tension.strength = 0.3
        
        # Execute Φ operator
        interpreter.stabilize(None, context)
        
        # phi_state = 1.0 - tension.strength
        # After stabilize, tension is reduced by 0.1, so: 1.0 - 0.2 = 0.8
        expected_phi_state = 1.0 - max(0, 0.3 - 0.1)
        assert abs(context.state.phi_state - expected_phi_state) < 1e-6
    
    def test_phi_with_zero_tension(self):
        """Test Φ operator with zero tension"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        context.tension.strength = 0.0
        
        interpreter.stabilize(None, context)
        
        # phi_state = 1.0 - 0.0 = 1.0
        assert abs(context.state.phi_state - 1.0) < 1e-6
    
    def test_phi_with_high_tension(self):
        """Test Φ operator with high tension"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        context.tension.strength = 0.8
        
        interpreter.stabilize(None, context)
        
        # tension after stabilize: 0.8 - 0.1 = 0.7
        # phi_state = 1.0 - 0.7 = 0.3
        expected_phi_state = 1.0 - 0.7
        assert abs(context.state.phi_state - expected_phi_state) < 1e-6


class TestEpsilonOperator:
    """Test ε (epsilon) operator sets epsilon_drift"""
    
    def test_epsilon_sets_epsilon_drift(self):
        """Test that ε operator sets epsilon_drift from depth"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        context.depth = 3
        
        # Execute ε operator
        interpreter.micro_ignite(None, context)
        
        # epsilon_drift = 0.1 * depth = 0.1 * 3 = 0.3
        assert abs(context.state.epsilon_drift - 0.3) < 1e-6
    
    def test_epsilon_with_zero_depth(self):
        """Test ε operator with zero depth"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        context.depth = 0
        
        interpreter.micro_ignite(None, context)
        
        assert context.state.epsilon_drift == 0.0
    
    def test_epsilon_with_large_depth(self):
        """Test ε operator with large depth"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        context.depth = 10
        
        interpreter.micro_ignite(None, context)
        
        # epsilon_drift = 0.1 * 10 = 1.0
        assert abs(context.state.epsilon_drift - 1.0) < 1e-6


class TestSigmaStabilization:
    """Test Σ (Sigma) operator performs ΦπεNode stabilization"""
    
    def test_sigma_basic_stabilization(self):
        """Test Σ performs (ψ + φ) * (1 - ε)"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        # Set ΦπεNode fields
        context.state.psi_signal = 2.0
        context.state.phi_state = 3.0
        context.state.epsilon_drift = 0.1
        
        # Execute Σ operator
        interpreter.coexist(None, context)
        
        # Expected: (2.0 + 3.0) * (1 - 0.1) = 5.0 * 0.9 = 4.5
        expected = (2.0 + 3.0) * (1 - 0.1)
        assert abs(context.state.stabilized_value - expected) < 1e-6
    
    def test_sigma_zero_drift(self):
        """Test Σ with zero drift (no dampening)"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.psi_signal = 2.0
        context.state.phi_state = 3.0
        context.state.epsilon_drift = 0.0
        
        interpreter.coexist(None, context)
        
        # Expected: (2.0 + 3.0) * (1 - 0.0) = 5.0
        expected = 2.0 + 3.0
        assert abs(context.state.stabilized_value - expected) < 1e-6
    
    def test_sigma_full_drift(self):
        """Test Σ with full drift (complete dampening)"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.psi_signal = 2.0
        context.state.phi_state = 3.0
        context.state.epsilon_drift = 1.0
        
        interpreter.coexist(None, context)
        
        # Expected: (2.0 + 3.0) * (1 - 1.0) = 0.0
        assert abs(context.state.stabilized_value - 0.0) < 1e-6
    
    def test_sigma_negative_values(self):
        """Test Σ with negative psi and phi"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.psi_signal = -2.0
        context.state.phi_state = 3.0
        context.state.epsilon_drift = 0.1
        
        interpreter.coexist(None, context)
        
        # Expected: (-2.0 + 3.0) * (1 - 0.1) = 1.0 * 0.9 = 0.9
        expected = (-2.0 + 3.0) * (1 - 0.1)
        assert abs(context.state.stabilized_value - expected) < 1e-6
    
    def test_sigma_large_values(self):
        """Test Σ with large values"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.psi_signal = 100.0
        context.state.phi_state = 200.0
        context.state.epsilon_drift = 0.2
        
        interpreter.coexist(None, context)
        
        # Expected: (100.0 + 200.0) * (1 - 0.2) = 300.0 * 0.8 = 240.0
        expected = (100.0 + 200.0) * (1 - 0.2)
        assert abs(context.state.stabilized_value - expected) < 1e-6


class TestFullStabilizationWorkflow:
    """Test complete ΦπεNode stabilization workflow using multiple operators"""
    
    def test_epsilon_psi_phi_sigma_sequence(self):
        """Test ε → Ψ → Φ → Σ operator sequence"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        # Set initial state
        context.depth = 2
        context.charge = 5.0
        context.tension.strength = 0.4
        
        # Execute ε (sets epsilon_drift)
        interpreter.micro_ignite(None, context)
        
        # Execute Ψ (sets psi_signal)
        interpreter.pulse(None, context)
        
        # Execute Φ (sets phi_state)
        interpreter.stabilize(None, context)
        
        # Execute Σ (performs stabilization)
        interpreter.coexist(None, context)
        
        # Verify intermediate values
        assert abs(context.state.epsilon_drift - 0.2) < 1e-6  # 0.1 * 2
        assert abs(context.state.psi_signal - 5.0) < 1e-6
        # phi_state = 1.0 - (0.4 - 0.1) = 0.7
        assert abs(context.state.phi_state - 0.7) < 1e-6
        
        # Verify final stabilized value
        # (5.0 + 0.7) * (1 - 0.2) = 5.7 * 0.8 = 4.56
        expected = (5.0 + 0.7) * (1 - 0.2)
        assert abs(context.state.stabilized_value - expected) < 1e-6
    
    def test_direct_value_setting(self):
        """Test directly setting ΦπεNode values and stabilizing"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        # Directly set values (simulating external input)
        context.state.psi_signal = 10.0
        context.state.phi_state = 15.0
        context.state.epsilon_drift = 0.05
        
        # Execute Σ
        interpreter.coexist(None, context)
        
        # Expected: (10.0 + 15.0) * (1 - 0.05) = 25.0 * 0.95 = 23.75
        expected = (10.0 + 15.0) * (1 - 0.05)
        assert abs(context.state.stabilized_value - expected) < 1e-6
    
    def test_multiple_stabilizations(self):
        """Test multiple stabilization cycles"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        # First stabilization
        context.state.psi_signal = 1.0
        context.state.phi_state = 2.0
        context.state.epsilon_drift = 0.1
        interpreter.coexist(None, context)
        
        result1 = context.state.stabilized_value
        expected1 = (1.0 + 2.0) * (1 - 0.1)
        assert abs(result1 - expected1) < 1e-6
        
        # Second stabilization with different values
        context.state.psi_signal = 3.0
        context.state.phi_state = 4.0
        context.state.epsilon_drift = 0.2
        interpreter.coexist(None, context)
        
        result2 = context.state.stabilized_value
        expected2 = (3.0 + 4.0) * (1 - 0.2)
        assert abs(result2 - expected2) < 1e-6
        
        # Verify results are different
        assert abs(result1 - result2) > 1e-6


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_all_zeros(self):
        """Test stabilization with all zero values"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.psi_signal = 0.0
        context.state.phi_state = 0.0
        context.state.epsilon_drift = 0.0
        
        interpreter.coexist(None, context)
        
        assert context.state.stabilized_value == 0.0
    
    def test_epsilon_greater_than_one(self):
        """Test stabilization with epsilon > 1 (over-dampening)"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.psi_signal = 5.0
        context.state.phi_state = 10.0
        context.state.epsilon_drift = 1.5
        
        interpreter.coexist(None, context)
        
        # Expected: (5.0 + 10.0) * (1 - 1.5) = 15.0 * (-0.5) = -7.5
        expected = (5.0 + 10.0) * (1 - 1.5)
        assert abs(context.state.stabilized_value - expected) < 1e-6
    
    def test_very_small_values(self):
        """Test stabilization with very small values"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.psi_signal = 1e-10
        context.state.phi_state = 1e-10
        context.state.epsilon_drift = 1e-10
        
        interpreter.coexist(None, context)
        
        expected = (1e-10 + 1e-10) * (1 - 1e-10)
        assert abs(context.state.stabilized_value - expected) < 1e-15


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
