# Tests for LOGIC_NODES_DESIGN — scalar field + structural operators.
#
# These are computational realizations chosen to fulfil the roles the
# Φπε proofs assign to Σ ζ Ξ Γ Τ. They are NOT derivations from the
# proofs. Each node has a Job and a Falsifier per the design doc.

import contextlib
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from phi_pi_e_interpreter import FieldContext, PhiPiEInterpreterFixed


def run(program, ctx=None):
    interp = PhiPiEInterpreterFixed()
    with contextlib.redirect_stdout(io.StringIO()):
        result = interp.execute(program, ctx) if ctx else interp.execute(program)
    return interp, result


class TestScalarField:
    def test_set_and_read(self):
        interp, result = run("#budget 42.5\n#budget")
        assert interp.last_context.get_scalar('#budget') == 42.5
        assert result == 42.5

    def test_unset_reads_zero(self):
        ctx = FieldContext()
        assert ctx.get_scalar('#nothing') == 0.0

    def test_scalars_are_a_distinct_token_class(self):
        interp = PhiPiEInterpreterFixed()
        assert interp.is_scalar_token('#budget')
        assert not interp.is_scalar_token('@z')
        assert not interp.is_register_token('#budget')
        assert interp.tokenize(interp.clean_input("#a 1.0")) == ['#a', '1.0']

    def test_comments_still_work(self):
        """'# text' is a comment; '#name' is a scalar. The canonical
        fixture's inline comments must survive."""
        interp = PhiPiEInterpreterFixed()
        assert interp.clean_input("Φ 5.0    # Set tension to 5.0") == "Φ 5.0"
        assert interp.clean_input("#gain 3.0  # a comment") == "#gain 3.0"

    def test_isolation_from_pinned_state(self):
        interp, _ = run("Φ 5.0\nΨ 3.0\nε 0.2\n#x 99.0\nΣ")
        s = interp.last_context.state
        assert (s.phi_state, s.psi_signal, s.epsilon_drift) == (5.0, 3.0, 0.2)
        assert abs(s.stabilized_value - 6.4) < 1e-9
        assert interp.last_context.get_scalar('#x') == 99.0

    def test_scalars_shared_across_forks(self):
        ctx = FieldContext()
        ctx.set_scalar('#s', 7.0)
        assert ctx.fork().get_scalar('#s') == 7.0


class TestSigmaSuperposition:
    """Job: hold plurality without collapsing it."""

    def test_holds_members_without_collapse(self):
        interp, n = run("@a 1.0 0.0\n@b 3.0 4.0\nΣ @a @b")
        sup = interp.last_context.superpositions['@a']
        assert sup == [1 + 0j, 3 + 4j]
        assert n == 2
        # the register itself is NOT reduced
        assert interp.last_context.read_register('@a') == 1 + 0j

    def test_collapse_selects_strongest(self):
        interp, mag = run("@a 1.0 0.0\n@b 3.0 4.0\nΣ @a @b\nΣ! @a")
        assert interp.last_context.read_register('@a') == 3 + 4j
        assert abs(mag - 5.0) < 1e-9

    def test_n_ary(self):
        interp, n = run("@a 1.0 0.0\n@b 2.0 0.0\n@c 3.0 0.0\nΣ @a @b @c")
        assert n == 3


class TestZetaRecurrence:
    """Job/Falsifier: detect CYCLES, which flat-round counting cannot
    see because the state keeps changing while repeating."""

    def test_no_recurrence_on_first_sight(self):
        interp, d = run("@a 1.0 1.0\nζ @a")
        assert d == 0.0

    def test_detects_exact_cycle(self):
        prog = ("@a 1.0 0.0\nζ @a\n@a 2.0 0.0\nζ @a\n"
                "@a 3.0 0.0\nζ @a\n@a 1.0 0.0\nζ @a")
        interp, depth = run(prog)
        assert depth == 3.0          # the 1.0 state recurs 3 steps back
        assert interp.last_context.get_scalar('#zeta') == 3.0

    def test_falsifier_flat_counting_would_miss_it(self):
        """In a 3-cycle every step changes the state, so a
        'no-improvement' counter never fires; ζ does."""
        prog = ("@a 1.0 0.0\nζ @a\n@a 2.0 0.0\nζ @a\n@a 1.0 0.0\nζ @a")
        interp, depth = run(prog)
        assert depth > 0                      # ζ sees the loop
        states = [1 + 0j, 2 + 0j, 1 + 0j]
        assert states[-1] != states[-2]       # a flat-counter sees change


class TestXiComposition:
    """Job: coalition — two states form a unit."""

    def test_composite_and_membership(self):
        interp, _ = run("@a 1.0 0.0\n@b 3.0 0.0\nΞ @a @b")
        assert interp.last_context.composites['@a'] == ['@a', '@b']
        composed = interp.last_context.read_register('@a')
        assert composed != 1 + 0j              # actually combined
        assert interp.last_context.read_register('@b') == 3 + 0j  # untouched

    def test_composition_is_bounded(self):
        """Ξ uses a Φ-stabilized combination, so it cannot amplify
        beyond the sum of its parts."""
        interp, _ = run("@a 2.0 0.0\n@b 3.0 0.0\nΞ @a @b")
        assert abs(interp.last_context.read_register('@a')) <= 5.0 + 1e-9


class TestGammaLineage:
    """Job: evolution with identity preservation."""

    def test_generation_and_lineage(self):
        interp, gen = run("@a 1.0 0.0\nΓ @a\nΓ @a\nΓ @a")
        assert gen == 3.0
        assert len(interp.last_context.lineage['@a']) == 3
        assert interp.last_context.get_scalar('#gamma') == 3.0

    def test_lineage_is_never_lost(self):
        """The testable invariant: prior states remain recoverable."""
        interp, _ = run("@a 1.0 0.0\nΓ @a\nΓ @a")
        lin = interp.last_context.lineage['@a']
        assert lin[0] == 1 + 0j
        assert all(abs(v) > 0 for v in lin)

    def test_generation_is_monotone(self):
        interp, _ = run("@a 1.0 0.0\nΓ @a\nΓ @a\nΓ @a\nΓ @a")
        assert interp.last_context.get_scalar('#gamma') == 4.0


class TestTauPhaseLock:
    """Job: synchronized action."""

    def test_aligns_phase_and_reports(self):
        interp, alignment = run("@a 1.0 1.0\n@r 2.0 0.0\nΤ @a @r")
        locked = interp.last_context.read_register('@a')
        assert abs(locked.imag) < 1e-9          # aligned to the real axis
        assert abs(abs(locked) - abs(1 + 1j)) < 1e-9   # magnitude preserved
        assert 0.0 <= alignment <= 1.0

    def test_already_aligned_scores_one(self):
        interp, alignment = run("@a 2.0 0.0\n@r 5.0 0.0\nΤ @a @r")
        assert abs(alignment - 1.0) < 1e-9

    def test_opposed_scores_zero(self):
        interp, alignment = run("@a 1.0 0.0\n@r -1.0 0.0\nΤ @a @r")
        assert abs(alignment) < 1e-9


class TestCorridorIntact:
    def test_canonical_fixture_unchanged(self):
        interp, result = run("Φ 5.0\nΨ 3.0\nε 0.2\nΣ")
        assert abs(result - 6.4) < 1e-9
        assert interp.last_context.superpositions == {}

    def test_bare_sigma_is_still_the_reducer(self):
        """Operand-kind dispatch: bare Σ reduces, Σ with registers
        superposes. Both live in the same program."""
        interp, result = run("Φ 5.0\nΨ 3.0\nε 0.2\nΣ\n@a 1.0 0.0\n@b 2.0 0.0\nΣ @a @b")
        assert interp.last_context.superpositions['@a'] == [1 + 0j, 2 + 0j]
        assert abs(interp.last_context.state.stabilized_value - 6.4) < 1e-9
