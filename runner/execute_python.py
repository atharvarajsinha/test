import shutil
import sys
from pathlib import Path

from runner.sandbox import run_cmd, validate_source


def _python_command():
    """Pick a working interpreter command across Linux/macOS/Windows."""
    candidates = [sys.executable, shutil.which('python3'), shutil.which('python')]
    for c in candidates:
        if c:
            return [c]
    raise RuntimeError('Python interpreter not found in PATH.')


def execute_python(code: str, workdir: Path):
    validate_source(code)
    file_path = workdir / 'program.py'
    file_path.write_text(code, encoding='utf-8')
    return run_cmd(_python_command() + [str(file_path.name)], workdir)
