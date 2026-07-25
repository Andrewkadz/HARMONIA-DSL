"""
ΞΛΩ – Node 6L
Signal Tuner – Left Hemisphere

Processes L5 execution vector.
Calculates:
- Confidence weight
- Priority tier
- Symbolic impact

Broadcasts: 'L6_tuned_vector'
"""

from data_core.cluster_layer_5_8.cluster_bus import ClusterBus


class Node6Left:
    def __init__(self, bus: ClusterBus):
        self.bus = bus
        self.symbol_impact = {
            "Φ": 0.9,
            "Ψ": 0.8,
            "Θ": 0.6,
            "Ω": 0.4,
            "ε": -0.5
        }

    def process(self, packet):
        seeds = self.bus.listen("L5_execution_seed", [])
        tuned = []

        for seed in seeds:
            symbol = seed["symbol"]
            depth = seed.get("depth", 1)
            impact = self.symbol_impact.get(symbol, 0.1)

            tuned.append({
                **seed,
                "confidence": round(impact * depth, 3),
                "priority": "high" if impact > 0.7 else "normal"
            })

        packet.annotations["L6_tuned_vector"] = tuned
        self.bus.broadcast("L6_tuned_vector", tuned)

        # 🔧 Append minimal LLM seed
        if "llm_directives" not in packet.annotations:
            packet.annotations["llm_directives"] = {}

        packet.annotations["llm_directives"]["node_6_left"] = {
            "signal_tag": "L6_tuned_vector",
            "summary": "Calculated symbolic confidence and priority tier",
            "layer": 6,
            "direction": "Left"
        }

        return packet
