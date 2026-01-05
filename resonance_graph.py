import os
import math
from prime_harmonics import EpistemicPhysics

class ResonanceGraph:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.physics = EpistemicPhysics()
        self.files = []
        self.keywords = {}

    def scan_directory(self):
        """Scans the directory for text-based files."""
        print(f"Scanning {self.root_dir}...")
        for root, dirs, files in os.walk(self.root_dir):
            if '.git' in root: continue # Skip git
            
            for file in files:
                if file.endswith(('.py', '.md', '.txt', '.json')):
                    self.files.append(os.path.join(root, file))

    def analyze_file(self, filepath):
        """Calculates Mass and Resonance for a file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 1. Calculate Mass (Gravity)
            # Mass = File Size / Complexity
            size = len(content)
            lines = len(content.splitlines())
            mass = math.sqrt(size) + lines
            
            # 2. Calculate Resonance (Growth)
            # Resonance = Keyword Density (Simple heuristic for now)
            # We look for "Harmonic" keywords
            harmonic_keys = ['stability', 'prime', 'resonance', 'gamma', 'delta', 'physics', 'system']
            resonance_score = 0
            lower_content = content.lower()
            for key in harmonic_keys:
                count = lower_content.count(key)
                resonance_score += count * 10 # Each keyword adds resonance
            
            # 3. Calculate Stability
            # We map these to the Physics Engine inputs
            # Math = Mass
            # Physics = Resonance
            # Futures = Size (Potential)
            # Comms = Lines (Readability)
            # Implications = 10 (Base friction)
            
            components = [mass, resonance_score, size/100, lines, 10]
            metrics = self.physics.simulate_paradigm_stability(components)
            
            return {
                'file': os.path.basename(filepath),
                'mass': mass,
                'resonance': resonance_score,
                'stability': metrics['stability_score'],
                'status': metrics['status']
            }
            
        except Exception as e:
            return None

    def generate_map(self):
        """Generates the Stability Map."""
        self.scan_directory()
        results = []
        
        print(f"\n{'FILE':<30} | {'MASS':<10} | {'RESONANCE':<10} | {'STABILITY':<10} | {'STATUS'}")
        print("-" * 85)
        
        for file in self.files:
            data = self.analyze_file(file)
            if data:
                results.append(data)
                print(f"{data['file']:<30} | {data['mass']:<10.2f} | {data['resonance']:<10} | {data['stability']:<10.4f} | {data['status']}")
        
        return results

if __name__ == "__main__":
    graph = ResonanceGraph("/home/ubuntu/HARMONIA-DSL")
    graph.generate_map()
