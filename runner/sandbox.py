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
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=5)
    out = (proc.stdout or '') + (proc.stderr or '')
    return out.strip()
