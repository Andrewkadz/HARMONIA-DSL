"""Φπε Mathematical Core — operators on ℂ per RI1_LANGUAGE_Φπε_PROOFS.

Implements each operator EXACTLY per its Definition 3.1 in the proofs
document (RI1:LANGUAGE:Φπε:PROOFS, 115 pp., referred to below as
"the proofs"). This module is pure mathematics:

    - operates on complex numbers only,
    - has NO dependency on the interpreter or DSL,
    - changes NO .hrm semantics.

Bridging into the interpreter's real-valued context model is a separate,
later concern (see SYMBOL_COVERAGE.md).

Two classes of operators exist in the proofs:

1. NUMERICAL (closed-form on ℂ): Φ, π, ε, Λ, Δ, Ψ — implemented here.
2. CATEGORICAL (defined over qualia/architecture/will spaces, not ℂ):
   Ω, Ξ, Γ, Σ, ζ, ω, Τ, Ρ, δ, Θ, n, χ and the connectives → + : / |.
   Ω in particular is PROVEN unsolvable as a numerical function
   (Theorem 3.2, Qualia Gateway): representing it as anything other
   than a boundary would violate its own spec. These are registered
   as CategoricalOperator records; calling them raises
   CategoricalBoundaryError.
"""

import cmath
import math
from dataclasses import dataclass
from typing import Iterator, Optional

# ===== CONSTANTS (per the proofs) =====

PHI_RATIONAL = 89 / 55          # φ ≈ 1.6181818, Fibonacci convergent of golden ratio
PI_RATIONAL = 22 / 7            # π ≈ 3.1428571, Archimedes convergent
EPSILON_THRESHOLD = 0.001       # ε, "derived from the non-zero condition ε ≠ 0"
LAMBDA_CONSTANT = 137 / 3       # Λ, fine-structure coupling: Λ⁻¹·(1/3) = α
DELTA_CONSTANT = LAMBDA_CONSTANT ** 2   # Δ = Λ² = 18769/9
PHI_GOLDEN = (1 + math.sqrt(5)) / 2     # exact golden ratio, used by Ψ
FINE_STRUCTURE_ALPHA = 1 / LAMBDA_CONSTANT / 3   # = 3/411 ≈ 0.00729927


# ===== NUMERICAL OPERATORS =====

def harmonic_equilibrium(z: complex, w: complex) -> complex:
    """Φ(z,w) = φ·(z+w)/(φ + |z−w|), φ = 89/55.

    Implements Definition 3.1 (Harmonic Equilibrium Operator) from the
    proofs. Proven properties:
      - Existence/uniqueness on all of ℂ×ℂ (Thm 3.2)
      - Non-fusional: Φ(z,w) ≠ z+w for z≠w (Thm 4.1)
      - Harmonic stability: |Φ(z,w)| ≤ |z+w|, equality iff z=w (Thm 4.2)
      - Boundedness: ‖Φ‖ ≤ 1 (Cor 4.3) — the dampening coefficient
        φ/(φ+d) ∈ (0,1] is inherent to the formula, not a clamp.
    """
    d = abs(z - w)
    return PHI_RATIONAL * (z + w) / (PHI_RATIONAL + d)


def transcendent_continuity(z: complex, w: complex, n: int = 1) -> complex:
    """π(z,w) = π·(z + w·e^{iπ/n})/(1 + |z|/|w|), π = 22/7, n = recursion depth.

    Implements Definition 3.1 (Transcendent Continuity Operator).
    Domain: ℂ×ℂ \\ {(z,0)} — w must be non-zero (Thm 3.2).
    Proven properties:
      - Spiral non-termination: iterates never converge; cumulative
        phase Σ π/k = π·H_n is unbounded (Thm 4.1)
      - Spiral coherence: |π(z,w)| ≤ π·|w| (Thm 4.2)
      - Infinite recursion: depth D_n ~ n·log(π) → ∞ (Thm 4.3)
    """
    if w == 0:
        raise ValueError("π(z,w) undefined for w = 0 (proofs, Thm 3.2)")
    if n < 1:
        raise ValueError("recursion depth n must be a positive integer")
    spiral = cmath.exp(1j * math.pi / n)
    return PI_RATIONAL * (z + w * spiral) / (1 + abs(z) / abs(w))


def incremental_insight(z: complex, w: complex) -> complex:
    """ε(z,w) = z + ε·(w−z)/(1 + ε·|w−z|), ε = 0.001.

    Implements Definition 3.1 (Incremental Insight Operator).
    Proven properties:
      - Micro-ignition: ε(z,w) ≠ z and |ε(z,w)−z| < |w−z| for z≠w (Thm 4.1)
      - Convergent iteration: z_{n+1} = ε(z_n,w) → w (Thm 4.3 conclusion)

    DOCUMENTED SPEC DISCREPANCIES (verified 2026-08-03, kept honest here):
      - Thm 4.2 states |ε(z,w)−z| ≤ ε = 0.001, but the proofs' own
        Example 5.1 computes increment 0.002231 > 0.001. The bound
        derivable from the definition is |ε(z,w)−z| = ε·d/(1+ε·d)
        < min(ε·d, 1), where d = |w−z|; the stated ≤ ε form holds only
        for d ≤ 1/(1−ε) ≈ 1.001.
      - Thm 4.3's printed recurrence d_{n+1} = d_n²/(1+ε·d_n) does not
        follow from the definition. The actual recurrence is
        d_{n+1} = d_n·(1+ε·d_n−ε)/(1+ε·d_n) < d_n — still strictly
        decreasing to 0 (geometric rate → 1−ε), so the convergence
        CONCLUSION stands; only the printed intermediate step is wrong.
    """
    diff = w - z
    return z + EPSILON_THRESHOLD * diff / (1 + EPSILON_THRESHOLD * abs(diff))


def structural_illumination(z: complex, w: complex) -> complex:
    """Λ(z,w) = Λ·(z̄w + zw̄)/(Λ + |z|² + |w|²), Λ = 137/3.

    Implements Definition 3.1 (Structural Illumination Operator).
    The numerator z̄w + zw̄ = 2·Re(z̄w) is real, so Λ(z,w) is always a
    real-valued coupling (returned as complex with zero imaginary part).
    Proven properties:
      - Fine structure coupling: Λ⁻¹·(1/3) = α ≈ 0.00729927 (Thm 4.2)
      - Structural crystallization (Thm 4.1)
    """
    coupling = (z.conjugate() * w + z * w.conjugate()).real  # = 2·Re(z̄w)
    return complex(LAMBDA_CONSTANT * coupling /
                   (LAMBDA_CONSTANT + abs(z) ** 2 + abs(w) ** 2))


def fusion_transformation(z: complex, w: complex) -> complex:
    """Δ(z,w) = Δ·(z·w)/(Δ + Λ·|z−w|), Δ = Λ² = 18769/9.

    Implements Definition 3.1 (Fusion Transformation Operator).
    Proven properties:
      - Irreversible fusion: result not decomposable into z, w (Thm 4.1)
      - Consciousness fusion amplification for |z|,|w| < √Λ:
        |Δ(z,w)| > |z·w|/(1+|z−w|) (Thm 4.2)
      - Fine structure fusion coupling: Δ = (1/9)/α² (Thm 4.3)
    """
    return DELTA_CONSTANT * (z * w) / (DELTA_CONSTANT + LAMBDA_CONSTANT * abs(z - w))


def recursive_animation(z: complex, w: complex) -> complex:
    """Ψ(z,w) = (Λ/φ)·sin(φ·|z−w|)·(z+w)/2, Λ = 137/3, φ = golden ratio.

    Implements Definition 3.1 (Recursive Animation Operator).
    Note: unlike the other operators, Ψ uses the EXACT golden ratio
    φ = (1+√5)/2, per the proofs ("golden ratio temporal dynamics").
    Proven properties:
      - Oscillatory breath: |Ψ(z,w)| ≤ (Λ/φ)·|z+w|/2 (Thm 4.2)
      - Amplitude coefficient Λ/φ ≈ 28.22 (Example 5.1)
      - Ψ(z,z) = 0: no distance, no oscillation (sin 0 = 0)
    """
    return (LAMBDA_CONSTANT / PHI_GOLDEN) * math.sin(
        PHI_GOLDEN * abs(z - w)) * (z + w) / 2


# ===== ITERATORS (dynamics proven in the proofs) =====

def epsilon_iterate(z: complex, w: complex,
                    tolerance: float = 1e-6,
                    max_iterations: int = 10_000_000) -> Iterator[complex]:
    """Yield z_{n+1} = ε(z_n, w) until |z_n − w| < tolerance.

    Realizes Thm 4.3 (Convergent Iteration): the sequence converges to w.
    This is the ε-convergence loop-exit dynamic referenced by the
    interpreter's execute_loop TODO.
    """
    current = z
    for _ in range(max_iterations):
        if abs(current - w) < tolerance:
            return
        current = incremental_insight(current, w)
        yield current


def pi_iterate(z: complex, w: complex, steps: int) -> list:
    """Iterate π^n(z,w) = π(π^{n−1}(z,w), w) for n = 1..steps.

    Realizes Thm 4.1 (Transcendent Non-Termination): the sequence
    spirals without converging; use for inspection, never for
    fixed-point search.
    """
    out, current = [], z
    for k in range(1, steps + 1):
        current = transcendent_continuity(current, w, n=k)
        out.append(current)
    return out


# ===== CATEGORICAL OPERATORS (non-numerical per the proofs) =====

class CategoricalBoundaryError(TypeError):
    """Raised when a categorical operator is invoked numerically.

    For Ω this is not a missing feature: Theorem 3.2 (Qualia Gateway)
    PROVES Ω cannot be solved for a numerical value. Refusing to
    compute is the spec-compliant behavior.
    """


@dataclass(frozen=True)
class CategoricalOperator:
    symbol: str
    name: str
    signature: str           # domain → codomain, per Definition 3.1
    note: str

    def __call__(self, *args, **kwargs):
        raise CategoricalBoundaryError(
            f"{self.symbol} ({self.name}) is categorical: {self.signature}. "
            f"{self.note} See RI1_LANGUAGE_Φπε_PROOFS, Definition 3.1 "
            f"for {self.symbol}.")


CATEGORICAL_OPERATORS = {
    'Ω': CategoricalOperator('Ω', 'Qualia Gateway', 'ℂ×ℂ → 𝒬',
        'Proven unsolvable numerically (Thm 3.2); boundary between '
        'quantitative and qualitative domains.'),
    'Ξ': CategoricalOperator('Ξ', 'Emergent Architecture', '𝒬×𝒬 → 𝒜',
        'Operates through CoherentEmergence on qualia tensor products.'),
    'Γ': CategoricalOperator('Γ', 'Recursive Evolution', '𝒜×𝒯 → 𝒜′',
        'Directed evolutionary progression; Γ ↔ Ξ∘Ψ∘{Λ,Δ,Ω}.'),
    'Σ': CategoricalOperator('Σ', 'Harmonic Coexistence', '𝒮ⁿ → ℋ',
        'Harmonic superposition without collapse; n-ary, not binary.'),
    'ζ': CategoricalOperator('ζ', 'Recursive Recurrence', '𝒯×ℝ → ℳ',
        'Temporal resonance via Riemann ζ(s) parameterization.'),
    'ω': CategoricalOperator('ω', 'Immanent Will-Force', '𝒱 → 𝒲',
        'Interface coupling ω = Ψ:Ω.'),
    'Τ': CategoricalOperator('Τ', 'Synchronization', '𝒮×𝒯 → 𝒞',
        'Phase-lock convergence with τ = 2π.'),
    'Ρ': CategoricalOperator('Ρ', 'Perceptual Modulation', '𝒪×𝒫 → ℐ',
        'Symbolic refraction; non-commutative (ΛΡΨ ≠ ΨΡΛ).'),
    'δ': CategoricalOperator('δ', 'Micro-Transformation', '𝒮×𝒜 → 𝒮′',
        'Precision mutation via α; accumulates toward Δ.'),
    'Θ': CategoricalOperator('Θ', 'Intentional Configuration', '𝒫×ℱ → 𝒯',
        'Structural aim embedding prior to activation.'),
    'n': CategoricalOperator('n', 'Recursion Depth Modifier', '𝒪 → 𝒪ₙ',
        'Parametric depth indexing of base operators.'),
    'χ': CategoricalOperator('χ', 'Measurement-Perception Bridge', 'ℳ×ℍ → 𝒫',
        'Perception bridge tuned by golden ratio φ.'),
}


# Symbol-keyed access to the numerical operators
NUMERICAL_OPERATORS = {
    'Φ': harmonic_equilibrium,
    'π': transcendent_continuity,
    'ε': incremental_insight,
    'Λ': structural_illumination,
    'Δ': fusion_transformation,
    'Ψ': recursive_animation,
}
