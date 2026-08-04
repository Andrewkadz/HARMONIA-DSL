# Tests for feat/operator-categories
#
# Encodes the categorical execution model (setters / reducers / modulators)
# aligned with the Φπε operator architecture. These tests pin the category
# structure and the uniform argument rule per category — NOT full semantics
# for every symbol (deliberately deferred; see SYMBOL_COVERAGE.md).

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


class TestCategoryStructure:
    def test_every_symbol_is_categorized(self):
        """No symbol may be dispatch-reachable without a category."""
        interp = PhiPiEInterpreterFixed()
        categorized = set().union(*interp.categories.values())
        assert set(interp.symbols.keys()) == categorized

    def test_categories_are_disjoint(self):
        interp = PhiPiEInterpreterFixed()
        cats = list(interp.categories.values())
        for i in range(len(cats)):
            for j in range(i + 1, len(cats)):
                assert not (cats[i] & cats[j])

    def test_category_of(self):
        interp = PhiPiEInterpreterFixed()
        assert interp.category_of('Φ') == 'setter'
        assert interp.category_of('Σ') == 'reducer'
        assert interp.category_of('Λ') == 'modulator'
        assert interp.category_of('☃') is None


class TestCategoryDispatchRules:
    def test_setters_consume_numeric_args(self):
        interp, _ = run("Φ 5.0\nΨ 3.0\nε 0.2")
        s = interp.last_context.state
        assert (s.phi_state, s.psi_signal, s.epsilon_drift) == (5.0, 3.0, 0.2)

    def test_modulators_do_not_consume_numeric_args(self):
        """'Λ -1': the modulator must NOT swallow the literal — it stays
        a bare value. Semantic state remains untouched by Λ."""
        interp, result = run("Λ -1")
        assert result == -1.0  # literal survived as current value
        s = interp.last_context.state
        assert s.phi_state == 0.0 and s.psi_signal == 0.0

    def test_reducers_read_state_and_return_scalar(self):
        interp, result = run("Φ 5.0\nΨ 3.0\nε 0.2\nΣ")
        assert isinstance(result, float)
        assert abs(result - 6.4) < 1e-9

    def test_modulators_pass_value_through(self):
        """A modulator between a reducer and the program end must not
        destroy the reducer's scalar result."""
        interp, result = run("Φ 5.0\nΨ 3.0\nε 0.2\nΣ\nΛ")
        assert abs(result - 6.4) < 1e-9  # Λ passed 6.4 through
