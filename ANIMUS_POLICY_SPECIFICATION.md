# ANIMUS Policy Specification: Deterministic Governance Framework

**Version:** 1.0  
**Status:** Validated  
**Date:** January 2026

---

## OVERVIEW

The ANIMUS Policy Translator converts harmonic swarm metrics into safe, deterministic, auditable OS-level actions. This document specifies the complete policy framework.

---

## CORE PRINCIPLE

**Complexity is gated by ANIMUS.**

The system automatically adjusts its behavior based on regulatory capacity:
- High ANIMUS → Allow complexity
- Medium ANIMUS → Moderate complexity
- Low ANIMUS → Stabilize and recover

---

## ANIMUS BUDGET COMPUTATION

### Input Metrics

From the harmonic swarm daemon:

```
Coherence (C):           [0, 1]    Phase alignment
Phase_Dispersion (PD):   [0, 1]    Phase spread
Recovery_Rate (RR):      [0, ∞)    Coherence recovery speed
Energy_Stability (ES):   [0, 1]    Energy coupling stability
Entropy_Proxy (EP):      [0, 1]    System disorder proxy
```

### Normalization

```
C_norm = C                                    # Already [0,1]
PD_norm = 1 - min(PD, 1.0)                   # Invert: low dispersion = high
RR_norm = min(RR / RR_max, 1.0)              # Cap at 1.0
ES_norm = ES                                  # Already [0,1]
EP_norm = 1 - min(EP, 1.0)                   # Invert: low entropy = high
```

### Weighted Aggregation

```
ANIMUS = w_c × C_norm
       + w_pd × PD_norm
       + w_rr × RR_norm
       + w_es × ES_norm
       + w_ep × EP_norm

Where weights sum to 1.0:
  w_c = 0.35    (Coherence is primary)
  w_pd = 0.20   (Phase dispersion is important)
  w_rr = 0.20   (Recovery speed matters)
  w_es = 0.15   (Energy stability is secondary)
  w_ep = 0.10   (Entropy proxy is tertiary)
```

### Result

```
ANIMUS ∈ [0, 1]

0.0 = Complete fragmentation, system unstable
0.5 = Moderate coherence, moderate complexity allowed
1.0 = Perfect coherence, maximum complexity allowed
```

---

## POLICY DECISION TREE

### Level 1: ANIMUS Threshold

```
IF ANIMUS >= 0.8:
    POLICY_LEVEL = "HIGH"
    
ELIF ANIMUS >= 0.5:
    POLICY_LEVEL = "MEDIUM"
    
ELIF ANIMUS >= 0.2:
    POLICY_LEVEL = "LOW"
    
ELSE:
    POLICY_LEVEL = "CRITICAL"
```

### Level 2: Component-Level Thresholds

For research-grade ANIMUS state vector, additional thresholds:

```
IF Coherence < 0.5:
    COHERENCE_ALERT = TRUE
    → Reduce concurrency immediately
    
IF Phase_Dispersion > 0.3:
    PHASE_ALERT = TRUE
    → Dampen velocity, reduce load
    
IF Recovery_Rate < 0.1:
    RECOVERY_ALERT = TRUE
    → Enter stabilization mode
    
IF Energy_Stability < 0.4:
    ENERGY_ALERT = TRUE
    → Reduce model size, defer heavy ops
```

---

## POLICY ACTIONS BY LEVEL

### HIGH POLICY (ANIMUS ≥ 0.8)

**Interpretation:** System is highly coherent, can handle complexity.

**Actions:**

1. **Process Scheduling**
   - Allow maximum concurrency
   - Aggressive parallelism
   - High priority for compute-intensive tasks

2. **Memory Management**
   - Allocate larger buffers
   - Allow memory-intensive models
   - Aggressive caching

3. **Model Selection**
   - Use larger models
   - Enable advanced features
   - Higher precision (float64)

4. **IO Operations**
   - Allow parallel IO
   - Aggressive prefetching
   - High bandwidth utilization

5. **Networking**
   - Allow many concurrent connections
   - High throughput mode
   - Aggressive buffering

### MEDIUM POLICY (0.5 ≤ ANIMUS < 0.8)

**Interpretation:** System is moderately coherent, moderate complexity.

**Actions:**

1. **Process Scheduling**
   - Moderate concurrency (50-75% of max)
   - Balanced parallelism
   - Mixed priority tasks

2. **Memory Management**
   - Standard buffer sizes
   - Medium-sized models
   - Selective caching

3. **Model Selection**
   - Use medium-sized models
   - Disable advanced features
   - Standard precision (float32)

4. **IO Operations**
   - Sequential IO preferred
   - Standard prefetching
   - Moderate bandwidth

5. **Networking**
   - Limited concurrent connections
   - Standard throughput
   - Conservative buffering

### LOW POLICY (0.2 ≤ ANIMUS < 0.5)

**Interpretation:** System coherence is degrading, reduce complexity.

**Actions:**

1. **Process Scheduling**
   - Reduce concurrency to 25-50%
   - Minimal parallelism
   - Single-threaded preferred

2. **Memory Management**
   - Reduce buffer sizes
   - Minimize memory usage
   - Disable caching

3. **Model Selection**
   - Use small models only
   - Disable all advanced features
   - Low precision (float16)

4. **IO Operations**
   - Strict sequential IO
   - Disable prefetching
   - Minimal bandwidth

5. **Networking**
   - Single connection only
   - Minimal throughput
   - Strict buffering

### CRITICAL POLICY (ANIMUS < 0.2)

**Interpretation:** System is fragmenting, enter stabilization mode.

**Actions:**

1. **Process Scheduling**
   - Single process only
   - No parallelism
   - Minimal task switching

2. **Memory Management**
   - Minimal memory allocation
   - Force garbage collection
   - Aggressive cleanup

3. **Model Selection**
   - Tiny models only
   - All features disabled
   - Minimal precision (int8)

4. **IO Operations**
   - No IO operations
   - Defer all non-critical IO
   - Focus on coherence recovery

5. **Networking**
   - No network operations
   - Defer all communication
   - Focus on local stabilization

---

## COMPONENT-LEVEL POLICIES

### Coherence-Based Actions

```
IF Coherence >= 0.9:
    # System is very synchronized
    → Allow aggressive scheduling
    → Enable speculative execution
    → Maximize parallelism

ELIF Coherence >= 0.7:
    # System is synchronized
    → Standard scheduling
    → Normal parallelism

ELIF Coherence >= 0.5:
    # System is moderately synchronized
    → Conservative scheduling
    → Reduced parallelism

ELSE:
    # System is fragmenting
    → Minimal scheduling
    → No parallelism
    → Focus on recovery
```

### Phase Dispersion-Based Actions

```
IF Phase_Dispersion < 0.1:
    # Phase is very tight
    → Allow phase-sensitive operations
    → Enable phase-locked loops

ELIF Phase_Dispersion < 0.2:
    # Phase is tight
    → Standard phase operations

ELIF Phase_Dispersion < 0.3:
    # Phase is loose
    → Dampen phase-sensitive ops
    → Increase phase margin

ELSE:
    # Phase is very loose
    → Disable phase-sensitive ops
    → Focus on phase recovery
```

### Recovery Rate-Based Actions

```
IF Recovery_Rate >= 1.0:
    # System recovers very quickly
    → Allow aggressive perturbations
    → Enable adaptive algorithms

ELIF Recovery_Rate >= 0.5:
    # System recovers quickly
    → Standard perturbations

ELIF Recovery_Rate >= 0.1:
    # System recovers slowly
    → Minimize perturbations
    → Reduce load changes

ELSE:
    # System recovers very slowly
    → No perturbations
    → Maintain steady state
    → Focus on recovery
```

---

## SAFETY CONSTRAINTS

### Hard Constraints (Never Violated)

```
1. Concurrency_Level <= f(ANIMUS)
   # Concurrency automatically capped based on ANIMUS

2. Model_Size <= g(ANIMUS)
   # Model size automatically limited based on ANIMUS

3. Memory_Allocation <= h(ANIMUS)
   # Memory automatically limited based on ANIMUS

4. IO_Bandwidth <= i(ANIMUS)
   # IO bandwidth automatically limited based on ANIMUS
```

### Soft Constraints (Preferred But Not Enforced)

```
1. Prefer sequential IO when ANIMUS < 0.6
2. Prefer small models when ANIMUS < 0.5
3. Prefer single-threaded when ANIMUS < 0.3
4. Prefer local operations when ANIMUS < 0.2
```

---

## DECISION AUDIT TRAIL

Every policy decision must be logged with:

```
{
  timestamp: ISO8601,
  animus_budget: float [0,1],
  policy_level: string,
  decision: string,
  action: string,
  reason: string,
  component_metrics: {
    coherence: float,
    phase_dispersion: float,
    recovery_rate: float,
    energy_stability: float,
    entropy_proxy: float
  }
}
```

**Example:**
```json
{
  "timestamp": "2026-01-12T10:30:45Z",
  "animus_budget": 0.75,
  "policy_level": "MEDIUM",
  "decision": "Reduce concurrency",
  "action": "Set max_threads = 4",
  "reason": "Coherence dropped to 0.72, entering MEDIUM policy",
  "component_metrics": {
    "coherence": 0.72,
    "phase_dispersion": 0.18,
    "recovery_rate": 0.85,
    "energy_stability": 0.68,
    "entropy_proxy": 0.25
  }
}
```

---

## POLICY TRANSITIONS

### Hysteresis (Prevent Oscillation)

To prevent rapid policy oscillation, use hysteresis:

```
ANIMUS_THRESHOLD_HIGH = 0.80
ANIMUS_THRESHOLD_LOW = 0.75

IF current_policy == "HIGH" AND ANIMUS < ANIMUS_THRESHOLD_LOW:
    → Transition to MEDIUM
    
ELIF current_policy == "MEDIUM" AND ANIMUS >= ANIMUS_THRESHOLD_HIGH:
    → Transition to HIGH
```

### Transition Delay

Add delay before transitioning to lower policy levels:

```
IF ANIMUS drops below threshold:
    Wait 5 seconds
    IF ANIMUS still below threshold:
        Transition to lower policy
    ELSE:
        Cancel transition
```

This prevents thrashing on transient dips.

---

## INTEGRATION WITH OS

### Process Priority

```
nice_value = -20 + 40 * (1 - ANIMUS)

ANIMUS = 1.0 → nice = -20 (highest priority)
ANIMUS = 0.5 → nice = 0   (normal priority)
ANIMUS = 0.0 → nice = +20 (lowest priority)
```

### CPU Affinity

```
num_cpus_allowed = ceil(total_cpus * ANIMUS)

ANIMUS = 1.0 → use all CPUs
ANIMUS = 0.5 → use half of CPUs
ANIMUS = 0.0 → use 1 CPU only
```

### Memory Limits

```
memory_limit = max_memory * ANIMUS

ANIMUS = 1.0 → full memory available
ANIMUS = 0.5 → half memory available
ANIMUS = 0.0 → minimal memory available
```

### IO Rate Limiting

```
io_rate_limit = max_io_bandwidth * ANIMUS

ANIMUS = 1.0 → full bandwidth
ANIMUS = 0.5 → half bandwidth
ANIMUS = 0.0 → minimal bandwidth
```

---

## POLICY TUNING

### Adjustable Parameters

```
w_c = 0.35          # Coherence weight (adjust 0.2-0.5)
w_pd = 0.20         # Phase dispersion weight (adjust 0.1-0.3)
w_rr = 0.20         # Recovery rate weight (adjust 0.1-0.3)
w_es = 0.15         # Energy stability weight (adjust 0.1-0.2)
w_ep = 0.10         # Entropy proxy weight (adjust 0.05-0.2)

THRESHOLD_HIGH = 0.80       # Adjust 0.7-0.9
THRESHOLD_MEDIUM = 0.50     # Adjust 0.4-0.6
THRESHOLD_LOW = 0.20        # Adjust 0.1-0.3

TRANSITION_DELAY = 5.0      # Seconds (adjust 1-10)
HYSTERESIS = 0.05           # Threshold band (adjust 0.01-0.1)
```

### Tuning Process

1. **Baseline:** Run with default parameters
2. **Measure:** Track system performance and coherence
3. **Adjust:** Increase weights for metrics that matter most
4. **Validate:** Confirm improvements
5. **Deploy:** Use tuned parameters in production

---

## POLICY EFFECTIVENESS METRICS

### Primary Metrics

```
Coherence_Maintained = (Final_Coherence - Initial_Coherence) / Initial_Coherence
  → Target: > 0 (coherence should not degrade)

Complexity_Allowed = Average_ANIMUS_Budget
  → Target: > 0.7 (system should allow reasonable complexity)

Recovery_Time = Time_to_Recover_After_Perturbation
  → Target: < 10 seconds (system should recover quickly)
```

### Secondary Metrics

```
Policy_Oscillation = Number_of_Policy_Transitions / Total_Time
  → Target: < 1 transition per hour (avoid thrashing)

False_Alarms = Transitions_to_LOW_that_recover_quickly / Total_LOW_transitions
  → Target: < 10% (avoid unnecessary stabilization)

Action_Effectiveness = Coherence_Improvement_After_Action / Expected_Improvement
  → Target: > 80% (actions should be effective)
```

---

## CONCLUSION

The ANIMUS Policy Framework provides:

1. **Deterministic governance** - All decisions are auditable
2. **Safety guarantees** - Complexity automatically gated
3. **Adaptive behavior** - System adjusts to conditions
4. **Transparency** - Full audit trail of decisions
5. **Tunability** - Parameters can be adjusted for different workloads

This enables systems to remain coherent, stable, and safe while operating under complex, dynamic conditions.

---

**Status: READY FOR IMPLEMENTATION**
