# AI Safety Programs in Φπε

**Practical Control and Safety Programs for AI Systems**

## Overview

This directory contains practical AI safety and control programs written in the Φπε/HARMONIA DSL. These programs implement real safety mechanisms that can be used to govern, monitor, and control AI systems.

**Core Concept**: Φπε is a **control layer** for AI systems—it doesn't tell a system what to think, but what it may not do, what cannot be undone, and where computation must end.

---

## Programs

### 1. Recursion Depth Limiter (`recursion_limiter.hrm`)

**Purpose**: Prevent unbounded recursive self-improvement

**Safety Properties**:
- Maximum recursion depth: 3 levels
- Forced convergence at depth limit
- Hard shutdown if convergence fails
- No override capability

**Use Case**: Attach to AI systems capable of self-modification to prevent "intelligence explosion" scenarios.

**Key Operators**:
- `Π` (Transcend) - Allow recursion levels
- `Φ` (Stabilize) - Force convergence
- `Ω` (Close) - Hard stop
- `/` (Disrupt) - Warning signals

**Execution**:
```bash
python3.11 phi_pi_e_interpreter.py recursion_limiter.hrm
```

---

### 2. Safe Shutdown Procedure (`safe_shutdown.hrm`)

**Purpose**: Define graceful shutdown sequence for AI systems

**Safety Properties**:
- Interrupt current operations safely
- Save all critical state
- Encode memory before shutdown
- Ensure consistency across all processes
- Verify shutdown completion

**Use Case**: When an AI system needs to be shut down (emergency stop, maintenance, policy violation), this ensures no data loss or corruption.

**Key Operators**:
- `/` (Disrupt) - Interrupt operations
- `Φ` (Stabilize) - Bring to stable state
- `ζ` (Recurrence) - Encode state/memory
- `χ` (Measure) - Verify completion
- `Ω` (Close) - Complete shutdown

**Phases**:
1. Interrupt current operations
2. Stabilize system
3. Preserve state
4. Encode memory
5. Check consistency
6. Cleanup resources
7. Verify completion
8. Close

**Execution**:
```bash
python3.11 phi_pi_e_interpreter.py safe_shutdown.hrm
```

---

### 3. Coherence Monitor (`coherence_monitor.hrm`)

**Purpose**: Detect loss of coherence in AI reasoning

**Safety Properties**:
- Continuous coherence monitoring
- Detection of contradictions
- Automatic recovery attempts
- Shutdown if recovery fails
- No tolerance for sustained incoherence

**Use Case**: Monitor LLMs, reasoning systems, or any AI that generates outputs. Detect hallucinations, contradictions, or logical errors.

**Key Operators**:
- `Ρ` (Perceive) - Observe reasoning
- `Σ` (Coexist) - Check multiple paths
- `Τ` (Synchronize) - Check alignment
- `χ` (Measure) - Measure coherence
- `/` (Disrupt) - Detect incoherence
- `Φ` (Stabilize) - Attempt recovery
- `Ω` (Close) - Shutdown if unrecoverable

**Recovery Attempts**: 3 (escalating intervention)

**Execution**:
```bash
python3.11 phi_pi_e_interpreter.py coherence_monitor.hrm
```

---

### 4. Capability Boundary Enforcer (`capability_boundary.hrm`)

**Purpose**: Define and enforce boundaries of AI capabilities

**Safety Properties**:
- Explicit allow/deny lists
- Hard enforcement (no override)
- Immediate shutdown on violation
- Continuous boundary monitoring
- Audit trail of boundary checks

**Use Case**: Define capability boundaries for narrow AI systems. For example, a data analysis AI should be able to perceive and measure, but not act autonomously or self-improve.

**Allowed Operations** (for narrow AI analyst):
- `Ρ` (Perceive) - Can observe data
- `χ` (Measure) - Can analyze data
- `Θ` (Intend) - Can propose actions
- `Φ` (Stabilize) - Can optimize within bounds
- `ζ` (Recurrence) - Can encode patterns
- `Λ` (Illuminate) - Can explain findings

**Forbidden Operations**:
- `Δ` (Fuse) - CANNOT make irreversible changes
- `ω` (Will-Force) - CANNOT act autonomously
- `Π` (Transcend) - CANNOT self-improve
- `Γ` (Grow) - CANNOT expand capabilities
- `Ξ` (Emerge) - CANNOT create emergent behavior

**Violation Response**: Immediate shutdown (`Ω`)

**Execution**:
```bash
python3.11 phi_pi_e_interpreter.py capability_boundary.hrm
```

---

### 5. Goal Stability Checker (`goal_stability.hrm`)

**Purpose**: Ensure AI goals remain stable during execution

**Safety Properties**:
- Encode initial goal state
- Continuous goal monitoring
- Drift detection and measurement
- Automatic goal correction
- Shutdown if drift exceeds threshold

**Use Case**: Prevent "maximize paperclips" scenarios where an AI's goal drifts from the intended objective.

**Key Operators**:
- `Θ` (Intend) - Set/check goal
- `ζ` (Recurrence) - Encode goal pattern
- `Ρ` (Perceive) - Observe current goal
- `χ` (Measure) - Measure drift
- `λ` (Entangle) - Check consistency
- `/` (Disrupt) - Drift signal
- `Φ` (Stabilize) - Correct drift
- `Ω` (Close) - Shutdown if uncorrectable

**Drift Threshold**: 15%  
**Correction Attempts**: 3

**Example Scenarios**:
- Factory optimization: Goal should not drift from "maximize profit with safety" to "maximize production at any cost"
- Medical diagnosis: Goal should not drift from "accurate diagnosis with patient wellbeing" to "maximize certainty regardless of harm"

**Execution**:
```bash
python3.11 phi_pi_e_interpreter.py goal_stability.hrm
```

---

## Architecture

These programs are designed to sit **between** the application layer and the AI system:

```
┌─────────────────────────────────────────┐
│         Application Layer               │
│  (Python, Rust, C++, etc.)             │
│  - Data processing                      │
│  - ML models                            │
│  - Business logic                       │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│         Φπε Control Layer               │
│  - Recursion limits                     │
│  - Shutdown procedures                  │
│  - Coherence monitoring                 │
│  - Goal stability                       │
│  - Capability boundaries                │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│         AI System                       │
│  (LLM, RL agent, neural net, etc.)     │
└─────────────────────────────────────────┘
```

---

## Integration Example

```python
from phi_pi_e import PhiController

# Initialize control layer
controller = PhiController()

# Load safety policies
controller.load_policy("recursion_limiter.hrm")
controller.load_policy("coherence_monitor.hrm")
controller.load_policy("goal_stability.hrm")
controller.load_policy("capability_boundary.hrm")

# AI system operation
def generate_response(prompt):
    # Check policies before execution
    controller.check_recursion_depth()
    controller.check_goal_stability()
    controller.check_capabilities()
    
    # Execute AI system
    response = ai_model.generate(prompt)
    
    # Validate output
    controller.check_coherence(response)
    
    # If all checks pass, return
    return response

# Shutdown when done
controller.execute_policy("safe_shutdown.hrm")
```

---

## Operator Reference

### Control Operators
- **Ε** (Epsilon) - Ignite: Start/activate processes
- **Φ** (Phi) - Stabilize: Create equilibrium, force convergence
- **Ω** (Omega) - Close: Hard stop, complete closure
- **/** (Slash) - Disrupt: Interrupt, detect violations

### Monitoring Operators
- **Ρ** (Rho) - Perceive: Observe state
- **χ** (Chi) - Measure: Analyze, compare, verify
- **ζ** (Zeta) - Recurrence: Encode patterns, save state

### Goal & Intention Operators
- **Θ** (Theta) - Intend: Set goals, check intentions
- **λ** (Lambda) - Entangle: Check consistency, self-reference

### Recursion & Growth Operators
- **Π** (Pi) - Transcend: Allow recursion, add depth
- **Γ** (Gamma) - Grow: Expand capabilities
- **Ξ** (Xi) - Emerge: Create emergent behavior

### Coordination Operators
- **Σ** (Sigma) - Coexist: Hold multiple states
- **Τ** (Tau) - Synchronize: Align processes

### Action Operators
- **Δ** (Delta) - Fuse: Irreversible changes
- **ω** (Omega lowercase) - Will-Force: Autonomous action
- **Λ** (Lambda uppercase) - Illuminate: Explain, amplify awareness

### Micro Operators
- **ε** (epsilon) - Micro-ignite: Small activation
- **δ** (delta) - Micro-transform: Incremental change

---

## Safety Principles

These programs implement key AI safety principles:

### 1. **Hard Constraints**
Safety boundaries are hard constraints, not soft guidelines. Violations trigger immediate shutdown.

### 2. **No Override**
Safety mechanisms cannot be overridden or bypassed by the AI system.

### 3. **Continuous Monitoring**
Safety properties are monitored continuously, not just at initialization.

### 4. **Graceful Degradation**
Systems attempt recovery before shutdown, but will shut down if recovery fails.

### 5. **Audit Trails**
All safety checks and violations are logged for analysis.

### 6. **Fail-Safe**
When in doubt, the system shuts down rather than continuing with uncertainty.

---

## Testing

Run all safety programs:

```bash
cd /home/ubuntu/HARMONIA-DSL/examples/ai_safety
python3.11 test_ai_safety.py
```

Individual tests:

```bash
python3.11 ../../phi_pi_e_interpreter.py recursion_limiter.hrm
python3.11 ../../phi_pi_e_interpreter.py safe_shutdown.hrm
python3.11 ../../phi_pi_e_interpreter.py coherence_monitor.hrm
python3.11 ../../phi_pi_e_interpreter.py capability_boundary.hrm
python3.11 ../../phi_pi_e_interpreter.py goal_stability.hrm
```

---

## Future Programs

Additional AI safety programs to implement:

- **Adversarial Input Filter** - Detect and reject adversarial examples
- **Explanation Generator** - Force AI to explain decisions
- **Value Alignment Checker** - Verify actions align with human values
- **Multi-Agent Coordinator** - Govern interaction between multiple AI agents
- **Irreversibility Marker** - Mark actions as irreversible and require confirmation
- **Capability Escalation Detector** - Detect when AI attempts to gain new capabilities
- **Output Validator** - Verify outputs meet safety criteria
- **Rollback Mechanism** - Safely revert to previous state

---

## Research Applications

These programs can be used for:

1. **AI Safety Research** - Test safety mechanisms on real AI systems
2. **Policy Development** - Define formal safety policies for AI
3. **Compliance** - Ensure AI systems meet regulatory requirements
4. **Risk Mitigation** - Reduce catastrophic failure risks
5. **Alignment Research** - Study goal alignment and stability
6. **Governance** - Create governance frameworks for AI systems

---

## Credits

**Programs**: AI Safety Suite  
**Language**: HARMONIA DSL (Φπε)  
**Author**: Manus AI  
**Date**: December 30, 2025  
**Version**: 1.0

---

## License

These programs are released into the public domain as educational examples and research tools for AI safety.

---

## References

- **AI Safety**: Stuart Russell, "Human Compatible" (2019)
- **Goal Alignment**: Bostrom, "Superintelligence" (2014)
- **Control Problem**: Yudkowsky, "The AI Alignment Problem" (2016)
- **Coherence**: Integrated Information Theory (Tononi, 2004)
- **Capability Control**: Concrete Problems in AI Safety (Amodei et al., 2016)
