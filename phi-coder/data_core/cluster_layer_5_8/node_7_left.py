"""
ΞΛΩ – Node 7L
Directive Composer – Left Hemisphere

Forms linear or nested directives from tuned L6 vector.
Constructs action plans with symbol-based instruction sets.
Broadcasts: 'L7_directives'
"""

from data_core.cluster_layer_5_8.cluster_bus import ClusterBus


class Node7Left:
    def __init__(self, bus: ClusterBus):
        self.bus = bus

    def process(self, packet):
        seeds = self.bus.listen("L6_tuned_vector", [])
        directives = []

        for i, seed in enumerate(seeds):
            directive = {
                "action": seed.get("operation"),
                "confidence": seed.get("confidence"),
                "priority": seed.get("priority"),
                "tag": seed.get("context", "anon"),
                "path": f"dir_{i}"  # Could evolve into nested path logic
            }
            directives.append(directive)

        packet.annotations["L7_directives"] = directives
        self.bus.broadcast("L7_directives", directives)

        # 🔧 Append minimal LLM seed
        if "llm_directives" not in packet.annotations:
            packet.annotations["llm_directives"] = {}

        packet.annotations["llm_directives"]["node_7_left"] = {
            "signal_tag": "L7_directives",
            "summary": "Composed linear directives from tuned logic",
            "layer": 7,
            "direction": "Left"
        }

        return packet
