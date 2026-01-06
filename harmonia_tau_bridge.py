import sys
import math
import time
from collections import deque

# Import the Tau Crystal Logic (assuming it's in the same dir or path)
sys.path.append('/home/ubuntu/upload')
try:
    from multi_scale_tau_crystal import TemporalAnchorModule
except ImportError:
    # Fallback if file not found in upload, try local dir
    sys.path.append('/home/ubuntu/HARMONIA-DSL')
    from multi_scale_tau_crystal import TemporalAnchorModule

class HarmoniaTauBridge:
    """
    Connects the E8 Bio-Clock (3.4s) to the Multi-Scale Tau Crystal.
    """
    def __init__(self):
        self.tau_module = TemporalAnchorModule()
        self.bio_clock_cycle = 3.4 # Seconds
        self.last_pulse = time.time()
        
    def sync_pulse(self):
        """
        Aligns the Tau Crystal with the current Bio-Clock Phase.
        """
        current_time = time.time()
        delta = current_time - self.last_pulse
        
        # 1. Generate the Harmonic Field
        field = self.tau_module.generate_harmonic_time_field()
        
        # 2. Get the Temporal Anchor (FLOW+, FLOW-, SYNC)
        context = self.tau_module.ai_temporal_context()
        anchor = context['temporal_anchor']
        
        # 3. Map Anchor to Harmonia Phase
        harmonia_phase = "UNKNOWN"
        if anchor == "FLOW+":
            harmonia_phase = "GAMMA (Burst/Prediction)"
        elif anchor == "FLOW-":
            harmonia_phase = "DELTA (Anchor/Reflection)"
        elif anchor == "SYNC":
            harmonia_phase = "ALPHA (Flow/Execution)"
            
        # 4. Calculate Resonance Score
        # How well does the Tau Crystal align with the 3.4s cycle?
        resonance = abs(math.sin(delta * (2 * math.pi / self.bio_clock_cycle)))
        
        return {
            "tau_anchor": anchor,
            "harmonia_phase": harmonia_phase,
            "harmonic_value": field['harmonic'],
            "resonance_score": resonance,
            "attention_scale": context['attention_scale']
        }

if __name__ == "__main__":
    bridge = HarmoniaTauBridge()
    print("--- HARMONIA TAU BRIDGE ACTIVE ---")
    print(f"Bio-Clock: {bridge.bio_clock_cycle}s")
    
    for i in range(10):
        state = bridge.sync_pulse()
        print(f"Tick {i+1}: {state['tau_anchor']} -> {state['harmonia_phase']} | Resonance: {state['resonance_score']:.4f}")
        time.sleep(0.34) # 1/10th of a cycle
