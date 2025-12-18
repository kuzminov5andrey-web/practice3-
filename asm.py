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

def set_bits(value, start_bit, num_bits, byte_array):
    for i in range(num_bits):
        bit_pos = start_bit + i
        byte_idx = bit_pos // 8
        bit_in_byte = bit_pos % 8
        
        if value & (1 << i):
            byte_array[byte_idx] |= (1 << bit_in_byte)
        else:
            byte_array[byte_idx] &= ~(1 << bit_in_byte)

def encode_instruction(opcode, fields):
    result = bytearray(14)
    
    a_value = fields.get("A", 0)
    b_value = fields.get("B", 0)
    c_value = fields.get("C", 0)
    d_value = fields.get("D", 0)
    
    if opcode == "LOAD_CONST":
        set_bits(a_value, 0, 7, result)
        set_bits(b_value, 7, 28, result)
        set_bits(c_value, 35, 30, result)
        
    elif opcode == "READ_MEM":
        set_bits(a_value, 0, 7, result)
        set_bits(b_value, 7, 13, result)
        set_bits(c_value, 20, 30, result)
        set_bits(d_value, 50, 30, result)
        
    elif opcode == "WRITE_MEM":
        set_bits(a_value, 0, 7, result)
        set_bits(b_value, 7, 30, result)
        set_bits(c_value, 37, 30, result)
        set_bits(d_value, 67, 13, result)
        
    elif opcode == "BITREVERSE":
        set_bits(a_value, 0, 7, result)
        set_bits(b_value, 7, 30, result)
        set_bits(c_value, 37, 30, result)
        
    else:
        return bytes([0]*14)
    
    return bytes(result)

result_binary = bytearray()
result_text_lines = []

if test_mode:
    print("=== ПРОМЕЖУТОЧНОЕ ПРЕДСТАВЛЕНИЕ ===\n")

for idx, cmd in enumerate(commands):
    if not isinstance(cmd, dict):
        continue
    
    opcode = cmd.get("opcode", "")
    fields = cmd.get("fields", {})
    
    encoded = encode_instruction(opcode, fields)
    result_binary += encoded
    result_text_lines.append(" ".join(f"{b:02X}" for b in encoded))
    
    if test_mode:
        print(f"Команда {idx}: {opcode}")
        for key in ['A', 'B', 'C', 'D']:
            if key in fields:
                print(f"  {key}: {fields[key]}")
        
        print(f"  Байты: {' '.join(f'{b:02X}' for b in encoded)}")
        print()

if text_mode:
    output_file.write_text("\n".join(result_text_lines), encoding="utf-8")
else:
    with output_file.open("wb") as f:
        f.write(result_binary)

print(f"Файл создан: {output_file} ({len(result_binary)} байт)")
