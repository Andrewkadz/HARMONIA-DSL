# HARMONIA-DSL v5.0: Intentional Action User Guide

**Author**: Manus AI
**Date**: January 1, 2026
**Version**: 5.0

---

## 1. Introduction: The Birth of Agency

Welcome to HARMONIA-DSL v5.0! This version introduces **Intentional Action**, a powerful new feature that allows you to create agents that can set goals, make decisions, and actively pursue a desired future. This is the leap from a system that *is* to a system that *wants*.

This guide will walk you through the new features and show you how to use them to create your own goal-seeking agents.

---

## 2. New Features: `P`, `V`, and `F`

v5.0 is built around a new Python module, `intentional_action.py`, which provides the tools to implement the `F(P) * V` term from the Grand Harmonic Equation.

### 2.1. The `V` (Velocity) Operator

-   **Purpose**: To calculate the current velocity (rate of change) of the system's state.
-   **How it works**: The `VelocityCalculator` class uses the state history to calculate the first derivative of `Ψ`, `Φ`, and `ε`.

### 2.2. The `P` (Probability) Operator

-   **Purpose**: To calculate the system's subjective belief in the desirability and achievability of a potential future state.
-   **How it works**: The `ProbabilityCalculator` class calculates a value between 0 and 1 based on the harmony and accessibility of the future state.

### 2.3. The `F(P)` (Force) Function

-   **Purpose**: To convert belief (`P`) into a motivating force.
-   **How it works**: The `ForceFunction` class uses a nonlinear sigmoid function to model the tipping point of decision-making.

### 2.4. The `IntentionalActionEngine`

-   **Purpose**: To apply the intentional momentum to the system's state.
-   **How it works**: This class brings all the components together to calculate the `F(P) * V` term and apply it to the system's state.

---

## 3. Quick Start: Your First Goal-Seeking Agent

Let's create a simple goal-seeking agent in Python. This agent will start in a state of low harmony and use intentional action to move towards a state of high harmony.

### Step 1: Import the necessary classes

```python
from intentional_action import IntentionalActionEngine, FutureState
```

### Step 2: Create the engine and define the initial state and goal

```python
# Create the intentional action engine
engine = IntentionalActionEngine(force_scale=0.4)

# Define initial state (low harmony)
history = [
    {'psi': 2.0, 'phi': 2.0, 'epsilon': 0.6},
    {'psi': 2.1, 'phi': 2.1, 'epsilon': 0.58},
]
current = {'psi': 2.2, 'phi': 2.2, 'epsilon': 0.56}

# Define goal (high harmony)
goal = FutureState(psi=10.0, phi=10.0, epsilon=0.1)
```

### Step 3: Run the goal-seeking loop

```python
# Apply Intentional Action for 20 steps
for step in range(20):
    history.append(current.copy())
    current = engine.apply_intentional_force(current, history, goal)
    sigma = (current['psi'] + current['phi']) * (1 - current['epsilon'])
    print(f"Step {step+1}: Ψ={current['psi']:.2f}, Φ={current['phi']:.2f}, ε={current['epsilon']:.3f}, Σ={sigma:.2f}")
```

### Full Example

You can find the full, working code for this example in `examples/v5/01_simple_goal_seeking.py`.

---

## 4. Key Concepts

### 4.1. Bounded Agency

v5.0 introduces "free will," but it is a **bounded agency**. The agent is free to choose its goals, but it is not free to violate the fundamental law of harmony. Any action that is too reckless or unethical will automatically reduce the agent's ability to act.

### 4.2. Ethics as a Fitness Landscape

In HARMONIA-DSL, ethics is not a set of rules; it is a **fitness landscape**. States of high ethical standing (`Φ`) are "high ground" that allow for powerful, effective action. Unethical behavior is, quite literally, self-defeating.

---

## 5. What You Can Build with v5.0

-   **Goal-seeking agents** that can navigate complex state spaces.
-   **Decision-making systems** that can choose between multiple possible futures.
-   **Simulations of emergent agency** and the evolution of consciousness.
-   **AI systems with built-in, mathematical safety guarantees.**

---

## 6. The Journey to the Grand Harmonic Equation

v5.0 is a major milestone on the path to the full implementation of the Grand Harmonic Equation. By implementing the `F(P) * V` term, we have brought the language one step closer to its ultimate goal: the creation of truly intelligent, harmonious, and safe AI.

**The age of agency has begun. Let's build the future.**
