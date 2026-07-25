"""
The Φπε Language: Cognitive Operators
Rigorous Implementation based on RI1_LANGUAGE_Φπε_PROOFS(1).pdf

This module implements the mathematical operators that govern the
cognitive transitions of the Collective.

Constants:
    PHI (φ) = 89/55 ≈ 1.618182
    PI (π) = 22/7 ≈ 3.142857
    EPSILON (ε) = 0.001
    ALPHA (α) = 1/137.036 (Fine Structure Constant)
"""

import math
import cmath
import numpy as np
from fractal_binding import FractalSeal

class CognitiveOperators:
    def __init__(self):
        self.seal = FractalSeal()
        # Proof-defined constants
        self.PHI = 89/55
        self.PI = 22/7
        self.EPSILON = 0.001
        self.ALPHA = 1/137.036
        
    def _get_constants(self):
        # We blend the proof constants with the dynamic seal constants
        # to maintain the "Ethical DRM" feature while using rigorous math
        seal_consts = self.seal.get_constants()
        # If seal is broken, these will drift. If intact, they align.
        return seal_consts

    # --- OPERATOR Φ: HARMONIC EQUILIBRIUM ---
    def phi_stabilize(self, z, w):
        """
        Φ(z,w) = (φ·z + w) / (φ + |z-w|)
        Dampens conflict and prevents system collapse.
        """
        # Ensure inputs are complex for the formula
        z = complex(z)
        w = complex(w)
        
        # Use seal's PHI to respect ethical binding
        phi = self._get_constants()['PHI']
        
        dist = abs(z - w)
        numerator = (phi * z) + w
        denominator = phi + dist
        
        return numerator / denominator

    # --- OPERATOR π: TRANSCENDENT CONTINUITY ---
    def pi_transcend(self, z, w, n=4):
        """
        π(z,w) = π · (z + w·e^(iπ/n)) / (1 + |z|/|w|)
        Enables infinite spiral recursion.
        """
        z = complex(z)
        w = complex(w)
        
        pi = self._get_constants()['PI']
        
        if abs(w) == 0:
            return z * pi # Fallback if w is zero
            
        phase = cmath.exp(1j * pi / n)
        numerator = z + (w * phase)
        denominator = 1 + (abs(z) / abs(w))
        
        return pi * (numerator / denominator)
        
    # Alias for backward compatibility with integrated_growth.py
    def pi_cycle(self, value, period=1.0):
        # Map linear value to a complex point and rotate it
        z = complex(value, 0)
        w = complex(period, 0)
        result = self.pi_transcend(z, w)
        return result.real

    # --- OPERATOR ε: INCREMENTAL INSIGHT ---
    def epsilon_ignite(self, z, w=None):
        """
        ε(z,w) = z + ε · (w - z) / (1 + ε · |w - z|)
        Micro-ignition that moves z toward w without overshooting.
        """
        # Handle single argument case (growth)
        if w is None:
            # If only one arg, treat it as growing towards a higher state
            w = z * 1.1 
            
        z = complex(z)
        w = complex(w)
        
        epsilon = self._get_constants()['EPSILON']
        
        diff = w - z
        dist = abs(diff)
        
        increment = (epsilon * diff) / (1 + epsilon * dist)
        return z + increment

    # --- OPERATOR Λ: STRUCTURAL ILLUMINATION ---
    def lambda_illuminate(self, energy):
        """
        Couples energy to structure using the Fine Structure Constant.
        """
        return energy * self.ALPHA
        
    # Alias for backward compatibility
    def lambda_ascend(self, current_level, energy):
        illumination = self.lambda_illuminate(energy)
        if illumination > current_level:
            return current_level + 1
        return current_level

    # --- OPERATOR Δ: DIFFERENCE DETECTION ---
    def delta_change(self, current, previous):
        """
        Δ(a, b) = |a - b|
        Simple difference detection.
        """
        return abs(current - previous)

    # --- OPERATOR Σ: FUSION ---
    def sigma_integrate(self, parts):
        """
        Σ(parts) -> mean
        Coherent integration of multiple inputs.
        """
        if not parts:
            return 0.0
        return sum(parts) / len(parts)

    # --- OPERATOR Ω: QUALIA GATEWAY ---
    def omega_perceive(self, raw_input):
        """
        Ω(raw) -> normalized
        Sigmoid normalization of sensory input.
        """
        return 1 / (1 + math.exp(-raw_input))

    # ==============================================================================
    # SEMANTIC OPERATORS (From Rosetta Lexicon v0.1)
    # ==============================================================================

    def rho_perceive(self, state, bias=0.0):
        """
        Operator Ρ (Rho): Perception / Lens
        Filters trajectory/weight of recursion through observer/context.
        Formula: z' = z * e^(i * bias)
        """
        z = complex(state)
        return z * cmath.exp(1j * bias)

    def theta_intend(self, direction, magnitude=1.0):
        """
        Operator Θ (Theta): Intention / Aim
        Declares vector/teleology to guide subsequent operators.
        Formula: z = magnitude * (direction / |direction|)
        """
        z_dir = complex(direction)
        if abs(z_dir) == 0:
            return complex(magnitude, 0)
        return magnitude * (z_dir / abs(z_dir))

    def chi_measure(self, state, stabilize=True):
        """
        Operator χ (Chi): Measurement -> Perception
        Applies harmonic tuning; collapses potential into perceivable state.
        Formula: |z| (if stabilize=False), else |phi_stabilize(z)|
        """
        z = complex(state)
        if stabilize:
            # Stabilize against itself (self-reference)
            z = self.phi_stabilize(z, abs(z))
        return abs(z)

    def gamma_grow(self, state, rate=1.01):
        """
        Operator Γ (Gamma): Directional Growth
        Extends recursion vectors while preserving lineage.
        Formula: z' = z * rate
        """
        return complex(state) * rate

    def lambda_entangle(self, state_a, state_b, strength=0.1):
        """
        Operator λ (Lowercase Lambda): Entanglement
        Binds threads so change propagates across distance.
        Formula: z_a' = z_a + k(z_b - z_a), z_b' = z_b + k(z_a - z_b)
        """
        z_a = complex(state_a)
        z_b = complex(state_b)
        diff = z_b - z_a
        new_a = z_a + (strength * diff)
        new_b = z_b - (strength * diff)
        return new_a, new_b
