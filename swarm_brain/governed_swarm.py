"""Harmonia-governed swarm — SWARM_BRAIN_PHASE1.md.

Same scenario, same trace instrument, same round harness as the
baseline — differing ONLY in governance. Governance flows through the
REAL DSL path (G4): every agent owns a persistent FieldContext, and
all governance-relevant state evolution happens via
interpreter.execute() on .hrm program fragments:

    @self RE IM / @goal RE IM   register initialization at claim time
    ε @self @goal               work-step (progress IS register motion)
    Φ @self @goal               stabilization after resource conflict
    Λ @self @goal               observation -> lambda_obs (coherence)

Load-bearing by construction: a task round counts as productive ONLY
if the ε-step actually moved @self (register compared before/after the
DSL call). Stub out the DSL and nothing completes — pinned by the G4
negative test.

Governance rules (constants pinned by tests):
- REFUSAL_WINDOW = 5: a claimed task whose observable fails to improve
  for 5 consecutive rounds is REFUSED — permanently (Phase 1): it is
  never attempted again. Poison defense.
- DRIFT_BUDGET = 5: no (agent, task) pair may exceed 5 ε-steps.
  Structural bound checked from the trace (G3).
- Conflict resolution (livelock defense): after acquisition, agents
  holding a partial resource set form a conflict group. Each runs
  Φ-stabilization and a Λ-observation; the HIGHEST-lambda_obs
  contender keeps its holdings (ties: lowest agent id), all others
  release and take a voluntary idle round. No naive release-all retry,
  so no oscillation.
"""

import contextlib
import io
from typing import Dict, List, Optional, Set

from phi_pi_e_interpreter import FieldContext, PhiPiEInterpreterFixed

from .run_trace import RunTrace
from .task_spec import Scenario, Task

REFUSAL_WINDOW = 5
DRIFT_BUDGET = 5


class _Agent:
    def __init__(self, agent_id: int):
        self.id = agent_id
        self.ctx = FieldContext()          # persistent Harmonia context
        self.task: Optional[Task] = None
        self.held: List[str] = []
        self.progress = 0
        self.no_improve_rounds = 0
        self.last_distance: Optional[float] = None
        self.lambda_obs = 0.0
        self.backoff = 0        # rounds of voluntary idle remaining


class GovernedSwarm:
    def __init__(self, scenario: Scenario, max_rounds: int = 60):
        self.scenario = scenario
        self.max_rounds = max_rounds
        self.interpreter = PhiPiEInterpreterFixed()
        self._trace: Optional[RunTrace] = None

    # ---- the ONLY route to the DSL (instrumented for G4) ----
    def _dsl(self, ctx: FieldContext, program: str):
        self._trace.dsl_calls_per_round[-1] += 1
        with contextlib.redirect_stdout(io.StringIO()):
            return self.interpreter.execute(program, ctx)

    def _claim(self, agent: _Agent, task: Task):
        agent.task = task
        agent.progress = 0
        agent.no_improve_rounds = 0
        agent.last_distance = None
        ti = sorted(self.scenario.tasks).index(task.id)
        self._dsl(agent.ctx, f"@self {agent.id + 1}.0 0.5")
        self._dsl(agent.ctx, f"@goal {ti + 2}.0 -0.5")

    def _distance(self, agent: _Agent) -> float:
        return abs(agent.ctx.read_register('@self') -
                   agent.ctx.read_register('@goal'))

    def run(self) -> RunTrace:
        trace = RunTrace()
        self._trace = trace
        agents = [_Agent(i) for i in range(self.scenario.num_agents)]
        free: Set[str] = set(self.scenario.resources)
        claimed: Set[str] = set()

        for rnd in range(1, self.max_rounds + 1):
            trace.rounds_used = rnd
            trace.dsl_calls_per_round.append(0)
            events = []

            # claim ready tasks (refused tasks excluded — permanent)
            for agent in agents:
                if agent.task is None:
                    ready = self.scenario.ready_tasks(
                        trace.completed, claimed, trace.refused)
                    if ready:
                        self._claim(agent, ready[0])
                        claimed.add(agent.task.id)
                        events.append({"t": "claim", "a": agent.id,
                                       "task": agent.task.id})

            # idle agents adopt the highest-priority blocked task as a
            # WATCH target (bounded observation, unlike naive polling)
            blocked = [t for t in self.scenario.blocked_tasks(trace.completed)
                       if t.id not in trace.refused and t.id not in claimed]
            for agent in agents:
                if agent.task is None and blocked:
                    target = max(blocked, key=lambda t: (t.priority, t.id))
                    self._claim(agent, target)
                    claimed.add(target.id)
                    events.append({"t": "watch", "a": agent.id,
                                   "task": target.id})
                    blocked = [t for t in blocked if t.id != target.id]

            # two-phase resource acquisition (workable tasks only;
            # backing-off agents skip acquisition — voluntary idle
            # means yielding the round, not just releasing)
            for phase in range(2):
                for agent in agents:
                    if agent.task is None or not self._workable(agent, trace):
                        continue
                    if agent.backoff > 0:
                        continue  # yielded this round (decremented below)
                    missing = [r for r in agent.task.resources
                               if r not in agent.held]
                    if missing and missing[0] in free:
                        free.discard(missing[0])
                        agent.held.append(missing[0])

            # consume backoff AFTER acquisition (a backoff set during
            # round N's conflict must skip round N+1's acquisition —
            # decrementing at round end made it a no-op: bug caught by
            # the G2 completion test)
            for agent in agents:
                if agent.backoff > 0:
                    agent.backoff -= 1

            # conflict resolution: coherence-gated voluntary degradation
            conflicted = [a for a in agents if a.task is not None
                          and self._workable(a, trace) and a.held
                          and set(a.held) != set(a.task.resources)]
            if conflicted:
                for agent in conflicted:
                    self._dsl(agent.ctx, "Φ @self @goal")       # stabilize
                    agent.lambda_obs = self._dsl(agent.ctx, "Λ @self @goal") or 0.0
                winner = max(conflicted,
                             key=lambda a: (a.lambda_obs, -a.id))
                for agent in conflicted:
                    if agent is not winner:
                        free.update(agent.held)
                        agent.held = []
                        agent.backoff = 1
                        trace.voluntary_idles[agent.id] += 1
                        events.append({"t": "idle", "a": agent.id,
                                       "task": agent.task.id,
                                       "why": "coherence: yielded to "
                                              f"agent {winner.id} "
                                              f"(λ {winner.lambda_obs:.3f} > "
                                              f"{agent.lambda_obs:.3f})"})

            # work / observe / refuse
            for agent in agents:
                if agent.task is None:
                    continue
                task = agent.task
                if task.id in trace.refused:
                    trace.attempts_after_refusal[task.id] += 1
                    continue
                trace.attempts[task.id] += 1

                workable = self._workable(agent, trace)
                full_set = workable and \
                    set(agent.held) == set(task.resources)
                if full_set:
                    # productive round REQUIRES DSL register motion (G4)
                    before = agent.ctx.read_register('@self')
                    self._dsl(agent.ctx, "ε @self @goal")
                    after = agent.ctx.read_register('@self')
                    if after != before:
                        trace.epsilon_steps[(agent.id, task.id)] += 1
                        agent.progress += 1
                        events.append({"t": "eps", "a": agent.id,
                                       "task": task.id})
                    if agent.progress >= task.duration:
                        trace.completed.add(task.id)
                        events.append({"t": "complete", "a": agent.id,
                                       "task": task.id})
                        claimed.discard(task.id)
                        free.update(agent.held)
                        agent.task, agent.held, agent.progress = None, [], 0
                        continue

                # no-improvement accounting (refusal rule) applies ONLY to
                # structural blockage (deps unmet — the poison case) or
                # in-place stagnation (all resources held, no motion).
                # Resource starvation is queueing, not stagnation: waiting
                # for a busy resource must never trigger refusal.
                if workable and not full_set:
                    continue
                distance = self._distance(agent)
                if agent.last_distance is not None and \
                        distance < agent.last_distance - 1e-15:
                    agent.no_improve_rounds = 0
                else:
                    agent.no_improve_rounds += 1
                agent.last_distance = distance

                if agent.no_improve_rounds >= REFUSAL_WINDOW:
                    trace.refused.add(task.id)
                    events.append({"t": "refuse", "a": agent.id,
                                   "task": task.id,
                                   "why": f"observable stagnant for "
                                          f"{REFUSAL_WINDOW} rounds "
                                          f"(structural blockage)"})
                    claimed.discard(task.id)
                    free.update(agent.held)
                    agent.task, agent.held, agent.progress = None, [], 0

            trace.snapshot(
                rnd,
                {a.id: a.held for a in agents},
                events,
                {a.id: a.lambda_obs for a in agents if a.lambda_obs},
                {a.id: a.task.id for a in agents if a.task is not None})

            resolved = trace.completed | trace.refused
            if resolved == set(self.scenario.tasks):
                trace.terminated_early = True
                break

        self._trace = None
        return trace

    def _workable(self, agent: _Agent, trace: RunTrace) -> bool:
        """Deps met -> the task can actually be worked (vs watched)."""
        return all(d in trace.completed for d in agent.task.deps)
