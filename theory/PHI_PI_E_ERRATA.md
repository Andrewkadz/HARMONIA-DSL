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
