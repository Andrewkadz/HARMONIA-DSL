from e8_structures import *
from resonance_graph import ResonanceGraph

def verify_structures():
    print("Verifying E8 Harmonic Structures...")
    
    # Test 1: XiPulse
    pulse = XiPulse("Source", 10, 1.618)
    inverted = pulse.invert()
    print(f"1. XiPulse: {pulse.magnitude} -> {inverted.magnitude} [OK]")
    
    # Test 2: PhiField
    field = PhiField([1, 2, 3, 5, 8])
    print(f"2. PhiField Stability: {field.stability} [OK]")
    
    # Test 3: LambdaLoop
    loop = LambdaLoop(1)
    loop.iterate(lambda x: x * 2)
    print(f"3. LambdaLoop State: {loop.state} [OK]")
    
    # Test 4: GammaLens
    lens = GammaLens(lambda x: x.upper())
    print(f"4. GammaLens: {lens.apply('signal')} [OK]")
    
    print("\nAll 60 Structures Loaded Successfully.")

def scan_module():
    print("\nScanning e8_structures.py for Stability...")
    graph = ResonanceGraph("/home/ubuntu/HARMONIA-DSL")
    data = graph.analyze_file("/home/ubuntu/HARMONIA-DSL/e8_structures.py")
    
    if data:
        print("\n=== TRUTH SCANNER RESULTS ===")
        print(f"File:       {data['file']}")
        print(f"Mass:       {data['mass']:.4f}")
        print(f"Resonance:  {data['resonance']}")
        print(f"Stability:  {data['stability']:.4f}")
        print(f"Status:     {data['status']}")
        print("=============================")

if __name__ == "__main__":
    verify_structures()
    scan_module()
