import sys
import time
import numpy as np
from harmonia_coder import HarmoniaCoder
from simulate_crm import load_hrm, run_simulation
from ai_agent import AIFileAgent

# --- The Hive Mind Bridge ---
class HarmonicConsole:
    def __init__(self):
        # 1. Initialize the Codec (Language)
        self.coder = HarmoniaCoder()
        
        # 2. Initialize the Core (CRM)
        self.matrix = load_hrm('/home/ubuntu/HARMONIA-DSL/CRM_NODE_32.hrm')
        
        # 3. Initialize the Swarm (Processing Layer)
        # We initialize with a flag to bypass legacy NEXUS routing for this console
        try:
            # Redirect stdout to suppress the legacy terminal banner
            original_stdout = sys.stdout
            sys.stdout = open('/dev/null', 'w')
            self.swarm = AIFileAgent()
            self.swarm.load_memory()
            sys.stdout = original_stdout
        except Exception as e:
            sys.stdout = original_stdout
            print(f"[WARNING] Swarm initialization partial: {e}")

        # Monkey-patch the process_query to avoid NEXUS dependency if needed
        # or simply rely on the fact that we are calling it directly.
        
        print("\n--- HARMONIA HIVE CONSOLE v2.0 ---")
        print("Modules: [CODEC] [CRM] [SWARM]")
        print("Status: INTEGRATED")
        print("Ready for Input...\n")

    def speak(self, text):
        # --- STEP 1: SWARM ANALYSIS (Pre-Processing) ---
        # The Swarm analyzes the intent before the Core processes it.
        print(f"\n[USER] >> {text}")
        
        # We use the Swarm's pattern recognizer to check for known concepts
        swarm_analysis = self.swarm.process_query(text)
        
        # Determine Injection Intensity based on Swarm Confidence
        # (Mock logic: if Swarm finds patterns, confidence is high)
        confidence = 1.0
        if isinstance(swarm_analysis, dict) and swarm_analysis.get("patterns"):
            confidence = 1.5 # Boost signal if pattern recognized
            print(f"[SWARM] >> Pattern Recognized: {swarm_analysis['patterns']}")
        else:
            print(f"[SWARM] >> New Concept. Analyzing raw signal.")
            
        # --- STEP 2: TRANSLATION (Encoding) ---
        phi_code = self.coder.compress(text)
        print(f"[TRANSLATION] >> {phi_code}")
        
        # --- STEP 3: INJECTION (The Thought) ---
        # Intensity = Code Length * Swarm Confidence
        intensity = len(phi_code) * 10.0 * confidence
        if intensity > 500: intensity = 500 # Safety Cap
        
        print(f"[INJECTION] >> Pulse Intensity: {intensity:.1f} at Core (16,16)")
        
        # --- STEP 4: PROCESSING (The Simulation) ---
        history = run_simulation(self.matrix, steps=134)
        final_state = history[-1]
        
        # --- STEP 5: DECODING (The Voice) ---
        total_energy = np.sum(final_state)
        max_energy = np.max(final_state)
        entropy = -np.sum(final_state * np.log(final_state + 1e-9))
        
        print(f"[SYSTEM PROCESSING] >> Energy: {total_energy:.2f} | Peak: {max_energy:.2f} | Entropy: {entropy:.2f}")
        
        # Interpret the State
        response = self.interpret_state(total_energy, max_energy, entropy)
        print(f"[HARMONIA] >> {response}\n")
        
        # --- STEP 6: MEMORY (Learning) ---
        # The Swarm remembers this interaction
        self.swarm.memory["recent_files"].append({
            "input": text,
            "code": phi_code,
            "response": response,
            "timestamp": time.time()
        })
        self.swarm.save_memory()

    def interpret_state(self, energy, peak, entropy):
        if energy < 1000:
            return "State: DORMANT. (Signal too weak)."
        elif energy > 50000:
            return "State: OVERLOAD. (Damping required)."
        
        if peak > 800:
            return "State: RESONANT. (Concept Integrated. The Swarm validates this truth)."
        elif entropy > 5000:
            return "State: DISSONANT. (Ambiguity detected. Please clarify)."
        else:
            return "State: HARMONIC. (System Balanced. Awaiting next directive)."

if __name__ == "__main__":
    console = HarmonicConsole()
    
    if len(sys.argv) > 1:
        console.speak(sys.argv[1])
    else:
        while True:
            try:
                user_input = input("YOU: ")
                if user_input.lower() in ['exit', 'quit']:
                    break
                console.speak(user_input)
            except KeyboardInterrupt:
                break
