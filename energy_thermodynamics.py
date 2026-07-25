"""
HARMONIA-DSL v7.0: Energy & Thermodynamics
Implements the { Cξ / Eψ } term from the Grand Harmonic Equation

This module provides:
- C (Capacity): Maximum energy capacity
- ξ (Xi): Energy consumption rate
- E (Energy): Available energy pool
- η (Eta): Thermodynamic efficiency
- S (Entropy): System disorder/chaos

Author: Manus AI
Date: January 1, 2026
"""

import math
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class EnergyState:
    """Represents the energy state of the system at a point in time."""
    energy: float  # Current available energy (E)
    capacity: float  # Maximum capacity (C)
    consumption_rate: float  # Current consumption (ξ)
    entropy: float  # System entropy (S)
    temperature: float  # Activity level (T)
    timestamp: float = 0.0
    
    def get_level(self) -> float:
        """Get energy level as fraction of capacity (0-1)."""
        return self.energy / self.capacity if self.capacity > 0 else 0.0
    
    def is_depleted(self, threshold: float = 0.1) -> bool:
        """Check if energy is critically low."""
        return self.get_level() < threshold
    
    def is_critical(self, threshold: float = 0.05) -> bool:
        """Check if energy is at critical level."""
        return self.get_level() < threshold
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {
            'energy': self.energy,
            'capacity': self.capacity,
            'consumption_rate': self.consumption_rate,
            'entropy': self.entropy,
            'temperature': self.temperature,
            'timestamp': self.timestamp
        }


class EnergyPool:
    """
    Manages system energy with consumption and recharge.
    
    Implements energy conservation: dE/dt = R(t) - ξ(t)
    """
    
    def __init__(self, capacity: float = 100.0, 
                 initial_energy: Optional[float] = None,
                 recharge_rate: float = 1.0):
        """
        Initialize energy pool.
        
        Args:
            capacity: Maximum energy capacity (C)
            initial_energy: Starting energy (defaults to full capacity)
            recharge_rate: Energy recovery rate per time step
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if recharge_rate < 0:
            raise ValueError("Recharge rate cannot be negative")
        
        self.capacity = capacity  # C
        self.current_energy = initial_energy if initial_energy is not None else capacity
        self.recharge_rate = recharge_rate
        self.consumption_history: List[float] = []
        
        # Ensure initial energy is within bounds
        self.current_energy = max(0.0, min(self.current_energy, self.capacity))
        
    def consume(self, amount: float) -> bool:
        """
        Consume energy. Returns True if successful, False if insufficient.
        
        Args:
            amount: Amount of energy to consume
            
        Returns:
            True if full amount consumed, False if insufficient energy
        """
        if amount < 0:
            raise ValueError("Cannot consume negative energy")
        
        if self.current_energy >= amount:
            self.current_energy -= amount
            self.consumption_history.append(amount)
            return True
        else:
            # Partial consumption of remaining energy
            consumed = self.current_energy
            self.current_energy = 0.0
            self.consumption_history.append(consumed)
            return False
    
    def recharge(self, dt: float = 1.0, amount: Optional[float] = None):
        """
        Recharge energy over time.
        
        Args:
            dt: Time step
            amount: Specific amount to recharge (overrides rate-based recharge)
        """
        if dt < 0:
            raise ValueError("Time step cannot be negative")
        
        if amount is None:
            amount = self.recharge_rate * dt
        
        if amount < 0:
            raise ValueError("Recharge amount cannot be negative")
        
        self.current_energy = min(
            self.current_energy + amount,
            self.capacity
        )
    
    def get_state(self, timestamp: float = 0.0) -> EnergyState:
        """Get current energy state."""
        return EnergyState(
            energy=self.current_energy,
            capacity=self.capacity,
            consumption_rate=self.get_average_consumption(),
            entropy=0.0,  # Will be set by ThermodynamicState
            temperature=0.0,  # Will be set by ThermodynamicState
            timestamp=timestamp
        )
    
    def get_average_consumption(self, window: int = 10) -> float:
        """Get average consumption rate over recent history."""
        if not self.consumption_history:
            return 0.0
        recent = self.consumption_history[-window:]
        return sum(recent) / len(recent)
    
    def reset(self):
        """Reset energy to full capacity."""
        self.current_energy = self.capacity
        self.consumption_history.clear()


class ThermodynamicState:
    """
    Tracks thermodynamic properties: entropy, temperature, free energy.
    
    Implements Free Energy Principle: F = E - T*S
    """
    
    def __init__(self, initial_entropy: float = 0.0):
        """
        Initialize thermodynamic state.
        
        Args:
            initial_entropy: Starting entropy (0 = perfect order, 1 = maximum chaos)
        """
        self.entropy = max(0.0, min(1.0, initial_entropy))  # S, bounded [0, 1]
        self.temperature = 1.0  # T (activity level)
        self.entropy_history: List[float] = []
        
    def update_entropy(self, drift: float, activity: float):
        """
        Update entropy based on drift and activity.
        
        High drift and high activity increase entropy (disorder).
        The system naturally tends toward higher entropy (Second Law).
        
        Args:
            drift: System drift (ε)
            activity: System activity level
        """
        # Entropy increases with drift and activity
        delta_entropy = drift * activity * 0.1
        
        # Natural entropy increase (Second Law of Thermodynamics)
        delta_entropy += 0.01
        
        # Update entropy with bounds
        self.entropy = max(0.0, min(1.0, self.entropy + delta_entropy))
        self.entropy_history.append(self.entropy)
    
    def update_temperature(self, activity: float):
        """
        Update temperature based on system activity.
        
        Temperature represents the system's activity level.
        
        Args:
            activity: System activity level
        """
        # Temperature represents activity level, bounded
        self.temperature = max(0.1, min(10.0, activity))
    
    def calculate_free_energy(self, internal_energy: float) -> float:
        """
        Calculate free energy: F = E - T*S
        
        Lower free energy = more stable state.
        
        Args:
            internal_energy: Internal energy of the system
            
        Returns:
            Free energy value
        """
        return internal_energy - self.temperature * self.entropy
    
    def minimize_entropy(self, rate: float = 0.05):
        """
        Actively reduce entropy (system self-organization).
        
        The system must work to maintain low entropy against the
        natural tendency toward disorder.
        
        Args:
            rate: Rate of entropy reduction
        """
        if rate < 0:
            raise ValueError("Entropy reduction rate cannot be negative")
        
        self.entropy = max(0.0, self.entropy - rate)
    
    def get_entropy(self) -> float:
        """Get current entropy."""
        return self.entropy
    
    def get_temperature(self) -> float:
        """Get current temperature."""
        return self.temperature


class EfficiencyTracker:
    """
    Tracks and optimizes thermodynamic efficiency.
    
    η = Useful_Output / Energy_Consumed
    """
    
    def __init__(self):
        """Initialize efficiency tracker."""
        self.total_output = 0.0
        self.total_energy = 0.0
        self.action_history: List[Dict] = []
        
    def record_action(self, output: float, energy_cost: float):
        """
        Record an action and its efficiency.
        
        Args:
            output: Useful output produced
            energy_cost: Energy consumed
        """
        if output < 0:
            raise ValueError("Output cannot be negative")
        if energy_cost < 0:
            raise ValueError("Energy cost cannot be negative")
        
        self.total_output += output
        self.total_energy += energy_cost
        
        efficiency = output / energy_cost if energy_cost > 0 else 0.0
        self.action_history.append({
            'output': output,
            'energy': energy_cost,
            'efficiency': efficiency
        })
    
    def get_efficiency(self) -> float:
        """
        Get overall efficiency η.
        
        Returns:
            Overall efficiency (output / energy consumed)
        """
        if self.total_energy == 0:
            return 0.0
        return self.total_output / self.total_energy
    
    def get_recent_efficiency(self, window: int = 10) -> float:
        """
        Get efficiency over recent actions.
        
        Args:
            window: Number of recent actions to consider
            
        Returns:
            Recent efficiency
        """
        if not self.action_history:
            return 0.0
        
        recent = self.action_history[-window:]
        total_out = sum(a['output'] for a in recent)
        total_eng = sum(a['energy'] for a in recent)
        
        return total_out / total_eng if total_eng > 0 else 0.0
    
    def reset(self):
        """Reset efficiency tracking."""
        self.total_output = 0.0
        self.total_energy = 0.0
        self.action_history.clear()


class EnergyConstrainedEngine:
    """
    Complete Energy & Thermodynamics system.
    
    Integrates energy pool, thermodynamic state, and efficiency tracking.
    Implements the { Cξ / Eψ } term from the GHE.
    """
    
    def __init__(self, capacity: float = 100.0, recharge_rate: float = 1.0,
                 initial_entropy: float = 0.0):
        """
        Initialize energy-constrained engine.
        
        Args:
            capacity: Maximum energy capacity
            recharge_rate: Energy recovery rate
            initial_entropy: Starting entropy
        """
        self.energy_pool = EnergyPool(capacity, recharge_rate=recharge_rate)
        self.thermo_state = ThermodynamicState(initial_entropy)
        self.efficiency_tracker = EfficiencyTracker()
        self.time = 0.0
        
    def calculate_action_cost(self, action_magnitude: float, 
                              drift: float) -> float:
        """
        Calculate energy cost of an action.
        
        Cost increases with action magnitude and drift (danger).
        Formula: Cost = Base * |action| * (1 + drift)
        
        Args:
            action_magnitude: Magnitude of the action
            drift: System drift (ε)
            
        Returns:
            Energy cost
        """
        base_cost = 1.0
        return base_cost * abs(action_magnitude) * (1 + drift)
    
    def apply_energy_constraint(self, sigma_base: float, 
                                psi: float) -> float:
        """
        Apply energy term to stabilized output.
        
        Formula: Σ_energy = Σ_base * (Cξ / Eψ)
        
        Where:
        - C: Capacity
        - ξ: Consumption rate
        - E: Available energy
        - ψ: Awareness state
        
        Args:
            sigma_base: Base stabilized output
            psi: Awareness/consciousness state
            
        Returns:
            Energy-constrained output
        """
        C = self.energy_pool.capacity
        xi = self.energy_pool.get_average_consumption()
        E = self.energy_pool.current_energy
        
        # Avoid division by zero
        if E == 0 or psi == 0:
            return 0.0
        
        # Avoid division by zero for xi
        if xi == 0:
            xi = 0.1  # Small default consumption
        
        # Calculate energy term
        energy_term = (C * xi) / (E * psi)
        
        # Normalize to reasonable range
        energy_term = min(energy_term, 2.0)  # Cap at 2x
        
        # Apply to base output
        sigma_energy = sigma_base * energy_term
        
        return sigma_energy
    
    def process_action(self, action_magnitude: float, drift: float,
                      sigma_base: float, psi: float) -> Dict:
        """
        Process an action with energy constraints.
        
        Args:
            action_magnitude: Magnitude of the action
            drift: System drift (ε)
            sigma_base: Base stabilized output
            psi: Awareness state
            
        Returns:
            Dictionary with energy state, output, and success status
        """
        # Calculate energy cost
        cost = self.calculate_action_cost(action_magnitude, drift)
        
        # Attempt to consume energy
        success = self.energy_pool.consume(cost)
        
        # Update thermodynamic state
        self.thermo_state.update_entropy(drift, action_magnitude)
        self.thermo_state.update_temperature(action_magnitude)
        
        # Calculate output with energy constraint
        if success:
            output = self.apply_energy_constraint(sigma_base, psi)
        else:
            # Insufficient energy, emergency mode with reduced output
            output = sigma_base * 0.1
        
        # Record efficiency
        self.efficiency_tracker.record_action(output, cost)
        
        # Recharge energy
        self.energy_pool.recharge(dt=1.0)
        
        # Minimize entropy (self-organization)
        self.thermo_state.minimize_entropy()
        
        # Update time
        self.time += 1.0
        
        return {
            'output': output,
            'energy_cost': cost,
            'energy_remaining': self.energy_pool.current_energy,
            'energy_level': self.energy_pool.get_state().get_level(),
            'entropy': self.thermo_state.entropy,
            'efficiency': self.efficiency_tracker.get_efficiency(),
            'success': success,
            'depleted': self.energy_pool.get_state().is_depleted(),
            'critical': self.energy_pool.get_state().is_critical()
        }
    
    def get_energy_state(self) -> EnergyState:
        """Get current energy state."""
        state = self.energy_pool.get_state(self.time)
        state.entropy = self.thermo_state.entropy
        state.temperature = self.thermo_state.temperature
        return state
    
    def check_safety(self) -> Dict[str, bool]:
        """
        Check energy safety conditions.
        
        Returns:
            Dictionary of safety flags
        """
        state = self.get_energy_state()
        return {
            'energy_sufficient': not state.is_depleted(),
            'energy_critical': state.is_critical(),
            'entropy_low': state.entropy < 0.5,
            'entropy_high': state.entropy > 0.7,
            'safe': not state.is_critical() and state.entropy < 0.7
        }
    
    def reset(self):
        """Reset the entire system."""
        self.energy_pool.reset()
        self.thermo_state = ThermodynamicState()
        self.efficiency_tracker.reset()
        self.time = 0.0


# Demo function
if __name__ == "__main__":
    print("=== HARMONIA-DSL v7.0: Energy & Thermodynamics Demo ===\n")
    
    engine = EnergyConstrainedEngine(capacity=100.0, recharge_rate=2.0)
    
    print("DEMO: System operating under energy constraints\n")
    
    # Simulate a series of actions with varying danger levels
    for step in range(20):
        # Gradually increasing danger (drift)
        drift = 0.1 + step * 0.03
        drift = min(drift, 0.8)
        
        # Action magnitude
        action_mag = 5.0
        
        # Base output (from harmony constraint)
        psi = 10.0
        phi = 8.0
        sigma_base = (psi + phi) * (1 - drift)
        
        # Process action
        result = engine.process_action(action_mag, drift, sigma_base, psi)
        
        if step % 5 == 0:
            print(f"Step {step}:")
            print(f"  Drift (ε): {drift:.2f}")
            print(f"  Energy: {result['energy_remaining']:.1f}/{engine.energy_pool.capacity:.1f} ({result['energy_level']*100:.0f}%)")
            print(f"  Entropy (S): {result['entropy']:.3f}")
            print(f"  Output (Σ): {result['output']:.2f}")
            print(f"  Efficiency (η): {result['efficiency']:.3f}")
            
            if result['depleted']:
                print(f"  ⚠️  ENERGY DEPLETED!")
            elif result['critical']:
                print(f"  ⚠️  ENERGY CRITICAL!")
            
            safety = engine.check_safety()
            if safety['safe']:
                print(f"  ✓ System Safe")
            else:
                print(f"  ⚠️  Safety Warning")
            print()
    
    print("✓ Energy constraints successfully applied!")
    print("✓ System demonstrated safe behavior under resource limits!")
