"""
ΞΛΩ – Node 5L
Execution Vectorizer – Left Hemisphere

Extracts collapse-ready logic nodes from Layer 4 vector.
Converts them into symbolic execution instructions.
Broadcasts seeds to right hemisphere via cluster_bus.
"""

from data_core.cluster_layer_5_8.cluster_bus import ClusterBus


class Node5Left:
    def __init__(self, bus: ClusterBus):
        self.bus = bus

    def process(self, packet):
        logic_vector = packet.annotations.get("L4_logic_vector", [])
        execution_seeds = []

        for node in logic_vector:
            if node.get("entropy_resolution") == "collapse":
                seed = {
                    "symbol": node["symbol"],
                    "operation": f"exec::{node['symbol']}",
                    "depth": node.get("depth", 1),
                    "context": node.get("memory_tag", "root")
                }
                execution_seeds.append(seed)

        # Broadcast execution seeds for 5R and future layers
        self.bus.broadcast("L5_execution_seed", execution_seeds)
        packet.annotations["L5_execution_vector"] = execution_seeds

        # 🔧 Append minimal LLM seed
        if "llm_directives" not in packet.annotations:
            packet.annotations["llm_directives"] = {}

        packet.annotations["llm_directives"]["node_5_left"] = {
            "signal_tag": "L5_execution_seed",
            "summary": "Completed execution seed phase",
            "layer": 5,
            "direction": "Left"
        }

        return packet
