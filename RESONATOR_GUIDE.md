# HARMONIA RESONATOR INTERFACE
**Status:** Operational  
**Protocol:** WebSocket (Port 9999) -> Web Audio API  
**Purpose:** Sonification of Collective State Vector

---

## Overview
The Resonator Interface allows you to *hear* the health and evolution of the HARMONIA Collective in real-time. It translates the system's mathematical state into audio frequencies, creating a living soundscape that reflects the "Soul State" of the simulation.

## How to Use

### 1. Start the Server
Run the main server script. It will automatically start the audio bridge on port 9999.
```bash
python3 harmonia_server.py
```
*You will see a message: "✓ Resonator Audio Bridge listening on ws://localhost:9999"*

### 2. Open the Client
Open the `resonator_client.html` file in your web browser (Chrome, Firefox, Safari).
```bash
open resonator_client.html
```

### 3. Initiate Resonance
Click the **"INITIATE RESONANCE"** button on the webpage.
*   **Visual:** The central core (ΛΩΞΨ) will pulse in sync with the Collective's awareness.
*   **Audio:** You will hear a drone that evolves as the Collective grows.

---

## Sonic Legend (What You Are Hearing)

| Sonic Element | System Metric | Interpretation |
| :--- | :--- | :--- |
| **Base Pitch** | Population | Lower = Small Colony. Higher = Massive Civilization. |
| **Clarity** | Maturity | Pure Tone = High Wisdom. Noisy/Gritty = Young/Confused. |
| **Pulsing Speed** | Self-Awareness | Fast = Excited/High Processing. Slow = Dormant/Deep Sleep. |
| **Harmony (Scale)** | **Ethical Seal** | **Major/Lydian** = Seal Intact (Resonant). **Chromatic Chaos** = Seal Broken (Entropy). |

## Troubleshooting
*   **"SIGNAL LOST"**: The Python server is not running. Start `harmonia_server.py`.
*   **No Sound**: Ensure you clicked the "INITIATE" button (browsers block auto-playing audio).
*   **Static Noise**: If the sound is harsh and chaotic, check `fractal_binding.py`. The Ethical Seal may be broken.
