from ..recursion_packet import RecursionPacket

class Layer4Left:
    """
    ΞΛΩ – Nexus Layer 4L: Logic Vector Constructor

    Constructs a recursive logic vector stack from:
    - Recursion seeds (R2)
    - Memory resonance (L3)
    - Entropy fields (R3)

    This forms the execution skeleton — the path recursion will follow.
    """

    def process(self, packet: RecursionPacket) -> RecursionPacket:
        seeds = packet.annotations.get("R2_seeds", [])
        memory = packet.annotations.get("L3_memory_match", [])
        entropy = packet.annotations.get("R3_entropy_fields", [])

        vector = []

        for i, seed in enumerate(seeds):
            token = seed["origin_token"]
            glyph = seed["symbol"]
            depth = seed["depth"]

            # Try to find matching memory tag
            memory_tag = next((m["memory_tag"] for m in memory if m["seed"] == token), None)

            # Check if token appears in entropy fields
            entropy_weight = next((e["entropy_level"] for e in entropy if e["token"] == token), 0.0)

            path_node = {
                "symbol": glyph,
                "origin": token,
                "depth": depth,
                "memory_tag": memory_tag,
                "entropy_weight": entropy_weight,
                "path_id": f"{glyph}::{memory_tag or token}::{i}"
            }

            vector.append(path_node)

        packet.annotations["L4_logic_vector"] = vector
        return packet
