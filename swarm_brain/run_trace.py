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
    # ε work-steps per (agent_id, task_id) — the G3 drift instrument
    epsilon_steps: Dict[tuple, int] = field(default_factory=lambda: defaultdict(int))
    # attempts recorded after a task was refused (must stay 0: permanent refusal)
    attempts_after_refusal: Dict[str, int] = field(default_factory=lambda: defaultdict(int))

    # per-round snapshots for visualization (additive; tests and
    # governance logic never read these)
    per_round: List[dict] = field(default_factory=list)

    @property
    def total_voluntary_idles(self) -> int:
        return sum(self.voluntary_idles.values())

    def snapshot(self, rnd: int, holdings: Dict[int, List[str]],
                 events: List[dict], lam: Dict[int, float],
                 assignments: Dict[int, str],
                 zpos: Dict[int, complex] = None,
                 zgoal: Dict[int, complex] = None) -> None:
        """Record one round's state for the visualizer.

        zpos/zgoal: the agents' actual @self/@goal register values —
        positions on the complex plane. Governed swarm only (the
        baseline has no registers, hence no field to move on)."""
        extra = {}
        if zpos is not None:
            extra["z"] = {str(a): [round(v.real, 6), round(v.imag, 6)]
                          for a, v in zpos.items()}
        if zgoal is not None:
            extra["g"] = {str(a): [round(v.real, 6), round(v.imag, 6)]
                          for a, v in zgoal.items()}
        self.per_round.append({
            **extra,
            "r": rnd,
            "hold": {str(a): list(rs) for a, rs in holdings.items() if rs},
            "assign": {str(a): t for a, t in assignments.items()},
            "done": sorted(self.completed),
            "ref": sorted(self.refused),
            "ev": events,
            "lam": {str(a): round(v, 4) for a, v in lam.items()},
            "dsl": self.dsl_calls_per_round[-1] if self.dsl_calls_per_round else 0,
        })

    @property
    def total_flip_flops(self) -> int:
        return sum(self.flip_flops.values())

    @property
    def total_dsl_calls(self) -> int:
        return sum(self.dsl_calls_per_round)

    def attempts_on(self, task_id: str) -> int:
        return self.attempts[task_id]
