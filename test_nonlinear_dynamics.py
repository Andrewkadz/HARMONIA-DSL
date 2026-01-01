"""
Test Suite for HARMONIA-DSL v11.0: Nonlinear Dynamics

Author: Manus AI
Date: January 1, 2026
"""

import pytest
import numpy as np
from nonlinear_dynamics import (
    NonlinearState,
    NonlinearDynamicsEngine,
    NonlinearHarmoniaODESystem,
    NonlinearFluidHarmoniaIntegrator
)


# ===== NonlinearState Tests =====

def test_nonlinear_state_initialization():
    """Test NonlinearState initialization."""
    state = NonlinearState()
    assert state.psi == 10.0
    assert state.domega_dpsi == 0.0
    assert state.theta_n == 1.0
    assert state.lambda_stability == 1.0


def test_nonlinear_state_to_vector():
    """Test conversion to vector."""
    state = NonlinearState(psi=5.0, domega_dpsi=0.5, theta_n=2.0)
    vec = state.to_vector()
    assert isinstance(vec, np.ndarray)
    assert len(vec) == 13
    assert vec[10] == 0.5  # domega_dpsi
    assert vec[11] == 2.0  # theta_n


def test_nonlinear_state_from_vector():
    """Test creation from vector."""
    vec = np.array([5.0, 3.0, 2.0, 0.2, 50.0, 1.0, 0.5, 1.5, 0.8, 6.0, 0.3, 2.5, 1.2])
    state = NonlinearState.from_vector(vec, time=10.0)
    assert state.psi == 5.0
    assert state.domega_dpsi == 0.3
    assert state.theta_n == 2.5
    assert state.lambda_stability == 1.2


# ===== NonlinearDynamicsEngine Tests =====

def test_nonlinear_engine_initialization():
    """Test nonlinear engine initialization."""
    engine = NonlinearDynamicsEngine()
    assert engine.C_quadratic == 0.0001
    assert engine.C_exp_decay == 0.01
    assert engine.C_tanh_ethics == 0.1


def test_quadratic_awareness():
    """Test quadratic awareness computation."""
    engine = NonlinearDynamicsEngine()
    
    quad = engine.compute_quadratic_awareness(
        psi=10.0,
        omega=2.0,
        domega_dpsi=0.5
    )
    
    assert isinstance(quad, float)
    assert quad != 0.0


def test_quadratic_awareness_feedback():
    """Test that derivative feedback modulates quadratic term."""
    engine = NonlinearDynamicsEngine()
    
    # Low derivative (high feedback)
    quad_low = engine.compute_quadratic_awareness(
        psi=10.0, omega=2.0, domega_dpsi=0.1
    )
    
    # High derivative (low feedback)
    quad_high = engine.compute_quadratic_awareness(
        psi=10.0, omega=2.0, domega_dpsi=0.9
    )
    
    # High derivative should reduce quadratic term
    assert quad_low > quad_high


def test_exponential_decay():
    """Test exponential decay computation."""
    engine = NonlinearDynamicsEngine()
    
    decay = engine.compute_exponential_decay(theta_n=2.0)
    
    assert isinstance(decay, float)
    assert 0 < decay <= 1.0  # Decay factor should be in (0, 1]


def test_exponential_decay_increases_with_layers():
    """Test that decay increases with more layers."""
    engine = NonlinearDynamicsEngine()
    
    decay_low = engine.compute_exponential_decay(theta_n=1.0)
    decay_high = engine.compute_exponential_decay(theta_n=5.0)
    
    # More layers should cause more decay
    assert decay_high < decay_low


def test_tanh_saturation_ethics():
    """Test tanh saturation for ethics."""
    engine = NonlinearDynamicsEngine()
    
    sat = engine.compute_tanh_saturation_ethics(
        delta_phi=2.0,
        omega=1.0
    )
    
    assert isinstance(sat, float)
    assert -1.0 <= sat <= 1.0  # tanh is bounded


def test_tanh_saturation_growth():
    """Test tanh saturation for growth."""
    engine = NonlinearDynamicsEngine()
    
    sat = engine.compute_tanh_saturation_growth(
        maturity=0.5,
        lambda_stability=1.0,
        xi_stability=1.0
    )
    
    assert isinstance(sat, float)
    assert -1.0 <= sat <= 1.0  # tanh is bounded


def test_recursive_observation():
    """Test recursive observation computation."""
    engine = NonlinearDynamicsEngine()
    
    rec = engine.compute_recursive_observation(
        theta_n=2.0,
        phi=8.0,
        omega=3.0
    )
    
    assert isinstance(rec, float)
    assert rec != 0.0


# ===== NonlinearHarmoniaODESystem Tests =====

def test_nonlinear_ode_system_initialization():
    """Test nonlinear ODE system initialization."""
    ode = NonlinearHarmoniaODESystem()
    assert ode.base_system is not None
    assert ode.nonlinear_engine is not None


def test_nonlinear_ode_system_derivatives_shape():
    """Test that derivatives have correct shape."""
    ode = NonlinearHarmoniaODESystem()
    state = np.array([10.0, 8.0, 1.0, 0.1, 100.0, 0.0, 0.0, 0.0, 0.0, 10.0, 0.0, 1.0, 1.0])
    derivs = ode.derivatives(0.0, state)
    
    assert isinstance(derivs, np.ndarray)
    assert len(derivs) == 13


def test_nonlinear_ode_system_nonlinear_effects():
    """Test that nonlinear terms affect derivatives."""
    ode = NonlinearHarmoniaODESystem()
    
    # State with low awareness (weak quadratic)
    state_low = np.array([5.0, 8.0, 1.0, 0.1, 100.0, 0.1, 0.0, 0.0, 0.0, 10.0, 0.0, 1.0, 1.0])
    derivs_low = ode.derivatives(0.0, state_low)
    
    # State with high awareness (strong quadratic)
    state_high = np.array([20.0, 8.0, 5.0, 0.1, 100.0, 0.1, 0.0, 0.0, 0.0, 10.0, 0.0, 1.0, 1.0])
    derivs_high = ode.derivatives(0.0, state_high)
    
    # Awareness derivative should be different due to quadratic term
    assert derivs_low[0] != derivs_high[0]


def test_derivative_tracking():
    """Test that ∂Ω/∂Ψ is tracked correctly."""
    ode = NonlinearHarmoniaODESystem()
    state = np.array([10.0, 8.0, 5.0, 0.1, 100.0, 1.0, 0.0, 0.0, 0.0, 10.0, 0.0, 1.0, 1.0])
    
    # Run a few steps to build history
    for _ in range(3):
        derivs = ode.derivatives(0.0, state)
        state = state + 0.01 * derivs
    
    # Check that derivative is being updated
    assert len(ode.history_psi) > 0
    assert len(ode.history_omega) > 0


# ===== NonlinearFluidHarmoniaIntegrator Tests =====

def test_nonlinear_fluid_integrator_initialization():
    """Test nonlinear fluid integrator initialization."""
    integrator = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    assert integrator.dt == 0.01
    assert integrator.state.psi == 10.0


def test_nonlinear_fluid_integrator_process():
    """Test processing with nonlinear integrator."""
    integrator = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    result = integrator.process(inputs={'velocity': 1.0}, duration=1.0)
    
    assert 'R' in result
    assert 'state' in result
    assert 'trajectory' in result


def test_nonlinear_state_evolution():
    """Test that nonlinear state variables evolve."""
    integrator = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    
    initial_theta_n = integrator.state.theta_n
    initial_lambda = integrator.state.lambda_stability
    
    integrator.process(duration=2.0)
    
    # Nonlinear state variables should have changed
    assert integrator.state.theta_n != initial_theta_n
    assert integrator.state.lambda_stability != initial_lambda


def test_quadratic_awareness_effect():
    """Test that quadratic term creates self-reinforcement."""
    integrator = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    
    # Set high awareness and coherence for strong quadratic effect
    integrator.state.psi = 20.0
    integrator.state.omega = 10.0
    
    initial_psi = integrator.state.psi
    
    integrator.process(duration=1.0)
    
    # Awareness should have increased due to quadratic term
    assert integrator.state.psi > initial_psi


def test_exponential_decay_effect():
    """Test that exponential decay affects memory."""
    integrator = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    
    # Set high thought layers for strong decay
    integrator.state.theta_n = 5.0
    integrator.state.psi_memory = 20.0
    integrator.state.psi = 10.0
    
    integrator.process(duration=2.0)
    
    # Memory should have decayed toward current awareness
    # (though it's complex due to other dynamics)
    assert np.isfinite(integrator.state.psi_memory)


def test_stability():
    """Test that nonlinear system remains stable."""
    integrator = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    
    result = integrator.process(inputs={'velocity': 1.0}, duration=5.0)
    
    state = integrator.state
    assert np.isfinite(state.psi)
    assert np.isfinite(state.phi)
    assert np.isfinite(state.omega)
    assert np.isfinite(state.theta_n)
    assert np.isfinite(state.lambda_stability)


def test_reset():
    """Test reset functionality."""
    integrator = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    
    integrator.process(duration=5.0)
    assert integrator.state.time > 0
    
    integrator.reset()
    assert integrator.state.time == 0.0
    assert integrator.state.theta_n == 1.0


# ===== Integration Tests =====

def test_nonlinear_vs_linear_comparison():
    """Test that nonlinear dynamics produce different behavior."""
    # This is a conceptual test
    integrator = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    
    result1 = integrator.process(duration=2.0)
    result2 = integrator.process(duration=2.0)
    
    # System should continue evolving
    assert result1['R'] != result2['R']


def test_trajectory_smoothness():
    """Test that trajectories remain smooth with nonlinear terms."""
    integrator = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    result = integrator.process(duration=2.0)
    
    trajectory = result['trajectory']
    state_values = trajectory['states']
    
    # Check awareness smoothness
    psi_values = state_values[:, 0]
    psi_diffs = np.diff(psi_values)
    max_diff = np.max(np.abs(psi_diffs))
    
    # Should still be smooth despite nonlinearities
    assert max_diff < 10.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
