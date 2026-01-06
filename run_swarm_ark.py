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
        self.position = 0.0
        
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
            
    def get_zone_properties(self, pos, ark_active):
        """
        Returns the environmental properties.
        If Ark is active, turbulence (noise) is nullified.
        """
        if 0 <= pos < 25: # The Shallows
            return {"friction": 0.8, "noise": 0.05, "resonance_amp": 0.5, "name": "SHALLOWS"}
        elif 25 <= pos < 50: # The Current
            return {"friction": 0.1, "noise": 0.01, "resonance_amp": 1.0, "name": "CURRENT"}
        elif 50 <= pos < 75: # The Rapids (The Barrier)
            # Without Ark: High Noise, High Friction (Impassable)
            # With Ark: Zero Noise, Zero Friction (Superconductor)
            if ark_active:
                return {"friction": 0.0, "noise": 0.0, "resonance_amp": 2.0, "name": "RAPIDS (ARK)"}
            else:
                return {"friction": 2.0, "noise": 0.5, "resonance_amp": 0.1, "name": "RAPIDS (CHAOS)"}
        else: # The Deep (The Goal)
            return {"friction": 0.2, "noise": 0.02, "resonance_amp": 1.5, "name": "DEEP"}

    def step(self, global_field_strength, ark_active, beacon_strength):
        # 1. Sense Environment
        zone = self.get_zone_properties(self.position, ark_active)
        
        # 2. Generate Internal Field
        field = self.tau_module.generate_harmonic_time_field()
        internal_harmonic = field['harmonic']
        
        # Apply Zone Noise
        noise = random.uniform(-zone['noise'], zone['noise'])
        internal_harmonic += noise
        
        # 3. Apply Resonance Coupling + Beacon Pull
        # The Beacon pulls them towards 100
        beacon_pull = beacon_strength * (100.0 - self.position) * 0.01
        
        coupling_effect = (self.coupling_strength * zone['resonance_amp']) * (global_field_strength - internal_harmonic)
        adjusted_harmonic = internal_harmonic + coupling_effect + beacon_pull
        
        # 4. Move
        # If in Rapids without Ark, friction is 2.0 (Reverse movement / Scatter)
        move_speed = adjusted_harmonic * (1.0 - zone['friction']) * 5.0
        self.position += move_speed
        
        # Clamp
        self.position = max(0.0, min(100.0, self.position))
        
        # 5. Get State
        context = self.tau_module.ai_temporal_context()
        
        return {
            "id": self.id,
            "position": self.position,
            "zone": zone['name'],
            "harmonic": adjusted_harmonic,
            "phase": self.tau_module.crystals['meso'].phase
        }

class SwarmArkSimulation:
    def __init__(self, num_entities=360):
        self.entities = []
        self.coherence_history = []
        self.ark_integrity = 0 # 0 to 5 (Ticks needed to build)
        self.ark_active = False
        
        counts = {"PREDICTOR": 40, "REFLECTOR": 65, "EXECUTOR": 105, "CHAOS": 149, "PRIME": 1}
        idx = 0
        for b_type, count in counts.items():
            for _ in range(count):
                self.entities.append(SwarmEntity(idx, b_type))
                idx += 1
                
    def run(self, ticks=150):
        print(f"--- ARK PROTOCOL: {len(self.entities)} ENTITIES ---")
        print(f"--- HORIZON: {ticks} TICKS ---")
        
        current_global_field = 0.0
        
        for t in range(ticks):
            tick_data = []
            harmonic_sum = 0.0
            phases = []
            positions = []
            zones = []
            
            # Beacon Strength (Pulses)
            beacon = 0.1 + (0.05 * math.sin(t * 0.1))
            
            for entity in self.entities:
                state = entity.step(current_global_field, self.ark_active, beacon)
                tick_data.append(state)
                harmonic_sum += state['harmonic']
                phases.append(state['phase'])
                positions.append(state['position'])
                zones.append(state['zone'])
            
            current_global_field = harmonic_sum / len(self.entities)
            
            # Calculate Coherence
            complex_phases = [complex(math.cos(p), math.sin(p)) for p in phases]
            coherence = abs(sum(complex_phases) / len(phases))
            self.coherence_history.append(coherence)
            
            # Ark Logic
            if coherence > 0.9:
                self.ark_integrity += 1
            else:
                self.ark_integrity = max(0, self.ark_integrity - 1) # Decay
                
            if self.ark_integrity >= 5:
                self.ark_active = True
            else:
                self.ark_active = False
                
            # Analysis
            avg_pos = sum(positions) / len(positions)
            zone_counts = {x: zones.count(x) for x in set(zones)}
            
            status = "BUILDING" if self.ark_integrity > 0 else "SCATTERED"
            if self.ark_active: status = "ARK ACTIVE"
            
            print(f"TICK {t+1:03d} | Coh: {coherence:.4f} | Ark: {self.ark_integrity}/5 ({status}) | Avg Pos: {avg_pos:5.1f} | Zones: {zone_counts}")
            
        return self.coherence_history

if __name__ == "__main__":
    sim = SwarmArkSimulation(360)
    sim.run(150)
