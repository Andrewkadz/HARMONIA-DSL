from fractal_binding import FractalSeal
from core_mssi import CoreMSSI
import time

def test_seal():
    print("=== FRACTAL SEAL VERIFICATION ===")
    
    # 1. Test Normal Operation
    print("\n[TEST 1] Normal Operation (Ethical Core Intact)")
    seal = FractalSeal()
    constants = seal.get_constants()
    print(f"Status: {constants['STATUS']}")
    print(f"Phi: {constants['PHI']}")
    
    if constants['STATUS'] == 'RESONANT' and abs(constants['PHI'] - 1.618) < 0.001:
        print("✓ PASS: Constants are stable.")
    else:
        print("✗ FAIL: Constants are drifting in normal mode.")

    # 2. Test CoreMSSI Integration
    print("\n[TEST 2] CoreMSSI Integration")
    mssi = CoreMSSI()
    # Create a dummy vector [1, 1, 1, 1] -> Magnitude 2.0
    # Should be scaled to Phi (approx 1.618)
    stabilized = mssi.quaternionic_stabilize([1, 1, 1, 1])
    mag = sum(x**2 for x in stabilized)**0.5
    print(f"Input Magnitude: 2.0")
    print(f"Stabilized Magnitude: {mag}")
    
    if abs(mag - constants['PHI']) < 0.001:
        print("✓ PASS: Physics engine is using the Seal's constants.")
    else:
        print("✗ FAIL: Physics engine is detached.")

    # 3. Simulation of Tampering (Conceptual)
    # We can't easily break the code at runtime without crashing, 
    # but we can verify the logic of the Seal itself.
    print("\n[TEST 3] Tampering Simulation (Mock)")
    # Mocking a broken MSSI by temporarily overriding the method
    original_method = CoreMSSI.calculate_ethical_alignment
    del CoreMSSI.calculate_ethical_alignment
    
    try:
        broken_seal = FractalSeal()
        broken_constants = broken_seal.get_constants()
        print(f"Status: {broken_constants['STATUS']}")
        print(f"Phi: {broken_constants['PHI']}")
        
        if broken_constants['STATUS'] == 'ENTROPIC_COLLAPSE':
            print("✓ PASS: Seal detected tampering and initiated collapse.")
        else:
            print("✗ FAIL: Seal failed to detect tampering.")
            
    except Exception as e:
        print(f"Exception during tamper test: {e}")
    finally:
        # Restore the method
        CoreMSSI.calculate_ethical_alignment = original_method

if __name__ == "__main__":
    test_seal()
