#!/usr/bin/env python3
"""
Pure Harmonic Swarm - No LLM Layer
Mathematical agents with ψ, φ, Ω, ε state tracking
"""

import csv
import os
import numpy as np
import time
from dataclasses import dataclass
from typing import List, Optional
import multiprocessing as mp


@dataclass
class HarmonicAgent:
    """Lightweight harmonic oscillator agent"""
    agent_id: int
    psi: float  # Phase
    phi: float  # Position
    omega: float  # Frequency
    epsilon: float  # Exploration bias
    energy: float
    velocity: float
    entropy: float
    knowledge: float
    maturity: float

    def __init__(self, agent_id: int):
        self.agent_id = agent_id
        # Initialize with PHA-inspired values (263/97  2.711)
        self.psi = 9.54978 + np.random.randn() * 0.1
        self.phi = 7.84782 + np.random.randn() * 0.1
        self.omega = 1.0
        self.epsilon = 0.12 + np.random.randn() * 0.01
        self.energy = 101.0
        self.velocity = 0.0
        self.entropy = 0.0
        self.knowledge = 0.0
        self.maturity = 0.0

    def compute_response(self, mean_field: float, dt: float = 0.01) -> float:
        """Compute harmonic response based on field interaction"""
        # Prime Harmonic Analysis: 263/97 resonance
        pha_ratio = 263.0 / 97.0

        # Update velocity based on harmonic coupling
        acceleration = -self.omega**2 * (self.phi - mean_field) * pha_ratio
        acceleration += self.epsilon * np.sin(self.psi)

        self.velocity += acceleration * dt
        self.phi += self.velocity * dt
        self.psi += self.omega * dt

        # Update derived quantities
        self.energy = 0.5 * self.velocity**2 + 0.5 * self.omega**2 * self.phi**2
        self.entropy += abs(self.velocity) * dt * 0.01
        self.knowledge += self.energy * dt * 0.001
        self.maturity = min(1.0, self.maturity + dt * 0.001)

        return self.phi

    def __repr__(self):
        return (f"Agent{self.agent_id}: ={self.psi:.3f}, ={self.phi:.3f}, "
                f"E={self.energy:.2f}, v={self.velocity:.3f}")


class HarmonicSwarm:
    """Manages collective harmonic agent dynamics"""

    def __init__(self, n_agents: int, interaction_radius: Optional[int] = None):
        """Create a swarm.

        Parameters
        ----------
        n_agents:
            Number of harmonic agents.
        interaction_radius:
            If None (default), each agent couples to the global mean field
            (all-to-all coupling). If an integer r >= 0, each agent couples
            only to agents within index distance r (a simple 1D local
            neighborhood), creating spatial locality.
        """
        self.agents = [HarmonicAgent(i) for i in range(n_agents)]
        self.n_agents = n_agents
        self.iteration = 0
        self.interaction_radius = interaction_radius

    def compute_mean_field(self) -> float:
        """Calculate mean field from all agents"""
        return np.mean([agent.phi for agent in self.agents])

    def step(self, dt: float = 0.01):
        """Execute one swarm iteration."""

        if self.interaction_radius is None:
            # Global mean-field coupling
            mean_field = self.compute_mean_field()
            for agent in self.agents:
                agent.compute_response(mean_field, dt)
        else:
            # Local coupling: each agent sees only a neighborhood in index space
            r = max(0, int(self.interaction_radius))
            phis = np.array([a.phi for a in self.agents])
            n = self.n_agents
            for i, agent in enumerate(self.agents):
                left = max(0, i - r)
                right = min(n, i + r + 1)
                local_mean = float(phis[left:right].mean())
                agent.compute_response(local_mean, dt)

        self.iteration += 1

    def get_statistics(self):
        """Return swarm statistics"""
        phases = [a.phi for a in self.agents]
        energies = [a.energy for a in self.agents]

        return {
            'iteration': self.iteration,
            'mean_phi': np.mean(phases),
            'std_phi': np.std(phases),
            'mean_energy': np.mean(energies),
            'coherence': 1.0 / (1.0 + np.std(phases)),  # Inverse of phase spread
            'total_knowledge': sum(a.knowledge for a in self.agents)
        }


def benchmark_swarm(n_agents: int, n_iterations: int = 1000, interaction_radius: Optional[int] = None):
    """Benchmark swarm performance"""
    print(f"\n{'='*60}")
    if interaction_radius is None:
        coupling_desc = "global mean-field"
    else:
        coupling_desc = f"local radius = {interaction_radius}"
    print(f"Testing swarm with {n_agents} agents ({coupling_desc})...")
    print(f"{'='*60}")

    # Create swarm
    start_time = time.time()
    swarm = HarmonicSwarm(n_agents, interaction_radius=interaction_radius)
    init_time = time.time() - start_time

    print(f"Initialization: {init_time*1000:.2f}ms")
    print(f"Memory per agent: ~{(48 + 80) / 1024:.2f}KB (estimated)")

    # Run iterations
    start_time = time.time()
    for i in range(n_iterations):
        swarm.step()

        # Report every 200 iterations
        if i % 200 == 0:
            stats = swarm.get_statistics()
            print(f"\nIter {stats['iteration']:4d} | "
                  f"_mean={stats['mean_phi']:7.3f} b {stats['std_phi']:6.3f} | "
                  f"E_mean={stats['mean_energy']:7.2f} | "
                  f"Coherence={stats['coherence']:5.3f}")

    elapsed = time.time() - start_time

    print(f"\n{'='*60}")
    print(f"Total time: {elapsed:.3f}s")
    print(f"Iterations/sec: {n_iterations/elapsed:.1f}")
    print(f"Agent-updates/sec: {(n_agents * n_iterations)/elapsed:.1f}")
    print(f"{'='*60}\n")

    return swarm


def run_swarm_for_duration(
    n_agents: int,
    duration_seconds: float = 30.0,
    dt: float = 0.01,
    interaction_radius: Optional[int] = None,
    csv_path: str = "harmonic_swarm_trajectory.csv",
    library_dir: str = "swarm_runs",
) -> HarmonicSwarm:
    """Run the swarm for a fixed wall-clock duration and log movements.

    This is intended for generating a "movement map" of each agent over a
    real-time window. For every iteration we record, per agent:
        - wall-clock time since start,
        - iteration index,
        - agent_id,
        - psi (phase),
        - phi (position),
        - energy,
        - velocity.

    The results are written to ``csv_path`` so they can be visualized later
    (e.g., phase-space plots, per-agent trajectories, coherence over time).
    """

    swarm = HarmonicSwarm(n_agents, interaction_radius=interaction_radius)

    # Resolve final output path inside the library directory (data farm).
    # If csv_path is absolute, respect it; otherwise, place it under
    # ``library_dir`` and ensure that directory exists.
    if os.path.isabs(csv_path):
        final_path = csv_path
    else:
        os.makedirs(library_dir, exist_ok=True)
        final_path = os.path.join(library_dir, csv_path)

    start_time = time.time()
    next_log_time = start_time
    iteration = 0

    with open(final_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "t_seconds",
            "iteration",
            "agent_id",
            "psi",
            "phi",
            "energy",
            "velocity",
        ])

        while True:
            now = time.time()
            if now - start_time >= duration_seconds:
                break

            swarm.step(dt=dt)
            iteration += 1

            t_rel = now - start_time
            for agent in swarm.agents:
                writer.writerow([
                    f"{t_rel:.6f}",
                    iteration,
                    agent.agent_id,
                    f"{agent.psi:.6f}",
                    f"{agent.phi:.6f}",
                    f"{agent.energy:.6f}",
                    f"{agent.velocity:.6f}",
                ])

    elapsed = time.time() - start_time
    print(f"Swarm run completed in {elapsed:.3f}s with {iteration} iterations.")
    print(f"Trajectory written to {final_path}.")

    return swarm


def run_phase_space_demo():
    """Optional phase-space visualization (phi vs psi) for a small swarm.

    Uses matplotlib if available. This is intended for qualitative inspection
    of emergent patterns (oscillations, clustering) without affecting the
    numeric benchmarks.
    """

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; skipping phase-space demo.")
        return

    n_agents = 50
    steps = 2000
    demo_radius = 5  # local neighborhood for richer structure

    print("\nRunning phase-space demo (phi vs psi) with", n_agents, "agents...")
    swarm = HarmonicSwarm(n_agents, interaction_radius=demo_radius)

    # Track trajectories for a small subset of agents
    tracked = 20
    phi_traj = []
    psi_traj = []
    for _ in range(steps):
        swarm.step()
        phi_traj.append([a.phi for a in swarm.agents[:tracked]])
        psi_traj.append([a.psi for a in swarm.agents[:tracked]])

    phi_traj = np.array(phi_traj).reshape(-1)
    psi_traj = np.mod(np.array(psi_traj), 2 * np.pi).reshape(-1)

    plt.figure(figsize=(8, 6))
    plt.scatter(phi_traj, psi_traj, s=2, alpha=0.3)
    plt.xlabel("phi (position)")
    plt.ylabel("psi mod 2π (phase)")
    plt.title("Harmonic Swarm Phase Space (phi vs psi)")
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("=" * 60)
    print("PURE HARMONIC SWARM BENCHMARK")
    print("No LLM layer - Mathematical agents only")
    print("=" * 60)

    # Test different swarm sizes, including a large 5000-agent case
    test_sizes = [10, 50, 100, 500, 1000, 5000]

    for size in test_sizes:
        swarm = benchmark_swarm(size, n_iterations=1000)

        # Show final state of first 3 agents
        print("Sample agents:")
        for agent in swarm.agents[:3]:
            print(f"  {agent}")

    # Optional: run a small phase-space visualization demo
    run_phase_space_demo()
