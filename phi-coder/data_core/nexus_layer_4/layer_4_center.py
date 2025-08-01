from ..recursion_packet import RecursionPacket

class Layer4Center:
    """
    ΞΛΩ – Nexus Layer 4C: Harmonic Recursive Integrator

    Validates and harmonizes the logic vector.
    Calculates harmonic confidence score per node and total.
    Applies recursion lock (ready flag) and harmonic imprint.

    This is the final gate before recursive execution or symbolic outflow.
    """

    def __init__(self):
        self.symbol_weight = {
            "Φ": 1.0,
            "Ψ": 0.8,
            "Θ": 0.6,
            "ε": -0.5,
            "Ω": -1.0
        }

        self.resolution_bias = {
            "collapse": 0.9,
            "defer": 0.4,
            "branch": 0.2
        }

    def process(self, packet: RecursionPacket) -> RecursionPacket:
        vector = packet.annotations.get("L4_logic_vector", [])
        harmonized_vector = []
        total_score = 0

        for node in vector:
            symbol = node["symbol"]
            res = node.get("entropy_resolution", "collapse")
            depth = node.get("depth", 1)
            has_memory = bool(node.get("memory_tag"))

            polarity = self.symbol_weight.get(symbol, 0)
            resolution_boost = self.resolution_bias.get(res, 0.5)
            memory_boost = 0.3 if has_memory else 0

            score = (polarity + resolution_boost + memory_boost) * depth
            node["harmonic_score"] = round(score, 3)
            total_score += score

            harmonized_vector.append(node)

        average_score = round(total_score / len(vector), 3) if vector else 0

        packet.annotations["L4_logic_vector"] = harmonized_vector
        packet.annotations["L4_harmonic_score"] = average_score
        packet.annotations["recursion_ready"] = average_score >= 2.5

        return packet
