from pathlib import Path
from runner.sandbox import run_cmd, validate_source


def execute_java(code: str, workdir: Path):
    validate_source(code)
    file_path = workdir / 'Main.java'
    file_path.write_text(code, encoding='utf-8')
    compile_out = run_cmd(['javac', file_path.name], workdir)
    if compile_out:
        return compile_out
    return run_cmd(['java', 'Main'], workdir)
