"""Invariant tests for the RI1 Epistemodynamics thermodynamic experiment.

The tests verify formulas, bounds, accounting, and determinism.  They do not
assert that a Φ policy is empirically superior: that is an experimental result
which depends on explicitly exposed model parameters.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from experiments.epistemodynamic_thermodynamics import (
    AdaptivePhi,
    FixedPhi,
    NoMediation,
    Phase,
    ThermoParameters,
    adaptive_phi_strength,
    closed_system_conservation_audit,
    coherence_optimal,
    energy_accounting_error,
    law4_entropy_production,
    law5_allowed_reduction,
    phase_of,
    run_open_system,
    run_policy_comparison,
    structural_energy,
)


def test_law2_structural_energy_formula():
    assert structural_energy(2.0, 0.25, 0.5) == pytest.approx(1.75)


def test_law4_entropy_production_is_suppressed_by_coherence():
    high_coherence = law4_entropy_production(0.90, 0.70, 0.005, 0.12)
    low_coherence = law4_entropy_production(0.10, 0.70, 0.005, 0.12)
    assert high_coherence < low_coherence


def test_law5_reduction_is_bounded_by_request_and_coherence_capacity():
    requested = 0.04
    no_coherence = law5_allowed_reduction(requested, 1.0, 0.0, 0.5)
    partial_coherence = law5_allowed_reduction(requested, 0.5, 0.25, 0.5)
    full_capacity = law5_allowed_reduction(requested, 1.0, 1.0, 0.5)
    assert no_coherence == 0.0
    assert 0.0 < partial_coherence < full_capacity
    assert full_capacity == requested


def test_law11_adaptive_phi_responds_to_entropy_coherence_imbalance():
    assert adaptive_phi_strength(0.80, 0.20) == pytest.approx(0.80)
    assert adaptive_phi_strength(0.20, 0.80) == pytest.approx(0.20)
    assert AdaptivePhi().phi(0.60, 0.60) == pytest.approx(0.50)


def test_law12_coherence_target_relaxes_as_entropy_rises():
    assert coherence_optimal(0.20) == pytest.approx(0.80)
    assert coherence_optimal(0.80) == pytest.approx(0.50)


def test_law6_and_law20_phase_boundaries():
    assert phase_of(0.84, 0.50) is Phase.SAFE
    assert phase_of(0.90, 0.50) is Phase.DANGER
    assert phase_of(0.95, 0.50) is Phase.COLLAPSED
    assert phase_of(0.50, 0.05) is Phase.COLLAPSED


def test_closed_law2_audit_requires_higher_coherence_when_entropy_increases():
    mass = 1.0
    entropy_before = 0.35
    coherence_before = 0.72
    total_energy = structural_energy(mass, entropy_before, coherence_before)
    audit = closed_system_conservation_audit(
        mass, total_energy, entropy_before, entropy_before + 0.10,
        coherence_before,
    )
    assert audit.feasible
    assert audit.coherence_required_after is not None
    assert audit.coherence_required_after > coherence_before


def test_open_system_trace_preserves_declared_total_energy_accounting():
    result = run_open_system(AdaptivePhi(), ThermoParameters(steps=30))
    for state in result.trace:
        assert 0.0 <= state.entropy <= 1.0
        assert 0.0 <= state.coherence <= 1.0
        assert state.reservoir >= -1e-12
        assert abs(energy_accounting_error(state, result.parameters)) < 1e-12


def test_experiment_is_deterministic():
    parameters = ThermoParameters(steps=30)
    first = run_open_system(FixedPhi(), parameters)
    second = run_open_system(FixedPhi(), parameters)
    assert first.trace == second.trace
    assert first.summary() == second.summary()


def test_policy_comparison_runs_three_declared_conditions():
    results = run_policy_comparison(ThermoParameters(steps=10))
    assert [result.policy for result in results] == [
        NoMediation().name,
        FixedPhi().name,
        AdaptivePhi().name,
    ]
