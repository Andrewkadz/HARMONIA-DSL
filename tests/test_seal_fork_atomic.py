# Seal persistence across fork() and atomic group updates.
#
# Review findings addressed here:
#   1. FieldContext.fork() shared zfield but lost the `closed` seal
#      set, so a child could rewrite a register the parent had sealed
#      with Ω. Seals (and the other lazily-created structural layers)
#      are now execution-global like zfield.
#   2. λ! and Υ wrote group results member-by-member, so a sealed
#      member could be left half-updated. Group updates are now
#      atomic: if the result would change any sealed destination the
#      whole operation is refused before any register is modified.

import contextlib
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from phi_pi_e_interpreter import FieldContext, PhiPiEInterpreterFixed


def run(program, ctx=None):
    interp = PhiPiEInterpreterFixed()
    ctx = ctx if ctx is not None else FieldContext()
    with contextlib.redirect_stdout(io.StringIO()):
        result = interp.execute(program, ctx)
    return interp, ctx, result


class TestSealPersistenceAcrossFork:
    def test_child_cannot_write_parent_sealed_register(self):
        _, ctx, _ = run("@a 5.0 0.0\nΩ @a")
        child = ctx.fork()
        child.write_register('@a', 99 + 0j)
        assert ctx.read_register('@a') == 1 + 0j
        assert child.read_register('@a') == 1 + 0j

    def test_parent_cannot_write_child_sealed_register(self):
        ctx = FieldContext()
        child = ctx.fork()
        _, child, _ = run("@b 7.0 0.0\nΩ @b", child)
        ctx.write_register('@b', 42 + 0j)
        assert ctx.read_register('@b') == 1 + 0j
        assert child.read_register('@b') == 1 + 0j

    def test_nested_forks_share_seals(self):
        _, ctx, _ = run("@a 5.0 0.0\nΩ @a")
        child = ctx.fork()
        grandchild = child.fork()
        grandchild.write_register('@a', 99 + 0j)
        assert ctx.read_register('@a') == 1 + 0j
        assert child.read_register('@a') == 1 + 0j
        assert grandchild.read_register('@a') == 1 + 0j

    def test_seal_query_visible_in_child(self):
        _, ctx, _ = run("@a 5.0 0.0\nΩ @a")
        child = ctx.fork()
        _, child, v = run("Ω? @a", child)
        assert v == 1.0
        assert child.get_scalar('#closed') == 1.0

    def test_repeated_writes_all_refused_and_counted(self):
        _, ctx, _ = run("@a 5.0 0.0\nΩ @a")
        child = ctx.fork()
        for i in range(3):
            child.write_register('@a', complex(i))
        assert ctx.read_register('@a') == 1 + 0j
        # scalars are shared too: refusals counted once per attempt
        assert ctx.get_scalar('#sealed_refusals') == 3.0

    def test_independent_contexts_are_isolated(self):
        _, ctx1, _ = run("@a 5.0 0.0\nΩ @a")
        ctx2 = FieldContext()
        ctx2.write_register('@a', 99 + 0j)
        assert ctx1.read_register('@a') == 1 + 0j
        assert ctx2.read_register('@a') == 99 + 0j
        assert ctx2.closed == set()

    def test_unsealed_registers_still_share_across_fork(self):
        _, ctx, _ = run("@a 5.0 0.0")
        child = ctx.fork()
        child.write_register('@a', 9 + 0j)
        assert ctx.read_register('@a') == 9 + 0j


class TestAtomicGroupUpdates:
    def _sealed_pair(self):
        # @a sealed at 1 (post-Ω), @b writable at 3
        _, ctx, _ = run("@a 5.0 0.0\n@b 3.0 0.0\nΩ @a")
        return ctx

    def test_lambda_resolve_refuses_when_sealed_member_would_change(self):
        ctx = self._sealed_pair()
        _, ctx, v = run("λ @a @b\nλ! @a", ctx)
        # shared would be 2.0; sealed @a=1 would change -> refuse all
        assert v == -1.0
        assert ctx.read_register('@a') == 1 + 0j
        assert ctx.read_register('@b') == 3 + 0j   # untouched
        assert ctx.get_scalar('#group_refused') == 1.0
        assert ctx.get_scalar('#sealed_refusals') == 1.0
        # entanglement metadata preserved
        assert '@b' in ctx.entangled.get('@a', set())

    def test_upsilon_refuses_when_sealed_operand_would_change(self):
        ctx = self._sealed_pair()
        _, ctx, v = run("Υ @a @b", ctx)
        assert v == -1.0
        assert ctx.read_register('@a') == 1 + 0j
        assert ctx.read_register('@b') == 3 + 0j
        assert ctx.get_scalar('#group_refused') == 1.0
        # dispersion is still reported as a diagnostic
        assert ctx.get_scalar('#upsilon') == 1.0

    def test_sealed_member_in_second_operand_position(self):
        _, ctx, _ = run("@a 3.0 0.0\n@b 5.0 0.0\nΩ @b")
        _, ctx, v = run("Υ @a @b", ctx)
        assert v == -1.0
        assert ctx.read_register('@a') == 3 + 0j
        assert ctx.read_register('@b') == 1 + 0j

    def test_fully_writable_group_still_merges(self):
        _, ctx, _ = run("@a 1.0 0.0\n@b 3.0 0.0")
        _, ctx, v = run("Υ @a @b", ctx)
        assert v == 1.0                      # dispersion
        assert ctx.read_register('@a') == 2 + 0j
        assert ctx.read_register('@b') == 2 + 0j

    def test_lambda_resolve_writable_group(self):
        _, ctx, _ = run("@a 1.0 0.0\n@b 3.0 0.0\nλ @a @b")
        _, ctx, v = run("λ! @a", ctx)
        assert v == 2.0
        assert ctx.read_register('@a') == 2 + 0j
        assert ctx.read_register('@b') == 2 + 0j

    def test_overlapping_entanglement_groups(self):
        # {a,b} and {b,c} merge into one group {a,b,c} on entangle
        _, ctx, _ = run("@a 0.0 0.0\n@b 3.0 0.0\n@c 6.0 0.0\n"
                        "λ @a @b\nλ @b @c")
        _, ctx, v = run("λ! @a", ctx)
        assert v == 3.0
        for n in ('@a', '@b', '@c'):
            assert ctx.read_register(n) == 3 + 0j

    def test_refusal_leaves_state_unchanged(self):
        ctx = self._sealed_pair()
        run("λ @a @b", ctx)          # entangle in setup
        before = {n: ctx.read_register(n) for n in ('@a', '@b')}
        ent_before = {k: set(v) for k, v in ctx.entangled.items()}
        run("Υ @a @b", ctx)
        run("λ! @a", ctx)
        for n in ('@a', '@b'):
            assert ctx.read_register(n) == before[n]
        assert ctx.entangled == ent_before

    def test_already_equal_sealed_destination_does_not_block(self):
        # sealed @a = 1; group {a,b} with b = 1 -> merged = 1,
        # sealed destination unchanged -> update proceeds
        _, ctx, _ = run("@a 5.0 0.0\n@b 1.0 0.0\nΩ @a")
        _, ctx, v = run("Υ @a @b", ctx)
        assert v == 0.0                      # zero dispersion
        assert ctx.read_register('@a') == 1 + 0j
        assert ctx.read_register('@b') == 1 + 0j
        assert ctx.get_scalar('#group_refused') == 0.0

    def test_refusal_count_accumulates(self):
        ctx = self._sealed_pair()
        run("Υ @a @b", ctx)
        run("Υ @a @b", ctx)
        assert ctx.get_scalar('#sealed_refusals') == 2.0
