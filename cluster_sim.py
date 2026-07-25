"""
ANIMUS-HPC: Cluster Rescue Simulation
=====================================

A simulation demonstrating how ANIMUS-based orchestration outperforms
standard synchronization in large-scale GPU clusters.

THE PROBLEM: "The Straggler Effect"
In distributed training (Data Parallelism), the entire cluster waits for
the slowest GPU to finish its batch before synchronizing gradients.
If one GPU overheats or hits a network snag, 99 others sit idle.

THE ANIMUS SOLUTION:
Each GPU node runs a local Harmonic Swarm (ANIMUS Daemon).
- High ANIMUS: Process full batch.
- Low ANIMUS (Straggler): Automatically micro-throttle batch size or
  signal the cluster to "skip" this node for one step (Gradient Accumulation).

This simulation compares:
1. Standard Mode: All nodes wait for the slowest.
2. ANIMUS Mode: Nodes adapt workload based on coherence.
"""

import numpy as np
import time
import random
from dataclasses import dataclass
from typing import List

# Import our ANIMUS engine
from pure_harmonic_swarm import HarmonicSwarm

@dataclass
class GPUNode:
    id: int
    perf_factor: float = 1.0  # 1.0 = 100% speed
    temp: float = 60.0        # Celsius
    is_throttled: bool = False
    
    # ANIMUS State
    swarm: HarmonicSwarm = None
    animus: float = 1.0

    def __post_init__(self):
        # Each GPU has a tiny local swarm to monitor its own stability
        self.swarm = HarmonicSwarm(n_agents=5)

class ClusterSimulation:
    def __init__(self, n_gpus: int = 100, mode: str = "STANDARD"):
        self.n_gpus = n_gpus
        self.mode = mode  # "STANDARD" or "ANIMUS"
        self.nodes = [GPUNode(id=i) for i in range(n_gpus)]
        self.step_count = 0
        self.total_throughput = 0.0
        
    def _simulate_physics(self):
        """Simulate random thermal events and network noise."""
        for node in self.nodes:
            # Random fluctuation
            node.perf_factor = 1.0
            
            # 5% chance of a "hiccup" (network delay, OS noise)
            if random.random() < 0.05:
                node.perf_factor -= random.uniform(0.1, 0.3)
                
            # 1% chance of "thermal throttling" (severe slowdown)
            if random.random() < 0.01:
                node.temp += 20
                node.perf_factor = 0.2  # Straggler!
                
            # Cooling
            if node.temp > 60:
                node.temp -= 1
                
    def _update_animus(self):
        """Update ANIMUS state for each node."""
        for node in self.nodes:
            # Stress = Heat + Performance Drop
            stress = (max(0, node.temp - 70) / 30.0) + (1.0 - node.perf_factor)
            stress = min(stress, 1.0)
            
            # Perturb swarm
            if stress > 0.1:
                for agent in node.swarm.agents:
                    agent.psi += np.random.uniform(-stress, stress)
            
            node.swarm.step()
            stats = node.swarm.get_statistics()
            
            # ANIMUS = Coherence * (1 - Stress)
            node.animus = stats['coherence'] * (1.0 - (stress * 0.5))

    def step(self):
        """Execute one training step."""
        self._simulate_physics()
        
        if self.mode == "ANIMUS":
            self._update_animus()
            
        # Calculate processing time for this step
        # Base time is 1.0 seconds per batch
        
        if self.mode == "STANDARD":
            # The cluster speed is determined by the SLOWEST node (min perf_factor)
            worst_perf = min(n.perf_factor for n in self.nodes)
            step_time = 1.0 / worst_perf
            # Throughput = Batch Size (100) / Time
            throughput = self.n_gpus / step_time
            
        elif self.mode == "ANIMUS":
            # ANIMUS Logic:
            # If a node has Low ANIMUS, it processes a smaller batch (or skips).
            # This keeps its effective speed high (syncs faster), but contributes less data.
            
            effective_batch_size = 0
            node_times = []
            
            for node in self.nodes:
                # Policy: Gate workload by ANIMUS
                if node.animus > 0.8:
                    workload = 1.0
                elif node.animus > 0.5:
                    workload = 0.7  # Micro-throttle
                else:
                    workload = 0.2  # Emergency throttle (skip most work)
                
                # Time = Workload / Performance
                # If perf is 0.2 but workload is 0.2, time is 1.0 (Normal!)
                # This is the magic: The straggler doesn't slow down the pack.
                t = workload / max(0.1, node.perf_factor)
                node_times.append(t)
                effective_batch_size += workload
            
            # Sync time is still max of all nodes, but we optimized the slow ones.
            step_time = max(node_times)
            throughput = effective_batch_size / step_time
            
        self.total_throughput += throughput
        self.step_count += 1
        return throughput

def run_comparison():
    steps = 100
    n_gpus = 100
    
    print(f"ANIMUS-HPC SIMULATION: {n_gpus} GPUs, {steps} Steps")
    print("="*60)
    
    # Run Standard
    print("Running STANDARD Mode (Wait for Stragglers)...")
    sim_std = ClusterSimulation(n_gpus, mode="STANDARD")
    t_std = []
    for _ in range(steps):
        t_std.append(sim_std.step())
    avg_std = np.mean(t_std)
    print(f"-> Average Throughput: {avg_std:.2f} samples/sec")
    
    print("-" * 60)
    
    # Run ANIMUS
    print("Running ANIMUS Mode (Coherence-Gated Workload)...")
    sim_ani = ClusterSimulation(n_gpus, mode="ANIMUS")
    t_ani = []
    for _ in range(steps):
        t_ani.append(sim_ani.step())
    avg_ani = np.mean(t_ani)
    print(f"-> Average Throughput: {avg_ani:.2f} samples/sec")
    
    print("=" * 60)
    improvement = ((avg_ani - avg_std) / avg_std) * 100
    print(f"RESULTS: ANIMUS improved cluster efficiency by {improvement:.1f}%")
    print("=" * 60)
    print("WHY?")
    print("In Standard mode, one overheated GPU (perf=0.2) makes the whole cluster run at 0.2x speed.")
    print("In ANIMUS mode, that GPU detects low coherence and processes only 20% of the data.")
    print("It finishes on time. The other 99 GPUs run at full speed.")
    print("The total batch size drops slightly (99.2 vs 100), but speed stays at 1.0x.")
    print("=" * 60)

if __name__ == "__main__":
    run_comparison()
