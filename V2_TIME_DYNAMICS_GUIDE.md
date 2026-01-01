# HARMONIA-DSL v2.0: Time & Dynamics User Guide

**From Static Calculations to Dynamic Simulations**

---

## Overview

HARMONIA-DSL v2.0 introduces **time and dynamics** into the language, transforming it from a static, algebraic model into a dynamic, calculus-based simulator of harmonic intelligence.

This upgrade enables:
- **Dynamic simulation** of system evolution over time
- **Calculus operators** (`∂` for derivatives, `∫` for integrals)
- **Memory and learning** through state history
- **Predictive safety** by monitoring rates of change
- **Formal verification** of long-term stability

---

## What's New in v2.0

### 1. TimeSteppingInterpreter

The new `TimeSteppingInterpreter` wraps the core interpreter and executes programs over discrete time steps, maintaining a complete history of all state variables.

```python
from time_stepping_interpreter import TimeSteppingInterpreter

interpreter = TimeSteppingInterpreter()
result = interpreter.run(program, num_steps=100)
```

### 2. State History

Every state variable now maintains a time-ordered history:
- `psi_signal` (ψ)
- `phi_state` (φ)
- `epsilon_drift` (ε)
- `stabilized_value` (Σ)
- `depth`, `charge`, `phase`

Access history:
```python
psi_history = result.get_history("psi_signal")
print(f"ψ evolved from {psi_history[0]} to {psi_history[-1]}")
```

### 3. New Operators

#### `∂` (Partial Derivative)

Computes the rate of change of a variable:

```
∂ psi_signal
```

This calculates `∂ψ/∂t ≈ ψ(t) - ψ(t-1)` and stores the result in `context.derivative_value`.

**Use cases:**
- Detect if a system is improving or degrading
- Predict future states based on current velocity
- Implement adaptive control (respond to trends, not just values)

#### `∫` (Time Integral)

Computes the accumulated value of a variable over time:

```
∫ psi_signal 10
```

This integrates ψ over the last 10 time steps using the trapezoidal rule.

**Use cases:**
- Calculate total experience or exposure
- Measure long-term stability (has the system been safe?)
- Implement energy calculations (work done over time)

---

## Quick Start

### Example 1: Basic Time-Stepping

```python
from time_stepping_interpreter import run_time_stepping

program = """
Φ 5 3 0.1
Σ
"""

result = run_time_stepping(program, num_steps=10)

print(f"Final stabilized value: {result.current_context.state.stabilized_value}")
print(f"History length: {len(result.history['stabilized_value'])}")
```

### Example 2: Monitoring Rate of Change

```python
from time_stepping_interpreter import TimeSteppingInterpreter

program = """
Φ 5 3 0.1
Ψ 0.5
∂ psi_signal
"""

interpreter = TimeSteppingInterpreter()
result = interpreter.run(program, num_steps=20)

# Check the rate of change
derivative = interpreter.compute_derivative(result, "psi_signal")
print(f"Rate of change: {derivative}")

if derivative > 0:
    print("System is increasing")
elif derivative < 0:
    print("System is decreasing")
else:
    print("System is stable")
```

### Example 3: Predictive Safety

```python
program = """
Φ 5 3 0.2
ε 0.05
∂ epsilon_drift
"""

interpreter = TimeSteppingInterpreter()
result = interpreter.run(program, num_steps=50)

drift_derivative = interpreter.compute_derivative(result, "epsilon_drift")

if drift_derivative > 0.1:
    print("⚠️  WARNING: Drift is increasing rapidly!")
    print("System is trending towards danger.")
elif drift_derivative < -0.1:
    print("✅ System is stabilizing")
else:
    print("✓ System is stable")
```

---

## Complete Example Programs

### 1. Oscillating System

```harmonia
# oscillating_system.hrm
# A system that oscillates between two states

Φ 5 3 0.1
Ψ 1
Λ -0.5
Σ
```

Run it:
```python
result = run_time_stepping(open("oscillating_system.hrm").read(), num_steps=50)

import matplotlib.pyplot as plt
plt.plot(result.get_history("psi_signal"))
plt.title("Oscillating ψ Signal")
plt.xlabel("Time Step")
plt.ylabel("ψ")
plt.show()
```

### 2. Accumulation and Integration

```harmonia
# accumulation.hrm
# A system that accumulates value over time

Φ 1 1 0.0
Ψ 0.1
∫ psi_signal
```

Run it:
```python
result = run_time_stepping(open("accumulation.hrm").read(), num_steps=100)

integral = interpreter.compute_integral(result, "psi_signal")
print(f"Total accumulated value: {integral}")
```

### 3. Adaptive Stabilization

```harmonia
# adaptive_stabilization.hrm
# A system that adapts based on its rate of change

Φ 10 5 0.3
∂ epsilon_drift
Σ
```

Run it:
```python
result = run_time_stepping(open("adaptive_stabilization.hrm").read(), num_steps=100)

drift_history = result.get_history("epsilon_drift")
print(f"Initial drift: {drift_history[0]}")
print(f"Final drift: {drift_history[-1]}")

if drift_history[-1] < drift_history[0]:
    print("✅ System successfully stabilized over time")
```

---

## API Reference

### TimeSteppingInterpreter

```python
class TimeSteppingInterpreter:
    def __init__(self, history_maxlen: int = 1000):
        """Initialize with maximum history length"""
    
    def run(self, program: str, num_steps: int, 
            initial_context: Optional[TimeSteppingContext] = None) -> TimeSteppingContext:
        """Execute a program over multiple time steps"""
    
    def run_file(self, filename: str, num_steps: int,
                 initial_context: Optional[TimeSteppingContext] = None) -> TimeSteppingContext:
        """Execute a .hrm file over multiple time steps"""
    
    def compute_derivative(self, ts_context: TimeSteppingContext, 
                          variable_name: str) -> float:
        """Compute ∂S/∂t for a variable"""
    
    def compute_integral(self, ts_context: TimeSteppingContext,
                        variable_name: str, window_size: Optional[int] = None) -> float:
        """Compute ∫ S dt for a variable"""
```

### TimeSteppingContext

```python
@dataclass
class TimeSteppingContext:
    current_context: FieldContext  # Current state
    current_time: int              # Current time step
    num_steps: int                 # Total steps executed
    history: Dict[str, deque]      # State history
    derivative_value: float        # Last computed derivative
    integral_value: float          # Last computed integral
    
    def update_history(self):
        """Record current state into history"""
    
    def get_history(self, variable_name: str) -> List[float]:
        """Get complete history of a variable"""
    
    def get_current_value(self, variable_name: str) -> float:
        """Get current value of a variable"""
```

---

## Mathematical Foundations

For the complete mathematical formalization, see:
- `/theory/V2_TIME_DYNAMICS_FORMALIZATION.md`

Key concepts:
- **Discrete Time Model**: Time progresses in discrete steps `t = 0, 1, 2, ...`
- **State History**: `H(S) = [S(t-n+1), ..., S(t)]`
- **Backward Difference**: `∂S/∂t ≈ S(t) - S(t-1)`
- **Trapezoidal Rule**: `∫ S dt ≈ sum of averages of consecutive pairs`

---

## Performance Considerations

- **History Length**: Set `history_maxlen` appropriately. Default is 1000 steps.
- **Memory Usage**: Each variable stores `history_maxlen` floats (~8 KB per variable at default)
- **Computation**: Time-stepping adds ~10-20% overhead compared to single execution
- **Optimization**: For long simulations, consider periodic history pruning

---

## What's Next?

v2.0 unlocks the path to the complete Grand Harmonic Equation:

- **v3.0**: Nonlinear dynamics (exponentials, resonance)
- **v4.0**: Multi-agent coordination
- **v5.0**: Energy and thermodynamics
- **v6.0**: Probability and uncertainty
- **v7.0**: Quantum integration
- **v8.0**: Consciousness modeling
- **v9.0**: Self-modification
- **v10.0+**: Complete GHE implementation

---

## Support

For questions, issues, or contributions:
- GitHub: https://github.com/Andrewkadz/HARMONIA-DSL
- Academic Paper: https://www.academia.edu/145699830/
- Theory: `/theory/` directory

**Welcome to the age of dynamic harmonic intelligence.** 🎵✨
