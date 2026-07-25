"""
ΞΛΩ – Node 7R
Directive Composer – Right Hemisphere

Transforms tuned right vector into recursion-ready directive trees.
Encodes:
- Recursion window
- Loop control
- Symbolic pathing and signatures

Broadcasts: 'R7_recursive_directives'
"""

from data_core.cluster_layer_5_8.cluster_bus import ClusterBus


class Node7Right:
    def __init__(self, bus: ClusterBus):
        self.bus = bus

    def process(self, packet):
        branches = self.bus.listen("R6_branch_tuning", [])
        recursive_directives = []

        for i, branch in enumerate(branches):
            directive = {
                "symbol": branch["symbol"],
                "type": branch["resolution"],
                "window": branch["recursion_window"],
                "viability": branch["branch_viability"],
                "loop_risk": branch["loop_risk"],
                "path": f"rdir_{i}",
                "containment": "echo_dampen" if branch["loop_risk"] > 0.7 else "none",
                "origin": branch.get("origin", "core")
            }
            recursive_directives.append(directive)

        packet.annotations["R7_recursive_directives"] = recursive_directives
        self.bus.broadcast("R7_recursive_directives", recursive_directives)

        # 🔧 Append minimal LLM seed
        if "llm_directives" not in packet.annotations:
            packet.annotations["llm_directives"] = {}

        packet.annotations["llm_directives"]["node_7_right"] = {
            "signal_tag": "R7_recursive_directives",
            "summary": "Generated recursion trees and loop control structures",
            "layer": 7,
            "direction": "Right"
        }

        return packet
