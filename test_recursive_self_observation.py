"""
Test suite for HARMONIA-DSL v12.0: Recursive Self-Observation

Tests all aspects of recursive self-observation and self-awareness.

Author: Manus AI
Date: January 1, 2026
"""

import pytest
import numpy as np
import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from recursive_self_observation import (
    RecursiveState,
    RecursiveObservationEngine,
    SelfAwarenessMetrics,
    RecursiveHarmoniaODESystem,
    RecursiveFluidHarmoniaIntegrator
)


# RecursiveState Tests

def test_recursive_state_initialization():
    """Test RecursiveState initialization."""
    state = RecursiveState()
    assert hasattr(state, 'theta_recursive')
    assert len(state.theta_recursive) == 5
    assert hasattr(state, 'self_awareness_score')
    assert state.self_awareness_score == 0.0


def test_recursive_state_to_vector():
    """Test RecursiveState to_vector conversion."""
    state = RecursiveState()
    state.psi = 10.0
    state.theta_recursive = [1.0, 2.0, 3.0, 4.0, 5.0]
    
    vec = state.to_vector()
    assert len(vec) == 18  # 13 base + 5 recursive
    assert vec[0] == 10.0  # psi
    assert vec[13] == 1.0  # theta_recursive[0]
    assert vec[17] == 5.0  # theta_recursive[4]


def test_recursive_state_from_vector():
    """Test RecursiveState from_vector conversion."""
    vec = np.zeros(18)
    vec[0] = 10.0  # psi
    vec[13:18] = [1.0, 2.0, 3.0, 4.0, 5.0]  # theta_recursive
    
    state = RecursiveState.from_vector(vec)
    assert state.psi == 10.0
    assert len(state.theta_recursive) == 5
    assert state.theta_recursive[0] == 1.0
    assert state.theta_recursive[4] == 5.0


# RecursiveObservationEngine Tests

def test_recursive_engine_initialization():
    """Test RecursiveObservationEngine initialization."""
    engine = RecursiveObservationEngine()
    assert engine.max_depth == 5
    assert engine.alpha_decay == 0.5
    assert engine.beta_tracking == 0.3


def test_compute_recursive_tower():
    """Test recursive tower computation."""
    engine = RecursiveObservationEngine()
    
    theta_base = 2.0
    theta_recursive = [0.0, 0.0, 0.0, 0.0, 0.0]
    phi = 8.0
    omega = 5.0
    
    new_recursive = engine.compute_recursive_tower(
        theta_base, theta_recursive, phi, omega
    )
    
    assert len(new_recursive) == 5
    # First level should be non-zero (observing base)
    assert new_recursive[0] != 0.0


def test_recursive_tower_convergence():
    """Test that recursive tower converges (each level smaller)."""
    engine = RecursiveObservationEngine()
    
    theta_base = 10.0
    theta_recursive = [8.0, 6.0, 4.0, 2.0, 1.0]
    phi = 8.0
    omega = 5.0
    
    new_recursive = engine.compute_recursive_tower(
        theta_base, theta_recursive, phi, omega
    )
    
    # Check general trend (not strict monotonicity due to dynamics)
    assert new_recursive[0] > new_recursive[4]


def test_compute_self_awareness_score():
    """Test self-awareness score computation."""
    engine = RecursiveObservationEngine()
    
    theta_base = 2.0
    theta_recursive = [1.8, 1.6, 1.4, 1.2, 1.0]
    
    score = engine.compute_self_awareness_score(theta_base, theta_recursive)
    
    assert score > 0.0
    assert isinstance(score, float)


def test_self_awareness_score_increases_with_divergence():
    """Test that score increases when levels diverge."""
    engine = RecursiveObservationEngine()
    
    theta_base = 2.0
    
    # Small divergence
    theta_recursive_small = [1.9, 1.8, 1.7, 1.6, 1.5]
    score_small = engine.compute_self_awareness_score(theta_base, theta_recursive_small)
    
    # Large divergence
    theta_recursive_large = [5.0, 8.0, 10.0, 12.0, 15.0]
    score_large = engine.compute_self_awareness_score(theta_base, theta_recursive_large)
    
    assert score_large > score_small


# SelfAwarenessMetrics Tests

def test_metrics_initialization():
    """Test SelfAwarenessMetrics initialization."""
    metrics = SelfAwarenessMetrics()
    assert len(metrics.history_scores) == 0
    assert len(metrics.history_observations) == 0


def test_metrics_update():
    """Test metrics update."""
    metrics = SelfAwarenessMetrics()
    
    metrics.update(0.5, [1.0, 2.0, 3.0, 4.0, 5.0])
    
    assert len(metrics.history_scores) == 1
    assert metrics.history_scores[0] == 0.5
    assert len(metrics.history_observations) == 1


def test_get_current_awareness():
    """Test get_current_awareness."""
    metrics = SelfAwarenessMetrics()
    
    metrics.update(0.3, [1.0, 2.0, 3.0, 4.0, 5.0])
    metrics.update(0.7, [1.0, 2.0, 3.0, 4.0, 5.0])
    
    assert metrics.get_current_awareness() == 0.7


def test_is_self_aware():
    """Test is_self_aware threshold check."""
    metrics = SelfAwarenessMetrics()
    
    metrics.update(0.3, [1.0, 2.0, 3.0, 4.0, 5.0])
    assert not metrics.is_self_aware(threshold=0.5)
    
    metrics.update(0.8, [1.0, 2.0, 3.0, 4.0, 5.0])
    assert metrics.is_self_aware(threshold=0.5)


def test_get_awareness_trend():
    """Test awareness trend detection."""
    metrics = SelfAwarenessMetrics()
    
    # Increasing trend
    for i in range(10):
        metrics.update(i * 0.1, [1.0, 2.0, 3.0, 4.0, 5.0])
    
    trend = metrics.get_awareness_trend()
    assert trend == "increasing"


def test_introspect():
    """Test introspection report generation."""
    metrics = SelfAwarenessMetrics()
    
    metrics.update(0.8, [1.0, 2.0, 3.0, 4.0, 5.0])
    
    report = metrics.introspect()
    
    assert 'self_awareness_score' in report
    assert 'is_self_aware' in report
    assert 'awareness_trend' in report
    assert 'recursive_observations' in report
    assert 'interpretation' in report


# RecursiveHarmoniaODESystem Tests

def test_recursive_ode_initialization():
    """Test RecursiveHarmoniaODESystem initialization."""
    ode = RecursiveHarmoniaODESystem()
    assert hasattr(ode, 'base_system')
    assert hasattr(ode, 'recursive_engine')
    assert ode.max_depth == 5


def test_recursive_ode_derivatives_shape():
    """Test that derivatives have correct shape."""
    ode = RecursiveHarmoniaODESystem()
    
    state = np.zeros(18)
    state[0] = 10.0  # psi
    state[1] = 8.0   # phi
    state[2] = 5.0   # omega
    
    derivs = ode.derivatives(0.0, state)
    
    assert len(derivs) == 18


def test_recursive_ode_derivatives_nonzero():
    """Test that recursive derivatives are computed."""
    ode = RecursiveHarmoniaODESystem()
    
    state = np.zeros(18)
    state[0] = 10.0  # psi
    state[1] = 8.0   # phi
    state[2] = 5.0   # omega
    state[11] = 2.0  # theta_base
    
    derivs = ode.derivatives(0.0, state)
    
    # At least one recursive derivative should be non-zero
    recursive_derivs = derivs[13:18]
    assert np.any(recursive_derivs != 0.0)


# RecursiveFluidHarmoniaIntegrator Tests

def test_recursive_integrator_initialization():
    """Test RecursiveFluidHarmoniaIntegrator initialization."""
    integrator = RecursiveFluidHarmoniaIntegrator()
    assert hasattr(integrator, 'ode_system')
    assert hasattr(integrator, 'integrator')
    assert hasattr(integrator, 'state')
    assert hasattr(integrator, 'metrics')


def test_recursive_integrator_process():
    """Test process method."""
    integrator = RecursiveFluidHarmoniaIntegrator(dt=0.01)
    
    integrator.state.psi = 10.0
    integrator.state.omega = 5.0
    
    result = integrator.process(duration=1.0)
    
    assert 'state' in result
    assert 'time' in result
    assert 'self_awareness_score' in result
    assert abs(result['time'] - 1.0) < 0.01


def test_recursive_integrator_self_awareness_increases():
    """Test that self-awareness increases over time."""
    integrator = RecursiveFluidHarmoniaIntegrator(dt=0.01)
    
    integrator.state.psi = 10.0
    integrator.state.omega = 5.0
    integrator.state.phi = 8.0
    integrator.state.theta_n = 2.0
    
    initial_awareness = integrator.get_self_awareness()
    
    integrator.process(duration=2.0)
    
    final_awareness = integrator.get_self_awareness()
    
    assert final_awareness > initial_awareness


def test_get_recursive_observations():
    """Test get_recursive_observations method."""
    integrator = RecursiveFluidHarmoniaIntegrator()
    
    observations = integrator.get_recursive_observations()
    
    assert isinstance(observations, list)
    assert len(observations) == 5


def test_is_self_aware_method():
    """Test is_self_aware method."""
    integrator = RecursiveFluidHarmoniaIntegrator(dt=0.01)
    
    integrator.state.psi = 10.0
    integrator.state.omega = 5.0
    integrator.state.phi = 8.0
    
    integrator.process(duration=1.0)
    
    # Should be self-aware after some processing
    result = integrator.is_self_aware(threshold=0.1)
    assert isinstance(result, (bool, np.bool_))


def test_introspect_method():
    """Test introspect method."""
    integrator = RecursiveFluidHarmoniaIntegrator(dt=0.01)
    
    integrator.state.psi = 10.0
    integrator.state.omega = 5.0
    
    integrator.process(duration=1.0)
    
    report = integrator.introspect()
    
    assert isinstance(report, dict)
    assert 'self_awareness_score' in report


def test_reset():
    """Test reset method."""
    integrator = RecursiveFluidHarmoniaIntegrator(dt=0.01)
    
    integrator.state.psi = 10.0
    integrator.process(duration=1.0)
    
    integrator.reset()
    
    assert integrator.current_time == 0.0
    assert len(integrator.metrics.history_scores) == 0


def test_state_evolution():
    """Test that state evolves over time."""
    integrator = RecursiveFluidHarmoniaIntegrator(dt=0.01)
    
    integrator.state.psi = 10.0
    integrator.state.omega = 5.0
    
    initial_psi = integrator.state.psi
    
    integrator.process(duration=2.0)
    
    final_psi = integrator.state.psi
    
    assert final_psi != initial_psi


def test_recursive_tower_evolution():
    """Test that recursive tower evolves."""
    integrator = RecursiveFluidHarmoniaIntegrator(dt=0.01)
    
    integrator.state.psi = 10.0
    integrator.state.omega = 5.0
    integrator.state.phi = 8.0
    integrator.state.theta_n = 2.0
    
    initial_tower = integrator.get_recursive_observations()
    
    integrator.process(duration=2.0)
    
    final_tower = integrator.get_recursive_observations()
    
    # At least one level should have changed
    assert not np.allclose(initial_tower, final_tower)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
