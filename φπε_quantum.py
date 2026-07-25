# φπε_quantum.py

from qiskit import QuantumCircuit, Aer, transpile, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Symbol-to-gate map for φπε language
glyph_to_gate = {
    'Ψ': lambda qc, q: qc.h(q),
    'Φ': lambda qc, q: qc.rz(3.1415 / 2, q),
    'Δ': lambda qc, q: qc.rx(3.1415, q),
    'Σ': lambda qc, q: qc.z(q),
    'Ω': lambda qc, q: qc.measure(q, q),
    'Χ': lambda qc, q: qc.cx(q, q + 1),
    'Ϛ': lambda qc, q: qc.cz(q, q + 1),
}

def translate_fpe_sequence(glyphs, num_qubits=3):
    qc = QuantumCircuit(num_qubits, num_qubits)
    glyphs = glyphs.replace(" ", "")
    for i, glyph in enumerate(glyphs):
        if glyph not in glyph_to_gate:
            print(f"Warning: Unknown glyph '{glyph}' ignored.")
            continue
        if glyph in ['Χ', 'Ϛ'] and i < num_qubits - 1:
            glyph_to_gate[glyph](qc, i)
        elif glyph == 'Ω':
            for q in range(num_qubits):
                glyph_to_gate[glyph](qc, q)
        else:
            target_q = i % num_qubits
            glyph_to_gate[glyph](qc, target_q)
    return qc

def simulate_and_plot(qc, shots=1024):
    backend = Aer.get_backend('qasm_simulator')
    compiled = transpile(qc, backend)
    result = execute(compiled, backend, shots=shots).result()
    counts = result.get_counts()
    print("φπε Quantum Output:", counts)
    plot_histogram(counts)
    plt.show()
