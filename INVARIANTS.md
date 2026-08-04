# HARMONIA-DSL Non-Regressible Invariants

These are hard constraints. Any change — refactor, feature, optimization —
that breaks one of these is wrong by definition and must be reverted or
reworked, regardless of what else it improves.

## 1. Lexical integrity (`tests/test_lexical_semantic_path.py`)

Numeric literals (ints, floats, negatives) are first-class tokens.
Statement boundaries (newlines) survive cleaning. `//` and `#` comments
are stripped before filtering and can never leak phantom tokens.

## 2. Argument binding

`Φ x` binds phi_state; `Φ ψ φ ε` (three literals) seeds full initial
conditions; `Ψ x` and `ε x` accumulate into psi_signal / epsilon_drift.
Symbols without arguments keep their legacy derived defaults.

## 3. Temporal semantics (`tests/test_time_dynamics.py`, `tests/test_time_history_semantics.py`)

One persistent FieldContext per time-stepping run. History is recorded
from real state every step. Initial-conditions lines fire at t=0 only.
Derivative = backward difference; integral = windowed Riemann sum, dt=1.
A constant signal c over n steps integrates to c·n.

## 4. The canonical fixture (`TestCanonicalFixture`)

```
Φ 5.0
Ψ 3.0
ε 0.2
Σ
```

must always tokenize to `Φ 5.0 Ψ 3.0 ε 0.2 Σ`, produce state
φ=5.0 ψ=3.0 ε=0.2, and output (ψ+φ)(1−ε) = 6.4. This is the language's
hello world with semantics. If this breaks, Harmonia has stopped being
a language, whatever else still passes.

## 5. Entry point

`from phi_pi_e_interpreter import PhiPiEInterpreter` must resolve
(compatibility alias), and `Φπε.py` must boot.

Enforcement: `python3 -m pytest tests/` must pass 100% before any merge.
