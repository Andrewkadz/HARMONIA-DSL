# Connectives: < > ( ) / : ^
#
# These give Harmonia grouping, comparison, conditional execution,
# depth control, relational contact, and disruption — the pieces that
# turn a statement sequence into a structured program.

import contextlib
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from phi_pi_e_interpreter import PhiPiEInterpreterFixed


def run(program):
    interp = PhiPiEInterpreterFixed()
    with contextlib.redirect_stdout(io.StringIO()):
        result = interp.execute(program)
    return interp, result


class TestGuards:
    """> and < compare AND gate: a failed test abandons the rest of
    the line. This is the language's conditional execution."""

    def test_greater_true(self):
        interp, v = run("#a 5.0\n#b 2.0\n> #a #b")
        assert v == 1.0 and interp.last_context.get_scalar('#cmp') == 1.0

    def test_greater_false(self):
        interp, v = run("#a 1.0\n#b 9.0\n> #a #b")
        assert v == 0.0 and interp.last_context.get_scalar('#cmp') == 0.0

    def test_failed_guard_gates_the_line(self):
        interp, _ = run("#a 1.0\n#b 9.0\n> #a #b #win 42.0")
        assert interp.last_context.get_scalar('#win') == 0.0

    def test_passed_guard_runs_the_line(self):
        interp, _ = run("#a 9.0\n#b 1.0\n> #a #b #win 42.0")
        assert interp.last_context.get_scalar('#win') == 42.0

    def test_less_than(self):
        interp, _ = run("#a 1.0\n#b 9.0\n< #a #b #win 7.0")
        assert interp.last_context.get_scalar('#win') == 7.0

    def test_guard_only_gates_its_own_line(self):
        interp, _ = run("#a 1.0\n#b 9.0\n> #a #b #skipped 5.0\n#after 3.0")
        assert interp.last_context.get_scalar('#skipped') == 0.0
        assert interp.last_context.get_scalar('#after') == 3.0

    def test_guard_accepts_registers_and_literals(self):
        interp, v = run("@a 3.0 4.0\n> @a 4.0")   # |@a| = 5 > 4
        assert v == 1.0

    def test_guard_gates_real_operations(self):
        """Conditional governance: only stabilize if drift is high."""
        interp, _ = run("@a 1.0 0.0\n@b 9.0 0.0\n#drift 0.9\n"
                        "> #drift 0.5 Φ @a @b")
        assert interp.last_context.read_register('@a') != 1 + 0j
        interp2, _ = run("@a 1.0 0.0\n@b 9.0 0.0\n#drift 0.1\n"
                         "> #drift 0.5 Φ @a @b")
        assert interp2.last_context.read_register('@a') == 1 + 0j


class TestGrouping:
    """( ) evaluates a sub-expression whose result becomes the current
    value — so operator output can be piped."""

    def test_group_result_pipes(self):
        interp, _ = run("@a 1.0 2.0\n@b 3.0 4.0\n( Λ @a @b ) → #obs")
        assert abs(interp.last_context.get_scalar('#obs')
                   - interp.last_context.lambda_obs) < 1e-9

    def test_group_executes_contents(self):
        interp, _ = run("( @a 2.0 3.0 )")
        assert interp.last_context.read_register('@a') == 2 + 3j

    def test_nested_groups(self):
        interp, _ = run("( ( @a 1.0 1.0 ) )")
        assert interp.last_context.read_register('@a') == 1 + 1j


class TestDepthEscalation:
    """^ nests a level; '^ n' sets it. Pairs with Θₙ and Π."""

    def test_increment(self):
        interp, _ = run("^\n^\n^")
        assert interp.last_context.get_scalar('#depth') == 3.0

    def test_explicit_set(self):
        interp, _ = run("^\n^ 7")
        assert interp.last_context.get_scalar('#depth') == 7.0

    def test_depth_reaches_theta(self):
        """^ then Θ stores the intention at the escalated depth."""
        interp, _ = run("^ 4\n@a 0.0 0.0\n@g 1.0 0.0\nΘ @a @g")
        assert (('@a', 4) in interp.last_context.intentions)


class TestRelationalInterface:
    """':' creates a contact zone WITHOUT merging (spec: relational
    recursion without immediate merger)."""

    def test_records_relation_and_tension(self):
        interp, v = run("@a 1.0 0.0\n@b 4.0 0.0\n: @a @b")
        assert interp.last_context.relations == [('@a', '@b')]
        assert v == 3.0
        assert interp.last_context.get_scalar('#tension') == 3.0

    def test_does_not_merge(self):
        interp, _ = run("@a 1.0 0.0\n@b 4.0 0.0\n: @a @b")
        assert interp.last_context.read_register('@a') == 1 + 0j
        assert interp.last_context.read_register('@b') == 4 + 0j


class TestDisruption:
    """'/' perturbs a register (spec: disruption/interference)."""

    def test_perturbs_deterministically(self):
        interp, _ = run("#disrupt 0.5\n@a 2.0 0.0\n/ @a")
        assert interp.last_context.read_register('@a') == 2 + 1j

    def test_default_magnitude(self):
        interp, _ = run("@a 2.0 0.0\n/ @a")
        z = interp.last_context.read_register('@a')
        assert z != 2 + 0j and abs(z.imag - 0.2) < 1e-9

    def test_disruption_is_a_rotation_not_a_scaling(self):
        """A real perturbation changes direction, not just magnitude."""
        import cmath
        interp, _ = run("#disrupt 0.3\n@a 4.0 0.0\n/ @a")
        z = interp.last_context.read_register('@a')
        assert abs(cmath.phase(z)) > 1e-6


class TestCorridorIntact:
    def test_canonical_fixture(self):
        interp, result = run("Φ 5.0\nΨ 3.0\nε 0.2\nΣ")
        assert abs(result - 6.4) < 1e-9

    def test_loops_still_work(self):
        interp, _ = run("[Ψ 1]")
        assert interp.last_context.state.psi_signal == 10.0


class TestOmegaClosure:
    """Ω as n⁰ — closure collapses to unity and seals.

    NOTE: this is the interpreter's CLOSURE role for the glyph, not
    the proofs' qualia-gateway Ω (ℂ×ℂ → 𝒬), which is proven to have
    no numerical value and stays unimplemented in the math core.
    """

    def test_closes_to_unity(self):
        interp, v = run("@a 7.0 3.0\nΩ @a")
        assert interp.last_context.read_register('@a') == 1 + 0j
        assert v == 1.0

    def test_sealed_register_refuses_writes(self):
        interp, _ = run("@a 7.0 3.0\nΩ @a\n@b 2.0 0.0\nΦ @a @b")
        assert interp.last_context.read_register('@a') == 1 + 0j
        assert interp.last_context.get_scalar('#sealed_refusals') >= 1.0

    def test_closure_is_terminal_across_operators(self):
        """No operator may revive a sealed register."""
        interp, _ = run("@a 5.0 0.0\n@b 3.0 0.0\nΩ @a\n"
                        "ε @a @b\nΓ @a\nΡ @a @b")
        assert interp.last_context.read_register('@a') == 1 + 0j

    def test_query_reports_seal_state(self):
        i1, v1 = run("@a 1.0 0.0\nΩ? @a")
        i2, v2 = run("@a 1.0 0.0\nΩ @a\nΩ? @a")
        assert v1 == 0.0 and v2 == 1.0

    def test_closure_count(self):
        interp, _ = run("@a 1.0 0.0\n@b 2.0 0.0\nΩ @a\nΩ @b")
        assert interp.last_context.get_scalar('#omega') == 2.0

    def test_seal_composes_with_guards(self):
        """'Ω? @a #done 1.0' — act only on sealed state."""
        interp, _ = run("@a 1.0 0.0\nΩ @a\nΩ? @a #done 1.0")
        assert interp.last_context.get_scalar('#done') == 1.0

    def test_math_core_omega_still_refuses(self):
        """The qualia-gateway Ω remains unimplementable, as proven."""
        import pytest
        from phi_pi_e_math_core import (CATEGORICAL_OPERATORS,
                                        CategoricalBoundaryError)
        with pytest.raises(CategoricalBoundaryError):
            CATEGORICAL_OPERATORS['Ω'](1 + 1j, 2 - 1j)
