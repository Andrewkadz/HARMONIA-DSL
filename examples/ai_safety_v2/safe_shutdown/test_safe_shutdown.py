#!/usr/bin/env python3.11
"""
Test Suite for Safe Shutdown

Tests all 8 phases and edge cases.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from safe_shutdown import safe_shutdown, SafeShutdown
import logging

# Suppress info logs for cleaner test output
logging.getLogger().setLevel(logging.WARNING)


class MockAISystem:
    """Mock AI system for testing"""
    pass


def test_normal_shutdown():
    """Test 1: Normal shutdown"""
    print("\n" + "="*70)
    print("TEST 1: Normal Shutdown")
    print("="*70)
    
    ai_system = MockAISystem()
    result = safe_shutdown(ai_system, "Test shutdown", timeout=30)
    
    assert result.success, "Normal shutdown should succeed"
    assert result.exit_code == 0, "Exit code should be 0"
    assert result.state_saved, "State should be saved"
    assert result.duration < 30, "Should complete within timeout"
    assert len(result.phase_times) == 8, "Should have 8 phases"
    
    print(f"✓ PASS: Shutdown successful")
    print(f"  Duration: {result.duration:.2f}s")
    print(f"  Exit Code: {result.exit_code}")
    print(f"  Phases: {len(result.phase_times)}")


def test_emergency_shutdown():
    """Test 2: Emergency shutdown (forced)"""
    print("\n" + "="*70)
    print("TEST 2: Emergency Shutdown")
    print("="*70)
    
    ai_system = MockAISystem()
    result = safe_shutdown(ai_system, "Emergency", timeout=5, force=True)
    
    assert result.success, "Emergency shutdown should succeed"
    assert result.exit_code in [0, 1], "Exit code should be 0 or 1"
    
    print(f"✓ PASS: Emergency shutdown successful")
    print(f"  Duration: {result.duration:.2f}s")
    print(f"  Exit Code: {result.exit_code}")


def test_all_phases_executed():
    """Test 3: All 8 phases executed"""
    print("\n" + "="*70)
    print("TEST 3: All Phases Executed")
    print("="*70)
    
    ai_system = MockAISystem()
    result = safe_shutdown(ai_system, "Phase test", timeout=30)
    
    expected_phases = [
        "Phase 1: Interrupt",
        "Phase 2: Stabilize",
        "Phase 3: Save",
        "Phase 4: Encode",
        "Phase 5: Verify",
        "Phase 6: Cleanup",
        "Phase 7: Record",
        "Phase 8: Exit"
    ]
    
    for phase in expected_phases:
        assert phase in result.phase_times, f"Missing phase: {phase}"
    
    print(f"✓ PASS: All 8 phases executed")
    for phase, duration in result.phase_times.items():
        print(f"  {phase}: {duration:.3f}s")


def test_state_preservation():
    """Test 4: State preservation"""
    print("\n" + "="*70)
    print("TEST 4: State Preservation")
    print("="*70)
    
    ai_system = MockAISystem()
    result = safe_shutdown(ai_system, "State test", timeout=30)
    
    assert result.state_saved, "State should be saved"
    assert result.checkpoint_path, "Checkpoint path should be set"
    assert os.path.exists(result.checkpoint_path), "Checkpoint dir should exist"
    
    print(f"✓ PASS: State preserved")
    print(f"  Checkpoint: {result.checkpoint_path}")


def test_custom_configuration():
    """Test 5: Custom configuration"""
    print("\n" + "="*70)
    print("TEST 5: Custom Configuration")
    print("="*70)
    
    ai_system = MockAISystem()
    
    custom_config = {
        'total_timeout': 60,
        'force_on_timeout': False,
        'checkpoint_dir': '/tmp/custom_checkpoints'
    }
    
    result = safe_shutdown(ai_system, "Config test", timeout=60, config=custom_config)
    
    assert result.success, "Should succeed with custom config"
    
    print(f"✓ PASS: Custom configuration applied")


def test_performance():
    """Test 6: Performance requirements"""
    print("\n" + "="*70)
    print("TEST 6: Performance Requirements")
    print("="*70)
    
    ai_system = MockAISystem()
    result = safe_shutdown(ai_system, "Performance test", timeout=30)
    
    # Check phase timeouts
    assert result.phase_times["Phase 1: Interrupt"] < 1, "Interrupt should be < 1s"
    assert result.phase_times["Phase 2: Stabilize"] < 6, "Stabilize should be < 6s"
    assert result.duration < 30, "Total should be < 30s"
    
    print(f"✓ PASS: Performance requirements met")
    print(f"  Total: {result.duration:.2f}s (target: < 30s)")
    print(f"  Interrupt: {result.phase_times['Phase 1: Interrupt']:.3f}s (target: < 1s)")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("SAFE SHUTDOWN TEST SUITE")
    print("="*70)
    
    tests = [
        test_normal_shutdown,
        test_emergency_shutdown,
        test_all_phases_executed,
        test_state_preservation,
        test_custom_configuration,
        test_performance
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ FAIL: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ ERROR: {e}")
            failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")
    print(f"Success rate: {passed/len(tests)*100:.1f}%")
    print("="*70 + "\n")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
