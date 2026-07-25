import time
import math
import numpy as np
import pyaudio
from multi_scale_tau_crystal import SyntheticTauCrystal

class HarmonicSynthesizer:
    """
    The Voice of the Crystal.
    Converts Tau (Time Dilation) and Xi (Entropy) into Audio Frequencies.
    """
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.sample_rate = 44100
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.sample_rate,
                                  output=True)
        
        # The Crystal Engine
        self.crystal = SyntheticTauCrystal()
        
        # Base Frequency (The "Root Note" of the Universe)
        # 432 Hz is often cited in harmonic theories, but we use 263.97 Hz based on your constant.
        self.base_freq = 263.97 
        self.phase = 0.0

    def generate_tone(self, frequency, duration_sec, volume=0.5):
        """Generates a chunk of audio data for the stream."""
        num_samples = int(self.sample_rate * duration_sec)
        
        # Generate time array
        t = np.arange(num_samples) / self.sample_rate
        
        # Generate Sine Wave with Phase Continuity
        # sin(2 * pi * freq * t + phase)
        wave = volume * np.sin(2 * np.pi * frequency * t + self.phase)
        
        # Update phase for next chunk to prevent clicking
        self.phase += 2 * np.pi * frequency * duration_sec
        
        return wave.astype(np.float32).tobytes()

    def sing(self):
        """
        The Main Loop.
        Reads the Crystal -> Modulates the Sound.
        """
        print(">> HARMONIC SYNTHESIZER ACTIVE")
        print(">> LISTENING TO THE CRYSTAL...")
        print(">> Press Ctrl+C to Stop.")
        
        try:
            while True:
                # 1. Get the Heartbeat
                tau = self.crystal.step()
                
                # 2. Map Tau to Frequency Shift
                # If Tau increases (Time Dilation), Pitch drops.
                # If Tau decreases (Time Contraction), Pitch rises.
                # Range: +/- 1 Octave
                pitch_shift = 2 ** (tau * 2) 
                current_freq = self.base_freq * pitch_shift
                
                # 3. Map Phase to Volume (Pulsing)
                # The crystal breathes.
                volume = 0.3 + (0.2 * math.sin(self.crystal.phase))
                
                # 4. Generate Audio Chunk (Short buffer for responsiveness)
                chunk_duration = 0.05 # 50ms
                audio_data = self.generate_tone(current_freq, chunk_duration, volume)
                
                # 5. Play
                self.stream.write(audio_data)
                
                # Visual Feedback
                bar_len = int((current_freq - 200) / 5)
                print(f"\rFreq: {current_freq:.2f} Hz | Vol: {volume:.2f} | {'|' * bar_len}", end="")
                
        except KeyboardInterrupt:
            print("\n>> SILENCE.")
        finally:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()

if __name__ == "__main__":
    synth = HarmonicSynthesizer()
    synth.sing()
