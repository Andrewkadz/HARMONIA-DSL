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

## Resolved items (ratified for Step 2, 2026-08-03)

Formerly the "open items." All three are now fixed contract:

1. **Register naming: `@name`.** Any token of the form `@name` is a
   register identifier referring to `context.zfield["@name"]`. The
   `@` prefix is reserved for complex registers only. The tokenizer
   treats `@name` as a distinct operand kind ("register identifier"),
   which is the basis for operand-kind dispatch. Register access never
   touches pinned scalars.
2. **Register initialization: `@z 1.0 2.0`** (bare command form; no
   complex literal class). First token names the register, second is
   the real part, third the imaginary part: sets
   `zfield["@z"] = 1.0+2.0j`. **Exactly two numeric arguments** —
   fewer or more is a hard error, never silently coerced.
   Re-initialization overwrites cleanly. Unset registers still read
   as 0j (Step-1 plumbing). A future `load` verb, if introduced, must
   be a strict superset of this form.
3. **Λ-reduction target: dedicated observable slot
   `context.lambda_obs`** (real-valued, 0.0 default). `Λ @z @w`
   applies the math-core Λ to the two registers and writes the real
   result to `lambda_obs`. Λ NEVER writes to pinned scalars
   (psi_signal / phi_state / epsilon_drift / stabilized_value);
   mirroring `lambda_obs` into a scalar, if ever wanted, is a
   separate explicit future operation. `lambda_obs` participates in
   context persistence and forking like other context fields. The
   math-core Λ is binary, so the register form takes exactly two
   register operands.

Dispatch consequences, restated as syntax rules: unary/literal Φ/Ψ/ε
keep pinned DSL semantics; `Λ @z @w` is the first math-core register
form; mixed forms (`Λ @z 1.0`, `Φ @z 1.0`, …) are rejected outright;
binary register forms for Φ/Ψ/ε are NOT part of Step 2 and may only be
added (Step 3) after Step-2 tests are green.

## Step 3 ratification (2026-08-03): binary Φ/Ψ/ε register forms

- `Φ @z @w`, `Ψ @z @w`, `ε @z @w` dispatch to the math-core operators
  (harmonic_equilibrium, recursive_animation, incremental_insight) on
  the registers' complex values.
- **Result destination: the FIRST operand register** (in-place
  evolution). Rationale: ε's proven iteration is z_{n+1} = ε(z_n, w),
  so `[ε @z @w]` in a loop evolves `@z` toward `@w` exactly as
  Thm 4.3 describes; the same single rule applies to Φ and Ψ for
  uniformity. The second operand is never written.
- Register operations **pass the interpreter's current value through
  unchanged** (like modulators): their observable output lives in the
  register layer, and only Λ crosses into ℝ (via lambda_obs).
- Scalar isolation unchanged: register forms touch no pinned scalar.
- Prohibitions maintained: mixed forms and single-register forms are
  errors; π/Δ binary register forms and any further symbols require a
  new ratified entry here first.
