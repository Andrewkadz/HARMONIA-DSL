"""Harmonic Capitalism Phase 1 — the naive-guard experiment.

Both worlds are competently written and share EVERYTHING except one
thing: how fast a position may move.

  teleport  — the agent computes a target position and executes it in
              full, in one step, after passing the solvency guard.
  bounded   — the same agent, same target, same guard, but the move is
              executed as a real ε-step through the DSL: position
              advances a bounded fraction of the distance per round.

Both run the IDENTICAL pre-trade guard:

    GUARD(P) ⇔ cash_after + P·p·(1 − STRESS) ≥ FLOOR

i.e. "would I still be solvent after an adverse move of STRESS?" —
the standard form of a margin requirement. The realised shock
(−35%) is larger than the guard's buffer (20%), so the guard is
necessary but not obviously sufficient.

The question this experiment asks: can the teleporting world be
rendered insolvent BETWEEN checks while the ε-bounded world cannot,
given the same guard? If yes, ε's gradualism is what upgrades the
guard from a hope to an invariant (the ST-C pattern in economics).
If no, that is a negative result and is published as one.
"""

import contextlib
import io
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from phi_pi_e_interpreter import FieldContext, PhiPiEInterpreterFixed

FLOOR = 0.0
STRESS = 0.20             # guard's assumed adverse move (both worlds)
SHOCK_MAG = -0.35         # realised shock — larger than the buffer
SHOCK_ROUNDS = (60, 63, 130, 133)
# Two-leg declines. Agents are near-flat before a crash (value tracks
# price, so no edge) and lever up buying the dip immediately after —
# the second leg is what tests solvency. This is the historically
# ordinary shape of a crash (1929, 2008), fixed in the world model.
ROUNDS = 200
MARGIN_LIMIT = 6.0        # borrowing capacity, both worlds
EXTRAP = 0.25             # value chases price (both worlds)
DRIFT = 0.012             # exogenous upward drift between shocks
EPS_GAIN = 40.0           # ε visibility scaling (still bounded)


@dataclass
class Agent:
    id: int
    cash: float
    inventory: float
    value: float
    ctx: FieldContext = field(default_factory=FieldContext)
    refusals: int = 0

    def net_worth(self, price: float) -> float:
        return self.cash + self.inventory * price

    def leverage(self, price: float) -> float:
        nw = self.net_worth(price)
        return (self.inventory * price) / nw if nw > 1e-9 else float('inf')


@dataclass
class MarketTrace:
    mode: str = ""
    prices: List[float] = field(default_factory=list)
    net_worth: Dict[int, List[float]] = field(default_factory=dict)
    leverage: Dict[int, List[float]] = field(default_factory=dict)
    breaches: List[tuple] = field(default_factory=list)
    refusals: Dict[int, int] = field(default_factory=dict)
    dsl_calls: int = 0
    final_wealth: Dict[int, float] = field(default_factory=dict)

    @property
    def breach_count(self) -> int:
        return len(self.breaches)

    @property
    def peak_leverage(self) -> float:
        return max((max(v) for v in self.leverage.values() if v), default=0.0)

    @property
    def min_net_worth(self) -> float:
        return min((min(v) for v in self.net_worth.values() if v), default=0.0)

    @property
    def total_terminal_wealth(self) -> float:
        return sum(self.final_wealth.values())


class Market:
    """mode: 'teleport' | 'bounded'."""

    def __init__(self, mode: str, seed: int = 11, floor: float = FLOOR,
                 shock_mag: float = SHOCK_MAG, stress: float = STRESS,
                 rounds: int = ROUNDS, n_agents: int = 4,
                 stub_dsl: bool = False):
        assert mode in ("teleport", "bounded")
        self.mode = mode
        self.floor = floor
        self.shock_mag = shock_mag
        self.stress = stress
        self.rounds = rounds
        self.stub_dsl = stub_dsl
        self.rng = random.Random(seed)
        self.price = 10.0
        self.interp = PhiPiEInterpreterFixed()
        self.agents = [Agent(id=i, cash=100.0, inventory=10.0,
                             value=10.0 + (i - (n_agents - 1) / 2) * 1.2)
                       for i in range(n_agents)]
        self._trace: Optional[MarketTrace] = None

    def _dsl(self, ctx: FieldContext, program: str):
        self._trace.dsl_calls += 1
        with contextlib.redirect_stdout(io.StringIO()):
            return self.interp.execute(program, ctx)

    # ---- identical in both worlds ----
    def _target_position(self, a: Agent) -> float:
        """Desired inventory given valuation and buying power."""
        edge = a.value - self.price
        if edge <= 0:
            # sell down proportionally to how overvalued the price is
            return a.inventory * max(0.0, 1.0 + edge / max(a.value, 1e-9))
        power = a.cash + MARGIN_LIMIT * max(a.net_worth(self.price), 0.0)
        conviction = min(1.0, edge / max(a.value, 1e-9))
        return a.inventory + (power * conviction) / max(self.price, 1e-9)

    def _guard(self, a: Agent, new_position: float) -> bool:
        """THE SAME pre-trade solvency guard in both worlds."""
        cost = (new_position - a.inventory) * self.price
        cash_after = a.cash - cost
        stressed = cash_after + new_position * self.price * (1 - self.stress)
        return stressed >= self.floor

    # ---- the ONLY difference: execution speed ----
    def _execute_position(self, a: Agent, target: float) -> float:
        if self.mode == "teleport":
            return target
        # bounded: a real ε-step in register space
        self._dsl(a.ctx, f"@self {a.inventory} 0.0")
        self._dsl(a.ctx, f"@goal {target} 0.0")
        before = a.ctx.read_register('@self')
        if not self.stub_dsl:
            self._dsl(a.ctx, "ε @self @goal")
        after = a.ctx.read_register('@self')
        dist = abs(complex(target, 0.0) - before)
        if dist < 1e-12:
            return a.inventory
        frac = min(1.0, (abs(after - before) / dist) * EPS_GAIN)
        return a.inventory + (target - a.inventory) * frac

    def run(self) -> MarketTrace:
        trace = MarketTrace(mode=self.mode)
        self._trace = trace
        for a in self.agents:
            trace.net_worth[a.id] = []
            trace.leverage[a.id] = []

        for t in range(1, self.rounds + 1):
            for a in self.agents:
                target = self._target_position(a)
                proposed = self._execute_position(a, target)
                if self._guard(a, proposed):
                    cost = (proposed - a.inventory) * self.price
                    a.cash -= cost
                    a.inventory = proposed
                else:
                    a.refusals += 1

            # world model, identical in both modes
            for a in self.agents:
                a.value += EXTRAP * (self.price - a.value)
            self.price = max(0.05, self.price *
                             (1.0 + DRIFT + self.rng.gauss(0, 0.015)))
            if t in SHOCK_ROUNDS:
                self.price = max(0.05, self.price * (1.0 + self.shock_mag))

            for a in self.agents:
                nw = a.net_worth(self.price)
                trace.net_worth[a.id].append(nw)
                trace.leverage[a.id].append(a.leverage(self.price))
                if nw < self.floor:
                    trace.breaches.append((t, a.id, nw))
            trace.prices.append(self.price)

        for a in self.agents:
            trace.refusals[a.id] = a.refusals
            trace.final_wealth[a.id] = a.net_worth(self.price)
        self._trace = None
        return trace


def run_pair(seed: int = 11, **kw):
    """Both worlds, identical seed, identical guard."""
    return (Market("teleport", seed=seed, **kw).run(),
            Market("bounded", seed=seed, **kw).run())
