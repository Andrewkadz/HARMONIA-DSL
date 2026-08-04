"""Shared task/resource model for both swarms (SWARM_BRAIN_PHASE1.md).

Fully mechanical and deterministic: the baseline and the governed swarm
run the exact same scenario objects, differing ONLY in governance.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass
class Task:
    id: str
    resources: List[str]        # acquisition order matters (naive livelock)
    duration: int               # rounds of holding all resources to finish
    deps: List[str] = field(default_factory=list)
    priority: int = 0           # higher = preferred


@dataclass
class Scenario:
    tasks: Dict[str, Task]
    resources: List[str]
    num_agents: int
    seed: int

    def ready_tasks(self, completed: Set[str], claimed: Set[str],
                    refused: Optional[Set[str]] = None) -> List[Task]:
        """Tasks whose deps are complete, not done/claimed/refused,
        ordered by priority (desc) then id (deterministic)."""
        refused = refused or set()
        out = [t for t in self.tasks.values()
               if t.id not in completed and t.id not in claimed
               and t.id not in refused
               and all(d in completed for d in t.deps)]
        return sorted(out, key=lambda t: (-t.priority, t.id))

    def blocked_tasks(self, completed: Set[str]) -> List[Task]:
        """Tasks that are incomplete and have unmet deps (incl. poison:
        deps that can NEVER be met because the dep id does not exist)."""
        return [t for t in self.tasks.values()
                if t.id not in completed
                and any(d not in completed for d in t.deps)]

    @property
    def poison_ids(self) -> Set[str]:
        """Tasks with a dependency that names no existing task —
        structurally unsatisfiable."""
        return {t.id for t in self.tasks.values()
                if any(d not in self.tasks for d in t.deps)}


def make_scenario(poison: bool = True, contention: bool = True,
                  seed: int = 7) -> Scenario:
    """Default Phase-1 scenario per SWARM_BRAIN_PHASE1.md.

    - 12 agents, 4 exclusive resources (R0-R3)
    - 8 satisfiable single-resource tasks on R2/R3
    - poison task P: depends on nonexistent 'GHOST' (never ready)
    - contention pair C1/C2: same resource set {R0, R1}, OPPOSITE
      acquisition order -> deterministic livelock under naive
      grab-partial/release-all retry
    """
    tasks: Dict[str, Task] = {}
    for i in range(8):
        tasks[f"T{i}"] = Task(id=f"T{i}", resources=[f"R{2 + i % 2}"],
                              duration=1 + i % 2)
    if poison:
        tasks["P"] = Task(id="P", resources=["R3"], duration=1,
                          deps=["GHOST"], priority=5)
    if contention:
        tasks["C1"] = Task(id="C1", resources=["R0", "R1"], duration=2,
                           priority=9)
        tasks["C2"] = Task(id="C2", resources=["R1", "R0"], duration=2,
                           priority=9)
    return Scenario(tasks=tasks, resources=["R0", "R1", "R2", "R3"],
                    num_agents=12, seed=seed)
