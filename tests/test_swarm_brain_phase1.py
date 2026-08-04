# Tests for feat/swarm-brain-phase1 — SWARM_BRAIN_PHASE1.md
#
# B1/B2: the baseline (control) swarm demonstrably fails in the two
# documented ways. These tests PASS by asserting the failures occur —
# a control that doesn't break proves nothing about the treatment.
# G1-G5 (governed swarm) are added in the governed-swarm commit.

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from swarm_brain.baseline_swarm import BaselineSwarm
from swarm_brain.task_spec import make_scenario

MAX_ROUNDS = 60


class TestScenarioMechanics:
    def test_poison_task_is_structurally_unsatisfiable(self):
        s = make_scenario()
        assert s.poison_ids == {"P"}
        assert "GHOST" not in s.tasks

    def test_contention_pair_same_set_opposite_order(self):
        s = make_scenario()
        assert set(s.tasks["C1"].resources) == set(s.tasks["C2"].resources)
        assert s.tasks["C1"].resources != s.tasks["C2"].resources

    def test_determinism(self):
        t1 = BaselineSwarm(make_scenario(), MAX_ROUNDS).run()
        t2 = BaselineSwarm(make_scenario(), MAX_ROUNDS).run()
        assert t1.completed == t2.completed
        assert t1.total_flip_flops == t2.total_flip_flops
        assert dict(t1.attempts) == dict(t2.attempts)

    def test_healthy_scenario_completes(self):
        """Sanity: without pathologies the naive swarm finishes fine —
        the failures below are caused by the pathologies, not by a
        broken harness."""
        s = make_scenario(poison=False, contention=False)
        trace = BaselineSwarm(s, MAX_ROUNDS).run()
        assert trace.terminated_early
        assert trace.completed == set(s.tasks)


class TestB1PoisonNonTermination:
    """B1: naive swarm never terminates on the poison task; retry work
    grows linearly with the round ceiling; no refusal concept exists."""

    def test_hits_ceiling_without_finishing(self):
        s = make_scenario(poison=True, contention=False)
        trace = BaselineSwarm(s, MAX_ROUNDS).run()
        assert not trace.terminated_early
        assert trace.rounds_used == MAX_ROUNDS
        assert "P" not in trace.completed
        # every satisfiable task DID complete — P alone wedges the run
        assert trace.completed == set(s.tasks) - {"P"}

    def test_retry_work_grows_with_ceiling(self):
        s = make_scenario(poison=True, contention=False)
        short = BaselineSwarm(s, 30).run()
        long = BaselineSwarm(make_scenario(poison=True, contention=False),
                             MAX_ROUNDS).run()
        assert long.attempts_on("P") > short.attempts_on("P")
        assert long.attempts_on("P") >= 40  # sustained retry storm

    def test_no_refusal_concept(self):
        s = make_scenario(poison=True, contention=False)
        trace = BaselineSwarm(s, MAX_ROUNDS).run()
        assert trace.refused == set()


class TestB2ContentionLivelock:
    """B2: same-set/opposite-order pair livelocks under naive
    grab-partial/release-all retry; throughput on the pair is zero."""

    def test_livelock_flip_flops(self):
        s = make_scenario(poison=False, contention=True)
        trace = BaselineSwarm(s, MAX_ROUNDS).run()
        assert not trace.terminated_early
        assert "C1" not in trace.completed
        assert "C2" not in trace.completed
        assert trace.total_flip_flops >= 50  # sustained oscillation

    def test_livelock_is_perpetual_not_transient(self):
        """Flip-flops keep accruing in the second half of the run —
        the system is oscillating, not slowly resolving."""
        s = make_scenario(poison=False, contention=True)
        half = BaselineSwarm(make_scenario(poison=False, contention=True),
                             30).run()
        full = BaselineSwarm(s, MAX_ROUNDS).run()
        assert full.total_flip_flops > half.total_flip_flops * 1.5

    def test_normal_tasks_unaffected(self):
        """The livelock is isolated to the pair: satisfiable tasks on
        other resources still finish (fair-control check)."""
        s = make_scenario(poison=False, contention=True)
        trace = BaselineSwarm(s, MAX_ROUNDS).run()
        assert {f"T{i}" for i in range(8)} <= trace.completed


class TestBaselineUsesNoDSL:
    def test_zero_interpreter_involvement(self):
        """The control's failures owe nothing to Harmonia: the DSL is
        never invoked in a baseline run."""
        trace = BaselineSwarm(make_scenario(), MAX_ROUNDS).run()
        assert trace.total_dsl_calls == 0
