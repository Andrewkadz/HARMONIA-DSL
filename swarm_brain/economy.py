"""Harmonic Capitalism Phase 1 — toy market (ECONOMY_SIM_PHASE1.md).

Two worlds on identical seeds and identical shocks:

  ungoverned  — agents trade on their valuation rule alone; position
                changes are applied at full requested size (unbounded
                per-round motion).
  governed    — the SAME proposals pass through the Harmonia layer:
                position moves toward the target by a bounded ε-step
                (executed through the real DSL), net worth is observed
                via Λ into lambda_obs, and any step whose guarded
                worst case would breach FLOOR is REFUSED.

The invariant: net_worth = cash + inventory·price >= FLOOR (= 0.0),
for every agent, every round, in governed mode only.
"""

import contextlib
import io
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from phi_pi_e_interpreter import FieldContext, PhiPiEInterpreterFixed

FLOOR = 0.0
KAPPA = 0.15              # price impact per net unit of demand
Q_MAX = 5.0               # legacy cap (unused by the greedy rule)
Q_MAX_UNITS = 400.0       # max units per proposal (allows full margin use)
SHOCK_ROUNDS = (60, 130)  # fixed in the world model, not tuned post hoc
SHOCK_MAG = -0.35
ROUNDS = 200
MARGIN_LIMIT = 6.0        # ungoverned agents may borrow up to 6× net worth
# (a highly levered book: a −35% move wipes equity above ~2.9× leverage,
#  which is the mechanism this experiment is built to exhibit)
EXTRAP = 0.25             # extrapolative expectations: value chases price
DRIFT = 0.004             # exogenous price drift per round
# Governed motion: fraction of the requested move executed per round.
# Derived from the ε-step actually taken in register space (see
# _epsilon_fraction) — bounded by construction.
EPS_GAIN = 40.0


@dataclass
class Agent:
    id: int
    cash: float
    inventory: float
    value: float
    ctx: FieldContext = field(default_factory=FieldContext)
    refusals: int = 0
    insolvent_rounds: int = 0

    def net_worth(self, price: float) -> float:
        return self.cash + self.inventory * price


@dataclass
class MarketTrace:
    prices: List[float] = field(default_factory=list)
    net_worth: Dict[int, List[float]] = field(default_factory=dict)
    breaches: List[tuple] = field(default_factory=list)   # (round, agent, nw)
    refusals: Dict[int, int] = field(default_factory=dict)
    dsl_calls: int = 0
    final_wealth: Dict[int, float] = field(default_factory=dict)

    @property
    def breach_count(self) -> int:
        return len(self.breaches)

    @property
    def total_terminal_wealth(self) -> float:
        return sum(self.final_wealth.values())

    @property
    def survivors(self) -> List[int]:
        return [a for a, w in self.final_wealth.items() if w >= FLOOR]


class Market:
    """Both modes share this class; `governed` selects the pathway."""

    def __init__(self, governed: bool, seed: int = 11,
                 shock_mag: float = SHOCK_MAG, floor: float = FLOOR,
                 rounds: int = ROUNDS, fake_epsilon: bool = False,
                 n_agents: int = 4):
        self.governed = governed
        self.floor = floor
        self.shock_mag = shock_mag
        self.rounds = rounds
        self.fake_epsilon = fake_epsilon
        self.rng = random.Random(seed)
        self.price = 10.0
        self.interp = PhiPiEInterpreterFixed()
        self.agents = [
            Agent(id=i, cash=100.0, inventory=10.0,
                  value=10.0 + (i - (n_agents - 1) / 2) * 1.6)
            for i in range(n_agents)]
        self._trace: Optional[MarketTrace] = None

    # ---- the only route to the DSL (instrumented, per G4/ST-B) ----
    def _dsl(self, ctx: FieldContext, program: str):
        self._trace.dsl_calls += 1
        with contextlib.redirect_stdout(io.StringIO()):
            return self.interp.execute(program, ctx)

    def _epsilon_fraction(self, agent: Agent, target: float) -> float:
        """Fraction of the requested position change to execute this
        round, obtained from a real ε-step in register space.

        Registers: @self = (position, 0), @goal = (target, 0). The
        executed fraction is the ε displacement divided by the full
        distance — bounded by construction (errata E1), so a governed
        agent cannot teleport across the solvency floor.
        """
        pos = agent.inventory
        self._dsl(agent.ctx, f"@self {pos} 0.0")
        self._dsl(agent.ctx, f"@goal {target} 0.0")
        before = agent.ctx.read_register('@self')
        if self.fake_epsilon:
            # E-C substitution: jump straight to the goal (unbounded)
            agent.ctx.write_register('@self', complex(target, 0.0))
        else:
            self._dsl(agent.ctx, "ε @self @goal")
        after = agent.ctx.read_register('@self')
        dist = abs(complex(target, 0.0) - before)
        if dist < 1e-12:
            return 0.0
        frac = abs(after - before) / dist
        if not self.fake_epsilon:
            frac = min(1.0, frac * EPS_GAIN)   # visible but still bounded
        return frac

    def _observe(self, agent: Agent) -> float:
        """Solvency observable through Λ (dead if the DSL is stubbed)."""
        nw = agent.net_worth(self.price)
        self._dsl(agent.ctx, f"@nw {nw} 0.0")
        self._dsl(agent.ctx, f"@floor {self.floor} 1.0")
        self._dsl(agent.ctx, "Λ @nw @floor")
        return agent.ctx.lambda_obs

    def run(self) -> MarketTrace:
        trace = MarketTrace()
        self._trace = trace
        for a in self.agents:
            trace.net_worth[a.id] = []

        for t in range(1, self.rounds + 1):
            net_demand = 0.0
            for a in self.agents:
                edge = a.value - self.price
                if abs(edge) < 1e-9:
                    continue
                # Greedy rule (per spec): buy if price < value, sell if
                # price > value — sized by conviction against available
                # buying power (cash + margin). This is what makes the
                # book leveraged going into a shock.
                if edge > 0:
                    power = a.cash + MARGIN_LIMIT * max(
                        a.net_worth(self.price), 0.0)
                    conviction = min(1.0, edge / max(a.value, 1e-9))
                    q = (power * conviction) / max(self.price, 1e-9)
                else:
                    q = -min(a.inventory, a.inventory *
                             min(1.0, -edge / max(a.value, 1e-9)))
                q = max(-Q_MAX_UNITS, min(Q_MAX_UNITS, q))
                target = a.inventory + q

                if self.governed:
                    frac = self._epsilon_fraction(a, target)
                    q_exec = q * frac
                    self._observe(a)   # Λ observation drives the guard
                    if a.ctx.lambda_obs == 0.0 and not self.fake_epsilon:
                        # observable is dead (DSL stubbed) -> cannot govern
                        q_exec = 0.0
                    # guarded worst case: does this step's own cost
                    # leave net worth above the floor?
                    cost = q_exec * self.price
                    nw_after = (a.cash - cost) + (a.inventory + q_exec) * self.price
                    if nw_after < self.floor or a.cash - cost < -1e-9:
                        a.refusals += 1
                        continue
                else:
                    # Ungoverned: trades on margin. Cash may go negative
                    # (borrowing) up to MARGIN_LIMIT × current net worth —
                    # the standard mechanism by which a leveraged book is
                    # rendered insolvent by an adverse price move.
                    q_exec = q
                    cost = q_exec * self.price
                    borrow = max(0.0, cost - a.cash)
                    if borrow > MARGIN_LIMIT * max(a.net_worth(self.price), 0.0):
                        allowed = a.cash + MARGIN_LIMIT * max(
                            a.net_worth(self.price), 0.0)
                        q_exec = allowed / self.price if self.price > 0 else 0.0
                        q_exec = max(0.0, min(q, q_exec)) if q > 0 else q
                        cost = q_exec * self.price
                    if a.inventory + q_exec < 0:
                        q_exec = -a.inventory
                        cost = q_exec * self.price

                a.cash -= cost
                a.inventory += q_exec
                net_demand += q_exec

            # --- extrapolative expectations (world model, both modes) ---
            # Valuations drift toward the recent price: the standard
            # behavioral-finance mechanism by which a rising market
            # keeps agents levered into it. Identical in both worlds.
            for a in self.agents:
                a.value += EXTRAP * (self.price - a.value)

            # --- price update ---
            # Price-taking agents: the price path is exogenous (a mild
            # upward drift with noise), so no agent can inflate its own
            # collateral. This keeps the solvency mechanism visible
            # rather than drowned in a demand-driven bubble.
            self.price = max(0.05, self.price * (1.0 + DRIFT
                                                 + self.rng.gauss(0, 0.02)))

            # --- shocks: applied AFTER the round's trading, so the
            # crash lands on the book agents have just built (fixed
            # schedule, part of the world model, both modes) ---
            if t in SHOCK_ROUNDS:
                self.price = max(0.05, self.price * (1.0 + self.shock_mag))

            # --- record + invariant check ---
            for a in self.agents:
                nw = a.net_worth(self.price)
                trace.net_worth[a.id].append(nw)
                if nw < self.floor:
                    a.insolvent_rounds += 1
                    trace.breaches.append((t, a.id, nw))
            trace.prices.append(self.price)

        for a in self.agents:
            trace.refusals[a.id] = a.refusals
            trace.final_wealth[a.id] = a.net_worth(self.price)
        self._trace = None
        return trace


def run_pair(seed: int = 11, **kw):
    """Both worlds, identical seed and shocks."""
    return (Market(governed=False, seed=seed, **kw).run(),
            Market(governed=True, seed=seed, **kw).run())
