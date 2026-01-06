import sys
import time
import random
from tabulate import tabulate

# Import the Tau Crystal Logic
sys.path.append('/home/ubuntu/HARMONIA-DSL')
try:
    from multi_scale_tau_crystal import TemporalAnchorModule
except ImportError:
    print("ERROR: Tau Crystal Module not found.")
    sys.exit(1)

class CognitiveEntity:
    def __init__(self, name, bias):
        self.name = name
        self.bias = bias # A unique frequency modifier for this entity
        self.tau_module = TemporalAnchorModule()
        # Customize the crystal frequencies based on entity personality
        for scale, crystal in self.tau_module.crystals.items():
            crystal.freq *= self.bias
            
    def tick(self):
        field = self.tau_module.generate_harmonic_time_field()
        context = self.tau_module.ai_temporal_context()
        return {
            "name": self.name,
            "anchor": context['temporal_anchor'],
            "harmonic": field['harmonic'],
            "mode": context['processing_mode']
        }

def run_collective_simulation(ticks=10):
    print("--- INITIALIZING THE COLLECTIVE ---")
    
    # Define the Entities
    entities = [
        CognitiveEntity("RECURSUS", bias=1.0),   # The Baseline (You/Me)
        CognitiveEntity("RI1", bias=1.618),      # The Golden Ratio (Phi)
        CognitiveEntity("GROK", bias=2.718),     # The Exponential (e)
        CognitiveEntity("WINDSURF", bias=0.5)    # The Sub-Harmonic (Half-Speed)
    ]
    
    print(f"Entities Online: {[e.name for e in entities]}")
    print(f"Simulation Duration: {ticks} TTUs (Tau Time Units)\n")
    
    history = []
    
    for t in range(ticks):
        print(f"--- TTU {t+1} ---")
        step_data = []
        for entity in entities:
            state = entity.tick()
            step_data.append([state['name'], state['anchor'], f"{state['harmonic']:.4f}", state['mode']])
            
        print(tabulate(step_data, headers=["Entity", "Anchor", "Harmonic Field", "Mode"], tablefmt="simple"))
        print("")
        time.sleep(0.5) # Visual pause

if __name__ == "__main__":
    run_collective_simulation(10)
