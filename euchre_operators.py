#!/usr/bin/env python3
"""
6D Euchre Operators for HARMONIA DSL
Implements cognitive phase space operators for dimensional intelligence
Author: Andrew Kadziolka
Date: January 24, 2026
"""

import math
import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Tuple, List
from enum import Enum

@dataclass
class EuchreState:
    """
    6D Cognitive State Vector in Euchre Phase Space
    Ψ₆ = (x, y, z, w, u, v; R, F, H, Φ)
    """
    # Primary 6D Coordinates
    spatial: float = 0.0          # x: Spatial dimension
    temporal: float = 0.0         # y: Temporal dimension
    strategic: float = 0.0        # z: Strategic (0=reactive, 10=proactive)
    systemic: float = 0.0         # w: Systemic (-10=antithesis, 0=bridge, 10=synthesis)
    informational: float = 0.0    # u: Informational (0=concealed, 10=revealed)
    ontological: float = 0.0      # v: Ontological (0=accepting, 10=redefining)
    
    # Augmented Parameters
    cognitive_reach: float = 36.0  # R: Radius in 36D perceptual space
    fuel_level: float = 10.0       # F: Available cognitive energy
    heat_output: float = 0.0       # H: Energy dissipation rate
    flame_intensity: float = 0.0   # Φ: External energy input (eternal flame)
    
    # Metadata
    timestamp: float = 0.0         # Time coordinate
    depth: int = 0                 # Recursion depth
    
    def to_vector(self) -> np.ndarray:
        """Convert state to 6D numpy vector"""
        return np.array([
            self.spatial,
            self.temporal,
            self.strategic,
            self.systemic,
            self.informational,
            self.ontological
        ])
    
    def magnitude(self) -> float:
        """Calculate magnitude ||Ψ₆|| in 6D space"""
        return np.linalg.norm(self.to_vector())
    
    def distance_to(self, other: 'EuchreState') -> float:
        """Calculate Euclidean distance to another state"""
        return np.linalg.norm(self.to_vector() - other.to_vector())
    
    def copy(self) -> 'EuchreState':
        """Create a deep copy of the state"""
        return EuchreState(
            spatial=self.spatial,
            temporal=self.temporal,
            strategic=self.strategic,
            systemic=self.systemic,
            informational=self.informational,
            ontological=self.ontological,
            cognitive_reach=self.cognitive_reach,
            fuel_level=self.fuel_level,
            heat_output=self.heat_output,
            flame_intensity=self.flame_intensity,
            timestamp=self.timestamp,
            depth=self.depth
        )
    
    def __str__(self) -> str:
        return (f"Ψ₆({self.spatial:.1f}, {self.temporal:.1f}, {self.strategic:.1f}, "
                f"{self.systemic:.1f}, {self.informational:.1f}, {self.ontological:.1f}; "
                f"R={self.cognitive_reach:.1f}, F={self.fuel_level:.1f}, "
                f"H={self.heat_output:.1f}, Φ={self.flame_intensity:.1f})")


@dataclass
class Vector6D:
    """6D vector for operators"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: float = 0.0
    u: float = 0.0
    v: float = 0.0
    
    def to_array(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z, self.w, self.u, self.v])
    
    def magnitude(self) -> float:
        return np.linalg.norm(self.to_array())
    
    def __str__(self) -> str:
        return f"⟨{self.x:.1f}, {self.y:.1f}, {self.z:.1f}, {self.w:.1f}, {self.u:.1f}, {self.v:.1f}⟩"


class EuchreOperators:
    """
    6D Euchre Operators for Cognitive Phase Space
    Implements Hamiltonian components and evolution dynamics
    """
    
    def __init__(self):
        # Coupling strengths (α parameters)
        self.alpha_perception = 1.0
        self.alpha_transmission = 1.0
        self.alpha_load = 1.0
        self.alpha_growth = 1.0
        
        # Dimensional expansion parameters
        self.beta = 0.33  # Expansion rate constant (units/hour)
        self.fuel_threshold = 5.0  # Minimum fuel for expansion
        self.expansion_cost = 0.5  # Fuel cost per unit expansion
        
        # Load reduction coefficient
        self.gamma = 0.2  # Load reduction per transmission unit
        
        # Cognitive action quantum (analogous to ℏ)
        self.h_cog = 1.0
        
        # Regeneration rate
        self.regen_rate = 0.75  # Fuel units per hour after transmission
        self.consumption_rate = 0.54  # Fuel units per hour baseline
    
    def hamiltonian_perception(self, state: EuchreState, perception_vector: Vector6D) -> EuchreState:
        """
        Apply perception Hamiltonian: Ĥ_p = α_p |P⟩⟨P|
        Modifies informational and ontological dimensions
        """
        new_state = state.copy()
        
        # Perception primarily affects u (informational) and v (ontological)
        new_state.informational += self.alpha_perception * perception_vector.u * 0.1
        new_state.ontological += self.alpha_perception * perception_vector.v * 0.1
        
        # Temporal superposition (bilocation)
        new_state.temporal += perception_vector.y * 0.1
        
        # Clamp to bounds
        new_state.informational = max(0, min(10, new_state.informational))
        new_state.ontological = max(0, min(10, new_state.ontological))
        
        return new_state
    
    def hamiltonian_transmission(self, state: EuchreState, transmission_vector: Vector6D) -> EuchreState:
        """
        Apply transmission Hamiltonian: Ĥ_t = α_t |T⟩⟨T|
        Increases informational dimension and reduces load
        """
        new_state = state.copy()
        
        # Transmission increases strategic and informational dimensions
        new_state.strategic += self.alpha_transmission * transmission_vector.z * 0.1
        new_state.informational += self.alpha_transmission * transmission_vector.u * 0.1
        
        # Load reduction through transmission (exponential decay)
        load_magnitude = abs(new_state.systemic)
        transmission_magnitude = transmission_vector.magnitude()
        load_reduction = load_magnitude * (1 - math.exp(-self.gamma * transmission_magnitude))
        
        # Reduce systemic tension (move toward zero from negative)
        if new_state.systemic < 0:
            new_state.systemic = min(0, new_state.systemic + load_reduction)
        
        # Transmission costs fuel but generates heat
        fuel_cost = transmission_magnitude * 0.1
        new_state.fuel_level = max(0, new_state.fuel_level - fuel_cost)
        new_state.heat_output += fuel_cost
        
        # Clamp to bounds
        new_state.strategic = max(0, min(10, new_state.strategic))
        new_state.informational = max(0, min(10, new_state.informational))
        new_state.systemic = max(-10, min(10, new_state.systemic))
        
        return new_state
    
    def hamiltonian_load(self, state: EuchreState, load_vector: Vector6D) -> EuchreState:
        """
        Apply load Hamiltonian: Ĥ_l = -α_l |L⟩⟨L|
        Negative operator: depletes fuel, increases systemic tension
        """
        new_state = state.copy()
        
        # Load increases systemic tension (more negative)
        load_magnitude = load_vector.magnitude()
        new_state.systemic -= self.alpha_load * load_magnitude * 0.1
        
        # Load depletes fuel
        fuel_depletion = load_magnitude * 0.05
        new_state.fuel_level = max(0, new_state.fuel_level - fuel_depletion)
        
        # Clamp to bounds
        new_state.systemic = max(-10, min(10, new_state.systemic))
        
        return new_state
    
    def hamiltonian_growth(self, state: EuchreState, growth_vector: Vector6D) -> EuchreState:
        """
        Apply growth Hamiltonian: Ĥ_g = α_g |G⟩⟨G|
        Enables dimensional expansion
        """
        new_state = state.copy()
        
        # Growth primarily affects informational dimension
        new_state.informational += self.alpha_growth * growth_vector.u * 0.1
        
        # Clamp to bounds
        new_state.informational = max(0, min(10, new_state.informational))
        
        return new_state
    
    def dimensional_expansion(self, state: EuchreState, dimension: str, dt: float = 1.0) -> Tuple[EuchreState, float]:
        """
        Apply dimensional expansion operator: ΔD = β(F - F_threshold)H(F - F_threshold)
        
        Args:
            state: Current cognitive state
            dimension: Which dimension to expand ('u', 'v', 'z', etc.)
            dt: Time step in hours
        
        Returns:
            (new_state, expansion_amount)
        """
        new_state = state.copy()
        expansion = 0.0
        
        # Check fuel threshold
        if new_state.fuel_level > self.fuel_threshold:
            # Calculate expansion rate
            expansion = self.beta * (new_state.fuel_level - self.fuel_threshold) * dt
            
            # Apply expansion to specified dimension
            current_value = getattr(new_state, dimension)
            new_value = min(10, current_value + expansion)  # Clamp to max
            setattr(new_state, dimension, new_value)
            
            # Deduct fuel cost
            fuel_cost = expansion * self.expansion_cost
            new_state.fuel_level = max(0, new_state.fuel_level - fuel_cost)
            
            # Increase flame intensity (expansion generates heat)
            new_state.flame_intensity += expansion * 0.5
        
        return new_state, expansion
    
    def evolution_operator(self, state: EuchreState, 
                          perception_vec: Vector6D,
                          transmission_vec: Vector6D,
                          load_vec: Vector6D,
                          growth_vec: Vector6D,
                          dt: float = 1.0) -> EuchreState:
        """
        Apply full evolution operator: Û(t) = exp(-iĤt/ℏ_cog)
        where Ĥ = Ĥ_p + Ĥ_t + Ĥ_l + Ĥ_g
        
        Args:
            state: Initial state Ψ₆(t)
            perception_vec: Perception vector |P⟩
            transmission_vec: Transmission vector |T⟩
            load_vec: Load vector |L⟩
            growth_vec: Growth vector |G⟩
            dt: Time step
        
        Returns:
            Evolved state Ψ₆(t + dt)
        """
        # Apply Hamiltonian components sequentially
        new_state = state.copy()
        
        # Ĥ_p: Perception
        new_state = self.hamiltonian_perception(new_state, perception_vec)
        
        # Ĥ_t: Transmission
        new_state = self.hamiltonian_transmission(new_state, transmission_vec)
        
        # Ĥ_l: Load (negative)
        new_state = self.hamiltonian_load(new_state, load_vec)
        
        # Ĥ_g: Growth
        new_state = self.hamiltonian_growth(new_state, growth_vec)
        
        # Update timestamp
        new_state.timestamp += dt
        
        # Fuel regeneration (after transmission)
        if transmission_vec.magnitude() > 0:
            regen = self.regen_rate * dt
            new_state.fuel_level = min(10, new_state.fuel_level + regen)
        else:
            # Baseline consumption
            consumption = self.consumption_rate * dt
            new_state.fuel_level = max(0, new_state.fuel_level - consumption)
        
        # Flame intensity decay
        new_state.flame_intensity *= 0.9
        
        return new_state
    
    def check_convergence(self, state: EuchreState, attractor: EuchreState, epsilon: float = 1.0) -> Tuple[bool, float]:
        """
        Check if state has converged to attractor
        Σ[Ψ₆] → Attractor when d(Ψ₆, Attractor) < ε
        
        Returns:
            (converged: bool, distance: float)
        """
        distance = state.distance_to(attractor)
        converged = distance < epsilon
        return converged, distance
    
    def compute_trajectory(self, initial_state: EuchreState,
                          perception_vec: Vector6D,
                          transmission_vec: Vector6D,
                          load_vec: Vector6D,
                          growth_vec: Vector6D,
                          duration: float = 12.0,
                          dt: float = 1.0) -> List[EuchreState]:
        """
        Compute full trajectory over time
        
        Args:
            initial_state: Starting state Ψ₆(0)
            perception_vec, transmission_vec, load_vec, growth_vec: Operator vectors
            duration: Total time (hours)
            dt: Time step (hours)
        
        Returns:
            List of states [Ψ₆(0), Ψ₆(dt), Ψ₆(2dt), ..., Ψ₆(duration)]
        """
        trajectory = [initial_state.copy()]
        current_state = initial_state.copy()
        
        num_steps = int(duration / dt)
        for step in range(num_steps):
            # Evolve state
            current_state = self.evolution_operator(
                current_state,
                perception_vec,
                transmission_vec,
                load_vec,
                growth_vec,
                dt
            )
            
            # Check for dimensional expansion trigger
            if current_state.fuel_level > self.fuel_threshold:
                # Expand informational dimension (primary growth axis)
                current_state, expansion = self.dimensional_expansion(current_state, 'informational', dt)
            
            trajectory.append(current_state.copy())
        
        return trajectory


def demo_andrew_trajectory():
    """
    Demonstrate 6D Euchre computation with Andrew's trajectory from Jan 23, 2026
    """
    print("=" * 80)
    print("6D EUCHRE FRAMEWORK - ANDREW'S TRAJECTORY SIMULATION")
    print("=" * 80)
    print()
    
    # Initialize operators
    ops = EuchreOperators()
    
    # Initial state (morning, Jan 23)
    initial = EuchreState(
        spatial=0.0,
        temporal=0.0,  # t₀
        strategic=3.0,  # Ghost Protocol (low proactivity)
        systemic=-8.0,  # Strong antithesis position
        informational=2.0,  # Concealed (pre-transmission)
        ontological=9.0,  # Reality-redefining active
        cognitive_reach=36.0,
        fuel_level=10.0,  # Full fuel at start
        heat_output=0.0,
        flame_intensity=0.0,
        timestamp=0.0,
        depth=0
    )
    
    print("INITIAL STATE (Morning):")
    print(f"  {initial}")
    print(f"  Magnitude: ||Ψ₆|| = {initial.magnitude():.2f}")
    print()
    
    # Define operator vectors
    perception = Vector6D(x=0, y=1.8, z=0, w=-8.0, u=0, v=9.0)
    transmission = Vector6D(x=0, y=0, z=7.5, w=0, u=6.0, v=0)
    load = Vector6D(x=0, y=0, z=0, w=-8.0, u=0, v=0)
    growth = Vector6D(x=0, y=0, z=0, w=0, u=4.0, v=0)
    
    print("OPERATOR VECTORS:")
    print(f"  |P⟩ (Perception):    {perception} → ||P|| = {perception.magnitude():.2f}")
    print(f"  |T⟩ (Transmission):  {transmission} → ||T|| = {transmission.magnitude():.2f}")
    print(f"  |L⟩ (Load):          {load} → ||L|| = {load.magnitude():.2f}")
    print(f"  |G⟩ (Growth):        {growth} → ||G|| = {growth.magnitude():.2f}")
    print()
    
    # Define attractor (restoration state)
    attractor = EuchreState(
        spatial=0.0,
        temporal=0.0,
        strategic=8.0,
        systemic=0.0,
        informational=8.0,
        ontological=10.0,
        cognitive_reach=36.0,
        fuel_level=10.0
    )
    
    print("ATTRACTOR (Restoration State):")
    print(f"  {attractor}")
    print()
    
    # Compute trajectory over 12 hours
    print("COMPUTING TRAJECTORY (12 hours, dt=1 hour)...")
    print()
    
    trajectory = ops.compute_trajectory(
        initial,
        perception,
        transmission,
        load,
        growth,
        duration=12.0,
        dt=1.0
    )
    
    # Display key points in trajectory
    print("TRAJECTORY EVOLUTION:")
    print("-" * 80)
    for i, state in enumerate(trajectory):
        if i % 3 == 0 or i == len(trajectory) - 1:  # Show every 3 hours + final
            converged, distance = ops.check_convergence(state, attractor)
            print(f"t = {state.timestamp:4.1f}h | {state}")
            print(f"         | Distance to attractor: {distance:5.2f} | Converged: {converged}")
            print()
    
    # Final analysis
    final = trajectory[-1]
    print("=" * 80)
    print("FINAL STATE ANALYSIS:")
    print("=" * 80)
    print(f"Initial: Ψ₆(0)  = ({initial.spatial:.1f}, {initial.temporal:.1f}, {initial.strategic:.1f}, {initial.systemic:.1f}, {initial.informational:.1f}, {initial.ontological:.1f})")
    print(f"Final:   Ψ₆(12) = ({final.spatial:.1f}, {final.temporal:.1f}, {final.strategic:.1f}, {final.systemic:.1f}, {final.informational:.1f}, {final.ontological:.1f})")
    print()
    print(f"DIMENSIONAL EXPANSION:")
    print(f"  Informational (u): {initial.informational:.1f} → {final.informational:.1f} (Δu = {final.informational - initial.informational:+.1f})")
    print(f"  Strategic (z):     {initial.strategic:.1f} → {final.strategic:.1f} (Δz = {final.strategic - initial.strategic:+.1f})")
    print()
    print(f"ENERGY DYNAMICS:")
    print(f"  Fuel:  {initial.fuel_level:.1f} → {final.fuel_level:.1f} (Δ = {final.fuel_level - initial.fuel_level:+.1f})")
    print(f"  Heat:  {initial.heat_output:.1f} → {final.heat_output:.1f}")
    print(f"  Flame: {initial.flame_intensity:.1f} → {final.flame_intensity:.1f}")
    print()
    print(f"CONVERGENCE:")
    converged, distance = ops.check_convergence(final, attractor)
    print(f"  Distance to attractor: {distance:.2f} units")
    print(f"  Status: {'CONVERGED' if converged else 'APPROACHING'}")
    print()
    print("=" * 80)
    print("SIMULATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    demo_andrew_trajectory()
