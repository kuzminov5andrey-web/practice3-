import json
import sys

if len(sys.argv) != 5:
    print("Использование: python interpreter.py program.json dump.json start end")
    sys.exit(1)

program_file = sys.argv[1]
dump_file = sys.argv[2]
start = int(sys.argv[3])
end = int(sys.argv[4])

MEMORY_SIZE = 10000
memory = [0] * MEMORY_SIZE

with open(program_file, 'r') as f:
    data = json.load(f)

program = data["program"]
program_start = 0

for i, cmd in enumerate(program):
    fields = cmd["fields"]
    a = fields["A"]
    
    cmd_value = a * 1000000
    if "B" in fields:
        cmd_value += fields["B"] * 1000
    if "C" in fields:
        cmd_value += fields["C"]
    
    memory[program_start + i] = cmd_value

pc = program_start

while pc < program_start + len(program):
    cmd_value = memory[pc]
    
    a = cmd_value // 1000000
    b = (cmd_value // 1000) % 1000
    c = cmd_value % 1000
    
    if a == 100:
        memory[c] = b
        print(f"LOAD_CONST: memory[{c}] = {b}")
    
    elif a == 109:
        src = b
        base_ptr = c
        dest = memory[base_ptr]
        if 0 <= src < MEMORY_SIZE and 0 <= dest < MEMORY_SIZE:
            memory[dest] = memory[src]
            print(f"WRITE_MEM: memory[{dest}] = memory[{src}]")
    
    elif a == 110:
        offset = b
        base_ptr = c
        dest = 200 + offset
        src = memory[base_ptr] + offset
        if 0 <= src < MEMORY_SIZE and 0 <= dest < MEMORY_SIZE:
            memory[dest] = memory[src]
            print(f"READ_MEM: memory[{dest}] = memory[{src}]")
    
    elif a == 77:
        print(f"BITREVERSE: пропущено")
    
    pc += 1

dump_data = {}
for addr in range(start, end + 1):
    if 0 <= addr < MEMORY_SIZE:
        dump_data[str(addr)] = memory[addr]

with open(dump_file, 'w') as f:
    json.dump(dump_data, f, indent=2)

print(f"Дамп сохранён в {dump_file}")