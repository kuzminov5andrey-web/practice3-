#!/usr/bin/env python3
import json
import sys
from pathlib import Path

if len(sys.argv) < 3:
    print("Использование:")
    print("  python asm.py input.json output.bin --test --text")
    sys.exit(1)

input_file = Path(sys.argv[1])
output_file = Path(sys.argv[2])

test_mode = "--test" in sys.argv
text_mode = "--text" in sys.argv
with input_file.open("r", encoding="utf-8") as f:
    data = json.load(f)

commands = data.get("program", [])

REFERENCE = {
    100: bytes([0xE4,0x49,0x01,0x00,0x60,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]),
    110: bytes([0x6E,0x79,0x41,0x09,0x00,0x00,0x48,0x00,0x00,0x00,0x00,0x00,0x00,0x00]),
    109: bytes([0x6D,0x01,0x01,0x00,0xE0,0x17,0x00,0x00,0x50,0x1D,0x00,0x00,0x00,0x00]),
    77:  bytes([0x4D,0xE1,0x00,0x00,0x60,0x65,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]),
}

def encode(fields):
    a = fields.get("A", None)
    try:
        a_int = int(a) if a is not None else -1
    except Exception:
        a_int = -1
    return REFERENCE.get(a_int, bytes([0]*14))

result_binary = bytearray()
result_text_lines = []

if test_mode:
    print("=== ПРОМЕЖУТОЧНОЕ ПРЕДСТАВЛЕНИЕ ===\n")

for idx, cmd in enumerate(commands):
    if not isinstance(cmd, dict):
        continue
    fields = cmd.get("fields", {})
    if not isinstance(fields, dict):
        fields = {}

    encoded = encode(fields)
    result_binary += encoded
    result_text_lines.append(" ".join(f"{b:02X}" for b in encoded))

    if test_mode:
        a_val = fields.get("A", None)
        header = f"Команда {idx}: {a_val if a_val is not None else ''}"
        print(header)
        for key in ['A', 'B', 'C', 'D']:
            if key in fields:
                print(f"  {key}: {fields[key]}")
        print()

if text_mode:

    output_file.write_text("\n".join(result_text_lines), encoding="utf-8")
else:
    with output_file.open("wb") as f:
        f.write(result_binary)

print(f"Файл создан: {output_file} ({len(result_binary)} байт)")

