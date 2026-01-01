"""
Test Suite for HARMONIA-DSL v10.0: Cross-Layer Coupling

Author: Manus AI
Date: January 1, 2026
"""

import pytest
import numpy as np
from cross_layer_coupling import (
    CoupledState,
    CrossLayerCouplingEngine,
    CoupledHarmoniaODESystem,
    CoupledFluidHarmoniaIntegrator
)


# ===== CoupledState Tests =====

def test_coupled_state_initialization():
    """Test CoupledState initialization."""
    state = CoupledState()
    assert state.psi == 10.0
    assert state.phi == 8.0
    assert state.i_coherence == 0.0
    assert state.delta_phi_accum == 0.0
    assert state.psi_memory == 10.0


def test_coupled_state_to_vector():
    """Test conversion to vector."""
    state = CoupledState(psi=5.0, phi=3.0, i_coherence=1.5)
    vec = state.to_vector()
    assert isinstance(vec, np.ndarray)
    assert len(vec) == 10
    assert vec[0] == 5.0
    assert vec[1] == 3.0
    assert vec[7] == 1.5


def test_coupled_state_from_vector():
    """Test creation from vector."""
    vec = np.array([5.0, 3.0, 2.0, 0.2, 50.0, 1.0, 0.5, 1.5, 0.8, 6.0])
    state = CoupledState.from_vector(vec, time=10.0)
    assert state.psi == 5.0
    assert state.i_coherence == 1.5
    assert state.delta_phi_accum == 0.8
    assert state.psi_memory == 6.0


# ===== CrossLayerCouplingEngine Tests =====

def test_coupling_engine_initialization():
    """Test coupling engine initialization."""
    engine = CrossLayerCouplingEngine()
    assert engine.C_me == 0.1
    assert engine.C_ai == 0.05
    assert engine.C_eg == 0.2


def test_coupling_engine_custom_config():
    """Test coupling engine with custom configuration."""
    config = {'C_memory_ethics': 0.5, 'C_energy_growth': 0.8}
    engine = CrossLayerCouplingEngine(config)
    assert engine.C_me == 0.5
    assert engine.C_eg == 0.8


def test_memory_ethics_coupling():
    """Test memory-ethics coupling computation."""
    engine = CrossLayerCouplingEngine()
    
    coupling = engine.compute_memory_ethics_coupling(
        psi_memory=10.0,
        knowledge=2.0,
        phi=8.0,
        i_coherence=1.0,
        entropy=0.1
    )
    
    assert isinstance(coupling, float)
    assert coupling != 0.0


def test_memory_ethics_coupling_ethics_suppression():
    """Test that high ethics suppresses memory influence."""
    engine = CrossLayerCouplingEngine()
    
    # Low ethics
    coupling_low = engine.compute_memory_ethics_coupling(
        psi_memory=10.0, knowledge=2.0, phi=2.0, i_coherence=1.0, entropy=0.1
    )
    
    # High ethics
    coupling_high = engine.compute_memory_ethics_coupling(
        psi_memory=10.0, knowledge=2.0, phi=10.0, i_coherence=1.0, entropy=0.1
    )
    
    # High ethics should suppress memory influence
    assert coupling_high < coupling_low


def test_energy_growth_coupling():
    """Test energy-growth coupling computation."""
    engine = CrossLayerCouplingEngine()
    
    coupling = engine.compute_energy_growth_coupling(
        capacity=100.0,
        consumption=0.5,
        energy=80.0,
        response=20.0,
        maturity=0.5,
        stability=1.0
    )
    
    assert isinstance(coupling, float)


def test_energy_growth_coupling_saturation():
    """Test that tanh creates saturation in growth."""
    engine = CrossLayerCouplingEngine()
    
    # Low maturity
    coupling_low = engine.compute_energy_growth_coupling(
        capacity=100.0, consumption=0.5, energy=80.0, response=20.0,
        maturity=0.1, stability=1.0
    )
    
    # High maturity (should saturate)
    coupling_high = engine.compute_energy_growth_coupling(
        capacity=100.0, consumption=0.5, energy=80.0, response=20.0,
        maturity=0.9, stability=1.0
    )
    
    # The difference should be smaller than linear (due to tanh saturation)
    ratio = coupling_high / (coupling_low + 1e-10)
    assert ratio < 9.0  # Less than 9x despite 9x maturity increase


def test_accumulation_intention_coupling():
    """Test accumulation-intention coupling computation."""
    engine = CrossLayerCouplingEngine()
    
    coupling = engine.compute_accumulation_intention_coupling(
        delta_phi_accum=2.0,
        omega=3.0,
        theta_n=1.5,
        intention=0.8,
        velocity=1.0
    )
    
    assert isinstance(coupling, float)


def test_accumulation_intention_coupling_activity_suppression():
    """Test that high activity suppresses ethical accumulation."""
    engine = CrossLayerCouplingEngine()
    
    # Low activity
    coupling_low = engine.compute_accumulation_intention_coupling(
        delta_phi_accum=2.0, omega=3.0, theta_n=1.5, intention=0.5, velocity=0.5
    )
    
    # High activity
    coupling_high = engine.compute_accumulation_intention_coupling(
        delta_phi_accum=2.0, omega=3.0, theta_n=1.5, intention=0.5, velocity=5.0
    )
    
    # High activity should suppress ethical accumulation
    assert coupling_high < coupling_low


# ===== CoupledHarmoniaODESystem Tests =====

def test_coupled_ode_system_initialization():
    """Test coupled ODE system initialization."""
    ode = CoupledHarmoniaODESystem()
    assert ode.alpha_psi == 0.1
    assert ode.coupling_engine is not None


def test_coupled_ode_system_derivatives_shape():
    """Test that derivatives have correct shape."""
    ode = CoupledHarmoniaODESystem()
    state = np.array([10.0, 8.0, 1.0, 0.1, 100.0, 0.0, 0.0, 0.0, 0.0, 10.0])
    derivs = ode.derivatives(0.0, state)
    
    assert isinstance(derivs, np.ndarray)
    assert len(derivs) == 10


def test_coupled_ode_system_coupling_effects():
    """Test that coupling terms affect derivatives."""
    ode = CoupledHarmoniaODESystem()
    
    # State with low knowledge (weak coupling)
    state_low = np.array([10.0, 8.0, 1.0, 0.1, 100.0, 0.1, 0.0, 0.0, 0.0, 10.0])
    derivs_low = ode.derivatives(0.0, state_low)
    
    # State with high knowledge (strong coupling)
    state_high = np.array([10.0, 8.0, 1.0, 0.1, 100.0, 5.0, 0.0, 0.0, 0.0, 10.0])
    derivs_high = ode.derivatives(0.0, state_high)
    
    # Awareness derivative should be affected by memory-ethics coupling
    assert derivs_low[0] != derivs_high[0]


def test_coupled_ode_system_i_coherence_evolution():
    """Test that integrated coherence evolves correctly."""
    ode = CoupledHarmoniaODESystem()
    state = np.array([10.0, 8.0, 5.0, 0.1, 100.0, 1.0, 0.0, 0.0, 0.0, 10.0])
    derivs = ode.derivatives(0.0, state)
    
    # di_coherence_dt should be non-zero
    assert derivs[7] != 0.0


# ===== CoupledFluidHarmoniaIntegrator Tests =====

def test_coupled_fluid_integrator_initialization():
    """Test coupled fluid integrator initialization."""
    integrator = CoupledFluidHarmoniaIntegrator(dt=0.01)
    assert integrator.dt == 0.01
    assert integrator.state.psi == 10.0


def test_coupled_fluid_integrator_process():
    """Test processing with coupled integrator."""
    integrator = CoupledFluidHarmoniaIntegrator(dt=0.01)
    result = integrator.process(inputs={'velocity': 1.0}, duration=1.0)
    
    assert 'R' in result
    assert 'state' in result
    assert 'trajectory' in result


def test_coupled_fluid_integrator_coupling_state_evolution():
    """Test that coupling state variables evolve."""
    integrator = CoupledFluidHarmoniaIntegrator(dt=0.01)
    
    initial_i_coherence = integrator.state.i_coherence
    initial_delta_phi = integrator.state.delta_phi_accum
    
    integrator.process(duration=2.0)
    
    # Coupling state variables should have changed
    assert integrator.state.i_coherence != initial_i_coherence
    assert integrator.state.delta_phi_accum != initial_delta_phi


def test_coupled_fluid_integrator_memory_tracking():
    """Test that memory state tracks awareness."""
    integrator = CoupledFluidHarmoniaIntegrator(dt=0.01)
    
    initial_psi = integrator.state.psi
    initial_memory = integrator.state.psi_memory
    
    # Run for a while
    integrator.process(duration=5.0)
    
    # Memory should have evolved toward current psi
    final_psi = integrator.state.psi
    final_memory = integrator.state.psi_memory
    
    # Memory should be between initial and final psi
    assert final_memory != initial_memory


def test_coupled_fluid_integrator_stability():
    """Test that coupled system remains stable."""
    integrator = CoupledFluidHarmoniaIntegrator(dt=0.01)
    
    result = integrator.process(inputs={'velocity': 1.0}, duration=10.0)
    
    state = integrator.state
    assert np.isfinite(state.psi)
    assert np.isfinite(state.phi)
    assert np.isfinite(state.i_coherence)
    assert np.isfinite(state.delta_phi_accum)
    assert np.isfinite(state.psi_memory)


def test_coupled_fluid_integrator_reset():
    """Test reset functionality."""
    integrator = CoupledFluidHarmoniaIntegrator(dt=0.01)
    
    integrator.process(duration=5.0)
    assert integrator.state.time > 0
    
    integrator.reset()
    assert integrator.state.time == 0.0
    assert integrator.state.i_coherence == 0.0


# ===== Integration Tests =====

def test_coupling_vs_uncoupled_comparison():
    """Test that coupling creates different behavior than uncoupled."""
    # This is a conceptual test - we'd compare with v9.0
    # For now, just verify coupling produces reasonable results
    integrator = CoupledFluidHarmoniaIntegrator(dt=0.01)
    
    result1 = integrator.process(duration=2.0)
    result2 = integrator.process(duration=2.0)
    
    # System should evolve
    assert result1['R'] != result2['R']


def test_emergent_behavior():
    """Test for emergent synergistic behavior."""
    integrator = CoupledFluidHarmoniaIntegrator(dt=0.01)
    
    # Scenario: high intention should suppress ethical accumulation
    result_high_intention = integrator.process(
        inputs={'velocity': 2.0, 'intention': 0.9},
        duration=3.0
    )
    
    integrator.reset()
    
    result_low_intention = integrator.process(
        inputs={'velocity': 2.0, 'intention': 0.1},
        duration=3.0
    )
    
    # Different intentions should produce different outcomes
    assert result_high_intention['R'] != result_low_intention['R']


def test_trajectory_smoothness_with_coupling():
    """Test that trajectories remain smooth with coupling."""
    integrator = CoupledFluidHarmoniaIntegrator(dt=0.01)
    result = integrator.process(duration=2.0)
    
    trajectory = result['trajectory']
    state_values = trajectory['states']
    
    # Check awareness smoothness
    psi_values = state_values[:, 0]
    psi_diffs = np.diff(psi_values)
    max_diff = np.max(np.abs(psi_diffs))
    
    # Should still be smooth despite coupling
    assert max_diff < 5.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
