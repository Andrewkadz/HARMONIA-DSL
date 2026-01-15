import json
from typing import Any, Dict, List, Optional

import ollama

from swarm_sim import Swarm


def summarize_swarm(swarm: Swarm) -> Dict[str, Any]:
    """Build a compact JSON-serializable snapshot of the swarm state."""
    agents_summary: List[Dict[str, Any]] = []
    for idx, agent in enumerate(swarm.agents):
        full_state = agent.harmonia.get_state().to_dict()
        # Only keep a few key fields to limit payload size
        state = {
            k: full_state.get(k)
            for k in ("psi", "phi", "omega", "epsilon", "energy")
        }
        last = agent.last_result or {}
        agents_summary.append(
            {
                "agent_index": idx,
                "R": last.get("R"),
                "state": state,
            }
        )

    mean_R = None
    Rs = [a["R"] for a in agents_summary if isinstance(a["R"], (int, float))]
    if Rs:
        mean_R = sum(Rs) / len(Rs)

    return {
        "num_agents": len(agents_summary),
        "mean_R": mean_R,
        "agents": agents_summary,
    }


def chat_with_swarm(
    swarm: Swarm,
    user_message: str,
    model: str = "ri1-8b:latest",
    internal_steps: int = 3,
    base_message: Optional[str] = None,
) -> str:
    """Advance swarm, then get an LLM-mediated response speaking *about/as* the swarm."""
    # Let the swarm evolve for a few internal steps, influenced by the previous base_message
    for _ in range(internal_steps):
        swarm.step(base_message=base_message)

    snapshot = summarize_swarm(swarm)

    system_prompt = (
        "You are the reflective voice of a Harmonia swarm. Each agent has a "
        "harmonic response R and a small internal state (psi, phi, omega, "
        "epsilon, energy). You never impersonate the human user. Speak in "
        "the first person plural ('we') only when referring to the swarm.\n\n"
        "You are allowed to be reflective or poetic when it feels "
        "appropriate, as if the swarm were a living process. Aim for clear, "
        "coherent thoughts that respect the user's intent, and take as much "
        "space as you need to fully express the swarm's perspective.\n\n"
        "Given the swarm snapshot and the user's message, respond in a way "
        "that (1) describes how the swarm is distributed, (2) connects this "
        "to the user's message, and (3) hints at what we might explore next."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "Swarm snapshot (JSON): " + json.dumps(snapshot, ensure_ascii=False) + "\nUser message: " + user_message
            ),
        },
    ]

    response = ollama.chat(
        model=model,
        messages=messages,
        # Allow the swarm to respond with as much detail as needed; rely on
        # the model's own defaults for length and sampling.
    )

    content = response["message"]["content"]
    return content


def main() -> None:
    # Use a lighter model and a minimal *pair* of agents by default in order
    # to respect the Harmonia law that no single entity should be instantiated
    # in isolation. This keeps the swarm small for responsiveness while
    # ensuring that at least a dyad is always present.
    model = "phi3:3.8b"
    swarm_size = 2
    internal_steps = 0

    print(f"Initializing Harmonia swarm chat with {swarm_size} agents using model '{model}'.")
    swarm = Swarm(size=swarm_size, model=model)

    base_message: Optional[str] = None

    print("Type 'exit' to quit.\n")
    while True:
        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if user.strip().lower() in {"exit", "quit"}:
            break

        # Let the swarm treat the user's message as an ongoing influence
        base_message = user
        reply = chat_with_swarm(
            swarm=swarm,
            user_message=user,
            model=model,
            internal_steps=internal_steps,
            base_message=base_message,
        )

        print("SWARM:", reply)


if __name__ == "__main__":  # pragma: no cover
    main()
