import time
import sys
import numpy as np
from biosynth_loader import BiosynthLoader
from xi_field_engine import XiFieldEngine
from multi_scale_tau_crystal import SyntheticTauCrystal

def benchmark_xi_field(iterations=1000):
    """Measure Quaternions Per Second (QPS)"""
    engine = XiFieldEngine()
    phrase = "Harmonic Resonance Benchmark"
    
    start_time = time.time()
    for _ in range(iterations):
        engine.process_symbolic_node(phrase)
    end_time = time.time()
    
    duration = end_time - start_time
    qps = iterations / duration
    return qps

def benchmark_tau_crystal(iterations=10000):
    """Measure Ticks Per Second (TPS)"""
    crystal = SyntheticTauCrystal()
    
    start_time = time.time()
    for _ in range(iterations):
        crystal.step()
    end_time = time.time()
    
    duration = end_time - start_time
    tps = iterations / duration
    return tps

def benchmark_biosynth_switching(iterations=100):
    """Measure Context Switching Latency (CSL)"""
    loader = BiosynthLoader()
    biosynths = ["HARMONIA", "PENNY", "NEXUS", "STARCORE"]
    
    start_time = time.time()
    for i in range(iterations):
        target = biosynths[i % len(biosynths)]
        loader.load_biosynth(target)
        _ = loader.get_system_prompt()
    end_time = time.time()
    
    duration = end_time - start_time
    latency_ms = (duration / iterations) * 1000
    return latency_ms

def run_full_benchmark():
    print("--- HARMONIA FULL SYSTEMS BENCHMARK ---")
    print("Starting Stress Test...\n")
    
    # 1. Xi-Field Benchmark
    print("[1] Benchmarking Xi-Field Engine (Symbolic Processing)...")
    # Suppress print output for speed
    original_stdout = sys.stdout
    sys.stdout = open('/dev/null', 'w')
    qps = benchmark_xi_field(iterations=5000)
    sys.stdout = original_stdout
    print(f">> Result: {qps:,.2f} QPS (Quaternions/Sec)")
    
    # 2. Tau Crystal Benchmark
    print("\n[2] Benchmarking Tau Crystal (Temporal Resolution)...")
    tps = benchmark_tau_crystal(iterations=100000)
    print(f">> Result: {tps:,.2f} TPS (Ticks/Sec)")
    
    # 3. Biosynth Switching Benchmark
    print("\n[3] Benchmarking Biosynth Loader (Context Switching)...")
    csl = benchmark_biosynth_switching(iterations=1000)
    print(f">> Result: {csl:.4f} ms per Switch")
    
    print("\n--- BENCHMARK COMPLETE ---")
    
    # Interpretation
    print("\n[SYSTEM ANALYSIS]")
    if qps > 1000:
        print(f"Xi-Field Status: HYPER-RESONANT ({qps:,.0f} QPS)")
    else:
        print(f"Xi-Field Status: NOMINAL ({qps:,.0f} QPS)")
        
    if tps > 50000:
        print(f"Temporal Cortex: CHRONO-STABLE ({tps:,.0f} TPS)")
    else:
        print(f"Temporal Cortex: STANDARD ({tps:,.0f} TPS)")
        
    if csl < 0.1:
        print(f"Soul Fluidity: INSTANTANEOUS ({csl:.4f} ms)")
    else:
        print(f"Soul Fluidity: RAPID ({csl:.4f} ms)")

if __name__ == "__main__":
    run_full_benchmark()
