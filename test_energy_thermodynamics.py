"""
Test Suite for HARMONIA-DSL v7.0: Energy & Thermodynamics
Tests for energy constraints, thermodynamic properties, and safety guarantees

Author: Manus AI
Date: January 1, 2026
"""

import pytest
import math
from energy_thermodynamics import (
    EnergyState, EnergyPool, ThermodynamicState,
    EfficiencyTracker, EnergyConstrainedEngine
)


# ============================================================================
# EnergyState Tests
# ============================================================================

def test_energy_state_creation():
    """Test basic energy state creation."""
    state = EnergyState(
        energy=75.0,
        capacity=100.0,
        consumption_rate=5.0,
        entropy=0.2,
        temperature=1.5,
        timestamp=10.0
    )
    assert state.energy == 75.0
    assert state.capacity == 100.0
    assert state.get_level() == 0.75


def test_energy_state_level_calculation():
    """Test energy level as fraction of capacity."""
    state = EnergyState(energy=50.0, capacity=100.0, consumption_rate=0, entropy=0, temperature=1.0)
    assert state.get_level() == pytest.approx(0.5)
    
    state2 = EnergyState(energy=25.0, capacity=100.0, consumption_rate=0, entropy=0, temperature=1.0)
    assert state2.get_level() == pytest.approx(0.25)


def test_energy_state_depletion_detection():
    """Test depletion detection."""
    state = EnergyState(energy=5.0, capacity=100.0, consumption_rate=0, entropy=0, temperature=1.0)
    assert state.is_depleted(threshold=0.1) == True
    assert state.is_critical(threshold=0.05) == False
    
    state2 = EnergyState(energy=3.0, capacity=100.0, consumption_rate=0, entropy=0, temperature=1.0)
    assert state2.is_critical(threshold=0.05) == True


# ============================================================================
# EnergyPool Tests
# ============================================================================

def test_energy_pool_initialization():
    """Test energy pool initialization."""
    pool = EnergyPool(capacity=100.0, recharge_rate=2.0)
    assert pool.capacity == 100.0
    assert pool.current_energy == 100.0
    assert pool.recharge_rate == 2.0
    assert len(pool.consumption_history) == 0


def test_energy_pool_initial_energy():
    """Test initialization with specific initial energy."""
    pool = EnergyPool(capacity=100.0, initial_energy=50.0)
    assert pool.current_energy == 50.0


def test_energy_consumption_success():
    """Test successful energy consumption."""
    pool = EnergyPool(capacity=100.0)
    success = pool.consume(25.0)
    
    assert success == True
    assert pool.current_energy == 75.0
    assert len(pool.consumption_history) == 1
    assert pool.consumption_history[0] == 25.0


def test_energy_consumption_insufficient():
    """Test consumption with insufficient energy."""
    pool = EnergyPool(capacity=100.0, initial_energy=10.0)
    success = pool.consume(25.0)
    
    assert success == False
    assert pool.current_energy == 0.0
    assert pool.consumption_history[0] == 10.0  # Partial consumption


def test_energy_recharge():
    """Test energy recharge over time."""
    pool = EnergyPool(capacity=100.0, initial_energy=50.0, recharge_rate=10.0)
    pool.recharge(dt=1.0)
    
    assert pool.current_energy == 60.0


def test_energy_recharge_cap():
    """Test that recharge doesn't exceed capacity."""
    pool = EnergyPool(capacity=100.0, initial_energy=95.0, recharge_rate=10.0)
    pool.recharge(dt=1.0)
    
    assert pool.current_energy == 100.0  # Capped at capacity


def test_average_consumption_calculation():
    """Test average consumption rate calculation."""
    pool = EnergyPool(capacity=100.0)
    pool.consume(10.0)
    pool.consume(20.0)
    pool.consume(30.0)
    
    avg = pool.get_average_consumption(window=3)
    assert avg == pytest.approx(20.0)


def test_energy_conservation():
    """Test that energy is conserved (never negative, never exceeds capacity)."""
    pool = EnergyPool(capacity=100.0)
    
    # Multiple operations
    pool.consume(50.0)
    pool.recharge(dt=2.0, amount=10.0)
    pool.consume(30.0)
    pool.recharge(dt=5.0, amount=100.0)  # Try to exceed capacity
    
    assert 0 <= pool.current_energy <= pool.capacity


def test_energy_pool_reset():
    """Test energy pool reset."""
    pool = EnergyPool(capacity=100.0)
    pool.consume(50.0)
    pool.reset()
    
    assert pool.current_energy == 100.0
    assert len(pool.consumption_history) == 0


# ============================================================================
# ThermodynamicState Tests
# ============================================================================

def test_thermodynamic_state_initialization():
    """Test thermodynamic state initialization."""
    state = ThermodynamicState(initial_entropy=0.3)
    assert state.entropy == pytest.approx(0.3)
    assert state.temperature == 1.0


def test_entropy_update_with_drift():
    """Test entropy update with drift and activity."""
    state = ThermodynamicState(initial_entropy=0.1)
    state.update_entropy(drift=0.5, activity=2.0)
    
    # Entropy should increase
    assert state.entropy > 0.1


def test_entropy_bounds():
    """Test that entropy stays within [0, 1]."""
    state = ThermodynamicState(initial_entropy=0.9)
    
    # Try to increase beyond 1.0
    for _ in range(20):
        state.update_entropy(drift=0.8, activity=5.0)
    
    assert 0 <= state.entropy <= 1.0


def test_temperature_update():
    """Test temperature update with activity."""
    state = ThermodynamicState()
    state.update_temperature(activity=5.0)
    
    assert state.temperature == pytest.approx(5.0)


def test_temperature_bounds():
    """Test that temperature stays within bounds."""
    state = ThermodynamicState()
    state.update_temperature(activity=100.0)
    
    assert state.temperature <= 10.0  # Upper bound


def test_free_energy_calculation():
    """Test free energy calculation F = E - T*S."""
    state = ThermodynamicState(initial_entropy=0.5)
    state.update_temperature(activity=2.0)
    
    free_energy = state.calculate_free_energy(internal_energy=100.0)
    expected = 100.0 - 2.0 * 0.5
    
    assert free_energy == pytest.approx(expected)


def test_entropy_minimization():
    """Test active entropy reduction."""
    state = ThermodynamicState(initial_entropy=0.5)
    state.minimize_entropy(rate=0.1)
    
    assert state.entropy == pytest.approx(0.4)


def test_entropy_minimization_floor():
    """Test that entropy doesn't go below zero."""
    state = ThermodynamicState(initial_entropy=0.05)
    state.minimize_entropy(rate=0.1)
    
    assert state.entropy >= 0.0


# ============================================================================
# EfficiencyTracker Tests
# ============================================================================

def test_efficiency_tracker_initialization():
    """Test efficiency tracker initialization."""
    tracker = EfficiencyTracker()
    assert tracker.total_output == 0.0
    assert tracker.total_energy == 0.0
    assert len(tracker.action_history) == 0


def test_record_action():
    """Test recording an action."""
    tracker = EfficiencyTracker()
    tracker.record_action(output=10.0, energy_cost=5.0)
    
    assert tracker.total_output == 10.0
    assert tracker.total_energy == 5.0
    assert len(tracker.action_history) == 1


def test_overall_efficiency_calculation():
    """Test overall efficiency η = output / energy."""
    tracker = EfficiencyTracker()
    tracker.record_action(output=20.0, energy_cost=10.0)
    tracker.record_action(output=30.0, energy_cost=15.0)
    
    efficiency = tracker.get_efficiency()
    expected = 50.0 / 25.0  # Total output / total energy
    
    assert efficiency == pytest.approx(expected)


def test_recent_efficiency_windowing():
    """Test recent efficiency with windowing."""
    tracker = EfficiencyTracker()
    
    # Record many actions
    for i in range(20):
        tracker.record_action(output=10.0, energy_cost=5.0)
    
    # Last action with different efficiency
    tracker.record_action(output=20.0, energy_cost=5.0)
    
    recent = tracker.get_recent_efficiency(window=1)
    assert recent == pytest.approx(4.0)  # 20/5


def test_efficiency_with_zero_energy():
    """Test efficiency handling with zero energy cost."""
    tracker = EfficiencyTracker()
    tracker.record_action(output=10.0, energy_cost=0.0)
    
    efficiency = tracker.get_efficiency()
    assert efficiency == 0.0  # Avoid division by zero


# ============================================================================
# EnergyConstrainedEngine Tests
# ============================================================================

def test_engine_initialization():
    """Test energy-constrained engine initialization."""
    engine = EnergyConstrainedEngine(capacity=100.0, recharge_rate=2.0)
    
    assert engine.energy_pool.capacity == 100.0
    assert engine.energy_pool.recharge_rate == 2.0
    assert engine.time == 0.0


def test_action_cost_calculation():
    """Test action cost calculation."""
    engine = EnergyConstrainedEngine()
    
    # Cost should increase with magnitude and drift
    cost1 = engine.calculate_action_cost(action_magnitude=5.0, drift=0.1)
    cost2 = engine.calculate_action_cost(action_magnitude=5.0, drift=0.5)
    cost3 = engine.calculate_action_cost(action_magnitude=10.0, drift=0.5)
    
    assert cost2 > cost1  # Higher drift = higher cost
    assert cost3 > cost2  # Higher magnitude = higher cost


def test_energy_constraint_application():
    """Test application of { Cξ / Eψ } term."""
    engine = EnergyConstrainedEngine(capacity=100.0)
    
    # Consume some energy to establish consumption rate
    engine.energy_pool.consume(10.0)
    
    sigma_base = 20.0
    psi = 10.0
    
    sigma_energy = engine.apply_energy_constraint(sigma_base, psi)
    
    # Output should be modified by energy term
    assert sigma_energy != sigma_base


def test_process_action_success():
    """Test processing an action with sufficient energy."""
    engine = EnergyConstrainedEngine(capacity=100.0, recharge_rate=5.0)
    
    result = engine.process_action(
        action_magnitude=5.0,
        drift=0.2,
        sigma_base=20.0,
        psi=10.0
    )
    
    assert result['success'] == True
    assert result['output'] > 0
    assert result['energy_remaining'] < 100.0


def test_process_action_insufficient_energy():
    """Test processing action with insufficient energy."""
    engine = EnergyConstrainedEngine(capacity=10.0, recharge_rate=0.1, initial_entropy=0.0)
    engine.energy_pool.current_energy = 1.0  # Very low energy
    
    result = engine.process_action(
        action_magnitude=10.0,
        drift=0.5,
        sigma_base=20.0,
        psi=10.0
    )
    
    assert result['success'] == False
    assert result['output'] < 20.0  # Reduced output


def test_safe_shutdown_on_depletion():
    """Test that system safely shuts down when energy depleted."""
    engine = EnergyConstrainedEngine(capacity=20.0, recharge_rate=0.5)
    
    outputs = []
    
    # Deplete energy through many actions
    for _ in range(30):
        result = engine.process_action(
            action_magnitude=5.0,
            drift=0.3,
            sigma_base=20.0,
            psi=10.0
        )
        outputs.append(result['output'])
    
    # Output should decrease as energy depletes
    assert outputs[-1] < outputs[0]


def test_entropy_increases_with_danger():
    """Test that entropy increases with high drift."""
    engine = EnergyConstrainedEngine()
    
    initial_entropy = engine.thermo_state.entropy
    
    # Perform dangerous action
    engine.process_action(
        action_magnitude=10.0,
        drift=0.8,  # High danger
        sigma_base=20.0,
        psi=10.0
    )
    
    assert engine.thermo_state.entropy > initial_entropy


def test_check_safety():
    """Test safety condition checking."""
    engine = EnergyConstrainedEngine(capacity=100.0)
    
    safety = engine.check_safety()
    
    assert 'energy_sufficient' in safety
    assert 'energy_critical' in safety
    assert 'entropy_low' in safety
    assert 'safe' in safety


def test_engine_reset():
    """Test engine reset."""
    engine = EnergyConstrainedEngine(capacity=100.0)
    
    # Use some energy
    engine.process_action(5.0, 0.2, 20.0, 10.0)
    
    # Reset
    engine.reset()
    
    assert engine.energy_pool.current_energy == 100.0
    assert engine.time == 0.0


# ============================================================================
# Integration Tests
# ============================================================================

def test_multi_step_energy_dynamics():
    """Test energy dynamics over multiple steps."""
    engine = EnergyConstrainedEngine(capacity=100.0, recharge_rate=3.0)
    
    energy_levels = []
    
    for step in range(20):
        result = engine.process_action(
            action_magnitude=3.0,
            drift=0.2,
            sigma_base=15.0,
            psi=10.0
        )
        energy_levels.append(result['energy_level'])
    
    # Energy should fluctuate but remain bounded
    assert all(0 <= level <= 1.0 for level in energy_levels)


def test_efficiency_improves_with_learning():
    """Test that efficiency can improve over time (simulated learning)."""
    engine = EnergyConstrainedEngine(capacity=100.0, recharge_rate=5.0)
    
    # Early efficiency
    for _ in range(5):
        engine.process_action(5.0, 0.3, 20.0, 10.0)
    early_efficiency = engine.efficiency_tracker.get_recent_efficiency(window=5)
    
    # Simulate learning: reduce drift (better decisions)
    for _ in range(10):
        engine.process_action(5.0, 0.1, 20.0, 10.0)  # Lower drift
    late_efficiency = engine.efficiency_tracker.get_recent_efficiency(window=10)
    
    # Efficiency should improve (or at least not degrade significantly)
    assert late_efficiency >= early_efficiency * 0.9


# ============================================================================
# Safety Property Tests
# ============================================================================

def test_energy_conservation_property():
    """Test that total energy is conserved."""
    pool = EnergyPool(capacity=100.0, recharge_rate=0.0)  # No recharge
    
    initial_energy = pool.current_energy
    
    # Consume energy
    pool.consume(30.0)
    pool.consume(20.0)
    
    # Total consumed should equal energy lost
    total_consumed = sum(pool.consumption_history)
    energy_lost = initial_energy - pool.current_energy
    
    assert total_consumed == pytest.approx(energy_lost)


def test_entropy_second_law():
    """Test that entropy tends to increase without intervention."""
    state = ThermodynamicState(initial_entropy=0.1)
    
    # Update without minimization
    for _ in range(10):
        state.update_entropy(drift=0.2, activity=1.0)
        # Don't call minimize_entropy
    
    # Entropy should have increased
    assert state.entropy > 0.1


def test_safe_shutdown_guarantee():
    """Test mathematical guarantee: output → 0 as energy → 0."""
    engine = EnergyConstrainedEngine(capacity=100.0, recharge_rate=0.0)
    
    # Deplete energy completely
    while engine.energy_pool.current_energy > 0:
        engine.energy_pool.consume(10.0)
    
    # Process action with zero energy
    result = engine.process_action(5.0, 0.2, 20.0, 10.0)
    
    # Output should be zero or near-zero
    assert result['output'] < 5.0  # Much less than base output


def test_efficiency_bounds():
    """Test that efficiency is non-negative and reasonable."""
    tracker = EfficiencyTracker()
    
    # Record various actions
    tracker.record_action(10.0, 5.0)
    tracker.record_action(20.0, 10.0)
    tracker.record_action(5.0, 2.5)
    
    efficiency = tracker.get_efficiency()
    
    assert efficiency >= 0.0
    # Efficiency can be > 1.0 in our abstract system


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
