"""
Test Suite for HARMONIA-DSL v8.0: Systemic Integration
Tests for complete GHE implementation with all 9 layers

Author: Manus AI
Date: January 1, 2026
"""

import pytest
from systemic_integration import (
    HarmoniaState, LayerAccumulator, SubjectiveTimeEngine,
    EthicalWeightingEngine, SelfRegulatingGrowthEngine,
    HarmoniaSystemIntegrator
)


# ============================================================================
# HarmoniaState Tests
# ============================================================================

def test_harmonia_state_creation():
    """Test basic state creation."""
    state = HarmoniaState()
    assert state.psi == 10.0
    assert state.phi == 8.0
    assert state.omega == 1.0


def test_harmonia_state_to_dict():
    """Test state conversion to dictionary."""
    state = HarmoniaState(psi=15.0, phi=10.0)
    d = state.to_dict()
    assert d['psi'] == 15.0
    assert d['phi'] == 10.0


# ============================================================================
# LayerAccumulator Tests
# ============================================================================

def test_layer_accumulator_initialization():
    """Test layer accumulator initialization."""
    accumulator = LayerAccumulator()
    assert len(accumulator.layers) == 0


def test_register_layer():
    """Test registering a layer."""
    accumulator = LayerAccumulator()
    accumulator.register_layer('test_layer', weight=0.8)
    
    assert 'test_layer' in accumulator.layers
    assert accumulator.weights['test_layer'] == 0.8


def test_set_contribution():
    """Test setting layer contribution."""
    accumulator = LayerAccumulator()
    accumulator.register_layer('test_layer')
    accumulator.set_contribution('test_layer', 5.0)
    
    assert accumulator.contributions['test_layer'] == 5.0


def test_accumulate_single_layer():
    """Test accumulation with single layer."""
    accumulator = LayerAccumulator()
    accumulator.register_layer('layer1', weight=1.0)
    accumulator.set_contribution('layer1', 10.0)
    
    total = accumulator.accumulate()
    assert total == pytest.approx(10.0)


def test_accumulate_multiple_layers():
    """Test accumulation with multiple layers."""
    accumulator = LayerAccumulator()
    accumulator.register_layer('layer1', weight=1.0)
    accumulator.register_layer('layer2', weight=0.5)
    accumulator.set_contribution('layer1', 10.0)
    accumulator.set_contribution('layer2', 20.0)
    
    total = accumulator.accumulate()
    # 1.0 * 10.0 + 0.5 * 20.0 = 20.0
    assert total == pytest.approx(20.0)


def test_get_layer_contribution():
    """Test getting individual layer contribution."""
    accumulator = LayerAccumulator()
    accumulator.register_layer('layer1')
    accumulator.set_contribution('layer1', 15.0)
    
    contrib = accumulator.get_layer_contribution('layer1')
    assert contrib == 15.0


def test_get_all_contributions():
    """Test getting all contributions."""
    accumulator = LayerAccumulator()
    accumulator.register_layer('layer1')
    accumulator.register_layer('layer2')
    accumulator.set_contribution('layer1', 5.0)
    accumulator.set_contribution('layer2', 10.0)
    
    all_contrib = accumulator.get_all_contributions()
    assert all_contrib['layer1'] == 5.0
    assert all_contrib['layer2'] == 10.0


# ============================================================================
# SubjectiveTimeEngine Tests
# ============================================================================

def test_time_engine_initialization():
    """Test time engine initialization."""
    engine = SubjectiveTimeEngine(dt=1.0)
    assert engine.current_time == 0.0
    assert engine.dt == 1.0


def test_update_time():
    """Test time advancement."""
    engine = SubjectiveTimeEngine(dt=1.0)
    engine.update_time()
    assert engine.current_time == 1.0
    
    engine.update_time(dt=2.0)
    assert engine.current_time == 3.0


def test_add_coherence():
    """Test adding coherence values."""
    engine = SubjectiveTimeEngine()
    engine.add_coherence(0.8)
    engine.add_coherence(0.9)
    
    assert len(engine.coherence_history) == 2


def test_calculate_coherence_change():
    """Test coherence change calculation."""
    engine = SubjectiveTimeEngine(dt=1.0)
    
    engine.add_coherence(0.5)
    engine.update_time()
    engine.add_coherence(0.7)
    
    d_omega = engine.calculate_coherence_change()
    assert d_omega == pytest.approx(0.2)


def test_get_temporal_term():
    """Test temporal term calculation."""
    engine = SubjectiveTimeEngine(dt=1.0)
    
    engine.add_coherence(0.5)
    engine.update_time()
    engine.add_coherence(0.7)
    
    temporal = engine.get_temporal_term(entropy=0.2)
    # ΔΩ/S = 0.2 / 0.2 = 1.0
    assert temporal == pytest.approx(1.0)


def test_project_future():
    """Test future projection."""
    engine = SubjectiveTimeEngine(dt=1.0)
    
    engine.add_coherence(0.5)
    engine.update_time()
    engine.add_coherence(0.6)
    
    projections = engine.project_future(steps=3)
    assert len(projections) == 3
    assert all(0 <= p <= 1.0 for p in projections)


def test_temporal_term_with_zero_entropy():
    """Test temporal term with very low entropy."""
    engine = SubjectiveTimeEngine()
    engine.add_coherence(0.5)
    engine.update_time()
    engine.add_coherence(0.6)
    
    # Should not crash with zero entropy
    temporal = engine.get_temporal_term(entropy=0.0)
    assert temporal > 0


# ============================================================================
# EthicalWeightingEngine Tests
# ============================================================================

def test_ethical_engine_initialization():
    """Test ethical engine initialization."""
    engine = EthicalWeightingEngine()
    assert 'safety' in engine.ethical_dimensions
    assert engine.base_beta == 1.0


def test_calculate_beta():
    """Test beta calculation."""
    engine = EthicalWeightingEngine()
    context = {'safety': 0.8}
    
    beta = engine.calculate_beta(context)
    assert beta > 0


def test_evaluate_ethics():
    """Test ethical evaluation."""
    engine = EthicalWeightingEngine()
    context = {'safety': 1.0}
    
    ethical_value = engine.evaluate_ethics({}, phi=8.0, context=context)
    assert ethical_value > 0


def test_learn_ethics():
    """Test ethical learning."""
    engine = EthicalWeightingEngine()
    initial_safety = engine.ethical_dimensions['safety']
    
    # Poor outcome should increase safety weight
    engine.learn_ethics(outcome=0.3, knowledge=0.5)
    
    assert engine.knowledge_factor == 0.5


def test_get_ethical_dimensions():
    """Test getting ethical dimensions."""
    engine = EthicalWeightingEngine()
    dimensions = engine.get_ethical_dimensions()
    
    assert 'safety' in dimensions
    assert 'fairness' in dimensions
    assert 'transparency' in dimensions


def test_beta_bounds():
    """Test that beta stays within bounds."""
    engine = EthicalWeightingEngine()
    
    # Extreme context
    context = {dim: 10.0 for dim in engine.ethical_dimensions}
    beta = engine.calculate_beta(context)
    
    assert 0.1 <= beta <= 2.0


# ============================================================================
# SelfRegulatingGrowthEngine Tests
# ============================================================================

def test_growth_engine_initialization():
    """Test growth engine initialization."""
    engine = SelfRegulatingGrowthEngine()
    assert engine.maturity_level == 0.0
    assert engine.growth_rate > 0


def test_calculate_growth():
    """Test growth calculation."""
    engine = SelfRegulatingGrowthEngine()
    
    growth = engine.calculate_growth(
        awareness=10.0,
        intention=5.0,
        dynamics=2.0
    )
    
    assert growth > 0


def test_maturity_increases():
    """Test that maturity increases with growth."""
    engine = SelfRegulatingGrowthEngine()
    initial_maturity = engine.maturity_level
    
    for _ in range(10):
        engine.calculate_growth(10.0, 5.0, 2.0)
    
    assert engine.maturity_level > initial_maturity


def test_adapt_parameters():
    """Test parameter adaptation."""
    engine = SelfRegulatingGrowthEngine()
    initial_rate = engine.growth_rate
    
    # Good performance
    for _ in range(15):
        engine.adapt_parameters(performance=0.8)
    
    # Growth rate should have changed
    assert engine.growth_rate != initial_rate


def test_evolve_system():
    """Test system evolution."""
    engine = SelfRegulatingGrowthEngine()
    
    evolution = engine.evolve_system()
    
    assert 'growth_rate' in evolution
    assert 'maturity' in evolution
    assert 'adaptations' in evolution


def test_get_maturity():
    """Test getting maturity level."""
    engine = SelfRegulatingGrowthEngine()
    
    maturity = engine.get_maturity()
    assert 0 <= maturity <= 1.0


def test_maturity_bounded():
    """Test that maturity stays within [0, 1]."""
    engine = SelfRegulatingGrowthEngine()
    
    # Try to exceed bounds
    for _ in range(1000):
        engine.calculate_growth(100.0, 100.0, 100.0)
    
    assert 0 <= engine.maturity_level <= 1.0


# ============================================================================
# HarmoniaSystemIntegrator Tests
# ============================================================================

def test_integrator_initialization():
    """Test system integrator initialization."""
    harmonia = HarmoniaSystemIntegrator()
    
    assert harmonia.state is not None
    assert harmonia.layer_accumulator is not None
    assert harmonia.time_engine is not None


def test_integrator_with_config():
    """Test integrator with custom configuration."""
    config = {
        'energy_capacity': 200.0,
        'recharge_rate': 5.0
    }
    harmonia = HarmoniaSystemIntegrator(config=config)
    
    assert harmonia.config['energy_capacity'] == 200.0


def test_process_without_input():
    """Test processing without input data."""
    harmonia = HarmoniaSystemIntegrator()
    result = harmonia.process()
    
    assert 'R' in result
    assert 'state' in result
    assert 'layers' in result


def test_process_with_input():
    """Test processing with input data."""
    harmonia = HarmoniaSystemIntegrator()
    
    input_data = {
        'psi': 15.0,
        'phi': 10.0,
        'velocity': 2.0
    }
    
    result = harmonia.process(input_data)
    
    assert result['state']['psi'] == 15.0
    assert result['state']['phi'] == 10.0


def test_harmonic_response_positive():
    """Test that harmonic response is non-negative."""
    harmonia = HarmoniaSystemIntegrator()
    
    for _ in range(10):
        result = harmonia.process()
        assert result['R'] >= 0


def test_all_layers_contribute():
    """Test that all layers contribute to the response."""
    harmonia = HarmoniaSystemIntegrator()
    result = harmonia.process()
    
    layers = result['layers']
    
    # Check that all registered layers have contributions
    assert 'awareness' in layers
    assert 'stability' in layers
    assert 'intention' in layers
    assert 'ethics' in layers


def test_state_updates():
    """Test that state updates across iterations."""
    harmonia = HarmoniaSystemIntegrator()
    
    result1 = harmonia.process({'knowledge': 0.0})
    result2 = harmonia.process({'knowledge': 1.0})
    
    assert result2['state']['knowledge'] == 1.0


def test_history_tracking():
    """Test that processing history is tracked."""
    harmonia = HarmoniaSystemIntegrator()
    
    for _ in range(5):
        harmonia.process()
    
    history = harmonia.get_history()
    assert len(history) == 5


def test_get_state():
    """Test getting current state."""
    harmonia = HarmoniaSystemIntegrator()
    harmonia.process()
    
    state = harmonia.get_state()
    assert isinstance(state, HarmoniaState)


def test_reset():
    """Test system reset."""
    harmonia = HarmoniaSystemIntegrator()
    
    # Process some iterations
    for _ in range(5):
        harmonia.process()
    
    # Reset
    harmonia.reset()
    
    assert harmonia.state.iteration == 0
    assert len(harmonia.history) == 0


def test_energy_constraint_affects_response():
    """Test that energy level affects harmonic response."""
    harmonia = HarmoniaSystemIntegrator()
    
    result_high_energy = harmonia.process({'energy': 100.0})
    
    harmonia.reset()
    result_low_energy = harmonia.process({'energy': 10.0})
    
    # Lower energy should result in lower response
    assert result_low_energy['R'] < result_high_energy['R']


def test_drift_affects_response():
    """Test that drift affects harmonic response."""
    harmonia = HarmoniaSystemIntegrator()
    
    result_low_drift = harmonia.process({'epsilon': 0.1})
    
    harmonia.reset()
    result_high_drift = harmonia.process({'epsilon': 0.8})
    
    # Higher drift should result in lower response
    assert result_high_drift['R'] < result_low_drift['R']


# ============================================================================
# Integration Tests
# ============================================================================

def test_multi_iteration_stability():
    """Test system stability over multiple iterations."""
    harmonia = HarmoniaSystemIntegrator()
    
    responses = []
    for _ in range(20):
        result = harmonia.process()
        responses.append(result['R'])
    
    # All responses should be valid
    assert all(r >= 0 for r in responses)


def test_growth_over_time():
    """Test that system grows over time."""
    harmonia = HarmoniaSystemIntegrator()
    
    initial_maturity = harmonia.growth_engine.get_maturity()
    
    for _ in range(50):
        harmonia.process({
            'psi': 10.0,
            'velocity': 1.0,
            'knowledge': 0.5
        })
    
    final_maturity = harmonia.growth_engine.get_maturity()
    assert final_maturity > initial_maturity


def test_ethical_learning_integration():
    """Test ethical learning integration with knowledge."""
    harmonia = HarmoniaSystemIntegrator()
    
    # Process with increasing knowledge
    for i in range(10):
        harmonia.process({'knowledge': i * 0.1})
        harmonia.ethical_engine.learn_ethics(0.8, i * 0.1)
    
    # Ethical engine should have updated knowledge factor
    assert harmonia.ethical_engine.knowledge_factor > 0


def test_temporal_coherence_tracking():
    """Test that temporal engine tracks coherence over time."""
    harmonia = HarmoniaSystemIntegrator()
    
    for i in range(10):
        harmonia.process({'omega': 0.5 + i * 0.05})
    
    # Should have coherence history
    assert len(harmonia.time_engine.coherence_history) > 0


def test_layer_accumulation_correctness():
    """Test that layer accumulation produces valid output."""
    harmonia = HarmoniaSystemIntegrator()
    result = harmonia.process()
    
    # Accumulated value should be positive and reasonable
    accumulated = result['accumulated']
    assert accumulated > 0
    assert accumulated < 1000  # Reasonable upper bound


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
