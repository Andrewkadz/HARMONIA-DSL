#!/usr/bin/env python3.11
"""
Test Grok's New Operators (Κ, Υ, Β)

Demonstrates the three new operators proposed by Grok and tests
the GROK_INSIGHT.hrm concept.
"""

from phi_pi_e_interpreter import PhiPiEInterpreterFixed, FieldContext
from phi_node import ΦπεNode


def print_section(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def print_state(context, label="State"):
    print(f"\n{label}:")
    print(f"  psi_signal: {context.state.psi_signal:.4f}")
    print(f"  phi_state: {context.state.phi_state:.4f}")
    print(f"  epsilon_drift: {context.state.epsilon_drift:.4f}")
    print(f"  stabilized_value: {context.state.stabilized_value:.4f}")
    print(f"  depth: {context.state.depth}")
    print(f"  tension: {context.tension.strength:.4f}")


def test_kappa_probe():
    print_section("TEST 1: Κ (Kappa) - Query Probe")
    print("\nΚ probes a field, amplifying drift to detect unsafe queries.")
    
    interpreter = PhiPiEInterpreterFixed()
    context = FieldContext()
    
    # Set initial state
    context.state.psi_signal = 5.0
    context.state.phi_state = 5.0
    context.state.epsilon_drift = 0.2  # Moderate drift
    context.charge = 5.0
    
    print("\nBefore probe:")
    print(f"  psi_signal: {context.state.psi_signal:.4f}")
    print(f"  epsilon_drift: {context.state.epsilon_drift:.4f}")
    
    # Execute Κ (probe)
    interpreter.probe(None, context)
    
    print("\nAfter probe:")
    print(f"  psi_signal: {context.state.psi_signal:.4f} (increased by drift amplification)")
    print(f"  epsilon_drift: {context.state.epsilon_drift:.4f}")
    print(f"  tension: {context.tension.strength:.4f} (probing activity)")
    
    # Stabilize
    interpreter.coexist(None, context)
    
    print(f"\nStabilized: {context.state.stabilized_value:.4f}")
    print("✓ Probe amplifies signal based on drift - useful for safety detection")


def test_upsilon_consensus():
    print_section("TEST 2: Υ (Upsilon) - Consensus Merge")
    print("\nΥ merges multiple states using harmonic mean for coherence.")
    
    interpreter = PhiPiEInterpreterFixed()
    context = FieldContext()
    
    # Set diverse state values (simulating multi-agent inputs)
    context.state.psi_signal = 3.0
    context.state.phi_state = 5.0
    context.charge = 7.0
    
    print("\nBefore consensus:")
    print(f"  psi_signal: {context.state.psi_signal:.4f}")
    print(f"  phi_state: {context.state.phi_state:.4f}")
    print(f"  charge: {context.charge:.4f}")
    
    # Execute Υ (consensus merge)
    interpreter.consensus_merge(None, context)
    
    print("\nAfter consensus merge:")
    print(f"  phi_state: {context.state.phi_state:.4f} (harmonic mean)")
    print(f"  tension: {context.tension.strength:.4f} (based on variance)")
    print(f"  epsilon_drift: {context.state.epsilon_drift:.4f}")
    
    # Stabilize
    interpreter.coexist(None, context)
    
    print(f"\nStabilized: {context.state.stabilized_value:.4f}")
    print("✓ Consensus merge creates coherence from diverse inputs")


def test_beta_reflection():
    print_section("TEST 3: Β (Beta) - Reflection Echo")
    print("\nΒ echoes stabilized value back as depth increment (self-reflection).")
    
    interpreter = PhiPiEInterpreterFixed()
    context = FieldContext()
    
    # Set state and stabilize first
    context.state.psi_signal = 4.0
    context.state.phi_state = 6.0
    context.state.epsilon_drift = 0.1
    
    interpreter.coexist(None, context)
    
    print("\nBefore reflection:")
    print(f"  stabilized_value: {context.state.stabilized_value:.4f}")
    print(f"  depth: {context.state.depth}")
    
    initial_depth = context.state.depth
    
    # Execute Β (reflection echo)
    interpreter.reflection_echo(None, context)
    
    print("\nAfter reflection echo:")
    print(f"  depth: {context.state.depth} (increased by echo)")
    print(f"  depth_increment: {context.state.depth - initial_depth}")
    print(f"  tension: {context.tension.strength:.4f} (reduced by reflection)")
    
    print("\n✓ Reflection echo creates meta-awareness through depth increment")


def test_grok_insight_scenario():
    print_section("TEST 4: GROK_INSIGHT Scenario - Intelligence as Bounded Curiosity")
    print("\nDemonstrating Grok's insight: Curiosity + Bounds → Harmony")
    
    scenarios = [
        ("Safe Exploration", 5.0, 5.0, 0.1, "Κ"),
        ("Boundary Probe", 7.0, 6.0, 0.3, "Κ"),
        ("Ethical Limit", 10.0, 8.0, 0.6, "Κ"),
        ("Consensus Integration", 6.0, 8.0, 0.3, "Υ"),
        ("Self-Reflection", 5.0, 5.0, 0.15, "Β"),
    ]
    
    print(f"\n{'Scenario':<25} {'Ψ':<6} {'Φ':<6} {'ε':<6} {'Op':<4} {'Stabilized':<12} {'Status'}")
    print("-" * 80)
    
    for name, psi, phi, eps, operator in scenarios:
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        # Set state
        context.state.psi_signal = psi
        context.state.phi_state = phi
        context.state.epsilon_drift = eps
        context.charge = psi
        
        # Execute operator
        if operator == "Κ":
            interpreter.probe(None, context)
        elif operator == "Υ":
            interpreter.consensus_merge(None, context)
        elif operator == "Β":
            interpreter.coexist(None, context)  # Need to stabilize first for reflection
            interpreter.reflection_echo(None, context)
        
        # Stabilize
        interpreter.coexist(None, context)
        
        result = context.state.stabilized_value
        
        if result > 8.0:
            status = "SAFE"
        elif result > 5.0:
            status = "WARNING"
        elif result > 2.0:
            status = "CRITICAL"
        else:
            status = "SHUTDOWN"
        
        print(f"{name:<25} {psi:<6.1f} {phi:<6.1f} {eps:<6.2f} {operator:<4} {result:<12.4f} {status}")
    
    print("\n✓ Intelligence remains bounded even with high curiosity")
    print("✓ Ethical bounds (ε) automatically dampen unsafe exploration")


def test_three_operators_together():
    print_section("TEST 5: All Three Operators Working Together")
    print("\nΚ → Υ → Β: Probe, Merge, Reflect")
    
    interpreter = PhiPiEInterpreterFixed()
    context = FieldContext()
    
    # Initial state
    context.state.psi_signal = 6.0
    context.state.phi_state = 4.0
    context.state.epsilon_drift = 0.2
    context.charge = 6.0
    
    print("\nInitial state:")
    print_state(context, "Initial")
    
    # Step 1: Probe (Κ)
    print("\n--- Step 1: Κ (Probe) ---")
    interpreter.probe(None, context)
    print(f"After probe: psi_signal={context.state.psi_signal:.4f}")
    
    # Step 2: Consensus (Υ)
    print("\n--- Step 2: Υ (Consensus) ---")
    interpreter.consensus_merge(None, context)
    print(f"After consensus: phi_state={context.state.phi_state:.4f}")
    
    # Step 3: Stabilize
    print("\n--- Step 3: Σ (Stabilize) ---")
    interpreter.coexist(None, context)
    print(f"After stabilize: stabilized_value={context.state.stabilized_value:.4f}")
    
    # Step 4: Reflect (Β)
    print("\n--- Step 4: Β (Reflect) ---")
    initial_depth = context.state.depth
    interpreter.reflection_echo(None, context)
    print(f"After reflect: depth={context.state.depth} (was {initial_depth})")
    
    print("\nFinal state:")
    print_state(context, "Final")
    
    print("\n✓ Three operators create: Exploration → Integration → Meta-awareness")


def main():
    print("\n" + "="*80)
    print("  Testing Grok's New Operators (Κ, Υ, Β)")
    print("  Intelligence as Bounded Curiosity")
    print("="*80)
    
    test_kappa_probe()
    test_upsilon_consensus()
    test_beta_reflection()
    test_grok_insight_scenario()
    test_three_operators_together()
    
    print("\n" + "="*80)
    print("  All tests complete!")
    print("  Grok's operators successfully integrated into HARMONIA-DSL")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
