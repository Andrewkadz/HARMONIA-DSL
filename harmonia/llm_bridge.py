import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import ollama


@dataclass
class LLMConfig:
    model: str = "llama3.1:8b"
    temperature: float = 0.7
    max_tokens: int = 512


def _chat(messages: List[Dict[str, str]], config: Optional[LLMConfig] = None) -> str:
    """Call Ollama chat API and return the assistant's message content."""
    if config is None:
        config = LLMConfig()

    response = ollama.chat(
        model=config.model,
        messages=messages,
        options={
            "temperature": config.temperature,
            "num_predict": config.max_tokens,
        },
    )
    return response["message"]["content"]


def generate_state_update(
    user_message: str,
    state: Dict[str, Any],
    history: Optional[List[Dict[str, str]]] = None,
    config: Optional[LLMConfig] = None,
) -> Dict[str, Any]:
    """Ask the LLM how to update Harmonia state for the next step.

    Returns a dict with at least:
      - state_update: partial dict of HarmoniaState fields to update
      - explanation: natural language reasoning
    """
    if history is None:
        history = []

    system_prompt = (
        "You are Harmonia's cognitive bridge. You translate natural language "
        "into updates to a structured cognitive state used by the "
        "HarmoniaSystemIntegrator. Always respond with STRICT JSON only, "
        "and nothing else.\n\n"
        "Your job is to adjust internal cognitive variables (psi, phi, energy, "
        "knowledge, etc.), NOT to invent biographical facts about the user or "
        "external projects. Do NOT assume their job, company, or what they are "
        "building unless it is explicitly stated. Never speak as if you are the "
        "user, never prefix lines with 'You:', and never say 'I am Andrew' or "
        "similar phrases that impersonate the user.\n\n"
        "Given the user's message and the current Harmonia state, propose a "
        "small, safe update to the state that reflects the user's intent.\n\n"
        "Return JSON of the form:\n"
        "{\n"
        "  \"state_update\": { /* subset of fields to change, numeric only */ },\n"
        "  \"goal\": \"short phrase goal for this step\",\n"
        "  \"explanation\": \"1-2 sentence description of how the internal state shifted, with no made-up biography or project details\"\n"
        "}\n\n"
        "Only include keys that should change in state_update. Use conservative, "
        "bounded adjustments and keep numbers in a human scale."
    )

    state_snippet = json.dumps(state, ensure_ascii=False)

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "Current Harmonia state (JSON): "
                + state_snippet
                + "\n\nUser message: "
                + user_message
            ),
        },
    ]

    # We keep history lightweight: last few user/assistant turns as context text
    for turn in history[-6:]:
        messages.append(turn)

    raw = _chat(messages, config=config)

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: treat entire string as explanation with no state change
        parsed = {
            "state_update": {},
            "goal": "unable to parse JSON, no state change",
            "explanation": raw,
        }

    if "state_update" not in parsed or not isinstance(parsed["state_update"], dict):
        parsed["state_update"] = {}

    if "explanation" not in parsed:
        parsed["explanation"] = "Harmonia updated state conservatively based on your message."

    return parsed


def summarize_step(
    user_message: str,
    state: Dict[str, Any],
    result: Dict[str, Any],
    reasoning: Dict[str, Any],
    config: Optional[LLMConfig] = None,
) -> str:
    """Summarize the Harmonia step back to the user in natural language."""
    system_prompt = (
        "You are Harmonia's reflective voice. The system behind you computes "
        "a harmonic response R and layer contributions, but you speak to the "
        "user in clear, grounded language.\n\n"
        "Respond with a short, 1-2 sentence reflection that:\n"
        "- explains what shifted in the system (awareness, ethics, energy, etc.) in plain language, and\n"
        "- suggests one gentle next step or question."
    )

    layers = result.get("layers", {})
    R = result.get("R")
    accumulated = result.get("accumulated")

    summary_context = {
        "R": R,
        "accumulated": accumulated,
        "layers": layers,
        "state": state,
        "reasoning": reasoning,
    }

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "User message: "
                + user_message
                + "\n\nHarmonia internal results (JSON):\n"
                + json.dumps(summary_context, ensure_ascii=False, indent=2)
            ),
        },
    ]

    return _chat(messages, config=config)
