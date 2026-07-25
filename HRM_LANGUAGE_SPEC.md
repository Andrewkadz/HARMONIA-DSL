# HARMONIA Language Specification (v1.0)

**The Executable Swarm Language**

`.hrm` files are not just configuration; they are **Harmonic Scores**. They define the initial conditions, physical laws, and homeostatic constraints of a swarm system. The `harmonia` runner executes these scores using the ANIMUS engine.

---

## 1. Structure

A `.hrm` program consists of four main blocks:

1.  **SYSTEM**: Defines the swarm topology and size.
2.  **DIMENSIONS**: Defines the initial state of agent variables (Ψ, Φ, Ω).
3.  **LAWS**: Defines the "physics" that run on every agent, every step.
4.  **CONSTRAINTS**: Defines global regulatory actions based on emergent metrics.

---

## 2. Syntax Reference

### 2.1 SYSTEM Block
```hrm
SYSTEM MySwarmName {
    AGENTS: 100          // Number of agents
    TOPOLOGY: MeanField  // Interaction graph (MeanField, Grid, Ring)
    DT: 0.05             // Time step size
}
```

### 2.2 DIMENSIONS Block
Initialize the state vectors.
```hrm
DIMENSIONS {
    PSI: 1.0   // Awareness (Phase)
    PHI: 1.0   // Ethics (Coupling Strength)
    OMEGA: 0.0 // Coherence (Output Metric)
}
```

### 2.3 LAWS Block
Laws define how agents react to inputs.
-   **Scope:** Local (runs on each agent independently).
-   **Inputs:** External signals (e.g., `Stress`, `InputData`).
-   **Actions:** `PERTURB`, `SET`, `DECAY`.

```hrm
LAW "ThermalNoise" {
    INPUT: Stress
    
    // If system is stressed, add noise to awareness
    IF Stress > 0.1:
        PERTURB PSI BY (Stress * 0.5)
}
```

### 2.4 CONSTRAINTS Block
Constraints monitor global emergent properties (ANIMUS).
-   **Scope:** Global (runs on the swarm as a whole).
-   **Metrics:** `COHERENCE`, `ENERGY`, `ENTROPY`.
-   **Actions:** `EMIT`, `SET_GLOBAL`.

```hrm
CONSTRAINT "SafetyGate" {
    // If coherence drops, signal a throttle
    WHEN COHERENCE < 0.8:
        EMIT "THROTTLE_ACTIVE"
        SET_GLOBAL MAX_CONCURRENCY = 4
}
```

---

## 3. Execution Model

1.  **Parse:** The runner reads the `.hrm` file and initializes the `HarmonicSwarm`.
2.  **Loop:**
    -   **Inject Inputs:** External data (Stress, Load) is passed to the swarm.
    -   **Apply Laws:** Agent states are updated based on inputs.
    -   **Step Physics:** The Kuramoto-Sakaguchi dynamics evolve the system.
    -   **Check Constraints:** Global metrics are computed; constraints trigger events.
3.  **Output:** The runner emits a JSON stream of metrics and events.

---

## 4. Example: Cluster Rescue

```hrm
SYSTEM ClusterRescue {
    AGENTS: 100
    TOPOLOGY: MeanField
}

DIMENSIONS {
    PSI: 1.0
    PHI: 1.0
}

LAW "ThermalThrottling" {
    INPUT: Temperature
    
    // Heat causes decoherence
    IF Temperature > 80:
        PERTURB PSI BY 0.5
}

CONSTRAINT "AnimusGate" {
    WHEN COHERENCE < 0.8:
        EMIT "THROTTLE"
}
```
