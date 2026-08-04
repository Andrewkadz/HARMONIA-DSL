# Tests for feat/bridge-step1-zfield — BRIDGE_DESIGN Step 1
#
# The shadow register layer (context.zfield) exists, is isolated from
# real scalar state in BOTH directions, persists across execution, and
# changes nothing about existing semantics while present but unused.
# No DSL syntax reaches zfield yet (that is Step 2, per BRIDGE_DESIGN).

import contextlib
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from phi_pi_e_interpreter import FieldContext, PhiPiEInterpreterFixed


class TestExistenceAndEmptiness:
    def test_fresh_context_has_empty_zfield(self):
        ctx = FieldContext()
        assert ctx.zfield == {}

    def test_unset_register_reads_as_zero(self):
        ctx = FieldContext()
        assert ctx.read_register('a') == 0j
        assert ctx.zfield == {}  # reading does not create

    def test_write_then_read(self):
        ctx = FieldContext()
        ctx.write_register('z1', 1 + 2j)
        assert ctx.read_register('z1') == 1 + 2j

    def test_real_values_coerced_to_complex(self):
        ctx = FieldContext()
        ctx.write_register('r', 5)
        assert ctx.read_register('r') == complex(5, 0)
        assert isinstance(ctx.read_register('r'), complex)


class TestIsolation:
    """BRIDGE_DESIGN Decision 1: the two layers share no state."""

    SCALARS = ('psi_signal', 'phi_state', 'epsilon_drift', 'stabilized_value')

    def test_register_writes_never_touch_real_scalars(self):
        ctx = FieldContext()
        before = {s: getattr(ctx.state, s) for s in self.SCALARS}
        before_mech = (ctx.phase, ctx.charge, ctx.depth)
        ctx.write_register('z1', 3 + 4j)
        ctx.write_register('z2', -1j)
        for s in self.SCALARS:
            assert getattr(ctx.state, s) == before[s]
        assert (ctx.phase, ctx.charge, ctx.depth) == before_mech

    def test_real_scalar_writes_never_touch_registers(self):
        ctx = FieldContext()
        ctx.write_register('z1', 2 + 2j)
        ctx.state.psi_signal = 7.0
        ctx.state.phi_state = 3.0
        ctx.state.epsilon_drift = 0.5
        assert ctx.read_register('z1') == 2 + 2j
        assert ctx.zfield == {'z1': 2 + 2j}

    def test_execution_leaves_zfield_untouched(self):
        """No DSL syntax reaches registers yet: running programs must
        never populate or alter zfield."""
        interp = PhiPiEInterpreterFixed()
        ctx = FieldContext()
        ctx.write_register('keep', 9 + 9j)
        with contextlib.redirect_stdout(io.StringIO()):
            interp.execute("Φ 5.0\nΨ 3.0\nε 0.2\nΣ\n[Ψ 1]", ctx)
        assert ctx.zfield == {'keep': 9 + 9j}


class TestPersistence:
    def test_registers_survive_execute(self):
        interp = PhiPiEInterpreterFixed()
        ctx = FieldContext()
        ctx.write_register('z1', 1 - 1j)
        with contextlib.redirect_stdout(io.StringIO()):
            interp.execute("Φ 5.0\nΣ", ctx)
        assert ctx.read_register('z1') == 1 - 1j

    def test_registers_persist_across_multiple_executes(self):
        """Time-model style: one persistent context, many executions."""
        interp = PhiPiEInterpreterFixed()
        ctx = FieldContext()
        ctx.write_register('acc', 4j)
        for _ in range(3):
            with contextlib.redirect_stdout(io.StringIO()):
                interp.execute("Ψ 1", ctx)
        assert ctx.read_register('acc') == 4j
        assert ctx.state.psi_signal == 3.0  # real layer evolved normally

    def test_fork_shares_register_layer(self):
        """Registers are execution-global: forks see and share the same
        dict — no divergent copies from modulator fork/discard cycles."""
        ctx = FieldContext()
        ctx.write_register('shared', 1 + 1j)
        child = ctx.fork()
        assert child.read_register('shared') == 1 + 1j
        child.write_register('from_child', 2j)
        assert ctx.read_register('from_child') == 2j
        assert child.zfield is ctx.zfield


class TestCorridorUnchanged:
    def test_canonical_fixture_with_zfield_present(self):
        """The invariant program produces 6.4 with the register layer
        present (and stays unused)."""
        interp = PhiPiEInterpreterFixed()
        with contextlib.redirect_stdout(io.StringIO()):
            result = interp.execute("Φ 5.0\nΨ 3.0\nε 0.2\nΣ")
        assert abs(result - 6.4) < 1e-9
        assert interp.last_context.zfield == {}
