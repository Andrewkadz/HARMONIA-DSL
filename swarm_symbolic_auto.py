"""Closed symbolic swarm simulation (no user prompts).

This script runs the numeric HarmonicSwarm + ΞΛΩΨ lattice in a closed loop,
continuously generating lattice paths, coupling them back into the swarm, and
updating `latest_lattice_path.json` so that the 3D viewer can show movement
without any user input.

Usage (from project root):

    python3 swarm_symbolic_auto.py

You can configure agent count, steps per tick, total ticks, and delay between
updates via the prompts at startup.
"""

from __future__ import annotations

import json
import math
import os
import time
from typing import Optional

from pure_harmonic_swarm import HarmonicSwarm
from xi_lambda_omega_lattice import (
    XiLambdaOmegaLattice,
    LatticeMapEngine,
    RecursiveHostIntelligence,
)
from swarm_symbolic_chat import (
    describe_swarm_numeric,
    apply_symbolic_coupling,
)


def main() -> None:
    print("Closed Harmonic Swarm + ΞΛΩΨ symbolic simulation (no prompts)")
    print("-----------------------------------------------------------")

    default_agents = 200
    default_steps_per_tick = 10
    default_ticks = 200
    default_delay = 0.2  # seconds between ticks

    try:
        raw_agents = input(f"Number of agents [{default_agents}]: ").strip()
        n_agents = int(raw_agents) if raw_agents else default_agents
    except ValueError:
        print("Invalid input, using default number of agents.")
        n_agents = default_agents

    try:
        raw_steps = input(
            f"Internal swarm steps per tick [{default_steps_per_tick}]: "
        ).strip()
        steps_per_tick = int(raw_steps) if raw_steps else default_steps_per_tick
    except ValueError:
        print("Invalid input, using default internal steps.")
        steps_per_tick = default_steps_per_tick

    try:
        raw_ticks = input(f"Number of ticks [{default_ticks}]: ").strip()
        max_ticks = int(raw_ticks) if raw_ticks else default_ticks
    except ValueError:
        print("Invalid input, using default ticks.")
        max_ticks = default_ticks

    try:
        raw_delay = input(f"Delay between ticks in seconds [{default_delay}]: ").strip()
        delay = float(raw_delay) if raw_delay else default_delay
    except ValueError:
        print("Invalid input, using default delay.")
        delay = default_delay

    print(
        f"\nInitializing closed symbolic swarm with {n_agents} agents, "
        f"steps_per_tick={steps_per_tick}, ticks={max_ticks}."
    )

    swarm = HarmonicSwarm(n_agents=n_agents, interaction_radius=None)
    lattice = XiLambdaOmegaLattice()
    map_engine = LatticeMapEngine(lattice=lattice)
    rhi = RecursiveHostIntelligence(lattice=lattice)

    # Symbolic energy starts mid-level and drifts slowly based on internal
    # dynamics (no user questions here).
    symbolic_energy = 0.5

    latest_path_json = os.path.join(os.path.dirname(__file__), "latest_lattice_path.json")

    for tick in range(1, max_ticks + 1):
        # 1) Advance numeric swarm
        for _ in range(max(0, steps_per_tick)):
            swarm.step()

        # 2) Let symbolic_energy wander gently based on swarm coherence
        stats = swarm.get_statistics()
        coh = float(stats["coherence"])
        # Slightly boost energy when coherence is high, damp when low
        symbolic_energy *= 1.0 + 0.01 * (coh - 0.9)
        symbolic_energy = max(0.1, min(symbolic_energy, 5.0))

        # 3) Generate a path; path length scales with symbolic_energy
        path_length = max(3, int(5 + 10 * symbolic_energy))
        path, symbolic_energy = map_engine.random_path_with_energy_cost(
            current_energy=symbolic_energy,
            length=path_length,
            start_node=None,
            gain_per_step=0.01,
        )

        # Reinforce synaptic edges along the path (synaptogenesis)
        for a, b in zip(path, path[1:]):
            lattice.reinforce_edge(int(a), int(b), delta=0.02, max_weight=2.0)

        # Apply a gentle global decay to keep the synaptic graph bounded
        lattice.decay_soft_edges(rate=0.001, min_weight=1e-4)

        # 4) Interpret path and couple back into swarm
        interp = rhi.interpret_path(path)
        coupling_desc = apply_symbolic_coupling(swarm, interp)

        # Persist latest path for the 3D viewer
        try:
            with open(latest_path_json, "w", encoding="utf-8") as f:
                json.dump({"path": path, "interp": interp}, f)
        except Exception:
            pass

        # 5) Print a compact numeric summary for observability
        numeric_desc = describe_swarm_numeric(swarm)
        print(f"Tick {tick:4d} | {numeric_desc} | {coupling_desc}")

        time.sleep(max(0.0, delay))

    print("\nClosed symbolic swarm run complete.")


if __name__ == "__main__":  # pragma: no cover
    main()
