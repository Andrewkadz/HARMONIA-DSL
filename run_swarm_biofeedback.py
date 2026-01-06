import sys
import math
import time
import random
import csv
import numpy as np

class SwarmEntity:
    def __init__(self, entity_id):
        self.id = entity_id
        self.x = random.uniform(40, 60)
        self.y = random.uniform(40, 60)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        
    def update(self, gravity, coherence, friction, velocity_scale, entropy, neighbors):
        # 1. Coherence (Theta) - Align with neighbors
        avg_vx = 0
        avg_vy = 0
        if neighbors:
            for n in neighbors:
                avg_vx += n.vx
                avg_vy += n.vy
            avg_vx /= len(neighbors)
            avg_vy /= len(neighbors)
            
            self.vx += (avg_vx - self.vx) * coherence
            self.vy += (avg_vy - self.vy) * coherence
            
        # 2. Gravity (Delta) - Pull to center
        dx = 50 - self.x
        dy = 50 - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            self.vx += (dx/dist) * gravity
            self.vy += (dy/dist) * gravity
            
        # 3. Entropy (Gamma) - Random jitter
        self.vx += random.uniform(-entropy, entropy)
        self.vy += random.uniform(-entropy, entropy)
        
        # 4. Friction (Alpha) - Slow down
        self.vx *= (1.0 - friction)
        self.vy *= (1.0 - friction)
        
        # 5. Velocity Scale (Beta) - Speed limit
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > velocity_scale:
            self.vx = (self.vx / speed) * velocity_scale
            self.vy = (self.vy / speed) * velocity_scale
            
        # Move
        self.x += self.vx
        self.y += self.vy
        
        # Clamp
        self.x = max(0, min(100, self.x))
        self.y = max(0, min(100, self.y))

class BioSwarmSimulation:
    def __init__(self, csv_path, num_entities=360):
        self.entities = [SwarmEntity(i) for i in range(num_entities)]
        self.eeg_data = self.load_eeg(csv_path)
        
    def load_eeg(self, path):
        data = []
        with open(path, 'r') as f:
            reader = csv.reader(f)
            # Skip header if it exists (heuristic: check if first col is date)
            # In the snippet, line 2 was data. We'll just try to parse floats.
            for row in reader:
                try:
                    # Mind Monitor Standard Columns (0-indexed)
                    # 2-5: Delta
                    # 6-9: Theta
                    # 10-13: Alpha
                    # 14-17: Beta
                    # 18-21: Gamma
                    
                    # We average the 4 sensors (TP9, AF7, AF8, TP10)
                    delta = sum([float(row[i]) for i in range(2, 6)]) / 4.0
                    theta = sum([float(row[i]) for i in range(6, 10)]) / 4.0
                    alpha = sum([float(row[i]) for i in range(10, 14)]) / 4.0
                    beta = sum([float(row[i]) for i in range(14, 18)]) / 4.0
                    gamma = sum([float(row[i]) for i in range(18, 22)]) / 4.0
                    
                    data.append({
                        'delta': delta,
                        'theta': theta,
                        'alpha': alpha,
                        'beta': beta,
                        'gamma': gamma
                    })
                except (ValueError, IndexError):
                    continue
        return data

    def normalize(self, val, min_val=-1.0, max_val=1.0):
        # EEG data is often in Bels or log scale, can be negative
        # We need 0.0 to 1.0
        # Simple min-max normalization based on typical Mind Monitor ranges
        # Delta: -1 to 1 -> 0 to 1
        return max(0.0, min(1.0, (val - min_val) / (max_val - min_val)))

    def run(self):
        print("--- INJECTING NEURAL DATA INTO SWARM ---")
        
        for t, brain_state in enumerate(self.eeg_data):
            if t >= 100: break # Run for 100 ticks
            
            # Map Brain to Physics
            # Note: Mind Monitor values are usually log10 of power density
            # Range is roughly -1.0 to 1.5
            
            gravity = self.normalize(brain_state['delta'], -0.5, 1.0) * 0.5
            coherence = self.normalize(brain_state['theta'], -0.5, 1.0)
            friction = self.normalize(brain_state['alpha'], -0.5, 1.0) * 0.2
            velocity = self.normalize(brain_state['beta'], -0.5, 1.0) * 2.0
            entropy = self.normalize(brain_state['gamma'], -0.5, 1.0) * 0.5
            
            # Run Swarm Step
            avg_dist = 0
            for entity in self.entities:
                # Simple neighbor check (random sample for speed)
                neighbors = random.sample(self.entities, 5)
                entity.update(gravity, coherence, friction, velocity, entropy, neighbors)
                
                dist = math.sqrt((entity.x - 50)**2 + (entity.y - 50)**2)
                avg_dist += dist
                
            avg_dist /= len(self.entities)
            
            # Determine Dominant State
            states = {
                'SLEEP': brain_state['delta'],
                'DREAM': brain_state['theta'],
                'RELAX': brain_state['alpha'],
                'FOCUS': brain_state['beta'],
                'INSIGHT': brain_state['gamma']
            }
            dominant = max(states, key=states.get)
            
            print(f"TICK {t+1:03d} | Brain: {dominant} | Swarm Radius: {avg_dist:5.1f} | G:{gravity:.2f} C:{coherence:.2f} V:{velocity:.2f}")

if __name__ == "__main__":
    sim = BioSwarmSimulation('/home/ubuntu/upload/mindMonitor_2026-01-04--23-45-31(1).csv')
    sim.run()
