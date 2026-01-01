"""
HARMONIA-DSL v10.0: Cross-Layer Coupling
Deep mathematical links between cognitive layers

This module implements the coupling terms from the advanced GHE formulation,
creating emergent, synergistic behavior across all layers.

Author: Manus AI
Date: January 1, 2026
"""

import numpy as np
import math
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, field

# Import v9.0 components
try:
    from continuous_dynamics import (
        ContinuousState,
        ContinuousTimeIntegrator,
        HarmoniaODESystem
    )
except ImportError:
    print("Warning: Could not import v9.0 components. Make sure continuous_dynamics.py is available.")


@dataclass
class CoupledState:
    """Extended state for coupled dynamics."""
    # Original 7 state variables
    psi: float = 10.0
    phi: float = 8.0
    omega: float = 1.0
    epsilon: float = 0.1
    energy: float = 100.0
    knowledge: float = 0.0
    maturity: float = 0.0
    
    # New coupling state variables
    i_coherence: float = 0.0  # Integrated ∫(ΔΩ/S)dt
    delta_phi_accum: float = 0.0  # Accumulated ΔΦ
    psi_memory: float = 10.0  # Memory state (Ψ±)
    
    time: float = 0.0
    
    def to_vector(self) -> np.ndarray:
        """Convert to numpy vector."""
        return np.array([
            self.psi, self.phi, self.omega, self.epsilon,
            self.energy, self.knowledge, self.maturity,
            self.i_coherence, self.delta_phi_accum, self.psi_memory
        ])
    
    @classmethod
    def from_vector(cls, vec: np.ndarray, time: float = 0.0):
        """Create from numpy vector."""
        return cls(
            psi=float(vec[0]),
            phi=float(vec[1]),
            omega=float(vec[2]),
            epsilon=float(vec[3]),
            energy=float(vec[4]),
            knowledge=float(vec[5]),
            maturity=float(vec[6]),
            i_coherence=float(vec[7]),
            delta_phi_accum=float(vec[8]),
            psi_memory=float(vec[9]),
            time=time
        )
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'psi': self.psi,
            'phi': self.phi,
            'omega': self.omega,
            'epsilon': self.epsilon,
            'energy': self.energy,
            'knowledge': self.knowledge,
            'maturity': self.maturity,
            'i_coherence': self.i_coherence,
            'delta_phi_accum': self.delta_phi_accum,
            'psi_memory': self.psi_memory,
            'time': self.time
        }


class CrossLayerCouplingEngine:
    """
    Computes cross-layer coupling terms from the advanced GHE formulation.
    
    Implements three primary coupling mechanisms:
    1. Memory-Ethics: (Ψ± * K) / (Φ * β) * exp[-∫(ΔΩ/S)dt]
    2. Energy-Growth: [Cξ * (Eψ/R)] * tanh(ΓΛ√Ξ)
    3. Accumulation-Intention: Σ(ΔΦ * Ω) / (Θn * F(P) + V)
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize coupling engine.
        
        Args:
            config: Configuration dictionary
        """
        if config is None:
            config = {}
        
        # Coupling strength parameters
        self.C_me = config.get('C_memory_ethics', 0.1)
        self.C_ai = config.get('C_accumulation_intention', 0.05)
        self.C_eg = config.get('C_energy_growth', 0.2)
        
        # Safety parameters
        self.epsilon_safe = 1e-6  # Prevent division by zero
        self.clip_exp = 10.0  # Clip exponential arguments
        
        # Ethical weighting (β from GHE)
        self.beta = config.get('beta', 1.0)
    
    def compute_memory_ethics_coupling(
        self,
        psi_memory: float,
        knowledge: float,
        phi: float,
        i_coherence: float,
        entropy: float
    ) -> float:
        """
        Compute memory-ethics coupling term.
        
        Formula: (Ψ± * K) / (Φ * β) * exp[-∫(ΔΩ/S)dt]
        
        Args:
            psi_memory: Memory state (Ψ±)
            knowledge: Knowledge accumulation (K)
            phi: Ethics (Φ)
            i_coherence: Integrated coherence change
            entropy: System entropy (S)
            
        Returns:
            coupling: Memory-ethics coupling contribution
        """
        # Numerator: memory * knowledge
        numerator = psi_memory * knowledge
        
        # Denominator: ethics * beta (with safety epsilon)
        denominator = max(phi * self.beta, self.epsilon_safe)
        
        # Exponential decay term
        if entropy > self.epsilon_safe:
            exp_arg = -i_coherence / entropy
            exp_arg = np.clip(exp_arg, -self.clip_exp, self.clip_exp)
            exp_term = np.exp(exp_arg)
        else:
            exp_term = 1.0
        
        coupling = self.C_me * (numerator / denominator) * exp_term
        
        return coupling
    
    def compute_energy_growth_coupling(
        self,
        capacity: float,
        consumption: float,
        energy: float,
        response: float,
        maturity: float,
        stability: float
    ) -> float:
        """
        Compute energy-growth coupling term.
        
        Formula: [Cξ * (Eψ/R)] * tanh(ΓΛ√Ξ)
        
        Args:
            capacity: Energy capacity (C)
            consumption: Energy consumption rate (ξ)
            energy: Available energy (Eψ)
            response: Harmonic response (R)
            maturity: Growth level (Γ)
            stability: System stability (Λ, approximated by Ξ)
            
        Returns:
            coupling: Energy-growth coupling contribution
        """
        # Energy ratio term
        response_safe = max(response, self.epsilon_safe)
        energy_ratio = energy / response_safe
        
        # Capacity-consumption product
        c_xi = capacity * consumption
        
        # Tanh saturation term
        stability_safe = max(stability, self.epsilon_safe)
        tanh_arg = maturity * np.sqrt(stability_safe)
        tanh_term = np.tanh(tanh_arg)
        
        coupling = self.C_eg * c_xi * energy_ratio * tanh_term
        
        return coupling
    
    def compute_accumulation_intention_coupling(
        self,
        delta_phi_accum: float,
        omega: float,
        theta_n: float,
        intention: float,
        velocity: float
    ) -> float:
        """
        Compute accumulation-intention coupling term.
        
        Formula: Σ(ΔΦ * Ω) / (Θn * F(P) + V)
        
        Args:
            delta_phi_accum: Accumulated ethical changes (ΔΦ)
            omega: Coherence (Ω)
            theta_n: Layer accumulation (Θn)
            intention: Intentional action (F(P))
            velocity: Agent velocity (V)
            
        Returns:
            coupling: Accumulation-intention coupling contribution
        """
        # Numerator: accumulated ethics * coherence
        numerator = delta_phi_accum * omega
        
        # Denominator: thought layers + intention + velocity
        denominator = max(theta_n * intention + velocity, self.epsilon_safe)
        
        coupling = self.C_ai * (numerator / denominator)
        
        return coupling


class CoupledHarmoniaODESystem:
    """
    Extended ODE system with cross-layer coupling.
    
    Extends the v9.0 HarmoniaODESystem to include coupling terms
    in the derivative calculations.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize coupled ODE system.
        
        Args:
            config: Configuration dictionary
        """
        if config is None:
            config = {}
        
        # Initialize base ODE system parameters
        self.alpha_psi = config.get('alpha_psi', 0.1)
        self.alpha_phi = config.get('alpha_phi', 0.02)
        self.alpha_omega = config.get('alpha_omega', 0.05)
        self.alpha_epsilon = config.get('alpha_epsilon', 0.02)
        
        self.beta_knowledge = config.get('beta_knowledge', 0.01)
        self.gamma_growth = config.get('gamma_growth', 0.001)
        
        self.energy_consumption = config.get('energy_consumption', 0.5)
        self.recharge_rate = config.get('recharge_rate', 2.0)
        
        self.coupling_memory_ethics = config.get('coupling_memory_ethics', 0.05)
        self.coupling_coherence = config.get('coupling_coherence', 0.1)
        
        # Initialize coupling engine
        self.coupling_engine = CrossLayerCouplingEngine(config)
        
        # Track previous phi for ΔΦ calculation
        self.prev_phi = None
    
    def derivatives(
        self,
        t: float,
        state: np.ndarray,
        inputs: Optional[Dict] = None
    ) -> np.ndarray:
        """
        Compute derivatives with coupling terms.
        
        Args:
            t: Current time
            state: State vector [10 dimensions]
            inputs: External inputs
            
        Returns:
            derivatives: [10 dimensions]
        """
        if inputs is None:
            inputs = {}
        
        # Unpack state (10 dimensions)
        psi, phi, omega, epsilon, energy, knowledge, maturity = state[:7]
        i_coherence, delta_phi_accum, psi_memory = state[7:]
        
        # External inputs
        velocity = inputs.get('velocity', 0.0)
        external_psi = inputs.get('psi', 0.0)
        intention = inputs.get('intention', 0.5)
        
        # Compute base derivatives (from v9.0)
        dpsi_dt_base = self._dpsi_dt_base(psi, phi, omega, epsilon, energy, external_psi)
        dphi_dt_base = self._dphi_dt_base(phi, psi, knowledge, maturity)
        domega_dt = self._domega_dt(omega, psi, phi, epsilon)
        depsilon_dt = self._depsilon_dt(epsilon, energy, velocity)
        denergy_dt = self._denergy_dt(energy, velocity)
        dknowledge_dt = self._dknowledge_dt(knowledge, psi, omega)
        dmaturity_dt_base = self._dmaturity_dt_base(maturity, psi, energy, knowledge)
        
        # Compute coupling terms
        entropy = max(epsilon, 0.01)  # Use epsilon as proxy for entropy
        
        # 1. Memory-Ethics Coupling (affects awareness)
        me_coupling = self.coupling_engine.compute_memory_ethics_coupling(
            psi_memory, knowledge, phi, i_coherence, entropy
        )
        
        # 2. Energy-Growth Coupling (affects maturity)
        response = (psi + phi) * (1 - epsilon)  # Approximate R
        capacity = 100.0  # Nominal capacity
        consumption = velocity * self.energy_consumption
        stability = omega  # Use coherence as proxy for stability
        
        eg_coupling = self.coupling_engine.compute_energy_growth_coupling(
            capacity, consumption, energy, response, maturity, stability
        )
        
        # 3. Accumulation-Intention Coupling (affects ethics)
        theta_n = 1.0 + knowledge  # Approximate layer accumulation
        
        ai_coupling = self.coupling_engine.compute_accumulation_intention_coupling(
            delta_phi_accum, omega, theta_n, intention, velocity
        )
        
        # Apply couplings to derivatives
        dpsi_dt = dpsi_dt_base + me_coupling
        dphi_dt = dphi_dt_base + ai_coupling
        dmaturity_dt = dmaturity_dt_base * (1 + eg_coupling)  # Multiplicative for growth
        
        # Derivatives for coupling state variables
        di_coherence_dt = domega_dt / max(entropy, 0.01)  # ∫(ΔΩ/S)dt
        
        # ΔΦ accumulation
        if self.prev_phi is not None:
            delta_phi = phi - self.prev_phi
        else:
            delta_phi = 0.0
        self.prev_phi = phi
        
        ddelta_phi_accum_dt = delta_phi * 100  # Scale up for visibility
        
        # Memory state evolution (simple decay toward current psi)
        dpsi_memory_dt = 0.1 * (psi - psi_memory)
        
        return np.array([
            dpsi_dt, dphi_dt, domega_dt, depsilon_dt,
            denergy_dt, dknowledge_dt, dmaturity_dt,
            di_coherence_dt, ddelta_phi_accum_dt, dpsi_memory_dt
        ])
    
    # Base derivative methods (from v9.0)
    def _dpsi_dt_base(self, psi, phi, omega, epsilon, energy, external_psi):
        coherence_drive = omega * (1 - epsilon)
        decay = -self.alpha_psi * psi
        external_drive = external_psi * 0.1
        return coherence_drive + decay + external_drive
    
    def _dphi_dt_base(self, phi, psi, knowledge, maturity):
        learning_influence = self.coupling_memory_ethics * psi * knowledge
        growth_influence = 0.1 * maturity
        decay = -self.alpha_phi * phi
        return learning_influence + growth_influence + decay
    
    def _domega_dt(self, omega, psi, phi, epsilon):
        harmony = (psi + phi) * (1 - epsilon)
        coherence_drive = self.coupling_coherence * harmony
        decay = -self.alpha_omega * omega
        return coherence_drive + decay
    
    def _depsilon_dt(self, epsilon, energy, velocity):
        activity_increase = velocity * 0.01
        energy_decrease = -energy * 0.001
        natural_growth = self.alpha_epsilon * epsilon
        
        if epsilon >= 0.9 and activity_increase > 0:
            activity_increase *= 0.1
        if epsilon <= 0.05 and energy_decrease < 0:
            energy_decrease *= 0.1
        
        return activity_increase + energy_decrease + natural_growth
    
    def _denergy_dt(self, energy, velocity):
        consumption = -self.energy_consumption * velocity
        recharge = self.recharge_rate
        
        if energy >= 150 and recharge > 0:
            recharge = 0
        if energy <= 0 and consumption < 0:
            consumption = 0
        
        return consumption + recharge
    
    def _dknowledge_dt(self, knowledge, psi, omega):
        learning_rate = self.beta_knowledge * psi * omega
        return learning_rate
    
    def _dmaturity_dt_base(self, maturity, psi, energy, knowledge):
        growth_rate = self.gamma_growth * psi * energy * knowledge
        logistic_term = (1 - maturity)
        return growth_rate * logistic_term


class CoupledFluidHarmoniaIntegrator:
    """
    High-level interface for coupled continuous-time dynamics.
    
    Extends v9.0 FluidHarmoniaIntegrator with cross-layer coupling.
    """
    
    def __init__(self, config: Optional[Dict] = None, dt: float = 0.01):
        """
        Initialize coupled fluid integrator.
        
        Args:
            config: Configuration dictionary
            dt: Integration time step
        """
        self.config = config or {}
        self.dt = dt
        
        self.ode_system = CoupledHarmoniaODESystem(config)
        self.integrator = ContinuousTimeIntegrator(method='rk4', dt=dt)
        
        self.state = CoupledState()
        self.history = []
    
    def process(
        self,
        inputs: Optional[Dict] = None,
        duration: float = 1.0
    ) -> Dict:
        """
        Process inputs over a duration with coupling.
        
        Args:
            inputs: External inputs
            duration: Time duration to integrate
            
        Returns:
            result: Dictionary with state and trajectory
        """
        if inputs is None:
            inputs = {}
        
        t0 = self.state.time
        state0 = self.state.to_vector()
        t_final = t0 + duration
        
        def f(t, state, params):
            return self.ode_system.derivatives(t, state, inputs)
        
        t_values, state_values = self.integrator.integrate(
            f, t0, state0, t_final
        )
        
        self.state = CoupledState.from_vector(state_values[-1], t_values[-1])
        
        self.history.append({
            't': t_values[-1],
            'state': self.state.to_dict()
        })
        
        R = self._compute_harmonic_response()
        
        return {
            'R': R,
            'state': self.state.to_dict(),
            'trajectory': {
                't': t_values,
                'states': state_values
            }
        }
    
    def _compute_harmonic_response(self) -> float:
        """Compute harmonic response with coupling effects."""
        s = self.state
        
        base = (s.psi + s.phi) * (1 - s.epsilon)
        energy_term = s.energy / 100.0 if s.energy > 0 else 0.0
        learning_term = s.knowledge * s.maturity
        coherence_term = s.omega
        
        # Coupling contribution
        coupling_term = 0.1 * s.i_coherence + 0.05 * s.delta_phi_accum
        
        R = base * energy_term + learning_term + coherence_term + coupling_term
        
        return float(R)
    
    def get_state(self) -> Dict:
        """Get current state."""
        return self.state.to_dict()
    
    def reset(self):
        """Reset to initial state."""
        self.state = CoupledState()
        self.history = []
        self.ode_system.prev_phi = None


# Demo
if __name__ == "__main__":
    print("=" * 70)
    print("HARMONIA-DSL v10.0: Cross-Layer Coupling Demo")
    print("=" * 70)
    print()
    
    agent = CoupledFluidHarmoniaIntegrator(dt=0.01)
    
    print("Initial State:")
    print(f"  Awareness (Ψ): {agent.state.psi:.2f}")
    print(f"  Ethics (Φ): {agent.state.phi:.2f}")
    print(f"  Memory (Ψ±): {agent.state.psi_memory:.2f}")
    print()
    
    print("Simulating 5 seconds with coupling enabled...")
    result = agent.process(inputs={'velocity': 1.0, 'intention': 0.8}, duration=5.0)
    
    print(f"\nFinal State (t={agent.state.time:.2f}s):")
    print(f"  Awareness (Ψ): {agent.state.psi:.2f}")
    print(f"  Ethics (Φ): {agent.state.phi:.2f}")
    print(f"  Memory (Ψ±): {agent.state.psi_memory:.2f}")
    print(f"  Integrated Coherence: {agent.state.i_coherence:.3f}")
    print(f"  Accumulated ΔΦ: {agent.state.delta_phi_accum:.3f}")
    print(f"  Harmonic Response (R): {result['R']:.2f}")
    
    print("\n✓ Cross-layer coupling successfully implemented!")
    print("✓ Memory, ethics, and growth are now deeply interlinked!")
