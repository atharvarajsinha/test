from pathlib import Path
from runner.sandbox import run_cmd, validate_source


def execute_cpp(code: str, workdir: Path):
    validate_source(code)
    file_path = workdir / 'program.cpp'
    bin_path = workdir / 'program.out'
    file_path.write_text(code, encoding='utf-8')
    compile_out = run_cmd(['g++', file_path.name, '-o', bin_path.name], workdir)
    if compile_out:
        return compile_out
    return run_cmd([str(bin_path)], workdir)
