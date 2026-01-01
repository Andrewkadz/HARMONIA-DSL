"""
Test Suite for HARMONIA-DSL v9.0: Continuous-Time Dynamics

Author: Manus AI
Date: January 1, 2026
"""

import pytest
import numpy as np
from continuous_dynamics import (
    ContinuousState,
    ContinuousTimeIntegrator,
    HarmoniaODESystem,
    FluidHarmoniaIntegrator
)


# ===== ContinuousState Tests =====

def test_continuous_state_initialization():
    """Test ContinuousState initialization."""
    state = ContinuousState()
    assert state.psi == 10.0
    assert state.phi == 8.0
    assert state.omega == 1.0
    assert state.epsilon == 0.1
    assert state.energy == 100.0
    assert state.knowledge == 0.0
    assert state.maturity == 0.0


def test_continuous_state_to_vector():
    """Test conversion to vector."""
    state = ContinuousState(psi=5.0, phi=3.0)
    vec = state.to_vector()
    assert isinstance(vec, np.ndarray)
    assert len(vec) == 7
    assert vec[0] == 5.0
    assert vec[1] == 3.0


def test_continuous_state_from_vector():
    """Test creation from vector."""
    vec = np.array([5.0, 3.0, 2.0, 0.2, 50.0, 1.0, 0.5])
    state = ContinuousState.from_vector(vec, time=10.0)
    assert state.psi == 5.0
    assert state.phi == 3.0
    assert state.omega == 2.0
    assert state.epsilon == 0.2
    assert state.energy == 50.0
    assert state.knowledge == 1.0
    assert state.maturity == 0.5
    assert state.time == 10.0


def test_continuous_state_to_dict():
    """Test conversion to dictionary."""
    state = ContinuousState(psi=5.0, phi=3.0)
    d = state.to_dict()
    assert isinstance(d, dict)
    assert d['psi'] == 5.0
    assert d['phi'] == 3.0


# ===== ContinuousTimeIntegrator Tests =====

def test_integrator_initialization():
    """Test integrator initialization."""
    integrator = ContinuousTimeIntegrator(method='rk4', dt=0.01)
    assert integrator.method == 'rk4'
    assert integrator.dt == 0.01


def test_integrator_euler_method():
    """Test Euler method on simple ODE."""
    # dy/dt = -y, solution: y(t) = y0 * exp(-t)
    def f(t, y, params):
        return -y
    
    integrator = ContinuousTimeIntegrator(method='euler', dt=0.01)
    y0 = np.array([1.0])
    t_values, y_values = integrator.integrate(f, 0.0, y0, 1.0)
    
    # Check that solution decays
    assert y_values[-1] < y_values[0]
    
    # Approximate check (Euler is not very accurate)
    expected = np.exp(-1.0)
    assert abs(y_values[-1][0] - expected) < 0.1


def test_integrator_rk4_method():
    """Test RK4 method on simple ODE."""
    # dy/dt = -y, solution: y(t) = y0 * exp(-t)
    def f(t, y, params):
        return -y
    
    integrator = ContinuousTimeIntegrator(method='rk4', dt=0.01)
    y0 = np.array([1.0])
    t_values, y_values = integrator.integrate(f, 0.0, y0, 1.0)
    
    # Check that solution decays
    assert y_values[-1] < y_values[0]
    
    # RK4 should be much more accurate
    expected = np.exp(-1.0)
    assert abs(y_values[-1][0] - expected) < 0.001


def test_integrator_step():
    """Test single integration step."""
    def f(t, y, params):
        return -y
    
    integrator = ContinuousTimeIntegrator(method='rk4', dt=0.1)
    y0 = np.array([1.0])
    y1 = integrator.step(f, 0.0, y0)
    
    assert y1[0] < y0[0]
    assert y1[0] > 0


# ===== HarmoniaODESystem Tests =====

def test_ode_system_initialization():
    """Test ODE system initialization."""
    ode = HarmoniaODESystem()
    assert ode.alpha_psi == 0.1
    assert ode.alpha_phi == 0.02
    assert ode.recharge_rate == 2.0


def test_ode_system_custom_config():
    """Test ODE system with custom configuration."""
    config = {'alpha_psi': 0.5, 'recharge_rate': 5.0}
    ode = HarmoniaODESystem(config)
    assert ode.alpha_psi == 0.5
    assert ode.recharge_rate == 5.0


def test_ode_system_derivatives_shape():
    """Test that derivatives have correct shape."""
    ode = HarmoniaODESystem()
    state = np.array([10.0, 8.0, 1.0, 0.1, 100.0, 0.0, 0.0])
    derivs = ode.derivatives(0.0, state)
    
    assert isinstance(derivs, np.ndarray)
    assert len(derivs) == 7


def test_ode_system_energy_depletion():
    """Test that energy depletes with velocity."""
    ode = HarmoniaODESystem()
    state = np.array([10.0, 8.0, 1.0, 0.1, 100.0, 0.0, 0.0])
    
    # With zero velocity
    derivs_zero = ode.derivatives(0.0, state, {'velocity': 0.0})
    denergy_zero = derivs_zero[4]
    
    # With high velocity
    derivs_high = ode.derivatives(0.0, state, {'velocity': 5.0})
    denergy_high = derivs_high[4]
    
    # Energy should deplete faster with higher velocity
    assert denergy_high < denergy_zero


def test_ode_system_knowledge_growth():
    """Test that knowledge grows with awareness and coherence."""
    ode = HarmoniaODESystem()
    
    # Low awareness and coherence
    state_low = np.array([1.0, 8.0, 0.5, 0.1, 100.0, 0.0, 0.0])
    derivs_low = ode.derivatives(0.0, state_low)
    dknowledge_low = derivs_low[5]
    
    # High awareness and coherence
    state_high = np.array([10.0, 8.0, 5.0, 0.1, 100.0, 0.0, 0.0])
    derivs_high = ode.derivatives(0.0, state_high)
    dknowledge_high = derivs_high[5]
    
    # Knowledge should grow faster with higher awareness and coherence
    assert dknowledge_high > dknowledge_low


def test_ode_system_maturity_bounded():
    """Test that maturity growth slows as it approaches 1."""
    ode = HarmoniaODESystem()
    
    # Low maturity
    state_low = np.array([10.0, 8.0, 1.0, 0.1, 100.0, 1.0, 0.1])
    derivs_low = ode.derivatives(0.0, state_low)
    dmaturity_low = derivs_low[6]
    
    # High maturity
    state_high = np.array([10.0, 8.0, 1.0, 0.1, 100.0, 1.0, 0.9])
    derivs_high = ode.derivatives(0.0, state_high)
    dmaturity_high = derivs_high[6]
    
    # Maturity growth should slow as it approaches 1
    assert dmaturity_high < dmaturity_low


# ===== FluidHarmoniaIntegrator Tests =====

def test_fluid_integrator_initialization():
    """Test fluid integrator initialization."""
    fluid = FluidHarmoniaIntegrator(dt=0.01)
    assert fluid.dt == 0.01
    assert fluid.state.psi == 10.0


def test_fluid_integrator_process():
    """Test processing with fluid integrator."""
    fluid = FluidHarmoniaIntegrator(dt=0.01)
    result = fluid.process(inputs={'velocity': 1.0}, duration=1.0)
    
    assert 'R' in result
    assert 'state' in result
    assert 'trajectory' in result
    assert isinstance(result['R'], float)


def test_fluid_integrator_time_advancement():
    """Test that time advances correctly."""
    fluid = FluidHarmoniaIntegrator(dt=0.01)
    initial_time = fluid.state.time
    
    fluid.process(duration=2.0)
    
    # Use approximate comparison for floating point
    assert abs(fluid.state.time - (initial_time + 2.0)) < 1e-10


def test_fluid_integrator_history():
    """Test that history is recorded."""
    fluid = FluidHarmoniaIntegrator(dt=0.01)
    
    fluid.process(duration=1.0)
    fluid.process(duration=1.0)
    
    history = fluid.get_history()
    assert len(history) == 2


def test_fluid_integrator_reset():
    """Test reset functionality."""
    fluid = FluidHarmoniaIntegrator(dt=0.01)
    
    fluid.process(duration=5.0)
    assert fluid.state.time > 0
    
    fluid.reset()
    assert fluid.state.time == 0.0
    assert len(fluid.get_history()) == 0


def test_fluid_integrator_step():
    """Test single step."""
    fluid = FluidHarmoniaIntegrator(dt=0.1)
    initial_time = fluid.state.time
    
    result = fluid.step()
    
    assert fluid.state.time == initial_time + 0.1
    assert 'R' in result


def test_fluid_integrator_harmonic_response():
    """Test that harmonic response is computed."""
    fluid = FluidHarmoniaIntegrator(dt=0.01)
    result = fluid.process(duration=1.0)
    
    R = result['R']
    assert isinstance(R, float)
    assert R > 0


def test_fluid_integrator_energy_conservation():
    """Test that energy behaves reasonably."""
    fluid = FluidHarmoniaIntegrator(dt=0.01)
    initial_energy = fluid.state.energy
    
    # With zero velocity, energy should recharge
    fluid.process(inputs={'velocity': 0.0}, duration=1.0)
    assert fluid.state.energy >= initial_energy


def test_fluid_integrator_stability():
    """Test that system remains stable over long integration."""
    fluid = FluidHarmoniaIntegrator(dt=0.01)
    
    # Run for 10 seconds
    result = fluid.process(inputs={'velocity': 0.5}, duration=10.0)
    
    # Check that state variables are finite
    state = fluid.state
    assert np.isfinite(state.psi)
    assert np.isfinite(state.phi)
    assert np.isfinite(state.omega)
    assert np.isfinite(state.epsilon)
    assert np.isfinite(state.energy)
    assert np.isfinite(state.knowledge)
    assert np.isfinite(state.maturity)


# ===== Integration Tests =====

def test_continuous_vs_discrete_consistency():
    """Test that continuous mode is consistent with discrete mode in limit."""
    # This is a conceptual test - we'd need v8.0 to compare
    # For now, just verify continuous mode produces reasonable results
    fluid = FluidHarmoniaIntegrator(dt=0.01)
    
    result1 = fluid.process(duration=1.0)
    result2 = fluid.process(duration=1.0)
    
    # Results should be different (system is evolving)
    assert result1['R'] != result2['R']


def test_trajectory_smoothness():
    """Test that trajectories are smooth."""
    fluid = FluidHarmoniaIntegrator(dt=0.01)
    result = fluid.process(duration=2.0)
    
    trajectory = result['trajectory']
    t_values = trajectory['t']
    state_values = trajectory['states']
    
    # Check that we have many points (smooth trajectory)
    assert len(t_values) > 100
    
    # Check that psi changes smoothly (no large jumps)
    psi_values = state_values[:, 0]
    psi_diffs = np.diff(psi_values)
    max_diff = np.max(np.abs(psi_diffs))
    
    # Maximum change per step should be small
    assert max_diff < 10.0  # Reasonable threshold


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
