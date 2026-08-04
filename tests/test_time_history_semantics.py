# Regression tests for fix/time-history-semantics
#
# Proves that the calculus operators are genuinely history-driven:
# before this fix, TimeSteppingInterpreter.run() read state from
# interpreter.fields['context'] (which never existed), so history
# recorded only zeros and every temporal operator returned 0.0.

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from time_stepping_interpreter import TimeSteppingInterpreter


class TestHistoryDriven:
    def test_constant_signal_integrates_nonzero(self):
        """Constant psi=5 over 10 steps must integrate to ~50, not 0."""
        interp = TimeSteppingInterpreter()
        result = interp.run("Φ 5 3 0.1", num_steps=10)
        history = result.get_history("psi_signal")
        assert history == [5.0] * 10  # history actually recorded
        integral = interp.compute_integral(result, "psi_signal")
        assert abs(integral - 50.0) < 1e-9

    def test_linear_signal_differentiates_nonzero(self):
        """Ψ 1 per step -> psi rises linearly -> derivative == 1, not 0."""
        interp = TimeSteppingInterpreter()
        result = interp.run("Φ 5 3 0.1\nΨ 1", num_steps=5)
        history = result.get_history("psi_signal")
        assert history == [6.0, 7.0, 8.0, 9.0, 10.0]  # init 5, +1/step
        derivative = interp.compute_derivative(result, "psi_signal")
        assert abs(derivative - 1.0) < 1e-9

    def test_oscillation_sees_repeated_variation(self):
        """A driven signal must produce a history with real variation."""
        interp = TimeSteppingInterpreter()
        result = interp.run("Φ 0 1 0\nΨ 0.5", num_steps=8)
        history = result.get_history("psi_signal")
        assert len(set(history)) == 8  # strictly changing every step
        assert history[-1] > history[0]

    def test_init_line_applies_only_at_t0(self):
        """'Φ a b c' seeds initial conditions once; it must not reset
        state on later steps (otherwise dynamics are frozen)."""
        interp = TimeSteppingInterpreter()
        result = interp.run("Φ 5 3 0.1\nε 0.05", num_steps=4)
        eps = result.get_history("epsilon_drift")
        expected = [0.15, 0.20, 0.25, 0.30]
        assert all(abs(a - b) < 1e-9 for a, b in zip(eps, expected))
