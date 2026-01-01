"""
HARMONIA-DSL v11.0: Nonlinear Dynamics
Sophisticated nonlinear terms for realistic behavior

This module implements the remaining nonlinear terms from the advanced GHE
formulation, including quadratic awareness, exponential decay, and tanh saturation.

Author: Manus AI
Date: January 1, 2026
"""

import numpy as np
import math
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass, field
from collections import deque

# Import v10.0 components
try:
    from cross_layer_coupling import (
        CoupledState,
        CoupledHarmoniaODESystem,
        CoupledFluidHarmoniaIntegrator
    )
    from continuous_dynamics import ContinuousTimeIntegrator
except ImportError:
    print("Warning: Could not import v10.0 components. Make sure cross_layer_coupling.py is available.")


@dataclass
class NonlinearState(CoupledState):
    """Extended state for nonlinear dynamics."""
    # Derivative tracking for ∂Ω/∂Ψ
    domega_dpsi: float = 0.0
    
    # Thought layer count (ΘN)
    theta_n: float = 1.0
    
    # Stability measure (Λ)
    lambda_stability: float = 1.0
    
    def to_vector(self) -> np.ndarray:
        """Convert to numpy vector."""
        base_vec = super().to_vector()
        return np.append(base_vec, [self.domega_dpsi, self.theta_n, self.lambda_stability])
    
    @classmethod
    def from_vector(cls, vec: np.ndarray, time: float = 0.0):
        """Create from numpy vector."""
        base_state = CoupledState.from_vector(vec[:10], time)
        return cls(
            **base_state.__dict__,
            domega_dpsi=float(vec[10]) if len(vec) > 10 else 0.0,
            theta_n=float(vec[11]) if len(vec) > 11 else 1.0,
            lambda_stability=float(vec[12]) if len(vec) > 12 else 1.0
        )


class NonlinearDynamicsEngine:
    """
    Computes nonlinear terms from the advanced GHE formulation.
    
    Implements:
    1. Quadratic awareness: |ΨΩ|^2 * (1 - ∂Ω/∂Ψ)
    2. Exponential decay: exp[-ΘN]
    3. Tanh saturation (ethics): tanh(ΔΦ / Ω)
    4. Tanh saturation (growth): tanh(ΓΛ / Ξ)
    5. Recursive observation: Θ(Θ(N)) [simplified]
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize nonlinear dynamics engine.
        
        Args:
            config: Configuration dictionary
        """
        if config is None:
            config = {}
        
        # Nonlinear strength parameters (reduced for stability)
        self.C_quadratic = config.get('C_quadratic', 0.0001)  # Very small for quadratic
        self.C_exp_decay = config.get('C_exp_decay', 0.01)  # Reduced decay
        self.C_tanh_ethics = config.get('C_tanh_ethics', 0.1)  # Reduced saturation
        self.C_tanh_growth = config.get('C_tanh_growth', 0.1)  # Reduced saturation
        self.C_recursive = config.get('C_recursive', 0.001)  # Very small recursive
        
        # Safety parameters
        self.epsilon_safe = 1e-6
        self.clip_tanh = 10.0
        self.clip_exp = 10.0
    
    def compute_quadratic_awareness(
        self,
        psi: float,
        omega: float,
        domega_dpsi: float
    ) -> float:
        """
        Compute quadratic awareness term.
        
        Formula: |ΨΩ|^2 * (1 - ∂Ω/∂Ψ)
        
        Args:
            psi: Awareness
            omega: Coherence
            domega_dpsi: Derivative of coherence w.r.t. awareness
            
        Returns:
            quadratic_term: Quadratic awareness contribution
        """
        # Product squared
        product = psi * omega
        product_squared = product ** 2
        
        # Derivative feedback term
        feedback = 1.0 - domega_dpsi
        
        quadratic_term = self.C_quadratic * product_squared * feedback
        
        return quadratic_term
    
    def compute_exponential_decay(
        self,
        theta_n: float
    ) -> float:
        """
        Compute exponential decay term.
        
        Formula: exp[-ΘN]
        
        Args:
            theta_n: Number of thought layers
            
        Returns:
            decay_factor: Exponential decay factor
        """
        # Clip to prevent overflow
        exp_arg = -self.C_exp_decay * theta_n
        exp_arg = np.clip(exp_arg, -self.clip_exp, self.clip_exp)
        
        decay_factor = np.exp(exp_arg)
        
        return decay_factor
    
    def compute_tanh_saturation_ethics(
        self,
        delta_phi: float,
        omega: float
    ) -> float:
        """
        Compute tanh saturation for ethics.
        
        Formula: tanh(ΔΦ / Ω)
        
        Args:
            delta_phi: Change in ethics
            omega: Coherence
            
        Returns:
            saturation_factor: Tanh saturation factor
        """
        omega_safe = max(omega, self.epsilon_safe)
        
        tanh_arg = self.C_tanh_ethics * (delta_phi / omega_safe)
        tanh_arg = np.clip(tanh_arg, -self.clip_tanh, self.clip_tanh)
        
        saturation_factor = np.tanh(tanh_arg)
        
        return saturation_factor
    
    def compute_tanh_saturation_growth(
        self,
        maturity: float,
        lambda_stability: float,
        xi_stability: float
    ) -> float:
        """
        Compute tanh saturation for growth.
        
        Formula: tanh(ΓΛ / Ξ)
        
        Args:
            maturity: Growth level (Γ)
            lambda_stability: Stability measure (Λ)
            xi_stability: Alternative stability measure (Ξ)
            
        Returns:
            saturation_factor: Tanh saturation factor
        """
        xi_safe = max(xi_stability, self.epsilon_safe)
        
        tanh_arg = self.C_tanh_growth * (maturity * lambda_stability / xi_safe)
        tanh_arg = np.clip(tanh_arg, -self.clip_tanh, self.clip_tanh)
        
        saturation_factor = np.tanh(tanh_arg)
        
        return saturation_factor
    
    def compute_recursive_observation(
        self,
        theta_n: float,
        phi: float,
        omega: float
    ) -> float:
        """
        Compute recursive observation term (simplified).
        
        Formula: Θ(Θ(N)) - simplified as Θ(N) * Φ * Ω
        
        Args:
            theta_n: Number of thought layers
            phi: Ethics
            omega: Coherence
            
        Returns:
            recursive_term: Recursive observation contribution
        """
        # Simplified version: layers observing ethical-coherent state
        recursive_term = self.C_recursive * theta_n * phi * omega
        
        return recursive_term


class NonlinearHarmoniaODESystem:
    """
    Extended ODE system with nonlinear dynamics.
    
    Extends CoupledHarmoniaODESystem from v10.0 to include nonlinear terms.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize nonlinear ODE system.
        
        Args:
            config: Configuration dictionary
        """
        if config is None:
            config = {}
        
        # Initialize base system (v10.0)
        self.base_system = CoupledHarmoniaODESystem(config)
        
        # Initialize nonlinear engine
        self.nonlinear_engine = NonlinearDynamicsEngine(config)
        
        # History buffer for derivative tracking
        self.history_psi = deque(maxlen=3)
        self.history_omega = deque(maxlen=3)
        
        # Track previous delta_phi for tanh saturation
        self.prev_delta_phi = 0.0
    
    def derivatives(
        self,
        t: float,
        state: np.ndarray,
        inputs: Optional[Dict] = None
    ) -> np.ndarray:
        """
        Compute derivatives with nonlinear terms.
        
        Args:
            t: Current time
            state: State vector [13 dimensions]
            inputs: External inputs
            
        Returns:
            derivatives: [13 dimensions]
        """
        if inputs is None:
            inputs = {}
        
        # Unpack state (13 dimensions)
        base_state = state[:10]
        domega_dpsi = state[10] if len(state) > 10 else 0.0
        theta_n = state[11] if len(state) > 11 else 1.0
        lambda_stability = state[12] if len(state) > 12 else 1.0
        
        psi, phi, omega, epsilon, energy, knowledge, maturity = base_state[:7]
        
        # Get base derivatives from v10.0
        base_derivs = self.base_system.derivatives(t, base_state, inputs)
        
        # Update history for derivative tracking
        self.history_psi.append(psi)
        self.history_omega.append(omega)
        
        # Compute ∂Ω/∂Ψ using finite differences
        if len(self.history_psi) >= 2:
            delta_psi = self.history_psi[-1] - self.history_psi[-2]
            delta_omega = self.history_omega[-1] - self.history_omega[-2]
            
            if abs(delta_psi) > 1e-10:
                domega_dpsi_new = delta_omega / delta_psi
            else:
                domega_dpsi_new = domega_dpsi
        else:
            domega_dpsi_new = domega_dpsi
        
        # Compute nonlinear terms
        
        # 1. Quadratic awareness
        quad_awareness = self.nonlinear_engine.compute_quadratic_awareness(
            psi, omega, domega_dpsi
        )
        
        # 2. Exponential decay
        exp_decay = self.nonlinear_engine.compute_exponential_decay(theta_n)
        
        # 3. Tanh saturation (ethics)
        delta_phi = base_derivs[1]  # dphi/dt from base
        tanh_ethics = self.nonlinear_engine.compute_tanh_saturation_ethics(
            delta_phi, omega
        )
        
        # 4. Tanh saturation (growth)
        xi_stability = omega  # Use coherence as proxy for Ξ
        tanh_growth = self.nonlinear_engine.compute_tanh_saturation_growth(
            maturity, lambda_stability, xi_stability
        )
        
        # 5. Recursive observation
        recursive_obs = self.nonlinear_engine.compute_recursive_observation(
            theta_n, phi, omega
        )
        
        # Apply nonlinear terms to derivatives (with safety clipping)
        dpsi_dt = base_derivs[0] + np.clip(quad_awareness, -10, 10) + np.clip(recursive_obs, -10, 10)
        dphi_dt = base_derivs[1] * (1 + np.clip(tanh_ethics, -1, 1))  # Multiplicative
        domega_dt = base_derivs[2]
        depsilon_dt = base_derivs[3]
        denergy_dt = base_derivs[4]
        dknowledge_dt = base_derivs[5]
        dmaturity_dt = base_derivs[6] * (1 + tanh_growth)  # Multiplicative
        
        # Coupling state derivatives (from base)
        di_coherence_dt = base_derivs[7]
        ddelta_phi_accum_dt = base_derivs[8]
        dpsi_memory_dt = base_derivs[9] * exp_decay  # Apply exponential decay
        
        # Derivatives for nonlinear state variables
        ddomega_dpsi_dt = (domega_dpsi_new - domega_dpsi) * 10  # Smooth update
        dtheta_n_dt = 0.01 * knowledge  # Layers grow with knowledge
        dlambda_stability_dt = 0.01 * (omega - lambda_stability)  # Track coherence
        
        return np.array([
            dpsi_dt, dphi_dt, domega_dt, depsilon_dt,
            denergy_dt, dknowledge_dt, dmaturity_dt,
            di_coherence_dt, ddelta_phi_accum_dt, dpsi_memory_dt,
            ddomega_dpsi_dt, dtheta_n_dt, dlambda_stability_dt
        ])


class NonlinearFluidHarmoniaIntegrator:
    """
    High-level interface for nonlinear continuous-time dynamics.
    
    Extends v10.0 CoupledFluidHarmoniaIntegrator with nonlinear dynamics.
    """
    
    def __init__(self, config: Optional[Dict] = None, dt: float = 0.01):
        """
        Initialize nonlinear fluid integrator.
        
        Args:
            config: Configuration dictionary
            dt: Integration time step
        """
        self.config = config or {}
        self.dt = dt
        
        self.ode_system = NonlinearHarmoniaODESystem(config)
        self.integrator = ContinuousTimeIntegrator(method='rk4', dt=dt)
        
        self.state = NonlinearState()
        self.history = []
    
    def process(
        self,
        inputs: Optional[Dict] = None,
        duration: float = 1.0
    ) -> Dict:
        """
        Process inputs over a duration with nonlinear dynamics.
        
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
        
        self.state = NonlinearState.from_vector(state_values[-1], t_values[-1])
        
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
        """Compute harmonic response with nonlinear effects."""
        s = self.state
        
        # Base response
        base = (s.psi + s.phi) * (1 - s.epsilon)
        
        # Nonlinear contributions
        quadratic_contrib = 0.01 * (s.psi * s.omega) ** 2
        recursive_contrib = 0.05 * s.theta_n * s.phi * s.omega
        
        R = base + quadratic_contrib + recursive_contrib + s.knowledge * s.maturity
        
        return float(R)
    
    def get_state(self) -> Dict:
        """Get current state."""
        return self.state.to_dict()
    
    def reset(self):
        """Reset to initial state."""
        self.state = NonlinearState()
        self.history = []
        self.ode_system.history_psi.clear()
        self.ode_system.history_omega.clear()


# Demo
if __name__ == "__main__":
    print("=" * 70)
    print("HARMONIA-DSL v11.0: Nonlinear Dynamics Demo")
    print("=" * 70)
    print()
    
    agent = NonlinearFluidHarmoniaIntegrator(dt=0.01)
    
    print("Initial State:")
    print(f"  Awareness (Ψ): {agent.state.psi:.2f}")
    print(f"  Coherence (Ω): {agent.state.omega:.2f}")
    print(f"  Thought Layers (ΘN): {agent.state.theta_n:.2f}")
    print()
    
    print("Simulating 5 seconds with nonlinear dynamics enabled...")
    result = agent.process(inputs={'velocity': 1.0}, duration=5.0)
    
    print(f"\nFinal State (t={agent.state.time:.2f}s):")
    print(f"  Awareness (Ψ): {agent.state.psi:.2f}")
    print(f"  Coherence (Ω): {agent.state.omega:.2f}")
    print(f"  Thought Layers (ΘN): {agent.state.theta_n:.2f}")
    print(f"  ∂Ω/∂Ψ: {agent.state.domega_dpsi:.3f}")
    print(f"  Stability (Λ): {agent.state.lambda_stability:.3f}")
    print(f"  Harmonic Response (R): {result['R']:.2f}")
    
    print("\n✓ Nonlinear dynamics successfully implemented!")
    print("✓ Quadratic, exponential, and tanh terms all active!")
