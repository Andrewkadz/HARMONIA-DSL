#!/usr/bin/env python3.11
"""
Test the fixed Φπε parser
"""

from phi_pi_e_interpreter_fixed import PhiPiEInterpreterFixed, FieldContext

def test_program(name, code, description):
    """Test a single program"""
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"DESCRIPTION: {description}")
    print(f"CODE: {code}")
    print(f"{'-'*70}")
    
    try:
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        result = interpreter.execute(code)
        
        print(f"\n✓ SUCCESS")
        print(f"Result: {result}")
        print(f"Final Context:")
        print(f"  Tension: {context.tension.strength:.4f}")
        print(f"  Phase: {context.phase:.4f}")
        print(f"  Charge: {context.charge:.4f}")
        print(f"  Depth: {context.depth}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("="*70)
    print("Fixed Φπε Parser Test Suite")
    print("="*70)
    
    tests = [
        ("Simple Oscillator", "Ε Ψ Ψ Φ Ω", "Basic oscillation pattern"),
        ("Recursive Growth", "Ε Γ Γ Γ Φ Σ Ω", "Recursive expansion"),
        ("Transcendent Recursion", "Ε Π Π Π Φ Σ Ω", "Deep recursion"),
        ("Fusion", "Ε Ε Δ Λ Φ Ω", "State fusion"),
        ("Disruption", "Ε Φ / / Φ Φ Ω", "Disruption and recovery"),
        ("Intentional", "Θ ω Γ Ρ Φ Ω", "Goal-directed process"),
        ("Emergence", "Ε Ξ ζ Λ Σ Ω", "Emergent pattern"),
        ("Micro-Transform", "Ε ε δ δ Φ Ω", "Incremental changes"),
        ("Loop Test", "Ε [ε δ] Φ Ω", "Loop with micro-transforms"),
        ("Complex", "Ε Π Ψ Γ Λ Φ Σ Ω", "Complex multi-operator"),
    ]
    
    results = []
    for name, code, desc in tests:
        success = test_program(name, code, desc)
        results.append((name, success))
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print(f"Success rate: {100*passed/total:.1f}%")

if __name__ == '__main__':
    main()
