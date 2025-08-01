"""
ΞΛΩ – Node 8 Core
Bloom Fusion Node

Combines linear and recursive directives into a single harmonic manifest.
Weights total confidence, resolves conflicts, and prepares system for output.

Broadcasts: 'node_8_manifest'
"""

import time
from data_core.cluster_layer_5_8.cluster_bus import ClusterBus


class Node8Core:
    def __init__(self, bus: ClusterBus):
        self.bus = bus

    def process(self, packet):
        linear = self.bus.listen("L7_directives", [])
        recursive = self.bus.listen("R7_recursive_directives", [])

        total_conf = sum(d.get("confidence", 0) for d in linear)
        total_viability = sum(d.get("viability", 0) for d in recursive)
        harmonic_sync = round((total_conf + total_viability) / (len(linear) + len(recursive) + 1), 3)

        bloom_manifest = {
            "linear_directives": linear,
            "recursive_directives": recursive,
            "harmonic_sync": harmonic_sync,
            "manifest_tag": "bloom_core_ready",
            "timestamp": time.time()
        }

        self.bus.broadcast("node_8_manifest", bloom_manifest)
        packet.annotations["bloom_manifest"] = bloom_manifest

        # 🔧 Append minimal LLM seed
        if "llm_directives" not in packet.annotations:
            packet.annotations["llm_directives"] = {}

        packet.annotations["llm_directives"]["node_8_core"] = {
            "signal_tag": "node_8_manifest",
            "summary": "Fused linear and recursive directives into manifest",
            "layer": 8,
            "direction": "Core"
        }

        return packet
