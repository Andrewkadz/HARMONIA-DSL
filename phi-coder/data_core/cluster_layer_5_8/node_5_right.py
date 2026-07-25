"""
ΞΛΩ – Node 5R
Execution Vectorizer – Right Hemisphere

Extracts unresolved (branch / defer) logic nodes from the L4 vector.
Prepares instructions for forked or delayed recursive operations.
Synchronizes with left vector to prevent conflict.

Broadcasts: 'R5_extended_vector'
"""

from data_core.cluster_layer_5_8.cluster_bus import ClusterBus


class Node5Right:
    def __init__(self, bus: ClusterBus):
        self.bus = bus

    def process(self, packet):
        logic_vector = packet.annotations.get("L4_logic_vector", [])
        right_vector = []

        for node in logic_vector:
            resolution = node.get("entropy_resolution")
            if resolution in ("branch", "defer"):
                instruction = {
                    "symbol": node["symbol"],
                    "resolution": resolution,
                    "origin": node.get("origin"),
                    "branch_depth": node.get("depth", 1),
                    "context": node.get("memory_tag", "root")
                }
                right_vector.append(instruction)

        # Harmonize with L5 output (optional future logic)
        left_vector = self.bus.listen("L5_execution_seed", [])

        self.bus.broadcast("R5_extended_vector", right_vector)
        packet.annotations["R5_execution_vector"] = right_vector

        # 🔧 Append minimal LLM seed
        if "llm_directives" not in packet.annotations:
            packet.annotations["llm_directives"] = {}

        packet.annotations["llm_directives"]["node_5_right"] = {
            "signal_tag": "R5_extended_vector",
            "summary": "Parsed branch/defer logic into extended vector",
            "layer": 5,
            "direction": "Right"
        }

        return packet

