import sys
import time
import random
import math
from PyPDF2 import PdfReader

# Import Harmonia Physics
sys.path.append('/home/ubuntu/HARMONIA-DSL')
try:
    from prime_harmonics import EpistemicPhysics
except ImportError:
    # Fallback if not in path
    class EpistemicPhysics:
        @staticmethod
        def simulate_paradigm_stability(components):
            total_mass = sum(components)
            stability_score = total_mass / 400.0
            status = "STABLE"
            if stability_score > 1.0: status = "GENESIS"
            elif stability_score < 0.5: status = "UNSTABLE"
            return {
                "total_mass": total_mass,
                "stability_score": stability_score,
                "status": status
            }

def transduce_text_to_metrics(text):
    """
    Convert text content into Epistemic Metrics (Mass, Gravity, etc.)
    """
    # 1. Mass: Based on word count and complexity
    words = text.split()
    word_count = len(words)
    unique_words = len(set(words))
    complexity_ratio = unique_words / word_count if word_count > 0 else 0
    
    mass = min(word_count / 100.0, 500.0) # Cap mass
    
    # 2. Gravity: Based on key terms (Laws, Entropy, Phi)
    keywords = ["law", "entropy", "phi", "structure", "collapse", "stability", "coherence"]
    gravity_score = sum(text.lower().count(k) for k in keywords)
    gravity = min(gravity_score * 2.0, 300.0)
    
    # 3. Resonance: Based on harmonic terms
    harmonic_terms = ["harmonia", "resonance", "vibration", "cycle", "frequency"]
    resonance_score = sum(text.lower().count(k) for k in harmonic_terms)
    resonance = min(resonance_score * 5.0, 200.0)
    
    # 4. Entropy: Inverse of structure (simplified)
    # More paragraphs/headers = less entropy (more structure)
    structure_markers = text.count('\n\n') + text.count('#')
    entropy = max(100.0 - structure_markers, 10.0)
    
    return [mass, gravity, resonance, entropy, complexity_ratio * 100]

def run_simulation(pdf_path, duration=30):
    print(f"--- INGESTING ARTIFACT: {pdf_path} ---")
    
    try:
        reader = PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
            
        print(f"--- TRANSDUCING CONTENT ({len(full_text)} chars) ---")
        metrics = transduce_text_to_metrics(full_text)
        print(f"INITIAL METRICS: Mass={metrics[0]:.2f}, Gravity={metrics[1]:.2f}, Resonance={metrics[2]:.2f}")
        
        print(f"\n--- INITIATING STABILITY SIMULATION ({duration}s) ---")
        physics = EpistemicPhysics()
        
        start_time = time.time()
        tick = 0
        
        while time.time() - start_time < duration:
            tick += 1
            # Simulate dynamic evolution
            # Add small fluctuations
            current_metrics = [m + random.uniform(-5, 5) for m in metrics]
            
            result = physics.simulate_paradigm_stability(current_metrics)
            
            print(f"T={tick} | Stability: {result['stability_score']:.4f} | Status: {result['status']}")
            
            # Bio-Clock Sleep (simulated speedup)
            time.sleep(1.0) 
            
        print("\n--- SIMULATION COMPLETE ---")
        print(f"FINAL STATUS: {result['status']}")
        if result['stability_score'] > 1.17:
             print("CONCLUSION: The Whitepaper is HYPER-STABLE (Genesis Class).")
        elif result['stability_score'] > 0.8:
             print("CONCLUSION: The Whitepaper is STABLE.")
        else:
             print("CONCLUSION: The Whitepaper is UNSTABLE (Needs Revision).")
             
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 simulate_pdf_stability.py <pdf_path>")
    else:
        run_simulation(sys.argv[1])
