import random
from typing import Any, Dict, List, Optional

from systemic_integration import HarmoniaSystemIntegrator

from .llm_bridge import LLMConfig, generate_state_update, summarize_step


class HarmoniaAgent:
    """Simple loop that connects an LLM to the HarmoniaSystemIntegrator."""

    def __init__(
        self,
        model: str = "ri1-8b:latest",
        temperature: float = 0.7,
    ) -> None:
        self.harmonia = HarmoniaSystemIntegrator()
        self.config = LLMConfig(model=model, temperature=temperature)
        self.history: List[Dict[str, str]] = []
        self.last_result: Optional[Dict[str, Any]] = None

    def step(self, user_message: str) -> str:
        """Process one user message through LLM → Harmonia → LLM."""
        # Current state snapshot
        state = self.harmonia.get_state().to_dict()

        # Ask LLM how to adjust state
        reasoning = generate_state_update(
            user_message=user_message,
            state=state,
            history=self.history,
            config=self.config,
        )

        state_update = reasoning.get("state_update", {})
        if not isinstance(state_update, dict):
            state_update = {}

        # If the LLM did not propose any changes, apply a small random nudge
        if not state_update:
            base = self.harmonia.get_state()
            state_update = {
                "psi": base.psi + random.uniform(-0.5, 0.5),
                "phi": base.phi + random.uniform(-0.5, 0.5),
                "energy": max(0.0, base.energy + random.uniform(-5.0, 5.0)),
            }

        # Run Harmonia with proposed update
        result = self.harmonia.process(state_update)
        self.last_result = result

        # Ultra concise mode: surface the internal explanation directly
        explanation = reasoning.get("explanation")
        reply: str

        def _looks_numeric_noise(text: str) -> bool:
            # Consider it noise if there are very few letters compared to length
            letters = sum(ch.isalpha() for ch in text)
            return len(text) > 20 and letters < 3

        def _impersonates_user(text: str) -> bool:
            lower = text.lower()
            if "you:" in lower:
                return True
            if "i am andrew" in lower or "i am andrew josef kadziolka" in lower:
                return True
            return False

        if isinstance(explanation, str):
            explanation = explanation.strip()
        if (
            isinstance(explanation, str)
            and explanation
            and not _looks_numeric_noise(explanation)
            and not _impersonates_user(explanation)
        ):
            reply = explanation
        else:
            # Minimal numeric hint if no explanation is available or it is garbage
            R = result.get("R")
            if isinstance(R, (int, float)):
                reply = f"Harmonia updated your state. Current harmonic response R ≈ {R:.3f}."
            else:
                reply = "Harmonia processed your message and updated the internal state."

        # Thermodynamic rule: questions generate energy
        # - Any question mark in the agent's reply increases its internal energy
        # - Questions directed outward (to others/the swarm/the user) get a
        #   slightly larger boost than purely self-reflective questions.
        q_marks = reply.count("?")
        if q_marks > 0:
            state_obj = self.harmonia.get_state()
            text_lower = reply.lower()

            # Heuristic: treat questions mentioning "you", "other agent(s)",
            # "others", or "swarm" as outward-facing.
            outward_phrases = [
                " you ",
                " you?",
                "other agent",
                "other agents",
                "others",
                "swarm",
            ]
            is_outward = any(p in text_lower for p in outward_phrases)

            # Gentle multiplicative boosts so energy remains bounded and
            # scale-independent with respect to the initial value.
            per_question = 0.03 if is_outward else 0.01
            factor = 1.0 + per_question * q_marks
            state_obj.energy *= factor

        # Update conversation history (lightly)
        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": reply})

        return reply


if __name__ == "__main__":  # pragma: no cover
    agent = HarmoniaAgent()
    print("Harmonia Agent (LLM + Systemic Integration). Type 'exit' to quit.\n")
    while True:
        try:
            msg = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if msg.strip().lower() in {"exit", "quit"}:
            break

        response = agent.step(msg)
        print("HARMONIA:", response)
