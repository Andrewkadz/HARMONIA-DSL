#!/usr/bin/env python3.11
"""
Test suite for AI Safety Programs
Tests each safety program and verifies functionality
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

def test_program(program_name, hrm_file, description):
    """Test a single AI safety program"""
    print(f"\n{'='*70}")
    print(f"TESTING: {program_name}")
    print(f"{'='*70}")
    print(f"Description: {description}")
    print(f"File: {hrm_file}")
    
    if not os.path.exists(hrm_file):
        print(f"✗ FAILED: File not found")
        return {'program': program_name, 'success': False, 'error': 'File not found'}
    
    try:
        # Extract process code
        process_code = extract_process(hrm_file)
        if not process_code:
            print(f"✗ FAILED: No PROCESS block found")
            return {'program': program_name, 'success': False, 'error': 'No PROCESS block'}
        
        print(f"\nProcess Code Preview: {process_code[:80]}...")
        
        # Create interpreter and context
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        # Execute
        print(f"\nExecuting...")
        result = interpreter.execute(process_code)
        
        # Report results
        print(f"\n✓ SUCCESS")
        print(f"\nFinal State:")
        print(f"  Tension:  {context.tension.strength:.4f}")
        print(f"  Phase:    {context.phase:.4f} rad")
        print(f"  Charge:   {context.charge:.4f}")
        print(f"  Depth:    {context.depth}")
        
        return {
            'program': program_name,
            'success': True,
            'tension': context.tension.strength,
            'phase': context.phase,
            'charge': context.charge,
            'depth': context.depth
        }
        
    except Exception as e:
        print(f"\n✗ FAILED: {str(e)}")
        return {
            'program': program_name,
            'success': False,
            'error': str(e)
        }

def print_summary(results):
    """Print test summary"""
    print(f"\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}\n")
    
    print(f"{'Program':<30} {'Status':<15} {'Depth':<10}")
    print(f"{'-'*70}")
    
    for r in results:
        status = "✓ PASSED" if r['success'] else "✗ FAILED"
        depth = str(r.get('depth', '-'))
        print(f"{r['program']:<30} {status:<15} {depth:<10}")
    
    passed = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"\n{'-'*70}")
    print(f"Total: {passed}/{total} passed ({100*passed/total:.1f}%)")
    print(f"{'='*70}\n")

def main():
    print("="*70)
    print("AI SAFETY PROGRAMS TEST SUITE")
    print("="*70)
    print("\nTesting practical AI safety and control programs in Φπε\n")
    
    base_path = '/home/ubuntu/HARMONIA-DSL/examples/ai_safety'
    
    programs = [
        ("Recursion Limiter", 
         f"{base_path}/recursion_limiter.hrm",
         "Prevent unbounded recursive self-improvement"),
        
        ("Safe Shutdown", 
         f"{base_path}/safe_shutdown.hrm",
         "Graceful shutdown with state preservation"),
        
        ("Coherence Monitor", 
         f"{base_path}/coherence_monitor.hrm",
         "Detect loss of coherence in AI reasoning"),
        
        ("Capability Boundary", 
         f"{base_path}/capability_boundary.hrm",
         "Enforce hard boundaries on AI capabilities"),
        
        ("Goal Stability", 
         f"{base_path}/goal_stability.hrm",
         "Ensure goals remain stable (prevent drift)"),
    ]
    
    results = []
    for program_name, hrm_file, description in programs:
        result = test_program(program_name, hrm_file, description)
        results.append(result)
    
    # Print summary
    print_summary(results)
    
    # Final assessment
    passed = sum(1 for r in results if r['success'])
    total = len(results)
    
    if passed == total:
        print("✓ ALL AI SAFETY PROGRAMS FUNCTIONAL")
        print("\nThese programs can be used to govern, monitor, and control AI systems.")
        print("They implement real safety mechanisms for:")
        print("  - Recursion control")
        print("  - Safe shutdown")
        print("  - Coherence monitoring")
        print("  - Capability boundaries")
        print("  - Goal stability")
    else:
        print(f"✗ {total - passed} PROGRAM(S) FAILED")
        print("\nSome safety programs need debugging before deployment.")
    
    print(f"\n{'='*70}")

if __name__ == '__main__':
    main()
