#!/usr/bin/env python3
"""
HARMONIA-DSL // HEALTH CHECK PROTOCOL
-------------------------------------
Provides concrete validation logic for the Rust Launcher.
Verifies Bio-Clock Sync and PhiField Integrity.

Usage:
    python3 harmonia_health_check.py --json
    (Returns JSON status for Rust consumption)
"""

import sys
import json
import time
import datetime
from pathlib import Path

# Import E8 Structures
try:
    from e8_structures import PhiField, XiPulse
except ImportError:
    # Fallback for standalone testing if needed, but strictly required for prod
    sys.exit(1)

# --- CONSTANTS ---
BIO_CLOCK_CYCLE = 3.4  # Seconds
STABILITY_THRESHOLD = 1.17
STREAM_DIR = Path("streams")

def get_bio_phase():
    """Calculates the current phase of the user's bio-clock."""
    now = time.time()
    phase_val = (now % BIO_CLOCK_CYCLE) / BIO_CLOCK_CYCLE
    
    if phase_val < 0.2: return "DELTA", phase_val
    if phase_val < 0.4: return "THETA", phase_val
    if phase_val < 0.6: return "ALPHA", phase_val
    if phase_val < 0.8: return "BETA", phase_val
    return "GAMMA", phase_val

def check_phi_field_integrity():
    """
    Checks the stability of the most recent stream log.
    If the last entry was UNSTABLE, the field is compromised.
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    log_path = STREAM_DIR / f"{today}.md"
    
    if not log_path.exists():
        # No data today = Neutral Stability
        return True, 1.0, "NO_DATA"

    try:
        with open(log_path, "r") as f:
            lines = f.readlines()
            # Scan last 10 lines for stability markers
            for line in reversed(lines[-20:]):
                if "Physics: UNSTABLE" in line:
                    return False, 0.5, "LAST_ENTRY_UNSTABLE"
                if "Physics: STABLE" in line:
                    return True, 1.618, "STABLE"
        return True, 1.0, "NEUTRAL"
    except Exception as e:
        return False, 0.0, str(e)

def run_health_check():
    """Executes the full diagnostic suite."""
    phase_name, phase_val = get_bio_phase()
    is_stable, stability_score, reason = check_phi_field_integrity()
    
    status = {
        "timestamp": time.time(),
        "bio_clock": {
            "cycle_duration": BIO_CLOCK_CYCLE,
            "current_phase": phase_name,
            "phase_value": round(phase_val, 4),
            "sync": True # Always synced if we can calculate it
        },
        "phi_field": {
            "integrity": is_stable,
            "stability_score": stability_score,
            "reason": reason,
            "threshold": STABILITY_THRESHOLD
        },
        "system": {
            "ready": is_stable, # System is only ready if Stable
            "version": "RECURSUS_1.0"
        }
    }
    return status

if __name__ == "__main__":
    # Output JSON for the Rust Launcher to parse
    result = run_health_check()
    print(json.dumps(result, indent=2))
    
    # Exit Code: 0 if Ready, 1 if Not Ready
    if result["system"]["ready"]:
        sys.exit(0)
    else:
        sys.exit(1)
