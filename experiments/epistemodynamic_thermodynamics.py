"""Deterministic thermodynamic probes for the RI1 Epistemodynamics laws.

This module is deliberately an *experiment*, not a claim that the supplied
laws have been empirically established.  It has two purposes:

1. CONSERVATION COMPATIBILITY AUDIT
   Laws 1 and 2 specify m = constant and E = m(1-S) + C².  For a closed
   system, an increase in S at fixed m and E requires an increase in C².
   That algebraic requirement can be compared directly to Laws 4, 6, and 14,
   which motivate entropy increase and coherence loss under stress.

2. OPEN-SYSTEM POLICY EXPERIMENT
   To make entropy increase and coherence loss jointly possible while
   conserving an explicit total, the experiment adds a declared energy
   reservoir D:

       E_total = m(1-S) + C² + D.

   D is a modelling extension, not a term supplied by the Epistemodynamics
   document.  It represents energy no longer stored in the two specified
   structural components.  Φ-mediated actions may draw from D, but may never
   create energy.

The open-system model operationalizes only the following explicit formulas:
- Law 2:  E_structural = m(1-S) + C²
- Law 4:  dS/dt is proportional to (1-C) * integration_rate
- Law 5:  permitted reduction scales with Φ * C_available/C_required
- Law 6:  S_critical=0.95, C_critical=0.05
- Law 11: Φ_optimal = 0.5 + 0.5(S-C)
- Law 12: C_optimal = 0.9 - 0.5S
- Law 20: SAFE / DANGER / COLLAPSE phase partition

All other update coefficients are declared parameters.  They are not derived
from the laws and should be swept or replaced with measured calibration data.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from math import isclose, sqrt
from typing import Dict, Iterable, List, Optional, Protocol


S_CRITICAL = 0.95
C_CRITICAL = 0.05
SAFE_ENTROPY = 0.85


class Phase(str, Enum):
    """Law 20-style phase labels."""

    SAFE = "safe"
    DANGER = "danger"
    COLLAPSED = "collapsed"


class MediationPolicy(Protocol):
    """A policy that selects a Φ strength from the current state."""

    name: str

    def phi(self, entropy: float, coherence: float) -> float:
        """Return a bounded mediation strength in [0, 1]."""


@dataclass(frozen=True)
class NoMediation:
    """Control condition: no Φ-mediated entropy reduction."""

    name: str = "no_mediation"

    def phi(self, entropy: float, coherence: float) -> float:
        return 0.0


@dataclass(frozen=True)
class FixedPhi:
    """A fixed-strength Φ policy used as a non-adaptive comparator."""

    strength: float = 0.5
    name: str = "fixed_phi"

    def phi(self, entropy: float, coherence: float) -> float:
        return _clamp(self.strength, 0.0, 1.0)


@dataclass(frozen=True)
class AdaptivePhi:
    """Law 11 policy: Φ = 0.5 + 0.5(S-C), clipped to a valid range."""

    name: str = "adaptive_phi"

    def phi(self, entropy: float, coherence: float) -> float:
        return _clamp(0.5 + 0.5 * (entropy - coherence), 0.0, 1.0)


@dataclass(frozen=True)
class ThermoParameters:
    """Declared calibration choices for the open-system extension.

    The law-provided thresholds and formulas are implemented directly.  The
    rates below are intentionally exposed so that this experiment is easy to
    falsify through parameter sweeps.
    """

    mass: float = 1.0
    total_energy: float = 2.0
    initial_entropy: float = 0.35
    initial_coherence: float = 0.72
    steps: int = 80
    integration_rate: float = 0.70
    natural_entropy_rate: float = 0.005
    entropy_coupling: float = 0.12
    requested_entropy_reduction: float = 0.040
    required_coherence: float = 0.50
    coherence_loss_per_entropy: float = 0.75
    coherence_recovery_per_reduction: float = 0.20
    target_relaxation_rate: float = 0.040

    def __post_init__(self) -> None:
        if self.mass <= 0 or self.total_energy <= 0:
            raise ValueError("mass and total_energy must be positive")
        if self.steps < 1:
            raise ValueError("steps must be at least 1")
        if not 0.0 <= self.initial_entropy <= 1.0:
            raise ValueError("initial_entropy must be in [0, 1]")
        if not 0.0 <= self.initial_coherence <= 1.0:
            raise ValueError("initial_coherence must be in [0, 1]")
        if self.total_energy < structural_energy(
            self.mass, self.initial_entropy, self.initial_coherence
        ):
            raise ValueError("total_energy must cover the initial structural state")
        for field_name in (
            "integration_rate",
            "natural_entropy_rate",
            "entropy_coupling",
            "requested_entropy_reduction",
            "required_coherence",
            "coherence_loss_per_entropy",
            "coherence_recovery_per_reduction",
            "target_relaxation_rate",
        ):
            if getattr(self, field_name) < 0:
                raise ValueError(f"{field_name} must be non-negative")


@dataclass(frozen=True)
class ConservationAudit:
    """A one-step closed-system implication of Law 2."""

    mass: float
    total_energy: float
    entropy_before: float
    entropy_after: float
    coherence_before: float
    coherence_required_after: Optional[float]
    feasible: bool

    @property
    def coherence_delta_required(self) -> Optional[float]:
        if self.coherence_required_after is None:
            return None
        return self.coherence_required_after - self.coherence_before


@dataclass(frozen=True)
class ThermoState:
    """One state in the declared open-system extension."""

    step: int
    entropy: float
    coherence: float
    reservoir: float
    phi: float
    entropy_produced: float
    entropy_reduced: float
    phase: Phase
    collapsed: bool

    @property
    def c_optimal(self) -> float:
        """Law 12 target coherence for this entropy level."""
        return coherence_optimal(self.entropy)


@dataclass(frozen=True)
class SimulationResult:
    """Full deterministic trace and summary for one policy."""

    policy: str
    parameters: ThermoParameters
    trace: List[ThermoState]

    @property
    def final(self) -> ThermoState:
        return self.trace[-1]

    @property
    def collapse_step(self) -> Optional[int]:
        for state in self.trace:
            if state.collapsed:
                return state.step
        return None

    @property
    def minimum_reservoir(self) -> float:
        return min(state.reservoir for state in self.trace)

    @property
    def maximum_entropy(self) -> float:
        return max(state.entropy for state in self.trace)

    @property
    def minimum_coherence(self) -> float:
        return min(state.coherence for state in self.trace)

    def summary(self) -> Dict[str, object]:
        return {
            "policy": self.policy,
            "steps_recorded": len(self.trace),
            "collapse_step": self.collapse_step,
            "final_entropy": self.final.entropy,
            "final_coherence": self.final.coherence,
            "final_reservoir": self.final.reservoir,
            "final_phase": self.final.phase.value,
            "max_entropy": self.maximum_entropy,
            "min_coherence": self.minimum_coherence,
            "min_reservoir": self.minimum_reservoir,
        }


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(value, high))


def structural_energy(mass: float, entropy: float, coherence: float) -> float:
    """Law 2 structural term: E = m(1-S) + C²."""
    return mass * (1.0 - entropy) + coherence**2


def adaptive_phi_strength(entropy: float, coherence: float) -> float:
    """Law 11: Φ_optimal = 0.5 + 0.5(S-C), constrained to [0,1]."""
    return AdaptivePhi().phi(entropy, coherence)


def coherence_optimal(entropy: float) -> float:
    """Law 12: C_optimal(S) = 0.9 - 0.5S, clipped to [0,1]."""
    return _clamp(0.9 - 0.5 * entropy, 0.0, 1.0)


def entropy_tolerance(artha: float) -> float:
    """Law 15: S_max = 0.95 + 0.05*Artha, bounded by physical entropy 1."""
    return _clamp(S_CRITICAL + 0.05 * artha, 0.0, 1.0)


def phase_of(entropy: float, coherence: float, artha: float = 0.0) -> Phase:
    """Law 6/20 classifier with Law 15's declared tolerance extension."""
    if entropy >= entropy_tolerance(artha) or coherence <= C_CRITICAL:
        return Phase.COLLAPSED
    if entropy >= SAFE_ENTROPY:
        return Phase.DANGER
    return Phase.SAFE


def law4_entropy_production(
    coherence: float,
    integration_rate: float,
    natural_entropy_rate: float,
    entropy_coupling: float,
) -> float:
    """Law 4 operationalization: baseline + k(1-C)·integration_rate."""
    return natural_entropy_rate + entropy_coupling * (1.0 - coherence) * integration_rate


def law5_allowed_reduction(
    requested_reduction: float,
    phi_strength: float,
    available_coherence: float,
    required_coherence: float,
) -> float:
    """Bound a requested reduction by Law 5's proportional mediation term.

    The Law 5 formula supplies a dimensionless capacity factor.  Multiplying
    it by a declared request creates a dimensionally consistent experiment.
    The action cannot exceed either the request or the available capacity.
    """
    if required_coherence <= 0:
        raise ValueError("required_coherence must be positive")
    capacity_factor = _clamp(phi_strength, 0.0, 1.0) * (
        max(0.0, available_coherence) / required_coherence
    )
    return max(0.0, min(requested_reduction, requested_reduction * capacity_factor))


def closed_system_conservation_audit(
    mass: float,
    total_energy: float,
    entropy_before: float,
    entropy_after: float,
    coherence_before: float,
) -> ConservationAudit:
    """Calculate the coherence implied by Law 2 in a strictly closed system.

    With m and E fixed, an entropy increase changes m(1-S).  C must change
    in the opposite direction to keep E fixed.  A negative radicand means
    there is no real-valued coherence satisfying the stated accounting.
    """
    radicand = total_energy - mass * (1.0 - entropy_after)
    required = sqrt(radicand) if radicand >= 0.0 else None
    return ConservationAudit(
        mass=mass,
        total_energy=total_energy,
        entropy_before=entropy_before,
        entropy_after=entropy_after,
        coherence_before=coherence_before,
        coherence_required_after=required,
        feasible=required is not None,
    )


def _constrain_to_energy_budget(
    entropy: float,
    coherence: float,
    parameters: ThermoParameters,
) -> tuple[float, float, float]:
    """Ensure E_structural ≤ E_total and return the residual reservoir D."""
    entropy = _clamp(entropy, 0.0, 1.0)
    coherence = _clamp(coherence, 0.0, 1.0)
    budget_for_coherence = parameters.total_energy - parameters.mass * (1.0 - entropy)
    if budget_for_coherence < 0.0:
        # The entropy state alone exceeds the total accounting budget.  Raise
        # entropy to the lowest value compatible with the fixed total.
        entropy = 1.0 - parameters.total_energy / parameters.mass
        entropy = _clamp(entropy, 0.0, 1.0)
        budget_for_coherence = parameters.total_energy - parameters.mass * (1.0 - entropy)
    max_coherence = sqrt(max(0.0, budget_for_coherence))
    coherence = min(coherence, max_coherence)
    reservoir = parameters.total_energy - structural_energy(
        parameters.mass, entropy, coherence
    )
    # Protect against harmless floating-point roundoff only.
    if reservoir < 0.0 and isclose(reservoir, 0.0, abs_tol=1e-12):
        reservoir = 0.0
    return entropy, coherence, reservoir


def run_open_system(
    policy: MediationPolicy,
    parameters: ThermoParameters = ThermoParameters(),
) -> SimulationResult:
    """Run the declared open-system extension under one Φ policy.

    The experiment stops at collapse.  It does not model recovery after
    collapse, consistent with Laws 3 and 8 unless a new external-input model
    is explicitly added.
    """
    entropy, coherence, reservoir = _constrain_to_energy_budget(
        parameters.initial_entropy, parameters.initial_coherence, parameters
    )
    trace: List[ThermoState] = []

    for step in range(parameters.steps):
        current_phase = phase_of(entropy, coherence)
        if current_phase is Phase.COLLAPSED:
            trace.append(
                ThermoState(
                    step=step,
                    entropy=entropy,
                    coherence=coherence,
                    reservoir=reservoir,
                    phi=policy.phi(entropy, coherence),
                    entropy_produced=0.0,
                    entropy_reduced=0.0,
                    phase=current_phase,
                    collapsed=True,
                )
            )
            break

        phi = policy.phi(entropy, coherence)
        produced = law4_entropy_production(
            coherence,
            parameters.integration_rate,
            parameters.natural_entropy_rate,
            parameters.entropy_coupling,
        )
        reduction = law5_allowed_reduction(
            parameters.requested_entropy_reduction,
            phi,
            coherence,
            parameters.required_coherence,
        )
        entropy_next = entropy + produced - reduction

        # This is the explicit Law 14-inspired asymmetry in the extension:
        # erosion is faster per unit entropy than rebuild is per unit
        # mediated reduction. The coefficients are declared, not law-derived.
        coherence_loss = parameters.coherence_loss_per_entropy * produced
        coherence_recovery = parameters.coherence_recovery_per_reduction * reduction * phi
        target_pull = 0.0
        if phi > 0.0:
            target_pull = parameters.target_relaxation_rate * (
                coherence_optimal(entropy) - coherence
            )
        coherence_next = coherence - coherence_loss + coherence_recovery + target_pull
        entropy_next, coherence_next, reservoir_next = _constrain_to_energy_budget(
            entropy_next, coherence_next, parameters
        )
        next_phase = phase_of(entropy_next, coherence_next)
        trace.append(
            ThermoState(
                step=step + 1,
                entropy=entropy_next,
                coherence=coherence_next,
                reservoir=reservoir_next,
                phi=phi,
                entropy_produced=produced,
                entropy_reduced=reduction,
                phase=next_phase,
                collapsed=next_phase is Phase.COLLAPSED,
            )
        )
        entropy, coherence, reservoir = entropy_next, coherence_next, reservoir_next
        if next_phase is Phase.COLLAPSED:
            break

    return SimulationResult(policy=policy.name, parameters=parameters, trace=trace)


def run_policy_comparison(
    parameters: ThermoParameters = ThermoParameters(),
) -> List[SimulationResult]:
    """Run the control, fixed Φ, and Law-11 adaptive Φ conditions."""
    policies: Iterable[MediationPolicy] = (
        NoMediation(),
        FixedPhi(),
        AdaptivePhi(),
    )
    return [run_open_system(policy, parameters) for policy in policies]


def energy_accounting_error(state: ThermoState, parameters: ThermoParameters) -> float:
    """Return E_total - [m(1-S)+C²+D]; expected numerical error is zero."""
    return parameters.total_energy - (
        structural_energy(parameters.mass, state.entropy, state.coherence)
        + state.reservoir
    )


def result_as_dict(result: SimulationResult) -> Dict[str, object]:
    """Stable JSON-friendly representation for an experiment archive."""
    return {
        "policy": result.policy,
        "parameters": asdict(result.parameters),
        "summary": result.summary(),
        "trace": [
            {
                **asdict(state),
                "phase": state.phase.value,
            }
            for state in result.trace
        ],
    }
