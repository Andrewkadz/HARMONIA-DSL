# BRIDGE_DESIGN — ℂ ↔ Context Bridge Architecture

Status: Ratified 2026-08-03 (Andrew / Claude / Perplexity review).
Governs `feat/complex-bridge`. Any deviation must be reflected here
before implementation.

## Decision 1: ℂ residency — shadow register layer

Complex values live in a shadow register layer (`context.zfield`, a
dict of named complex registers) separate from the interpreter's real
scalars (psi_signal, phi_state, epsilon_drift, stabilized_value).

- Math-core operators (`phi_pi_e_math_core.py`) act **solely on
  registers**. They never read or write the real scalars directly.
- **Λ is the canonical reducer** from ℂ to real state: it provably
  returns real values (see math core), so it is the designated
  "observe a register into a real scalar" operation. No other operator
  crosses the boundary in that direction.
- Existing real-valued invariants (INVARIANTS.md) remain untouched by
  construction: nothing in the register layer can alter pinned
  semantics, because the two layers share no state.

Rejected alternatives: complexifying the existing scalars (surgery on
invariant-pinned state; fragile canonical fixture) and a full
complex-native AST rewrite (correct direction, v2-scale; presupposes
bridge experience we don't yet have — it is this design's promotion
path, not its competitor).

## Decision 2: Glyph collision — arity/operand-kind dispatch

The proofs' Φ/Ψ/ε are binary operators on ℂ×ℂ; the DSL's Φ/Ψ/ε are
unary real setters with invariant-pinned semantics. Same glyphs,
different operations. Resolution:

- **Unary / literal forms keep current DSL semantics, permanently.**
  `Φ 5.0`, `Ψ 1`, `ε 0.2`, and 3-literal `Φ a b c` behave exactly as
  pinned by the canonical fixture and invariants.
- **Binary register forms dispatch to the math core.** Two register
  operands → math-core operator → result register.
- **Mixed forms (register + literal) are FORBIDDEN** for math-core
  dispatch. A symbol followed by one register and one literal is a
  parse error, not a guess. (Safeguard: prevents underspecified
  accidental dispatch.)
- Dispatch is deterministic at parse time: registers are syntactically
  distinct from numeric literals, so operand shape fully determines
  which semantics apply. Precedent: Φ already dispatches on arity
  (1 literal = bind, 3 literals = init).

## Decision 3: ε convergence and loop exit

- **ε = 0.001 is canonical and is never scaled, silently or loudly.**
  Contraction per step is ~(1−ε); halving distance takes
  ln2/ε ≈ 693 iterations (errata E2).
- **Batching is the semantic definition** of loop-level convergence:
  one DSL convergence step = N internal math-core iterations on the
  register (N ≈ 1000; exact N fixed at implementation and pinned by
  test). The operator stays exact; only the observation granularity
  coarsens.
- **Analytic skip-ahead is permitted as optimization only:** from the
  pinned recurrence, n = ln(tol/d₀)/ln(1−ε) steps may be applied in
  closed form, provided observable behavior is identical to honest
  iteration (test-enforced equivalence).
- **ε-driven loop exit is opt-in via a new, explicitly marked loop
  form** that names the register whose convergence gates exit, a
  tolerance, and a **hard iteration cap** (termination guarantee even
  under pathological register states).
- **Plain `[..]` semantics are fixed forever**: exactly 10 iterations,
  shared context, `[Ψ 1]` → ψ = 10.0. The new loop form is additive
  syntax, never a reinterpretation.

## Implementation plan (feat/complex-bridge, in order)

1. `context.zfield` + register read/write plumbing; no syntax yet.
   Tests: registers exist, isolated from real scalars.
2. Register syntax + parser support (naming scheme settled here;
   constraints: visually distinct from literals and glyphs, cannot
   collide with existing token classes).
3. Binary-form dispatch for Φ/Ψ/ε (+ Λ as reducer, Δ, π). Tests:
   each binary form reproduces math-core values exactly (PDF fixtures
   through the DSL path); mixed forms rejected.
4. Convergence loop form with batching + cap. Tests: converges on
   known register pairs; cap fires on non-converging (π-driven)
   registers; plain `[..]` invariants untouched.
5. Skip-ahead optimization behind equivalence tests.

Each step lands only with its tests; full suite green throughout;
INVARIANTS.md checked at every step.

## Open items (settle during step 2, before syntax freezes)

These items must be resolved during Step 2 of the implementation plan.
Until then, they are considered provisional and must not be
implemented implicitly.

- Register naming syntax (proposal: `@name`; must not collide with
  existing allowed-character set — parser change required either way).
- How registers are initialized from DSL source (complex literal
  syntax vs. loading two reals; leaning: load form `@z 1.0 2.0`
  = 1+2i, avoiding a new literal class).
- Whether Λ-reduction writes to a chosen real scalar or to a
  dedicated observable slot (leaning: dedicated slot first —
  writing into pinned scalars touches the corridor and needs its own
  invariant review).
