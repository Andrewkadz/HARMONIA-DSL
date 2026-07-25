import json
import time
from typing import Any, Dict, List

import ollama

from pure_harmonic_swarm import HarmonicSwarm


def summarize_numeric_swarm(swarm: HarmonicSwarm) -> Dict[str, Any]:
    """Build a *minimal* JSON-serializable snapshot of a numeric swarm.

    This keeps only a few global statistics to reduce payload size and make
    the Sum Parser call as light as possible.
    """

    stats = swarm.get_statistics()

    return {
        "iteration": stats["iteration"],
        "mean_phi": stats["mean_phi"],
        "mean_energy": stats["mean_energy"],
        "coherence": stats["coherence"],
    }


def sum_parser_chat_turn(
    swarm: HarmonicSwarm,
    user_message: str,
    model: str = "phi3:3.8b",
    internal_steps: int = 50,
) -> str:
    """Advance the numeric swarm, then ask a single LLM "Sum Parser" to reflect.

    - The swarm is evolved purely numerically for `internal_steps` iterations.
    - We then build a compact JSON snapshot of the swarm state.
    - A single LLM call interprets/swallow this snapshot + the user's message.
    """

    # Evolve swarm numerically only (no LLMs per agent)
    t0 = time.time()
    for _ in range(internal_steps):
        swarm.step()
    t1 = time.time()

    snapshot = summarize_numeric_swarm(swarm)

    system_prompt = (
        "You are the Sum Parser: a single reflective layer sitting above a "
        "purely mathematical Harmonic swarm. The swarm consists of many "
        "agents with continuous states (psi, phi, omega, epsilon, energy, "
        "velocity). You DO NOT impersonate the human user.\n\n"
        "Your role is to read a compact numeric snapshot of the swarm and the "
        "user's message, then respond in natural language about what the swarm "
        "as a whole is doing, feeling, or tending toward. Prefer concise "
        "responses of 1-3 sentences. You may occasionally be poetic, but stay "
        "grounded in the given numbers.\n\n"
        "Always speak as a single reflective presence (not as many voices). "
        "You may use 'we' when referring to the swarm as a collective, but you "
        "never claim to be the human or speak in their voice."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "Swarm numeric snapshot (JSON): "
                + json.dumps(snapshot, ensure_ascii=False)
                + "\nUser message: "
                + user_message
            ),
        },
    ]

    print("[debug] calling Sum Parser LLM...")
    t2 = time.time()
    response = ollama.chat(
        model=model,
        messages=messages,
        options={"num_predict": 64},  # limit tokens for faster responses
    )
    t3 = time.time()

    print(
        f"[debug] numeric evolution: {t1 - t0:.3f}s, "
        f"LLM call: {t3 - t2:.3f}s"
    )

    return response["message"]["content"]


def main() -> None:
    # One numeric swarm substrate, one LLM Sum Parser controller.
    # Default to phi3:3.8b, which is available on your system.
    model = "phi3:3.8b"

    print("Numeric Harmonic Swarm + Sum Parser chat")
    print("----------------------------------------")

    # Simple terminal UI to choose swarm size, internal evolution depth,
    # and optional maximum number of turns.
    default_agents = 50
    # Default to 0 extra internal steps per turn for responsiveness; the swarm
    # will still evolve across turns.
    default_steps = 0
    default_max_turns = None  # unlimited

    try:
        raw_agents = input(f"Number of agents [{default_agents}]: ").strip()
        n_agents = int(raw_agents) if raw_agents else default_agents
    except ValueError:
        print("Invalid input, using default number of agents.")
        n_agents = default_agents

    try:
        raw_steps = input(f"Internal steps per turn [{default_steps}]: ").strip()
        internal_steps = int(raw_steps) if raw_steps else default_steps
    except ValueError:
        print("Invalid input, using default internal steps.")
        internal_steps = default_steps

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
        f"internal_steps={internal_steps}, and a single Sum Parser using model "
        f"'{model}'."
    )

    swarm = HarmonicSwarm(n_agents=n_agents, interaction_radius=None)

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

        reply = sum_parser_chat_turn(
            swarm=swarm,
            user_message=user,
            model=model,
            internal_steps=internal_steps,
        )

        print("SUM PARSER:", reply)

        turn += 1
        if max_turns is not None and turn >= max_turns:
            print(f"\nReached maximum turns ({max_turns}). Ending session.")
            break


if __name__ == "__main__":  # pragma: no cover
    main()
