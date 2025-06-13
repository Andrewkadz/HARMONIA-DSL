# HΛRM GUI: Harmonia_Coder.py — OS-Themed Symbolic App
# Central Nexus Interface with Keyboard, Editor, and Memory Management
# Includes: Black/Gold theme, custom symbolic keyboard, program management

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import os
import re

# Define the set of Harmonic symbols
HARMONIC_SYMBOLS = [
    "Φ", "Π", "Ε", "Δ", "Ψ", "Λ", "Γ", "Ω", "Σ", "Ξ",
    "ζ", "λ", "ω", "Τ", "Ρ", "δ",
    "→", "+", "[]", "/", "|", ":", "⊕", "↻", "∴", "≠", "=", "Cξ", "Θ", "Ωn"
]

class HarmoniaCoder:
    def __init__(self, root):
        self.root = root
        self.root.title("Harmonia OS — Nexus Interface")
        self.root.geometry("1200x800")
        self.root.configure(bg="black")

        self.set_theme()
        self.setup_ui()

    def insert_symbol(self, symbol):
        """Insert selected symbol into editor"""
        self.editor.insert(tk.INSERT, symbol)
        self.editor.see(tk.END)
    def __init__(self, root):
        self.root = root
        self.root.title("Harmonia OS — Symbolic DSL Environment")
        self.root.geometry("1100x750")
        self.root.configure(bg="black")

        self.set_theme()
        self.setup_ui()

    def set_theme(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background="black", foreground="#FFD700", fieldbackground="black")
        style.configure("TButton", background="black", foreground="#FFD700", borderwidth=1, focusthickness=2)
        style.map("TButton", background=[("active", "#333333")])
        style.configure("TNotebook", background="black", foreground="#FFD700")
        style.configure("TNotebook.Tab", background="black", foreground="#FFD700")
        style.map("TNotebook.Tab", background=[("selected", "#1a1a1a")], foreground=[("selected", "#FFD700")])

    def setup_ui(self):
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=True, fill='both')

        # Editor with Keyboard tab
        self.editor_frame = ttk.Frame(self.tabs)
        self.tabs.add(self.editor_frame, text='ΞΣ DSL Editor')

        editor_subframe = tk.Frame(self.editor_frame, bg="black")
        editor_subframe.pack(fill='both', expand=True)

        # Editor with keyboard
        editor_container = tk.Frame(editor_subframe, bg="black")
        editor_container.pack(fill='both', expand=True)

        self.editor = scrolledtext.ScrolledText(editor_container, height=20, bg="black", fg="#FFD700", insertbackground="#FFD700")
        self.editor.pack(side='left', expand=True, fill='both', padx=10, pady=10)

        # Add keyboard frame
        keyboard_frame = tk.Frame(editor_container, bg="black")
        keyboard_frame.pack(side='right', fill='y', pady=10)

        # Create keyboard buttons
        for idx, symbol in enumerate(HARMONIC_SYMBOLS):
            btn = tk.Button(keyboard_frame, text=symbol, width=4, bg="black", fg="#FFD700", 
                           command=lambda s=symbol: self.insert_symbol(s))
            btn.grid(row=idx//8, column=idx%8, padx=1, pady=1)

        self.program_listbox = tk.Listbox(editor_subframe, width=30, bg="black", fg="#FFD700", selectbackground="#333333", highlightthickness=0)
        self.program_listbox.pack(side='right', fill='y', pady=10)
        self.refresh_program_list()

        self.program_listbox.bind("<<ListboxSelect>>", self.load_selected_program)

        button_frame = ttk.Frame(self.editor_frame)
        button_frame.pack()
        ttk.Button(button_frame, text="Parse", command=self.parse_input).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Run Φπε", command=self.run_phiepsilon).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Refresh Programs", command=self.refresh_program_list).pack(side='left', padx=5)

        # Output tabs
        self.memory_tab = self.add_tab_view("ΞΣ Memory", "ΞΣ_MEMORY.txt")
        self.index_tab = self.add_tab_view("ΞΣ Index", "ΞΣ_Index.txt")
        self.tree_tab = self.add_tab_view("ΞΣ Tree View", "ΞΣ_TREE_VIEW.txt")
        self.response_tab = self.add_tab_view("ΦShell Response", "PhiShell_response.txt")

    def refresh_program_list(self):
        self.program_listbox.delete(0, tk.END)
        files = sorted([f for f in os.listdir() if f.endswith(".hrm") or f.endswith(".txt")])
        for f in files:
            self.program_listbox.insert(tk.END, f)

    def load_selected_program(self, event):
        selection = self.program_listbox.curselection()
        if selection:
            filename = self.program_listbox.get(selection[0])
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.editor.delete("1.0", tk.END)
                    self.editor.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load {filename}: {e}")

    def add_tab_view(self, title, filepath):
        frame = ttk.Frame(self.tabs)
        self.tabs.add(frame, text=title)
        text_area = scrolledtext.ScrolledText(frame, height=25, bg="black", fg="#FFD700", insertbackground="#FFD700")
        text_area.pack(expand=True, fill='both', padx=10, pady=10)
        self.update_view(text_area, filepath)
        return text_area

    def update_view(self, widget, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                widget.delete('1.0', tk.END)
                widget.insert(tk.END, f.read())
        except FileNotFoundError:
            widget.insert(tk.END, f"{filepath} not found.")

    def parse_input(self):
        content = self.editor.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No DSL input to parse.")
            return
        try:
            subprocess.run(["python", "harm_parser.py", content], check=True)
            messagebox.showinfo("Parsed", "Expression parsed and memory updated.")
            self.refresh_outputs()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_phiepsilon(self):
        content = self.editor.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No DSL input to run.")
            return
        try:
            subprocess.run(["python", "Φπε.py", "--evaluate", content], check=False)
            messagebox.showinfo("Φπε Run", "Routed to Φπε.py.")
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

    def refresh_outputs(self):
        self.update_view(self.memory_tab, "ΞΣ_MEMORY.txt")
        self.update_view(self.index_tab, "ΞΣ_Index.txt")
        self.update_view(self.tree_tab, "ΞΣ_TREE_VIEW.txt")
        self.update_view(self.response_tab, "PhiShell_response.txt")

if __name__ == "__main__":
    root = tk.Tk()
    app = HarmoniaCoder(root)
    root.mainloop()
