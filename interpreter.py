#!/usr/bin/env python3
import json
import sys

if len(sys.argv) != 5:
    print("Использование: python interpreter.py bitreverse_test.json bitreverse_dump.json 495 510")
    sys.exit(1)

program_file = sys.argv[1]
dump_file = sys.argv[2]
start = int(sys.argv[3])
end = int(sys.argv[4])

MEM_SIZE = 10000
memory = [0] * MEM_SIZE

with open(program_file, "r", encoding="utf-8") as f:
    data = json.load(f)

program = data["program"]

def bitreverse(x):
    r = 0
    for i in range(32):
        if x & (1 << i):
            r |= 1 << (31 - i)
    return r

pc = 0
while pc < len(program):
    fields = program[pc]["fields"]
    A = fields["A"]

    if A == 100:
        memory[fields["C"]] = fields["B"]

    elif A == 110:
        addr = memory[fields["C"]] + fields["B"]
        if 0 <= addr < MEM_SIZE:
            memory[fields["D"]] = memory[addr]

    elif A == 109:
        addr = memory[fields["C"]] + fields["D"]
        if 0 <= addr < MEM_SIZE:
            memory[addr] = memory[fields["B"]]

    elif A == 77:
        memory[fields["B"]] = bitreverse(memory[fields["C"]])

    pc += 1

dump = {}
for addr in range(start, end + 1):
    if 0 <= addr < MEM_SIZE:
        dump[str(addr)] = memory[addr]

with open(dump_file, "w", encoding="utf-8") as f:
    json.dump(dump, f, indent=2)

print(f"Дамп памяти сохранён в {dump_file}")
