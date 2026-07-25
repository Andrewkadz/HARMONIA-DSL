import json
import math
import os
import subprocess
from typing import Optional

from pure_harmonic_swarm import HarmonicSwarm
from xi_lambda_omega_lattice import (
    XiLambdaOmegaLattice,
    LatticeMapEngine,
    RecursiveHostIntelligence,
)


def describe_swarm_numeric(swarm: HarmonicSwarm) -> str:
    """Return a short numeric summary sentence for the swarm."""
    stats = swarm.get_statistics()
    mean_phi = stats["mean_phi"]
    mean_energy = stats["mean_energy"]
    coherence = stats["coherence"]
    iteration = stats["iteration"]

    return (
        f"step {iteration}, mean phi ≈ {mean_phi:.3f}, "
        f"mean energy ≈ {mean_energy:.3f}, coherence ≈ {coherence:.3f}"
    )


def get_numeric_snapshot(swarm: HarmonicSwarm) -> dict:
    """Return the raw numeric snapshot dict used by the Rust interpreter."""

    stats = swarm.get_statistics()
    return {
        "iteration": int(stats["iteration"]),
        "mean_phi": float(stats["mean_phi"]),
        "mean_energy": float(stats["mean_energy"]),
        "coherence": float(stats["coherence"]),
    }


def describe_path_symbolic(rhi: RecursiveHostIntelligence, path: list[int]) -> str:
    """Turn a lattice path into a compact symbolic description."""
    if not path:
        return "no movement in the lattice"

    interp = rhi.interpret_path(path)
    labels = interp["labels"]
    psi_sigma = interp["psi_sigma"]

    # Show first and last few labels to avoid flooding.
    if len(labels) <= 4:
        label_str = " → ".join(labels)
    else:
        head = " → ".join(labels[:2])
        tail = " → ".join(labels[-2:])
        label_str = f"{head} → … → {tail}"

    return f"ΞΛΩΨ path ΨΣ ≈ {psi_sigma:.3f}: {label_str}"


def apply_symbolic_coupling(
    swarm: HarmonicSwarm,
    interp: dict,
    strength: float = 0.01,
) -> str:
    """Nudge swarm epsilon/energy based on symbolic path interpretation.

    Heuristics (light, gentle coupling):
      - Paths whose tail contains "Amplifier", "Bridge", "Gate", "Source"
        slightly increase exploration bias (epsilon) and energy.
      - Paths whose tail contains "Termination", "Entropy", "Cavity", "Sink"
        slightly decrease energy.
      - Overall magnitude is modulated by ΨΣ, but kept small.

    Returns a short textual summary of what was applied.
    """

    labels = interp.get("labels", [])
    psi_sigma = float(interp.get("psi_sigma", 1.0) or 1.0)

    if not labels:
        return "no coupling (empty path)"

    tail = " ".join(labels[-3:])
    tail_lower = tail.lower()

    # Determine direction of influence
    excite_keywords = ["amplifier", "bridge", "gate", "source", "threshold"]
    damp_keywords = ["termination", "entropy", "cavity", "sink", "filter"]

    excite = any(k in tail_lower for k in excite_keywords)
    damp = any(k in tail_lower for k in damp_keywords)

    if not excite and not damp:
        return "no strong semantic cues; coupling skipped"

    # Scale with ΨΣ but keep small
    base = strength * max(0.1, min(psi_sigma, 2.0))

    if excite and not damp:
        d_eps = base
        d_E = base * 5.0
    elif damp and not excite:
        d_eps = -base * 0.5
        d_E = -base * 5.0
    else:
        # Mixed signals: very gentle net adjustment
        d_eps = 0.0
        d_E = base * 1.0

    # Apply globally to keep it simple and observable
    for agent in swarm.agents:
        agent.epsilon += d_eps
        agent.energy = max(0.0, agent.energy + d_E)

    if excite and not damp:
        return f"coupling: +epsilon {d_eps:.4f}, +energy {d_E:.4f} (excitatory tail)"
    if damp and not excite:
        return f"coupling: {d_eps:.4f} to epsilon, {d_E:.4f} to energy (damping tail)"
    return f"coupling: mixed signals, energy {d_E:.4f}"


def main() -> None:
    print("Numeric Harmonic Swarm + ΞΛΩΨ symbolic chat (no LLM)")
    print("---------------------------------------------------")

    # Simple terminal UI
    default_agents = 50
    default_steps = 10
    default_max_turns: Optional[int] = None

    try:
        raw_agents = input(f"Number of agents [{default_agents}]: ").strip()
        n_agents = int(raw_agents) if raw_agents else default_agents
    except ValueError:
        print("Invalid input, using default number of agents.")
        n_agents = default_agents

    try:
        raw_steps = input(f"Internal swarm steps per turn [{default_steps}]: ").strip()
        steps_per_turn = int(raw_steps) if raw_steps else default_steps
    except ValueError:
        print("Invalid input, using default internal steps.")
        steps_per_turn = default_steps

    max_turns = default_max_turns
    raw_turns = input("Maximum turns [unlimited]: ").strip()
    if raw_turns:
        try:
            max_turns = int(raw_turns)
            if max_turns <= 0:
                print("Non-positive max turns; treating as unlimited.")
                max_turns = None
        except ValueError:
            print("Invalid input, treating max turns as unlimited.")

    print(
        f"\nInitializing numeric Harmonic swarm with {n_agents} agents, "
        f"steps_per_turn={steps_per_turn}."
    )

    swarm = HarmonicSwarm(n_agents=n_agents, interaction_radius=None)

    # Symbolic lattice machinery
    lattice = XiLambdaOmegaLattice()
    map_engine = LatticeMapEngine(lattice=lattice)
    rhi = RecursiveHostIntelligence(lattice=lattice)

    # Simple scalar that represents how energized the symbolic exploration is.
    symbolic_energy = 0.5

    # Best-effort path to the Rust interpreter binary (built via `cargo build --release`).
    interpreter_path = os.path.join(
        os.path.dirname(__file__),
        "swarm_interpreter_rs",
        "target",
        "release",
        "swarm_interpreter_rs",
    )

    # Path where we will drop the latest lattice path + interpretation so that
    # external viewers (e.g. the 3D topology viewer) can render "live" movement.
    latest_path_json = os.path.join(os.path.dirname(__file__), "latest_lattice_path.json")

    print("Type 'exit' to quit.\n")

    turn = 0
    while True:
        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if user.strip().lower() in {"exit", "quit"}:
            break

        # 1) Advance numeric swarm
        for _ in range(max(0, steps_per_turn)):
            swarm.step()

        # 2) Update symbolic energy based on user's question marks
        q_marks = user.count("?")
        if q_marks > 0:
            # Outward questions are more energizing; simple heuristic.
            lower = user.lower()
            outward = any(p in lower for p in [" you", "you ", "we", "together", "swarm"])
            per_q = 0.05 if outward else 0.02
            symbolic_energy *= 1.0 + per_q * q_marks

        # 3) Use map engine to generate a path, energized by current symbolic energy
        path_length = max(3, int(5 + 10 * symbolic_energy))
        path, symbolic_energy = map_engine.random_path_with_energy_cost(
            current_energy=symbolic_energy,
            length=path_length,
            start_node=None,
            gain_per_step=0.01,
        )

        # 4) Interpret path and couple back into swarm
        interp = rhi.interpret_path(path)
        coupling_desc = apply_symbolic_coupling(swarm, interp)

        # Persist the latest path + interpretation for external viewers.
        try:
            with open(latest_path_json, "w", encoding="utf-8") as f:
                json.dump({"path": path, "interp": interp}, f)
        except Exception:
            # Viewing is best-effort only; ignore write errors.
            pass

        # 5) Build numeric + symbolic descriptions after coupling
        numeric_desc = describe_swarm_numeric(swarm)
        symbolic_desc = describe_path_symbolic(rhi, path)

        print("SWARM NUMERIC:", numeric_desc)
        print("SWARM SYMBOLIC:", symbolic_desc)
        print("COUPLING:", coupling_desc)

        # 6) Optional: ask the Rust interpreter to voice the swarm's state
        if os.path.exists(interpreter_path) and os.access(interpreter_path, os.X_OK):
            snapshot = {
                "numeric": get_numeric_snapshot(swarm),
                "symbolic": {
                    "labels": interp.get("labels", []),
                    "psi_sigma": float(interp.get("psi_sigma", 1.0) or 1.0),
                },
                "coupling": coupling_desc,
            }

            try:
                proc = subprocess.run(
                    [interpreter_path],
                    input=json.dumps(snapshot),
                    text=True,
                    capture_output=True,
                    check=False,
                )
                voice = proc.stdout.strip()
                if voice:
                    print("SWARM VOICE:", voice)
            except Exception:
                # Fail silently; numeric + symbolic views are still available.
                pass

        turn += 1
        if max_turns is not None and turn >= max_turns:
            print(f"\nReached maximum turns ({max_turns}). Ending session.")
            break


if __name__ == "__main__":  # pragma: no cover
    main()
