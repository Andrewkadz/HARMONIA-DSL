# SWARM_BRAIN_PHASE1 — First Governed Swarm Task

Status: Ratified 2026-08-03 (Andrew / Claude / Perplexity). Governs
`feat/swarm-brain-phase1`. G4 (governance authenticity) is
non-negotiable. Any deviation must be reflected here before
implementation. BRIDGE_DESIGN Step 3 is merged (prerequisite met).

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

## Resolved items (pinned at implementation, 2026-08-04)

- **Coherence comparison is local to the conflict group** (deviation
  from the global-mean leaning, logged here per process): agents with
  partial resource holdings form a conflict group; each runs
  Φ-stabilization then Λ-observation; the highest-lambda_obs
  contender keeps its holdings (ties: lowest id), all others release
  AND back off one full round (skip acquisition — yielding the round,
  not just the resources, is what breaks re-contention cycles).
  Global-mean thresholding deferred to Phase 2 with multi-group
  contention.
- **REFUSAL_WINDOW R = 5** consecutive rounds without observable
  improvement, counted ONLY under structural blockage (deps unmet —
  the poison case) or in-place stagnation (all resources held, no
  register motion). Resource starvation is queueing, not stagnation:
  rounds spent waiting for a busy resource never count toward
  refusal. (Discovered at implementation: without this distinction,
  agents queueing for shared resources were spuriously refused —
  caught by G1's full-completion assertion.)
- **Refusal is permanent** (Phase 1): refused tasks are excluded from
  claiming forever; attempts_after_refusal must stay 0. Cooldown is
  Phase 2.
- **DRIFT_BUDGET = 5** ε-steps per (agent, task). Note: the poison
  task accrues ZERO ε-steps (it is never workable — refusal comes
  from flat observations, not drift exhaustion), so the stricter
  "poison hits exactly the budget" variant does not apply; tests pin
  what is true: all pairs ≤ budget, poison = 0.
