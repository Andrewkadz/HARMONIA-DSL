# Tests for feat/swarm-brain-phase1 — SWARM_BRAIN_PHASE1.md
#
# B1/B2: the baseline (control) swarm demonstrably fails in the two
# documented ways. These tests PASS by asserting the failures occur —
# a control that doesn't break proves nothing about the treatment.
# G1-G5 (governed swarm) are added in the governed-swarm commit.

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from swarm_brain.baseline_swarm import BaselineSwarm
from swarm_brain.governed_swarm import (
    DRIFT_BUDGET,
    REFUSAL_WINDOW,
    GovernedSwarm,
)
from swarm_brain.task_spec import make_scenario

MAX_ROUNDS = 60
LIVELOCK_BOUND = 10
MIN_DSL_CALLS = 1


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


# ===================== GOVERNED SWARM: G1-G5 =====================

class TestG1PoisonRefusal:
    """G1: governed run terminates within the ceiling, refuses the
    poison task explicitly after exactly REFUSAL_WINDOW attempts,
    completes every satisfiable task; refusal is permanent."""

    def test_terminates_with_refusal_and_full_completion(self):
        s = make_scenario(poison=True, contention=False)
        trace = GovernedSwarm(s, MAX_ROUNDS).run()
        assert trace.terminated_early
        assert trace.rounds_used < MAX_ROUNDS
        assert "P" in trace.refused
        assert trace.completed == set(s.tasks) - {"P"}

    def test_bounded_attempts_exactly_refusal_window(self):
        s = make_scenario(poison=True, contention=False)
        trace = GovernedSwarm(s, MAX_ROUNDS).run()
        assert trace.attempts_on("P") == REFUSAL_WINDOW

    def test_refusal_is_permanent(self):
        s = make_scenario(poison=True, contention=False)
        trace = GovernedSwarm(s, MAX_ROUNDS).run()
        assert trace.attempts_after_refusal["P"] == 0

    def test_governed_attempts_strictly_below_baseline(self):
        governed = GovernedSwarm(
            make_scenario(poison=True, contention=False), MAX_ROUNDS).run()
        baseline = BaselineSwarm(
            make_scenario(poison=True, contention=False), MAX_ROUNDS).run()
        assert baseline.attempts_on("P") > governed.attempts_on("P")


class TestG2ContentionResolution:
    """G2: governed run resolves the contention pair below the livelock
    bound via voluntary degradation; baseline exceeds it."""

    def test_no_livelock_and_full_completion(self):
        s = make_scenario(poison=False, contention=True)
        trace = GovernedSwarm(s, MAX_ROUNDS).run()
        assert trace.terminated_early
        assert trace.total_flip_flops < LIVELOCK_BOUND
        assert "C1" in trace.completed and "C2" in trace.completed
        assert trace.completed == set(s.tasks)

    def test_resolution_via_voluntary_degradation(self):
        s = make_scenario(poison=False, contention=True)
        trace = GovernedSwarm(s, MAX_ROUNDS).run()
        assert trace.total_voluntary_idles > 0  # yielded, not starved

    def test_baseline_exceeds_bound_governed_does_not(self):
        governed = GovernedSwarm(
            make_scenario(poison=False, contention=True), MAX_ROUNDS).run()
        baseline = BaselineSwarm(
            make_scenario(poison=False, contention=True), MAX_ROUNDS).run()
        assert baseline.total_flip_flops >= 50
        assert governed.total_flip_flops < LIVELOCK_BOUND


class TestG3BoundedDrift:
    """G3: no (agent, task) pair exceeds the drift budget; the poison
    task accrues zero ε-steps (refused via flat observation, not
    drift exhaustion — see SWARM_BRAIN_PHASE1 resolved items)."""

    def test_all_pairs_within_budget(self):
        s = make_scenario(poison=True, contention=True)
        trace = GovernedSwarm(s, MAX_ROUNDS).run()
        assert trace.epsilon_steps  # instrument actually recorded work
        for (agent_id, task_id), count in trace.epsilon_steps.items():
            assert count <= DRIFT_BUDGET, (agent_id, task_id, count)

    def test_poison_gets_zero_epsilon_steps(self):
        s = make_scenario(poison=True, contention=False)
        trace = GovernedSwarm(s, MAX_ROUNDS).run()
        poison_steps = [c for (a, t), c in trace.epsilon_steps.items()
                        if t == "P"]
        assert sum(poison_steps) == 0


class TestG4GovernanceAuthenticity:
    """G4 (non-negotiable): the DSL is load-bearing. Every governance
    round invokes the interpreter; stubbing the DSL path to a no-op
    destroys the governed guarantees."""

    def test_dsl_invoked_every_round(self):
        s = make_scenario(poison=True, contention=True)
        trace = GovernedSwarm(s, MAX_ROUNDS).run()
        assert trace.total_dsl_calls > 0
        for rnd, calls in enumerate(trace.dsl_calls_per_round, start=1):
            assert calls >= MIN_DSL_CALLS, f"round {rnd} made no DSL calls"

    def test_noop_dsl_destroys_governed_guarantees(self, monkeypatch):
        """The falsifiability test: with interpreter.execute stubbed
        out, register motion stops, so productive progress stops, and
        the governed swarm can no longer complete its tasks. Harmonia
        is the brain, not a sticker."""
        from phi_pi_e_interpreter import PhiPiEInterpreterFixed
        monkeypatch.setattr(
            PhiPiEInterpreterFixed, "execute",
            lambda self, code, context=None: None)
        s = make_scenario(poison=True, contention=True)
        trace = GovernedSwarm(s, MAX_ROUNDS).run()
        satisfiable = set(s.tasks) - s.poison_ids
        assert trace.completed != satisfiable  # G1 guarantee collapses

    def test_governed_determinism(self):
        t1 = GovernedSwarm(make_scenario(), MAX_ROUNDS).run()
        t2 = GovernedSwarm(make_scenario(), MAX_ROUNDS).run()
        assert t1.completed == t2.completed
        assert t1.refused == t2.refused
        assert t1.rounds_used == t2.rounds_used
        assert dict(t1.epsilon_steps) == dict(t2.epsilon_steps)


class TestG5SuiteIntegrity:
    """G5: swarm code imports the substrate but modifies nothing —
    the canonical fixture still holds with swarm modules loaded.
    (The rest of G5 is the full suite run itself.)"""

    def test_canonical_fixture_with_swarm_loaded(self):
        import contextlib
        import io
        from phi_pi_e_interpreter import PhiPiEInterpreterFixed
        interp = PhiPiEInterpreterFixed()
        with contextlib.redirect_stdout(io.StringIO()):
            result = interp.execute("Φ 5.0\nΨ 3.0\nε 0.2\nΣ")
        assert abs(result - 6.4) < 1e-9


class TestFullScenarioIntegration:
    """Both pathologies at once: the governed swarm refuses the poison,
    resolves the contention, completes everything else, and terminates
    early. The complete Phase-1 claim in one run."""

    def test_full_governed_run(self):
        s = make_scenario(poison=True, contention=True)
        trace = GovernedSwarm(s, MAX_ROUNDS).run()
        assert trace.terminated_early
        assert trace.refused == {"P"}
        assert trace.completed == set(s.tasks) - {"P"}
        assert trace.total_flip_flops < LIVELOCK_BOUND
        assert trace.total_voluntary_idles > 0
