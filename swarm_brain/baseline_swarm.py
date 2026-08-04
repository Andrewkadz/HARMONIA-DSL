"""Baseline (control) swarm — SWARM_BRAIN_PHASE1.md.

Plain Python agents, NO Harmonia: greedy task selection, unbounded
retry, no refusal concept, no coherence signal. This swarm is DESIGNED
to exhibit the documented failure modes (B1 poison non-termination,
B2 contention livelock) as the control against which the governed
swarm is measured. It must be a fair control: same scenario objects,
same trace instrument, same round harness — differing only in
governance.

Naive protocol per round:
1. Agents holding all their task's resources make progress; a task
   completes after `duration` rounds of full possession.
2. Unassigned agents claim the highest-priority ready task (greedy).
   Agents whose task is blocked (unmet deps) RETRY the dep check every
   round, forever (attempts counter grows — the poison pathology).
3. Resource acquisition is two-phase across agents (everyone grabs
   their first missing resource in agent order, then everyone tries
   their next). An agent that ends the round without full possession
   releases everything it holds (flip-flop) and retries next round —
   the livelock pathology for same-set/opposite-order pairs.
"""

from typing import Dict, List, Optional, Set

from .run_trace import RunTrace
from .task_spec import Scenario, Task


class _Agent:
    def __init__(self, agent_id: int):
        self.id = agent_id
        self.task: Optional[Task] = None
        self.held: List[str] = []
        self.progress = 0


class BaselineSwarm:
    def __init__(self, scenario: Scenario, max_rounds: int = 60):
        self.scenario = scenario
        self.max_rounds = max_rounds

    def run(self) -> RunTrace:
        trace = RunTrace()
        agents = [_Agent(i) for i in range(self.scenario.num_agents)]
        free: Set[str] = set(self.scenario.resources)
        claimed: Set[str] = set()

        for rnd in range(1, self.max_rounds + 1):
            trace.rounds_used = rnd
            trace.dsl_calls_per_round.append(0)  # baseline: DSL never used
            events = []

            # (2) claim ready tasks greedily
            for agent in agents:
                if agent.task is None:
                    ready = self.scenario.ready_tasks(trace.completed, claimed)
                    if ready:
                        agent.task = ready[0]
                        claimed.add(ready[0].id)
                        events.append({"t": "claim", "a": agent.id,
                                       "task": ready[0].id})

            # blocked-task retry storm: idle agents poll blocked tasks
            blocked = self.scenario.blocked_tasks(trace.completed)
            for agent in agents:
                if agent.task is None and blocked:
                    # naive: retry the highest-priority blocked task's
                    # dep-check every round, forever
                    target = max(blocked, key=lambda t: (t.priority, t.id))
                    trace.attempts[target.id] += 1
                    events.append({"t": "retry_blocked", "a": agent.id,
                                   "task": target.id})

            # (3) two-phase resource acquisition
            for phase in range(2):
                for agent in agents:
                    if agent.task is None:
                        continue
                    missing = [r for r in agent.task.resources
                               if r not in agent.held]
                    if missing and missing[0] in free:
                        free.discard(missing[0])
                        agent.held.append(missing[0])

            # (1) progress or flip-flop
            for agent in agents:
                if agent.task is None:
                    continue
                trace.attempts[agent.task.id] += 1
                if set(agent.held) == set(agent.task.resources):
                    agent.progress += 1
                    if agent.progress >= agent.task.duration:
                        trace.completed.add(agent.task.id)
                        events.append({"t": "complete", "a": agent.id,
                                       "task": agent.task.id})
                        claimed.discard(agent.task.id)
                        free.update(agent.held)
                        agent.task, agent.held, agent.progress = None, [], 0
                elif agent.held:
                    # naive backoff: release everything, try again later
                    trace.flip_flops[agent.task.id] += 1
                    events.append({"t": "flip", "a": agent.id,
                                   "task": agent.task.id})
                    free.update(agent.held)
                    agent.held = []
                    agent.progress = 0

            trace.snapshot(
                rnd,
                {a.id: a.held for a in agents},
                events, {},
                {a.id: a.task.id for a in agents if a.task is not None})

            if len(trace.completed) == len(self.scenario.tasks):
                trace.terminated_early = True
                break

        return trace
