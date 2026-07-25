#!/usr/bin/env python3
# Simple converter for `.1` universal container files.
# Reads header (before a blank line or '---'), then writes payload to the target format.

import sys
from pathlib import Path

def parse_one(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    header = {}
    payload_start = 0
    for i, line in enumerate(text):
        s = line.strip()
        if s == "" or s == "---":
            payload_start = i + 1
            break
        if ":" in line:
            k, v = line.split(":", 1)
            header[k.strip()] = v.strip()
    payload = "\n".join(text[payload_start:])
    return header, payload

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_filetypeone.py <file.1>")
        return 1
    src = Path(sys.argv[1])
    if not src.exists():
        print(f"Not found: {src}")
        return 1

    header, payload = parse_one(src)
    outfmt = header.get("OutputFormat", "txt").lower()
    ext_map = {"py":"py","hrm":"hrm","json":"json","pdf":"pdf","txt":"txt"}
    ext = ext_map.get(outfmt, outfmt)

    out = src.with_suffix("." + ext)

    # Pass-through demo; add real transforms later.
    if outfmt == "py" and not payload.lstrip().startswith(("#","\"\"\"","'")):
        payload = f"# Generated from {src.name}\n" + payload
    elif outfmt == "hrm" and not payload.lstrip().startswith(("//","#")):
        payload = f"// Generated from {src.name}\n" + payload

    out.write_text(payload, encoding="utf-8")
    print(f"Converted {src.name} -> {out.name}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
