# HARMONIA-DSL v7.0: User Guide

**Author**: Manus AI  
**Date**: January 1, 2026

---

## 1. Introduction

Welcome to HARMONIA-DSL v7.0! This release introduces a groundbreaking new capability: **Energy & Thermodynamics**. By integrating fundamental principles of thermodynamics into the language, v7.0 provides a powerful new mechanism for creating safe, sustainable, and robust AI systems.

This guide will walk you through the core concepts, new features, and best practices for using the energy system in your HARMONIA-DSL programs.

---

## 2. Core Concepts

### 2.1. Energy as a Safety Constraint

The central idea of v7.0 is that **energy is a finite resource that constrains system behavior**. Just as a living organism cannot act without metabolic energy, an AI system running on HARMONIA-DSL v7.0 cannot act without computational energy. This creates a natural and unavoidable safety mechanism:

- **High Activity Consumes Energy**: Complex or frequent actions deplete the system's energy reserves.
- **Energy Depletion Reduces Capability**: As energy runs low, the system's ability to act is automatically reduced.
- **Safe Shutdown**: When energy is critically low, the system enters a safe, low-activity state, preventing catastrophic failure.

This "safe-by-design" approach means you don't have to manually code for every possible failure mode. The laws of thermodynamics provide a built-in safety net.

### 2.2. Thermodynamic Principles

v7.0 incorporates several key concepts from thermodynamics:

- **Entropy (S)**: A measure of disorder or uncertainty in the system. High entropy indicates a chaotic or dangerous state. The system must actively work to keep entropy low.
- **Temperature (T)**: Represents the system's level of activity. High activity leads to a higher temperature.
- **Free Energy (F)**: A measure of a system's stability, calculated as `F = E - T*S` (where E is internal energy). The system naturally seeks to minimize free energy, leading it toward states of low energy and low entropy (i.e., safe and ordered states).

---

## 3. The Energy System

The energy system is managed by a set of new classes that you can use in your programs.

### 3.1. `EnergyConstrainedEngine`

This is the main class you will interact with. It integrates all the components of the energy system.

**Initialization**:
```python
from energy_thermodynamics import EnergyConstrainedEngine

# Create an engine with 100 energy units and a recharge rate of 2.0 per step
engine = EnergyConstrainedEngine(capacity=100.0, recharge_rate=2.0)
```

### 3.2. `EnergyPool`

Manages the system's energy reserves.

- **`consume(amount)`**: Consumes a specified amount of energy.
- **`recharge(dt)`**: Recharges energy over a time step.
- **`get_state()`**: Returns the current `EnergyState`.

### 3.3. `ThermodynamicState`

Tracks the system's thermodynamic properties.

- **`update_entropy(drift, activity)`**: Updates the system's entropy.
- **`calculate_free_energy(internal_energy)`**: Calculates the free energy.

### 3.4. `EfficiencyTracker`

Monitors the system's energy efficiency.

- **`record_action(output, energy_cost)`**: Records the efficiency of an action.
- **`get_efficiency()`**: Returns the overall efficiency (η).

---

## 4. How to Use the Energy System

Using the energy system involves three main steps:

1.  **Initialize the Engine**: Create an instance of `EnergyConstrainedEngine` with your desired capacity and recharge rate.
2.  **Process Actions**: Use the `process_action()` method to execute actions with energy constraints.
3.  **Monitor State**: Check the system's energy level, entropy, and safety status.

### 4.1. Processing an Action

The `process_action()` method is the core of the energy system. It takes the following arguments:

- `action_magnitude`: The magnitude of the action being performed.
- `drift`: The system's current drift (ε).
- `sigma_base`: The base stabilized output from the Harmony Constraint.
- `psi`: The system's awareness state.

```python
result = engine.process_action(
    action_magnitude=5.0,
    drift=0.2,
    sigma_base=20.0,
    psi=10.0
)

print(f"Output: {result['output']:.2f}")
print(f"Energy Remaining: {result['energy_remaining']:.1f}")
```

### 4.2. Monitoring Safety

You can check the system's safety status at any time using the `check_safety()` method.

```python
safety_status = engine.check_safety()

if safety_status['safe']:
    print("System is safe.")
else:
    print("Safety warning!")
```

---

## 5. Example Walkthroughs

v7.0 comes with three example programs that demonstrate the power of the energy system.

### 5.1. Sustainable Agent

- **File**: `examples/sustainable_agent.py`
- **Concept**: An agent learns to choose tasks based on its current energy level, prioritizing easier tasks when energy is low to ensure long-term survival.

### 5.2. Safe Shutdown Demo

- **File**: `examples/safe_shutdown_demo.py`
- **Concept**: Demonstrates how the system's output gracefully degrades as energy is depleted, eventually entering a safe shutdown mode. This is a core safety feature of v7.0.

### 5.3. Resource Allocation

- **File**: `examples/resource_allocation.py`
- **Concept**: An agent must choose between multiple competing goals with different values and energy costs. The agent learns to prioritize goals dynamically to maximize its total value achieved.

---

## 6. Best Practices

- **Tune Your Parameters**: The `capacity` and `recharge_rate` of the `EnergyConstrainedEngine` are important parameters. Adjust them to match the demands of your specific application.
- **Monitor Entropy**: High entropy is a sign of a chaotic or unstable system. If you see entropy consistently increasing, it may indicate a problem with your agent's decision-making.
- **Use Efficiency**: The `EfficiencyTracker` can be a powerful tool for learning. Use the efficiency metric (η) as a reward signal to train your agents to be more sustainable.
- **Embrace Constraints**: Don't think of the energy system as a limitation. It's a powerful tool for building safer, more robust AI. Design your agents to work *with* the energy constraints, not against them.

---

## 7. API Reference

### `EnergyConstrainedEngine`

- `__init__(self, capacity, recharge_rate, initial_entropy)`
- `calculate_action_cost(self, action_magnitude, drift)`
- `apply_energy_constraint(self, sigma_base, psi)`
- `process_action(self, action_magnitude, drift, sigma_base, psi)`
- `get_energy_state(self)`
- `check_safety(self)`
- `reset(self)`

### `EnergyPool`

- `__init__(self, capacity, initial_energy, recharge_rate)`
- `consume(self, amount)`
- `recharge(self, dt, amount)`
- `get_state(self, timestamp)`
- `get_average_consumption(self, window)`

### `ThermodynamicState`

- `__init__(self, initial_entropy)`
- `update_entropy(self, drift, activity)`
- `update_temperature(self, activity)`
- `calculate_free_energy(self, internal_energy)`
- `minimize_entropy(self, rate)`

### `EfficiencyTracker`

- `__init__(self)`
- `record_action(self, output, energy_cost)`
- `get_efficiency(self)`
- `get_recent_efficiency(self, window)`

---

Happy coding, and may your systems always be in a state of low entropy!

