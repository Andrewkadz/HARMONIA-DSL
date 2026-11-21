# Errata tests for the Φπε math core — verified 2026-08-11.
#
# These pin properties that the proofs PDF states incorrectly. Same
# convention as the existing ε errata already documented in
# phi_pi_e_math_core.incremental_insight: where the PDF and the
# computation disagree, the computation is authoritative.
#
# Two independent errata:
#   E1 (Φ): Thms 4.1 and 4.2 fail on the zero-sum family z + w = 0.
#   E2 (π): Thm 4.1's non-termination is false. |π^n(z,w)| converges
#           to the Thm 4.2 bound π·|w|, which is an attractor, not a
#           ceiling. The existing test_non_termination passes only
#           because its 40-step window is too short to see it.

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from phi_pi_e_math_core import (
    PI_RATIONAL,
    harmonic_equilibrium,
    pi_iterate,
    transcendent_continuity,
)

ZERO_SUM = [1 + 0j, 2.5 + 0j, 3 + 4j, -7j, 0.001 + 0.002j]


class TestPhiZeroSumErratum:
    """Φ Thms 4.1 / 4.2 require the unstated hypothesis z + w ≠ 0."""

    @pytest.mark.parametrize("a", ZERO_SUM)
    def test_non_fusional_fails_on_zero_sum(self, a):
        """Thm 4.1 claims Φ(z,w) ≠ z+w for z ≠ w. False when z+w = 0.

        Proof step 'c·x ≠ x for c ∈ (0,1)' holds only for x ≠ 0.
        """
        z, w = a, -a
        assert z != w
        assert harmonic_equilibrium(z, w) == z + w  # the counterexample

    @pytest.mark.parametrize("a", ZERO_SUM)
    def test_stability_equality_without_z_equals_w(self, a):
        """Thm 4.2 claims |Φ| = |z+w| iff z = w. False when z+w = 0."""
        z, w = a, -a
        assert z != w
        assert abs(harmonic_equilibrium(z, w)) == abs(z + w)

    @pytest.mark.parametrize("a", ZERO_SUM)
    def test_corrected_statements_hold(self, a):
        """Both theorems are true once z + w ≠ 0 is assumed."""
        z, w = a, -a + 1  # perturb off the zero-sum line
        if z == w or z + w == 0:
            pytest.skip("degenerate")
        assert harmonic_equilibrium(z, w) != z + w
        assert abs(harmonic_equilibrium(z, w)) < abs(z + w)


class TestPiConvergenceErratum:
    """π Thm 4.1 (non-termination) contradicts Thm 4.2 (bound)."""

    def test_fixed_depth_orbit_reaches_fixed_point(self):
        """With n held fixed — the literal reading of Def 3.1, where n
        is a free parameter — the orbit converges to a fixed point of
        modulus exactly π·|w|. Thm 4.1 asserts this cannot happen."""
        w = 1 + 0j
        for n in (1, 5, 50):
            o = 3 + 4j
            for _ in range(300):
                o = transcendent_continuity(o, w, n=n)
            assert abs(abs(o) - PI_RATIONAL * abs(w)) < 1e-9
            assert abs(transcendent_continuity(o, w, n=n) - o) < 1e-9

    def test_modulus_converges_to_the_bound(self):
        """With n = step index (pi_iterate's convention) the modulus
        still converges to π·|w|. The Thm 4.2 bound is an attractor."""
        w = 1 + 1j
        trail = pi_iterate(2 + 3j, w, steps=20_000)
        assert abs(abs(trail[-1]) - PI_RATIONAL * abs(w)) < 1e-12

    def test_step_size_decays_to_zero(self):
        """Motion per step decays geometrically. test_non_termination
        asserts every recent move exceeds 1e-6; true at 40 steps,
        false by 5000."""
        w = 1 + 1j
        short = pi_iterate(2 + 3j, w, steps=40)
        long_ = pi_iterate(2 + 3j, w, steps=5_000)
        m_short = [abs(b - a) for a, b in zip(short[-10:], short[-9:])]
        m_long = [abs(b - a) for a, b in zip(long_[-10:], long_[-9:])]
        assert all(m > 1e-6 for m in m_short)      # the old test's window
        assert not all(m > 1e-6 for m in m_long)   # the same claim, refuted

    def test_modulus_never_exceeds_bound(self):
        """Thm 4.2 itself stands — this is the salvageable half."""
        w = 1 + 1j
        for z in trail_starts():
            for v in pi_iterate(z, w, steps=200):
                assert abs(v) <= PI_RATIONAL * abs(w) + 1e-9


def trail_starts():
    return [2 + 3j, -5 + 0.5j, 0.01 + 0.01j, 100 + 100j]
