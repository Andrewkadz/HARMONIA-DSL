# CoherentFlow: ANIMUS-Gated Task Scheduler

**A Reference Implementation of the ANIMUS Paradigm**

CoherentFlow is a Python task scheduler that uses **ANIMUS (Regulatory Capacity)** to dynamically manage concurrency. Unlike traditional schedulers that use fixed thread pools, CoherentFlow uses a **Harmonic Swarm** to "feel" system stability and adjust workload in real-time.

---

## THE PROBLEM

Running heavy background workloads (video rendering, compilation, data processing) is a balancing act:
- **Too few workers:** CPU is idle, task takes too long.
- **Too many workers:** System freezes, mouse lags, UI becomes unresponsive.

Traditional solutions (fixed thread pools) are brittle. They don't know if you opened a web browser or started a game while the task is running.

## THE ANIMUS SOLUTION

CoherentFlow runs a **Harmonic Swarm** (17 mathematical agents) alongside your workload.
1.  **Measure:** It monitors system stress (CPU, Memory, Load).
2.  **Perturb:** Stress "perturbs" the swarm, causing phase dispersion.
3.  **React:**
    -   **High Coherence (High ANIMUS):** "System is singing." -> **Increase Concurrency.**
    -   **Low Coherence (Low ANIMUS):** "System is stuttering." -> **Throttle Concurrency.**

This guarantees **maximum throughput** while maintaining **system responsiveness**.

---

## USAGE

```python
from coherent_flow import CoherentFlowScheduler

def my_heavy_task(data):
    # Do something CPU intensive
    return process(data)

# Create scheduler
# max_workers=16 means "up to 16", but ANIMUS will decide the actual number.
scheduler = CoherentFlowScheduler(max_workers=16)

# Submit tasks
for item in big_dataset:
    scheduler.submit(my_heavy_task, item)

# Run
scheduler.run()
```

---

## RUNNING THE DEMO

```bash
python3.11 demo_workload.py
```

You will see the scheduler adjust the number of workers in real-time:

```
🟢 ANIMUS: 0.92 | Stress: 0.20 | Workers: 16/16 | Queue: 45
🟡 ANIMUS: 0.65 | Stress: 0.80 | Workers: 12/12 | Queue: 33
🔴 ANIMUS: 0.35 | Stress: 0.95 | Workers: 4/4   | Queue: 21
```

---

## FILES

-   `coherent_flow.py`: The core scheduler implementation.
-   `demo_workload.py`: A heavy workload simulation.
-   `pure_harmonic_swarm.py`: The underlying ANIMUS engine.

---

**Status:** Working Prototype
**License:** MIT
