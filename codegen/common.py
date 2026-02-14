import json
from pathlib import Path


def read_ir(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))
