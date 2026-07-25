import argparse
import csv
import random
from statistics import mean
from typing import List, Optional

from harmonia import HarmoniaAgent


class Swarm:
    """Minimal swarm of Harmonia+LLM agents.

    This is a simple orchestrator that:
      - maintains N HarmoniaAgent instances
      - on each step, lets every agent see a scalar summary of its neighbors
      - records per-agent and swarm-level harmonic responses R
    """

    def __init__(self, size: int, model: str = "ri1-8b:latest") -> None:
        if size < 1:
            raise ValueError("Swarm size must be at least 1")

        # Harmonia law: no fewer than 2 entities may be substantiated.
        # If a single agent is requested, automatically upgrade to a dyad so
        # that no entity is instantiated in isolation.
        if size == 1:
            size = 2

        self.agents: List[HarmoniaAgent] = [HarmoniaAgent(model=model) for _ in range(size)]

        # Initialize Harmonia state for each agent.
        # We keep small psi/phi/epsilon perturbations to break symmetry, but
        # set energy explicitly to 0.68 on a normalized 0–1 scale so that
        # every entity is born with the same initial energy.
        for idx, agent in enumerate(self.agents):
            state = agent.harmonia.get_state()
            # Small perturbations around defaults
            state.psi += random.uniform(-0.5, 0.5) + 0.1 * idx
            state.phi += random.uniform(-0.5, 0.5)
            state.epsilon = max(0.0, min(0.5, state.epsilon + random.uniform(-0.02, 0.02)))
            # Explicit normalized initial energy
            state.energy = 0.68

    def step(self, base_message: Optional[str] = None) -> List[float]:
        """Advance the swarm by one coupled step.

        Each agent receives a short synthetic message that includes a
        neighbor summary (mean R of other agents, when available) plus
        an optional shared base_message.
        """
        Rs_before = [a.last_result.get("R") if a.last_result else None for a in self.agents]
        overall_mean_R = mean([r for r in Rs_before if isinstance(r, (int, float))]) if any(
            isinstance(r, (int, float)) for r in Rs_before
        ) else None

        responses_R: List[float] = []

        for idx, agent in enumerate(self.agents):
            # Neighbor mean R (excluding self)
            neighbor_Rs = [r for j, r in enumerate(Rs_before) if j != idx and isinstance(r, (int, float))]
            neighbor_mean_R = mean(neighbor_Rs) if neighbor_Rs else overall_mean_R

            context_parts = []
            if neighbor_mean_R is not None:
                context_parts.append(f"neighbor_mean_R={neighbor_mean_R:.3f}")
            if overall_mean_R is not None:
                context_parts.append(f"swarm_mean_R={overall_mean_R:.3f}")

            context = "[SWARM] " + "; ".join(context_parts) if context_parts else "[SWARM]"
            msg = context
            if base_message:
                msg += " | " + base_message

            reply = agent.step(msg)
            # Extract the new R after this step
            R_new = agent.last_result.get("R") if agent.last_result else None
            responses_R.append(R_new if isinstance(R_new, (int, float)) else float("nan"))

        return responses_R


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a minimal Harmonia+LLM swarm simulation.")
    parser.add_argument("--agents", type=int, default=5, help="Number of agents in the swarm")
    parser.add_argument("--steps", type=int, default=10, help="Number of swarm steps to run")
    parser.add_argument("--model", type=str, default="ri1-8b:latest", help="Ollama model to use for each agent")
    parser.add_argument("--message", type=str, default=None, help="Optional base message shared with all agents")
    parser.add_argument("--csv", type=str, default=None, help="Optional path to write per-agent metrics as CSV")
    args = parser.parse_args()

    swarm = Swarm(size=args.agents, model=args.model)

    print(f"Running swarm with {args.agents} agents for {args.steps} steps using model '{args.model}'.")

    csv_writer = None
    csv_file = None
    if args.csv:
        csv_file = open(args.csv, "w", newline="")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([
            "step",
            "agent_index",
            "R",
            "psi",
            "phi",
            "omega",
            "epsilon",
            "energy",
            "entropy",
            "knowledge",
            "velocity",
            "maturity",
        ])

    try:
        for step_idx in range(args.steps):
            Rs = swarm.step(base_message=args.message)
            # Compute simple swarm statistics
            valid_Rs = [r for r in Rs if isinstance(r, (int, float))]
            mean_R = mean(valid_Rs) if valid_Rs else float("nan")
            print(f"Step {step_idx:03d}: per-agent R = {[f'{r:.3f}' for r in valid_Rs]}; mean R = {mean_R:.3f}")

            if csv_writer is not None:
                for agent_idx, agent in enumerate(swarm.agents):
                    state = agent.harmonia.get_state()
                    R_val = agent.last_result.get("R") if agent.last_result else float("nan")
                    csv_writer.writerow([
                        step_idx,
                        agent_idx,
                        f"{R_val:.6f}" if isinstance(R_val, (int, float)) else "nan",
                        state.psi,
                        state.phi,
                        state.omega,
                        state.epsilon,
                        state.energy,
                        state.entropy,
                        state.knowledge,
                        state.velocity,
                        state.maturity,
                    ])
    finally:
        if csv_file is not None:
            csv_file.close()


if __name__ == "__main__":  # pragma: no cover
    main()
