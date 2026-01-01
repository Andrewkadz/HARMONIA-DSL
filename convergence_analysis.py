"""
HARMONIA-DSL v4.0: Convergence Analysis

This module implements the `lim` operator and `CONVERGENCE` command,
allowing systems to predict their long-term fate and identify attractors.

Implements the Grand Harmonic Equation term: lim ( ΨΩ → ∞ )
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum
import math


class AttractorType(Enum):
    """Types of attractors a system can converge to"""
    POINT = "POINT"              # Converges to a single stable state
    PERIODIC = "PERIODIC"        # Converges to a repeating cycle
    STRANGE = "STRANGE"          # Bounded but chaotic (not implemented yet)
    DIVERGENT = "DIVERGENT"      # Does not converge


@dataclass
class SystemSnapshot:
    """A snapshot of the system state at a point in time"""
    iteration: int
    psi_signal: float
    phi_state: float
    epsilon_drift: float
    stabilized_value: float
    
    def distance_to(self, other: 'SystemSnapshot') -> float:
        """Calculate the Euclidean distance between two snapshots"""
        return math.sqrt(
            (self.psi_signal - other.psi_signal) ** 2 +
            (self.phi_state - other.phi_state) ** 2 +
            (self.epsilon_drift - other.epsilon_drift) ** 2 +
            (self.stabilized_value - other.stabilized_value) ** 2
        )
    
    def __eq__(self, other) -> bool:
        """Check if two snapshots are approximately equal"""
        if not isinstance(other, SystemSnapshot):
            return False
        return self.distance_to(other) < 1e-6


@dataclass
class ConvergenceResult:
    """Results of a convergence analysis"""
    attractor_type: AttractorType
    converged: bool
    iterations: int
    
    # For point attractors
    attractor_state: Optional[SystemSnapshot] = None
    
    # For periodic attractors
    attractor_period: Optional[int] = None
    attractor_cycle: Optional[List[SystemSnapshot]] = None
    
    # Convergence metrics
    final_distance: float = 0.0
    convergence_rate: float = 0.0


class ConvergenceAnalyzer:
    """
    Implements convergence analysis for HARMONIA-DSL systems.
    
    This class provides the `lim` operator functionality, allowing systems
    to simulate their long-term evolution and identify attractors.
    """
    
    def __init__(self):
        self.history: List[SystemSnapshot] = []
        self.result: Optional[ConvergenceResult] = None
    
    def take_snapshot(self, context, iteration: int) -> SystemSnapshot:
        """Take a snapshot of the current system state"""
        return SystemSnapshot(
            iteration=iteration,
            psi_signal=context.state.psi_signal,
            phi_state=context.state.phi_state,
            epsilon_drift=context.state.epsilon_drift,
            stabilized_value=context.state.stabilized_value
        )
    
    def detect_point_attractor(self, tolerance: float) -> Optional[ConvergenceResult]:
        """
        Detect if the system has converged to a point attractor.
        
        A point attractor is detected if the distance between consecutive
        snapshots is less than the tolerance for several iterations.
        """
        if len(self.history) < 10:
            return None
        
        # Check the last 5 snapshots
        recent = self.history[-5:]
        distances = [recent[i].distance_to(recent[i+1]) for i in range(len(recent)-1)]
        
        if all(d < tolerance for d in distances):
            # Converged to a point attractor
            final_state = self.history[-1]
            return ConvergenceResult(
                attractor_type=AttractorType.POINT,
                converged=True,
                iterations=len(self.history),
                attractor_state=final_state,
                final_distance=distances[-1],
                convergence_rate=sum(distances) / len(distances)
            )
        
        return None
    
    def detect_periodic_attractor(self, tolerance: float, max_period: int = 50) -> Optional[ConvergenceResult]:
        """
        Detect if the system has converged to a periodic attractor (limit cycle).
        
        A periodic attractor is detected if the system returns to a previous
        state within tolerance after a fixed number of iterations.
        """
        if len(self.history) < 20:
            return None
        
        current = self.history[-1]
        
        # Check for periods from 2 to max_period
        for period in range(2, min(max_period, len(self.history) // 2)):
            if len(self.history) < period * 3:
                continue
            
            # Check if the last 3 cycles match
            cycle_matches = True
            for cycle_idx in range(3):
                idx1 = -(cycle_idx * period + 1)
                idx2 = -((cycle_idx + 1) * period + 1)
                
                if abs(idx2) > len(self.history):
                    cycle_matches = False
                    break
                
                if self.history[idx1].distance_to(self.history[idx2]) > tolerance:
                    cycle_matches = False
                    break
            
            if cycle_matches:
                # Extract the cycle
                cycle = self.history[-period:]
                return ConvergenceResult(
                    attractor_type=AttractorType.PERIODIC,
                    converged=True,
                    iterations=len(self.history),
                    attractor_period=period,
                    attractor_cycle=cycle,
                    final_distance=self.history[-1].distance_to(self.history[-period-1]),
                    convergence_rate=0.0
                )
        
        return None
    
    def analyze_convergence(
        self,
        context,
        update_function,
        max_iterations: int = 1000,
        tolerance: float = 0.001
    ) -> ConvergenceResult:
        """
        Analyze the long-term convergence of a system.
        
        Args:
            context: The system context
            update_function: A function that updates the system for one time step
            max_iterations: Maximum number of iterations to simulate
            tolerance: Convergence tolerance
        
        Returns:
            ConvergenceResult containing the attractor type and details
        """
        self.history = []
        
        # Take initial snapshot
        self.history.append(self.take_snapshot(context, 0))
        
        # Simulate the system
        for iteration in range(1, max_iterations + 1):
            # Update the system
            try:
                update_function(context)
            except (OverflowError, ValueError) as e:
                # System diverged to infinity
                self.result = ConvergenceResult(
                    attractor_type=AttractorType.DIVERGENT,
                    converged=False,
                    iterations=iteration,
                    final_distance=float('inf')
                )
                return self.result
            
            # Take snapshot
            snapshot = self.take_snapshot(context, iteration)
            self.history.append(snapshot)
            
            # Check for convergence every 10 iterations (after initial 20)
            if iteration > 20 and iteration % 10 == 0:
                # Check for point attractor
                point_result = self.detect_point_attractor(tolerance)
                if point_result:
                    self.result = point_result
                    return point_result
                
                # Check for periodic attractor
                periodic_result = self.detect_periodic_attractor(tolerance)
                if periodic_result:
                    self.result = periodic_result
                    return periodic_result
        
        # Did not converge within max_iterations
        self.result = ConvergenceResult(
            attractor_type=AttractorType.DIVERGENT,
            converged=False,
            iterations=max_iterations,
            final_distance=self.history[-1].distance_to(self.history[-2]) if len(self.history) > 1 else float('inf')
        )
        return self.result
    
    def get_attractor_type(self) -> str:
        """Get the type of attractor (for CONVERGENCE command)"""
        if self.result is None:
            return "UNKNOWN"
        return self.result.attractor_type.value
    
    def get_attractor_state(self) -> Optional[Dict[str, float]]:
        """Get the attractor state (for CONVERGENCE command)"""
        if self.result is None or self.result.attractor_state is None:
            return None
        
        state = self.result.attractor_state
        return {
            "psi": state.psi_signal,
            "phi": state.phi_state,
            "epsilon": state.epsilon_drift,
            "sigma": state.stabilized_value
        }
    
    def get_attractor_period(self) -> Optional[int]:
        """Get the period of the attractor (for CONVERGENCE command)"""
        if self.result is None:
            return None
        return self.result.attractor_period
    
    def is_stable(self) -> bool:
        """Check if the system is stable (for CONVERGENCE command)"""
        if self.result is None:
            return False
        return self.result.converged and self.result.attractor_type != AttractorType.DIVERGENT
    
    def get_convergence_info(self) -> Dict[str, Any]:
        """Get complete convergence information"""
        if self.result is None:
            return {"analyzed": False}
        
        info = {
            "analyzed": True,
            "attractor_type": self.result.attractor_type.value,
            "converged": self.result.converged,
            "iterations": self.result.iterations,
            "stable": self.is_stable(),
            "final_distance": self.result.final_distance
        }
        
        if self.result.attractor_state:
            info["attractor_state"] = self.get_attractor_state()
        
        if self.result.attractor_period:
            info["attractor_period"] = self.result.attractor_period
        
        return info


# Convenience function for use in other modules
def analyze_system_convergence(
    context,
    update_function,
    max_iterations: int = 1000,
    tolerance: float = 0.001
) -> ConvergenceAnalyzer:
    """
    Analyze the convergence of a HARMONIA-DSL system.
    
    Returns a ConvergenceAnalyzer with the results.
    """
    analyzer = ConvergenceAnalyzer()
    analyzer.analyze_convergence(context, update_function, max_iterations, tolerance)
    return analyzer
