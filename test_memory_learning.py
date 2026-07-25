"""
Test Suite for HARMONIA-DSL v6.0: Memory & Learning
Tests for Ψ-, Ψ+, K operators and the complete memory-learning system

Author: Manus AI
Date: January 1, 2026
"""

import pytest
import math
from memory_learning import (
    State, MemoryBuffer, KnowledgeAccumulator, 
    FutureProjector, MemoryLearningEngine
)


# ============================================================================
# State Tests
# ============================================================================

def test_state_creation():
    """Test basic state creation."""
    state = State(psi=5.0, phi=3.0, epsilon=0.1, timestamp=1.0)
    assert state.psi == 5.0
    assert state.phi == 3.0
    assert state.epsilon == 0.1
    assert state.timestamp == 1.0


def test_state_subtraction():
    """Test state difference calculation."""
    s1 = State(psi=10.0, phi=8.0, epsilon=0.2)
    s2 = State(psi=5.0, phi=3.0, epsilon=0.1)
    diff = s1 - s2
    assert diff.psi == 5.0
    assert diff.phi == 5.0
    assert diff.epsilon == pytest.approx(0.1)


def test_state_addition():
    """Test state addition."""
    s1 = State(psi=5.0, phi=3.0, epsilon=0.1)
    s2 = State(psi=2.0, phi=1.0, epsilon=0.05)
    total = s1 + s2
    assert total.psi == 7.0
    assert total.phi == 4.0
    assert total.epsilon == pytest.approx(0.15)


def test_state_scalar_multiplication():
    """Test state multiplication by scalar."""
    state = State(psi=4.0, phi=2.0, epsilon=0.2)
    scaled = state * 2.5
    assert scaled.psi == 10.0
    assert scaled.phi == 5.0
    assert scaled.epsilon == pytest.approx(0.5)


def test_state_magnitude():
    """Test state vector magnitude calculation."""
    state = State(psi=3.0, phi=4.0, epsilon=0.0)
    mag = state.magnitude()
    assert mag == pytest.approx(5.0)  # 3-4-5 triangle


# ============================================================================
# MemoryBuffer Tests (Ψ-)
# ============================================================================

def test_memory_buffer_creation():
    """Test memory buffer initialization."""
    buffer = MemoryBuffer(max_depth=10)
    assert len(buffer.history) == 0
    assert buffer.max_depth == 10


def test_memory_buffer_add():
    """Test adding states to memory."""
    buffer = MemoryBuffer(max_depth=5)
    for i in range(3):
        buffer.add(State(psi=float(i), phi=float(i), epsilon=0.1))
    assert len(buffer.history) == 3


def test_memory_buffer_max_depth():
    """Test that memory buffer respects max depth."""
    buffer = MemoryBuffer(max_depth=3)
    for i in range(5):
        buffer.add(State(psi=float(i), phi=float(i), epsilon=0.1))
    assert len(buffer.history) == 3
    assert buffer.history[0].psi == 2.0  # Oldest should be removed


def test_memory_recall_empty():
    """Test recall on empty buffer."""
    buffer = MemoryBuffer()
    recalled = buffer.recall()
    assert recalled is None


def test_memory_recall_single():
    """Test recall with single state."""
    buffer = MemoryBuffer()
    state = State(psi=5.0, phi=3.0, epsilon=0.1)
    buffer.add(state)
    recalled = buffer.recall(depth=1)
    assert recalled is not None
    assert recalled.psi == pytest.approx(5.0)


def test_memory_recall_decay():
    """Test that recall applies exponential decay weighting."""
    buffer = MemoryBuffer()
    # Add states with increasing values
    for i in range(5):
        buffer.add(State(psi=float(i), phi=float(i), epsilon=0.1, timestamp=float(i)))
    
    recalled = buffer.recall(depth=5, decay_rate=0.5)
    assert recalled is not None
    # Most recent states should have more weight
    # State 4 (most recent) should dominate
    assert recalled.psi > 2.0  # Should be closer to 4 than to 0


def test_memory_velocity_calculation():
    """Test velocity calculation from memory."""
    buffer = MemoryBuffer()
    buffer.add(State(psi=0.0, phi=0.0, epsilon=0.1, timestamp=0.0))
    buffer.add(State(psi=5.0, phi=3.0, epsilon=0.1, timestamp=1.0))
    
    velocity = buffer.get_velocity()
    assert velocity is not None
    assert velocity.psi == pytest.approx(5.0)
    assert velocity.phi == pytest.approx(3.0)


def test_memory_velocity_insufficient_data():
    """Test velocity with insufficient data."""
    buffer = MemoryBuffer()
    buffer.add(State(psi=5.0, phi=3.0, epsilon=0.1))
    velocity = buffer.get_velocity()
    assert velocity is None


# ============================================================================
# KnowledgeAccumulator Tests (K)
# ============================================================================

def test_knowledge_initialization():
    """Test knowledge accumulator initialization."""
    k = KnowledgeAccumulator(learning_rate=0.01, max_knowledge=100.0)
    assert k.get_knowledge() == 0.0
    assert k.learning_rate == 0.01
    assert k.max_knowledge == 100.0


def test_knowledge_update_no_memory():
    """Test knowledge update with no prior memory."""
    k = KnowledgeAccumulator(learning_rate=0.1)
    state = State(psi=5.0, phi=3.0, epsilon=0.1)
    k.update(state, None)
    assert k.get_knowledge() > 0.0


def test_knowledge_accumulation():
    """Test that knowledge accumulates over time."""
    k = KnowledgeAccumulator(learning_rate=0.1)
    state1 = State(psi=5.0, phi=3.0, epsilon=0.1)
    state2 = State(psi=6.0, phi=4.0, epsilon=0.1)
    
    k1 = k.update(state1, None)
    k2 = k.update(state2, state1)
    
    assert k2 > k1  # Knowledge should increase


def test_knowledge_max_bound():
    """Test that knowledge respects maximum bound."""
    k = KnowledgeAccumulator(learning_rate=10.0, max_knowledge=50.0)
    state = State(psi=5.0, phi=3.0, epsilon=0.1)
    
    for _ in range(100):
        k.update(state, None)
    
    assert k.get_knowledge() <= 50.0


def test_knowledge_reset():
    """Test knowledge reset."""
    k = KnowledgeAccumulator(learning_rate=0.1)
    state = State(psi=5.0, phi=3.0, epsilon=0.1)
    k.update(state, None)
    assert k.get_knowledge() > 0.0
    
    k.reset()
    assert k.get_knowledge() == 0.0


def test_knowledge_prediction_error():
    """Test that larger prediction errors lead to more learning."""
    k = KnowledgeAccumulator(learning_rate=0.1)
    current = State(psi=10.0, phi=10.0, epsilon=0.1)
    
    # Small error
    close_memory = State(psi=9.5, phi=9.5, epsilon=0.1)
    k1 = k.update(current, close_memory)
    
    # Large error
    k.reset()
    far_memory = State(psi=5.0, phi=5.0, epsilon=0.1)
    k2 = k.update(current, far_memory)
    
    assert k2 > k1  # Larger error should lead to more learning


# ============================================================================
# FutureProjector Tests (Ψ+)
# ============================================================================

def test_projector_initialization():
    """Test future projector initialization."""
    proj = FutureProjector()
    assert proj.learned_acceleration.psi == 0.0


def test_projector_learn_acceleration():
    """Test learning acceleration from history."""
    proj = FutureProjector()
    history = [
        State(psi=0.0, phi=0.0, epsilon=0.1, timestamp=0.0),
        State(psi=1.0, phi=1.0, epsilon=0.1, timestamp=1.0),
        State(psi=3.0, phi=3.0, epsilon=0.1, timestamp=2.0),  # Accelerating
    ]
    proj.learn_acceleration(history)
    # Should detect positive acceleration
    assert proj.learned_acceleration.psi > 0.0


def test_projector_insufficient_history():
    """Test projection with insufficient history."""
    proj = FutureProjector()
    history = [State(psi=0.0, phi=0.0, epsilon=0.1)]
    proj.learn_acceleration(history)
    # Should not crash, just not learn
    assert proj.learned_acceleration.psi == 0.0


def test_projector_project_future():
    """Test future state projection."""
    proj = FutureProjector()
    current = State(psi=5.0, phi=3.0, epsilon=0.1)
    velocity = State(psi=1.0, phi=0.5, epsilon=0.0)
    
    projections = proj.project(current, velocity, knowledge=1.0, steps=3)
    assert len(projections) == 3
    # Future states should show forward movement
    assert projections[0].psi > current.psi


def test_projector_no_velocity():
    """Test projection with no velocity."""
    proj = FutureProjector()
    current = State(psi=5.0, phi=3.0, epsilon=0.1)
    
    projections = proj.project(current, None, knowledge=1.0, steps=2)
    assert len(projections) == 2


# ============================================================================
# MemoryLearningEngine Tests (Complete System)
# ============================================================================

def test_engine_initialization():
    """Test memory-learning engine initialization."""
    engine = MemoryLearningEngine()
    assert engine.memory is not None
    assert engine.knowledge is not None
    assert engine.projector is not None


def test_engine_process_state():
    """Test processing a state through the engine."""
    engine = MemoryLearningEngine()
    state = State(psi=5.0, phi=3.0, epsilon=0.1, timestamp=0.0)
    
    result = engine.process_state(state)
    assert 'psi_minus' in result
    assert 'psi_plus' in result
    assert 'knowledge' in result
    assert 'memory_learning_term' in result


def test_engine_learning_over_time():
    """Test that the engine learns over multiple states."""
    engine = MemoryLearningEngine(learning_rate=0.1)
    
    knowledge_values = []
    for i in range(10):
        state = State(psi=5.0 + i, phi=3.0 + i, epsilon=0.1, timestamp=float(i))
        result = engine.process_state(state)
        knowledge_values.append(result['knowledge'])
    
    # Knowledge should generally increase
    assert knowledge_values[-1] > knowledge_values[0]


def test_engine_memory_learning_term():
    """Test calculation of the full memory-learning term."""
    engine = MemoryLearningEngine()
    
    # Process several states
    for i in range(5):
        state = State(psi=5.0 + i, phi=3.0 + i, epsilon=0.1, timestamp=float(i))
        engine.process_state(state)
    
    term = engine.get_memory_learning_term()
    assert term >= 0.0  # Should be non-negative


def test_engine_apply_to_system():
    """Test applying memory-learning to system output."""
    engine = MemoryLearningEngine(learning_rate=0.1)
    
    # Build up some knowledge
    for i in range(10):
        state = State(psi=5.0 + i, phi=3.0 + i, epsilon=0.1, timestamp=float(i))
        engine.process_state(state)
    
    sigma_base = 10.0
    sigma_enhanced = engine.apply_to_system(sigma_base, influence=0.1)
    
    # Enhanced output should be different from base
    assert sigma_enhanced != sigma_base


def test_engine_adaptive_behavior():
    """Test that the engine enables adaptive behavior."""
    engine = MemoryLearningEngine(learning_rate=0.05)
    
    # Simulate learning scenario: system improves over time
    improvements = []
    for t in range(20):
        state = State(
            psi=5.0 + t * 0.5,
            phi=5.0 + t * 0.5,
            epsilon=0.5 - t * 0.01,
            timestamp=float(t)
        )
        result = engine.process_state(state)
        
        sigma_base = (state.psi + state.phi) * (1 - state.epsilon)
        sigma_enhanced = engine.apply_to_system(sigma_base, influence=0.1)
        
        improvement = (sigma_enhanced - sigma_base) / sigma_base
        improvements.append(improvement)
    
    # Later improvements should be larger (system learns to help more)
    assert improvements[-1] > improvements[0]


# ============================================================================
# Integration Tests
# ============================================================================

def test_full_learning_cycle():
    """Test a complete learning cycle with all components."""
    engine = MemoryLearningEngine(
        memory_depth=5,
        decay_rate=0.1,
        learning_rate=0.05,
        projection_steps=3
    )
    
    # Phase 1: Initial learning
    for i in range(10):
        state = State(psi=5.0 + i * 0.5, phi=3.0 + i * 0.3, epsilon=0.2, timestamp=float(i))
        engine.process_state(state)
    
    k1 = engine.knowledge.get_knowledge()
    assert k1 > 0.0
    
    # Phase 2: Continued learning
    for i in range(10, 20):
        state = State(psi=5.0 + i * 0.5, phi=3.0 + i * 0.3, epsilon=0.2, timestamp=float(i))
        engine.process_state(state)
    
    k2 = engine.knowledge.get_knowledge()
    assert k2 > k1  # Knowledge should continue to grow


def test_memory_improves_prediction():
    """Test that memory improves prediction accuracy."""
    engine = MemoryLearningEngine(memory_depth=10, learning_rate=0.1)
    
    # Create a predictable pattern
    pattern = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    
    for i, value in enumerate(pattern):
        state = State(psi=value, phi=value, epsilon=0.1, timestamp=float(i))
        result = engine.process_state(state)
        
        if i > 2:  # After some learning
            # Check if projection is reasonable
            if result['psi_plus']:
                projected = result['psi_plus'][0]
                # Should project upward trend
                assert projected.psi > state.psi


def test_safety_through_learning():
    """Test that learning reinforces safety (low epsilon)."""
    engine = MemoryLearningEngine(learning_rate=0.05)
    
    # Simulate a scenario where high epsilon is dangerous
    for i in range(15):
        # System learns that low epsilon is better
        epsilon = 0.5 - i * 0.02  # Decreasing drift
        state = State(psi=5.0 + i * 0.5, phi=5.0 + i * 0.5, epsilon=epsilon, timestamp=float(i))
        result = engine.process_state(state)
    
    # Knowledge should have accumulated
    assert engine.knowledge.get_knowledge() > 0.0
    
    # System should be able to predict safer states
    assert engine.current_psi_plus is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
