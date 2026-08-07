# Tests for feat/bridge-step3-ops — BRIDGE_DESIGN Step 3
#
# Binary Φ/Ψ/ε register forms: math-core operators on zfield registers,
# result written in-place to the first operand, current value passed
# through, pinned scalars untouched, prohibitions maintained.

import contextlib
import io
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from phi_pi_e_interpreter import FieldContext, PhiPiEInterpreterFixed
from phi_pi_e_math_core import (
    harmonic_equilibrium,
    incremental_insight,
    recursive_animation,
)

Z, W = 1 + 2j, 3 + 4j
INIT = "@z 1.0 2.0\n@w 3.0 4.0\n"


def run(program, ctx=None):
    interp = PhiPiEInterpreterFixed()
    with contextlib.redirect_stdout(io.StringIO()):
        result = interp.execute(program, ctx) if ctx else interp.execute(program)
    return interp, result


def run_raises(program):
    interp = PhiPiEInterpreterFixed()
    with contextlib.redirect_stdout(io.StringIO()):
        with pytest.raises(RuntimeError):
            interp.execute(program)


class TestBinaryFormsMatchMathCore:
    def test_phi_register_form(self):
        interp, _ = run(INIT + "Φ @z @w")
        assert interp.last_context.read_register('@z') == \
            harmonic_equilibrium(Z, W)
        assert interp.last_context.read_register('@w') == W  # never written

    def test_psi_register_form(self):
        interp, _ = run(INIT + "Ψ @z @w")
        assert interp.last_context.read_register('@z') == \
            recursive_animation(Z, W)
        assert interp.last_context.read_register('@w') == W

    def test_epsilon_register_form(self):
        interp, _ = run(INIT + "ε @z @w")
        assert interp.last_context.read_register('@z') == \
            incremental_insight(Z, W)
        assert interp.last_context.read_register('@w') == W

    def test_epsilon_loop_evolves_first_operand(self):
        """'[ε @z @w]' = 10 in-place ε-iterations: @z moves toward @w
        exactly as z_{n+1} = ε(z_n, w) prescribes (Thm 4.3)."""
        interp, _ = run(INIT + "[ε @z @w]")
        expected = Z
        for _ in range(10):
            expected = incremental_insight(expected, W)
        got = interp.last_context.read_register('@z')
        assert abs(got - expected) < 1e-12
        assert abs(got - W) < abs(Z - W)  # strictly closer than start

    def test_chained_ops_compose(self):
        """Φ then Ψ on the same register: second op sees first's output."""
        interp, _ = run(INIT + "Φ @z @w\nΨ @z @w")
        expected = recursive_animation(harmonic_equilibrium(Z, W), W)
        assert interp.last_context.read_register('@z') == expected


class TestIsolationAndPassThrough:
    SCALARS = ('psi_signal', 'phi_state', 'epsilon_drift', 'stabilized_value')

    def test_register_ops_touch_no_pinned_scalar(self):
        interp, result = run(
            "Φ 5.0\nΨ 3.0\nε 0.2\nΣ\n" + INIT +
            "Φ @z @w\nΨ @z @w\nε @z @w")
        s = interp.last_context.state
        assert (s.phi_state, s.psi_signal, s.epsilon_drift) == (5.0, 3.0, 0.2)
        assert abs(s.stabilized_value - 6.4) < 1e-9

    def test_current_value_passes_through(self):
        """Register ops must not clobber the interpreter's scalar
        result: Σ's 6.4 survives subsequent register operations."""
        _, result = run("Φ 5.0\nΨ 3.0\nε 0.2\nΣ\n" + INIT + "Φ @z @w")
        assert abs(result - 6.4) < 1e-9

    def test_unary_forms_completely_unchanged(self):
        """Same glyphs, literal operands: pinned DSL semantics."""
        interp, result = run("Φ 5.0\nΨ 3.0\nε 0.2\nΣ")
        assert abs(result - 6.4) < 1e-9
        assert interp.last_context.zfield == {}

    def test_full_bridge_pipeline(self):
        """End-to-end ℂ path: init -> binary op -> Λ reduction to ℝ."""
        interp, result = run(INIT + "Φ @z @w\nΛ @z @w")
        from phi_pi_e_math_core import structural_illumination
        expected = structural_illumination(
            harmonic_equilibrium(Z, W), W).real
        assert abs(interp.last_context.lambda_obs - expected) < 1e-12


class TestProhibitionsStillHold:
    def test_mixed_form_phi(self):
        run_raises("@z 1.0 2.0\nΦ @z 1.0")

    def test_mixed_form_psi_literal_first(self):
        run_raises("@w 3.0 4.0\nΨ 1.0 @w")

    def test_single_register_epsilon(self):
        run_raises("@z 1.0 2.0\nε @z")

    def test_non_structural_symbols_still_reject_registers(self):
        """Σ and Γ moved to the tier-2 structural set
        (LOGIC_NODES_DESIGN); symbols outside BOTH tiers still reject
        register operands."""
        run_raises("@z 1.0 2.0\nΩ @z")
        run_raises("@z 1.0 2.0\nΛ @z 1.0")   # mixed form, still banned
