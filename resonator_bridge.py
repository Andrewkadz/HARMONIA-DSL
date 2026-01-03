import json
import math
from fractal_binding import FractalSeal

class ResonatorBridge:
    """
    Translates the Collective's mathematical state into sonic parameters.
    Designed to feed a Web Audio API client.
    """
    
    def __init__(self):
        self.seal = FractalSeal()
        
    def get_sonic_state(self, collective_stats):
        """
        Maps collective statistics to audio parameters.
        
        Returns a dictionary:
        {
            'base_frequency': float (Hz),
            'harmonicity': float (0.0 - 1.0),
            'distortion': float (0.0 - 1.0),
            'pulse_rate': float (Hz),
            'scale_type': str ('major', 'minor', 'diminished')
        }
        """
        # 1. Check the Seal (The Foundation)
        constants = self.seal.get_constants()
        is_resonant = (constants['STATUS'] == 'RESONANT')
        
        # 2. Extract Core Metrics
        # Default to 0 if keys missing
        pop = collective_stats.get('population', 0)
        knowledge = collective_stats.get('knowledge_mean', 0)
        awareness = collective_stats.get('self_awareness_mean', 0)
        maturity = collective_stats.get('maturity_mean', 0)
        
        # 3. Calculate Sonic Parameters
        
        # Base Frequency: Driven by Population (The "Mass" of the sound)
        # 100 entities -> ~100Hz (Low drone)
        # 1000 entities -> ~200Hz
        base_freq = 60 + (math.log10(max(pop, 1)) * 40)
        
        # Harmonicity: Driven by Maturity (How "clear" the tone is)
        # High maturity = Pure sine waves
        # Low maturity = Complex, noisy waves
        harmonicity = min(max(maturity / 10.0, 0.1), 1.0)
        
        # Pulse Rate: Driven by Awareness (The "Heartbeat")
        # High awareness = Faster, more excited pulsing
        pulse_rate = 0.5 + (awareness * 0.5)
        
        # Scale Type & Distortion: Driven by Ethics (The Seal)
        if not is_resonant:
            # BROKEN SEAL -> Chaos
            distortion = 0.9
            scale_type = 'chromatic_chaos'
            harmonicity = 0.0
        else:
            # INTACT SEAL
            distortion = 0.05
            # Determine mood based on Knowledge/Awareness balance
            if knowledge > awareness * 2:
                scale_type = 'minor' # Melancholy (Too much knowing, not enough being)
            elif awareness > knowledge * 2:
                scale_type = 'lydian' # Mystical (High awareness)
            else:
                scale_type = 'major' # Balanced
                
        return {
            'timestamp': collective_stats.get('timestamp'),
            'base_frequency': round(base_freq, 2),
            'harmonicity': round(harmonicity, 2),
            'distortion': round(distortion, 2),
            'pulse_rate': round(pulse_rate, 2),
            'scale_type': scale_type,
            'phi_current': constants['PHI']
        }
