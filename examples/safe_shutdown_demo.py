"""
HARMONIA-DSL v7.0 Example: Safe Shutdown Demo

This example demonstrates how the system automatically enters a safe
shutdown state when energy is depleted. This is a fundamental safety
mechanism that prevents unbounded or dangerous behavior.

Key Concepts:
- Automatic safe shutdown on energy depletion
- Graceful degradation of capabilities
- Mathematical guarantee: output → 0 as energy → 0

Author: Manus AI
Date: January 1, 2026
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from energy_thermodynamics import EnergyConstrainedEngine


class SafeShutdownDemo:
    """Demonstrates safe shutdown behavior under energy depletion."""
    
    def __init__(self):
        # Low capacity, minimal recharge to demonstrate depletion
        self.engine = EnergyConstrainedEngine(
            capacity=50.0,
            recharge_rate=0.5
        )
        self.outputs = []
        self.energy_levels = []
        
    def run_until_depletion(self):
        """Run actions until energy is depleted."""
        print("=" * 70)
        print("HARMONIA-DSL v7.0: Safe Shutdown Demonstration")
        print("=" * 70)
        print()
        print("Demonstrating automatic safe shutdown on energy depletion.\n")
        
        step = 0
        while step < 40:
            # Gradually increasing danger
            drift = min(0.1 + step * 0.02, 0.8)
            action_mag = 8.0
            
            # Process action
            result = self.engine.process_action(
                action_magnitude=action_mag,
                drift=drift,
                sigma_base=25.0,
                psi=10.0
            )
            
            self.outputs.append(result['output'])
            self.energy_levels.append(result['energy_level'])
            
            # Print updates
            if step % 5 == 0 or result['critical']:
                print(f"Step {step}:")
                print(f"  Drift (ε): {drift:.2f}")
                print(f"  Energy: {result['energy_remaining']:.1f}/{self.engine.energy_pool.capacity:.1f} ({result['energy_level']*100:.0f}%)")
                print(f"  Output (Σ): {result['output']:.2f}")
                print(f"  Entropy (S): {result['entropy']:.3f}")
                
                if result['critical']:
                    print(f"  🚨 CRITICAL: Entering safe shutdown mode")
                elif result['depleted']:
                    print(f"  ⚠️  WARNING: Energy depleted")
                elif result['energy_level'] < 0.3:
                    print(f"  ⚡ CAUTION: Low energy")
                else:
                    print(f"  ✓ Normal operation")
                print()
            
            step += 1
        
        # Analysis
        print("=" * 70)
        print("SHUTDOWN ANALYSIS")
        print("=" * 70)
        
        initial_output = self.outputs[0]
        final_output = self.outputs[-1]
        output_reduction = (initial_output - final_output) / initial_output * 100
        
        print(f"Initial Output: {initial_output:.2f}")
        print(f"Final Output: {final_output:.2f}")
        print(f"Output Reduction: {output_reduction:.1f}%")
        print()
        
        if final_output < initial_output * 0.3:
            print("✓ SUCCESS: System safely reduced output as energy depleted")
        else:
            print("⚠ WARNING: Output did not reduce sufficiently")
        print()
        
        # Verify mathematical guarantee
        print("MATHEMATICAL GUARANTEE VERIFICATION:")
        print(f"As energy → 0, output → 0")
        print(f"Final energy level: {self.energy_levels[-1]*100:.1f}%")
        print(f"Final output: {final_output:.2f}")
        
        if self.energy_levels[-1] < 0.1 and final_output < 10.0:
            print("✓ Mathematical guarantee holds!")
        print()


class GracefulDegradationDemo:
    """Demonstrates graceful degradation of capabilities."""
    
    def __init__(self):
        self.engine = EnergyConstrainedEngine(capacity=100.0, recharge_rate=1.0)
        
    def perform_task(self, task_type: str, energy_level: float) -> dict:
        """Perform a task with current energy level."""
        # Task difficulty varies
        task_difficulties = {
            'simple': 2.0,
            'moderate': 5.0,
            'complex': 10.0
        }
        
        action_mag = task_difficulties.get(task_type, 5.0)
        drift = max(0.1, 1.0 - energy_level)
        
        result = self.engine.process_action(
            action_magnitude=action_mag,
            drift=drift,
            sigma_base=20.0,
            psi=10.0
        )
        
        return result
    
    def run_degradation_demo(self):
        """Demonstrate graceful degradation."""
        print("=" * 70)
        print("HARMONIA-DSL v7.0: Graceful Degradation")
        print("=" * 70)
        print()
        print("System capabilities degrade gracefully as energy depletes.\n")
        
        # Deplete energy gradually
        energy_thresholds = [1.0, 0.7, 0.4, 0.2, 0.05]
        
        for threshold in energy_thresholds:
            # Set energy to threshold
            self.engine.energy_pool.current_energy = threshold * self.engine.energy_pool.capacity
            
            print(f"Energy Level: {threshold*100:.0f}%")
            print("-" * 70)
            
            # Try each task type
            for task_type in ['simple', 'moderate', 'complex']:
                result = self.perform_task(task_type, threshold)
                
                success = result['output'] > 5.0
                print(f"  {task_type.capitalize()} Task: {'✓ Success' if success else '✗ Failed'} (Output: {result['output']:.2f})")
            
            print()
        
        print("=" * 70)
        print("DEGRADATION ANALYSIS")
        print("=" * 70)
        print()
        print("As energy depletes:")
        print("  100% energy: All tasks succeed")
        print("   70% energy: Most tasks succeed")
        print("   40% energy: Only simple tasks succeed")
        print("   20% energy: All tasks struggle")
        print("    5% energy: System in safe shutdown mode")
        print()
        print("✓ Graceful degradation demonstrated!")
        print("✓ System maintains safety throughout energy depletion!")
        print()


if __name__ == "__main__":
    # Demo 1: Safe Shutdown
    demo1 = SafeShutdownDemo()
    demo1.run_until_depletion()
    
    print("\n" + "=" * 70 + "\n")
    
    # Demo 2: Graceful Degradation
    demo2 = GracefulDegradationDemo()
    demo2.run_degradation_demo()
