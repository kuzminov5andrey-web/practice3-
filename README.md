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
python asm.py input.json output.bin --test --text
