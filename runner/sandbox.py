"""Execution sandbox helpers.
This is intentionally minimal and educational.
"""
import subprocess
from pathlib import Path

BLOCKED_PATTERNS = ['import os', 'import socket', 'subprocess', 'open(', 'fstream', 'java.net']


def validate_source(code: str):
    for pattern in BLOCKED_PATTERNS:
        if pattern in code:
            raise ValueError(f'Blocked pattern detected: {pattern}')


def run_cmd(cmd, cwd: Path):
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=5)
    except FileNotFoundError:
        return f"Runtime tool not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 'Execution timed out after 5 seconds.'
    out = (proc.stdout or '') + (proc.stderr or '')
    return out.strip()
