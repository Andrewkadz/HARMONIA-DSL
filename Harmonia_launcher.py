"""
Harmonia Launcher GUI
======================

This script provides a simple graphical interface to explore a cloned copy of
the HARMONIA‑DSL repository.  When run from the root of the repository it
displays a tree of all files and sub‑directories, lets you load and view
`.hrm` modules, and launches core applications like the Phi‑Coder AI or the
Harmonia Coder GUI.

To use it:
1. Ensure you have Python 3 installed with Tkinter available.
2. Run `python harmonia_launcher.py` from the root of the repository.
3. Use the **Browse** button to change the directory if needed.
4. Use **Load Boot .hrm** to open any `.hrm` file in a viewer window.
5. Click **Launch Phi‑Coder AI** to start `harmonia_ai.py` in a new process.
6. Click **Launch Harmonia GUI** to start the GUI defined in `APPS/Harmonia_Coder.py`.

This launcher does not modify any repository files; it merely provides a
convenient entry point into the Harmonia environment.
"""

import os
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext


class HarmoniaLauncher(tk.Tk):
    """Main window for exploring and launching Harmonia components."""

    def __init__(self):
        super().__init__()
        self.title("Harmonia Launcher")
        self.geometry("900x600")

        # Track the directory being displayed.  Default to the current working directory.
        self.dir_path = tk.StringVar(value=os.getcwd())

        # Top frame for directory controls
        controls = tk.Frame(self)
        controls.pack(fill="x", padx=10, pady=5)

        tk.Label(controls, text="Repository Directory:").pack(side="left")
        dir_entry = tk.Entry(controls, textvariable=self.dir_path)
        dir_entry.pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(controls, text="Browse", command=self.browse_directory).pack(side="left")

        # Treeview to display the directory contents
        self.tree = ttk.Treeview(self, columns=("fullpath",), show='tree')
        self.tree.heading('#0', text='Harmonia Files', anchor='w')
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Buttons for launching scripts
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        tk.Button(btn_frame, text="Load Boot .hrm", command=self.load_hrm).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Launch Phi‑Coder AI", command=self.launch_phi_coder).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Launch Harmonia GUI", command=self.launch_harmonia_gui).pack(side="left", padx=5)

        self.populate_tree()

    def browse_directory(self) -> None:
        """Prompt the user to choose a different base directory and reload the tree."""
        selected = filedialog.askdirectory(initialdir=self.dir_path.get())
        if selected:
            self.dir_path.set(selected)
            self.populate_tree()

    def populate_tree(self) -> None:
        """Populate the tree view with the contents of the selected directory."""
        root_dir = self.dir_path.get()
        self.tree.delete(*self.tree.get_children())

        def add_nodes(parent, path):
            try:
                entries = sorted(os.listdir(path))
            except (OSError, IOError):
                return
            for entry in entries:
                full_path = os.path.join(path, entry)
                # Insert node into tree; store fullpath as hidden value in first column
                node = self.tree.insert(parent, 'end', text=entry, values=(full_path,))
                if os.path.isdir(full_path):
                    add_nodes(node, full_path)

        add_nodes('', root_dir)

    def load_hrm(self) -> None:
        """Open a .hrm file in a simple text viewer."""
        hrm_path = filedialog.askopenfilename(
            initialdir=self.dir_path.get(),
            filetypes=[("Harmonia HRM files", "*.hrm"), ("All files", "*.*")],
        )
        if not hrm_path:
            return
        try:
            with open(hrm_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")
            return

        # Display the content in a new window
        viewer = tk.Toplevel(self)
        viewer.title(os.path.basename(hrm_path))
        viewer.geometry("800x600")
        text_widget = scrolledtext.ScrolledText(viewer)
        text_widget.pack(fill="both", expand=True)
        text_widget.insert('1.0', content)
        text_widget.configure(state='disabled')

    def launch_phi_coder(self) -> None:
        """Launch the main Harmonia AI (harmonia_ai.py) in a separate process."""
        script = os.path.join(self.dir_path.get(), 'harmonia_ai.py')
        if not os.path.exists(script):
            tk.messagebox.showerror("Error", f"Cannot find harmonia_ai.py in {self.dir_path.get()}")
            return
        subprocess.Popen(["python", script], cwd=self.dir_path.get())

    def launch_harmonia_gui(self) -> None:
        """Launch the Harmonia Coder GUI (APPS/Harmonia_Coder.py)."""
        script = os.path.join(self.dir_path.get(), 'APPS', 'Harmonia_Coder.py')
        if not os.path.exists(script):
            tk.messagebox.showerror("Error", "Cannot find APPS/Harmonia_Coder.py in the selected directory")
            return
        subprocess.Popen(["python", script], cwd=self.dir_path.get())


if __name__ == '__main__':
    # Only run if this script is executed directly; create and start the GUI.
    app = HarmoniaLauncher()
    app.mainloop()
