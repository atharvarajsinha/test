import tempfile
from datetime import datetime
from pathlib import Path

from django.conf import settings

from lexer.python_lexer import lex_python
from lexer.java_lexer import lex_java
from lexer.cpp_lexer import lex_cpp
from parser.python_parser import parse_python
from parser.java_parser import parse_java
from parser.cpp_parser import parse_cpp
from ast.ast_builder import normalize_ast
from ir.ir_generator import ast_to_ir
from codegen.ir_to_python import generate_python
from codegen.ir_to_java import generate_java
from codegen.ir_to_cpp import generate_cpp
from runner.execute_python import execute_python
from runner.execute_java import execute_java
from runner.execute_cpp import execute_cpp

LEXERS = {'python': lex_python, 'java': lex_java, 'cpp': lex_cpp}
PARSERS = {'python': parse_python, 'java': parse_java, 'cpp': parse_cpp}
RUNNERS = {'python': execute_python, 'java': execute_java, 'cpp': execute_cpp}
CODEGEN = {'python': generate_python, 'java': generate_java, 'cpp': generate_cpp}


def _artifact_paths(stamp: str):
    base = Path(settings.ARTIFACTS_DIR) / stamp
    base.mkdir(parents=True, exist_ok=True)
    return base, base / 'tokens.json', base / 'ast.json', base / 'ir.json'


def compile_code(source_language: str, target_language: str, code: str):
    stamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    base, tokens_path, ast_path, ir_path = _artifact_paths(stamp)

    with tempfile.TemporaryDirectory() as tmpdir:
        temp = Path(tmpdir)
        original_output = RUNNERS[source_language](code, temp)

        LEXERS[source_language](code, tokens_path)
        PARSERS[source_language](tokens_path, ast_path)
        normalize_ast(ast_path)
        ast_to_ir(ast_path, ir_path)

        converted_file = base / {
            'python': 'converted.py',
            'java': 'Main.java',
            'cpp': 'converted.cpp',
        }[target_language]
        converted_code = CODEGEN[target_language](ir_path, converted_file)
        converted_output = RUNNERS[target_language](converted_code, temp)

    return {
        'tokens_file': str(tokens_path),
        'ast_file': str(ast_path),
        'ir_file': str(ir_path),
        'converted_code': converted_code,
        'original_output': original_output,
        'converted_output': converted_output,
    }


def run_code(language: str, code: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        return RUNNERS[language](code, Path(tmpdir))
