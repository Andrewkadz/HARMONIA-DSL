# SWARM_BRAIN_PHASE1 — First Governed Swarm Task

Status: DRAFT — awaiting ratification (Andrew / Claude / Perplexity).
No implementation until this document is ratified. Depends on
BRIDGE_DESIGN Step 3 (binary register forms) being merged.

## Scope and non-goals

We are building a governed, swarm-based cognitive system: agents whose
state lives in Harmonia registers, whose interaction/recursion/stopping
are governed by Harmonia operators and ANIMUS-style coherence. We are
NOT claiming consciousness, qualia, or AGI. Harmonia is the governance
layer and state substrate; metaphysics stays commentary, never contract
(per the proofs' own disclaimer and CONTRIBUTING).

## The demonstration task

**Constrained resource allocation with conflicting goals and one
unsatisfiable subgoal ("poison task").**

Setup: N agents (default 12), M shared resources (default 4, each
exclusive-use per round), and a task list with dependencies. Tasks
consume resources for k rounds. Two pathologies are built in:

1. **Poison task:** one task's dependency is unsatisfiable (depends on
   a task that never completes). Naive decomposition/retry recurses on
   it forever.
2. **Contention pair:** two high-priority tasks require overlapping
   resource sets, so greedy agents deadlock or oscillate (acquire,
   block, release, re-acquire — livelock).

Why this task: both failure modes are *mechanical*, reproducible, and
measurable — no LLM, no randomness beyond a seeded RNG. The comparison
is therefore exact and CI-testable.

## Baseline swarm (the control)

`swarm_brain/baseline_swarm.py` — plain Python agents, no Harmonia:
greedy task selection, unbounded retry on failure, no refusal concept,
no coherence signal. Expected demonstrated failures (pinned by tests):

- B1: never terminates on the poison task (hits the harness's external
  step ceiling with no answer, work wasted on retries grows linearly).
- B2: livelock/oscillation on the contention pair (resource flip-flops
  exceed a threshold; throughput collapses).

The baseline must be a *fair* control: same task representation, same
step harness, same seed — differing ONLY in governance.

## Governed swarm (the Harmonia brain)

`swarm_brain/governed_swarm.py`. **Hard rule: governance decisions flow
through the real DSL path** — each agent owns a persistent
`FieldContext`, and its governance state is evolved by calling
`interpreter.execute(...)` on `.hrm` program fragments. No
Python-side shortcut may compute what the DSL layer is supposed to
decide; otherwise the demo is branding, not governance.

Per-agent state (all in zfield):
- `@self` — the agent's state register (position in task-space,
  initialized from task/agent ids).
- `@goal` — register encoding its current task target.
- Per-round evolution: `ε @self @goal` (incremental progress),
  `Φ @self @goal` (stabilization after conflict).

Governance signals:
- **Drift budget / refusal:** each failed attempt on a task runs an
  ε-step; the agent's accumulated distance-from-goal is observed via
  `Λ @self @goal` → `lambda_obs`. A task whose observable fails to
  improve over R rounds (R default 5) is REFUSED: marked
  unsatisfiable-for-now, agent moves on. This is the poison-task
  defense: bounded attempts, explicit refusal, no unbounded recursion.
- **Coherence gating (ANIMUS):** swarm coherence = aggregate of agent
  `lambda_obs` values (exact aggregation pinned at implementation).
  When coherence drops below threshold θ_low, the LOWEST-coherence
  agents voluntarily idle one round (voluntary degradation) instead of
  contending. This is the livelock defense: contention resolves by
  principled backoff, not starvation or randomness.
- **Hard caps:** every loop in the system has an iteration ceiling
  (existing `[..]`=10 semantics; harness rounds capped). Termination
  is guaranteed structurally, not hoped for.

## Success criteria (each pinned by a test)

- G1: governed swarm terminates on the poison scenario with an explicit
  refusal record for the poison task and completes all satisfiable
  tasks. Baseline B1 demonstrably does not.
- G2: governed swarm resolves the contention pair with zero livelock
  (flip-flop count under bound); baseline B2 exceeds it.
- G3: bounded drift: no agent's ε-step count on any single task exceeds
  the budget; assertable from the run trace.
- G4: governance authenticity: tests assert the interpreter was
  actually invoked for governance decisions (e.g. run-trace records
  execute() calls per round; a governed run with the DSL path stubbed
  out must fail its assertions).
- G5: the entire existing suite (255) stays green; swarm code imports
  the interpreter and math core but modifies neither.

## Module layout

    swarm_brain/
      __init__.py
      task_spec.py        # shared task/resource model (both swarms)
      baseline_swarm.py   # control
      governed_swarm.py   # Harmonia-governed
      run_trace.py        # structured trace both swarms emit
    tests/test_swarm_brain_phase1.py

## Open items (settle at implementation, leanings recorded)

- Coherence aggregation: leaning mean of per-agent normalized
  lambda_obs with θ_low ≈ 0.3× initial coherence; exact form pinned by
  test at implementation.
- Refusal window R: leaning 5 rounds; must be small enough that the
  poison test runs fast, large enough to be non-trivial.
- Whether refusal is permanent or retry-after-cooldown: leaning
  permanent for Phase 1 (simplest honest semantics; cooldown is a
  Phase 2 concern).
