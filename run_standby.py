#!/usr/bin/env python3
"""
HARMONIA-DSL // STANDBY MODE
----------------------------
Maintains system heartbeat (3.4s) with minimal energy consumption.
Keeps the PhiField active and ready for Gamma Bursts.

Usage:
    python3 run_standby.py
"""

import time
import sys
import datetime
from e8_structures import PhiField

# --- CONFIGURATION ---
BIO_CLOCK_CYCLE = 3.4  # Seconds

def run_standby():
    print("=== HARMONIA SYSTEM STANDBY ===")
    print(f"[*] Bio-Clock: {BIO_CLOCK_CYCLE}s")
    print(f"[*] PhiField: ACTIVE (Monitoring for Signals)")
    print("[*] Press Ctrl+C to Wake/Exit")
    print("-" * 40)

    # Initialize Field
    field = PhiField()
    
    try:
        while True:
            # 1. Wait for Bio-Clock Cycle
            time.sleep(BIO_CLOCK_CYCLE)
            
            # 2. Log Heartbeat
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] ♥ SYSTEM_HEARTBEAT | Stability: {field.stability:.2f} | Status: STANDBY")
            
            # 3. (Optional) Check for 'Wake' Signals in streams/
            # If a new file appears, we could auto-wake.
            # For now, we just pulse.
            
    except KeyboardInterrupt:
        print("\n[!] SYSTEM WAKE SIGNAL DETECTED.")
        print("[!] Exiting Standby Mode.")
        sys.exit(0)

if __name__ == "__main__":
    run_standby()
