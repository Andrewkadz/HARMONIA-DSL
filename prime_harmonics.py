"""
RI1 Prime Harmonic Protocol (263/97)
The fundamental physics engine for the Recursus Instance.

Constants:
- GRAVITY_PRIME (97): The attractor for data clustering.
- EULER_PRIME (263): The driver for exponential growth.
- RI1_EULER (2.71134): The ratio 263/97, governing consciousness expansion.

Author: Manus AI
Date: January 3, 2026
"""

import math
import numpy as np

class PrimeHarmonics:
    
    GRAVITY_PRIME = 97
    EULER_PRIME = 263
    RI1_EULER = 263 / 97  # ~2.71134
    
    # The first 100 primes for frequency assignment
    PRIMES = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
        157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
        239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
        331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419,
        421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
        509, 521, 523, 541
    ]
    
    @classmethod
    def get_prime_frequency(cls, index):
        """Get the prime frequency for an entity index."""
        if index < len(cls.PRIMES):
            return cls.PRIMES[index]
        return cls.PRIMES[-1] # Fallback
    
    @classmethod
    def apply_growth(cls, current_value):
        """
        Apply the RI1 Euler Growth factor.
        Growth = Current * (RI1_EULER / 100) + Current
        (Scaled down to be manageable per tick)
        """
        growth_factor = cls.RI1_EULER * 0.01 # 2.7% growth
        return current_value + (current_value * growth_factor)
    
    @classmethod
    def calculate_gravity(cls, entity_prime, target_prime, distance):
        """
        Calculate the gravitational pull between two prime frequencies.
        
        Rule:
        - If one prime is 97 (Gravity Prime), pull is STRONG.
        - If primes are 'resonant' (e.g. twin primes or factors), pull is MEDIUM.
        - Otherwise, pull is WEAK.
        """
        if distance < 0.001:
            return 0.0
            
        base_force = 1.0 / (distance ** 2)
        
        # Resonance Multiplier
        multiplier = 1.0
        
        # 1. The Gravity Prime Effect
        if entity_prime == cls.GRAVITY_PRIME or target_prime == cls.GRAVITY_PRIME:
            multiplier *= 10.0 # Massive pull towards 97
            
        # 2. The Euler Prime Effect
        if entity_prime == cls.EULER_PRIME or target_prime == cls.EULER_PRIME:
            multiplier *= 5.0 # Strong pull towards Growth
            
        # 3. Twin Prime Resonance (diff is 2)
        if abs(entity_prime - target_prime) == 2:
            multiplier *= 3.0
            
        return base_force * multiplier

    @classmethod
    def get_beacon_signal(cls):
        """
        Returns the signal signature of the Prime Beacon.
        """
        return {
            'prime': cls.GRAVITY_PRIME,
            'intensity': 1000.0, # High intensity beacon
            'message': "CONVERGE"
        }
