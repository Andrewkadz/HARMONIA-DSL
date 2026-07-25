import os
from pathlib import Path

base = Path("RECURSOR.hrmpkg")

print("Scanning .hrm files for encoding errors...\n")
for root, dirs, files in os.walk(base):
    for file in files:
        if file.endswith(".hrm"):
            path = Path(root) / file
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    f.read()
                print(f"[✓] {path} is valid UTF-8")
            except UnicodeDecodeError as e:
                print(f"[✗] {path} has encoding issues: {e}")
