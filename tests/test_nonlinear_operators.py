"""
Test suite for HARMONIA-DSL v3.0 Nonlinear Operators

Tests the three new nonlinear operators:
- exp- (Exponential Decay)
- tanh (Hyperbolic Tangent)
- ^2 (Resonance)
"""

import pytest
import sys
import math
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from nonlinear_operators import NonlinearOperators
from dataclasses import dataclass


@dataclass
class TestState:
    """Test state for operators"""
    psi_signal: float = 0.0
    phi_state: float = 0.0
    epsilon_drift: float = 0.0


@dataclass
class TestContext:
    """Test context for operators"""
    state: TestState


class TestOperatorMixin(NonlinearOperators):
    """Test class with nonlinear operators"""
    pass


class TestExponentialDecay:
    """Tests for the exp- (Exponential Decay) operator"""
    
    def test_basic_decay(self):
        """Test basic exponential decay"""
        op = TestOperatorMixin()
        context = TestContext(state=TestState(psi_signal=10.0))
        
        op.exponential_decay(None, context, "psi", decay_rate=0.5, dt=1.0)
        
        expected = 10.0 * math.exp(-0.5)
        assert abs(context.state.psi_signal - expected) < 0.0001
    
    def test_decay_to_zero(self):
        """Test that decay approaches zero"""
        op = TestOperatorMixin()
        context = TestContext(state=TestState(psi_signal=100.0))
        
        for _ in range(50):
            op.exponential_decay(None, context, "psi", decay_rate=0.5, dt=1.0)
        
        assert context.state.psi_signal < 0.01
    
    def test_decay_rate_effect(self):
        """Test that higher decay rate leads to faster decay"""
        op1 = TestOperatorMixin()
        op2 = TestOperatorMixin()
        context1 = TestContext(state=TestState(psi_signal=10.0))
        context2 = TestContext(state=TestState(psi_signal=10.0))
        
        op1.exponential_decay(None, context1, "psi", decay_rate=0.1, dt=1.0)
        op2.exponential_decay(None, context2, "psi", decay_rate=0.5, dt=1.0)
        
        assert context2.state.psi_signal < context1.state.psi_signal
    
    def test_decay_all_variables(self):
        """Test decay on all three variables"""
        op = TestOperatorMixin()
        context = TestContext(state=TestState(psi_signal=10.0, phi_state=8.0, epsilon_drift=0.5))
        
        op.exponential_decay(None, context, "psi", decay_rate=0.3, dt=1.0)
        op.exponential_decay(None, context, "phi", decay_rate=0.3, dt=1.0)
        op.exponential_decay(None, context, "epsilon", decay_rate=0.3, dt=1.0)
        
        assert context.state.psi_signal < 10.0
        assert context.state.phi_state < 8.0
        assert context.state.epsilon_drift < 0.5
    
    def test_decay_with_different_dt(self):
        """Test that dt affects decay rate"""
        op1 = TestOperatorMixin()
        op2 = TestOperatorMixin()
        context1 = TestContext(state=TestState(psi_signal=10.0))
        context2 = TestContext(state=TestState(psi_signal=10.0))
        
        op1.exponential_decay(None, context1, "psi", decay_rate=0.5, dt=1.0)
        op2.exponential_decay(None, context2, "psi", decay_rate=0.5, dt=2.0)
        
        assert context2.state.psi_signal < context1.state.psi_signal


class TestHyperbolicTangent:
    """Tests for the tanh (Hyperbolic Tangent) operator"""
    
    def test_basic_saturation(self):
        """Test basic tanh saturation"""
        op = TestOperatorMixin()
        context = TestContext(state=TestState(psi_signal=1.0))
        
        op.hyperbolic_tangent(None, context, "psi", scale_factor=1.0)
        
        expected = math.tanh(1.0)
        assert abs(context.state.psi_signal - expected) < 0.0001
    
    def test_saturation_bounds(self):
        """Test that tanh saturates between -scale and +scale"""
        op = TestOperatorMixin()
        context = TestContext(state=TestState(psi_signal=100.0))
        
        op.hyperbolic_tangent(None, context, "psi", scale_factor=10.0)
        
        assert context.state.psi_signal <= 10.0
        assert context.state.psi_signal >= -10.0
    
    def test_saturation_symmetry(self):
        """Test that tanh is symmetric around zero"""
        op1 = TestOperatorMixin()
        op2 = TestOperatorMixin()
        context1 = TestContext(state=TestState(psi_signal=5.0))
        context2 = TestContext(state=TestState(psi_signal=-5.0))
        
        op1.hyperbolic_tangent(None, context1, "psi", scale_factor=10.0)
        op2.hyperbolic_tangent(None, context2, "psi", scale_factor=10.0)
        
        assert abs(context1.state.psi_signal + context2.state.psi_signal) < 0.0001
    
    def test_saturation_all_variables(self):
        """Test saturation on all three variables"""
        op = TestOperatorMixin()
        context = TestContext(state=TestState(psi_signal=10.0, phi_state=8.0, epsilon_drift=0.9))
        
        op.hyperbolic_tangent(None, context, "psi", scale_factor=5.0)
        op.hyperbolic_tangent(None, context, "phi", scale_factor=5.0)
        op.hyperbolic_tangent(None, context, "epsilon", scale_factor=0.5)
        
        assert context.state.psi_signal <= 5.0
        assert context.state.phi_state <= 5.0
        assert context.state.epsilon_drift <= 0.5
    
    def test_scale_factor_effect(self):
        """Test that scale factor affects output range"""
        op1 = TestOperatorMixin()
        op2 = TestOperatorMixin()
        context1 = TestContext(state=TestState(psi_signal=10.0))
        context2 = TestContext(state=TestState(psi_signal=10.0))
        
        op1.hyperbolic_tangent(None, context1, "psi", scale_factor=5.0)
        op2.hyperbolic_tangent(None, context2, "psi", scale_factor=10.0)
        
        assert context2.state.psi_signal > context1.state.psi_signal


class TestResonance:
    """Tests for the ^2 (Resonance) operator"""
    
    def test_basic_squaring(self):
        """Test basic squaring operation"""
        op = TestOperatorMixin()
        context = TestContext(state=TestState(psi_signal=3.0))
        
        op.resonance(None, context, "psi")
        
        assert abs(context.state.psi_signal - 9.0) < 0.0001
    
    def test_explosive_growth(self):
        """Test that resonance leads to explosive growth"""
        op = TestOperatorMixin()
        context = TestContext(state=TestState(psi_signal=1.1))
        
        initial = context.state.psi_signal
        for _ in range(5):
            op.resonance(None, context, "psi")
        
        assert context.state.psi_signal > initial * 10
    
    def test_sign_preservation(self):
        """Test that resonance preserves sign"""
        op1 = TestOperatorMixin()
        op2 = TestOperatorMixin()
        context1 = TestContext(state=TestState(psi_signal=3.0))
        context2 = TestContext(state=TestState(psi_signal=-3.0))
        
        op1.resonance(None, context1, "psi")
        op2.resonance(None, context2, "psi")
        
        assert context1.state.psi_signal > 0
        assert context2.state.psi_signal < 0
    
    def test_resonance_all_variables(self):
        """Test resonance on all three variables"""
        op = TestOperatorMixin()
        context = TestContext(state=TestState(psi_signal=2.0, phi_state=3.0, epsilon_drift=0.5))
        
        op.resonance(None, context, "psi")
        op.resonance(None, context, "phi")
        op.resonance(None, context, "epsilon")
        
        assert abs(context.state.psi_signal - 4.0) < 0.0001
        assert abs(context.state.phi_state - 9.0) < 0.0001
        assert abs(context.state.epsilon_drift - 0.25) < 0.0001
    
    def test_small_values_shrink(self):
        """Test that values < 1 shrink under resonance"""
        op = TestOperatorMixin()
        context = TestContext(state=TestState(psi_signal=0.5))
        
        op.resonance(None, context, "psi")
        
        assert context.state.psi_signal < 0.5


class TestCombinedNonlinearity:
    """Tests for combined nonlinear operators"""
    
    def test_decay_then_resonance(self):
        """Test decay followed by resonance"""
        op = TestOperatorMixin()
        context = TestContext(state=TestState(psi_signal=10.0))
        
        op.exponential_decay(None, context, "psi", decay_rate=0.5, dt=1.0)
        initial_after_decay = context.state.psi_signal
        op.resonance(None, context, "psi")
        
        assert context.state.psi_signal > initial_after_decay
    
    def test_resonance_then_saturation(self):
        """Test resonance followed by saturation"""
        op = TestOperatorMixin()
        context = TestContext(state=TestState(psi_signal=2.0))
        
        for _ in range(3):
            op.resonance(None, context, "psi")
        
        # Without saturation, this would be huge
        before_saturation = context.state.psi_signal
        op.hyperbolic_tangent(None, context, "psi", scale_factor=10.0)
        
        assert context.state.psi_signal <= 10.0
        assert context.state.psi_signal < before_saturation
    
    def test_oscillator_stability(self):
        """Test that combined operators create stable oscillations"""
        op = TestOperatorMixin()
        context = TestContext(state=TestState(psi_signal=2.0))
        
        for _ in range(20):
            op.resonance(None, context, "psi")
            op.hyperbolic_tangent(None, context, "psi", scale_factor=5.0)
            op.exponential_decay(None, context, "psi", decay_rate=0.1, dt=1.0)
        
        # Should stabilize to a reasonable value
        assert context.state.psi_signal < 10.0
        assert context.state.psi_signal > 0.1


class TestErrorHandling:
    """Tests for error handling"""
    
    def test_invalid_variable_name(self):
        """Test that invalid variable names raise errors"""
        op = TestOperatorMixin()
        context = TestContext(state=TestState())
        
        with pytest.raises(ValueError):
            op.exponential_decay(None, context, "invalid", decay_rate=0.5, dt=1.0)
        
        with pytest.raises(ValueError):
            op.hyperbolic_tangent(None, context, "invalid", scale_factor=1.0)
        
        with pytest.raises(ValueError):
            op.resonance(None, context, "invalid")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
