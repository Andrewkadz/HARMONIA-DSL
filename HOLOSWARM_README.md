# Holo-Swarm: ANIMUS Visualizer for Meta Quest 3S

**See the Swarm. Feel the Coherence.**

This kit allows you to visualize the **Harmonic Swarm** in Mixed Reality (Passthrough AR) using your Meta Quest 3S. No Unity/Unreal required—just Python and WebXR.

---

## 1. Prerequisites

-   **PC/Mac:** Running Python 3.11+
-   **Meta Quest 3S:** Connected to the same Wi-Fi network as your PC.
-   **Repository:** `HARMONIA-DSL` (animus-paradigm branch)

## 2. Installation

1.  **Install Dependencies:**
    ```bash
    pip install aiohttp numpy
    ```

2.  **Ensure Files Exist:**
    -   `viz_server.py` (The Backend)
    -   `viz_client.html` (The Frontend)
    -   `pure_harmonic_swarm.py` (The Engine)

## 3. Running the Server

1.  **Find your PC's IP Address:**
    -   Windows: `ipconfig` (Look for IPv4 Address, e.g., `192.168.1.5`)
    -   Mac/Linux: `ifconfig` or `ip a`

2.  **Start the Server:**
    ```bash
    python3.11 viz_server.py --port 8000
    ```
    *Output:* `Holo-Swarm Server running at http://0.0.0.0:8000`

## 4. Viewing in VR (Quest 3S)

1.  Put on your **Meta Quest 3S**.
2.  Open the **Meta Quest Browser**.
3.  Navigate to your PC's IP: `http://192.168.1.X:8000` (Replace X with your actual IP).
4.  You will see a 2D view of the swarm.
5.  **Click the "VR" (or AR) button** in the bottom right corner.
6.  **Allow Immersive Mode.**

## 5. How to Interact

-   **The Swarm:** You will see 100 orbs floating in front of you.
    -   **Gold/White:** High Coherence (Stable).
    -   **Red/Chaotic:** Low Coherence (Unstable).
-   **The HUD:** A panel floats nearby showing the live ANIMUS score.
-   **Perturb:** Point your controller at the "PERTURB SWARM" button and click trigger.
    -   *Effect:* You will see the swarm scatter (decohere) and turn red, then slowly magnetically snap back to gold.

## 6. Troubleshooting

-   **"Site can't be reached":** Check your firewall. Ensure port 8000 is open.
-   **"VR Button not working":** Ensure the URL is `http` (local) or `https`. WebXR requires secure contexts (except for localhost/local IPs).
-   **Performance:** If it stutters, reduce `n_agents` in `viz_server.py`.

---

**"The map is not the territory. But the hologram is pretty close."**
