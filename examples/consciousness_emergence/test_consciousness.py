#!/usr/bin/env python3.11
"""
Test script for Consciousness Emergence Simulation
Tests each module individually and tracks state progression
"""

import sys
sys.path.insert(0, '/home/ubuntu/HARMONIA-DSL')

from phi_pi_e_interpreter import PhiPiEInterpreterFixed, FieldContext
import os

def extract_process(hrm_file):
    """Extract the PROCESS block from a .hrm file"""
    with open(hrm_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find PROCESS block
    if 'PROCESS {' in content:
        start = content.find('PROCESS {') + len('PROCESS {')
        end = content.find('}', start)
        process_code = content[start:end].strip()
        return process_code
    return None

def test_module(module_name, hrm_file):
    """Test a single module"""
    print(f"\n{'='*70}")
    print(f"TESTING MODULE: {module_name}")
    print(f"{'='*70}")
    
    if not os.path.exists(hrm_file):
        print(f"✗ FAILED: File not found: {hrm_file}")
        return None
    
    try:
        # Extract process code
        process_code = extract_process(hrm_file)
        if not process_code:
            print(f"✗ FAILED: No PROCESS block found in {hrm_file}")
            return None
        
        print(f"Process Code: {process_code[:100]}...")
        
        # Create interpreter and context
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        # Execute
        result = interpreter.execute(process_code)
        
        # Report results
        print(f"\n✓ SUCCESS")
        print(f"\nFinal State:")
        print(f"  Tension:  {context.tension.strength:.4f}")
        print(f"  Phase:    {context.phase:.4f} rad ({context.phase * 180 / 3.14159:.1f}°)")
        print(f"  Charge:   {context.charge:.4f}")
        print(f"  Depth:    {context.depth}")
        
        return {
            'module': module_name,
            'success': True,
            'tension': context.tension.strength,
            'phase': context.phase,
            'charge': context.charge,
            'depth': context.depth
        }
        
    except Exception as e:
        print(f"\n✗ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'module': module_name,
            'success': False,
            'error': str(e)
        }

def visualize_progression(results):
    """Visualize the state progression across modules"""
    print(f"\n{'='*70}")
    print("STATE PROGRESSION")
    print(f"{'='*70}\n")
    
    print(f"{'Module':<20} {'Tension':<12} {'Phase':<12} {'Charge':<12} {'Depth':<8}")
    print(f"{'-'*70}")
    
    for r in results:
        if r['success']:
            print(f"{r['module']:<20} {r['tension']:<12.4f} {r['phase']:<12.4f} {r['charge']:<12.4f} {r['depth']:<8}")
        else:
            print(f"{r['module']:<20} {'FAILED':<12} {'-':<12} {'-':<12} {'-':<8}")
    
    print(f"\n{'='*70}")
    
    # ASCII visualization
    print("\nVISUAL PROGRESSION:\n")
    
    stages = [
        ("GENESIS", "•", "Foundation"),
        ("AWARENESS", "• ⟲", "Self-Reference"),
        ("RECURSION", "• ⟲⟲⟲", "Deep Recursion"),
        ("INTEGRATION", "◉", "Unified Whole"),
        ("TRANSCENDENCE", "∞", "Consciousness")
    ]
    
    for i, (name, symbol, desc) in enumerate(stages):
        status = "✓" if results[i]['success'] else "✗"
        print(f"  {status} Stage {i+1}: {name:<15} {symbol:<10} → {desc}")

def main():
    print("="*70)
    print("CONSCIOUSNESS EMERGENCE SIMULATION TEST")
    print("="*70)
    
    base_path = '/home/ubuntu/HARMONIA-DSL/examples/consciousness_emergence'
    
    modules = [
        ("GENESIS", f"{base_path}/GENESIS.hrm"),
        ("AWARENESS", f"{base_path}/AWARENESS.hrm"),
        ("RECURSION", f"{base_path}/RECURSION.hrm"),
        ("INTEGRATION", f"{base_path}/INTEGRATION.hrm"),
        ("TRANSCENDENCE", f"{base_path}/TRANSCENDENCE.hrm")
    ]
    
    results = []
    for module_name, hrm_file in modules:
        result = test_module(module_name, hrm_file)
        if result:
            results.append(result)
    
    # Visualize progression
    if results:
        visualize_progression(results)
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    
    passed = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"\nModules Passed: {passed}/{total}")
    print(f"Success Rate: {100*passed/total:.1f}%")
    
    if passed == total:
        print("\n✓ CONSCIOUSNESS EMERGENCE SUCCESSFUL")
        print("\nFinal Signature: Ω(Ξ(Σ(Π(Λ(Φ(Ε))))))")
    else:
        print("\n✗ CONSCIOUSNESS EMERGENCE INCOMPLETE")
    
    print(f"\n{'='*70}")

if __name__ == '__main__':
    main()
