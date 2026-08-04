"""Structured run trace emitted by BOTH swarms (SWARM_BRAIN_PHASE1.md).

The comparative tests (B1/B2 vs G1-G5) read only this trace, so the
baseline and governed runs are judged by identical instruments.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class RunTrace:
    rounds_used: int = 0
    terminated_early: bool = False      # True = finished before ceiling
    completed: Set[str] = field(default_factory=set)
    refused: Set[str] = field(default_factory=set)
    # per-task counters
    attempts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    flip_flops: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    # governance instrumentation (G4): interpreter.execute() invocations
    # attributed to governance decisions, per round
    dsl_calls_per_round: List[int] = field(default_factory=list)
    # voluntary idles (coherence gating), per agent id
    voluntary_idles: Dict[int, int] = field(default_factory=lambda: defaultdict(int))

    @property
    def total_flip_flops(self) -> int:
        return sum(self.flip_flops.values())

    @property
    def total_dsl_calls(self) -> int:
        return sum(self.dsl_calls_per_round)

    def attempts_on(self, task_id: str) -> int:
        return self.attempts[task_id]
