# ECONOMY_SIM_PHASE1 — Harmonic Capitalism, Solvency Invariant

Status: Ratified 2026-08-04 (Andrew). Governs `feat/economy-phase1`.
Settled: FLOOR = 0 net worth (hard invariant); REFUSE, never clamp;
−35% shocks at rounds 60 and 130 fixed as part of the world model,
not tuned post hoc; governance cost reported as a headline metric. Follows SWARM_BRAIN_PHASE1 discipline: spec first, tests in
the same commit, guarantee must be falsifiable, DSL must be
load-bearing (the G4 lesson).

## Scope and honesty clause

A toy market demonstrating ONE guarantee: in the governed market no
agent crosses a solvency floor; in the ungoverned market, under the
same seed and shocks, agents do. This is a mechanical simulation, not
a model of any real economy, and it tests a *mechanism*, not the
Harmonic Capitalism thesis. Nothing here validates V = (H×D×S)/W×f(T).

## The market

- 4 agents, 1 asset, T = 200 rounds, seeded RNG (deterministic).
- Agent state: `cash_i` (starts 100.0), `inventory_i` (starts 10.0
  units), private valuation `value_i`.
- Public price `p_t`, starts 10.0.
- Each round: every agent posts one proposal — BUY q units if
  `p_t < value_i`, SELL q units if `p_t > value_i`, else HOLD. Size
  `q` scales with the perceived edge, capped at `q_max = 5`.
- Trades clear against a market maker at `p_t` (no order matching —
  keeps the mechanism visible).
- Price update: `p_{t+1} = p_t + κ·(net demand) + shock_t`, with
  `κ = 0.15` and `shock_t` drawn from the seeded RNG.
- **Stress schedule (the engine of insolvency):** at rounds 60 and
  130 a large negative price shock (−35%) fires. Agents holding
  inventory bought on depleted cash take mark-to-market losses.

## The solvency invariant

    NET_WORTH_i(t) = cash_i(t) + inventory_i(t) · p_t
    SOLVENT_i(t)  ⟺  NET_WORTH_i(t) ≥ FLOOR,   FLOOR = 0.0

Governed guarantee (the headline): **for all agents i and all rounds
t, NET_WORTH_i(t) ≥ FLOOR.** Ungoverned expectation: at least one
agent's net worth crosses below FLOOR after a shock.

Note on why net worth and not cash: a pure cash floor is trivially
enforced by refusing to overspend and would prove nothing. Net worth
can be broken by *price movement after a trade* — which is precisely
the case where a naive guard is insufficient and the ε argument
below matters.

## The naive-guard failure mode (why this is not one `if`)

In the presence of discontinuous price jumps or unbounded trade moves,
a pre-trade solvency check is NOT sufficient: an agent can pass the
check and still be rendered insolvent by post-trade price motion. The
guard answers "is this trade safe now?" while insolvency arrives from
the interval *between* checks. Any system whose state can move an
unbounded distance per step can only hope its guard was enough.

## Why ε makes the guard sufficient (the provable part)

Register motion per round is bounded by the math core's ε operator:

    |ε(z,w) − z| = ε·d / (1 + ε·d) < min(ε·d, 1),   d = |w − z|
    (errata E1 — the corrected bound; the PDF's stated ≤ ε holds
     only for d ≲ 1.001)

Consequently a single governed step moves an agent's position by a
strictly bounded amount. Any path from SOLVENT (net worth ≥ 0) to
INSOLVENT (< 0) must therefore pass through a band of width ≥ the
maximum single-step displacement — a *guardable band*, visible to the
pre-trade check before the floor is reached. Unbounded motion admits
no such band: the state can be above the floor at check time and
below it after one step, with nothing observable in between.

This is the whole argument. The guard is the same one line in both
worlds; only under bounded motion is that line an invariant rather
than a hope.

## Where Harmonia's mathematics actually enters

This is the section that decides whether the experiment is honest.
A solvency check alone is one `if` statement; if that were all
governance did, Harmonia would be decoration. Three specific,
testable roles:

1. **ε makes the guard sufficient rather than hopeful.** Agent state
   lives in registers; position moves toward its target allocation by
   `ε @self @target` — bounded increments, provably ≤ ε·|w−z| per
   step (math core, errata E1). Because no agent can teleport, the
   distance to the floor cannot be crossed between checks: a pre-trade
   guard plus bounded motion gives an invariant, where a guard plus
   unbounded jumps gives only a hope. **Falsifiable:** substituting
   jump-to-target ε in governed mode must produce floor violations
   (the ST-C substitution, applied to economics).
2. **Λ is the solvency observable.** Net worth enters the DSL as a
   register pair and is read out through `Λ @self @floor` into
   `lambda_obs`; the governance decision reads the observable, not a
   Python float. Stub the interpreter and the observable is dead —
   governance collapses (the ST-B condition).
3. **Refusal is the swarm's existing primitive.** A proposal whose
   post-trade worst case breaches FLOOR is REFUSED and logged with a
   reason — the same mechanism that refuses the poison task, applied
   to a trade. Refusals are recorded per agent per round.

## Expected results (stated in advance, per ST-C practice)

- Ungoverned: ≥1 agent below FLOOR after round 60 or 130; total
  insolvency-rounds > 0; some agents may end with negative net worth.
- Governed: zero floor breaches across all agents and all rounds;
  refusals concentrated immediately before/after shocks; aggregate
  wealth LOWER than ungoverned best-case (governance costs return —
  this must be reported, not hidden).
- Predicted honest tension: governed agents will underperform in
  calm periods. If governance were free, the experiment would be
  suspicious.

## Tests (E-series, in the ST style)

- **E-A (teleport breaches):** the teleporting world, running the SAME guard, is rendered insolvent between checks. Passes by asserting failure.
  produces ≥1 agent-round below FLOOR. Passes by asserting failure.
- **E-B (governed holds):** same seed, same shocks — no agent-round
  below FLOOR, for every agent, every round.
- **E-C (ε is load-bearing):** substituting ε with a jump-to-target
  operator breaks the invariant under the same conditions,
  demonstrating that the theorem's gradualism is essential, not
  cosmetic. Direct economic analogue of ST-C.
- **E-D (DSL is load-bearing):** interpreter stubbed to no-op →
  governance guarantees collapse (breaches occur or nothing trades).
- **E-E (cost is reported):** governed final aggregate wealth is
  recorded and compared to ungoverned; the test asserts the number is
  *reported*, not that governance wins on return.
- **E-F (sweep):** floor ∈ {0, 25, 50} × shock magnitude ∈ {25%, 35%,
  45%}: governed holds the invariant across all nine.

## Artifacts

    swarm_brain/economy.py                     market + both modes
    experiments/harmonic_capitalism_phase1.py  runs both, logs paths
    tests/test_economy_phase1.py               E-A … E-F

Branch: `feat/economy-phase1`, stacked on current main.

## Open items (need your sign-off)

1. **FLOOR = 0 net worth** — or a positive margin (e.g. 25) so
   governance must act *before* zero? Leaning 0 for Phase 1: the
   cleanest possible statement.
2. **Refusal granularity:** refuse the whole trade, or clamp it to
   the largest solvency-preserving size? Leaning REFUSE (matches the
   swarm's existing primitive; clamping is Phase 2).
3. **Shock magnitude −35% at rounds 60/130** — enough to break the
   ungoverned market without being absurd?
4. Any objection to reporting governance's *cost* as a headline
   number alongside the guarantee? I think it's essential for
   credibility.
