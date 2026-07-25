# HARMONIA-DSL: Mac Deployment Guide

This guide will help you run the HARMONIA Hive Mind Console on your local Mac using Windsurf.

## Prerequisites

1.  **Python 3.10+**: Ensure you have Python installed (`python3 --version`).
2.  **Ollama (Optional but Recommended)**:
    *   Download from [ollama.com](https://ollama.com).
    *   Run `ollama run llama2` (or your preferred model) in a separate terminal window to start the local AI server.
    *   *Note: The system will still work without Ollama, but "Swarm Intelligence" features will use mock logic.*

## Quick Start (Windsurf)

Open the `HARMONIA-DSL` folder in Windsurf and run these 3 commands in the integrated terminal:

### 1. Create a Virtual Environment (Recommended)
This keeps your Mac clean and prevents library conflicts.
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
This installs NumPy, Matplotlib, and other required libraries.
```bash
pip install -r requirements.txt
```

### 3. Run the Hive Mind
Launch the console.
```bash
python3 harmonic_console.py
```

## What to Expect

*   **The Console**: You will see the `HARMONIA HIVE CONSOLE v2.0` banner.
*   **Interaction**: Type natural language queries (e.g., "Analyze the stability of the system").
*   **Visualization**: When the CRM simulation runs, a window should pop up showing the 3-stage heatmap (Reaction, Midpoint, Result).
*   **Ollama**: If Ollama is running, you will see `[SWARM]` logs indicating it is analyzing your intent.

## Troubleshooting

*   **"Module not found"**: Make sure you ran `pip install -r requirements.txt` *after* activating the virtual environment.
*   **"Connection refused" (Ollama)**: Ensure Ollama is running in the background (`ollama serve` or the desktop app).
*   **Visualization doesn't appear**: On some Macs, you might need to install `python3-tk` (`brew install python-tk`) if the window doesn't show, but usually `matplotlib` handles this automatically.

*End of Line.*
