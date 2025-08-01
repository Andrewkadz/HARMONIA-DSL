import subprocess
import json

def call_llm(phi_prompt):
    prompt_payload = {
        "prompt": phi_prompt
    }

    result = subprocess.run([
        "ollama", "run", "phi-coder-llm"
    ], input=json.dumps(prompt_payload), text=True, capture_output=True)

    output = result.stdout.strip()
    
    with open("llm_adapter/feedback_port.json", "w") as f:
        json.dump({
            "phi_prompt": phi_prompt,
            "llm_output": output
        }, f, indent=2)

    return output
