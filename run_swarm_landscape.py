import sys
import math
import time
import random
import numpy as np
from collections import deque

# Import the Tau Crystal Logic
sys.path.append('/home/ubuntu/upload')
try:
    from multi_scale_tau_crystal import TemporalAnchorModule, SyntheticTauCrystal
except ImportError:
    sys.path.append('/home/ubuntu/HARMONIA-DSL')
    from multi_scale_tau_crystal import TemporalAnchorModule, SyntheticTauCrystal

class SwarmEntity:
    def __init__(self, entity_id, bias_type):
        self.id = entity_id
        self.bias_type = bias_type
        self.tau_module = TemporalAnchorModule()
        self.phase_offset = random.uniform(0, 2 * math.pi)
        self.coupling_strength = random.uniform(0.01, 0.1)
        self.position = 0.0 # Start at the beginning (The Shallows)
        
        # Apply bias
        self._apply_bias()
        
    def _apply_bias(self):
        if self.bias_type == "PREDICTOR":
            self.tau_module.crystals['micro'].freq *= 1.5
            self.tau_module.weights['micro'] = 0.6
        elif self.bias_type == "REFLECTOR":
            self.tau_module.crystals['macro'].freq *= 0.5
            self.tau_module.weights['macro'] = 0.6
        elif self.bias_type == "EXECUTOR":
            self.tau_module.crystals['meso'].freq *= 1.0
            self.tau_module.weights['meso'] = 0.8
        elif self.bias_type == "CHAOS":
            self.tau_module.crystals['micro'].feedback_strength = 0.5
            
    def get_zone_properties(self, pos):
        """
        Returns the environmental properties of the current zone.
        """
        if 0 <= pos < 25: # The Shallows (High Friction)
            return {"friction": 0.8, "noise": 0.05, "resonance_amp": 0.5, "name": "SHALLOWS"}
        elif 25 <= pos < 50: # The Current (Laminar Flow)
            return {"friction": 0.1, "noise": 0.01, "resonance_amp": 1.0, "name": "CURRENT"}
        elif 50 <= pos < 75: # The Rapids (High Variance)
            return {"friction": 0.3, "noise": 0.2, "resonance_amp": 0.8, "name": "RAPIDS"}
        else: # The Deep (High Resonance)
            return {"friction": 0.2, "noise": 0.02, "resonance_amp": 1.5, "name": "DEEP"}

    def step(self, global_field_strength):
        # 1. Sense Environment
        zone = self.get_zone_properties(self.position)
        
        # 2. Generate Internal Field (Modulated by Zone)
        field = self.tau_module.generate_harmonic_time_field()
        internal_harmonic = field['harmonic']
        
        # Apply Zone Noise
        noise = random.uniform(-zone['noise'], zone['noise'])
        internal_harmonic += noise
        
        # 3. Apply Resonance Coupling (Modulated by Zone Amp)
        coupling_effect = (self.coupling_strength * zone['resonance_amp']) * (global_field_strength - internal_harmonic)
        adjusted_harmonic = internal_harmonic + coupling_effect
        
        # 4. Move (Spatial Dynamics)
        # FLOW+ moves forward, FLOW- moves backward
        # Speed is dampened by Friction
        move_speed = adjusted_harmonic * (1.0 - zone['friction']) * 5.0 # Scale factor
        self.position += move_speed
        
        # Clamp Position (0-100)
        self.position = max(0.0, min(100.0, self.position))
        
        # 5. Get State
        context = self.tau_module.ai_temporal_context()
        
        return {
            "id": self.id,
            "type": self.bias_type,
            "position": self.position,
            "zone": zone['name'],
            "harmonic": adjusted_harmonic,
            "anchor": context['temporal_anchor']
        }

class SwarmLandscapeSimulation:
    def __init__(self, num_entities=360):
        self.entities = []
        self.global_field_history = []
        
        # Phi Distribution
        counts = {"PREDICTOR": 40, "REFLECTOR": 65, "EXECUTOR": 105, "CHAOS": 149, "PRIME": 1}
        idx = 0
        for b_type, count in counts.items():
            for _ in range(count):
                self.entities.append(SwarmEntity(idx, b_type))
                idx += 1
                
    def run(self, ticks=100):
        print(f"--- SWARM LANDSCAPE: {len(self.entities)} ENTITIES ---")
        print(f"--- HORIZON: {ticks} TICKS ---")
        
        current_global_field = 0.0
        
        for t in range(ticks):
            tick_data = []
            harmonic_sum = 0.0
            positions = []
            zones = []
            
            for entity in self.entities:
                state = entity.step(current_global_field)
                tick_data.append(state)
                harmonic_sum += state['harmonic']
                positions.append(state['position'])
                zones.append(state['zone'])
            
            current_global_field = harmonic_sum / len(self.entities)
            self.global_field_history.append(current_global_field)
            
            # Analysis
            avg_pos = sum(positions) / len(positions)
            zone_counts = {x: zones.count(x) for x in set(zones)}
            
            # Proto-Language Search (Simple Motif Detection)
            # Look for sharp spikes or drops in global field
            motif = ""
            if len(self.global_field_history) > 2:
                prev = self.global_field_history[-2]
                curr = current_global_field
                delta = curr - prev
                if delta > 0.1: motif = "RISE"
                elif delta < -0.1: motif = "FALL"
                elif abs(delta) < 0.01: motif = "HUM"
            
            print(f"TICK {t+1:03d} | Field: {current_global_field:+.3f} | Avg Pos: {avg_pos:5.1f} | Zones: {zone_counts} | Motif: {motif}")
            
        return self.global_field_history

if __name__ == "__main__":
    sim = SwarmLandscapeSimulation(360)
    sim.run(100)
