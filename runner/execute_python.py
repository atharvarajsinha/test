import shutil
import subprocess
import sys
from pathlib import Path

from runner.sandbox import run_cmd, validate_source


WINDOWS_STORE_ALIAS_HINT = 'Python was not found; run without arguments to install from the Microsoft Store'


def _candidate_commands():
    """Return interpreter command candidates in priority order."""
    candidates = []

    if sys.executable:
        candidates.append([sys.executable])

    p3 = shutil.which('python3')
    if p3:
        candidates.append([p3])

    p = shutil.which('python')
    if p:
        candidates.append([p])

    # Windows launcher fallback.
    py = shutil.which('py')
    if py:
        candidates.append([py, '-3'])

    # De-duplicate while preserving order.
    seen = set()
    unique = []
    for cmd in candidates:
        key = tuple(cmd)
        if key not in seen:
            unique.append(cmd)
            seen.add(key)
    return unique


def _is_usable_interpreter(cmd):
    """Probe command and reject known unusable launcher aliases."""
    try:
        probe = subprocess.run(
            cmd + ['--version'],
            capture_output=True,
            text=True,
            timeout=2,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False

    combined = f"{probe.stdout}\n{probe.stderr}".strip()
    if WINDOWS_STORE_ALIAS_HINT in combined:
        return False

    return probe.returncode == 0 and 'Python' in combined


def _python_command():
    """Pick a working interpreter command across Linux/macOS/Windows."""
    for cmd in _candidate_commands():
        if _is_usable_interpreter(cmd):
            return cmd
    raise RuntimeError(
        'No working Python interpreter found. On Windows, disable App Execution Alias for python.exe '
        'or install Python and ensure it is on PATH.'
    )


def execute_python(code: str, workdir: Path):
    validate_source(code)
    file_path = workdir / 'program.py'
    file_path.write_text(code, encoding='utf-8')
    return run_cmd(_python_command() + [str(file_path.name)], workdir)
