# Regression tests for fix/loop-context
#
# Before this fix, execute_loop() called execute() without passing the
# caller's context, so every loop iteration ran against a fresh
# FieldContext — loops could never accumulate state.

import contextlib
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from phi_pi_e_interpreter import PhiPiEInterpreterFixed


class TestLoopContextPersistence:
    def test_loop_accumulates_state(self):
        """'[Ψ 1]' runs the pulse 10 times on ONE context:
        psi must reach 10.0, not 1.0 (and not 0.0)."""
        interp = PhiPiEInterpreterFixed()
        with contextlib.redirect_stdout(io.StringIO()):
            interp.execute("[Ψ 1]")
        assert interp.last_context.state.psi_signal == 10.0

    def test_loop_does_not_reset_context(self):
        """State set before a loop must survive into and past it,
        and the loop must build on it rather than start from zero."""
        interp = PhiPiEInterpreterFixed()
        with contextlib.redirect_stdout(io.StringIO()):
            interp.execute("Φ 5.0\nΨ 2.0\n[ε 0.01]\nΣ")
        state = interp.last_context.state
        assert state.phi_state == 5.0          # pre-loop state survived
        assert state.psi_signal == 2.0         # pre-loop state survived
        assert abs(state.epsilon_drift - 0.1) < 1e-9   # 10 × 0.01 accumulated
        # Σ after the loop sees the accumulated drift:
        assert abs(state.stabilized_value - (2.0 + 5.0) * (1 - 0.1)) < 1e-9
