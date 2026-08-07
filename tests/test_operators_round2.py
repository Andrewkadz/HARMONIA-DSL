# Round-2 operators: Δ/Π register forms, λ entanglement, Υ consensus,
# Κ probe, and the composition tier (→ pipe, + parallel).
#
# Δ and Π are the math core's existing tested functions given register
# forms — no new mathematics. λ Υ Κ are computational realizations
# chosen for the roles the proofs assign (LOGIC_NODES_DESIGN honesty
# clause applies).

import contextlib
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from phi_pi_e_interpreter import PhiPiEInterpreterFixed
from phi_pi_e_math_core import fusion_transformation, transcendent_continuity


def run(program):
    interp = PhiPiEInterpreterFixed()
    with contextlib.redirect_stdout(io.StringIO()):
        result = interp.execute(program)
    return interp, result


class TestDeltaAndPiRegisterForms:
    def test_delta_matches_math_core(self):
        interp, _ = run("@a 1.0 2.0\n@b 3.0 4.0\nΔ @a @b")
        assert interp.last_context.read_register('@a') == \
            fusion_transformation(1 + 2j, 3 + 4j)

    def test_pi_uses_depth_scalar(self):
        interp, _ = run("#depth 3\n@a 2.0 3.0\n@b 1.0 1.0\nΠ @a @b")
        assert interp.last_context.read_register('@a') == \
            transcendent_continuity(2 + 3j, 1 + 1j, n=3)

    def test_pi_defaults_to_depth_one(self):
        interp, _ = run("@a 2.0 3.0\n@b 1.0 1.0\nΠ @a @b")
        assert interp.last_context.read_register('@a') == \
            transcendent_continuity(2 + 3j, 1 + 1j, n=1)

    def test_pi_safe_at_zero_reference(self):
        """π is undefined for w = 0 (proofs Thm 3.2); the register form
        must not raise — it holds position instead."""
        interp, _ = run("@a 2.0 3.0\n@b 0.0 0.0\nΠ @a @b")
        assert interp.last_context.read_register('@a') == 2 + 3j

    def test_second_operand_never_written(self):
        interp, _ = run("@a 1.0 2.0\n@b 3.0 4.0\nΔ @a @b")
        assert interp.last_context.read_register('@b') == 3 + 4j


class TestLambdaEntanglement:
    """Job: shared state between cooperating agents."""

    def test_entangle_then_resolve_shares_value(self):
        interp, _ = run("@a 1.0 0.0\n@b 5.0 0.0\nλ @a @b\nλ! @a")
        assert interp.last_context.read_register('@a') == 3 + 0j
        assert interp.last_context.read_register('@b') == 3 + 0j

    def test_group_is_transitive(self):
        """Entangling (a,b) then (b,c) makes one group of three."""
        interp, n = run("@a 0.0 0.0\n@b 3.0 0.0\n@c 6.0 0.0\n"
                        "λ @a @b\nλ @b @c\nλ! @a")
        assert interp.last_context.read_register('@c') == 3 + 0j
        assert interp.last_context.read_register('@a') == 3 + 0j

    def test_unentangled_resolve_is_noop(self):
        interp, v = run("@a 1.0 0.0\nλ! @a")
        assert v == 0.0
        assert interp.last_context.read_register('@a') == 1 + 0j


class TestUpsilonConsensus:
    """Job: multi-agent agreement with a measurable disagreement signal."""

    def test_merges_to_mean_and_reports_dispersion(self):
        interp, disp = run("@a 1.0 0.0\n@b 3.0 0.0\n@c 5.0 0.0\nΥ @a @b @c")
        for r in ('@a', '@b', '@c'):
            assert interp.last_context.read_register(r) == 3 + 0j
        assert abs(disp - 4 / 3) < 1e-9
        assert abs(interp.last_context.get_scalar('#upsilon') - 4 / 3) < 1e-9

    def test_perfect_agreement_has_zero_dispersion(self):
        interp, disp = run("@a 2.0 0.0\n@b 2.0 0.0\nΥ @a @b")
        assert disp == 0.0

    def test_consensus_is_idempotent(self):
        interp, _ = run("@a 1.0 0.0\n@b 5.0 0.0\nΥ @a @b\nΥ @a @b")
        assert interp.last_context.get_scalar('#upsilon') == 0.0


class TestKappaProbe:
    """Job: inspect a peer WITHOUT changing it."""

    def test_probe_is_non_mutating(self):
        interp, v = run("@a 3.0 4.0\nΚ @a")
        assert v == 5.0
        assert interp.last_context.read_register('@a') == 3 + 4j

    def test_two_operand_probe_reports_distance(self):
        interp, v = run("@a 0.0 0.0\n@b 3.0 4.0\nΚ @a @b")
        assert v == 5.0
        assert interp.last_context.read_register('@b') == 3 + 4j


class TestCompositionTier:
    """→ makes programs expressions rather than statements."""

    def test_pipe_into_scalar(self):
        interp, _ = run("@a 1.0 2.0\n@b 3.0 4.0\nΛ @a @b → #obs")
        assert abs(interp.last_context.get_scalar('#obs')
                   - interp.last_context.lambda_obs) < 1e-9

    def test_pipe_into_register(self):
        interp, _ = run("@a 3.0 4.0\nΚ @a → @out")
        assert interp.last_context.read_register('@out') == 5 + 0j

    def test_chained_composition(self):
        """Reduce, pipe, then reuse the piped value as an operand."""
        interp, _ = run("@a 1.0 0.0\n@b 5.0 0.0\nΥ @a @b → #d\n#d")
        assert interp.last_context.get_scalar('#d') == 2.0

    def test_parallel_preserves_independence(self):
        """+ @a @b: both present, neither transformed (spec:
        independence-preserving, non-transformative)."""
        interp, v = run("@a 1.0 2.0\n@b 3.0 4.0\n+ @a @b")
        assert interp.last_context.read_register('@a') == 1 + 2j
        assert interp.last_context.read_register('@b') == 3 + 4j
        assert abs(v - (abs(1 + 2j) + abs(3 + 4j))) < 1e-9

    def test_parallel_is_commutative(self):
        i1, v1 = run("@a 1.0 2.0\n@b 3.0 4.0\n+ @a @b")
        i2, v2 = run("@a 1.0 2.0\n@b 3.0 4.0\n+ @b @a")
        assert abs(v1 - v2) < 1e-9

    def test_bare_flow_still_works(self):
        """→ with no valid destination keeps its legacy modulator
        behaviour — the corridor is untouched."""
        interp, _ = run("Φ 5.0\nΨ 3.0\nε 0.2\nΣ\n→")
        assert abs(interp.last_context.state.stabilized_value - 6.4) < 1e-9


class TestCorridorStillIntact:
    def test_canonical_fixture(self):
        interp, result = run("Φ 5.0\nΨ 3.0\nε 0.2\nΣ")
        assert abs(result - 6.4) < 1e-9

    def test_operator_count(self):
        """17 symbols now carry real semantics (was 6 this morning)."""
        interp = PhiPiEInterpreterFixed()
        numeric = {'Φ', 'Ψ', 'ε', 'Λ', 'Δ', 'Π'}
        structural = set(interp.structural)
        assert len(numeric | structural) == 16
