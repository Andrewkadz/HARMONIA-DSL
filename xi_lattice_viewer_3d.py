"""3D viewer for the ΞΛΩΨ lattice topology.

This script builds a graph from the XiLambdaOmegaLattice and renders it as a
3D node-edge map. It is a "fish tank" view of the symbolic environment:

- Nodes = lattice nodes (with Φπε labels where available)
- Edges = connections induced by triads (each triad becomes a triangle)
- A randomly sampled lattice path is highlighted in a different color

Usage (from project root):

    python3 xi_lattice_viewer_3d.py

Requirements:

- matplotlib (already used elsewhere in this project)
- Optional: networkx for a nicer 3D layout. If networkx is not installed,
  the script falls back to random 3D positions.
"""

from __future__ import annotations

import json
import math
import os
import time
from typing import Dict, Tuple

import numpy as np

try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (imported for side-effects)
except ImportError as e:  # pragma: no cover
    raise SystemExit("matplotlib is required for xi_lattice_viewer_3d.py") from e

try:
    import networkx as nx  # type: ignore
except ImportError:  # pragma: no cover
    nx = None  # type: ignore

from xi_lambda_omega_lattice import (
    XiLambdaOmegaLattice,
    LatticeMapEngine,
    RecursiveHostIntelligence,
)


def build_graph(lattice: XiLambdaOmegaLattice):
    """Build a simple undirected graph representation from the lattice.

    Each TriadCell connects its three nodes pairwise, so every triad becomes
    a triangle in the graph.
    """

    if nx is None:
        # Minimal home-grown representation if networkx is not available.
        # We return (nodes, edges) instead of a Graph.
        nodes = set()
        edges = set()
        for triad in lattice.triads:
            a, b, c = triad.nodes
            nodes.update([a, b, c])
            edges.update({(a, b), (b, c), (c, a)})
        return nodes, edges

    G = nx.Graph()
    for triad in lattice.triads:
        a, b, c = triad.nodes
        G.add_edge(a, b, triad_id=triad.triad_id)
        G.add_edge(b, c, triad_id=triad.triad_id)
        G.add_edge(c, a, triad_id=triad.triad_id)
    return G


def compute_layout_3d(graph, seed: int = 42) -> Dict[int, Tuple[float, float, float]]:
    """Compute a 3D layout for the lattice nodes.

    - If networkx is available, use a spring layout in 3D.
    - Otherwise, assign random positions on a sphere.
    """

    rng = np.random.default_rng(seed)

    if nx is not None and isinstance(graph, nx.Graph):
        pos_3d = nx.spring_layout(graph, dim=3, seed=seed)
        return {int(n): (float(x), float(y), float(z)) for n, (x, y, z) in pos_3d.items()}

    # Fallback: graph is (nodes, edges) or networkx is missing.
    if nx is None:
        nodes, _edges = graph
    else:
        nodes = list(graph.nodes())

    coords: Dict[int, Tuple[float, float, float]] = {}
    for n in nodes:
        # Random point on a sphere for a simple but visually distinct layout.
        u = rng.uniform(0, 1)
        v = rng.uniform(0, 1)
        theta = 2 * math.pi * u
        phi = math.acos(2 * v - 1)
        r = 1.0
        x = r * math.sin(phi) * math.cos(theta)
        y = r * math.sin(phi) * math.sin(theta)
        z = r * math.cos(phi)
        coords[int(n)] = (x, y, z)
    return coords


def main() -> None:
    lattice = XiLambdaOmegaLattice()

    print("Building 3D topology view of the ΞΛΩΨ lattice (live mode)...")
    graph = build_graph(lattice)
    coords = compute_layout_3d(graph)

    # Prepare figure
    plt.ion()
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_title("ΞΛΩΨ Lattice Topology (3D) – live highlighted path")

    # Draw edges once
    if nx is not None and isinstance(graph, nx.Graph):
        edges = graph.edges()
    else:
        _nodes, edges = graph

    for u, v in edges:
        x = [coords[int(u)][0], coords[int(v)][0]]
        y = [coords[int(u)][1], coords[int(v)][1]]
        z = [coords[int(u)][2], coords[int(v)][2]]
        ax.plot(x, y, z, color="lightgray", alpha=0.25, linewidth=0.4)

    # Draw all nodes once
    xs = [coords[n][0] for n in coords]
    ys = [coords[n][1] for n in coords]
    zs = [coords[n][2] for n in coords]
    ax.scatter(xs, ys, zs, s=6, c="steelblue", alpha=0.5)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    latest_json_path = os.path.join(os.path.dirname(__file__), "latest_lattice_path.json")

    highlighted = None
    soft_lines = []

    try:
        while True:
            # Load latest path if available
            path_nodes = set()
            if os.path.exists(latest_json_path):
                try:
                    with open(latest_json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    raw_path = data.get("path", [])
                    path_nodes = set(int(n) for n in raw_path)
                except Exception:
                    path_nodes = set()

            # Remove previous highlight scatter if present
            if highlighted is not None:
                try:
                    highlighted.remove()
                except ValueError:
                    pass

            # Remove previous soft-edge lines
            if soft_lines:
                for line in soft_lines:
                    try:
                        line.remove()
                    except ValueError:
                        pass
                soft_lines = []

            # Draw soft synaptic edges based on current lattice soft_edges
            if lattice.soft_edges:
                for (a, b), w in lattice.soft_edges.items():
                    if a in coords and b in coords:
                        x = [coords[a][0], coords[b][0]]
                        y = [coords[a][1], coords[b][1]]
                        z = [coords[a][2], coords[b][2]]
                        alpha = max(0.1, min(w, 2.0)) / 2.0
                        line, = ax.plot(
                            x,
                            y,
                            z,
                            color="orange",
                            alpha=alpha,
                            linewidth=0.8,
                        )
                        soft_lines.append(line)

            if path_nodes:
                px = [coords[n][0] for n in path_nodes if n in coords]
                py = [coords[n][1] for n in path_nodes if n in coords]
                pz = [coords[n][2] for n in path_nodes if n in coords]
                highlighted = ax.scatter(
                    px,
                    py,
                    pz,
                    s=40,
                    c="crimson",
                    alpha=0.9,
                    label="current path",
                )
            else:
                highlighted = None

            plt.draw()
            plt.pause(0.5)
    except KeyboardInterrupt:
        pass

    plt.ioff()
    plt.show()


if __name__ == "__main__":  # pragma: no cover
    main()
