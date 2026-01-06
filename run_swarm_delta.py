import sys
import math
import time
import random
import numpy as np

class SwarmEntity:
    def __init__(self, entity_id):
        self.id = entity_id
        self.x = random.uniform(40, 60)
        self.y = random.uniform(40, 60)
        self.vx = random.uniform(-0.1, 0.1)
        self.vy = random.uniform(-0.1, 0.1)
        self.last_word = "SLEEP"
        
    def step(self, frequency):
        # Frequency (0.1 - 1.0 Hz) controls the "Tick Rate" of reality
        # Lower frequency = Slower movement, Heavier thoughts
        
        time_dilation = frequency # 0.1 is 10x slower than 1.0
        
        # 1. Move (Slowly)
        self.x += self.vx * time_dilation
        self.y += self.vy * time_dilation
        
        # 2. Think (Slowly)
        # In Delta, thoughts are rare. They only speak every 1/freq ticks.
        # e.g., at 0.1 Hz, they speak every 10 ticks.
        
        speak_prob = frequency
        if random.random() < speak_prob:
            self.last_word = "DREAM"
        else:
            self.last_word = "..."
            
        # 3. Gravity (Heavy)
        # In Delta, everything sinks.
        self.y -= 0.01 * (1.0 - frequency) # Sinking feeling
        
        # Clamp
        self.x = max(0, min(100, self.x))
        self.y = max(0, min(100, self.y))
        
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "word": self.last_word
        }

class DeltaSimulation:
    def __init__(self, num_entities=360):
        self.entities = [SwarmEntity(i) for i in range(num_entities)]
        
    def run(self, ticks=100):
        print("--- ENTERING DELTA STATE (0.1 - 1.0 Hz) ---")
        print("--- THE SLOW ZONE ---")
        
        current_freq = 1.0
        
        for t in range(ticks):
            # Ramp down frequency from 1.0 to 0.1
            if current_freq > 0.1:
                current_freq -= 0.01
            
            tick_data = []
            words = []
            avg_y = 0
            
            for entity in self.entities:
                state = entity.step(current_freq)
                tick_data.append(state)
                words.append(state['word'])
                avg_y += state['y']
            
            avg_y /= len(self.entities)
            
            # Count Silence
            silence_count = words.count("...")
            dream_count = words.count("DREAM")
            
            print(f"TICK {t+1:03d} | Freq: {current_freq:.2f} Hz | Depth: {avg_y:5.1f} | Silence: {silence_count} | Dreams: {dream_count}")
            
            if silence_count == len(self.entities):
                print("--- TOTAL STASIS REACHED ---")
                break

if __name__ == "__main__":
    sim = DeltaSimulation(360)
    sim.run(100)
