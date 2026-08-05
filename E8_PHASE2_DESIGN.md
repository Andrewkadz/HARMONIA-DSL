# E8_PHASE2_DESIGN — 8D State Space and the Real E8 Lattice

Status: DRAFT — awaiting ratification (Andrew / Claude / Perplexity).
No implementation until ratified. Builds on SWARM_BRAIN_PHASE1
(merged prerequisite) and follows the same rules: tests or it doesn't
exist; the DSL stays load-bearing; no silent metaphysics.

## Motivation and honesty clause

Phase 1's state space is ℂ — 2 real dimensions, the minimum that
carries meaning. The (ΞΛΩΨ₃₃₃) document envisions E8 harmonic shells;
this design implements the REAL E8 lattice — a genuine, computable
mathematical object — rather than E8-as-naming. Every E8 claim below
is a known theorem of lattice theory, implementable and testable.
The (ΞΛΩΨ₃₃₃) document itself is classified as vision corpus
(roadmap tier of the precedence chain), like the proofs PDF's
categorical operators: mined for direction, never cited as spec.

## The mathematics (all standard, all testable)

- **E8 lattice**: points of ℝ⁸ that are either all-integer or
  all-half-integer coordinates with even coordinate sum
  (E8 = D8 ∪ (D8 + ½⁸)).
- **Shells**: concentric layers by squared norm (always an even
  integer). The first shell is the 240 roots at |x|² = 2 — this
  gives "harmonic shell" a precise, countable meaning.
- **Nearest-point quantization**: the Conway–Sloane decoder (decode
  in D8 and in D8+½⁸, keep the closer) finds the exact nearest
  lattice point in O(n log n) per vector. E8 is the optimal known
  8-dimensional quantizer, so snapping introduces provably minimal
  distortion; quantization error is bounded by the covering radius 1.

## Decision 1: 8D state via existing machinery (no interpreter changes)

Each agent's state becomes FOUR complex registers — `@s0 @s1 @s2 @s3`
(with goals `@g0..@g3`) — which is ℝ⁸ exactly. All evolution uses the
EXISTING ratified operations: `ε @sk @gk` per component, `Φ @sk @gk`
stabilization, `Λ @sk @gk` observation. The corridor, BRIDGE_DESIGN,
and all 289 tests are untouched by construction. The interpreter
does not learn about E8; the swarm layer composes it.

## Decision 2: e8_lattice.py — a pure math module (math-core rules)

New module `e8_lattice.py`, sibling to `phi_pi_e_math_core.py`, same
purity rules (no interpreter imports, no swarm imports):

- `is_lattice_point(v)` — membership test
- `nearest_point(v)` — Conway–Sloane decoder, exact
- `shell_index(p)` — |p|²/2 for lattice points
- `first_shell()` — the 240 roots, generated not hardcoded

Tests pin known mathematics: exactly 240 first-shell roots, all at
|x|²=2; decoder matches brute-force nearest-root search on vectors
near the first shell; quantization error ≤ covering radius 1 on
random vectors; D8/D8+½ membership cases.

## Decision 3: what E8 does for governance (load-bearing rule)

The G4 lesson applies: E8 must do decision work, not decoration.
Ratified uses (Phase 2a implements the first; 2b the second):

1. **Shell-indexed coherence**: an agent's 8D state quantizes to a
   lattice point; its SHELL INDEX is a discrete coherence class.
   Refusal and conflict decisions read shell membership instead of
   raw distances — decisions become discrete, enumerable, and robust
   to drift below the packing radius (noise inside a lattice cell
   cannot change any decision — a provable stability property no
   raw-threshold scheme has).
2. **Shell transitions as events**: crossing shells is a discrete,
   loggable governance event ("agent 3 dropped from shell 4 to
   shell 2") — the terrarium's next teaching layer.

Falsifiability (G4-style): a test must show a decision that raw
2D distance gets wrong (flips under sub-cell noise) that shell
membership gets right (invariant under the same noise).

## Decision 4: terrarium upgrade — honest 8D → 2D projection

The terrarium renders ℝ⁸ via selectable projections: coordinate-pair
views (s0 plane, s1 plane, …) and the Petrie projection of E8 — the
famous 30-fold-symmetric rendering, computed from the real projection
matrix, with the 240 first-shell roots drawn as the shell ring.
Agents appear at their projected 8D positions; shell index shown as
ring membership. No fictional geometry: every pixel derives from the
recorded 8D state.

## Implementation plan (in order, each step lands with tests)

1. `e8_lattice.py` + tests — pure math, no other changes.
2. Swarm layer: agents carry `@s0..@s3` / `@g0..@g3`; per-component
   ε/Φ/Λ via existing DSL; trace records 8D positions. Suite green.
3. Shell-indexed governance (replaces raw-distance refusal input) +
   the falsifiability test from Decision 3.
4. Terrarium projections (coordinate planes + Petrie + shell rings).

## Open items (leanings recorded; resolve before the step that uses them)

- State scaling: raw agent coordinates are O(1)-O(12); lattice cells
  have radius ~1, so a scale factor maps working range onto a few
  shells. Leaning: fixed global scale chosen so initial states span
  shells 1-4; pinned by test.
- Whether all four components evolve every round or one per round
  (cost: 4× DSL calls). Leaning: all four, budget is trivial.
- Petrie projection matrix source: computed from Coxeter element
  eigenvectors at build time, or a pinned constant matrix with a
  verification test. Leaning: pinned constants + test that verifies
  the defining property, so no runtime eigendecomposition.
