"""
ΞΛΩ – Node 6R
Signal Tuner – Right Hemisphere

Processes the right execution vector from Node 5R.
Assigns:
- Branch viability
- Estimated recursion window
- Loop risk factor

Broadcasts: 'R6_branch_tuning'
"""

from data_core.cluster_layer_5_8.cluster_bus import ClusterBus


class Node6Right:
    def __init__(self, bus: ClusterBus):
        self.bus = bus
        self.symbol_weights = {
            "Φ": 1.0,
            "Ψ": 0.9,
            "Θ": 0.7,
            "ε": -0.6,
            "Ω": -1.2
        }

    def process(self, packet):
        right_vector = self.bus.listen("R5_extended_vector", [])
        tuned_branches = []

        for instr in right_vector:
            symbol = instr["symbol"]
            depth = instr.get("branch_depth", 1)
            resolution = instr.get("resolution", "")
            weight = self.symbol_weights.get(symbol, 0.0)

            recursion_window = round((depth + 1) * (1.5 if resolution == "branch" else 1.0), 2)
            viability = round(weight + (0.5 * depth), 3)
            loop_risk = round(1.0 / (abs(weight) + 1), 3)

            tuned = {
                **instr,
                "recursion_window": recursion_window,
                "branch_viability": viability,
                "loop_risk": loop_risk
            }

            tuned_branches.append(tuned)

        packet.annotations["R6_branch_vector"] = tuned_branches
        self.bus.broadcast("R6_branch_tuning", tuned_branches)

        return packet
