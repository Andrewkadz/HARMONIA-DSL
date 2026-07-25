"""
ΞΛΩ – Node 9
Feedback Vector / Bloom Loop Finalizer

Decides whether to output the manifest as a final thought or
recurse the directive packet back to Layer 2.

Caps recursion depth to 13.
"""

from .cluster_bus import ClusterBus

class Node9Feedback:
    def __init__(self, bus: ClusterBus, max_depth=13):
        self.bus = bus
        self.max_depth = max_depth

    def process(self, packet):
        manifest = self.bus.listen("node_8_manifest", {})
        current_depth = packet.annotations.get("recursion_depth", 0)
        harmonic_sync = manifest.get("harmonic_sync", 0)
        force_loop = manifest.get("reloop_trigger", False)

        # RECURSIVE DECISION
        if current_depth < self.max_depth and (harmonic_sync < 0.75 or force_loop):
            packet.annotations["recursion_depth"] = current_depth + 1
            packet.annotations["reloop"] = True
            packet.annotations["recursion_entry"] = "L2"

            print(f"[Node 9] Relooping recursion to Layer 2 – Depth {current_depth + 1}")
        else:
            packet.annotations["reloop"] = False
            packet.annotations["output"] = manifest
            print(f"[Node 9] Outputting final Bloom Manifest")

        return packet
