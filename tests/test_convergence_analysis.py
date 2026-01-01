"""
Test suite for HARMONIA-DSL v4.0 Convergence Analysis

Tests the lim operator and CONVERGENCE command functionality.
"""

import pytest
import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from convergence_analysis import (
    ConvergenceAnalyzer, AttractorType, SystemSnapshot,
    ConvergenceResult, analyze_system_convergence
)
from nonlinear_operators import NonlinearOperators
from dataclasses import dataclass


@dataclass
class TestState:
    psi_signal: float = 0.0
    phi_state: float = 0.0
    epsilon_drift: float = 0.0
    stabilized_value: float = 0.0


@dataclass
class TestContext:
    state: TestState


class TestSystem(NonlinearOperators):
    def stabilize(self, context):
        context.state.stabilized_value = (
            (context.state.psi_signal + context.state.phi_state) * 
            (1 - context.state.epsilon_drift)
        )


class TestSystemSnapshot:
    """Tests for SystemSnapshot"""
    
    def test_snapshot_creation(self):
        snapshot = SystemSnapshot(0, 1.0, 2.0, 0.1, 3.0)
        assert snapshot.iteration == 0
        assert snapshot.psi_signal == 1.0
        assert snapshot.phi_state == 2.0
        assert snapshot.epsilon_drift == 0.1
        assert snapshot.stabilized_value == 3.0
    
    def test_distance_calculation(self):
        s1 = SystemSnapshot(0, 0.0, 0.0, 0.0, 0.0)
        s2 = SystemSnapshot(1, 3.0, 4.0, 0.0, 0.0)
        distance = s1.distance_to(s2)
        assert abs(distance - 5.0) < 0.0001  # 3-4-5 triangle
    
    def test_snapshot_equality(self):
        s1 = SystemSnapshot(0, 1.0, 2.0, 0.1, 3.0)
        s2 = SystemSnapshot(1, 1.0, 2.0, 0.1, 3.0)
        assert s1 == s2


class TestPointAttractorDetection:
    """Tests for point attractor detection"""
    
    def test_simple_decay_to_zero(self):
        """Test system that decays to zero"""
        system = TestSystem()
        context = TestContext(state=TestState(psi_signal=10.0, phi_state=5.0))
        
        def update(ctx):
            system.exponential_decay(None, ctx, "psi", decay_rate=0.5, dt=1.0)
            system.exponential_decay(None, ctx, "phi", decay_rate=0.5, dt=1.0)
            system.stabilize(ctx)
        
        analyzer = ConvergenceAnalyzer()
        result = analyzer.analyze_convergence(context, update, max_iterations=200, tolerance=0.01)
        
        assert result.attractor_type == AttractorType.POINT
        assert result.converged == True
        assert result.attractor_state is not None
        assert result.attractor_state.psi_signal < 0.1
        assert result.attractor_state.phi_state < 0.1
    
    def test_convergence_to_nonzero_point(self):
        """Test system that converges to a non-zero stable state"""
        system = TestSystem()
        context = TestContext(state=TestState(psi_signal=10.0, phi_state=5.0))
        
        def update(ctx):
            # Decay towards 1.0, not 0.0
            ctx.state.psi_signal = ctx.state.psi_signal * 0.9 + 1.0 * 0.1
            ctx.state.phi_state = ctx.state.phi_state * 0.9 + 1.0 * 0.1
            system.stabilize(ctx)
        
        analyzer = ConvergenceAnalyzer()
        result = analyzer.analyze_convergence(context, update, max_iterations=500, tolerance=0.001)
        
        assert result.attractor_type == AttractorType.POINT
        assert result.converged == True
        assert abs(result.attractor_state.psi_signal - 1.0) < 0.01
        assert abs(result.attractor_state.phi_state - 1.0) < 0.01
    
    def test_fast_convergence(self):
        """Test system that converges quickly"""
        system = TestSystem()
        context = TestContext(state=TestState(psi_signal=1.0, phi_state=1.0))
        
        def update(ctx):
            # Set to zero immediately
            ctx.state.psi_signal = 0.0
            ctx.state.phi_state = 0.0
            system.stabilize(ctx)
        
        analyzer = ConvergenceAnalyzer()
        result = analyzer.analyze_convergence(context, update, max_iterations=100, tolerance=0.001)
        
        assert result.attractor_type == AttractorType.POINT
        assert result.converged == True
        assert result.iterations < 50  # Should converge quickly


class TestPeriodicAttractorDetection:
    """Tests for periodic attractor detection"""
    
    def test_simple_two_state_cycle(self):
        """Test system that oscillates between two states"""
        context = TestContext(state=TestState(psi_signal=1.0, phi_state=0.0))
        
        def update(ctx):
            # Simple flip-flop
            temp = ctx.state.psi_signal
            ctx.state.psi_signal = ctx.state.phi_state
            ctx.state.phi_state = temp
        
        analyzer = ConvergenceAnalyzer()
        result = analyzer.analyze_convergence(context, update, max_iterations=100, tolerance=0.001)
        
        assert result.attractor_type == AttractorType.PERIODIC
        assert result.converged == True
        assert result.attractor_period == 2
    
    def test_three_state_cycle(self):
        """Test system with period-3 cycle"""
        context = TestContext(state=TestState(psi_signal=1.0, phi_state=2.0, epsilon_drift=3.0))
        
        def update(ctx):
            # Rotate through three states
            temp = ctx.state.psi_signal
            ctx.state.psi_signal = ctx.state.phi_state
            ctx.state.phi_state = ctx.state.epsilon_drift / 10.0  # Scale down to prevent overflow
            ctx.state.epsilon_drift = temp * 10.0
        
        analyzer = ConvergenceAnalyzer()
        result = analyzer.analyze_convergence(context, update, max_iterations=200, tolerance=0.001)
        
        assert result.attractor_type == AttractorType.PERIODIC
        assert result.converged == True
        assert result.attractor_period == 3


class TestDivergentSystems:
    """Tests for divergent system detection"""
    
    def test_exponential_growth(self):
        """Test system that grows exponentially"""
        system = TestSystem()
        context = TestContext(state=TestState(psi_signal=1.5, phi_state=1.5))
        
        def update(ctx):
            system.resonance(None, ctx, "psi")
            system.resonance(None, ctx, "phi")
        
        analyzer = ConvergenceAnalyzer()
        result = analyzer.analyze_convergence(context, update, max_iterations=50, tolerance=0.001)
        
        assert result.attractor_type == AttractorType.DIVERGENT
        assert result.converged == False
    
    def test_linear_growth(self):
        """Test system that grows linearly"""
        context = TestContext(state=TestState(psi_signal=0.0))
        
        def update(ctx):
            ctx.state.psi_signal += 1.0  # Linear growth
        
        analyzer = ConvergenceAnalyzer()
        result = analyzer.analyze_convergence(context, update, max_iterations=100, tolerance=0.001)
        
        assert result.attractor_type == AttractorType.DIVERGENT
        assert result.converged == False


class TestConvergenceAnalyzer:
    """Tests for ConvergenceAnalyzer class"""
    
    def test_analyzer_initialization(self):
        analyzer = ConvergenceAnalyzer()
        assert len(analyzer.history) == 0
        assert analyzer.result is None
    
    def test_take_snapshot(self):
        analyzer = ConvergenceAnalyzer()
        context = TestContext(state=TestState(psi_signal=1.0, phi_state=2.0))
        snapshot = analyzer.take_snapshot(context, 0)
        
        assert snapshot.iteration == 0
        assert snapshot.psi_signal == 1.0
        assert snapshot.phi_state == 2.0
    
    def test_get_attractor_type(self):
        analyzer = ConvergenceAnalyzer()
        context = TestContext(state=TestState(psi_signal=1.0))
        
        def update(ctx):
            ctx.state.psi_signal *= 0.5
        
        analyzer.analyze_convergence(context, update, max_iterations=100, tolerance=0.001)
        
        assert analyzer.get_attractor_type() == "POINT"
    
    def test_is_stable(self):
        analyzer = ConvergenceAnalyzer()
        context = TestContext(state=TestState(psi_signal=1.0))
        
        def update(ctx):
            ctx.state.psi_signal *= 0.5
        
        analyzer.analyze_convergence(context, update, max_iterations=100, tolerance=0.001)
        
        assert analyzer.is_stable() == True
    
    def test_get_convergence_info(self):
        analyzer = ConvergenceAnalyzer()
        context = TestContext(state=TestState(psi_signal=1.0))
        
        def update(ctx):
            ctx.state.psi_signal *= 0.5
        
        analyzer.analyze_convergence(context, update, max_iterations=100, tolerance=0.001)
        info = analyzer.get_convergence_info()
        
        assert info["analyzed"] == True
        assert info["converged"] == True
        assert info["stable"] == True
        assert "attractor_state" in info


class TestSafetyVerification:
    """Tests for safety verification use cases"""
    
    def test_verify_safe_system(self):
        """Test that a safe system is verified as safe"""
        system = TestSystem()
        context = TestContext(state=TestState(psi_signal=10.0, phi_state=5.0, epsilon_drift=0.1))
        
        def update(ctx):
            system.exponential_decay(None, ctx, "psi", decay_rate=0.3, dt=1.0)
            system.exponential_decay(None, ctx, "phi", decay_rate=0.3, dt=1.0)
            system.stabilize(ctx)
        
        analyzer = ConvergenceAnalyzer()
        result = analyzer.analyze_convergence(context, update, max_iterations=500, tolerance=0.001)
        
        # System should be stable
        assert analyzer.is_stable() == True
        assert result.attractor_type == AttractorType.POINT
        
        # Final state should be safe (low values)
        assert result.attractor_state.psi_signal < 1.0
        assert result.attractor_state.phi_state < 1.0
        assert result.attractor_state.epsilon_drift < 0.5
    
    def test_detect_unsafe_system(self):
        """Test that an unsafe system is detected"""
        system = TestSystem()
        context = TestContext(state=TestState(psi_signal=2.0, phi_state=2.0))
        
        def update(ctx):
            system.resonance(None, ctx, "psi")
            system.resonance(None, ctx, "phi")
        
        analyzer = ConvergenceAnalyzer()
        result = analyzer.analyze_convergence(context, update, max_iterations=50, tolerance=0.001)
        
        # System should be unstable
        assert analyzer.is_stable() == False
        assert result.attractor_type == AttractorType.DIVERGENT


class TestConvenienceFunction:
    """Tests for the convenience function"""
    
    def test_analyze_system_convergence(self):
        """Test the convenience function"""
        context = TestContext(state=TestState(psi_signal=10.0))
        
        def update(ctx):
            ctx.state.psi_signal *= 0.5
        
        analyzer = analyze_system_convergence(context, update, max_iterations=100, tolerance=0.001)
        
        assert analyzer.result is not None
        assert analyzer.result.converged == True
        assert analyzer.is_stable() == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
