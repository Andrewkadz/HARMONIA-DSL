# Symbol Coverage Inventory

Generated from live handler source (`phi_pi_e_interpreter.py`) and test-suite
cross-reference on `main` (covering `BRIDGE_DESIGN` Steps 1–3, `fix/loop-context`,
and `LOGIC_NODES_DESIGN`). "Pinned scalars" means the `ΦπεNode` state that
carries corridor meaning (`psi_signal`, `phi_state`, `epsilon_drift`,
`stabilized_value`); `phase`/`charge`/`tension` are internal field mechanics.

## Status codes

- **BOUND** — accepts numeric argument(s) that bind into pinned `ΦπεNode` scalar state
- **SEMANTIC** — no numeric argument, reads/writes pinned `ΦπεNode` scalar fields
- **TIER-1 @REGISTER** — binary `@z @w` dispatch into `phi_pi_e_math_core.py` on `context.zfield` (or `context.lambda_obs` for `Λ`), isolated from pinned scalars
- **TIER-2 STRUCTURAL** — `@register` structural realization (`LOGIC_NODES_DESIGN`) on `context.superpositions` / `history` / `composites` / `lineage` / `scalars` (`#name`), isolated from pinned scalars
- **CEREMONIAL** — executes, mutates only `phase`/`charge`/`tension`/`fork`, ignores numeric args (or is a categorical boundary stub such as `Ω`)

## Symbols

| Symbol | Handler / Dispatch | Tier-1 (literal / bare) | Tier-1 `@register` | Tier-2 structural (`@register`) | Semantic fields touched | Tested | Status |
|---|---|---|---|---|---|---|---|
| Φ | `stabilize` / math core | yes (1: `φ`, 3: `ψ φ ε` init) | `Φ @z @w` → `harmonic_equilibrium` (`@z`) | — | `phi_state` (+ `psi_signal`, `epsilon_drift`); `zfield` | yes | BOUND + TIER-1 @REGISTER |
| Ψ | `pulse` / math core | yes (additive `ψ`) | `Ψ @z @w` → `recursive_animation` (`@z`) | — | `psi_signal`; `zfield` | yes | BOUND + TIER-1 @REGISTER |
| ε | `micro_ignite` / math core | yes (additive `ε`) | `ε @z @w` → `incremental_insight` (`@z`) | — | `epsilon_drift`; `zfield` | yes | BOUND + TIER-1 @REGISTER |
| Λ | `illuminate` / math core | bare = CEREMONIAL pass-through | `Λ @z @w` → `structural_illumination` (`lambda_obs`) | — | `context.lambda_obs` (ℂ → ℝ) | yes | TIER-1 @REGISTER (bare CEREMONIAL) |
| Σ | `coexist` / `_sigma_superpose` | bare = SEMANTIC `(ψ+φ)(1−ε)` | — | `Σ @a @b [@c ...]` → superposition | `stabilized_value`; `superpositions`, `#sigma` | yes | SEMANTIC + TIER-2 STRUCTURAL |
| Σ! | `_sigma_collapse` | — (no bare form) | — | `Σ! @a` → collapse to max `\|z\|` | `zfield`, `superpositions` | yes | TIER-2 STRUCTURAL |
| ζ | `recurrence` / `_zeta_recurrence` | bare = CEREMONIAL | — | `ζ @a` → cycle distance | `history`, `#zeta` | yes | TIER-2 STRUCTURAL (bare CEREMONIAL) |
| Ξ | `emerge` / `_xi_compose` | bare = CEREMONIAL | — | `Ξ @a @b` → Φ-stabilized coalition | `zfield`, `composites`, `#xi` | yes | TIER-2 STRUCTURAL (bare CEREMONIAL) |
| Γ | `grow` / `_gamma_evolve` | bare = CEREMONIAL | — | `Γ @a` → generation + lineage | `zfield`, `lineage`, `#gamma` | yes | TIER-2 STRUCTURAL (bare CEREMONIAL) |
| Τ | `synchronize` / `_tau_phaselock` | bare = CEREMONIAL | — | `Τ @a @ref` → phase alignment | `zfield`, `#tau` | yes | TIER-2 STRUCTURAL (bare CEREMONIAL) |
| Κ | `probe` | no arg | — | — | `psi_signal`, `probe_count` | yes | SEMANTIC |
| Υ | `consensus_merge` | no arg | — | — | `phi_state`, `epsilon_drift` | yes | SEMANTIC |
| Β | `reflection_echo` | no arg | — | — | `depth` | yes | SEMANTIC |
| Ε | `ignite` | no | — | — | — (fork/phase/charge only) | yes | CEREMONIAL |
| Π | `transcend` | no | pending Step 4 (`π` in math core) | — | — (fork/phase/depth only) | no | CEREMONIAL (bare; Step 4 pending) |
| Δ | `fuse` | no | pending Step 4 (`Δ` in math core) | — | — (tension/phase only) | no | CEREMONIAL (bare; Step 4 pending) |
| δ | `micro_transform` | no | — | — | — (tension/phase only) | no | CEREMONIAL |
| λ | `entangle` | no | — | — | — (tension/phase only) | no | CEREMONIAL |
| Ω | `close` | no | refuses by design (Thm 3.2) | refuses by design | — (resets mechanics; math core raises `CategoricalBoundaryError`) | yes | CATEGORICAL / CEREMONIAL |
| ω | `will_force` | no | — | — | — (fork/phase/charge only) | no | CEREMONIAL |
| Ρ | `perceive` | no | — | — | — (phase only) | no | CEREMONIAL |
| Θ | `intend` | no | — | — | — (charge only) | no | CEREMONIAL |
| η / n | `index` | no | — | — | — (no mutation) | no | CEREMONIAL |
| χ | `measure` | no | — | — | — (phase only) | no | CEREMONIAL |

## Operators & Syntax Forms

| Form / Op | Handler | Semantic / Register / Scalar fields | Tested | Status |
|---|---|---|---|---|
| `@name RE IM` | register init | writes `context.zfield[@name] = RE + IMj` (strictly 2 numeric args) | yes | TIER-1 @REGISTER (`BRIDGE_DESIGN` Step 2) |
| `#name val` / `#name` | scalar attribute | sets / reads `context.scalars[#name]` (isolated from `ΦπεNode`) | yes | TIER-2 SCALAR (`LOGIC_NODES_DESIGN`) |
| `=` | `stabilize` | `phi_state` (alias of `Φ`) | yes | BOUND |
| `[]` | `execute_loop` | re-executes body 10× on **shared persistent `FieldContext`** (`[Ψ 1]` → `ψ = 10.0`; `[ε @z @w]` → 10 ε-steps) | yes | SEMANTIC (fixed in `fix/loop-context`) |
| `→` | `flow` | — (fork/phase/charge only) | yes | CEREMONIAL |
| `+` | `simultaneity` | — (pass-through) | no | CEREMONIAL |
| `:` | `interact` | — (tension/phase only) | no | CEREMONIAL |
| `/` | `disrupt` | — (tension/phase/charge only) | no | CEREMONIAL |
| `\|` | `orthogonal` | — (tension/phase only) | no | CEREMONIAL |

## Summary

- **3** symbols are Tier-1 **BOUND** (`Φ`, `Ψ`, `ε`) plus `=` alias (`Φ`).
- **4** symbols are Tier-1 **SEMANTIC** without arguments (`Σ`, `Κ`, `Υ`, `Β`).
- **4** symbols have **TIER-1 @REGISTER** binary dispatch (`Φ`, `Ψ`, `ε` in-place on `zfield`; `Λ` reducing ℂ → ℝ into `lambda_obs`).
- **6** symbols/tokens have **TIER-2 STRUCTURAL** `@register` dispatch (`Σ`, `Σ!`, `ζ`, `Ξ`, `Γ`, `Τ`), isolated from pinned `ΦπεNode` scalars.
- **11** symbols (`Ε`, `Π`, `Δ`, `δ`, `λ`, `Ω`, `ω`, `Ρ`, `Θ`, `η`/`n`, `χ`) + **5** connectives (`→`, `+`, `:`, `/`, `|`) remain **CEREMONIAL** in `phi_pi_e_interpreter.py` on `main`.
  - **Note on `Ω`:** `Ω` refusing numerical and `@register` evaluation is deliberate Theorem 3.2 compliance (`CategoricalBoundaryError`), not missing work.
  - **Note on `Π` / `Δ` and convergence loops:** Closed-form `π` and `Δ` exist in `phi_pi_e_math_core.py`; their `@register` dispatch and opt-in ε-convergence loop syntax are governed by `BRIDGE_DESIGN.md` Step 4.
  - **Note on `[]`:** The historical context-reset loop bug was fixed in `fix/loop-context` (`tests/test_loop_context.py`).

## Canonical fixture (must never break)

```
Φ 5.0    # equilibrium      tokens: Φ 5.0 Ψ 3.0 ε 0.2 Σ
Ψ 3.0    # pulse            state:  φ=5.0 ψ=3.0 ε=0.2
ε 0.2    # drift            output: (3+5)·(1−0.2) = 6.4
Σ        # stabilize
```

Enforced by `tests/test_lexical_semantic_path.py::TestCanonicalFixture`.
