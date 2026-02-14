from pathlib import Path
from runner.sandbox import run_cmd, validate_source


def execute_python(code: str, workdir: Path):
    validate_source(code)
    file_path = workdir / 'program.py'
    file_path.write_text(code, encoding='utf-8')
    return run_cmd(['python3', str(file_path.name)], workdir)
