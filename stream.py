#!/usr/bin/env python3
"""
HARMONIA-DSL // HARMONIC STREAM (stream.py)
-------------------------------------------
Zero-Friction Cognitive Logging Interface for High-Gamma Minds.
Connects directly to the E8 Cognitive Architecture.

Usage:
    python3 stream.py "Your thought here"
    python3 stream.py --tag "PROJECT_X" "Thought related to Project X"
    python3 stream.py --status

Function:
    1. Wraps input text in a XiPulse (Signal).
    2. Calculates Mass (Length) and Charge (Sentiment/Keywords).
    3. Feeds into PhiField (Stabilizer).
    4. Appends to Daily Stream Log (streams/YYYY-MM-DD.md).
"""

import sys
import os
import argparse
import datetime
import math
from pathlib import Path

# Import E8 Cognitive Structures
try:
    from e8_structures import XiPulse, PhiField, SigmaThetaGraph
except ImportError as e:
    print(f"CRITICAL ERROR: e8_structures.py not found or failed to import: {e}")
    print("Ensure you are running this from the HARMONIA-DSL root directory.")
    sys.exit(1)

# --- CONFIGURATION ---
STREAM_DIR = Path("streams")
BIO_CLOCK_CYCLE = 3.4  # Seconds (User's Bio-Resonance)

def ensure_stream_dir():
    """Ensures the streams directory exists."""
    if not STREAM_DIR.exists():
        STREAM_DIR.mkdir()
        print(f"[*] Created Stream Directory: {STREAM_DIR}")

def get_daily_log_path():
    """Returns the path for today's stream log."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return STREAM_DIR / f"{today}.md"

def calculate_bio_phase():
    """Calculates the current phase of the user's bio-clock."""
    now = datetime.datetime.now().timestamp()
    phase = (now % BIO_CLOCK_CYCLE) / BIO_CLOCK_CYCLE
    if phase < 0.2: return "DELTA (Anchor)"
    if phase < 0.4: return "THETA (Dream)"
    if phase < 0.6: return "ALPHA (Bridge)"
    if phase < 0.8: return "BETA (Work)"
    return "GAMMA (Burst)"

def process_stream(content, tags=None):
    """
    Processes a raw thought stream through the E8 physics engine.
    """
    # 1. Create XiPulse (The Signal)
    # XiPulse(source, magnitude, harmonic_bias)
    pulse = XiPulse(
        source="USER_STREAM",
        magnitude=len(content) / 100.0,  # Magnitude based on length
        harmonic_bias=1.618  # Default Phi bias
    )
    
    # 2. Calculate Physics
    mass = len(content) / 100.0  # Cognitive Mass
    # Simple keyword-based charge detection
    charge = 1.0
    if "?" in content: charge = 0.5 # (Inquiry)
    if "!" in content: charge = 1.5 # (Insight)
    if "fail" in content.lower() or "error" in content.lower(): charge = -1.0 # (Entropy)
    
    # 3. Stabilize via PhiField
    # PhiField(inputs=[])
    field = PhiField(inputs=[])
    field.add_signal(pulse.magnitude) # PhiField expects numeric inputs in current impl
    stability_score = field.stability
    is_stable = stability_score > 1.17 # User's Stability Threshold
    
    # 4. Format Output
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    bio_phase = calculate_bio_phase()
    
    entry = f"""
## [{timestamp}] {bio_phase} // STABILITY: {stability_score:.2f}
**SIGNAL:** `{content}`
*   **Mass:** {mass:.2f} | **Charge:** {charge:.2f}
*   **Tags:** {tags if tags else "None"}
*   **Physics:** {"STABLE" if is_stable else "UNSTABLE"}
---
"""
    return entry

def main():
    parser = argparse.ArgumentParser(description="HARMONIA-DSL Harmonic Stream")
    parser.add_argument("content", nargs="*", help="The thought content to stream.")
    parser.add_argument("--tag", help="Optional tag for the stream.")
    parser.add_argument("--status", action="store_true", help="Show current system status.")
    
    args = parser.parse_args()
    
    ensure_stream_dir()
    log_path = get_daily_log_path()
    
    # Handle Status Check
    if args.status:
        print(f"\n--- HARMONIA STREAM STATUS ---")
        print(f"Bio-Clock: {BIO_CLOCK_CYCLE}s")
        print(f"Current Phase: {calculate_bio_phase()}")
        print(f"Log File: {log_path}")
        if log_path.exists():
            print(f"Today's Mass: {log_path.stat().st_size} bytes")
        else:
            print("Today's Mass: 0 bytes (No streams yet)")
        return

    # Handle Content Stream
    if not args.content:
        # Interactive Mode if no args
        print(f"--- HARMONIA STREAM [INTERACTIVE] ---")
        print(f"Phase: {calculate_bio_phase()}")
        print("Type your stream (Ctrl+C to exit):")
        try:
            while True:
                user_input = input(f"[{datetime.datetime.now().strftime('%H:%M')}] > ")
                if user_input.strip():
                    entry = process_stream(user_input, args.tag)
                    with open(log_path, "a") as f:
                        f.write(entry)
                    print(f"   >>> Absorbed. (Log: {log_path.name})")
        except KeyboardInterrupt:
            print("\nStream Closed.")
            return
    else:
        # One-shot Mode
        content = " ".join(args.content)
        entry = process_stream(content, args.tag)
        
        # Initialize file if new
        if not log_path.exists():
            with open(log_path, "w") as f:
                f.write(f"# HARMONIC STREAM LOG // {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
                f.write(f"User: Resonator | Threshold: 1.17 | Clock: {BIO_CLOCK_CYCLE}s\n\n")
        
        with open(log_path, "a") as f:
            f.write(entry)
        
        print(f"Stream Absorbed. [{calculate_bio_phase()}]")

if __name__ == "__main__":
    main()
