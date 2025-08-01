# cluster_bus.py

class ClusterBus:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.log = []

    def transmit(self, packet, layer_id, direction, transform_fn=None):
        # Safety checks
        if not hasattr(packet, 'annotations') or not isinstance(packet.annotations, dict):
            raise ValueError("Invalid packet: Missing annotations dictionary")

        # Regulatory check: depth limit (e.g., 13 max)
        depth = packet.annotations.get("recursion_depth", 0)
        if depth > 13:
            packet.annotations["trace"].append(f"⚠ Bus halted: Recursion depth {depth} exceeded at Layer {layer_id}")
            return packet

        # Optional transformation hook
        if transform_fn:
            packet = transform_fn(packet)

        # Log and tag trace
        entry = f"✅ Bus routed: Layer {layer_id} → {direction} | Depth={depth}"
        packet.annotations["trace"].append(entry)
        self.log.append(entry)

        # Verbose console output
        if self.verbose:
            print("[ClusterBus]", entry)

        return packet

    def feedback_loop(self, packet, strength=1.0):
        """ Optionally return packet to previous node with feedback modulation """
        packet.annotations["trace"].append(f"↩ Feedback loop initiated (strength={strength})")
        return packet

    def halt(self, packet, reason):
        """ Mark packet as halted with reason """
        packet.annotations["trace"].append(f"⛔ HALT: {reason}")
        return packet
    def broadcast(self, tag, payload, packet=None):
        """
        Broadcast a symbolic payload across the recursion field.
        Optionally records to the trace if packet is provided.
        """
        signal = f"📡 Broadcast: {tag} → {payload}"
        self.log.append(signal)
        if packet is not None:
            packet.annotations["trace"].append(signal)
        if self.verbose:
            print("[ClusterBus]", signal)
        return signal
    def listen(self, tag, default=None):
        """
        Retrieve the latest broadcast matching the tag.
        Returns the payload (if encoded) or fallback default.
        """
        for signal in reversed(self.log):
            if signal.startswith(f"📡 Broadcast: {tag} → "):
                try:
                    payload = signal.split("→", 1)[1].strip()
                    return eval(payload) if payload else default
                except:
                    return default
        return default
