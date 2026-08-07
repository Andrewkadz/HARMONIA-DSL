# Tests for feat/bridge-step2-register-syntax — BRIDGE_DESIGN Step 2
#
# Register syntax (@name), initialization form (@z RE IM, exactly two
# numeric args), and Λ register reduction into context.lambda_obs.
# Pins the ratified resolved items 1-3 and the dispatch prohibitions
# (mixed forms rejected; no non-Λ symbol accepts registers in Step 2).

import contextlib
import io
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from phi_pi_e_interpreter import FieldContext, PhiPiEInterpreterFixed
from phi_pi_e_math_core import structural_illumination


def run(program, ctx=None):
    interp = PhiPiEInterpreterFixed()
    with contextlib.redirect_stdout(io.StringIO()):
        if ctx is None:
            result = interp.execute(program)
        else:
            result = interp.execute(program, ctx)
    return interp, result


def run_raises(program):
    interp = PhiPiEInterpreterFixed()
    with contextlib.redirect_stdout(io.StringIO()):
        with pytest.raises(RuntimeError):
            interp.execute(program)


class TestRegisterTokenization:
    def test_register_is_single_token(self):
        interp = PhiPiEInterpreterFixed()
        assert interp.tokenize(interp.clean_input("@z 1.0 2.0")) == \
            ['@z', '1.0', '2.0']

    def test_register_names_with_underscores_and_digits(self):
        interp = PhiPiEInterpreterFixed()
        tokens = interp.tokenize(interp.clean_input("@epsilon_reg2 0.5 -0.5"))
        assert tokens == ['@epsilon_reg2', '0.5', '-0.5']

    def test_register_distinct_operand_kind(self):
        interp = PhiPiEInterpreterFixed()
        assert interp.is_register_token('@z')
        assert not interp.is_register_token('5.0')
        assert not interp.is_number_token('@z')
        assert not interp.is_register_token('Φ')


class TestRegisterInitialization:
    def test_init_creates_complex_value(self):
        interp, _ = run("@z 1.0 2.0")
        assert interp.last_context.read_register('@z') == 1 + 2j

    def test_reinit_overwrites_cleanly(self):
        interp, _ = run("@z 1.0 2.0\n@z 3.0 4.0")
        assert interp.last_context.read_register('@z') == 3 + 4j

    def test_negative_components(self):
        interp, _ = run("@w -1.5 -0.25")
        assert interp.last_context.read_register('@w') == complex(-1.5, -0.25)

    def test_unset_registers_still_read_zero(self):
        interp, _ = run("@z 1.0 2.0")
        assert interp.last_context.read_register('@never_set') == 0j

    def test_zero_args_rejected(self):
        run_raises("@z")

    def test_one_arg_rejected(self):
        run_raises("@z 1.0")

    def test_three_args_rejected(self):
        run_raises("@z 1.0 2.0 3.0")

    def test_non_numeric_args_rejected(self):
        run_raises("@z a b")  # letters are not numeric operands


class TestLambdaReduction:
    def test_lambda_reduces_to_lambda_obs(self):
        interp, result = run("@z 2.0 3.0\n@w 1.0 -2.0\nΛ @z @w")
        expected = structural_illumination(2 + 3j, 1 - 2j).real
        assert abs(interp.last_context.lambda_obs - expected) < 1e-12
        assert result == interp.last_context.lambda_obs

    def test_lambda_obs_defaults_to_zero(self):
        ctx = FieldContext()
        assert ctx.lambda_obs == 0.0

    def test_lambda_never_touches_pinned_scalars(self):
        interp, _ = run("Φ 5.0\nΨ 3.0\nε 0.2\n@z 2.0 3.0\n@w 1.0 -2.0\nΛ @z @w\nΣ")
        s = interp.last_context.state
        # pinned scalars exactly as the canonical fixture demands:
        assert (s.phi_state, s.psi_signal, s.epsilon_drift) == (5.0, 3.0, 0.2)
        assert abs(s.stabilized_value - 6.4) < 1e-9
        assert interp.last_context.lambda_obs != 0.0

    def test_mixed_form_rejected(self):
        run_raises("@z 2.0 3.0\nΛ @z 1.0")

    def test_single_register_rejected(self):
        run_raises("@z 2.0 3.0\nΛ @z")

    def test_legacy_unary_lambda_unchanged(self):
        """'Λ -1' (no registers) keeps modulator pass-through semantics
        pinned by the category tests."""
        interp, result = run("Λ -1")
        assert result == -1.0
        assert interp.last_context.lambda_obs == 0.0

    def test_lambda_obs_carried_by_fork(self):
        ctx = FieldContext()
        ctx.lambda_obs = 3.25
        child = ctx.fork()
        assert child.lambda_obs == 3.25


class TestStepTwoProhibitions:
    def test_setters_reject_register_operands(self):
        run_raises("@z 1.0 2.0\nΦ @z")

    def test_binary_setter_register_form_now_available(self):
        """Flipped at Step 3: 'Φ @z @w' is now the math-core register
        form (full coverage in test_binary_register_ops.py)."""
        interp, _ = run("@z 1.0 2.0\n@w 3.0 4.0\nΦ @z @w")
        assert interp.last_context.read_register('@z') != 1 + 2j

    def test_reducer_sigma_now_superposes(self):
        """SUPERSEDED by LOGIC_NODES_DESIGN: 'Σ @z' is no longer a
        prohibition — with register operands Σ is the tier-2
        superposition node. Bare 'Σ' keeps its reducer semantics
        (pinned by the canonical fixture), so the corridor is intact."""
        interp, _ = run("@z 1.0 2.0\n@w 3.0 4.0\nΣ @z @w")
        assert interp.last_context.superpositions['@z'] == [1 + 2j, 3 + 4j]


class TestPersistenceThroughSyntax:
    def test_registers_survive_across_executes(self):
        interp = PhiPiEInterpreterFixed()
        ctx = FieldContext()
        run("@z 1.0 2.0", ctx)
        with contextlib.redirect_stdout(io.StringIO()):
            interp.execute("Ψ 1", ctx)
        assert ctx.read_register('@z') == 1 + 2j

    def test_canonical_fixture_untouched_by_register_syntax_presence(self):
        interp, result = run("Φ 5.0\nΨ 3.0\nε 0.2\nΣ")
        assert abs(result - 6.4) < 1e-9
        assert interp.last_context.zfield == {}
        assert interp.last_context.lambda_obs == 0.0
