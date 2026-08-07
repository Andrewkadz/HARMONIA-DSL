# LOGIC_NODES_DESIGN — Structural Operators and the Scalar Field

Status: DRAFT for ratification. Extends BRIDGE_DESIGN (complex
registers) with a second operator tier and a scalar attribute layer.
Same rules: tests or it doesn't exist; each node must have a job and
must break something when removed.

## Honesty clause (read first)

The Φπε proofs define Σ, ζ, Ξ, Γ, Τ over non-numeric spaces (state
space, memory resonance space, architecture space). They specify
**what each operator is for**, not how to compute it. What follows are
**computational realizations chosen by us** to fulfil those roles.
They are not derivations from the proofs and must never be presented
as such. Where a realization succeeds, that is evidence about the
realization, not confirmation of the theory.

Ω remains unimplemented and unimplementable by its own Theorem 3.2.

## Tier 2: structural operators

Existing tier (BRIDGE_DESIGN): numeric operators on ℂ registers —
`Φ Ψ ε Λ` (and `Δ π` in the math core). Unchanged, invariants intact.

New tier: operators over *structures* rather than complex scalars.
They read and write the same `@name` registers plus new structural
slots on the context.

### Σ — superposition (n-ary, non-collapsing)

    Σ @a @b [@c ...]        -> superposition slot
    Σ! @s                   -> collapse to the strongest member

Spec role: "stable plurality of contradictory states preserved
without forced resolution."
Realization: `context.superpositions[name] = [complex, ...]`, an
ordered multiset that is NOT reduced on write. `Σ!` collapses by
maximum |z| (deterministic; ties by insertion order).
**Job:** an agent holds two viable plans without committing early.
**Falsifier:** with Σ removed, an agent forced to commit at first
evaluation performs worse on a scenario where the first option is
later invalidated.

### ζ — recurrence detection

    ζ @self                 -> writes recurrence depth to scalar `#zeta`

Spec role: "recognition of structural patterns across temporal
intervals."
Realization: each context keeps a bounded history of register
signatures (rounded complex values). ζ scans backwards for the most
recent match of the current signature and reports the distance in
steps (0 = no recurrence found).
**Job:** a better refusal criterion — *"I have been in this exact
configuration before"* — strictly sharper than counting flat rounds,
because it detects cycles, not just stagnation.
**Falsifier:** a scenario where an agent loops through a repeating
3-state cycle: flat-round counting never fires (state keeps changing),
ζ-based refusal does.

### Ξ — composition

    Ξ @a @b                 -> writes a composite to @a

Spec role: emergent architecture from qualia tensor interaction.
Realization: a composite register whose value is the Φ-stabilized
combination of its parts, *plus* a recorded membership list
(`context.composites[name] = [members]`) so the structure is
inspectable and reversible in principle.
**Job:** coalition formation — two agents form a unit that acts as
one.
**Falsifier:** a task requiring joint resource capacity that neither
agent can satisfy alone; without Ξ it is never completed.

### Γ — evolution with identity preservation

    Γ @self                 -> advances generation, retains lineage

Spec role: "advances capability without identity loss."
Realization: increments `context.generation[name]` and appends the
prior value to a lineage list. The invariant — testable — is that
lineage is never lost and generation is monotone.
**Job:** versioned agent state where "is this the same agent?" has a
checkable answer.
**Falsifier:** an audit test asserting lineage continuity across
transitions; without Γ, identity across change is unrecoverable.

### Τ — phase lock

    Τ @self @ref            -> aligns phase, reports readiness in `#tau`

Spec role: convergence readiness through phase alignment (τ = 2π).
Realization: sets the agent's phase to the reference's modulo 2π and
writes an alignment score (1 − normalized phase distance) to a scalar.
**Job:** synchronized action — agents act together on the round where
alignment crosses a threshold.
**Falsifier:** a task requiring simultaneous action by ≥3 agents;
without Τ they never coincide.

## The scalar field (root attributes)

Motivation: `@name` holds one complex value. Systems need named
*attributes* at root — budgets, thresholds, counters, flags, readouts
— without inventing a register per number.

    #name value             set a scalar attribute
    #name                   (bare) read it into the current value

- Stored in `context.scalars: Dict[str, float]`, sibling to `zfield`.
- Distinct token class: `#` prefix, same lexing discipline as `@`.
- Structural operators write their readouts here (`#zeta`, `#tau`).
- **Isolation rule (as with zfield):** scalars never alias the pinned
  ΦπεNode state (psi_signal / phi_state / epsilon_drift /
  stabilized_value). Nothing in this tier can touch the corridor.
- Scalars are shared across forks, like registers.

## Invariants (non-negotiable, per INVARIANTS.md)

Everything above is ADDITIVE. The canonical fixture
(`Φ 5.0 / Ψ 3.0 / ε 0.2 / Σ` → 6.4) must be unchanged — note this
means **bare `Σ` with no register operands keeps its existing reducer
semantics**; the superposition form requires register operands and is
distinguished by operand kind, exactly as BRIDGE_DESIGN Decision 2
prescribes. Same for the other reused glyphs.

## Implementation order

1. Scalar field `#name` + tests (no operators yet).
2. ζ and Τ (both write scalars; smallest surface).
3. Σ superposition + `Σ!` collapse.
4. Ξ composition, Γ lineage.
5. One swarm scenario per node exercising its Job, plus its Falsifier
   test.

Branch: `feat/logic-nodes`, stacked on current main.

---

## ROUND 2 (2026-08-04): register forms, coordination nodes, composition

**Δ and Π register forms.** `Δ @a @b` and `Π @a @b` dispatch to the
math core's existing tested functions — no new mathematics, just the
wiring. Π reads its recursion depth from `#depth` (default 1) and
holds position when the reference register is 0, since π is undefined
there (proofs Thm 3.2).

**Coordination nodes** (computational realizations, honesty clause
above applies):

- `λ @a @b` entangles registers into a symmetric group (transitive);
  `λ! @a` resolves the group to their shared mean. Job: shared state
  between cooperating agents.
- `Υ @a @b [...]` consensus merge — writes the mean to every operand
  and reports dispersion to `#upsilon` (0 = perfect agreement,
  idempotent). Job: multi-agent agreement WITH a measurable
  disagreement signal.
- `Κ @a [@b]` probe — reports magnitude, or distance with two
  operands, to `#kappa`, and mutates nothing. Job: inspect a peer
  before negotiating.

**Composition tier.** This is the structural change: programs become
expressions rather than flat statement sequences.

- `→ @dst` / `→ #dst` pipes the current value into a register or
  scalar, so operator outputs can be named and reused:
  `Λ @a @b → #obs`.
- `+ @a @b` parallel coexistence — both present, neither transformed,
  commutative (spec: independence-preserving, non-transformative).
- Bare `→` with no valid destination keeps its legacy modulator
  behaviour, so nothing in the corridor moves.

**Count:** 16 symbols now carry real semantics (6 at the start of the
day). Remaining ceremonial: Ε Θ Ρ Ω ω δ η χ n Β and the connectives
`: / |`. Ω stays unimplemented by its own Theorem 3.2.

## ROUND 3: Θ (intention, depth-indexed) and Ρ (perception)

**Θ @self @aim — structural aim declared before acting.**
Spec role: "structural aim embedding prior to activation," angular
directional dynamics, indexed by depth (Θₙ). Realization: records
(position at declaration, aim direction) under (register, depth),
depth read from `#depth`. **Θ configures; it never acts** — the
register is untouched. `Θ? @self` then audits: cosine alignment
between realized displacement and declared direction, written to
`#theta_align` (1 = moved as intended, 0 = orthogonal, −1 = opposed).
Deeper intentions govern — the innermost declared aim is audited.
**Job:** pre-commitment. Declared intent becomes auditable against
realized behaviour, which is a governance primitive nothing else in
the language provides.
**Falsifier:** an agent drifting from its declared aim is undetectable
without Θ; with it, misalignment is a number.

**Ρ @a @lens — refraction through a perspective.**
Spec role: "identical patterns generate different meanings based on
refractive properties," explicitly NON-COMMUTATIVE (ΛΡΨ ≠ ΨΡΛ).
Realization: `Ρ(a,l) = a·e^{i·arg(l)} / (1 + |l − a|)` — the subject
is rotated by the lens's phase and attenuated by their separation.
Asymmetric by construction; the lens is never mutated.
**Job:** order-dependent observation — the same state read through
different lenses, or at a different point in a sequence, yields a
different value.
**Falsifier (tested):** Ρ(a,l) ≠ Ρ(l,a), and `Ρ then Φ` ≠ `Φ then Ρ`.
This is the spec's own defining property, and it holds.

**Count: 19 symbol forms with real semantics** (6 at the start of the
day). Remaining ceremonial: Ε ω δ η χ n Β Ω and the connectives
`: / |`. Ω stays unimplemented by its own Theorem 3.2.

## ROUND 4: connectives — `< > ( ) / : ^`

The pieces that turn a statement sequence into a structured program.

- **`> A B` / `< A B` — guard.** Compares scalars, register
  magnitudes, or literals; writes 1/0 to `#cmp`; and if the test
  FAILS, abandons the rest of the line. This is Harmonia's
  conditional execution: `> #drift 0.5 Φ @a @b` stabilizes only when
  drift is high. Gating is line-scoped — the next line always runs.
- **`( ... )` — grouping.** Evaluates a sub-expression whose result
  becomes the current value, so operator output can be piped:
  `( Λ @a @b ) → #obs`. Nestable.
- **`^` / `^ n` — depth escalation.** Nests one level, or sets the
  level outright. Feeds `#depth`, which Θₙ and Π both read, so
  intentions and spiral recursion share one notion of depth.
- **`: @a @b` — relational interface.** Records a contact pair and
  reports their tension to `#tension`, WITHOUT merging — the spec's
  "active relational recursion without immediate merger." Both
  registers are left untouched.
- **`/ @a` — disruption.** Perturbs a register by `#disrupt`
  (default 0.1) as a rotation rather than a scaling, so it changes
  direction, not just magnitude.

**Count: 24 symbol forms with real semantics** (6 at the start of the
day). Remaining ceremonial: Ε ω δ η χ n Β and `|`. Ω stays
unimplemented by its own Theorem 3.2.
