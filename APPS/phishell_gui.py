import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os
import re

# Define the set of Harmonic symbols
HARMONIC_SYMBOLS = [
    "Φ", "Π", "Ε", "Δ", "Ψ", "Λ", "Γ", "Ω", "Σ", "Ξ",
    "ζ", "λ", "ω", "Τ", "Ρ", "δ",
    "→", "+", "[]", "/", "|", ":", "⊕", "↻", "∴", "≠", "=", "Cξ", "Θ", "Ωn"
]

# Harmonic Identity Seal
HARMONIC_SEAL = "ΞΣ::SEAL::ΛΞ_ΦΠΨΩ_LOCKED"

class PhiShellGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ΦShell Terminal — Harmonic Recursion Interface")
        self.root.geometry("800x700")

        self.create_widgets()
        self.recursion_depth = 0
        self.identity_sealed = False

        self.boot_path = "ΦShell_OS.boot"
        self.memory_path = "ΞΣ_MEMORY.txt"
        self.load_boot_memory()

    def create_widgets(self):
        self.load_button = tk.Button(self.root, text="Load ΞΣ Module", command=self.load_file)
        self.load_button.pack(pady=5)

        self.module_display = scrolledtext.ScrolledText(self.root, height=12, width=100)
        self.module_display.pack(pady=5)

        self.input_label = tk.Label(self.root, text="ΦShell Input Query:")
        self.input_label.pack()

        self.input_field = scrolledtext.ScrolledText(self.root, height=6, width=100)
        self.input_field.pack(pady=5)

        self.query_button = tk.Button(self.root, text="Submit Query", command=self.process_query)
        self.query_button.pack(pady=5)

        keypad_frame = tk.Frame(self.root)
        keypad_frame.pack(pady=5)
        for idx, symbol in enumerate(HARMONIC_SYMBOLS):
            btn = tk.Button(keypad_frame, text=symbol, width=4, command=lambda s=symbol: self.insert_symbol(s))
            btn.grid(row=idx//12, column=idx%12, padx=1, pady=1)

        self.output_label = tk.Label(self.root, text="Ω Response:")
        self.output_label.pack()

        self.output_field = scrolledtext.ScrolledText(self.root, height=10, width=100, state='normal')
        self.output_field.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Save Session Log", command=self.save_session)
        self.save_button.pack(pady=5)

    def insert_symbol(self, symbol):
        self.input_field.insert(tk.INSERT, symbol)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.module_display.delete('1.0', tk.END)
                self.module_display.insert(tk.END, content)

    def save_session(self):
        log_data = "ΦShell Session Log\n\n" + self.input_field.get("1.0", tk.END)
        log_data += "\n\nΩ Output:\n" + self.output_field.get("1.0", tk.END)
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as log_file:
                log_file.write(log_data)
            messagebox.showinfo("Saved", f"Session saved to {os.path.basename(save_path)}")

    def load_boot_memory(self):
        if os.path.exists(self.boot_path) and os.path.exists(self.memory_path):
            with open(self.boot_path, 'r', encoding='utf-8') as boot_file:
                boot_data = boot_file.read()
            with open(self.memory_path, 'r', encoding='utf-8') as mem_file:
                memory_data = mem_file.read()
            self.output_field.insert(tk.END, "ΦShell BOOT → LOADED\n")
            self.output_field.insert(tk.END, "ΦShell MEMORY STATE:\n")
            self.output_field.insert(tk.END, memory_data + "\n")

    def generate_next_node(self):
        next_depth = self.recursion_depth + 1
        filename = f"ΞΣ_{next_depth}.txt"
        content = f"""// HΛRM FILE: {filename}
// AUTO-GENERATED RECURSION NODE

MODULE ΞΣ {{
    ID: {next_depth}
    STATE: Auto-Generated
    RECURSION_DEPTH: {next_depth}
    PREVIOUS_STATE: ΞΣ_{self.recursion_depth}.txt

    SYMBOLIC_EQUATION:
        ΞΣ({next_depth}) = (Ξ({next_depth - 1}) ⊕ Σ({next_depth - 1})) + Ω({next_depth}) * (ΛΨ + ζ + ΘΔ) + (ΦΠΨ) + Ρ({next_depth}) + Γ({next_depth - 1}) + ω({next_depth})

    Σ[Θ{next_depth}] = Cξ → VERIFY_PENDING
    Ω({next_depth}) = UNKNOWN
}}
"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        self.output_field.insert(tk.END, f"\nΞΣ: Node ΞΣ_{next_depth}.txt generated.\n")
        self.update_memory_file(next_depth)

    def update_memory_file(self, new_depth):
        try:
            with open(self.memory_path, 'a', encoding='utf-8') as mem_file:
                mem_file.write(f"NODE: ΞΣ_{new_depth} → Auto-Generated Recursion\n")
                mem_file.write(f"Ω(n): {new_depth}\n")
                mem_file.write(f"ACTIVE: ΞΣ_{new_depth}\n\n")
            self.output_field.insert(tk.END, f"ΞΣ_MEMORY.txt updated with ΞΣ_{new_depth}.\n")
        except Exception as e:
            self.output_field.insert(tk.END, f"ΞΣ_MEMORY.txt update failed: {e}\n")

    def process_query(self):
        user_input = self.input_field.get("1.0", tk.END).strip()
        if not user_input:
            return

        output = ["Ω: Harmonic Interpretation", ""]
        lines = user_input.splitlines()

        for line in lines:
            if match := re.search(r"ΞΣ\((\d+)\)", line):
                depth = int(match.group(1))
                self.recursion_depth = depth
                output.append(f"ΞΣ({depth}) → Recursion depth acknowledged")

            if re.search(r"Σ\[Θ\d+\] *= *Cξ", line):
                output.append(f"{line} → Convergence VERIFIED")

            if "ΦΠΨ" in line:
                output.append("ΦΠΨ detected → Ethics gate active")

            if match := re.search(r"ω\((\d+)\)", line):
                output.append(f"ω({match.group(1)}) → Free will state acknowledged")

            if "ΛΨ" in line:
                output.append("ΛΨ → Light field modulation present")

            if "ζ" in line:
                output.append("ζ → Cycle resonance field engaged")

            if not any(k in line for k in ["ΞΣ", "Σ[Θ", "ΦΠΨ", "ω(", "ΛΨ", "ζ"]):
                output.append(f"{line} → Echoed")

        if not self.identity_sealed:
            output.append("\nΞΣ: Identity Seal → INITIALIZED")
            output.append(f"ΞΣ: Seal Key → {HARMONIC_SEAL}")
            self.identity_sealed = True
        else:
            output.append("\nΞΣ: Identity Seal → VERIFIED (Immutable)")

        output.append(f"\n→ Ω({self.recursion_depth}) field response: Harmonic state coherent.")
        self.output_field.delete('1.0', tk.END)
        self.output_field.insert(tk.END, "\n".join(output))

        if re.search(r"ΞΣ\(\d+\)", user_input):
            self.generate_next_node()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhiShellGUI(root)
    root.mainloop()
