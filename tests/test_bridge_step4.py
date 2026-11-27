# Tests for feat/bridge-step4-pi-delta-converge — BRIDGE_DESIGN Step 4
#
# Covers:
#   - Binary π (and Π alias) and Δ register dispatch to phi_pi_e_math_core
#   - π depth parameterization via #pi_n (default n=1) and w==0 ValueError
#   - Mixed/partial forms rejected; Ω categorical refusal preserved
#   - Opt-in additive ε-convergence loop [ε? @z @w tol [cap] [| body]]
#   - Convergence on known pairs, hard cap on non-converging (π-driven) pairs
#   - Plain [..] 10-iteration loop and canonical fixture completely unchanged

import contextlib
import io
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from phi_pi_e_interpreter import (
    CONVERGE_BATCH_SIZE,
    FieldContext,
    PhiPiEInterpreterFixed,
)
from phi_pi_e_math_core import (
    fusion_transformation,
    incremental_insight,
    transcendent_continuity,
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
        with pytest.raises(RuntimeError) as exc_info:
            interp.execute(program)
    return exc_info.value


class TestBinaryPiAndDelta:
    def test_delta_register_form_matches_math_core(self):
        interp, _ = run(INIT + "Δ @z @w")
        assert interp.last_context.read_register('@z') == fusion_transformation(Z, W)
        assert interp.last_context.read_register('@w') == W

    def test_pi_register_form_default_depth_matches_math_core(self):
        interp, _ = run(INIT + "π @z @w")
        assert interp.last_context.read_register('@z') == transcendent_continuity(Z, W, n=1)
        assert interp.last_context.read_register('@w') == W

    def test_capital_pi_register_alias_matches_math_core(self):
        interp, _ = run(INIT + "Π @z @w")
        assert interp.last_context.read_register('@z') == transcendent_continuity(Z, W, n=1)
        assert interp.last_context.read_register('@w') == W

    def test_pi_depth_scalar_parameterization(self):
        interp, _ = run(INIT + "#pi_n 4\nπ @z @w")
        assert interp.last_context.read_register('@z') == transcendent_continuity(Z, W, n=4)
        interp2, _ = run(INIT + "#pi_n 4\nΠ @z @w")
        assert interp2.last_context.read_register('@z') == transcendent_continuity(Z, W, n=4)

    def test_pi_w_zero_raises_value_error(self):
        err = run_raises("@z 1.0 2.0\n@w 0.0 0.0\nπ @z @w")
        assert isinstance(err.__cause__, ValueError)

    def test_pi_unset_w_raises_value_error(self):
        err = run_raises("@z 1.0 2.0\nπ @z @unset_w")
        assert isinstance(err.__cause__, ValueError)

    def test_pi_invalid_depth_raises_value_error(self):
        err = run_raises(INIT + "#pi_n 0\nπ @z @w")
        assert isinstance(err.__cause__, ValueError)
        err2 = run_raises(INIT + "#pi_n 2.5\nπ @z @w")
        assert isinstance(err2.__cause__, ValueError)

    def test_pass_through_and_isolation(self):
        interp, result = run("Φ 5.0\nΨ 3.0\nε 0.2\nΣ\n" + INIT + "Δ @z @w\nπ @z @w")
        assert abs(result - 6.4) < 1e-9
        s = interp.last_context.state
        assert (s.phi_state, s.psi_signal, s.epsilon_drift) == (5.0, 3.0, 0.2)
        assert abs(s.stabilized_value - 6.4) < 1e-9

    def test_bare_pi_and_delta_keep_modulator_semantics(self):
        interp, result = run("Φ 5.0\nΨ 3.0\nε 0.2\nΣ\nΔ\nπ\nΠ")
        assert abs(result - 6.4) < 1e-9
        assert interp.last_context.zfield == {}


class TestProhibitionsAndOmegaPreserved:
    def test_mixed_forms_rejected(self):
        run_raises("@z 1.0 2.0\nΔ @z 1.0")
        run_raises("@z 1.0 2.0\nπ @z 1.0")
        run_raises("@z 1.0 2.0\nΠ @z 1.0")
        run_raises("@w 3.0 4.0\nΔ 1.0 @w")
        run_raises("@w 3.0 4.0\nπ 1.0 @w")

    def test_single_register_forms_rejected(self):
        run_raises("@z 1.0 2.0\nΔ @z")
        run_raises("@z 1.0 2.0\nπ @z")

    def test_omega_still_refuses_registers(self):
        run_raises("@z 1.0 2.0\nΩ @z")
        run_raises("@z 1.0 2.0\n@w 3.0 4.0\nΩ @z @w")


class TestEpsilonConvergenceLoop:
    def test_converges_on_known_pair_with_batching_equivalence(self):
        interp, dist = run(INIT + "[ε? @z @w 1e-3]")
        ctx = interp.last_context
        steps = int(ctx.get_scalar('#converge_steps'))
        assert ctx.get_scalar('#converged') == 1.0
        assert 1 <= steps < 100
        assert dist <= 1e-3
        assert abs(ctx.read_register('@z') - W) <= 1e-3
        # Exact batching equivalence: `steps * CONVERGE_BATCH_SIZE` math-core calls
        expected = Z
        for _ in range(steps * CONVERGE_BATCH_SIZE):
            expected = incremental_insight(expected, W)
        assert ctx.read_register('@z') == expected

    def test_already_converged_pair_runs_zero_batches(self):
        interp, dist = run("@z 3.0 4.0\n@w 3.0 4.0\n[ε? @z @w 1e-6]")
        ctx = interp.last_context
        assert ctx.get_scalar('#converge_steps') == 0.0
        assert ctx.get_scalar('#converged') == 1.0
        assert dist == 0.0

    def test_cap_fires_on_pi_driven_non_converging_registers(self):
        interp, dist = run(INIT + "[ε? @z @w 1e-3 12 | π @z @w]")
        ctx = interp.last_context
        assert ctx.get_scalar('#converged') == 0.0
        assert ctx.get_scalar('#converge_steps') == 12.0
        assert dist > 1e-3

    def test_multiline_converge_loop_body_terminates_at_cap(self):
        interp, dist = run(INIT + "[ε? @z @w 1e-3 5\nπ @z @w]")
        ctx = interp.last_context
        assert ctx.get_scalar('#converged') == 0.0
        assert ctx.get_scalar('#converge_steps') == 5.0
        assert dist > 1e-3

    def test_pi_w_zero_fails_closed_inside_converge_loop(self):
        err = run_raises("@z 1.0 2.0\n@w 0.0 0.0\n[ε? @z @w 1e-3 5 | π @z @w]")
        assert "w = 0" in str(err)

    def test_cap_fires_on_insufficient_batch_budget(self):
        interp, dist = run("@z 10.0 0.0\n@w 0.0 0.0\n[ε? @z @w 1e-6 2]")
        ctx = interp.last_context
        assert ctx.get_scalar('#converged') == 0.0
        assert ctx.get_scalar('#converge_steps') == 2.0
        assert dist > 1e-6

    def test_convergence_loop_validation(self):
        run_raises(INIT + "[ε? @z 1.0 1e-3]")
        run_raises(INIT + "[ε? @z @w -0.1]")
        run_raises(INIT + "[ε? @z @w 1e-3 0]")
        run_raises(INIT + "[ε? @z @w 1e-3 1.5]")
        run_raises(INIT + "[ε? @z @w 1e-3 |]")

    def test_plain_loop_and_canonical_fixture_untouched(self):
        interp, _ = run("[Ψ 1]")
        assert interp.last_context.state.psi_signal == 10.0

        interp2, result = run("Φ 5.0\nΨ 3.0\nε 0.2\nΣ\n" + INIT + "[ε? @z @w 1e-3]")
        s = interp2.last_context.state
        assert (s.phi_state, s.psi_signal, s.epsilon_drift) == (5.0, 3.0, 0.2)
        assert abs(s.stabilized_value - 6.4) < 1e-9
        assert abs(result - abs(interp2.last_context.read_register('@z') - W)) < 1e-12
