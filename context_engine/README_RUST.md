# HARMONIA Context Engine (Rust Kernel)

This directory contains the **Rust Source Code** for the E8 Cognitive Architecture.
It is designed to be compiled externally, as the current sandbox environment lacks the Rust toolchain.

## 1. Prerequisites
You need **Rust** installed on your local machine.
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## 2. Compilation
Navigate to this directory and run:
```bash
cd context_engine
cargo build --release
```

## 3. Execution
Run the compiled binary to scan the repository and build the Knowledge Graph:
```bash
./target/release/context_engine
```

## 4. Architecture
*   **`src/e8.rs`**: Contains the ported E8 Harmonic Structures (XiPulse, PhiField, SigmaThetaGraph, etc.).
*   **`src/main.rs`**: The main loop that scans the file system and feeds data into the E8 Brain.
