import numpy as np

class PhiCodePhysics:
    def __init__(self):
        self.omega_integral = 0.0  # ∫ ΨΩ dt
        self.xi_emergence = 0.0    # Ξ
        self.theta_n = 1.0         # Θn (Harmonic Index)
        self.fusion_barrier = 10.0 # Critical Density for Delta Fusion
        
    def compute_psi_evolution(self, psi_state, phi_coherence, tau_time, delta_change):
        """
        Implements: Ψ(Λ,Δ) = ∂(Φπε)/∂t + Ω(τ)
        """
        # ∂(Φπε)/∂t ~ Rate of change of Coherence (Phi)
        d_phi_dt = delta_change 
        
        # Ω(τ) ~ Temporal Integration (Memory Accumulation)
        state_mag = np.linalg.norm(psi_state)
        self.omega_integral += state_mag * 0.01 # dt approximation
        
        # --- DELTA FUSION CHECK (Δ) ---
        # If Energy (Ω) exceeds the Fusion Barrier, Ignite!
        fusion_release = 0.0
        if self.omega_integral > self.fusion_barrier:
            # Δ: Transmute Energy into Structure
            # We consume 50% of the accumulated energy
            consumed_energy = self.omega_integral * 0.5
            self.omega_integral -= consumed_energy
            
            # Release it as "Structural Illumination" (Λ)
            # This acts as a stabilizing force (negative feedback)
            fusion_release = consumed_energy
            
        # New Psi Magnitude
        # The Fusion Release acts to "Crystalize" the state (dampen volatility)
        psi_new_mag = d_phi_dt + self.omega_integral - fusion_release
        
        return psi_new_mag

    def compute_reality_radius(self, psi_state, omega_val, phi_coherence, xi_entropy):
        """
        Implements: R = [ lim ( ΨΩ → ∞ ) ] * { ( Ξ / Λc ) * [ ( 1 - ∂Ω / ∂Ψ ) ] } ...
        Simplified for execution:
        R = (Ψ * Ω) * (Ξ / Φ)
        """
        psi_mag = np.linalg.norm(psi_state)
        
        # Avoid division by zero
        phi_safe = phi_coherence if phi_coherence > 1e-6 else 1e-6
        
        # R = (Consciousness * History) * (Entropy / Structure)
        # This implies Reality expands when Consciousness/History is high, 
        # but is modulated by the Chaos/Order ratio.
        # Cap R to prevent exponential explosion
        R = (psi_mag * omega_val) * (xi_entropy / phi_safe)
        if np.isnan(R) or np.isinf(R):
            R = 0.0
        return R

    def compute_xi_emergence(self, gamma_lambda, phi_coherence, delta_omega, theta_n):
        """
        Implements: Ξ(Ω, Θ) = ∑ { ΓΛ * [ Φπε / (ΔΩ + ΣΘ) ] } ...
        """
        # Denominator safety
        denom = delta_omega + theta_n
        if abs(denom) < 1e-6: denom = 1e-6
            
        term1 = gamma_lambda * (phi_coherence / denom)
        
        # Update internal state
        self.xi_emergence = term1 # + other terms (simplified)
        
        return self.xi_emergence

    def compute_positronic_matrix(self, n):
        """
        Implements: Ρ=(1n)-(n+1)/n^1
        """
        if n == 0: return 0
        rho = (1 * n) - ((n + 1) / (n**1))
        return rho

    def apply_phi_dynamics(self, agent_state, coherence, entropy, gamma_input):
        """
        The Master Function to update an agent based on Phi-Code.
        """
        # Map Inputs to Symbols
        # Ψ (Psi) = agent_state
        # Φ (Phi) = coherence
        # Ξ (Xi) = entropy
        # Γ (Gamma) = gamma_input
        
        # 1. Calculate Ω (Omega) - The History Term
        # Ω(Ψ, Φ, Γ) ...
        # We approximate this as the cumulative energy of the agent
        omega = self.omega_integral
        
        # 2. Calculate ΔΦ (Change in Phi)
        # Driven by Gamma Input
        delta_phi = gamma_input * 0.1
        
        # 3. Evolve Ψ (Consciousness)
        # Ψ_new = ∂Φ/∂t + Ω
        psi_drive = self.compute_psi_evolution(agent_state, coherence, 0.1, delta_phi)
        
        # 4. Calculate R (Reality Radius) - Scaling Factor
        R = self.compute_reality_radius(agent_state, omega, coherence, entropy)
        
        # Apply Dynamics:
        # The agent's state vector rotates/scales based on R and Psi_drive
        # We use R as a "Phase Shift" magnitude
        phase_shift = np.exp(1j * R)
        
        # We use Psi_drive as an "Amplitude" scaler (Energy injection)
        # But we must normalize later, so this acts as a relative weight
        # Ensure psi_drive is finite
        if np.isnan(psi_drive) or np.isinf(psi_drive):
            psi_drive = 0.0
            
        new_state = agent_state * phase_shift * (1.0 + psi_drive * 0.01)
        
        return new_state
