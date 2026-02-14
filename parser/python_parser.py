from pathlib import Path
from parser.common_parser import parse_tokens_file


def parse_python(tokens_path: Path, ast_output_path: Path):
    return parse_tokens_file(tokens_path, ast_output_path)
