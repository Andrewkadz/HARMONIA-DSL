# HARMONIA-DSL v3.0: Nonlinear Dynamics User Guide

**Author**: Manus AI
**Date**: January 1, 2026
**Version**: 3.0

---

## 1. Welcome to v3.0: Embracing Nonlinearity

HARMONIA-DSL v3.0 is a major leap forward, introducing **nonlinear dynamics** into the language. This allows you to model complex, real-world systems that were impossible in previous versions.

This guide will walk you through the new operators, what they do, and how to use them to create sophisticated, emergent behavior.

---

## 2. The Three Nonlinear Operators

v3.0 introduces three new operators that are the building blocks of nonlinearity.

### 2.1. `exp-` (Exponential Decay)

**Purpose**: To model natural dampening, forgetting, and decay to a baseline.

**Syntax**: `exp- <variable> <decay_rate>`

**What it does**: Applies the formula `variable_new = variable_old * e^(-decay_rate * dt)` to the specified variable (`psi`, `phi`, or `epsilon`).

**Use Cases**:
-   Modeling memory decay over time.
-   Simulating the cooling of an object.
-   Creating systems that naturally return to equilibrium.

### 2.2. `tanh` (Hyperbolic Tangent)

**Purpose**: To model saturation, diminishing returns, and soft thresholds.

**Syntax**: `tanh <variable> <scale_factor>`

**What it does**: Applies the formula `variable_new = scale_factor * tanh(variable_old)`. This maps any input to a value between `-scale_factor` and `+scale_factor`.

**Use Cases**:
-   Modeling neural activation functions (neurons have a max firing rate).
-   Preventing runaway positive feedback loops.
-   Simulating systems with natural limits (e.g., a market with a limited number of buyers).

### 2.3. `^2` (Resonance)

**Purpose**: To model amplified interactions, feedback loops, and explosive growth.

**Syntax**: `^2 <variable>`

**What it does**: Applies the formula `variable_new = variable_old ^ 2` (while preserving the sign).

**Use Cases**:
-   Modeling viral spread on social media.
-   Simulating epidemic growth.
-   Creating positive feedback loops that lead to emergent behavior.

**WARNING**: This operator can lead to explosive growth. It should almost always be paired with a `tanh` operator to create bounded, stable systems.

---

## 3. How to Use the New Operators

The new operators are used within a HARMONIA-DSL program just like the existing operators. They are designed to be used within a time-stepping simulation (v2.0).

Here is a simple example of how to create a stable oscillator:

```python
# Python code demonstrating the use of the operators

from nonlinear_operators import NonlinearOperators
from dataclasses import dataclass

@dataclass
class OscillatorState:
    psi_signal: float = 2.0
    phi_state: float = 3.0

@dataclass
class OscillatorContext:
    state: OscillatorState

class StableOscillator(NonlinearOperators):
    pass

system = StableOscillator()
context = OscillatorContext(state=OscillatorState())

for t in range(30):
    # 1. Apply resonance to amplify the signal
    system.resonance(None, context, "psi")
    
    # 2. Apply tanh to saturate the signal and prevent runaway growth
    system.hyperbolic_tangent(None, context, "psi", scale_factor=5.0)
    
    # 3. Apply decay to the other variable to create dampening
    system.exponential_decay(None, context, "phi", decay_rate=0.1, dt=1.0)
    
    # 4. Print the current state
    print(f"t={t}: ψ={context.state.psi_signal:.4f}, φ={context.state.phi_state:.4f}")
```

This simple program creates a complex, oscillating system that is stable and bounded, thanks to the interplay of the three nonlinear operators.

---

## 4. Example Programs

We have created four new example programs to demonstrate the power of v3.0:

-   **01_memory_decay.py**: Models how memories fade over time using `exp-`.
-   **02_neural_activation.py**: Models how neurons saturate using `tanh`.
-   **03_viral_spread.py**: Models viral growth using `^2`.
-   **04_stable_oscillator.py**: Combines all three operators to create a stable, oscillating system.

You can find these examples in the `/examples/v3/` directory.

---

## 5. The Big Picture: What v3.0 Unlocks

v3.0 is a transformative step for HARMONIA-DSL. It enables you to model:

-   **Complex Systems**: Create systems with feedback loops, emergent behavior, and chaotic dynamics.
-   **Biological Systems**: Model neurons, population dynamics, and other biological phenomena.
-   **Social Systems**: Simulate viral spread, market dynamics, and other social phenomena.
-   **Consciousness**: The combination of resonance, saturation, and decay is a key component of many theories of consciousness.

**v3.0 is the bridge from simple, linear systems to the complex, nonlinear reality of our world.**

---

## 6. Next Steps

-   **Explore the examples**: Run the example programs to see the new operators in action.
-   **Experiment**: Try combining the operators in new ways to create your own complex systems.
-   **Provide feedback**: Let us know what you think of v3.0 and what you would like to see in future versions.

**Welcome to the next level of harmonic intelligence.**
