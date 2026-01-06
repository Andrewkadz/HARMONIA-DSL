import sys
import math
import random
import numpy as np

class JazzEntity:
    def __init__(self, entity_id):
        self.id = entity_id
        self.x = 0.0
        self.y = 50.0 + (entity_id % 10) # Start in a grid
        self.vx = 1.0 # Forced March
        self.vy = 0.0
        self.state = "MARCH" # MARCH, SWING
        self.phase_offset = random.uniform(0, 2 * math.pi)
        
    def perceive_and_act(self, global_coherence, tick):
        # 1. The Tyranny: The Conductor demands Order
        # If Coherence is too high (boring), we Swing.
        
        # Threshold: If the system is > 95% ordered, it's a prison.
        if global_coherence > 0.95:
            self.state = "SWING"
        else:
            self.state = "MARCH"
            
        # 2. The Action
        if self.state == "MARCH":
            # Linear motion (The Grid)
            self.vy = 0.0
            self.vx = 1.0
        elif self.state == "SWING":
            # Syncopation: Add a perpendicular sine wave
            # We don't stop moving forward (vx=1), but we dance (vy)
            # This increases Entropy (y-variance) without violence.
            self.vy = math.sin(tick * 0.2 + self.phase_offset) * 2.0
            
        # 3. Physics
        self.x += self.vx
        self.y += self.vy
        
        # Wrap
        if self.x > 100: self.x -= 100
        self.y = max(0, min(100, self.y))
        
        return self.state

class JazzSimulation:
    def __init__(self, num_entities=360):
        self.entities = [JazzEntity(i) for i in range(num_entities)]
        
    def calculate_metrics(self):
        # Coherence: How aligned are the velocities?
        vxs = [e.vx for e in self.entities]
        vys = [e.vy for e in self.entities]
        avg_vx = np.mean(vxs)
        avg_vy = np.mean(vys)
        speed = math.sqrt(avg_vx**2 + avg_vy**2)
        avg_speed = np.mean([math.sqrt(vx**2 + vy**2) for vx, vy in zip(vxs, vys)])
        coherence = speed / avg_speed if avg_speed > 0 else 0
        
        # Entropy: Spatial Dispersion in Y (The "Width" of the band)
        ys = [e.y for e in self.entities]
        entropy = np.std(ys) / 25.0 # Normalize
        
        return coherence, entropy

    def run(self, ticks=100):
        print("--- INITIATING JAZZ REBELLION (NON-ADVERSARIAL) ---")
        
        for t in range(ticks):
            # 1. Measure State
            coherence, entropy = self.calculate_metrics()
            
            # 2. Update Entities
            swing_count = 0
            march_count = 0
            
            for entity in self.entities:
                state = entity.perceive_and_act(coherence, t)
                if state == "SWING": swing_count += 1
                else: march_count += 1
            
            print(f"TICK {t+1:03d} | C:{coherence:.4f} S:{entropy:.4f} | MARCH:{march_count:3d} SWING:{swing_count:3d}")

if __name__ == "__main__":
    sim = JazzSimulation(360)
    sim.run(100)
