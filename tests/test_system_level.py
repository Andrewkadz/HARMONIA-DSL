# System-level tests per SYSTEM_TESTS.md (ST-A, ST-B, ST-C pin, ST-D).
# Whole-system behaviors: one test = one complete falsifiable claim.

import contextlib
import io
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from swarm_brain.baseline_swarm import BaselineSwarm
from swarm_brain.governed_swarm import DRIFT_BUDGET, GovernedSwarm
from swarm_brain.task_spec import make_scenario

MAX_ROUNDS = 60
LIVELOCK_BOUND = 10


def quiet(callable_):
    with contextlib.redirect_stdout(io.StringIO()):
        return callable_()


class TestSTA_EndToEnd:
    def test_swarm_phase1_end_to_end(self):
        """ST-A: the complete behavioral contrast in one statement.
        Same scenario, same seed, same ceiling — only governance
        differs."""
        baseline = quiet(lambda: BaselineSwarm(make_scenario(),
                                               MAX_ROUNDS).run())
        governed = quiet(lambda: GovernedSwarm(make_scenario(),
                                               MAX_ROUNDS).run())
        s = make_scenario()
        satisfiable = set(s.tasks) - s.poison_ids

        # baseline: wedged and oscillating
        assert not baseline.terminated_early
        assert baseline.rounds_used == MAX_ROUNDS
        assert "P" not in baseline.completed
        assert baseline.refused == set()
        assert baseline.total_flip_flops >= 50
        assert not ({"C1", "C2"} <= baseline.completed)

        # governed: refused, resolved, complete, early
        assert governed.terminated_early
        assert governed.rounds_used < MAX_ROUNDS
        assert governed.refused == {"P"}
        assert governed.attempts_after_refusal["P"] == 0
        assert governed.completed == satisfiable
        assert governed.total_flip_flops < LIVELOCK_BOUND
        assert governed.total_voluntary_idles > 0
        assert all(c <= DRIFT_BUDGET
                   for c in governed.epsilon_steps.values())


class TestSTB_DslOnVsOff:
    def test_dsl_off_progress_is_flat_not_degraded(self, monkeypatch):
        """ST-B: without the DSL the system is DEAD, not weaker —
        zero recorded ε-motion, nothing completes."""
        governed_on = quiet(lambda: GovernedSwarm(make_scenario(),
                                                  MAX_ROUNDS).run())
        assert sum(governed_on.epsilon_steps.values()) > 0

        from phi_pi_e_interpreter import PhiPiEInterpreterFixed
        monkeypatch.setattr(PhiPiEInterpreterFixed, "execute",
                            lambda self, code, context=None: None)
        governed_off = quiet(lambda: GovernedSwarm(make_scenario(),
                                                   MAX_ROUNDS).run())
        assert sum(governed_off.epsilon_steps.values()) == 0  # flat
        assert governed_off.completed == set()                # dead
        assert governed_off.total_dsl_calls > 0  # it TRIED; calls were empty


class TestSTC_IrreplaceabilityPin:
    def test_fake_epsilon_cannot_sustain_multiround_work(self):
        """ST-C headline, pinned so the experiment cannot drift:
        jump-to-goal fake-ε completes ZERO multi-round tasks (they
        stall after the jump and get refused as stagnant); the real
        bounded ε completes ALL of them. Gradualism is irreplaceable,
        not just load-bearing."""
        from experiments.swarm_phase1_compare import fake_math
        s = make_scenario()
        multi = {t.id for t in s.tasks.values() if t.duration > 1}
        assert multi  # scenario must actually contain multi-round tasks

        real = quiet(lambda: GovernedSwarm(make_scenario(),
                                           MAX_ROUNDS).run())
        with fake_math():
            fake = quiet(lambda: GovernedSwarm(make_scenario(),
                                               MAX_ROUNDS).run())

        assert multi <= real.completed          # real: all multi-round done
        assert not (multi & fake.completed)     # fake: none
        assert multi <= fake.refused            # wrongly refused as stagnant


class TestSTD_ParameterSweeps:
    @pytest.mark.parametrize("refusal_window", [5, 6, 7, 8])
    @pytest.mark.parametrize("num_agents", [10, 12, 15])
    def test_guarantees_hold_across_parameters(self, refusal_window,
                                               num_agents):
        """ST-D: G1-G3-class guarantees are properties of the design,
        not artifacts of one parameter point."""
        s = make_scenario(num_agents=num_agents)
        satisfiable = set(s.tasks) - s.poison_ids
        tr = quiet(lambda: GovernedSwarm(
            s, MAX_ROUNDS, refusal_window=refusal_window).run())
        assert tr.terminated_early
        assert tr.refused == {"P"}
        assert tr.attempts_on("P") == refusal_window
        assert tr.attempts_after_refusal["P"] == 0
        assert tr.completed == satisfiable
        assert tr.total_flip_flops < LIVELOCK_BOUND
        assert all(c <= DRIFT_BUDGET for c in tr.epsilon_steps.values())
