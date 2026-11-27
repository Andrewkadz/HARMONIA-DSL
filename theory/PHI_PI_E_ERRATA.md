# Φπε Proofs — Errata and Corrections

Referenced by the Work-in-Progress disclaimer in
`theory/RI1_LANGUAGE_Φπε_PROOFS_2026-08-03.pdf` (current version; earlier draft retained as RI1_LANGUAGE_Φπε_PROOFS.pdf). Precedence order per that
disclaimer: **implementation and tests are authoritative** where they
disagree with the PDF text. Authoritative sources:
`phi_pi_e_math_core.py` and `tests/test_math_core.py`.

## E1 — ε operator, Theorem 4.2 (Precision Threshold)

**PDF states:** |ε(z,w) − z| ≤ ε = 0.001 for all z, w.

**Status: incorrect as stated.** The PDF's own Example 5.1 computes an
increment of 0.002231 > 0.001 (|w−z| = 2.236). The bound derivable from
Definition 3.1 is:

    |ε(z,w) − z| = ε·d / (1 + ε·d) < min(ε·d, 1),  where d = |w − z|

The stated ≤ ε form holds only in the regime d ≤ 1/(1−ε) ≈ 1.001.

**Correction pinned by:** `TestEpsilonProperties::test_precision_threshold_true_bound`.
Discovered 2026-08-03 during math-core implementation.

## E2 — ε operator, Theorem 4.3 (Convergent Iteration), printed recurrence

**PDF states:** d_{n+1} = d_n² / (1 + ε·d_n).

**Status: recurrence does not follow from Definition 3.1.** The actual
distance recurrence is:

    d_{n+1} = d_n · (1 + ε·d_n − ε) / (1 + ε·d_n)

which is strictly decreasing to 0, so the theorem's **conclusion stands**
(z_n → w). But the rate is geometric, ~(1−ε) = 0.999 per step (≈700
iterations to halve a distance), not the fast quadratic collapse the
printed recurrence would imply. Anything built on ε-convergence timing
(e.g. loop-exit criteria) must budget for the slow rate or use a scaled ε.

**Correction pinned by:** `TestEpsilonProperties::test_convergent_iteration`
and `test_actual_recurrence_formula`.

## E3 — Φ operator, Theorem 4.1 (Non-Fusional Property) and Theorem 4.2 equality condition

**PDF states:** Theorem 4.1: "For `z, w ∈ ℂ` with `z ≠ w`, we have `Φ(z,w) ≠ z + w`." Theorem 4.2: "`|Φ(z,w)| ≤ |z + w|` with equality if and only if `z = w`."

**Status: requires hypothesis `z + w ≠ 0` (i.e. `w ≠ −z`).** For any nonzero
`z ∈ ℂ` and `w = −z`, we have `z ≠ w` (`|z − w| = 2|z| > 0`), yet:

    Φ(z, −z) = φ·(z + (−z)) / (φ + 2|z|) = 0 = z + w

For example, at `z = 1 + i`, `w = −1 − i`, `z ≠ w` holds while
`Φ(z, w) = 0 = z + w`. Correspondingly, Theorem 4.2's equality condition
`|Φ(z, w)| = |z + w|` holds if and only if `z = w` **or** `z + w = 0`.
`phi_pi_e_math_core.harmonic_equilibrium` implements Definition 3.1 directly
and requires no code change.

**Correction pinned by:** `TestPhiProperties::test_non_fusional_requires_nonzero_sum`.

## E4 — π operator, Theorem 4.2 (Spiral Coherence), printed bound

**PDF states:** "`|π(z,w)| ≤ π·|z + w|`".

**Status: printed statement is a typo for the bound derived in its own proof.**
When `z = −w ≠ 0`, `z + w = 0` so the printed right-hand side is `0`, whereas
`|π(z, −z, n)| = π·|z|·|1 − e^{iπ/n}| / 2 > 0` for every `n ≥ 1`. At
`z = 1, w = −1, n = 4`:

    π·|1 + (−1)| = 0  <  (11/7)·√(2 − √2) ≈ 1.202719  (|π(1, −1, 4)|)

(or `≈ 1.203178` when `π = 22/7` is also used in the phase exponent).
The PDF's own proof of Theorem 4.2 derives the true universal bound via the
triangle inequality and `1 + |z|/|w|`:

    |π(z, w)| ≤ π·(|z| + |w|) / (1 + |z|/|w|) = π·|w|   for all w ≠ 0

`TestPiProperties::test_spiral_coherence_bound` already tests `PI_RATIONAL * abs(w)`.

**Correction pinned by:** `TestPiProperties::test_spiral_coherence_bound` and
`TestPiProperties::test_printed_sum_bound_counterexample`.

## E5 — π operator, Theorem 4.3 growth claim & Example 5.1 phase constant

**PDF states:** Theorem 4.3 proof: "Since each `|π^k(z,w)|` grows as `π^k`
through spiral expansion, we have `D_n ~ n·log(π) → ∞` as `n → ∞`."
Example 5.1 (`z = 2 + 3i, w = 1 + i, n = 4`): "`e^{iπ/4} ≈ 0.7069 + 0.7073i`",
"`π(z,w) ≈ 1.7705 + 3.9085i`", "`|π(z,w)| ≈ 4.2908`".

**Status: proof scaling step contradicts Theorem 4.2; Example 5.1 uses `22/7` in the exponent.**

1. **Theorem 4.3 proof:** By Theorem 4.2's proof bound, `|π^k(z,w)| ≤ π·|w|`
   uniformly for every `k ≥ 1` (not exponential growth `π^k`). Starting from
   `z_0 = 2 + 3i, w = 1 + i`, all iterates stay strictly bounded by
   `(22/7)·√2 ≈ 4.444671` (`|π^{100}(z_0, w)| ≈ 4.444670`). The theorem's
   **conclusion** (`D_n → ∞` for `w ≠ 0` when iterates remain nonzero) still
   holds because `e^{iπ/k} → 1` drives `π^k(z,w) → (22/7)·w`, so
   `log(1 + |π^{k−1}(z,w)|/|w|) → log(1 + 22/7) = log(29/7) ≈ 1.421386` and
   `D_n` diverges linearly (`D_{100} ≈ 141.2435` vs `100·log(22/7) ≈ 114.5132`).
2. **Example 5.1 phase constant:** Evaluating `e^{i·(22/7)/4}` produces
   `0.706883 + 0.707330i` (`≈ 0.7069 + 0.7073i`), `π(z,w) ≈ 1.770472 + 3.908495i`
   (`≈ 1.7705 + 3.9085i`), and `|π(z,w)| ≈ 4.290793` (`≈ 4.2908`). Meanwhile,
   `phi_pi_e_math_core.transcendent_continuity` uses `cmath.exp(1j * math.pi / n)`
   (`0.707107 + 0.707107i`, giving `1.770868 + 3.908495i`, modulus `4.290957`,
   phase difference `≈ 3.161 × 10⁻⁴`). Per the specification precedence rule,
   `phi_pi_e_math_core.py` (`math.pi` in `cmath.exp`, `PI_RATIONAL = 22/7` as the
   outer multiplier) is authoritative.

**Correction pinned by:** `TestPiProperties::test_iterates_stay_bounded_by_pi_w`,
`TestPdfWorkedExamples::test_pi_spiral_phase_example`, and
`TestPdfWorkedExamples::test_pi_example_5_1_exponent_constant`.

## E6 — Λ operator, Theorem 4.1 (Structural Crystallization inequality)

**PDF states:** "For `z ≠ w` with `arg(z) ≠ arg(w)`, `Λ(z,w)` exhibits enhanced
real coupling `|Λ(z,w)| > |2·Re(z̄w)| / (|z|² + |w|²)`."

**Status: requires non-orthogonality (`Re(z̄w) ≠ 0`) and `|z|² + |w|² > 137/134`.**
1. For any orthogonal pair (`Re(z̄w) = 0`, e.g., `z = 1, w = i`, where `z ≠ w`
   and `arg(z) ≠ arg(w)`), both sides equal `0`, falsifying `0 > 0`.
2. Whenever `Re(z̄w) ≠ 0`, dividing out `|2·Re(z̄w)| > 0` reduces the inequality
   to `Λ / (Λ + r²) > 1 / r²` with `r² = |z|² + |w|²` and `Λ = 137/3`, which
   holds **if and only if**:

       |z|² + |w|² > Λ / (Λ − 1) = 137 / 134 ≈ 1.022388

   For example, `z = 0.5, w = 0.5·e^{iπ/6}` (`|z|² + |w|² = 0.5 ≤ 137/134`) gives
   `|Λ(z,w)| ≈ 0.428323 < 0.866025 ≈ |2·Re(z̄w)| / (|z|² + |w|²)`.

**Correction pinned by:** `TestLambdaProperties::test_crystallization_requires_nonorthogonal_and_norm_threshold`.

## E7 — Δ operator, Definition 3.1 simplification & Theorem 4.2 domain

**PDF states:** Definition 3.1: "`Δ(z,w) = Δ·(z·w)/(Δ + Λ|z − w|)`" with
`Δ = Λ²`, `Λ = 137/3`. Theorem 4.2: "For symbolic states in the consciousness
regime `|z|, |w| < √Λ`, the fusion exhibits amplification `|Δ(z,w)| > |z·w|/(1 + |z − w|)`."

**Status: `Λ` cancels cleanly in Definition 3.1, and Theorem 4.2 holds without the `√Λ` bound.**
1. Substituting `Δ = Λ²` and dividing numerator and denominator by `Λ = 137/3 > 0`:

       Δ(z,w) = (137/3)·z·w / (137/3 + |z − w|) = 137·z·w / (137 + 3·|z − w|)

2. Because `137 / (137 + 3·d) > 1 / (1 + d) ⇔ 134·d > 0` for `d = |z − w| > 0`,
   the amplification inequality `|Δ(z,w)| > |z·w| / (1 + |z − w|)` holds for
   **all** nonzero `z, w ∈ ℂ` with `z ≠ w`, not only `|z|, |w| < √Λ ≈ 6.757712`.
   For instance, at `z = 10, w = 20` (outside `√Λ`),
   `|Δ(10, 20)| ≈ 164.071856 > 18.181818 = |z·w| / (1 + |z − w|)`.

**Correction pinned by:** `TestDeltaProperties::test_simplified_exact_form` and
`TestDeltaProperties::test_fusion_amplification_universal`.

## Notes on scope (not errors)

- **Ω** is proven non-numerical by its own Theorem 3.2; the math core
  intentionally refuses evaluation (`CategoricalBoundaryError`). This is
  spec compliance, not a gap.
- Λ Thm 4.3 ("Λ = c^(cosθ/sinθ)", consciousness-light coupling) and
  similar physics-facing claims are not implemented or tested; they are
  outside the math core's scope and carry no code dependency.

## Process

New discrepancies found during implementation get an entry here (E3, E4,
…) plus a pinning test before any code relies on the corrected form.
