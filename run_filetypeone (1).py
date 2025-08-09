#!/usr/bin/env python3
"""
Simple converter for `.1` universal container files.

This script reads a `.1` file, parses its header to extract the
`InputFormat` and `OutputFormat`, and then writes the payload to a
file with the appropriate extension.  It serves as a demonstration
of how the universal container can be used to bridge between HRM
scripts and Python modules.

Usage:
    python run_filetypeone.py <path/to/file.1>

For HRM→Python conversions, the payload is written directly to a
`.py` file.  For Python→HRM conversions, the payload is written to
`.hrm` file with a simple comment header.  Other input/output
formats will produce an informative error.
"""
import sys
from pathlib import Path


def parse_one(file_path: Path):
    """Parse the header and payload of a `.1` file."""
    with file_path.open('r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    header = {}
    payload_lines = []
    in_payload = False
    for line in lines:
        # The first blank line separates header and payload
        if not in_payload and line.strip() == '':
            in_payload = True
            continue
        if in_payload:
            payload_lines.append(line)
        else:
            if ':' in line:
                key, value = line.split(':', 1)
                header[key.strip()] = value.strip()
    return header, '\n'.join(payload_lines)


def convert_file(file_path: Path):
    header, payload = parse_one(file_path)
    input_format = header.get('InputFormat')
    output_format = header.get('OutputFormat')
    base_name = file_path.with_suffix('')  # remove .1 extension
    if not input_format or not output_format:
        print(f"Missing InputFormat or OutputFormat in header for {file_path}")
        return
    if input_format == 'hrm' and output_format == 'py':
        out_path = base_name.with_suffix('.py')
        with out_path.open('w', encoding='utf-8') as out:
            out.write('# Generated from {}\n'.format(file_path.name))
            out.write(payload + '\n')
        print(f"Converted {file_path.name} → {out_path.name}")
    elif input_format == 'py' and output_format == 'hrm':
        out_path = base_name.with_suffix('.hrm')
        with out_path.open('w', encoding='utf-8') as out:
            out.write('// Generated from {}\n'.format(file_path.name))
            out.write(payload + '\n')
        print(f"Converted {file_path.name} → {out_path.name}")
    else:
        print(f"Unsupported conversion: {input_format} → {output_format}")


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return
    for file_arg in argv[1:]:
        path = Path(file_arg)
        if not path.exists() or path.suffix != '.1':
            print(f"Skipping {file_arg}: not a .1 file or does not exist")
            continue
        convert_file(path)


if __name__ == '__main__':
    main(sys.argv)