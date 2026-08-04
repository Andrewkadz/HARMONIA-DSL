# Regression tests for fix/dsl-lexical-semantic-path
#
# Covers the defects documented in PARSER_BUGS.md and found in the
# 2026-08-03 validation pass:
#   1. Numeric literals silently discarded by tokenize()
#   2. Newlines destroyed by clean_input() (statement boundaries lost)
#   3. '#' comments leaking phantom tokens (e.g. 'n' from "tension")
#   4. Operator handlers never binding program arguments into context
#   5. Φπε.py entry point dead due to renamed interpreter class

import contextlib
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from phi_pi_e_interpreter import PhiPiEInterpreterFixed


class TestNumberTokenization:
    def test_numbers_are_tokens(self):
        interp = PhiPiEInterpreterFixed()
        tokens = interp.tokenize(interp.clean_input("Φ 5.0\nΨ 3.0\nε 0.2\nΣ"))
        assert tokens == ['Φ', '5.0', 'Ψ', '3.0', 'ε', '0.2', 'Σ']

    def test_int_float_negative(self):
        interp = PhiPiEInterpreterFixed()
        tokens = interp.tokenize("Φ 5 Ψ -0.25 ε 3.")
        assert '5' in tokens and '-0.25' in tokens and '3.' in tokens


class TestNewlinePreservation:
    def test_statement_boundaries_kept(self):
        interp = PhiPiEInterpreterFixed()
        assert interp.clean_input("Φ 5.0\nΨ 2.0") == "Φ 5.0\nΨ 2.0"


class TestCommentStripping:
    def test_hash_comment_no_phantom_tokens(self):
        interp = PhiPiEInterpreterFixed()
        cleaned = interp.clean_input("Φ 5.0    # Set tension (phi_state) to 5.0")
        assert cleaned == "Φ 5.0"
        assert interp.tokenize(cleaned) == ['Φ', '5.0']

    def test_slash_comment_still_stripped(self):
        interp = PhiPiEInterpreterFixed()
        assert interp.clean_input("Ε          // Ignite: Start") == "Ε"


class TestArgumentBinding:
    def test_minimal_program_produces_non_default_context(self):
        """The GROK_LIVE_DEMO Demo 1 program must produce its documented
        result: Stabilized = (psi + phi) * (1 - eps) = (3+5)*(1-0.2) = 6.4"""
        interp = PhiPiEInterpreterFixed()
        with contextlib.redirect_stdout(io.StringIO()):
            result = interp.execute("Φ 5.0\nΨ 3.0\nε 0.2\nΣ")
        state = interp.last_context.state
        assert state.phi_state == 5.0
        assert state.psi_signal == 3.0
        assert state.epsilon_drift == 0.2
        assert abs(state.stabilized_value - 6.4) < 1e-9
        assert abs(result - 6.4) < 1e-9

    def test_handlers_without_args_keep_defaults(self):
        """Backward compatibility: no literals -> old derived defaults."""
        interp = PhiPiEInterpreterFixed()
        with contextlib.redirect_stdout(io.StringIO()):
            interp.execute("Φ\nΨ\nΣ")
        state = interp.last_context.state
        assert state.phi_state == 1.0  # 1.0 - max(0, 0-0.1) tension default
        assert state.psi_signal == 0.0


class TestEntryPointBoot:
    def test_legacy_class_name_importable(self):
        from phi_pi_e_interpreter import PhiPiEInterpreter
        assert PhiPiEInterpreter is PhiPiEInterpreterFixed


class TestCanonicalFixture:
    """The canonical 'hello world with semantics' for HARMONIA-DSL.

    Every future refactor MUST preserve this exact pipeline:
        source -> token stream -> state transition -> final output.
    If this test breaks, the language has lost meaning, whatever else
    still passes.
    """

    SOURCE = "Φ 5.0    # equilibrium\nΨ 3.0    # pulse\nε 0.2    # drift\nΣ        # stabilize"
    EXPECTED_TOKENS = ['Φ', '5.0', 'Ψ', '3.0', 'ε', '0.2', 'Σ']
    EXPECTED_STATE = {"phi_state": 5.0, "psi_signal": 3.0, "epsilon_drift": 0.2}
    EXPECTED_OUTPUT = 6.4  # (psi + phi) * (1 - eps) = (3+5)*(1-0.2)

    def test_canonical_pipeline(self):
        interp = PhiPiEInterpreterFixed()
        tokens = interp.tokenize(interp.clean_input(self.SOURCE))
        assert tokens == self.EXPECTED_TOKENS
        with contextlib.redirect_stdout(io.StringIO()):
            result = interp.execute(self.SOURCE)
        state = interp.last_context.state
        for name, expected in self.EXPECTED_STATE.items():
            assert abs(getattr(state, name) - expected) < 1e-9, name
        assert abs(result - self.EXPECTED_OUTPUT) < 1e-9
