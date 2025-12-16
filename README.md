# Ассемблер УВМ (вариант 13)

## Формат: json
{
  "program": [
    {
      "opcode": "НАЗВАНИЕ",
      "fields": {"A": число, "B": число, "C": число, "D": число}
    }
  ]
}

## Использование
Этап 1
python asm.py input.json output.bin --test --text
Этап 2
python interpreter.py array_copy.json memory_dump.json 90 210

