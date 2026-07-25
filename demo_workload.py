"""
CoherentFlow Demo: Heavy Workload Simulation
============================================

This script demonstrates CoherentFlow handling a heavy, CPU-intensive workload.
It compares a naive approach (launch everything) vs. the ANIMUS approach.

The workload simulates "video processing" or "data mining" - tasks that
spike CPU and memory usage.
"""

import time
import math
import random
from coherent_flow import CoherentFlowScheduler

def heavy_computation(n_iterations: int):
    """Simulate a CPU-intensive task (e.g., matrix math)."""
    result = 0.0
    # Create some memory pressure too
    data = [random.random() for _ in range(10000)]
    
    start = time.time()
    for i in range(n_iterations):
        # Do some math
        val = math.sin(i) * math.cos(i)
        result += val
        # Access memory
        idx = int(abs(val) * 9999)
        data[idx] = val
        
    return result

def run_demo():
    print("="*60)
    print("COHERENT FLOW DEMO: ANIMUS-GATED SCHEDULING")
    print("="*60)
    print("Simulating 50 heavy tasks (CPU + Memory intensive)...")
    print("Watch how the worker count adjusts to system stress.")
    print("-" * 60)
    
    # Initialize Scheduler
    # We set max_workers high (16) to show how it throttles down.
    # If we ran 16 of these at once on a standard laptop, it might freeze.
    scheduler = CoherentFlowScheduler(max_workers=16, swarm_size=17)
    
    # Submit 50 tasks
    # Each task takes roughly 0.5 - 1.0 seconds of pure CPU
    for i in range(50):
        scheduler.submit(heavy_computation, 200000)
        
    # Run
    start_time = time.time()
    scheduler.run()
    end_time = time.time()
    
    # Report
    stats = scheduler.get_report()
    print("-" * 60)
    print("RESULTS:")
    print(f"Total Time:      {stats['duration']:.2f} seconds")
    print(f"Throughput:      {stats['throughput']:.2f} tasks/sec")
    print(f"Avg ANIMUS:      {stats['avg_animus']:.2f} (Coherence)")
    print(f"Avg Concurrency: {stats['avg_concurrency']:.2f} workers")
    print("="*60)
    print("Observation:")
    print("Notice that 'Avg Concurrency' is likely LESS than 16.")
    print("The scheduler voluntarily slowed down to keep the system coherent.")
    print("="*60)

if __name__ == "__main__":
    run_demo()
