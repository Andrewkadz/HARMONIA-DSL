import sys
import os
import subprocess
from datetime import datetime

# 🔧 Ensure correct path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
cluster_dir = os.path.join(current_dir, 'cluster_layer_5_8')
sys.path.append(cluster_dir)

# ✅ Imports
from data_core.cluster_layer_5_8.cluster_bus import ClusterBus
from node_5_left import Node5Left
from node_5_right import Node5Right
from node_6_left import Node6Left
from node_6_right import Node6Right
from node_7_left import Node7Left
from node_7_right import Node7Right
from node_8_core import Node8Core

# 📦 Recursion packet structure
class RecursionPacket:
    def __init__(self, prompt):
        self.annotations = {
            "prompt": prompt,
            "recursion_depth": 0,
            "trace": []
        }

# 🌱 Bloom cycle through nodes 5–8
def hemispheric_bloom_cycle(packet):
    bus = ClusterBus(verbose=True)

    # Layer 5
    packet = Node5Left(bus).process(packet)
    packet = Node5Right(bus).process(packet)

    # Layer 6
    packet = Node6Left(bus).process(packet)
    packet = Node6Right(bus).process(packet)

    # Layer 7
    packet = Node7Left(bus).process(packet)
    packet = Node7Right(bus).process(packet)

    # Layer 8
    packet = Node8Core(bus).process(packet)

    return packet

# 💬 Convert manifest into a language prompt
def send_to_llm(manifest):
    prompt = f"🧬 Bloom Manifest – {datetime.now().isoformat()} –\n"
    for d in manifest.get("linear_directives", []):
        prompt += f"[{d['priority']}] {d['action']} ({d['tag']} @ {d['path']}) | confidence: {d['confidence']}\n"

    print("\n📡 SENDING TO LLM:\n")
    print(prompt)

    try:
        result = subprocess.run(
            ["ollama", "run", "phi", prompt],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"[LLM Error] {str(e)}"

# 🔁 Execution entry point
if __name__ == "__main__":
    while True:
        prompt = input("\n💬 > ")
        if prompt.strip().lower() in ["exit", "quit"]:
            break

        packet = RecursionPacket(prompt)

        # 🧬 Inject a mock L4 vector for testing
        packet.annotations["L4_logic_vector"] = [
            {"symbol": "Φ", "entropy_resolution": "collapse", "depth": 2, "memory_tag": "root"},
            {"symbol": "Ψ", "entropy_resolution": "collapse", "depth": 1, "memory_tag": "branch"},
            {"symbol": "Θ", "entropy_resolution": "none", "depth": 1, "memory_tag": "inert"},
        ]

        result = hemispheric_bloom_cycle(packet)
        result.annotations["L4_logic_vector"] = packet.annotations["L4_logic_vector"]

        print("\n🌸 Bloom Manifest Output:")
        print(result.annotations.get("bloom_manifest", "No manifest generated."))

        print("\n📜 Trace Path:")
        for step in result.annotations.get("trace", []):
            print("-", step)

        print("\n🧠 LLM RESPONSE:\n")
        response = send_to_llm(result.annotations.get("bloom_manifest", {}))
        print(f"💬 {response}")
