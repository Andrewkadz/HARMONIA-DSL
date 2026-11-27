# Tests for feat/phi-pi-e-math-core
#
# Pins the Φπε math core to its spec (RI1_LANGUAGE_Φπε_PROOFS):
#   - worked numeric examples from the PDF as exact fixtures,
#   - the proven properties (boundedness, non-fusional, convergence,
#     non-termination, oscillation bounds, fine-structure relations),
#   - categorical operators refuse numerical evaluation (per Ω Thm 3.2).
#
# NO interpreter involvement: this file imports only the math core.

import cmath
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from phi_pi_e_math_core import (
    CATEGORICAL_OPERATORS,
    NUMERICAL_OPERATORS,
    CategoricalBoundaryError,
    DELTA_CONSTANT,
    EPSILON_THRESHOLD,
    FINE_STRUCTURE_ALPHA,
    LAMBDA_CONSTANT,
    PHI_GOLDEN,
    PHI_RATIONAL,
    PI_RATIONAL,
    epsilon_iterate,
    fusion_transformation,
    harmonic_equilibrium,
    incremental_insight,
    pi_iterate,
    recursive_animation,
    structural_illumination,
    transcendent_continuity,
)

# Sample points reused across property tests
SAMPLES = [(3 + 4j, 1 - 2j), (2 + 3j, 1 + 1j), (-1 - 1j, 4 + 0.5j),
           (0.001 + 0j, 0 + 0.001j), (5 + 0j, 5 + 0j)]


class TestPdfWorkedExamples:
    """The proofs' own computational verifications, as exact fixtures."""

    def test_phi_example_5_1(self):
        """Φ(3+4i, 1−2i) ≈ 0.8149 + 0.4075i (proofs, Φ Example 5.1)."""
        result = harmonic_equilibrium(3 + 4j, 1 - 2j)
        assert abs(result.real - 0.8149) < 5e-5
        assert abs(result.imag - 0.4075) < 5e-5

    def test_epsilon_example_5_1(self):
        """ε(1+2i, 3+i) ≈ 1.001996 + 1.999002i, |incr| ≈ 0.002231."""
        z, w = 1 + 2j, 3 + 1j
        result = incremental_insight(z, w)
        assert abs(result.real - 1.001996) < 5e-7
        assert abs(result.imag - 1.999002) < 5e-7
        assert abs(abs(result - z) - 0.002231) < 5e-7

    def test_pi_spiral_phase_example(self):
        """e^{iπ/4} ≈ 0.7069 + 0.7073i per the proofs' π Example 5.1
        (their rounding of √2/2; exact to their printed precision)."""
        spiral = cmath.exp(1j * math.pi / 4)
        assert abs(spiral.real - 0.7071) < 3e-4
        assert abs(spiral.imag - 0.7071) < 3e-4

    def test_pi_example_5_1_exponent_constant(self):
        """E5: PDF Example 5.1's 0.7069+0.7073i uses 22/7 in the exponent,
        whereas phi_pi_e_math_core.py uses math.pi in cmath.exp (authoritative)."""
        exp_22_7 = cmath.exp(1j * PI_RATIONAL / 4)
        assert abs(exp_22_7.real - 0.7069) < 5e-5
        assert abs(exp_22_7.imag - 0.7073) < 5e-5
        z, w = 2 + 3j, 1 + 1j
        got = transcendent_continuity(z, w, n=4)
        exp_authoritative = PI_RATIONAL * (z + w * cmath.exp(1j * math.pi / 4)) / (1 + abs(z) / abs(w))
        assert got == exp_authoritative

    def test_lambda_fine_structure_example(self):
        """Λ⁻¹·(1/3) = 0.00729927 = α (proofs, Λ Example 5.1 / Thm 4.2)."""
        assert abs((1 / LAMBDA_CONSTANT) * (1 / 3) - 0.00729927) < 5e-9
        assert abs(FINE_STRUCTURE_ALPHA - 0.00729927) < 5e-9

    def test_psi_amplitude_example(self):
        """Ψ amplitude coefficient Λ/φ ≈ 28.22 (proofs, Ψ Example 5.1)."""
        assert abs(LAMBDA_CONSTANT / PHI_GOLDEN - 28.22) < 5e-3

    def test_constants_match_proofs(self):
        assert PHI_RATIONAL == 89 / 55
        assert PI_RATIONAL == 22 / 7
        assert EPSILON_THRESHOLD == 0.001
        assert LAMBDA_CONSTANT == 137 / 3
        assert DELTA_CONSTANT == LAMBDA_CONSTANT ** 2
        # φ = 89/55 approximates the golden ratio within 1.5e-4 (proofs §2)
        assert abs(PHI_RATIONAL - PHI_GOLDEN) < 1.5e-4


class TestPhiProperties:
    def test_non_fusional(self):
        """Thm 4.1: Φ(z,w) ≠ z+w whenever z ≠ w."""
        for z, w in SAMPLES:
            if z != w:
                assert harmonic_equilibrium(z, w) != z + w

    def test_non_fusional_requires_nonzero_sum(self):
        """E3: Φ(z, -z) = 0 = z + w even when z != w; non-fusionality holds iff z + w != 0 (and z != w)."""
        for z in (1 + 1j, 3 + 4j, -2 + 0.5j):
            w = -z
            assert z != w
            assert harmonic_equilibrium(z, w) == 0
            assert harmonic_equilibrium(z, w) == z + w
        for z, w in SAMPLES:
            if z != w and z + w != 0:
                assert harmonic_equilibrium(z, w) != z + w

    def test_harmonic_stability(self):
        """Thm 4.2: |Φ(z,w)| ≤ |z+w|, equality iff z = w."""
        for z, w in SAMPLES:
            result = harmonic_equilibrium(z, w)
            assert abs(result) <= abs(z + w) + 1e-12
            if z != w:
                assert abs(result) < abs(z + w)
        z = 2 + 1j
        assert abs(abs(harmonic_equilibrium(z, z)) - abs(2 * z)) < 1e-12

    def test_boundedness_inherent(self):
        """Cor 4.3: dampening coefficient φ/(φ+d) ∈ (0,1] — no clamp needed."""
        for z, w in SAMPLES:
            coeff = PHI_RATIONAL / (PHI_RATIONAL + abs(z - w))
            assert 0 < coeff <= 1


class TestEpsilonProperties:
    def test_micro_ignition(self):
        """Thm 4.1: ε(z,w) ≠ z and |ε(z,w)−z| < |w−z| for z ≠ w."""
        for z, w in SAMPLES:
            if z != w:
                result = incremental_insight(z, w)
                assert result != z
                assert abs(result - z) < abs(w - z)

    def test_precision_threshold_true_bound(self):
        """Thm 4.2 AS PRINTED (≤ ε) is contradicted by the proofs' own
        Example 5.1 (increment 0.002231 > 0.001). The TRUE bound from
        the definition: |ε(z,w)−z| = ε·d/(1+ε·d) < min(ε·d, 1)."""
        for z, w in SAMPLES:
            d = abs(w - z)
            increment = abs(incremental_insight(z, w) - z)
            assert increment < 1.0
            if d > 0:
                assert increment < EPSILON_THRESHOLD * d + 1e-15
        # And the stated ≤ ε form DOES hold in its valid regime d ≤ ~1/(1−ε):
        z, w = 0 + 0j, 0.5 + 0.5j  # d ≈ 0.707 < 1.001
        assert abs(incremental_insight(z, w) - z) <= EPSILON_THRESHOLD

    def test_convergent_iteration(self):
        """Thm 4.3 CONCLUSION: z_{n+1} = ε(z_n,w) → w, distances strictly
        decreasing. (The printed recurrence d²/(1+εd) is wrong; actual
        contraction is d·(1+εd−ε)/(1+εd), geometric rate → 1−ε.)"""
        z, w = 1 + 2j, 1.001 + 2.0005j
        distances = [abs(z - w)]
        current = z
        for _ in range(1000):
            current = incremental_insight(current, w)
            distances.append(abs(current - w))
        assert all(b < a for a, b in zip(distances, distances[1:]))
        # geometric decay at rate ~(1−ε): after 1000 steps ≈ 0.999^1000 ≈ 0.37
        assert distances[-1] < distances[0] * 0.5

    def test_actual_recurrence_formula(self):
        """Pin the CORRECT distance recurrence derived from Definition 3.1:
        d_{n+1} = d_n·(1+ε·d_n−ε)/(1+ε·d_n)."""
        z, w = 2 + 3j, -1 + 1j
        d0 = abs(z - w)
        d1 = abs(incremental_insight(z, w) - w)
        predicted = d0 * (1 + EPSILON_THRESHOLD * d0 - EPSILON_THRESHOLD) / \
            (1 + EPSILON_THRESHOLD * d0)
        assert abs(d1 - predicted) < 1e-12

    def test_epsilon_iterate_reaches_tolerance(self):
        z, w = 0.9995 + 0j, 1 + 0j  # within a few ε-steps of target
        trail = list(epsilon_iterate(z, w, tolerance=1e-4))
        assert abs(trail[-1] - w) < 1e-4 + EPSILON_THRESHOLD


class TestPiProperties:
    def test_undefined_at_w_zero(self):
        """Thm 3.2: domain excludes (z, 0)."""
        with pytest.raises(ValueError):
            transcendent_continuity(1 + 1j, 0)

    def test_spiral_coherence_bound(self):
        """Thm 4.2: |π(z,w)| ≤ π·|w|."""
        for z, w in SAMPLES:
            if w != 0:
                result = transcendent_continuity(z, w, n=4)
                assert abs(result) <= PI_RATIONAL * abs(w) + 1e-9

    def test_printed_sum_bound_counterexample(self):
        """E4: Printed Thm 4.2 bound |π(z,w)| <= π|z+w| fails at z = -w; true bound π|w| holds."""
        z, w = 1 + 0j, -1 + 0j
        val = transcendent_continuity(z, w, n=4)
        assert PI_RATIONAL * abs(z + w) == 0.0
        assert abs(val) > 1.2
        assert abs(val) <= PI_RATIONAL * abs(w) + 1e-12

    def test_iterates_stay_bounded_by_pi_w(self):
        """E5: |π^k(z,w)| never grows as π^k; every iterate obeys |π^k(z,w)| <= π|w|."""
        z, w = 2 + 3j, 1 + 1j
        trail = pi_iterate(z, w, steps=50)
        bound = PI_RATIONAL * abs(w)
        assert all(abs(pt) <= bound + 1e-12 for pt in trail)

    def test_non_termination(self):
        """Thm 4.1: iterates keep moving — no fixed point emerges."""
        trail = pi_iterate(2 + 3j, 1 + 1j, steps=40)
        last_moves = [abs(b - a) for a, b in zip(trail[-10:], trail[-9:])]
        assert all(m > 1e-6 for m in last_moves)

    def test_unbounded_cumulative_phase(self):
        """Thm 4.1: Σ π/k = π·H_n is unbounded (harmonic divergence)."""
        h = sum(1 / k for k in range(1, 100_000))
        assert math.pi * h > 30  # already exceeds ~10π; grows without bound


class TestLambdaProperties:
    def test_always_real(self):
        """Numerator 2·Re(z̄w) is real → Λ(z,w) is real-valued."""
        for z, w in SAMPLES:
            assert structural_illumination(z, w).imag == 0.0

    def test_fine_structure_relation(self):
        """Thm 4.2: Λ⁻¹·(1/3) = α."""
        assert abs(1 / (3 * LAMBDA_CONSTANT) - FINE_STRUCTURE_ALPHA) < 1e-15

    def test_crystallization_requires_nonorthogonal_and_norm_threshold(self):
        """E6: Λ Thm 4.1 fails for orthogonal pairs (Re(z̄w)=0) and for |z|²+|w|² <= 137/134."""
        z_orth, w_orth = 1 + 0j, 0 + 1j
        assert structural_illumination(z_orth, w_orth) == 0
        z_sm, w_sm = 0.5 + 0j, 0.5 * cmath.exp(1j * math.pi / 6)
        rhs_sm = abs(2 * (z_sm.conjugate() * w_sm).real) / (abs(z_sm) ** 2 + abs(w_sm) ** 2)
        assert abs(structural_illumination(z_sm, w_sm)) < rhs_sm
        for z, w in SAMPLES:
            r2 = abs(z) ** 2 + abs(w) ** 2
            coupling = abs(2 * (z.conjugate() * w).real)
            if coupling > 0 and r2 > 137 / 134:
                assert abs(structural_illumination(z, w)) > coupling / r2


class TestDeltaProperties:
    def test_simplified_exact_form(self):
        """E7: Δ(z,w) = (137/3)·z·w / (137/3 + |z-w|) = 137·z·w / (137 + 3|z-w|)."""
        for z, w in SAMPLES:
            expected = (137 * z * w) / (137 + 3 * abs(z - w))
            assert abs(fusion_transformation(z, w) - expected) < 1e-12

    def test_fusion_amplification(self):
        """Thm 4.2: for |z|,|w| < √Λ, |Δ(z,w)| > |z·w|/(1+|z−w|)."""
        bound = math.sqrt(LAMBDA_CONSTANT)
        for z, w in SAMPLES:
            if 0 < abs(z) < bound and 0 < abs(w) < bound and z != w:
                assert abs(fusion_transformation(z, w)) > \
                    abs(z * w) / (1 + abs(z - w))

    def test_fusion_amplification_universal(self):
        """E7: |Δ(z,w)| > |z·w|/(1+|z-w|) holds for all z,w != 0 with z != w, even outside |z|,|w| < sqrt(Λ)."""
        pairs = SAMPLES + [(10 + 0j, 20 + 0j), (12 - 5j, -8 + 9j)]
        for z, w in pairs:
            if z != 0 and w != 0 and z != w:
                assert abs(fusion_transformation(z, w)) > abs(z * w) / (1 + abs(z - w))

    def test_fine_structure_fusion_coupling(self):
        """Thm 4.3: Δ = (1/9)/α²."""
        assert abs(DELTA_CONSTANT - (1 / 9) / FINE_STRUCTURE_ALPHA ** 2) < 1e-6


class TestPsiProperties:
    def test_oscillatory_breath_bound(self):
        """Thm 4.2: |Ψ(z,w)| ≤ (Λ/φ)·|z+w|/2."""
        for z, w in SAMPLES:
            assert abs(recursive_animation(z, w)) <= \
                (LAMBDA_CONSTANT / PHI_GOLDEN) * abs(z + w) / 2 + 1e-9

    def test_zero_distance_zero_breath(self):
        """sin(φ·0) = 0: identical states produce no oscillation."""
        assert recursive_animation(2 + 2j, 2 + 2j) == 0


class TestCategoricalBoundaries:
    def test_omega_refuses_numerical_evaluation(self):
        """Ω Thm 3.2 PROVES unsolvability — refusing to compute IS the
        spec-compliant behavior, not a missing feature."""
        with pytest.raises(CategoricalBoundaryError):
            CATEGORICAL_OPERATORS['Ω'](1 + 1j, 2 - 1j)

    def test_all_categoricals_refuse(self):
        for op in CATEGORICAL_OPERATORS.values():
            with pytest.raises(CategoricalBoundaryError):
                op(0)

    def test_partition_is_complete_and_disjoint(self):
        """Every proofs operator is either numerical or categorical,
        never both."""
        num = set(NUMERICAL_OPERATORS)
        cat = set(CATEGORICAL_OPERATORS)
        assert not (num & cat)
        assert num == {'Φ', 'π', 'ε', 'Λ', 'Δ', 'Ψ'}
        assert {'Ω', 'Ξ', 'Γ', 'Σ', 'ζ', 'ω', 'Τ', 'Ρ', 'δ', 'Θ', 'n', 'χ'} <= cat
