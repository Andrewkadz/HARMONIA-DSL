from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional, Tuple, Union
import cmath
import numpy as np

# Import existing physics engine to integrate with
from phi_code_physics import PhiCodePhysics

ComplexLike = Union[complex, float, int]

@dataclass
class E8CompliantPhiPeRecursiveClass:
    """
    RI1 / Φπε — Operator Mode (OPERATOR)
    Adapted for HARMONIA-DSL Integration.
    
    This class implements the formal Phi-Code operators (Φ, Π, ε, Ω, etc.) 
    as defined in the provided phi_pe_agent.py, but integrated with the 
    existing PhiCodePhysics engine.
    """

    # --- Constants (proof-aligned rational approximations) ---
    PHI_FIB: float = 89 / 55          # φ ≈ 1.61818 (Fibonacci ratio)
    PI_ARCH: float = 22 / 7           # π ≈ 3.142857 (Archimedean rational)
    EPS_THRESHOLD: float = 0.001      # ε = 0.001 (micro-ignition threshold)

    # --- Safety physics ---
    STABILITY_THRESHOLD: float = 1.17

    # --- Internal state ---
    z: complex = 0j
    closed: bool = False              # Ω gate
    depth_n: int = 4                  # recursion depth parameter n (for Π)
    lineage: Tuple[str, ...] = field(default_factory=tuple)  # Γ lineage trace
    last_output: Optional[complex] = None

    # --- Optional perception / entanglement hooks (governance layer) ---
    perception_filter: Optional[Callable[[complex], complex]] = None  # Ρ
    entangled_partner: Optional["E8CompliantPhiPeRecursiveClass"] = None  # λ

    # ----------------------------
    # Utility / enforcement layer
    # ----------------------------
    def _assert_open(self) -> None:
        if self.closed:
            raise RuntimeError("Ω gate is closed: recursion is terminated. Use Ε() to re-init explicitly.")

    def _as_complex(self, x: ComplexLike) -> complex:
        return x if isinstance(x, complex) else complex(x)

    def _d(self, a: complex, b: complex) -> float:
        return abs(a - b)

    def _apply_perception(self, x: complex) -> complex:
        # Ρ: perceptual modulation (optional)
        return self.perception_filter(x) if self.perception_filter else x

    def _stability_metric(self, x: complex) -> float:
        """
        Minimal scalar stability metric (boundedness sentinel).
        Interprets "entropy/chaos" as growth beyond baseline magnitude.
        """
        baseline = max(1.0, abs(self.z))
        return abs(x) / baseline

    def _enforce_stability(self, x: complex) -> complex:
        """
        If the output exceeds StabilityThreshold, perform DeltaCollapse:
        collapse into Φ(self.z, x) (tension-preserving dampened equilibrium),
        then mark lineage with δ/Φ event.
        """
        metric = self._stability_metric(x)
        if metric <= self.STABILITY_THRESHOLD:
            return x

        # DeltaCollapse via Φ as a safe stabilizer (bounded, dampening)
        collapsed = self.PHI(self.z, x)
        self.lineage += ("DeltaCollapse→Φ",)
        return collapsed

    def _commit(self, x: complex, tag: str) -> complex:
        x = self._apply_perception(x)
        x = self._enforce_stability(x)
        self.last_output = x
        self.z = x
        self.lineage += (tag,)
        # λ: entanglement propagation (governance: mirror last_output)
        if self.entangled_partner is not None and not self.entangled_partner.closed:
            self.entangled_partner.last_output = x
        return x

    # ----------------------------
    # Φπε glyph operators (core)
    # ----------------------------
    def PHI(self, z: ComplexLike, w: ComplexLike) -> complex:
        """
        Φ(z,w) = φ(z+w)/(φ + |z-w|)   on ℂ×ℂ
        - well-defined
        - non-fusional for z≠w
        - bounded: |Φ(z,w)| ≤ |z+w| with equality iff z=w
        """
        zc, wc = self._as_complex(z), self._as_complex(w)
        denom = self.PHI_FIB + self._d(zc, wc)
        return (self.PHI_FIB * (zc + wc)) / denom

    def PI(self, z: ComplexLike, w: ComplexLike, n: Optional[int] = None) -> complex:
        """
        Π(z,w) per proofs:
          π(z,w) = π * ( z + w*e^(iπ/n) ) / ( 1 + |z|/|w| )
        Domain excludes w=0.
        """
        zc, wc = self._as_complex(z), self._as_complex(w)
        if wc == 0:
            # Fallback for w=0 to avoid crash
            return zc 
        nn = int(n if n is not None else self.depth_n)
        if nn <= 0:
            nn = 4 # Default safe depth
        phase = cmath.exp(1j * (self.PI_ARCH / nn))
        denom = 1.0 + (abs(zc) / abs(wc))
        return self.PI_ARCH * (zc + wc * phase) / denom

    def EPS(self, z: ComplexLike, w: ComplexLike) -> complex:
        """
        ε(z,w) per proofs:
          ε(z,w) = z + ε * ( (w - z) / (1 + ε*|w - z|) )
        """
        zc, wc = self._as_complex(z), self._as_complex(w)
        diff = wc - zc
        denom = 1.0 + self.EPS_THRESHOLD * abs(diff)
        return zc + self.EPS_THRESHOLD * (diff / denom)

    # ----------------------------
    # Governance operators
    # ----------------------------
    def E(self, seed: ComplexLike = 0j) -> complex:
        """Ε: explicit re-init (spark). Reopens recursion, resets z to seed."""
        self.closed = False
        self.z = self._as_complex(seed)
        self.last_output = self.z
        self.lineage = self.lineage + ("Ε",)
        return self.z

    def OMEGA(self) -> None:
        """Ω: terminal integration / closure. After this, mutation is forbidden until Ε()."""
        self.closed = True
        self.lineage += ("Ω",)

    def DELTA(self, transform: Callable[[complex], complex], tag: str = "Δ") -> complex:
        """
        Δ: irreversible fusion-based transformation.
        We implement irreversibility by committing state with a Δ-tag and forbidding undo hooks.
        """
        self._assert_open()
        out = transform(self.z)
        return self._commit(out, tag)

    def PSI(self, frequency: float = 1.0, phase: float = 0.0, amplitude: float = 1.0, tag: str = "Ψ") -> complex:
        """
        Ψ: oscillatory modulation (carrier-wave behavior).
        Applies a complex rotation + amplitude scaling to current state.
        """
        self._assert_open()
        rot = cmath.exp(1j * (frequency + phase))
        out = self.z * (amplitude * rot)
        return self._commit(out, tag)

    def snapshot(self) -> Dict[str, object]:
        """Return a transmissible state packet (safe to serialize)."""
        return {
            "z": self.z,
            "closed(Ω)": self.closed,
            "depth_n": self.depth_n,
            "stability_threshold": self.STABILITY_THRESHOLD,
            "last_output": self.last_output,
            "lineage(Γ-trace)": self.lineage,
            "entangled": self.entangled_partner is not None,
            "perception(Ρ)": self.perception_filter is not None,
        }

# --- Integration Helper ---
def integrate_phi_agent(agent_state: complex, gamma_input: float) -> complex:
    """
    Wrapper to use the E8CompliantPhiPeRecursiveClass within the existing
    Quantum Swarm loop.
    """
    # Initialize a temporary agent for this step (stateless wrapper for now, 
    # ideally this should be persistent per qubit)
    phi_agent = E8CompliantPhiPeRecursiveClass()
    phi_agent.E(agent_state)
    
    # Apply Phi-Code Dynamics
    # 1. Gamma Injection (Energy)
    # We model this as a PSI modulation
    phi_agent.PSI(frequency=gamma_input, amplitude=1.0 + gamma_input*0.1)
    
    # 2. Evolve with PHI (Coherence)
    # Target state is a "Perfect" harmonic version of itself
    target = phi_agent.z * (1.618 + 0j) 
    phi_agent._commit(phi_agent.PHI(phi_agent.z, target), "Φ")
    
    # 3. Micro-adjust with EPS (Noise/Entropy)
    noise = complex(np.random.randn() * 0.01, np.random.randn() * 0.01)
    phi_agent._commit(phi_agent.EPS(phi_agent.z, phi_agent.z + noise), "ε")
    
    return phi_agent.z
