from ..recursion_packet import RecursionPacket

class LayerR2:
    """
    ΞΛΩ – Right Hemisphere Layer 2
    Purpose: Recursion Pattern Seeding
    Observes symbolic stream, identifies recursion-worthy symbols, and generates
    recursion seeds with:
    - Depth vector
    - Origin symbol
    - Suggested recursion path

    Output is stored in packet.annotations["R2_seeds"]
    """

    def __init__(self):
        self.seed_depth_map = {
            "Φ": 3,
            "Ψ": 2,
            "ε": 1,
            "Θ": 4,
            "Ω": 0,
        }

    def process(self, packet: RecursionPacket) -> RecursionPacket:
        symbolic_stream = packet.annotations.get("L2_tokens", [])
        seeds = []

        for idx, (token, glyph) in enumerate(symbolic_stream):
            if glyph in self.seed_depth_map:
                seed = {
                    "origin_token": token,
                    "symbol": glyph,
                    "depth": self.seed_depth_map[glyph],
                    "position": idx
                }
                seeds.append(seed)

        packet.annotations["R2_seeds"] = seeds
        return packet
