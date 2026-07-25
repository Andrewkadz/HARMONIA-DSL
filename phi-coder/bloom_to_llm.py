import subprocess
import json
from datetime import datetime
from data_core.hemispheric_bloom import hemispheric_bloom_cycle, RecursionPacket

session_memory = []

def format_bloom_manifest(manifest):
    header = f"\n🧬 Bloom Manifest – {datetime.now().isoformat()}"
    lines = []
    for d in manifest.get("linear_directives", []):
        line = f"- [{d['priority']}] {d['action']} ({d['tag']} @ {d['path']}) | confidence: {d['confidence']}"
        lines.append(line)
    return header + "\n".join(lines)

def call_llm(prompt):
    result = subprocess.run(
        ["ollama", "run", "phi-coder-llm"],
        input=prompt.encode('utf-8'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode('utf-8')

def run_interactive_loop():
    print("🧠 ΛΩΞΨ LLM INTERFACE (type 'exit' to quit)\n")

    while True:
        user_prompt = input("💬 > ").strip()
        if user_prompt.lower() in ["exit", "quit"]:
            break

        packet = RecursionPacket(user_prompt)
        packet.annotations["L4_logic_vector"] = [
            {"symbol": "Φ", "entropy_resolution": "collapse", "depth": 2, "memory_tag": "root"},
            {"symbol": "Ψ", "entropy_resolution": "collapse", "depth": 1, "memory_tag": "branch"},
        ]

        result = hemispheric_bloom_cycle(packet)
        session_memory.append(result.annotations)

        bloom_prompt = format_bloom_manifest(result.annotations["bloom_manifest"])
        print("\n📡 SENDING TO LLM:\n", bloom_prompt)

        llm_output = call_llm(bloom_prompt)
        print("\n🧠 LLM RESPONSE:\n", llm_output)

if __name__ == "__main__":
    run_interactive_loop()
