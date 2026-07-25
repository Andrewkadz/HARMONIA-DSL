# HARMONIA-DSL v6.0: Memory & Learning - User Guide

**Author**: Manus AI  
**Date**: January 1, 2026  
**Version**: 6.0

---

## 1. Introduction to v6.0

v6.0 is a landmark release for HARMONIA-DSL, introducing the `{ Ψ± * K }` term from the Grand Harmonic Equation (GHE). This update transforms agents from reactive entities into **learning systems** capable of memory, foresight, and skill acquisition. This guide provides a comprehensive overview of the new capabilities and how to use them.

### Key Features

- **Ψ- (Psi-minus)**: The ability to recall and learn from past experiences.
- **Ψ+ (Psi-plus)**: The ability to project future states based on learned patterns.
- **K (Kappa)**: A measure of accumulated knowledge that grows with experience.

These components work together to create a powerful learning system that enhances an agent's ability to navigate its environment, avoid danger, and achieve goals, all while remaining bound by the core safety principles of HARMONIA-DSL.

---

## 2. The Core Components

The memory and learning system is composed of several interconnected classes that work together to provide the new capabilities.

### 2.1. `State`

A dataclass representing the system's state at a point in time, including `psi`, `phi`, `epsilon`, and a `timestamp`.

### 2.2. `MemoryBuffer` (Ψ-)

This class implements the Ψ- operator. It stores a history of states and provides a `recall()` method that returns a weighted average of past states, with more recent states having a greater influence.

### 2.3. `KnowledgeAccumulator` (K)

This class implements the K operator. It tracks the accumulated knowledge of the system. Knowledge increases when the agent encounters new situations (i.e., when there is a large difference between the current state and the recalled memory).

### 2.4. `FutureProjector` (Ψ+)

This class implements the Ψ+ operator. It learns the underlying dynamics of the system (acceleration) and uses this to project future states. The `project()` method returns a list of possible future states.

### 2.5. `MemoryLearningEngine`

This is the main class that integrates all the other components. It provides a simple interface to process new states, update knowledge, and get the full memory-learning term.

---

## 3. How to Use v6.0

Using the new memory and learning capabilities is straightforward. The following steps outline the basic workflow:

1.  **Instantiate the `MemoryLearningEngine`**: Create an instance of the engine, optionally configuring parameters like `memory_depth`, `decay_rate`, and `learning_rate`.

2.  **Process States**: For each new state your agent encounters, pass it to the `engine.process_state()` method. This will update the memory buffer, knowledge accumulator, and future projector.

3.  **Apply to System Output**: Use the `engine.apply_to_system()` method to get an enhanced output that incorporates the memory-learning term. This enhanced output can then be used to guide the agent's actions.

### Example Code Snippet

```python
from memory_learning import State, MemoryLearningEngine

# 1. Instantiate the engine
engine = MemoryLearningEngine(learning_rate=0.1)

# 2. Process a new state
current_state = State(psi=10.0, phi=8.0, epsilon=0.2, timestamp=1.0)
result = engine.process_state(current_state)

# 3. Get the enhanced output
base_output = (current_state.psi + current_state.phi) * (1 - current_state.epsilon)
enhanced_output = engine.apply_to_system(base_output, influence=0.1)

print(f"Base Output: {base_output:.2f}")
print(f"Enhanced Output: {enhanced_output:.2f}")
```

---

## 4. Example Programs

To demonstrate the power of v6.0, we have created three example programs that showcase different aspects of the new memory and learning capabilities.

### 4.1. Adaptive Safety Agent

This agent learns to avoid dangerous states (high epsilon) and maintain a state of harmony. It uses memory to remember which actions led to danger in the past and future projection to take preemptive action.

**To run this example:**
```bash
python3.11 examples/adaptive_safety_agent.py
```

### 4.2. Pattern Learning Agent

This agent learns to recognize and predict cyclical patterns in its environment. It demonstrates how memory can be used to improve prediction accuracy over time.

**To run this example:**
```bash
python3.11 examples/pattern_learning_agent.py
```

### 4.3. Predictive Control Agent

This agent uses future projection to take preemptive action and prevent problems before they occur. It demonstrates how Ψ+ can be used for proactive control.

**To run this example:**
```bash
python3.11 examples/predictive_control_agent.py
```

---

## 5. Conclusion

v6.0 is a significant step forward for HARMONIA-DSL, providing the foundational components for creating truly intelligent and adaptive agents. By enabling agents to learn from the past and project into the future, we are moving closer to our goal of creating verifiably safe AI that can learn and grow while remaining fundamentally aligned with human values.
