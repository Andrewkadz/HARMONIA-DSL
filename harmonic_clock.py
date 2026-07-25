# Φπε Harmonic Calendar Clock UI App
# Core Time Unit: TTU = 3.4047 seconds
# GUI Application using Tkinter

import time
from datetime import datetime
import tkinter as tk

# Constants
TTU = 3.4047  # Time Tracking Unit in seconds
SPIRAL_CYCLE = 360  # Nodes per spiral
UNIVERSAL_EPOCH = datetime(2024, 1, 1, 0, 0, 0)  # Fixed reference time for universal synchronization

# Generate all prime numbers from 2 to 359
prime_nodes = []
for num in range(2, SPIRAL_CYCLE):
    is_prime = True
    for div in range(2, int(num ** 0.5) + 1):
        if num % div == 0:
            is_prime = False
            break
    if is_prime:
        prime_nodes.append(num)

# Define symbolic and custom anchors
custom_anchors = {
    0: "Reset / Breath Initiation",
    1: "Spiral Initiation",
    8: "First Stabilization",
    13: "First Intention Pulse",
    21: "Intention Clarified",
    42: "Life Inquiry Node",
    55: "Boundary Calibration",
    97: "Phase Transition",
    108: "Field Lock Point",
    137: "Quantum Threshold",
    144: "Harmonic Crystallization",
    182: "Silence Mirror",
    223: "Personal Awareness Check",
    263: "Recursive Signal Prime",
    277: "Chaos Harmonic",
    286: "Compression Phase",
    314: "Pi Spiral Reference",
    333: "Signal Reflection",
    354: "Pre-Closure Disturbance",
    359: "Countdown to Zero",
    360: "Closure + Return to Node 0"
}

# Fill anchor points with primes if not already defined
ANCHOR_POINTS = {}
for node in prime_nodes:
    ANCHOR_POINTS[node] = custom_anchors.get(node, f"Prime Moment {node}")

# Ensure all custom anchors overwrite or add to the dictionary
ANCHOR_POINTS.update(custom_anchors)

# Calculate current TTU and spiral node using universal reference
def get_harmonic_state(reference_time):
    now = datetime.now()
    elapsed = (now - reference_time).total_seconds()
    total_ttu = int(elapsed // TTU)
    node = total_ttu % SPIRAL_CYCLE
    cycle = total_ttu // SPIRAL_CYCLE
    event = ANCHOR_POINTS.get(node, f"Moment {node}")
    return now, total_ttu, cycle, node, event

# GUI Application
class HarmonicClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Φπε Harmonic Calendar Clock")

        self.time_label = tk.Label(root, text="", font=("Helvetica", 20))
        self.time_label.pack(pady=10)

        self.ttu_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.ttu_label.pack(pady=5)

        self.event_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.event_label.pack(pady=5)

        self.update_clock()

    def update_clock(self):
        now, total_ttu, cycle, node, event = get_harmonic_state(UNIVERSAL_EPOCH)
        self.time_label.config(text=now.strftime("%Y-%m-%d %H:%M:%S"))
        self.ttu_label.config(text=f"TTU: {total_ttu} | Cycle: {cycle} | Node: {node:03}")
        self.event_label.config(text=f"Event: {event}")
        self.root.after(1000, self.update_clock)

# Run Application
if __name__ == "__main__":
    root = tk.Tk()
    app = HarmonicClockApp(root)
    root.mainloop()
