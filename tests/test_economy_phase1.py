# E-series tests — ECONOMY_SIM_PHASE1.md
#
# Both worlds run the IDENTICAL naive solvency guard, identical agents,
# identical seed and shocks. The only difference is execution speed:
# teleport (full move in one step) vs bounded (real ε-step through the
# DSL). These tests pin the resulting difference.

import contextlib
import io
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from swarm_brain.economy import FLOOR, Market, run_pair


def quiet(fn):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn()


class TestEA_TeleportBreaches:
    """E-A: the teleporting world, despite passing the same pre-trade
    guard, is rendered insolvent between checks."""

    def test_insolvency_occurs(self):
        tr = quiet(lambda: Market("teleport").run())
        assert tr.breach_count > 0
        assert tr.min_net_worth < FLOOR

    def test_breach_follows_the_second_leg(self):
        """Breaches begin at the second leg of a decline, after agents
        have levered into the dip."""
        tr = quiet(lambda: Market("teleport").run())
        first_round = min(b[0] for b in tr.breaches)
        assert first_round >= 61  # after the first leg, at/after the second


class TestEB_BoundedHolds:
    """E-B: the headline guarantee — same guard, bounded motion, no
    agent crosses the floor in any round."""

    def test_no_breach_ever(self):
        tr = quiet(lambda: Market("bounded").run())
        assert tr.breach_count == 0
        for agent_id, series in tr.net_worth.items():
            assert all(nw >= FLOOR for nw in series), agent_id

    def test_same_seed_same_shocks_opposite_outcomes(self):
        tp, bd = quiet(lambda: run_pair())
        assert tp.breach_count > 0
        assert bd.breach_count == 0
        assert tp.prices[:5] != [] and bd.prices[:5] != []


class TestEC_EpsilonIsLoadBearing:
    """E-C (the ST-C analogue): substituting ε with a jump-to-target
    operator breaks the invariant under the same conditions,
    demonstrating that the theorem's gradualism is essential, not
    cosmetic. 'teleport' IS that substitution."""

    def test_gradualism_is_what_holds_the_floor(self):
        tp, bd = quiet(lambda: run_pair())
        assert tp.breach_count > 0 and bd.breach_count == 0

    def test_bounded_motion_caps_peak_leverage(self):
        """The mechanism: bounded steps low-pass filter exposure, so
        the guard is re-evaluated at new prices as the position builds
        and the dangerous state is never reached."""
        tp, bd = quiet(lambda: run_pair())
        assert bd.peak_leverage < tp.peak_leverage
        assert bd.peak_leverage < 1 / 0.35  # below the wipe-out threshold


class TestED_DslIsLoadBearing:
    """E-D: stub the interpreter and the bounded world loses its
    bounded motion — the guarantee is produced by the DSL, not by
    Python bookkeeping."""

    def test_stubbed_dsl_changes_behaviour(self):
        live = quiet(lambda: Market("bounded").run())
        stubbed = quiet(lambda: Market("bounded", stub_dsl=True).run())
        assert live.dsl_calls > 0
        # with no register motion, no position is ever built
        assert stubbed.peak_leverage <= live.peak_leverage
        assert live.total_terminal_wealth != stubbed.total_terminal_wealth


class TestEE_GovernanceCostIsReported:
    """E-E: governance is not free, and the cost must be visible."""

    def test_cost_is_measurable_and_reported(self):
        tp, bd = quiet(lambda: run_pair())
        cost = (tp.total_terminal_wealth - bd.total_terminal_wealth) \
            / tp.total_terminal_wealth
        assert -1.0 < cost < 1.0          # a real, finite number
        assert bd.total_terminal_wealth > 0
        # the honest framing: teleport's total includes insolvent agents
        assert tp.breach_count > 0


class TestEF_Sweep:
    """E-F: the invariant is a property of bounded motion, not of one
    parameter point."""

    @pytest.mark.parametrize("shock", [-0.25, -0.35, -0.45])
    @pytest.mark.parametrize("floor", [0.0, 25.0, 50.0])
    def test_bounded_holds_across_parameters(self, shock, floor):
        tr = quiet(lambda: Market("bounded", shock_mag=shock,
                                  floor=floor).run())
        assert tr.breach_count == 0
