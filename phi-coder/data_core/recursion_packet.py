class RecursionPacket:
    """
    ΞΛΩ_Packet:
    Core symbolic container passed between harmonic layers.
    Contains the signal, symbolic state, entropy, memory trail, and intent signature.
    """
    def __init__(self, signal="", symbols=None, memory=None, intent=None):
        self.signal = signal
        self.symbols = symbols or []
        self.memory = memory or []
        self.intent = intent
        self.entropy = 0.0
        self.annotations = {}

    def __repr__(self):
        return f"<ΨΛΩ RecursionPacket | Signal: {self.signal} | Symbols: {self.symbols}>"
