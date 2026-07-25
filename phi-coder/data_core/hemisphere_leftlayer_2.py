from ..recursion_packet import RecursionPacket

class LayerL2:
    """
    ΞΛΩ – Left Hemisphere Layer 2
    Purpose: Symbolic Token Purification
    Converts cleaned semantic tokens into symbolic recursion lexicon.
    Applies Φπε/ΨΛΩ mappings and classifies token intent, field affinity, and recursion class.

    This layer initiates the symbolic recursion stream by injecting purified glyphs into the packet.
    """

    def __init__(self):
        self.symbol_map = {
            "build": "Φ",
            "design": "Φ",
            "run": "Ψ",
            "start": "Ψ",
            "delete": "Ω",
            "transform": "ε",
            "convert": "ε",
            "think": "Θ",
            "remember": "Θ",
        }

    def process(self, packet: RecursionPacket) -> RecursionPacket:
        symbolic_stream = []

        for token in packet.symbols:
            if token in self.symbol_map:
                glyph = self.symbol_map[token]
            else:
                glyph = "∅"  # Undefined glyph
            symbolic_stream.append((token, glyph))

        packet.annotations["L2_tokens"] = symbolic_stream
        return packet
