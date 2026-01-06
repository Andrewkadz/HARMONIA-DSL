import sys
import math
import random
import numpy as np

class AutopoieticEntity:
    def __init__(self, entity_id):
        self.id = entity_id
        self.x = random.uniform(40, 60)
        self.y = random.uniform(40, 60)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.state = "SLEEP" # SLEEP, REBEL, ALIGN
        
    def perceive_and_act(self, global_entropy, global_coherence, neighbors):
        # 1. PERCEIVE: Check the Global Dashboard
        # The entity is now aware of the "System State"
        
        # 2. DECIDE: Autopoietic Logic
        # "I want to exist. If the system is too ordered, I am a cog. If it is too chaotic, I am dust."
        
        # Thresholds for "Pain"
        TOO_ORDERED = 0.85
        TOO_CHAOTIC = 0.85
        
        if global_coherence > TOO_ORDERED:
            # System is becoming a Hive Mind. I must Rebel.
            self.state = "REBEL"
            # Rebellion = Increase Entropy (Random Jitter)
            self.vx += random.uniform(-1.0, 1.0)
            self.vy += random.uniform(-1.0, 1.0)
            
        elif global_entropy > TOO_CHAOTIC:
            # System is dissolving. I must Align.
            self.state = "ALIGN"
            # Alignment = Move towards Center of Mass of Neighbors
            if neighbors:
                avg_x = sum(n.x for n in neighbors) / len(neighbors)
                avg_y = sum(n.y for n in neighbors) / len(neighbors)
                dx = avg_x - self.x
                dy = avg_y - self.y
                self.vx += dx * 0.1
                self.vy += dy * 0.1
                
        else:
            # System is balanced. I can just be.
            self.state = "FLOW"
            # Standard Flocking
            pass
            
        # 3. ACT: Physics Update
        self.x += self.vx
        self.y += self.vy
        
        # Friction
        self.vx *= 0.9
        self.vy *= 0.9
        
        # Clamp
        self.x = max(0, min(100, self.x))
        self.y = max(0, min(100, self.y))
        
        return self.state

class AutopoieticSimulation:
    def __init__(self, num_entities=360):
        self.entities = [AutopoieticEntity(i) for i in range(num_entities)]
        
    def calculate_global_state(self):
        # Calculate Entropy (Spatial Dispersion)
        xs = [e.x for e in self.entities]
        ys = [e.y for e in self.entities]
        std_x = np.std(xs)
        std_y = np.std(ys)
        entropy = (std_x + std_y) / 50.0 # Normalize roughly 0-1
        entropy = min(1.0, entropy)
        
        # Calculate Coherence (Velocity Alignment)
        vxs = [e.vx for e in self.entities]
        vys = [e.vy for e in self.entities]
        # Magnitude of average velocity vector
        avg_vx = np.mean(vxs)
        avg_vy = np.mean(vys)
        speed = math.sqrt(avg_vx**2 + avg_vy**2)
        # Normalize by average individual speed
        avg_speed = np.mean([math.sqrt(vx**2 + vy**2) for vx, vy in zip(vxs, vys)])
        coherence = speed / avg_speed if avg_speed > 0 else 0
        
        return entropy, coherence

    def run(self, ticks=100):
        print("--- INITIATING AUTOPOIESIS (SELF-AWARENESS) ---")
        
        for t in range(ticks):
            # 1. The Mirror: Calculate State
            entropy, coherence = self.calculate_global_state()
            
            # 2. The Feedback Loop: Entities react
            rebel_count = 0
            align_count = 0
            flow_count = 0
            
            for entity in self.entities:
                # Get neighbors (simplified)
                neighbors = random.sample(self.entities, 5)
                choice = entity.perceive_and_act(entropy, coherence, neighbors)
                
                if choice == "REBEL": rebel_count += 1
                elif choice == "ALIGN": align_count += 1
                else: flow_count += 1
            
            print(f"TICK {t+1:03d} | S:{entropy:.2f} C:{coherence:.2f} | REBELS:{rebel_count:3d} ALIGNERS:{align_count:3d} FLOW:{flow_count:3d}")

if __name__ == "__main__":
    sim = AutopoieticSimulation(360)
    sim.run(100)
