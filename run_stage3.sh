#!/bin/bash
python interpreter_stage3.py bitreverse_test.json dump.json 495 510
python - << 'EOF'
import json
d = json.load(open("dump.json"))
print("500:", d["500"], "-> 501:", d["501"])
print("502:", d["502"], "-> 503:", d["503"])
print("504:", d["504"], "-> 505:", d["505"])
EOF
