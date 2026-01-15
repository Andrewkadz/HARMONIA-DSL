import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import csv
from typing import List, Dict, Any
from collections import deque

class SyntheticTauCrystal:
    def __init__(self, freq=1.0, feedback_strength=0.99, name="crystal"):
        self.tau = 0.0
        self.phase = 0.0
        self.freq = freq
        self.feedback_strength = feedback_strength
        self.name = name
        self.history = []

    def step(self):
        # Θ oscillatory stability
        theta = np.sin(self.phase)
        
        # ΔΦ phase drift
        delta_phi = np.sin(self.phase + 0.1) - np.sin(self.phase)
        
        # Harmonic Time Equation
        self.tau = self.feedback_strength * (theta + delta_phi)
        
        # Advance phase
        self.phase += 2 * np.pi * self.freq / 100.0
        
        self.history.append(self.tau)
        return self.tau

class TemporalAnchorModule:
    """AI Temporal Anchor using multi-scale tau crystals"""
    
    def __init__(self):
        # Multi-scale crystal ensemble (Fourier layers)
        self.crystals = {
            'micro': SyntheticTauCrystal(freq=10.0, feedback_strength=0.995, name='micro'),
            'meso': SyntheticTauCrystal(freq=1.0, feedback_strength=0.99, name='meso'), 
            'macro': SyntheticTauCrystal(freq=0.1, feedback_strength=0.985, name='macro'),
            'ultra': SyntheticTauCrystal(freq=0.01, feedback_strength=0.98, name='ultra')
        }
        # Bounded history to avoid unbounded memory growth
        self.harmonic_field = deque(maxlen=10_000)
        # Weights for combining scales into the harmonic field
        self.weights = {'micro': 0.1, 'meso': 0.4, 'macro': 0.3, 'ultra': 0.2}
        self.temporal_state = {}
        
    def generate_harmonic_time_field(self) -> Dict[str, float]:
        """Generate multi-scale harmonic time field"""
        field = {}
        combined_tau = 0.0
        
        for scale, crystal in self.crystals.items():
            tau_value = crystal.step()
            field[scale] = tau_value
            
            # Weighted combination for harmonic field
            combined_tau += self.weights[scale] * tau_value
            
        field['harmonic'] = combined_tau
        self.harmonic_field.append(combined_tau)
        return field
    
    def get_temporal_anchor(self) -> str:
        """Convert harmonic field to temporal anchor state"""
        if not self.harmonic_field:
            return "INIT"
            
        current_harmonic = self.harmonic_field[-1]
        
        if current_harmonic > 0.3:
            return "FLOW+"  # Forward temporal flow
        elif current_harmonic < -0.3:
            return "FLOW-"  # Reverse temporal flow  
        else:
            return "SYNC"   # Synchronized temporal state
    
    def ai_temporal_context(self) -> Dict[str, Any]:
        """Provide temporal context for AI decision making"""
        anchor = self.get_temporal_anchor()
        
        # AI behavioral modulation based on temporal state
        context = {
            'temporal_anchor': anchor,
            'processing_mode': self._get_processing_mode(anchor),
            'attention_scale': self._get_attention_scale(),
            'memory_priority': self._get_memory_priority(anchor)
        }
        
        return context
    
    def _get_processing_mode(self, anchor: str) -> str:
        modes = {
            'FLOW+': 'predictive',    # Focus on future states
            'FLOW-': 'reflective',    # Focus on past patterns
            'SYNC': 'present',        # Focus on current state
            'INIT': 'exploratory'     # Initial exploration mode
        }
        return modes.get(anchor, 'adaptive')
    
    def _get_attention_scale(self) -> str:
        # Determine optimal attention scale from crystal ensemble
        if len(self.harmonic_field) == 0:
            variance = 0
        else:
            recent_field = list(self.harmonic_field)
            if len(recent_field) > 10:
                recent_field = recent_field[-10:]
            variance = np.var(recent_field) if recent_field else 0
        
        if variance > 0.5:
            return 'micro'      # High variance = focus on details
        elif variance > 0.1:
            return 'meso'       # Medium variance = balanced focus
        else:
            return 'macro'      # Low variance = broad focus
    
    def _get_memory_priority(self, anchor: str) -> float:
        # Memory consolidation priority based on temporal flow
        priorities = {
            'FLOW+': 0.8,    # High priority for forward flow
            'FLOW-': 0.9,    # Highest priority for reverse flow (reflection)
            'SYNC': 0.6,     # Medium priority for sync state
            'INIT': 0.4      # Lower priority during initialization
        }
        return priorities.get(anchor, 0.5)

# === Phase Error Analysis Add-On ===
def analyze_phase_error(harmonic_field, window: int = 100) -> np.ndarray:
    """
    Compute phase error as deviation from rolling mean.
    Args:
        harmonic_field: list, deque, or np.array of harmonic values over time
        window: smoothing window size
    Returns:
        np.array of phase error magnitudes
    """
    # Convert to numpy array
    arr = np.array(list(harmonic_field), dtype=float)
    if arr.size == 0:
        return arr
    # Ensure window is valid
    win = max(1, min(window, arr.size))
    kernel = np.ones(win, dtype=float) / win
    # Use 'same' to align with input length
    rolling_mean = np.convolve(arr, kernel, mode='same')
    error = arr - rolling_mean
    return np.abs(error)

# Demonstration of AI Temporal Structuring
def demonstrate_ai_temporal_integration(steps: int | None = 100, infinite: bool = False, stop_prob: float = 1e-15, hard_cap: int = 10**12):
    """Show how AI system uses tau crystals for temporal structuring.

    Args:
        steps: Number of steps to run when not in infinite mode. Default 100.
        infinite: If True, run indefinitely until KeyboardInterrupt or near-impossible termination.
        stop_prob: Ultra-rare per-step probability to self-terminate.
        hard_cap: Extremely large step cap as a final safeguard.
    """
    
    anchor_module = TemporalAnchorModule()
    ai_decisions = []
    
    print("AI Temporal Anchor Demonstration")
    print("=" * 50)
    
    current_step = 0
    pattern = deque(maxlen=60)
    encoded = os.getenv('TAU_ENCODED', '0') == '1'
    term_plot = os.getenv('TAU_TERMINAL_PLOT', '0') == '1'

    # Helper: generate a compact sparkline for values in recent history
    def sparkline(vals: List[float], width: int = 60) -> str:
        if not vals:
            return ' ' * width
        # Coerce to list so slicing works for deque/history types
        vals = list(vals)
        # Take the most recent up to width points and normalize to [-1, 1]
        recent = vals[-width:]
        vmin = min(recent)
        vmax = max(recent)
        # Avoid divide-by-zero; if flat, return mid-level marks
        if vmax - vmin < 1e-9:
            return '-' * len(recent) + ' ' * (width - len(recent))
        # Unicode blocks for nicer plot; ASCII fallback
        unicode_blocks = ['\u2581','\u2582','\u2583','\u2584','\u2585','\u2586','\u2587','\u2588']
        ascii_blocks = ['.', ':', '-', '=', '+', '*', '#', '@']
        # Determine whether to force ASCII
        force_ascii = os.getenv('TAU_ASCII', '0') == '1'
        chosen_blocks = ascii_blocks if force_ascii else unicode_blocks
        out = []
        for v in recent:
            # Normalize 0..1
            t = (v - vmin) / (vmax - vmin)
            idx = int(t * (len(chosen_blocks) - 1))
            out.append(chosen_blocks[idx])
        # Pad if fewer than width
        if len(out) < width:
            out.extend([' '] * (width - len(out)))
        s = ''.join(out)
        # If using Unicode, ensure the console can encode it; otherwise fallback to ASCII
        if not force_ascii:
            enc = (getattr(sys.stdout, 'encoding', None) or 'utf-8').lower()
            try:
                s.encode(enc, errors='strict')
            except Exception:
                # Rebuild with ASCII blocks
                out_ascii = []
                for v in recent:
                    t = (v - vmin) / (vmax - vmin)
                    idx = int(t * (len(ascii_blocks) - 1))
                    out_ascii.append(ascii_blocks[idx])
                if len(out_ascii) < width:
                    out_ascii.extend([' '] * (width - len(out_ascii)))
                s = ''.join(out_ascii)
        return s
    try:
        if infinite:
            while True:
                # Generate harmonic time field
                field = anchor_module.generate_harmonic_time_field()
                
                # Get AI temporal context
                context = anchor_module.ai_temporal_context()
                
                # Record decision
                decision = {
                    'step': current_step,
                    'temporal_anchor': context['temporal_anchor'],
                    'processing_mode': context['processing_mode'],
                    'attention_scale': context['attention_scale'],
                    'memory_priority': context['memory_priority'],
                    'harmonic_field': field['harmonic']
                }
                # Avoid unbounded memory growth: keep only the last 10,000
                ai_decisions.append(decision)
                if len(ai_decisions) > 10_000:
                    ai_decisions = ai_decisions[-10_000:]
                
                if current_step % 20 == 0:
                    # Update rolling pattern based on anchor state
                    anchor = context['temporal_anchor']
                    sym = '+' if anchor == 'FLOW+' else ('-' if anchor == 'FLOW-' else '0')
                    pattern.append(sym)
                    pattern_str = ' '.join(pattern) if encoded else ''.join(pattern)
                    # Optional terminal plot of harmonic field
                    plot_str = ''
                    if term_plot:
                        # Build from the harmonic history stored in anchor_module.harmonic_field
                        plot_str = sparkline(anchor_module.harmonic_field, width=60)
                    # Overwrite a single status line (no scroll) in infinite mode
                    if term_plot:
                        print(
                            f"\rStep {current_step:>9,d} | Anchor: {context['temporal_anchor']:5s} | "
                            f"Mode: {context['processing_mode']:10s} | Scale: {context['attention_scale']:5s} | "
                            f"Mem: {context['memory_priority']:.2f} | Harm: {field['harmonic']:+.3f} | "
                            f"Plot: {plot_str} | Pat: {pattern_str:<60}",
                            end="",
                            flush=True,
                        )
                    else:
                        print(
                            f"\rStep {current_step:>9,d} | Anchor: {context['temporal_anchor']:5s} | "
                            f"Mode: {context['processing_mode']:10s} | Scale: {context['attention_scale']:5s} | "
                            f"Memory: {context['memory_priority']:.2f} | Harmonic: {field['harmonic']:+.3f} | "
                            f"Pattern: {pattern_str:<60}",
                            end="",
                            flush=True,
                        )
                current_step += 1

                # Near-impossible termination checks
                if current_step >= hard_cap:
                    break
                if np.random.random() < stop_prob:
                    break
            # Ensure the next output starts on a new line after in-place updates
            print()
        else:
            total_steps = 100 if steps is None else steps
            for step in range(total_steps):
                # Generate harmonic time field
                field = anchor_module.generate_harmonic_time_field()
                
                # Get AI temporal context
                context = anchor_module.ai_temporal_context()
                
                # Simulate AI decision making based on temporal context
                decision = {
                    'step': step,
                    'temporal_anchor': context['temporal_anchor'],
                    'processing_mode': context['processing_mode'],
                    'attention_scale': context['attention_scale'],
                    'memory_priority': context['memory_priority'],
                    'harmonic_field': field['harmonic']
                }
                
                ai_decisions.append(decision)
                
                # Print periodic updates (line-by-line and/or in-place terminal plot)
                if os.getenv('TAU_TERMINAL_PLOT', '0') == '1' and step % 5 == 0:
                    # Update rolling pattern and optional plot just like infinite mode
                    anchor = context['temporal_anchor']
                    sym = '+' if anchor == 'FLOW+' else ('-' if anchor == 'FLOW-' else '0')
                    pattern.append(sym)
                    pattern_str = ' '.join(pattern) if encoded else ''.join(pattern)
                    plot_str = sparkline(anchor_module.harmonic_field, width=60)
                    print(
                        f"\rStep {step:>9,d} | Anchor: {context['temporal_anchor']:5s} | "
                        f"Mode: {context['processing_mode']:10s} | Scale: {context['attention_scale']:5s} | "
                        f"Mem: {context['memory_priority']:.2f} | Harm: {field['harmonic']:+.3f} | "
                        f"Plot: {plot_str} | Pat: {pattern_str:<60}",
                        end="",
                        flush=True,
                    )
                elif step % 20 == 0:
                    print(
                        f"Step {step:3d}: {context['temporal_anchor']:6s} | "
                        f"Mode: {context['processing_mode']:10s} | "
                        f"Scale: {context['attention_scale']:5s} | "
                        f"Memory: {context['memory_priority']:.2f}"
                    )
            if os.getenv('TAU_TERMINAL_PLOT', '0') == '1':
                print()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting demo loop...")
    
    return ai_decisions, anchor_module

# Visualization of multi-scale harmonic fields
def visualize_harmonic_fields(anchor_module, steps=200):
    """Visualize the multi-scale tau crystal ensemble"""
    
    # Generate data
    data = {scale: [] for scale in anchor_module.crystals.keys()}
    data['harmonic'] = []
    
    for _ in range(steps):
        field = anchor_module.generate_harmonic_time_field()
        for scale in anchor_module.crystals.keys():
            data[scale].append(field[scale])
        data['harmonic'].append(field['harmonic'])
    
    # Create visualization
    fig, axes = plt.subplots(3, 2, figsize=(15, 12))
    fig.suptitle('Multi-Scale Tau Crystal Harmonic Time Fields', fontsize=16)
    
    # Individual crystal plots
    scales = list(anchor_module.crystals.keys())
    for i, scale in enumerate(scales):
        row, col = i // 2, i % 2
        axes[row, col].plot(data[scale], label=f'{scale.capitalize()} τ-crystal')
        axes[row, col].set_title(f'{scale.capitalize()} Scale (f={anchor_module.crystals[scale].freq})')
        axes[row, col].set_ylabel('τ value')
        axes[row, col].grid(True, alpha=0.3)
        axes[row, col].legend()
    
    # Combined harmonic field
    axes[2, 0].plot(data['harmonic'], 'r-', linewidth=2, label='Harmonic Field')
    axes[2, 0].set_title('Combined Harmonic Time Field')
    axes[2, 0].set_xlabel('Time Steps')
    axes[2, 0].set_ylabel('Harmonic τ')
    axes[2, 0].grid(True, alpha=0.3)
    axes[2, 0].legend()
    
    # Temporal anchor states
    anchors = []
    for i in range(len(data['harmonic'])):
        if data['harmonic'][i] > 0.3:
            anchors.append(1)
        elif data['harmonic'][i] < -0.3:
            anchors.append(-1)
        else:
            anchors.append(0)
    
    axes[2, 1].plot(anchors, 'g-', linewidth=2, label='Temporal Anchor')
    axes[2, 1].set_title('AI Temporal Anchor States')
    axes[2, 1].set_xlabel('Time Steps')
    axes[2, 1].set_ylabel('Anchor State')
    axes[2, 1].set_yticks([-1, 0, 1])
    axes[2, 1].set_yticklabels(['FLOW-', 'SYNC', 'FLOW+'])
    axes[2, 1].grid(True, alpha=0.3)
    axes[2, 1].legend()
    
    plt.tight_layout()
    # Save to a portable, relative path in the current working directory
    out_path = os.path.join(os.getcwd(), 'harmonic_time_fields.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Environment-controlled infinite mode
    # Set TAU_INFINITE=1 to run indefinitely (Ctrl+C to stop)
    # Optional: TAU_STEPS to override finite steps (default 100)
    # Optional: TAU_STOP_PROB to adjust ultra-rare termination (default 1e-15)
    # Visualization remains finite to avoid memory blow-up.
    tau_infinite = os.getenv('TAU_INFINITE', '0') == '1'
    tau_steps_env = os.getenv('TAU_STEPS')
    tau_steps = int(tau_steps_env) if (tau_steps_env and tau_steps_env.isdigit()) else 100
    tau_stop_prob = float(os.getenv('TAU_STOP_PROB', '1e-15'))

    # Run demonstration
    decisions, anchor_module = demonstrate_ai_temporal_integration(
        steps=tau_steps,
        infinite=tau_infinite,
        stop_prob=tau_stop_prob,
    )
    
    print(f"\nGenerated {len(decisions)} AI decisions based on tau crystal temporal anchoring")
    
    # Create visualization (finite) unless skipped
    if os.getenv('TAU_SKIP_VIS', '0') != '1':
        print("\nVisualizing harmonic time fields...")
        visualize_harmonic_fields(anchor_module)
    
    # Run Phase Error Analysis Add-On
    try:
        harmonic_series = list(anchor_module.harmonic_field)
        if len(harmonic_series) > 0:
            phase_error = analyze_phase_error(harmonic_series, window=100)

            # Save to CSV
            with open("phase_error.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Step", "PhaseError"])
                for i, val in enumerate(phase_error):
                    writer.writerow([i, float(val)])

            # Plot error vs. time
            plt.figure(figsize=(10, 5))
            plt.plot(phase_error, label="Phase Error Magnitude", color="blue")
            plt.xlabel("Step")
            plt.ylabel("Error")
            plt.title("Tau-Crystal Phase Error Over Time")
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig("phase_sync.png", dpi=200)
            plt.close()

            print("[INFO] Phase error analysis complete.")
            print("       - Saved to phase_error.csv")
            print("       - Plot saved as phase_sync.png")
        else:
            print("[WARN] Phase error analysis skipped: harmonic field is empty.")
    except Exception as e:
        print(f"[ERROR] Phase error analysis failed: {e}")

    print("\nTau Crystal AI Integration Complete!")
    print("- Multi-scale harmonic time fields generated")
    print("- Temporal anchor module operational") 
    print("- AI temporal structuring demonstrated")
