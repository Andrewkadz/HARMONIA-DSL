# SYSTEM_TESTS — Scenario-Level Test Specifications

Status: Spec for `feat/system-tests-phase1`. Rule (per process): no
system test without a spec entry here; spec and tests land in the
same commit. Unit/criterion tests (B1/B2, G1-G5) live in
`test_swarm_brain_phase1.py`; these are WHOLE-SYSTEM behaviors.

## ST-A: End-to-end behavioral difference (one scenario, both swarms)

Scenario: full Phase-1 world (poison + contention + healthy mix),
same seed, same harness, same ceiling.
Assert in a SINGLE test, so the complete behavioral contrast is one
falsifiable statement:
- baseline: hits ceiling, P unresolved, C1/C2 livelocked (50+
  flip-flops), no refusal concept;
- governed: early termination, P refused (exactly R attempts,
  permanent), C1/C2 completed with <10 flip-flops via voluntary
  idles, every satisfiable task completed, drift within budget.

## ST-B: DSL-on vs DSL-off (governance is not optional)

Same scenario, governed swarm twice: interpreter live vs
interpreter stubbed to no-op.
Assert: with DSL on, all guarantees hold; with DSL off, progress is
FLAT (zero recorded ε-steps, nothing completes) — not merely
degraded. Extends G4: the trace itself shows a dead system, not a
weaker one.

## ST-C: Fake-math experiment (experiments/, not tests/)

`experiments/swarm_phase1_compare.py` runs three variants on the
same scenario: baseline, governed (real math core), governed with
FAKE operators (ε jumps straight to goal; Φ identity; Λ constant),
and prints a comparison table + per-round highlights.

Purpose (honesty instrument): distinguishes LOAD-BEARING (G4 already
proves removal breaks the system) from IRREPLACEABLE (does this
specific math outperform trivial substitutes?).
Expected finding, stated in advance: fake-ε (jump-to-goal) should
BREAK multi-round tasks — progress requires fresh register motion
every round, and a register already at its goal cannot move again —
demonstrating that ε's proven gradualism (bounded, never-arriving
increments) is what makes sustained multi-round work expressible.
If the finding differs, the script's output is the evidence and this
spec gets amended, not the output.
A pinning test in tests/ asserts the experiment's headline result so
it cannot silently drift.

## ST-D: Parameter sweeps (robustness, not tuning)

Sweep refusal window R ∈ {5, 6, 7, 8} and agent count ∈ {10, 12, 15}
on the full scenario. For every combination assert the invariant
guarantees: early termination, P refused with exactly R attempts,
no livelock (<10 flip-flops), all satisfiable tasks complete, drift
within budget. R < 5 is excluded by design: R must exceed the
worst-case legitimate wait (~3 rounds, see SWARM_BRAIN_PHASE1
resolved items); sweeping into known-invalid territory tests the
documentation, not the system.

## Standing rule

Full suite (`python3 -m pytest tests/`) after every change; no merge
proposal unless green. Experiments print; tests assert. Anything an
experiment reveals that matters gets promoted to a pinned test.
