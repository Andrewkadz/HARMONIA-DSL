from ..recursion_packet import RecursionPacket

class LayerL1:
    """
    ΞΛΩ – Left Hemisphere Layer 1
    Purpose: Noise filtration from prompt input.
    Operates as pre-symbolic stabilizer — removes meaningless filler,
    filters redundancy, stabilizes signal for recursion entry.

    This layer ensures only coherent patterns enter symbolic sequence.
    """

    def __init__(self):
        self.noise_tokens = {"uh", "um", "like", "...", "actually", "basically"}

    def process(self, packet: RecursionPacket) -> RecursionPacket:
        clean_symbols = [
            token for token in packet.symbols
            if token not in self.noise_tokens and len(token.strip()) > 1
        ]

        packet.symbols = clean_symbols
        packet.annotations["L1_noise_removed"] = True
        return packet
