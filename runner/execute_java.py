import re
from pathlib import Path

from runner.sandbox import run_cmd, validate_source


CLASS_RE = re.compile(r'public\s+class\s+([A-Za-z_][A-Za-z0-9_]*)')


def _class_name(code: str) -> str:
    m = CLASS_RE.search(code)
    return m.group(1) if m else 'Main'


def execute_java(code: str, workdir: Path):
    validate_source(code)
    class_name = _class_name(code)
    file_path = workdir / f'{class_name}.java'
    file_path.write_text(code, encoding='utf-8')
    compile_out = run_cmd(['javac', file_path.name], workdir)
    if compile_out:
        return compile_out
    return run_cmd(['java', class_name], workdir)
